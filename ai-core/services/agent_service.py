from __future__ import annotations

from pathlib import Path

from io_utils import run_script


def validate(project_root: Path) -> tuple[bool, str]:
    result = run_script(project_root, "validate-agent-run.py", ["--project-root", str(project_root), "--check-contracts", "--check-templates"])
    return result.returncode == 0, result.stdout + result.stderr


def start(project_root: Path, requirement_rel: str, profile: str) -> tuple[bool, str]:
    result = run_script(project_root, "run-agent-workflow.py", ["--project-root", str(project_root), "--requirement", requirement_rel, "--profile", profile])
    return result.returncode == 0, result.stdout + result.stderr
