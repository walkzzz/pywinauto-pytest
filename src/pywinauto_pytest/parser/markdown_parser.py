import markdown
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from .base_parser import BaseParser
from ..models import TestSuite, TestCase, TestStep


class MarkdownParser(BaseParser):
    """Markdown 格式测试用例解析器"""
    
    def parse(self, file_path: str) -> TestSuite:
        """解析 Markdown 文件，返回 TestSuite 对象"""
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 将 Markdown 转换为 HTML，便于解析
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 解析测试套件名称（h1 标签）
        h1_tag = soup.find('h1')
        test_suite_name = h1_tag.text if h1_tag else 'Unnamed Suite'
        test_suite = TestSuite(name=test_suite_name, tests=[])
        
        # 解析测试用例（h2 标签）
        h2_tags = soup.find_all('h2')
        for h2_tag in h2_tags:
            test_case = self._parse_test_case(h2_tag)
            test_suite.tests.append(test_case)
        
        return test_suite
    
    def supports(self, file_path: str) -> bool:
        """检查是否支持 Markdown 文件"""
        ext = self._get_file_extension(file_path)
        return ext in ['md', 'markdown']
    
    def _parse_test_case(self, h2_tag) -> TestCase:
        """解析单个测试用例"""
        test_case_name = h2_tag.text.strip()
        test_case = TestCase(name=test_case_name, steps=[])
        
        steps = []
        teardown_steps = []
        
        # 使用 find_next 方法查找下一个 ol 标签，跳过中间的文本节点
        ol_tag = h2_tag.find_next('ol')
        if ol_tag:
            for li in ol_tag.find_all('li'):
                step = self._parse_step(li)
                if step:
                    steps.append(step)
        
        # 查找 Teardown 部分
        p_tag = h2_tag.find_next('p')
        while p_tag:
            if p_tag.text.strip().startswith('Teardown'):
                # 直接解析 p 标签内的 strong 标签
                strong_tags = p_tag.find_all('strong')
                for strong_tag in strong_tags:
                    if strong_tag.text == 'close_application':
                        step = TestStep(action='close_application')
                        teardown_steps.append(step)
                break
            p_tag = p_tag.find_next('p')
        
        test_case.steps = steps
        test_case.teardown = teardown_steps
        return test_case
    
    def _parse_step(self, li_tag) -> TestStep:
        """解析单个测试步骤"""
        # 从 li 标签中提取 action（strong 标签的文本）
        strong_tag = li_tag.find('strong')
        if not strong_tag:
            return None
        
        action = strong_tag.text.strip()
        
        # 提取 strong 标签后面的文本
        rest = ''
        next_sibling = strong_tag.next_sibling
        while next_sibling:
            if hasattr(next_sibling, 'text'):
                rest += next_sibling.text
            next_sibling = next_sibling.next_sibling
        
        # 移除前面的冒号和空格
        if rest.startswith(':'):
            rest = rest[1:].strip()
        
        target = None
        locator = None
        expected = None
        
        # 处理预期结果
        if ' == ' in rest:
            main_part, expected = rest.split(' == ', 1)
            expected = expected.strip()
        else:
            main_part = rest
        
        # 处理 target 和 locator
        if '(' in main_part and ')' in main_part:
            target_end = main_part.index('(')
            target = main_part[:target_end].strip()
            locator = main_part[target_end + 1:-1].strip()
        else:
            target = main_part.strip()
        
        return TestStep(
            action=action,
            target=target,
            locator=locator,
            expected=expected
        )
