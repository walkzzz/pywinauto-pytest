from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class TestStep:
    """测试步骤数据模型"""
    action: str
    target: Optional[str] = None
    locator: Optional[str] = None
    expected: Optional[str] = None
    data: Optional[Dict[str, Any]] = field(default_factory=dict)
    description: Optional[str] = None


@dataclass
class TestCase:
    """测试用例数据模型"""
    name: str
    steps: List[TestStep]
    teardown: List[TestStep] = field(default_factory=list)
    setup: List[TestStep] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class TestSuite:
    """测试套件数据模型"""
    name: str
    tests: List[TestCase]
    setup: List[TestStep] = field(default_factory=list)
    teardown: List[TestStep] = field(default_factory=list)
    description: Optional[str] = None
