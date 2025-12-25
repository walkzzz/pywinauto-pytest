import yaml
from typing import Dict, Any, List
from .base_parser import BaseParser
from ..models import TestSuite, TestCase, TestStep


class YAMLParser(BaseParser):
    """YAML 格式测试用例解析器"""
    
    def parse(self, file_path: str) -> TestSuite:
        """解析 YAML 文件，返回 TestSuite 对象"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 解析测试套件
        test_suite = TestSuite(
            name=data.get('test_suite', 'Unnamed Suite'),
            tests=[]
        )
        
        # 解析测试套件级别的 setup 和 teardown
        if 'setup' in data:
            test_suite.setup = self._parse_steps(data['setup'])
        if 'teardown' in data:
            test_suite.teardown = self._parse_steps(data['teardown'])
        
        # 解析测试用例
        for test_data in data.get('tests', []):
            test_case = TestCase(
                name=test_data.get('name', 'Unnamed Test'),
                steps=self._parse_steps(test_data.get('steps', []))
            )
            
            # 解析测试用例级别的 setup 和 teardown
            if 'setup' in test_data:
                test_case.setup = self._parse_steps(test_data['setup'])
            if 'teardown' in test_data:
                test_case.teardown = self._parse_steps(test_data['teardown'])
            
            # 解析测试标签
            if 'tags' in test_data:
                test_case.tags = test_data['tags']
            
            # 解析测试描述
            if 'description' in test_data:
                test_case.description = test_data['description']
            
            test_suite.tests.append(test_case)
        
        return test_suite
    
    def supports(self, file_path: str) -> bool:
        """检查是否支持 YAML 文件"""
        ext = self._get_file_extension(file_path)
        return ext in ['yaml', 'yml']
    
    def _parse_steps(self, steps_data: List[Dict[str, Any]]) -> List[TestStep]:
        """解析测试步骤"""
        steps = []
        for step_data in steps_data:
            step = TestStep(
                action=step_data.get('action', ''),
                target=step_data.get('target'),
                locator=step_data.get('locator'),
                expected=step_data.get('expected'),
                data=step_data.get('data', {}),
                description=step_data.get('description')
            )
            steps.append(step)
        return steps
