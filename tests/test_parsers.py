"""测试解析器功能"""
import os
import tempfile
import pytest
from pywinauto_pytest.parser import get_parser
from pywinauto_pytest.parser.yaml_parser import YAMLParser
from pywinauto_pytest.parser.json_parser import JSONParser
from pywinauto_pytest.parser.markdown_parser import MarkdownParser


class TestYAMLParser:
    """测试 YAML 解析器"""
    
    def test_supports(self):
        """测试是否支持 YAML 文件"""
        parser = YAMLParser()
        assert parser.supports("test.yaml") is True
        assert parser.supports("test.yml") is True
        assert parser.supports("test.json") is False
    
    def test_parse(self, sample_yaml_content):
        """测试解析 YAML 内容"""
        parser = YAMLParser()
        
        # 创建临时 YAML 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(sample_yaml_content)
            temp_file = f.name
        
        try:
            # 解析文件
            test_suite = parser.parse(temp_file)
            
            # 验证解析结果
            assert test_suite.name == "Sample Test Suite"
            assert len(test_suite.tests) == 1
            
            test_case = test_suite.tests[0]
            assert test_case.name == "Sample Test"
            assert len(test_case.steps) == 3
            assert len(test_case.teardown) == 1
            
            # 验证步骤
            assert test_case.steps[0].action == "start_application"
            assert test_case.steps[0].target == "calc.exe"
            
            assert test_case.steps[1].action == "click"
            assert test_case.steps[1].target == "Button"
            assert test_case.steps[1].locator == "1"
            
            assert test_case.steps[2].action == "assert_text"
            assert test_case.steps[2].target == "Edit"
            assert test_case.steps[2].expected == "1"
        finally:
            # 删除临时文件
            os.unlink(temp_file)


class TestJSONParser:
    """测试 JSON 解析器"""
    
    def test_supports(self):
        """测试是否支持 JSON 文件"""
        parser = JSONParser()
        assert parser.supports("test.json") is True
        assert parser.supports("test.yaml") is False
    
    def test_parse(self, sample_json_content):
        """测试解析 JSON 内容"""
        parser = JSONParser()
        
        # 创建临时 JSON 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(sample_json_content)
            temp_file = f.name
        
        try:
            # 解析文件
            test_suite = parser.parse(temp_file)
            
            # 验证解析结果
            assert test_suite.name == "Sample Test Suite"
            assert len(test_suite.tests) == 1
            
            test_case = test_suite.tests[0]
            assert test_case.name == "Sample Test"
            assert len(test_case.steps) == 3
            assert len(test_case.teardown) == 1
        finally:
            # 删除临时文件
            os.unlink(temp_file)


class TestMarkdownParser:
    """测试 Markdown 解析器"""
    
    def test_supports(self):
        """测试是否支持 Markdown 文件"""
        parser = MarkdownParser()
        assert parser.supports("test.md") is True
        assert parser.supports("test.markdown") is True
        assert parser.supports("test.yaml") is False
    
    def test_parse(self, sample_md_content):
        """测试解析 Markdown 内容"""
        parser = MarkdownParser()
        
        # 创建临时 Markdown 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(sample_md_content)
            temp_file = f.name
        
        try:
            # 解析文件
            test_suite = parser.parse(temp_file)
            
            # 验证解析结果
            assert test_suite.name == "Sample Test Suite"
            assert len(test_suite.tests) == 1
            
            test_case = test_suite.tests[0]
            assert test_case.name == "Sample Test"
            assert len(test_case.steps) == 3
            assert len(test_case.teardown) == 1
        finally:
            # 删除临时文件
            os.unlink(temp_file)


class TestParserRegistry:
    """测试解析器注册和获取"""
    
    def test_get_parser(self):
        """测试获取解析器"""
        assert isinstance(get_parser("test.yaml"), YAMLParser)
        assert isinstance(get_parser("test.json"), JSONParser)
        assert isinstance(get_parser("test.md"), MarkdownParser)
        assert get_parser("test.txt") is None
