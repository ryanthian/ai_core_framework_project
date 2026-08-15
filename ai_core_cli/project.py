from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


FRAMEWORK_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = FRAMEWORK_ROOT / "ai-core" / "runtime"
SERVICES_ROOT = FRAMEWORK_ROOT / "ai-core" / "services"
TEMPLATE_ROOT = FRAMEWORK_ROOT / "ai-project-template"

for path in [RUNTIME_ROOT, SERVICES_ROOT]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def resolve_project(path: str | None = None, require: bool = True) -> Path:
    start = Path(path or os.getcwd()).resolve()
    if start.is_file():
        start = start.parent
    for candidate in [start, *start.parents]:
        if (candidate / ".ai" / "project.json").exists():
            return candidate
        if (candidate / ".ai").exists() and not require:
            return candidate
    if require:
        raise ProjectNotFound(start)
    return start


class ProjectNotFound(Exception):
    def __init__(self, start: Path):
        super().__init__(f"AI-Core project not found from {start}")
        self.start = start


def git_info(project: Path) -> dict:
    def run(args: list[str]) -> str:
        result = subprocess.run(["git", *args], cwd=str(project), text=True, capture_output=True)
        return result.stdout.strip() if result.returncode == 0 else ""

    inside = run(["rev-parse", "--is-inside-work-tree"]) == "true"
    if not inside:
        return {"repository": False}
    status = run(["status", "--short"])
    return {
        "repository": True,
        "branch": run(["branch", "--show-current"]) or "(detached)",
        "commit": run(["rev-parse", "--short", "HEAD"]),
        "dirty": bool(status),
    }


def framework_git_info() -> dict:
    return git_info(FRAMEWORK_ROOT)


def run_subprocess(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=str(cwd or FRAMEWORK_ROOT), text=True, capture_output=True)
