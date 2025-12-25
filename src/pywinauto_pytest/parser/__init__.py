from typing import Optional, List
from .base_parser import BaseParser
from .yaml_parser import YAMLParser
from .json_parser import JSONParser
from .excel_parser import ExcelParser
from .markdown_parser import MarkdownParser

# 注册所有解析器
PARSERS: List[BaseParser] = [
    YAMLParser(),
    JSONParser(),
    ExcelParser(),
    MarkdownParser()
]


def get_parser(file_path: str) -> Optional[BaseParser]:
    """根据文件路径获取合适的解析器"""
    for parser in PARSERS:
        if parser.supports(file_path):
            return parser
    return None


def register_parser(parser: BaseParser) -> None:
    """注册自定义解析器"""
    PARSERS.append(parser)
