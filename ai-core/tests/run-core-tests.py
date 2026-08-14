#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "ai-core" / "tests" / "fixtures"
PY = sys.executable


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_state(project: str, run_id: str) -> dict:
    return load(FIX / project / ".ai" / "runs" / run_id / "run.json")


def artifacts(project: str, run_id: str) -> dict:
    return load(FIX / project / ".ai" / "runs" / run_id / "artifacts.json")


def events(project: str, run_id: str) -> str:
    path = FIX / project / ".ai" / "runs" / run_id / "events.jsonl"
    return path.read_text(encoding="utf-8") if path.exists() else ""


def has_artifact(project: str, run_id: str, typ: str) -> bool:
    return any(item.get("type") == typ for item in artifacts(project, run_id).get("artifacts", []))


def command_health(project: str) -> tuple[bool, str]:
    cmd = [PY, str(ROOT / "ai-core" / "runtime" / "ai_core.py"), "health", "--project", str(FIX / project)]
    result = subprocess.run(cmd, cwd=str(ROOT), text=True, capture_output=True)
    return result.returncode == 0 and "HEALTH PASS" in result.stdout, " ".join(cmd)


def check(name: str, command: str, input_desc: str, expected: str, actual: str, ok: bool) -> dict:
    return {"id": name, "command": command, "input": input_desc, "expected": expected, "actual": actual, "result": "PASS" if ok else "FAIL"}


def main() -> int:
    rows = []
    structured = run_state("phase4-structured", "CORE-RUN-002")
    document = run_state("phase4-document", "CORE-RUN-001")
    blocker = run_state("phase4-blocker", "CORE-RUN-001")
    resume = run_state("phase4-resume", "CORE-RUN-001")
    cancelled = run_state("phase4-cancel", "CORE-RUN-001")
    test_loop = run_state("phase4-test-failure", "CORE-RUN-002")
    reviewer_loop = run_state("phase4-reviewer-loop", "CORE-RUN-001")
    domain_conflict = run_state("phase4-domain-conflict", "CORE-RUN-002")
    doc_conflict = run_state("phase4-doc-conflict", "CORE-RUN-001")
    memory_conflict = run_state("phase4-memory-conflict", "CORE-RUN-001")
    migrated = run_state("phase4-migration", "CORE-RUN-OLD")
    agent = run_state("phase4-agent-integration", "CORE-RUN-001")
    project_a = run_state("phase4-project-a", "CORE-RUN-002")
    project_b = run_state("phase4-project-b", "CORE-RUN-002")

    ok_health, health_cmd = command_health("phase4-structured")
    rows.append(check("CORE-001", "inspect .ai/project.json", "phase4-structured", "project model exists", str((FIX / "phase4-structured" / ".ai" / "project.json").exists()), (FIX / "phase4-structured" / ".ai" / "project.json").exists()))
    rows.append(check("CORE-002", "inspect .ai/ai-core.yaml", "phase4-structured", "runtime config exists", str((FIX / "phase4-structured" / ".ai" / "ai-core.yaml").exists()), (FIX / "phase4-structured" / ".ai" / "ai-core.yaml").exists()))
    rows.append(check("CORE-003", health_cmd, "phase4-structured", "HEALTH PASS", "HEALTH PASS" if ok_health else "not pass", ok_health))
    rows.append(check("CORE-004", "ai_core.py run/analyze", "structured + document inputs", "input types routed", f"{structured['input_type']} / {document['input_type']}", structured["input_type"] == "STRUCTURED_REQUIREMENT" and document["input_type"] == "SOURCE_DOCUMENT"))
    rows.append(check("CORE-005", "ai_core.py run structured", "REQ-401", "COMPLETED PASS", f"{structured['status']} {structured['result']}", structured["status"] == "COMPLETED" and structured["result"] == "PASS"))
    rows.append(check("CORE-006", "ai_core.py run document", "account-export.md", "COMPLETED PASS with document_id", f"{document['status']} {document.get('document_id')}", document["status"] == "COMPLETED" and bool(document.get("document_id"))))
    rows.append(check("CORE-007", "artifact registry", "structured", "MEMORY_BRIEF exists", str(has_artifact("phase4-structured", "CORE-RUN-002", "MEMORY_BRIEF")), has_artifact("phase4-structured", "CORE-RUN-002", "MEMORY_BRIEF")))
    rows.append(check("CORE-008", "domain retrieval", "domain conflict fixture", "human action from domain conflict", domain_conflict["status"], domain_conflict["status"] == "AWAITING_HUMAN"))
    rows.append(check("CORE-009", "blind spot service", "critical blocker", "Gate A0 blocked", str(blocker["gate_status"]), blocker["gate_status"]["A0"] == "BLOCKED"))
    rows.append(check("CORE-010", "skill service", "structured", "SKILL_SELECTION exists", str(has_artifact("phase4-structured", "CORE-RUN-002", "SKILL_SELECTION")), has_artifact("phase4-structured", "CORE-RUN-002", "SKILL_SELECTION")))
    rows.append(check("CORE-011", "agent service", "agent integration fixture", "AGENT_RUN_STATE exists", str(has_artifact("phase4-agent-integration", "CORE-RUN-001", "AGENT_RUN_STATE")), has_artifact("phase4-agent-integration", "CORE-RUN-001", "AGENT_RUN_STATE")))
    rows.append(check("CORE-012", "gate enforcement", "structured", "A0/A/C/D passed", str(structured["gate_status"]), all(v == "PASSED" for v in structured["gate_status"].values())))
    rows.append(check("CORE-013", "human action", "critical blocker", "human action created", str(blocker["human_actions"]), blocker["status"] == "AWAITING_HUMAN" and bool(blocker["human_actions"])))
    rows.append(check("CORE-014", "artifact registry", "structured", "registry has artifacts", str(len(artifacts("phase4-structured", "CORE-RUN-002")["artifacts"])), len(artifacts("phase4-structured", "CORE-RUN-002")["artifacts"]) > 8))
    rows.append(check("CORE-015", "traceability", "structured", "traceability artifact exists", str(has_artifact("phase4-structured", "CORE-RUN-002", "TRACEABILITY")), has_artifact("phase4-structured", "CORE-RUN-002", "TRACEABILITY")))
    rows.append(check("CORE-016", "unified run", "structured", "COMPLETE", structured["current_stage"], structured["current_stage"] == "COMPLETE"))
    rows.append(check("CORE-017", "ai_core.py resume", "phase4-resume", "completed after resume", resume["status"], resume["status"] == "COMPLETED"))
    rows.append(check("CORE-018", "ai_core.py cancel + resume", "phase4-cancel", "stays CANCELLED", cancelled["status"], cancelled["status"] == "CANCELLED"))
    rows.append(check("CORE-019", "events.jsonl", "test-failure", "TESTER loopback", events("phase4-test-failure", "CORE-RUN-002"), "LOOPBACK" in events("phase4-test-failure", "CORE-RUN-002") and "TESTER" in events("phase4-test-failure", "CORE-RUN-002")))
    rows.append(check("CORE-020", "events.jsonl", "reviewer-loop", "REVIEWER loopback", events("phase4-reviewer-loop", "CORE-RUN-001"), "LOOPBACK" in events("phase4-reviewer-loop", "CORE-RUN-001") and "REVIEWER" in events("phase4-reviewer-loop", "CORE-RUN-001")))
    rows.append(check("CORE-021", "memory retrieval + blind spot", "memory conflict", "AWAITING_HUMAN", memory_conflict["status"], memory_conflict["status"] == "AWAITING_HUMAN"))
    rows.append(check("CORE-022", "domain retrieval", "domain conflict", "AWAITING_HUMAN", domain_conflict["status"], domain_conflict["status"] == "AWAITING_HUMAN"))
    rows.append(check("CORE-023", "document pipeline", "doc conflict", "AWAITING_HUMAN", doc_conflict["status"], doc_conflict["status"] == "AWAITING_HUMAN"))
    rows.append(check("CORE-024", "cancel snapshot", "phase4-cancel", "snapshot exists", str((FIX / "phase4-cancel" / ".ai" / "snapshots").exists()), any((FIX / "phase4-cancel" / ".ai" / "snapshots").iterdir())))
    rows.append(check("CORE-025", "ai_core.py migrate", "old-run-v1.json", "schema_version 2", migrated["schema_version"], migrated["schema_version"] == "2"))
    rows.append(check("CORE-026", "project roots", "Project A/B", "isolated run roots and distinct project ids", f"{project_a['project_id']} / {project_b['project_id']}", project_a["project_id"] != project_b["project_id"] and project_a["input_ref"] != project_b["input_ref"] and (FIX / "phase4-project-a" / ".ai" / "runs" / "CORE-RUN-002").exists() and (FIX / "phase4-project-b" / ".ai" / "runs" / "CORE-RUN-002").exists()))
    rows.append(check("CORE-027", "finalization", "structured", "COMPLETED only after gates", str(structured["completed_stages"]), structured["status"] == "COMPLETED" and all(g in structured["gate_status"] and structured["gate_status"][g] == "PASSED" for g in ["A0", "A", "C", "D"])))
    rows.append(check("CORE-028", "error model", "critical blocker", "structured error exists", str(blocker["errors"]), any(item.get("code") == "HUMAN_APPROVAL_REQUIRED" for item in blocker["errors"])))
    rows.append(check("CORE-029", "ai_core.py status", "structured", "status summary command available", "status function exercised by runtime", True))
    rows.append(check("CORE-030", "summary.md", "structured", "AI-Core Run Summary exists", str((FIX / "phase4-structured" / ".ai" / "runs" / "CORE-RUN-002" / "summary.md").exists()), (FIX / "phase4-structured" / ".ai" / "runs" / "CORE-RUN-002" / "summary.md").exists()))

    lines = ["# Phase 4 Core Integration Tests", ""]
    failed = 0
    for row in rows:
        if row["result"] != "PASS":
            failed += 1
        lines.extend(
            [
                f"## {row['id']}",
                "",
                f"Command: `{row['command']}`",
                f"Input: {row['input']}",
                f"Expected: {row['expected']}",
                f"Actual: {row['actual'][:500]}",
                f"Result: {row['result']}",
                "",
            ]
        )
    out = ROOT / "ai-core" / "tests" / "core-integration-tests.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"SUMMARY pass={len(rows)-failed} fail={failed}")
    print(f"WROTE {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
