from __future__ import annotations

import re
from pathlib import Path

from io_utils import read_json, run_script


def _doc_id_from_output(output: str) -> str:
    match = re.search(r"(DOC-\d+)", output)
    if not match:
        raise RuntimeError(f"could not determine document id from output: {output}")
    return match.group(1)


def ingest(project_root: Path, file_ref: str, title: str, authority: str = "AUTHORITATIVE") -> tuple[str, str, bool]:
    result = run_script(project_root, "ingest-document.py", ["--project", str(project_root), "--file", str(project_root / file_ref), "--title", title, "--authority", authority])
    output = result.stdout + result.stderr
    if result.returncode == 2 and "DUPLICATE" in output:
        return _doc_id_from_output(output), output, True
    if result.returncode != 0:
        raise RuntimeError(output)
    return _doc_id_from_output(output), output, False


def extract(project_root: Path, document_id: str) -> str:
    result = run_script(project_root, "extract-document.py", ["--project", str(project_root), "--document-id", document_id])
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def analyze(project_root: Path, document_id: str) -> str:
    result = run_script(project_root, "analyze-document-intelligence.py", ["--project", str(project_root), "--document-id", document_id])
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def review(project_root: Path, document_id: str) -> str:
    result = run_script(project_root, "review-document-intelligence.py", ["--project", str(project_root), "--document-id", document_id, "--approve-all-safe"])
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def promote(project_root: Path, document_id: str) -> str:
    result = run_script(project_root, "promote-document-intelligence.py", ["--project", str(project_root), "--document-id", document_id, "--target", "all"])
    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout + result.stderr


def refs(project_root: Path, document_id: str) -> dict:
    base = project_root / ".ai" / "documents"
    return {
        "manifest": f".ai/documents/manifests/{document_id}.json",
        "extracted": f".ai/documents/extracted/{document_id}.json",
        "intelligence": f".ai/documents/reviews/{document_id}-intelligence.md",
        "review": f".ai/documents/reviews/{document_id}-review.json",
        "promotion": f".ai/documents/processed/{document_id}-promotion.json",
        "change_impact": f".ai/documents/processed/{document_id}-change-impact.json",
        "manifest_data": read_json(base / "manifests" / f"{document_id}.json"),
    }
