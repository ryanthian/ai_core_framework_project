from __future__ import annotations

from pathlib import Path

from .base import BaseParser
from .csv_parser import CSVParser
from .docx_parser import DOCXParser
from .html_parser import HTMLTextParser
from .json_parser import JSONParser
from .markdown_parser import MarkdownParser
from .pdf_parser import PDFParser
from .text_parser import TextParser


PARSERS: dict[str, type[BaseParser]] = {
    ".txt": TextParser,
    ".md": MarkdownParser,
    ".markdown": MarkdownParser,
    ".html": HTMLTextParser,
    ".htm": HTMLTextParser,
    ".json": JSONParser,
    ".csv": CSVParser,
    ".docx": DOCXParser,
    ".pdf": PDFParser,
}


def parser_for(path: Path) -> BaseParser:
    parser_cls = PARSERS.get(path.suffix.lower())
    if not parser_cls:
        raise ValueError(f"unsupported file type: {path.suffix}")
    return parser_cls()


def source_type_for(path: Path) -> str:
    return parser_for(path).source_type
