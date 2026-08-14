from __future__ import annotations

from pathlib import Path

from io_utils import read_json, write_json


def project_file(project_root: Path) -> Path:
    return project_root / ".ai" / "project.json"


def config_file(project_root: Path) -> Path:
    return project_root / ".ai" / "ai-core.yaml"


def ensure_project(project_root: Path, workspace_root: Path) -> dict:
    ai_root = project_root / ".ai"
    if not ai_root.exists():
        raise SystemExit(f"PROJECT_NOT_INITIALIZED: {project_root} has no .ai directory")
    for rel in ["runs", "snapshots", "human-actions"]:
        (ai_root / rel).mkdir(parents=True, exist_ok=True)
    if not project_file(project_root).exists():
        data = {
            "schema_version": "2",
            "project_id": project_root.name,
            "project_name": project_root.name,
            "project_root": str(project_root),
            "ai_root": str(ai_root),
            "repository_root": str(project_root),
            "initialized_at": "",
            "active_domain_packs": ".ai/domain-packs.yaml",
            "skills_root": str(workspace_root / "codex-skills"),
            "current_runs": [],
            "status": "ACTIVE",
        }
        write_json(project_file(project_root), data)
    else:
        data = read_json(project_file(project_root))
        changed = False
        if data.get("project_id") in {"", "ai-project-template"} and project_root.name != "ai-project-template":
            data["project_id"] = project_root.name
            changed = True
        if data.get("project_name") in {"", "AI Project Template"} and project_root.name != "ai-project-template":
            data["project_name"] = project_root.name
            changed = True
        if data.get("project_root") in {"", "."}:
            data["project_root"] = str(project_root)
            changed = True
        if data.get("repository_root") in {"", "."}:
            data["repository_root"] = str(project_root)
            changed = True
        if data.get("ai_root") in {"", ".ai"}:
            data["ai_root"] = str(ai_root)
            changed = True
        if changed:
            write_json(project_file(project_root), data)
    if not config_file(project_root).exists():
        config_file(project_root).write_text(
            "\n".join(
                [
                    "schema_version: 2",
                    "default_profile: STANDARD",
                    f"skills_root: {workspace_root / 'codex-skills'}",
                    "domain_registry: domain-packs/index.md",
                    "memory_enabled: true",
                    "document_intelligence_enabled: true",
                    "blind_spot_enabled: true",
                    "agent_harness_enabled: true",
                    "max_role_retries: 3",
                    "require_human_for_critical: true",
                    "artifact_retention: preserve",
                    "validation_mode: strict",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return read_json(project_file(project_root))


def load_project(project_root: Path) -> dict:
    if not project_file(project_root).exists():
        raise SystemExit(f"PROJECT_NOT_INITIALIZED: missing {project_file(project_root)}")
    return read_json(project_file(project_root))
