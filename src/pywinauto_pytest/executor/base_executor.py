from abc import ABC, abstractmethod
from typing import Optional
from ..models import TestStep


class BaseExecutor(ABC):
    """执行器抽象基类"""
    
    @abstractmethod
    def execute_step(self, step: TestStep) -> None:
        """执行单个测试步骤"""
        pass
    
    def setup(self) -> None:
        """执行器初始化操作"""
        pass
    
    def teardown(self) -> None:
        """执行器清理操作"""
        pass
    
    def _validate_step(self, step: TestStep) -> None:
        """验证测试步骤的有效性"""
        if not step.action:
            raise ValueError("测试步骤必须包含 action")
