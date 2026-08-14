from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from .base import BaseParser, ParsedSection, ParseResult


class DOCXParser(BaseParser):
    source_type = "DOCX"

    def parse(self, path: Path) -> ParseResult:
        sections: list[ParsedSection] = []
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
        root = ElementTree.fromstring(xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        for idx, para in enumerate(root.findall(".//w:p", ns), start=1):
            text = "".join(node.text or "" for node in para.findall(".//w:t", ns)).strip()
            if text:
                clean = re.sub(r"\s+", " ", text)
                sections.append(ParsedSection(location=f"paragraph:{idx}", text=clean))
        return ParseResult(
            parser="docx_parser",
            parser_version=self.parser_version,
            source_type=self.source_type,
            status="PARSED",
            language="unknown",
            sections=sections,
            section_count=len(sections),
        )
