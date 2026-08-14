from __future__ import annotations

import argparse
import datetime as _dt
import re
from pathlib import Path


KNOWLEDGE_CLASSES = {
    "PROJECT_FACT",
    "BUSINESS_RULE",
    "ARCHITECTURE",
    "INTEGRATION",
    "DATA_MODEL",
    "API_BEHAVIOR",
    "SECURITY_RULE",
    "UI_RULE",
    "OPERATIONAL_RULE",
    "KNOWN_PITFALL",
    "REUSABLE_PATTERN",
    "GLOSSARY",
    "CONSTRAINT",
}

CONFIDENCES = {"VERIFIED", "SUPPORTED", "UNVERIFIED", "DEPRECATED"}
KNOWLEDGE_STATUSES = {"ACTIVE", "DEPRECATED", "SUPERSEDED", "ARCHIVED"}
SOURCE_TYPES = {
    "CODE",
    "TEST",
    "REQUIREMENT",
    "DECISION",
    "DOCUMENT",
    "API_RESPONSE",
    "USER_CONFIRMED",
    "SYSTEM_OBSERVATION",
    "HANDOFF",
}
DECISION_STATUSES = {"PROPOSED", "ACCEPTED", "SUPERSEDED", "REJECTED", "REVERSED"}


def today() -> str:
    return _dt.date.today().isoformat()


def project_root(path: str | None) -> Path:
    root = Path(path or ".").resolve()
    if not (root / ".ai").exists():
        raise SystemExit(f"FAIL project root has no .ai directory: {root}")
    return root


def parse_list(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    text = value.strip()
    if not text or text == "[]":
        return []
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [part.strip().strip("\"'") for part in text.split(",") if part.strip()]


def format_list(values: list[str]) -> str:
    if not values:
        return "[]"
    return "[" + ", ".join(values) + "]"


def parse_frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            meta[f"__malformed_{len(meta)}"] = line
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta, body


def write_frontmatter(path: Path, meta: dict[str, str], body: str) -> None:
    lines = ["---"]
    for key, value in meta.items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    path.write_text("\n".join(lines) + "\n" + body.lstrip(), encoding="utf-8")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug[:60] or "entry"


def next_id(existing: list[str], prefix: str) -> str:
    max_num = 0
    for item in existing:
        match = re.fullmatch(prefix + r"-(\d+)", item)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"{prefix}-{max_num + 1:03d}"


def knowledge_files(root: Path) -> list[Path]:
    folder = root / ".ai" / "knowledge"
    return sorted(
        path
        for path in folder.glob("*.md")
        if path.name not in {"index.md", "README.md", "knowledge-capture-rule.md"}
    )


def decision_files(root: Path) -> list[Path]:
    folder = root / ".ai" / "decisions"
    return sorted(path for path in folder.glob("*.md") if path.name not in {"index.md", "README.md"})


def read_entries(paths: list[Path]) -> list[tuple[Path, dict[str, str], str]]:
    return [(path, *parse_frontmatter(path)) for path in paths]


def pipe_row(values: list[str]) -> str:
    return "| " + " | ".join(value.replace("|", "\\|") for value in values) + " |"


def update_knowledge_index(root: Path) -> None:
    rows = [
        "# Knowledge Index",
        "",
        "| ID | Title | Class | Confidence | Scope | Tags | Status | Updated |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for path, meta, _body in read_entries(knowledge_files(root)):
        rows.append(
            pipe_row(
                [
                    meta.get("id", ""),
                    meta.get("title", ""),
                    meta.get("class", ""),
                    meta.get("confidence", ""),
                    meta.get("scope", ""),
                    meta.get("tags", "[]"),
                    meta.get("status", ""),
                    meta.get("updated", ""),
                ]
            )
        )
    (root / ".ai" / "knowledge" / "index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def update_decision_index(root: Path) -> None:
    rows = [
        "# Decision Index",
        "",
        "| ID | Title | Status | Date | Scope | Related Requirement | Superseded By |",
        "|---|---|---|---|---|---|---|",
    ]
    for path, meta, _body in read_entries(decision_files(root)):
        rows.append(
            pipe_row(
                [
                    meta.get("id", ""),
                    meta.get("title", ""),
                    meta.get("status", ""),
                    meta.get("date", ""),
                    meta.get("scope", ""),
                    meta.get("related_requirement", ""),
                    meta.get("superseded_by", ""),
                ]
            )
        )
    (root / ".ai" / "decisions" / "index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def existing_ids(entries: list[tuple[Path, dict[str, str], str]]) -> list[str]:
    return [meta.get("id", "") for _path, meta, _body in entries if meta.get("id")]


def require_ref(root: Path, ref: str) -> bool:
    if not ref:
        return False
    return (root / ref).exists()


def normalize_rule_key(meta: dict[str, str], body: str) -> str:
    title = meta.get("title", "").lower()
    title = re.sub(
        r"\b(alphabetical|business-defined|business|fixed|deterministic|follow|follows|are|is|use|uses|order|ordered)\b",
        "",
        title,
    )
    title = re.sub(r"[^a-z0-9]+", " ", title).strip()
    return title


def body_section(body: str, heading: str) -> str:
    pattern = re.compile(rf"^# {re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(body)
    if not match:
        return ""
    start = match.end()
    next_match = re.search(r"^# ", body[start:], re.MULTILINE)
    end = start + next_match.start() if next_match else len(body)
    return body[start:end].strip()


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--project-root", default=".", help="Project root containing .ai")
