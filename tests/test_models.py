"""测试数据模型"""
import pytest
from pywinauto_pytest.models import TestStep, TestCase, TestSuite


class TestTestStep:
    """测试测试步骤数据模型"""
    
    def test_init(self):
        """测试初始化"""
        step = TestStep(
            action="click",
            target="Button",
            locator="1",
            expected="1",
            description="点击按钮 1"
        )
        
        assert step.action == "click"
        assert step.target == "Button"
        assert step.locator == "1"
        assert step.expected == "1"
        assert step.description == "点击按钮 1"
        assert step.data == {}
    
    def test_init_with_data(self):
        """测试带数据的初始化"""
        step = TestStep(
            action="type",
            target="Edit",
            data={"text": "test"}
        )
        
        assert step.action == "type"
        assert step.target == "Edit"
        assert step.data == {"text": "test"}
    
    def test_default_values(self):
        """测试默认值"""
        step = TestStep(action="wait")
        
        assert step.action == "wait"
        assert step.target is None
        assert step.locator is None
        assert step.expected is None
        assert step.description is None
        assert step.data == {}


class TestTestCase:
    """测试测试用例数据模型"""
    
    def test_init(self):
        """测试初始化"""
        steps = [
            TestStep(action="start_application", target="calc.exe"),
            TestStep(action="click", target="Button", locator="1")
        ]
        
        test_case = TestCase(
            name="测试用例",
            steps=steps,
            description="这是一个测试用例"
        )
        
        assert test_case.name == "测试用例"
        assert len(test_case.steps) == 2
        assert test_case.description == "这是一个测试用例"
        assert len(test_case.setup) == 0
        assert len(test_case.teardown) == 0
        assert len(test_case.tags) == 0
    
    def test_with_setup_teardown(self):
        """测试带 setup 和 teardown 的测试用例"""
        steps = [TestStep(action="click", target="Button", locator="1")]
        setup = [TestStep(action="start_application", target="calc.exe")]
        teardown = [TestStep(action="close_application")]
        tags = ["smoke", "ui"]
        
        test_case = TestCase(
            name="测试用例",
            steps=steps,
            setup=setup,
            teardown=teardown,
            tags=tags
        )
        
        assert len(test_case.setup) == 1
        assert len(test_case.teardown) == 1
        assert test_case.tags == ["smoke", "ui"]


class TestTestSuite:
    """测试测试套件数据模型"""
    
    def test_init(self):
        """测试初始化"""
        test_cases = [
            TestCase(
                name="测试用例 1",
                steps=[TestStep(action="click", target="Button", locator="1")]
            )
        ]
        
        test_suite = TestSuite(
            name="测试套件",
            tests=test_cases,
            description="这是一个测试套件"
        )
        
        assert test_suite.name == "测试套件"
        assert len(test_suite.tests) == 1
        assert test_suite.description == "这是一个测试套件"
        assert len(test_suite.setup) == 0
        assert len(test_suite.teardown) == 0
    
    def test_with_setup_teardown(self):
        """测试带 setup 和 teardown 的测试套件"""
        test_cases = [
            TestCase(
                name="测试用例 1",
                steps=[TestStep(action="click", target="Button", locator="1")]
            )
        ]
        setup = [TestStep(action="start_application", target="calc.exe")]
        teardown = [TestStep(action="close_application")]
        
        test_suite = TestSuite(
            name="测试套件",
            tests=test_cases,
            setup=setup,
            teardown=teardown
        )
        
        assert len(test_suite.setup) == 1
        assert len(test_suite.teardown) == 1
