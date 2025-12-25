import os
import time
from typing import Optional
from pywinauto import Application
from pywinauto.findwindows import find_window
from .base_executor import BaseExecutor
from ..models import TestStep
from ..logger import logger


class PywinautoExecutor(BaseExecutor):
    """基于 pywinauto 的 UI 操作执行器"""
    
    def __init__(self):
        super().__init__()
        self.app: Optional[Application] = None
        self.current_window = None
    
    def execute_step(self, step: TestStep) -> None:
        """执行单个测试步骤"""
        self._validate_step(step)
        logger.info(f"执行步骤: {step.action}, 目标: {step.target}, 定位器: {step.locator}")
        
        # 根据 action 执行不同的操作
        action_method = getattr(self, f"_action_{step.action}", None)
        if not action_method:
            raise NotImplementedError(f"不支持的操作类型: {step.action}")
        
        action_method(step)
    
    def setup(self) -> None:
        """执行器初始化操作"""
        logger.info("初始化 pywinauto 执行器")
    
    def teardown(self) -> None:
        """执行器清理操作"""
        logger.info("清理 pywinauto 执行器")
        if self.app:
            try:
                self.app.kill()
            except Exception as e:
                logger.warning(f"关闭应用程序失败: {str(e)}")
    
    def _action_start_application(self, step: TestStep) -> None:
        """启动应用程序"""
        if not step.target:
            raise ValueError("启动应用程序必须指定 target")
        
        app_path = step.target
        logger.info(f"启动应用程序: {app_path}")
        
        # 检查应用程序是否已经在运行
        try:
            self.app = Application(backend="uia").connect(path=app_path)
            logger.info(f"应用程序 {app_path} 已经在运行，直接连接")
        except:
            # 启动新的应用程序
            self.app = Application(backend="uia").start(app_path)
            logger.info(f"成功启动应用程序: {app_path}")
        
        # 获取主窗口
        self.current_window = self.app.window(title_re="*")
        self.current_window.wait('visible')
    
    def _action_close_application(self, step: TestStep) -> None:
        """关闭应用程序"""
        if self.app:
            logger.info("关闭应用程序")
            self.app.kill()
            self.app = None
            self.current_window = None
    
    def _action_click(self, step: TestStep) -> None:
        """点击操作"""
        element = self._find_element(step.target, step.locator)
        element.click()
        logger.info(f"成功点击元素: {step.target}({step.locator})")
    
    def _action_type(self, step: TestStep) -> None:
        """输入文本操作"""
        element = self._find_element(step.target, step.locator)
        text = step.data.get('text', '') if step.data else ''
        element.type_keys(text)
        logger.info(f"成功输入文本: {text} 到元素: {step.target}({step.locator})")
    
    def _action_set_text(self, step: TestStep) -> None:
        """设置文本操作"""
        element = self._find_element(step.target, step.locator)
        text = step.data.get('text', '') if step.data else ''
        element.set_text(text)
        logger.info(f"成功设置文本: {text} 到元素: {step.target}({step.locator})")
    
    def _action_assert_text(self, step: TestStep) -> None:
        """断言文本操作"""
        element = self._find_element(step.target, step.locator)
        actual_text = element.texts()[0] if element.texts() else ''
        expected_text = step.expected or ''
        
        if actual_text != expected_text:
            raise AssertionError(f"文本断言失败: 实际值 '{actual_text}', 期望值 '{expected_text}'")
        
        logger.info(f"文本断言成功: 实际值 '{actual_text}' == 期望值 '{expected_text}'")
    
    def _action_assert_exists(self, step: TestStep) -> None:
        """断言元素存在"""
        element = self._find_element(step.target, step.locator)
        if not element.exists():
            raise AssertionError(f"元素不存在: {step.target}({step.locator})")
        
        logger.info(f"元素存在断言成功: {step.target}({step.locator})")
    
    def _action_assert_not_exists(self, step: TestStep) -> None:
        """断言元素不存在"""
        try:
            element = self._find_element(step.target, step.locator)
            if element.exists():
                raise AssertionError(f"元素应该不存在，但实际存在: {step.target}({step.locator})")
        except Exception:
            # 找不到元素，断言成功
            pass
        
        logger.info(f"元素不存在断言成功: {step.target}({step.locator})")
    
    def _action_wait(self, step: TestStep) -> None:
        """等待操作"""
        wait_time = int(step.data.get('time', 1)) if step.data else 1
        logger.info(f"等待 {wait_time} 秒")
        time.sleep(wait_time)
    
    def _action_switch_window(self, step: TestStep) -> None:
        """切换窗口"""
        window_title = step.locator or ""
        logger.info(f"切换到窗口: {window_title}")
        
        if self.app:
            self.current_window = self.app.window(title_re=window_title)
            self.current_window.wait('visible')
            self.current_window.set_focus()
    
    def _find_element(self, target: Optional[str], locator: Optional[str]) -> any:
        """查找元素"""
        if not self.current_window:
            raise RuntimeError("当前没有活跃窗口，请先启动应用程序")
        
        if not target:
            raise ValueError("查找元素必须指定 target")
        
        logger.info(f"查找元素: {target}({locator})")
        
        # 根据 target 和 locator 查找元素
        if target.lower() == "window":
            return self.current_window
        
        # 使用不同的定位方式查找元素
        if locator:
            # 尝试使用标题查找
            try:
                element = self.current_window.child_window(title=locator, control_type=target)
                if element.exists():
                    return element
            except Exception as e:
                logger.debug(f"使用标题查找元素失败: {str(e)}")
            
            # 尝试使用自动化 ID 查找
            try:
                element = self.current_window.child_window(auto_id=locator, control_type=target)
                if element.exists():
                    return element
            except Exception as e:
                logger.debug(f"使用自动化 ID 查找元素失败: {str(e)}")
            
            # 尝试使用类名查找
            try:
                element = self.current_window.child_window(class_name=locator, control_type=target)
                if element.exists():
                    return element
            except Exception as e:
                logger.debug(f"使用类名查找元素失败: {str(e)}")
            
            # 尝试使用索引查找
            try:
                index = int(locator)
                elements = self.current_window.child_windows(control_type=target)
                if elements and 0 <= index < len(elements):
                    return elements[index]
            except Exception as e:
                logger.debug(f"使用索引查找元素失败: {str(e)}")
        else:
            # 只使用 control_type 查找
            try:
                element = self.current_window.child_window(control_type=target)
                if element.exists():
                    return element
            except Exception as e:
                logger.debug(f"只使用 control_type 查找元素失败: {str(e)}")
        
        raise RuntimeError(f"找不到元素: {target}({locator})")
