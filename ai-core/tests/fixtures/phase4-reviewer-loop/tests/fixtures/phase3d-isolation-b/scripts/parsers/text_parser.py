from __future__ import annotations

from pathlib import Path

from .base import BaseParser, ParsedSection, ParseResult, non_empty_lines, read_text


class TextParser(BaseParser):
    source_type = "TXT"

    def parse(self, path: Path) -> ParseResult:
        text = read_text(path)
        sections = [
            ParsedSection(location=f"line:{line_no}", text=line)
            for line_no, line in non_empty_lines(text)
        ]
        return ParseResult(
            parser="text_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
