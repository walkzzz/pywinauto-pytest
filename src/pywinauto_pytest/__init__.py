"""pywinauto-pytest 库 - 用于自动化 UI 测试的 pytest 插件"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .plugin import PywinautoTestItem, PywinautoFile
from .executor.pywinauto_executor import PywinautoExecutor
from .allure_integration import AllureIntegration
from .models import TestSuite, TestCase, TestStep

__all__ = [
    "PywinautoTestItem",
    "PywinautoFile",
    "PywinautoExecutor",
    "AllureIntegration",
    "TestSuite",
    "TestCase",
    "TestStep"
]
