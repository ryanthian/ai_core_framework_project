from __future__ import annotations

import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


DOCUMENT_STATUSES = {
    "INGESTED",
    "EXTRACTED",
    "NEEDS_REVIEW",
    "REVIEWED",
    "PARTIALLY_APPROVED",
    "APPROVED",
    "REJECTED",
    "SUPERSEDED",
    "CANCELLED",
}
AUTHORITIES = {"AUTHORITATIVE", "APPROVED", "WORKING_DRAFT", "REFERENCE", "UNVERIFIED"}
SOURCE_TYPES = {"PDF", "DOCX", "TXT", "MD", "HTML", "JSON", "CSV"}
ITEM_TYPES = {
    "REQUIREMENT",
    "BUSINESS_RULE",
    "PROJECT_FACT",
    "CONSTRAINT",
    "GLOSSARY",
    "API_CONTRACT",
    "DATA_RULE",
    "SECURITY_RULE",
    "PROCESS_STEP",
    "ACCEPTANCE_CRITERION",
    "DEPENDENCY",
    "ASSUMPTION",
    "UNKNOWN",
    "RISK",
    "DECISION_CANDIDATE",
    "ACTION_ITEM",
    "CONTACT_OR_ROLE",
    "DATE_OR_DEADLINE",
}
EXTRACTION_CONFIDENCES = {"HIGH", "MEDIUM", "LOW"}
ITEM_STATUSES = {"PROPOSED", "APPROVED", "CORRECT", "REJECTED", "NEEDS_CLARIFICATION", "DUPLICATE", "CONFLICT", "PROMOTED"}


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def project_root(path: str) -> Path:
    root = Path(path).resolve()
    if not (root / ".ai").exists():
        raise SystemExit(f"FAIL project root has no .ai directory: {root}")
    return root


def documents_dir(root: Path) -> Path:
    return root / ".ai" / "documents"


def ensure_document_dirs(root: Path) -> None:
    for rel in ["inbox", "processed", "extracted", "reviews", "manifests", "rejected", "runs"]:
        (documents_dir(root) / rel).mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_path(root: Path, document_id: str) -> Path:
    return documents_dir(root) / "manifests" / f"{document_id}.json"


def extracted_path(root: Path, document_id: str) -> Path:
    return documents_dir(root) / "extracted" / f"{document_id}.json"


def report_path(root: Path, document_id: str) -> Path:
    return documents_dir(root) / "reviews" / f"{document_id}-intelligence.md"


def review_path(root: Path, document_id: str) -> Path:
    return documents_dir(root) / "reviews" / f"{document_id}-review.json"


def doc_run_path(root: Path, document_id: str) -> Path:
    return documents_dir(root) / "runs" / f"{document_id}.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def next_document_id(root: Path) -> str:
    ids = []
    for path in (documents_dir(root) / "manifests").glob("DOC-*.json"):
        match = re.match(r"DOC-(\d+)", path.stem)
        if match:
            ids.append(int(match.group(1)))
    return f"DOC-{(max(ids) + 1) if ids else 1:03d}"


def find_by_hash(root: Path, source_hash: str) -> dict[str, Any] | None:
    for path in (documents_dir(root) / "manifests").glob("DOC-*.json"):
        manifest = load_json(path)
        if manifest.get("source_hash") == source_hash and manifest.get("status") != "SUPERSEDED":
            return manifest
    return None


def safe_copy_source(root: Path, src: Path, document_id: str) -> Path:
    target = documents_dir(root) / "inbox" / f"{document_id}{src.suffix.lower()}"
    if target.exists():
        raise SystemExit(f"FAIL managed source already exists: {target}")
    shutil.copy2(src, target)
    return target


def update_index(root: Path) -> None:
    ensure_document_dirs(root)
    rows = [
        "# Document Index",
        "",
        "| Document ID | Title | Type | Authority | Status | Extracted Items | Open Unknowns | Conflicts | Review Status | Promotion Status | Version |",
        "|---|---|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for path in sorted((documents_dir(root) / "manifests").glob("DOC-*.json")):
        manifest = load_json(path)
        document_id = manifest["document_id"]
        extracted = extracted_path(root, document_id)
        item_count = unknowns = conflicts = 0
        if extracted.exists():
            data = load_json(extracted)
            items = data.get("items", [])
            item_count = len(items)
            unknowns = sum(1 for item in items if item.get("type") == "UNKNOWN")
            conflicts = sum(1 for item in items if item.get("status") == "CONFLICT" or item.get("conflict"))
        rows.append(
            "| {document_id} | {title} | {source_type} | {authority} | {status} | {item_count} | {unknowns} | {conflicts} | {review_status} | {promotion_status} | {version} |".format(
                document_id=document_id,
                title=manifest.get("title", ""),
                source_type=manifest.get("source_type", ""),
                authority=manifest.get("authority", manifest.get("classification", "")),
                status=manifest.get("status", ""),
                item_count=item_count,
                unknowns=unknowns,
                conflicts=conflicts,
                review_status=manifest.get("review_status", ""),
                promotion_status=manifest.get("promotion_status", ""),
                version=manifest.get("version", "v1"),
            )
        )
    (documents_dir(root) / "index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def load_existing_knowledge(root: Path) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for path in (root / ".ai" / "knowledge").glob("KNOW-*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        title = ""
        kid = path.stem
        for line in text.splitlines():
            if line.startswith("id:"):
                kid = line.split(":", 1)[1].strip()
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
        records.append({"id": kid, "title": title, "path": str(path.relative_to(root)), "text": text.lower()})
    return records


def redact_sensitive(text: str) -> str:
    patterns = [
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?([A-Za-z0-9_\-./+=]{8,})",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"(?i)(postgres|mysql|mongodb)://[^\s]+",
    ]
    redacted = text
    for pattern in patterns:
        redacted = re.sub(pattern, lambda m: m.group(0).split(m.group(2))[0] + "[REDACTED]" if len(m.groups()) >= 2 else "[REDACTED_PRIVATE_KEY]", redacted)
    return redacted


def has_sensitive(text: str) -> bool:
    patterns = [
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{8,}",
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        r"(?i)(postgres|mysql|mongodb)://[^\s]+",
    ]
    return any(re.search(pattern, text) for pattern in patterns)
