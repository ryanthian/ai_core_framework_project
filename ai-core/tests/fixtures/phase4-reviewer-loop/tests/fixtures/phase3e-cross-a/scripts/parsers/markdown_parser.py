from __future__ import annotations

from pathlib import Path

from .base import BaseParser, ParsedSection, ParseResult, read_text


class MarkdownParser(BaseParser):
    source_type = "MD"

    def parse(self, path: Path) -> ParseResult:
        lines = read_text(path).splitlines()
        sections: list[ParsedSection] = []
        current_heading = "Document"
        buffer: list[str] = []
        start_line = 1

        def flush(end_line: int) -> None:
            nonlocal buffer, start_line
            text = "\n".join(line for line in buffer if line.strip()).strip()
            if text:
                sections.append(
                    ParsedSection(
                        location=f"heading:{current_heading}|lines:{start_line}-{end_line}",
                        text=text,
                        metadata={"heading": current_heading},
                    )
                )
            buffer = []

        for idx, line in enumerate(lines, start=1):
            if line.startswith("#"):
                flush(idx - 1)
                current_heading = line.lstrip("#").strip() or "Untitled"
                start_line = idx
                buffer = [line]
            else:
                if not buffer:
                    start_line = idx
                buffer.append(line)
        flush(len(lines))

        return ParseResult(
            parser="markdown_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
