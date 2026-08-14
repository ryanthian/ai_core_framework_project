from __future__ import annotations

import json
from pathlib import Path

from constants import ARTIFACT_TYPES
from events import now


def registry_path(run_dir: Path) -> Path:
    return run_dir / "artifacts.json"


def init_registry(run_dir: Path) -> dict:
    data = {"schema_version": "2", "artifacts": []}
    write_registry(run_dir, data)
    return data


def load_registry(run_dir: Path) -> dict:
    path = registry_path(run_dir)
    if not path.exists():
        return init_registry(run_dir)
    return json.loads(path.read_text(encoding="utf-8"))


def write_registry(run_dir: Path, registry: dict) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    registry_path(run_dir).write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def register_artifact(run_dir: Path, artifact_id: str, artifact_type: str, path: str, created_by_role: str = "AI_CORE", status: str = "CREATED", input_refs: list[str] | None = None, related_refs: list[str] | None = None, version: str = "v1") -> None:
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"unsupported artifact type: {artifact_type}")
    registry = load_registry(run_dir)
    existing = [item for item in registry["artifacts"] if item["artifact_id"] == artifact_id and item["version"] == version]
    if existing:
        raise ValueError(f"duplicate artifact: {artifact_id} {version}")
    registry["artifacts"].append(
        {
            "artifact_id": artifact_id,
            "type": artifact_type,
            "path": path,
            "version": version,
            "created_by_role": created_by_role,
            "created_at": now(),
            "status": status,
            "input_refs": input_refs or [],
            "related_refs": related_refs or [],
        }
    )
    write_registry(run_dir, registry)


def validate_registry(project_root: Path, run_dir: Path) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    registry = load_registry(run_dir)
    seen = set()
    for item in registry.get("artifacts", []):
        key = (item.get("artifact_id"), item.get("version"))
        if key in seen:
            failures.append(f"duplicate artifact {key}")
        seen.add(key)
        if item.get("type") not in ARTIFACT_TYPES:
            failures.append(f"invalid artifact type {item.get('type')}")
        rel = item.get("path", "")
        if rel and not (project_root / rel).exists():
            failures.append(f"missing artifact file {rel}")
    if not registry.get("artifacts"):
        warnings.append("artifact registry is empty")
    return failures, warnings
