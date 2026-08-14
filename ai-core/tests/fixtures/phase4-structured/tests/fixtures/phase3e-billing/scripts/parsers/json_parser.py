from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .base import BaseParser, ParsedSection, ParseResult, read_text


def walk(value: Any, prefix: str = "$") -> list[ParsedSection]:
    items: list[ParsedSection] = []
    if isinstance(value, dict):
        for key, child in value.items():
            items.extend(walk(child, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            items.extend(walk(child, f"{prefix}[{idx}]"))
    else:
        items.append(ParsedSection(location=f"jsonpath:{prefix}", text=str(value)))
    return items


class JSONParser(BaseParser):
    source_type = "JSON"

    def parse(self, path: Path) -> ParseResult:
        data = json.loads(read_text(path))
        sections = walk(data)
        return ParseResult(
            parser="json_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
