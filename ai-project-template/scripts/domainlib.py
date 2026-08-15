from __future__ import annotations

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any


PACK_STATUSES = {"ACTIVE", "EXPERIMENTAL", "DEPRECATED", "DISABLED"}
ITEM_TYPES = {
    "GLOSSARY",
    "BUSINESS_RULE",
    "CONSTRAINT",
    "SECURITY_RULE",
    "DATA_RULE",
    "API_RULE",
    "BLIND_SPOT_PATTERN",
    "TEST_PATTERN",
    "ARCHITECTURE_PATTERN",
    "KNOWN_PITFALL",
    "DECISION_GUIDANCE",
    "DOCUMENT_EXTRACTION_HINT",
    "VALIDATION_CHECK",
    "REUSABLE_PATTERN",
}
CONFIDENCES = {"VERIFIED", "SUPPORTED", "UNVERIFIED", "DEPRECATED"}


def today() -> str:
    return datetime.utcnow().date().isoformat()


def project_root(path: str) -> Path:
    root = Path(path).resolve()
    if not (root / ".ai").exists():
        raise SystemExit(f"FAIL project root has no .ai directory: {root}")
    return root


def workspace_root(project: Path) -> Path:
    env_root = os.environ.get("AI_CORE_FRAMEWORK_ROOT", "")
    if env_root and (Path(env_root) / "domain-packs").is_dir():
        return Path(env_root).resolve()
    cur = project.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "domain-packs").is_dir():
            return candidate
    fallback = Path(__file__).resolve().parents[2]
    if (fallback / "domain-packs").is_dir():
        return fallback
    raise SystemExit("FAIL domain-packs directory not found")


def domain_root(project: Path) -> Path:
    return workspace_root(project) / "domain-packs"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def pack_file(root: Path, pack_id: str, filename: str, version: str = "") -> Path:
    base = domain_root(root) / pack_id
    if version and (base / "versions" / version / filename).exists():
        return base / "versions" / version / filename
    return base / filename


def load_manifest(root: Path, pack_id: str, version: str = "") -> dict[str, Any]:
    path = pack_file(root, pack_id, "manifest.json", version)
    if not path.exists():
        raise SystemExit(f"FAIL pack manifest not found: {path}")
    return load_json(path)


def load_rules(root: Path, pack_id: str, version: str = "") -> list[dict[str, Any]]:
    path = pack_file(root, pack_id, "rules.json", version)
    if not path.exists():
        raise SystemExit(f"FAIL pack rules not found: {path}")
    return load_json(path).get("items", [])


def activation_file(root: Path) -> Path:
    return root / ".ai" / "domain-packs.yaml"


def parse_activation(root: Path) -> list[dict[str, str]]:
    path = activation_file(root)
    if not path.exists():
        return []
    active: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- pack:"):
            if current:
                active.append(current)
            current = {"pack": stripped.split(":", 1)[1].strip()}
        elif current and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = value.strip()
    if current:
        active.append(current)
    return active


def write_activation(root: Path, rows: list[dict[str, str]]) -> None:
    lines = ["active:"]
    if not rows:
        lines[0] = "active: []"
    else:
        for row in rows:
            lines.extend([
                f"  - pack: {row['pack']}",
                f"    version: {row['version']}",
                f"    activated_at: {row.get('activated_at', today())}",
            ])
    activation_file(root).write_text("\n".join(lines) + "\n", encoding="utf-8")


def active_packs(root: Path) -> list[dict[str, Any]]:
    rows = parse_activation(root)
    result = []
    for row in rows:
        manifest = load_manifest(root, row["pack"], row.get("version", ""))
        if manifest["version"] != row["version"]:
            result.append({"activation": row, "manifest": manifest, "version_mismatch": True})
        else:
            result.append({"activation": row, "manifest": manifest, "version_mismatch": False})
    return result


def score_terms(query: str, text: str) -> int:
    terms = [term.lower() for term in re.split(r"[^A-Za-z0-9_-]+", query) if len(term) > 2]
    lower = text.lower()
    return sum(1 for term in terms if term in lower)


def relevant_domain_rules(root: Path, query: str, limit: int = 12) -> list[tuple[int, dict[str, Any], dict[str, Any]]]:
    matches = []
    for active in active_packs(root):
        manifest = active["manifest"]
        if active["version_mismatch"] or manifest.get("status") in {"DISABLED", "DEPRECATED"}:
            continue
        for rule in load_rules(root, manifest["id"], manifest["version"]):
            haystack = " ".join([
                rule.get("id", ""),
                rule.get("title", ""),
                rule.get("type", ""),
                " ".join(rule.get("tags", [])),
                rule.get("statement", ""),
            ])
            score = score_terms(query, haystack)
            if score:
                matches.append((score, manifest, rule))
    return sorted(matches, key=lambda item: (-item[0], item[2].get("id", "")))[:limit]
