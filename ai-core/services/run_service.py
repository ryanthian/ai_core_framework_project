from __future__ import annotations

import shutil
from pathlib import Path

from artifacts import init_registry
from constants import SCHEMA_VERSION, STAGES
from events import append_event, now
from io_utils import read_json, write_json


def run_dir(project_root: Path, run_id: str) -> Path:
    return project_root / ".ai" / "runs" / run_id


def run_file(project_root: Path, run_id: str) -> Path:
    return run_dir(project_root, run_id) / "run.json"


def next_run_id(project_root: Path) -> str:
    nums = []
    for path in (project_root / ".ai" / "runs").glob("CORE-RUN-*"):
        if path.is_dir():
            try:
                nums.append(int(path.name.rsplit("-", 1)[1]))
            except ValueError:
                continue
    return f"CORE-RUN-{(max(nums) + 1) if nums else 1:03d}"


def create_run(project_root: Path, project_id: str, input_type: str, input_ref: str, profile: str) -> dict:
    rid = next_run_id(project_root)
    rdir = run_dir(project_root, rid)
    rdir.mkdir(parents=True, exist_ok=False)
    init_registry(rdir)
    state = {
        "schema_version": SCHEMA_VERSION,
        "run_id": rid,
        "project_id": project_id,
        "input_type": input_type,
        "input_ref": input_ref,
        "requirement_id": "",
        "document_id": "",
        "profile": profile,
        "status": "NEW",
        "current_stage": "INGEST" if input_type == "SOURCE_DOCUMENT" else "REQUIREMENT_ANALYSIS",
        "current_role": "",
        "started_at": now(),
        "updated_at": now(),
        "completed_stages": [],
        "skipped_stages": [],
        "blocked_reason": "",
        "human_approval": {},
        "artifact_refs": {},
        "memory_refs": [],
        "domain_refs": [],
        "skill_refs": [],
        "gate_status": {"A0": "NOT_STARTED", "A": "NOT_STARTED", "C": "NOT_STARTED", "D": "NOT_STARTED"},
        "retry_counts": {},
        "result": "",
        "errors": [],
        "human_actions": [],
        "metadata": {"duration": "", "model": "", "estimated_effort": "", "role_attempts": {}},
    }
    save_run(project_root, state)
    append_event(rdir, "RUN_CREATED", input_type=input_type, input_ref=input_ref, profile=profile)
    return state


def load_run(project_root: Path, run_id: str) -> dict:
    path = run_file(project_root, run_id)
    if not path.exists():
        raise SystemExit(f"RUN_STATE_INVALID: missing {path}")
    return read_json(path)


def save_run(project_root: Path, state: dict) -> None:
    state["updated_at"] = now()
    write_json(run_file(project_root, state["run_id"]), state)


def mark_stage(state: dict, stage: str, status: str = "COMPLETED") -> None:
    if stage not in STAGES:
        raise ValueError(f"unknown stage: {stage}")
    key = "skipped_stages" if status == "SKIPPED_NOT_APPLICABLE" else "completed_stages"
    if stage not in state[key]:
        state[key].append(stage)
    state["current_stage"] = stage


def snapshot(project_root: Path, state: dict, reason: str) -> str:
    source = run_dir(project_root, state["run_id"])
    target = project_root / ".ai" / "snapshots" / f"{state['run_id']}-{reason}-{now().replace(':', '').replace('-', '')}"
    target.mkdir(parents=True, exist_ok=False)
    for name in ["run.json", "artifacts.json", "events.jsonl", "traceability.md", "summary.md"]:
        src = source / name
        if src.exists():
            shutil.copy2(src, target / name)
    for rel in [".ai/project.json", ".ai/ai-core.yaml", ".ai/knowledge/index.md", ".ai/decisions/index.md", ".ai/documents/index.md"]:
        src = project_root / rel
        if src.exists():
            dest = target / rel.replace("/", "__")
            shutil.copy2(src, dest)
    return str(target.relative_to(project_root))
