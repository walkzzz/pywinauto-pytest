import os
import pytest
from typing import List, Optional, Type
from pytest import Collector, Item, File
from .parser import get_parser
from .models import TestSuite
from .executor.pywinauto_executor import PywinautoExecutor
from .allure_integration import AllureIntegration
from .logger import logger


class PywinautoTestItem(Item):
    """自定义测试用例项"""
    def __init__(self, name, parent, test_case):
        super().__init__(name, parent)
        self.test_case = test_case
        self.executor = PywinautoExecutor()
        self.allure = AllureIntegration()
    
    def runtest(self):
        """执行测试用例"""
        logger.info(f"开始执行测试用例: {self.test_case.name}")
        
        try:
            # 执行测试用例的 setup 步骤
            for step in self.test_case.setup:
                self.allure.start_step(step.action, step.description)
                self.executor.execute_step(step)
                self.allure.stop_step()
            
            # 执行测试用例的主要步骤
            for step in self.test_case.steps:
                self.allure.start_step(step.action, step.description)
                self.executor.execute_step(step)
                self.allure.stop_step()
            
            logger.info(f"测试用例执行成功: {self.test_case.name}")
        except Exception as e:
            self.allure.attach_screenshot("失败截图")
            logger.error(f"测试用例执行失败: {self.test_case.name}, 错误: {str(e)}")
            raise
        finally:
            # 执行测试用例的 teardown 步骤
            for step in self.test_case.teardown:
                try:
                    self.allure.start_step(step.action, "清理步骤")
                    self.executor.execute_step(step)
                    self.allure.stop_step()
                except Exception as e:
                    logger.warning(f"清理步骤执行失败: {step.action}, 错误: {str(e)}")

    def repr_failure(self, excinfo):
        """自定义失败信息"""
        return f"测试用例 '{self.test_case.name}' 执行失败: {excinfo.value}"

    def reportinfo(self):
        """报告信息"""
        return self.fspath, 0, f"测试用例: {self.test_case.name}"


class PywinautoFile(Collector):
    """自定义文件收集器"""
    def __init__(self, fspath, parent):
        super().__init__(fspath, parent)
    
    def collect(self) -> List[PywinautoTestItem]:
        """收集测试用例"""
        logger.info(f"正在收集测试用例: {self.fspath}")
        
        # 获取文件对应的解析器
        parser = get_parser(self.fspath.strpath)
        if not parser:
            logger.warning(f"不支持的文件格式: {self.fspath}")
            return []
        
        try:
            # 解析测试用例
            test_suite = parser.parse(self.fspath.strpath)
            
            # 创建测试用例项
            items = []
            for test_case in test_suite.tests:
                item = PywinautoTestItem(test_case.name, self, test_case)
                items.append(item)
            
            logger.info(f"成功收集到 {len(items)} 个测试用例")
            return items
        except Exception as e:
            logger.error(f"解析测试文件失败: {self.fspath}, 错误: {str(e)}")
            return []


@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser):
    """添加命令行选项"""
    group = parser.getgroup("pywinauto-pytest")
    group.addoption(
        "--pywinauto-file",
        action="store",
        help="指定单个 pywinauto 测试文件路径"
    )
    group.addoption(
        "--pywinauto-path",
        action="store",
        help="指定 pywinauto 测试文件目录路径"
    )


@pytest.hookimpl(trylast=True)
def pytest_collect_file(parent, path):
    """收集测试文件"""
    # 获取命令行参数
    pywinauto_file = parent.config.getoption("--pywinauto-file")
    pywinauto_path = parent.config.getoption("--pywinauto-path")
    
    # 检查是否需要处理当前文件
    if pywinauto_file:
        # 只处理指定的单个文件
        if path.strpath == pywinauto_file:
            return PywinautoFile.from_parent(parent=parent, fspath=path)
    elif pywinauto_path:
        # 处理指定目录下的所有支持的文件
        if os.path.commonpath([pywinauto_path, path.strpath]) == pywinauto_path:
            parser = get_parser(path.strpath)
            if parser:
                return PywinautoFile.from_parent(parent=parent, fspath=path)
    
    # 默认不处理
    return None
