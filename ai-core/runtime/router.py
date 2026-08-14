from __future__ import annotations

from pathlib import Path


DOCUMENT_SUFFIXES = {".pdf", ".docx", ".txt", ".md", ".html", ".json", ".csv"}


def classify_input(project_root: Path, input_ref: str, explicit: str = "AUTO") -> str:
    if explicit in {"STRUCTURED_REQUIREMENT", "SOURCE_DOCUMENT"}:
        return explicit
    path = (project_root / input_ref).resolve()
    if ".ai/requirements" in str(path) or input_ref.startswith(".ai/requirements/"):
        return "STRUCTURED_REQUIREMENT"
    if path.suffix.lower() in DOCUMENT_SUFFIXES:
        return "SOURCE_DOCUMENT"
    return "STRUCTURED_REQUIREMENT"
