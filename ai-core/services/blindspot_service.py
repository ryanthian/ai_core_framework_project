from __future__ import annotations

from pathlib import Path

from io_utils import run_script


def run(project_root: Path, project: str, requirement_rel: str, memory_rel: str, output_rel: str, mode: str) -> tuple[bool, str]:
    result = run_script(
        project_root,
        "run-blind-spot-pass.py",
        ["--project-root", str(project_root), "--project", project, "--requirement", requirement_rel, "--memory-brief", memory_rel, "--mode", mode, "--output", output_rel],
    )
    return result.returncode == 0, result.stdout + result.stderr


def verdict(project_root: Path, report_rel: str) -> tuple[str, int, int]:
    text = (project_root / report_rel).read_text(encoding="utf-8")
    v = "UNKNOWN"
    for line in text.splitlines():
        if line.strip() in {"READY_FOR_PLAN", "READY_WITH_ACCEPTED_RISK", "BLOCKED"}:
            v = line.strip()
    critical_open = text.count("- Severity: CRITICAL\n- Status: OPEN")
    high_open = text.count("- Severity: HIGH\n- Status: OPEN")
    return v, critical_open, high_open
