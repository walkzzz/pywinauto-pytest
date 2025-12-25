"""测试配置文件"""
import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_dir():
    """测试目录 fixture"""
    return Path(__file__).parent


@pytest.fixture(scope="session")
def test_data_dir(test_dir):
    """测试数据目录 fixture"""
    return test_dir / "test_data"


@pytest.fixture(scope="session")
def sample_yaml_content():
    """示例 YAML 测试用例内容"""
    return """
test_suite: Sample Test Suite
tests:
  - name: Sample Test
    steps:
      - action: start_application
        target: calc.exe
      - action: click
        target: Button
        locator: "1"
      - action: assert_text
        target: Edit
        expected: "1"
    teardown:
      - action: close_application
"""


@pytest.fixture(scope="session")
def sample_json_content():
    """示例 JSON 测试用例内容"""
    return """
{
  "test_suite": "Sample Test Suite",
  "tests": [
    {
      "name": "Sample Test",
      "steps": [
        {
          "action": "start_application",
          "target": "calc.exe"
        },
        {
          "action": "click",
          "target": "Button",
          "locator": "1"
        },
        {
          "action": "assert_text",
          "target": "Edit",
          "expected": "1"
        }
      ],
      "teardown": [
        {
          "action": "close_application"
        }
      ]
    }
  ]
}
"""


@pytest.fixture(scope="session")
def sample_md_content():
    """示例 Markdown 测试用例内容"""
    return """
# Sample Test Suite

## Sample Test
1. **start_application**: calc.exe
2. **click**: Button("1")
3. **assert_text**: Edit() == "1"

**Teardown**:
- **close_application**
"""
