import pytest
from typing import Optional
from .executor.pywinauto_executor import PywinautoExecutor
from .allure_integration import AllureIntegration


@pytest.fixture(scope="session")
def pywinauto_executor():
    """pywinauto 执行器 fixture，会话级别"""
    executor = PywinautoExecutor()
    executor.setup()
    yield executor
    executor.teardown()


@pytest.fixture(scope="function")
def app(pywinauto_executor):
    """应用程序 fixture，函数级别，自动管理应用程序的启动和关闭"""
    # 这里可以根据需要配置默认应用程序
    # 例如：pywinauto_executor._action_start_application("calc.exe")
    yield pywinauto_executor
    # 自动关闭应用程序
    pywinauto_executor._action_close_application(None)


@pytest.fixture(scope="function")
def allure_integration():
    """Allure 报告集成 fixture"""
    return AllureIntegration()


@pytest.fixture(scope="function")
def screenshot_taker(allure_integration):
    """截图工具 fixture"""
    def take_screenshot(name: str = "截图"):
        """拍摄当前屏幕截图并添加到 Allure 报告"""
        allure_integration.attach_screenshot(name)
    
    return take_screenshot


@pytest.fixture(scope="session")
def test_data_dir(request):
    """测试数据目录 fixture"""
    import os
    # 获取测试数据目录路径
    test_dir = os.path.dirname(request.module.__file__)
    data_dir = os.path.join(test_dir, "test_data")
    return data_dir
