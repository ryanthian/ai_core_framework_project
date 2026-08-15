#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd or ROOT), text=True, capture_output=True)


def record(rows: list[dict], test_id: str, command: list[str], input_desc: str, expected: str, actual: str, ok: bool) -> None:
    rows.append(
        {
            "id": test_id,
            "command": " ".join(command),
            "input": input_desc,
            "expected": expected,
            "actual": actual[:900],
            "result": "PASS" if ok else "FAIL",
        }
    )


def main() -> int:
    rows: list[dict] = []

    cmd = [PY, "codex-skills/tests/validate-skills.py", "codex-skills"]
    r = run(cmd)
    record(rows, "REG-001", cmd, "Phase 1 skills", "skill validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    workflow_files = [
        ROOT / "ai-project-template" / "docs" / "ai-project-workflow.md",
        ROOT / "AGENTS.md",
    ]
    actual = "\n".join(str(path.relative_to(ROOT)) for path in workflow_files if path.exists())
    ok = all(path.exists() for path in workflow_files) and "MEMORY RETRIEVAL" in (ROOT / "ai-project-template" / "docs" / "ai-project-workflow.md").read_text(encoding="utf-8")
    record(rows, "REG-002", ["inspect", "workflow docs"], "Phase 2 workflow", "workflow docs exist and include memory retrieval", actual, ok)

    cmd = [PY, "scripts/validate-memory.py", "--project-root", "tests/fixtures/phase3a-memory-demo"]
    r = run(cmd, ROOT / "ai-project-template")
    record(rows, "REG-003", cmd, "Phase 3A memory fixture", "memory validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    cmd = [
        PY,
        "scripts/validate-blind-spots.py",
        "--project-root",
        "tests/fixtures/phase3b-blindspot-demo",
        "--report",
        ".ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md",
    ]
    r = run(cmd, ROOT / "ai-project-template")
    record(rows, "REG-004", cmd, "Phase 3B blind spot fixture", "blind spot validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    cmd = [PY, "scripts/validate-agent-run.py", "--project-root", ".", "--check-contracts", "--check-templates"]
    r = run(cmd, ROOT / "ai-project-template")
    record(rows, "REG-005", cmd, "Phase 3C agent harness fixture", "agent validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    cmd = [
        PY,
        "scripts/validate-document-intelligence.py",
        "--project",
        "tests/fixtures/phase3d-doc-intel",
        "--document-id",
        "DOC-001",
        "--require-item-type",
        "REQUIREMENT",
        "--require-item-type",
        "BUSINESS_RULE",
        "--require-reviewed",
        "--require-promoted",
        "--require-index",
    ]
    r = run(cmd, ROOT / "ai-project-template")
    record(rows, "REG-006", cmd, "Phase 3D document fixture", "document validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    cmd = [PY, "scripts/validate-domain-pack.py", "--project", "tests/fixtures/phase3e-access", "--check-activation"]
    r = run(cmd, ROOT / "ai-project-template")
    record(rows, "REG-007", cmd, "Phase 3E domain pack fixture", "domain validator exits 0", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    cmd = [PY, "ai-core/tests/run-core-tests.py"]
    r = run(cmd)
    record(rows, "REG-008", cmd, "Phase 4 AI-Core runtime", "core integration tests pass", r.stdout + r.stderr, r.returncode == 0 and "fail=0" in r.stdout)

    failed = sum(1 for row in rows if row["result"] != "PASS")
    lines = ["# Phase 5 Regression Tests", ""]
    for row in rows:
        lines.extend(
            [
                f"## {row['id']}",
                "",
                f"Command: `{row['command']}`",
                f"Input: {row['input']}",
                f"Expected: {row['expected']}",
                f"Actual: {row['actual']}",
                f"Result: {row['result']}",
                "",
            ]
        )
    out = ROOT / "ai-core" / "tests" / "regression-tests.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"SUMMARY pass={len(rows) - failed} fail={failed}")
    print(f"WROTE {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
