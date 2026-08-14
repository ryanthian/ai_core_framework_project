from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from .base import BaseParser, ParsedSection, ParseResult, read_text


class _TextHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_heading = "Document"
        self.parts: list[tuple[str, str]] = []
        self._capture_heading = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._capture_heading = tag.lower()

    def handle_endtag(self, tag: str) -> None:
        if self._capture_heading == tag.lower():
            self._capture_heading = ""

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        if self._capture_heading:
            self.current_heading = text
        else:
            self.parts.append((self.current_heading, text))


class HTMLTextParser(BaseParser):
    source_type = "HTML"

    def parse(self, path: Path) -> ParseResult:
        parser = _TextHTMLParser()
        parser.feed(read_text(path))
        sections = [
            ParsedSection(location=f"heading:{heading}|item:{idx}", text=text, metadata={"heading": heading})
            for idx, (heading, text) in enumerate(parser.parts, start=1)
        ]
        return ParseResult(
            parser="html_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
