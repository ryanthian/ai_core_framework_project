from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_script(project_root: Path, script: str, args: list[str]) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(project_root / "scripts" / script), *args]
    env = os.environ.copy()
    env.setdefault("AI_CORE_FRAMEWORK_ROOT", str(Path(__file__).resolve().parents[2]))
    return subprocess.run(cmd, cwd=str(project_root), text=True, capture_output=True, env=env)
