from __future__ import annotations

from pathlib import Path

from io_utils import run_script


def retrieve(project_root: Path, project: str, query: str, output_rel: str) -> tuple[bool, str]:
    result = run_script(project_root, "retrieve-memory.py", ["--project-root", str(project_root), "--project", project, "--query", query, "--output", output_rel])
    return result.returncode == 0, result.stdout + result.stderr


def validate(project_root: Path) -> tuple[bool, str]:
    result = run_script(project_root, "validate-memory.py", ["--project-root", str(project_root)])
    return result.returncode == 0, result.stdout + result.stderr
