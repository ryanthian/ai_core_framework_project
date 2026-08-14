from __future__ import annotations

from pathlib import Path

from .base import BaseParser, ParsedSection, ParseResult


class PDFParser(BaseParser):
    source_type = "PDF"

    def parse(self, path: Path) -> ParseResult:
        warnings: list[str] = []
        sections: list[ParsedSection] = []
        page_count = 0
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception:
            return ParseResult(
                parser="pdf_parser",
                parser_version=self.parser_version,
                source_type=self.source_type,
                status="UNSUPPORTED_PARSER_MISSING",
                language="unknown",
                sections=[],
                warnings=["pypdf is not installed; PDF text extraction unavailable"],
            )
        reader = PdfReader(str(path))
        page_count = len(reader.pages)
        for idx, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                sections.append(ParsedSection(location=f"page:{idx}", text=text[:4000]))
        status = "PARSED" if sections else "OCR_REQUIRED"
        if not sections:
            warnings.append("No extractable PDF text found; OCR is required")
        return ParseResult(
            parser="pdf_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status=status,
            language="unknown",
            sections=sections,
            warnings=warnings,
            page_count=page_count,
            section_count=len(sections),
        )
