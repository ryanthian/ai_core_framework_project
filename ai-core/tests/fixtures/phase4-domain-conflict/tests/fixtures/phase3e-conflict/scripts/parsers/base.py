from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ParsedSection:
    location: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ParseResult:
    parser: str
    parser_version: str
    source_type: str
    status: str
    language: str
    sections: list[ParsedSection]
    warnings: list[str] = field(default_factory=list)
    page_count: int = 0
    section_count: int = 0


class ParserError(Exception):
    pass


class BaseParser:
    source_type = "UNKNOWN"
    parser_version = "1.0"

    def parse(self, path: Path) -> ParseResult:
        raise NotImplementedError


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def non_empty_lines(text: str) -> list[tuple[int, str]]:
    return [(idx, line.rstrip()) for idx, line in enumerate(text.splitlines(), start=1) if line.strip()]
