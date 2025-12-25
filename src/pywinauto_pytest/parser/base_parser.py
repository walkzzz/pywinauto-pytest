from abc import ABC, abstractmethod
from typing import Optional
from ..models import TestSuite


class BaseParser(ABC):
    """解析器抽象基类"""
    
    @abstractmethod
    def parse(self, file_path: str) -> TestSuite:
        """解析测试文件，返回 TestSuite 对象"""
        pass
    
    @abstractmethod
    def supports(self, file_path: str) -> bool:
        """检查是否支持该文件格式"""
        pass
    
    def _get_file_extension(self, file_path: str) -> str:
        """获取文件扩展名"""
        return file_path.split('.')[-1].lower()
