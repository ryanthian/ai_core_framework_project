from __future__ import annotations

import csv
from pathlib import Path

from .base import BaseParser, ParsedSection, ParseResult


class CSVParser(BaseParser):
    source_type = "CSV"

    def parse(self, path: Path) -> ParseResult:
        sections: list[ParsedSection] = []
        with path.open(newline="", encoding="utf-8", errors="replace") as handle:
            reader = csv.DictReader(handle)
            for row_idx, row in enumerate(reader, start=2):
                for col, value in row.items():
                    if value and value.strip():
                        sections.append(
                            ParsedSection(
                                location=f"csv:{path.name}|row:{row_idx}|column:{col}",
                                text=value.strip(),
                                metadata={"row": row_idx, "column": col},
                            )
                        )
        return ParseResult(
            parser="csv_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
