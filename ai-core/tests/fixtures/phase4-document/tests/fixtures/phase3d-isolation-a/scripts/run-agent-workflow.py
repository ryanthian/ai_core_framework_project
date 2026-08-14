#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


ROLES = [
    "DOCUMENT_ANALYST",
    "DOCUMENT_REVIEWER",
    "REQUIREMENT_ANALYST",
    "MEMORY_RETRIEVER",
    "BLIND_SPOT_REVIEWER",
    "SKILL_SELECTOR",
    "PLANNER",
    "IMPLEMENTER",
    "TESTER",
    "REVIEWER",
    "VERIFIER",
    "MEMORY_CURATOR",
    "HANDOFF_WRITER",
]

PROFILES = {
    "LEAN": ["REQUIREMENT_ANALYST", "MEMORY_RETRIEVER", "BLIND_SPOT_REVIEWER", "PLANNER", "IMPLEMENTER", "TESTER", "VERIFIER"],
    "STANDARD": ROLES,
    "DEEP": ROLES,
    "DOCUMENT_STANDARD": ["DOCUMENT_ANALYST", "DOCUMENT_REVIEWER", *ROLES[2:]],
    "DOCUMENT_DEEP": ["DOCUMENT_ANALYST", "DOCUMENT_REVIEWER", *ROLES[2:]],
}

STATUSES = {"NOT_STARTED", "RUNNING", "BLOCKED", "FAILED", "COMPLETED", "CANCELLED", "AWAITING_HUMAN"}
ROLE_FILES = {
    "DOCUMENT_ANALYST": ".ai/agents/document-analyst.md",
    "DOCUMENT_REVIEWER": ".ai/agents/document-reviewer.md",
    "REQUIREMENT_ANALYST": ".ai/agents/requirement-analyst.md",
    "MEMORY_RETRIEVER": ".ai/agents/memory-retriever.md",
    "BLIND_SPOT_REVIEWER": ".ai/agents/blind-spot-reviewer.md",
    "SKILL_SELECTOR": ".ai/agents/skill-selector.md",
    "PLANNER": ".ai/agents/planner.md",
    "IMPLEMENTER": ".ai/agents/implementer.md",
    "TESTER": ".ai/agents/tester.md",
    "REVIEWER": ".ai/agents/reviewer.md",
    "VERIFIER": ".ai/agents/verifier.md",
    "MEMORY_CURATOR": ".ai/agents/memory-curator.md",
    "HANDOFF_WRITER": ".ai/agents/handoff-writer.md",
}


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def root(path: str) -> Path:
    project = Path(path).resolve()
    if not (project / ".ai").exists():
        raise SystemExit(f"FAIL project root has no .ai directory: {project}")
    return project


def requirement_id(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("id:"):
            return line.split(":", 1)[1].strip().strip("\"'")
        if "Requirement ID:" in line:
            return line.split("Requirement ID:", 1)[1].strip()
    return path.stem.split("-", 1)[0]


def state_path(project: Path, run_id: str) -> Path:
    return project / ".ai" / "runs" / f"{run_id}.json"


def events_path(project: Path, run_id: str) -> Path:
    return project / ".ai" / "runs" / f"{run_id}-events.jsonl"


def trace_path(project: Path, run_id: str) -> Path:
    return project / ".ai" / "runs" / f"{run_id}-traceability.md"


def log_event(project: Path, run_id: str, event: str, **data) -> None:
    row = {"time": now(), "event": event, **data}
    with events_path(project, run_id).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def load_state(project: Path, run_id: str) -> dict:
    path = state_path(project, run_id)
    if not path.exists():
        raise SystemExit(f"FAIL run state not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(project: Path, state: dict) -> None:
    path = state_path(project, state["run_id"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def init_run(project: Path, requirement: str, profile: str, max_role_retries: int) -> dict:
    req_path = project / requirement
    if not req_path.exists():
        raise SystemExit(f"FAIL requirement not found: {req_path}")
    rid = requirement_id(req_path)
    run_id = f"RUN-{rid}"
    if state_path(project, run_id).exists():
        raise SystemExit(f"FAIL run already exists; use --resume {run_id}: {run_id}")
    state = {
        "run_id": run_id,
        "requirement_id": rid,
        "requirement_ref": requirement,
        "project": project.name,
        "profile": profile,
        "started": now(),
        "current_role": PROFILES[profile][0],
        "completed_roles": [],
        "blocked_role": "",
        "gate_status": {"A0": "NOT_STARTED", "A": "NOT_STARTED", "C": "NOT_STARTED", "D": "NOT_STARTED"},
        "artifact_refs": {},
        "overall_status": "RUNNING",
        "role_attempts": {},
        "max_role_retries": max_role_retries,
        "loopbacks": [],
        "human_approval": {},
        "metadata": {"estimated_effort": "", "model": "", "duration": "", "role_attempts": {}},
    }
    save_state(project, state)
    log_event(project, run_id, "RUN_STARTED", role=state["current_role"], profile=profile)
    return state


def next_role(state: dict) -> str:
    sequence = PROFILES[state["profile"]]
    current = state.get("current_role")
    if current not in sequence:
        return ""
    idx = sequence.index(current)
    return sequence[idx + 1] if idx + 1 < len(sequence) else ""


def complete_role(project: Path, state: dict, role: str, artifact: str = "") -> None:
    if state["overall_status"] not in {"RUNNING", "AWAITING_HUMAN"}:
        raise SystemExit(f"FAIL cannot complete role while run is {state['overall_status']}")
    if role != state["current_role"]:
        raise SystemExit(f"FAIL current role is {state['current_role']}, not {role}")
    if role in {"SKILL_SELECTOR", "PLANNER"} and state["gate_status"].get("A0") != "PASSED":
        raise SystemExit("FAIL Gate A0 must pass before skill selection/planning can complete")
    if role == "IMPLEMENTER" and state["gate_status"].get("A") != "PASSED":
        raise SystemExit("FAIL Gate A must pass before implementation can complete")
    if role == "VERIFIER" and "TESTER" not in state["completed_roles"]:
        raise SystemExit("FAIL verifier requires test evidence first")
    if role == "VERIFIER" and state["profile"] in {"STANDARD", "DEEP"} and "REVIEWER" not in state["completed_roles"]:
        raise SystemExit("FAIL verifier requires review evidence first")
    if role == "MEMORY_CURATOR" and state["gate_status"].get("C") != "PASSED":
        raise SystemExit("FAIL Gate C must pass before memory curation")
    if artifact:
        if not (project / artifact).exists():
            raise SystemExit(f"FAIL artifact does not exist: {artifact}")
        state["artifact_refs"][role] = artifact
    if role not in state["completed_roles"]:
        state["completed_roles"].append(role)
    state["role_attempts"][role] = state["role_attempts"].get(role, 0) + 1
    log_event(project, state["run_id"], "ROLE_COMPLETED", role=role, artifact=artifact)
    upcoming = next_role(state)
    if upcoming:
        state["current_role"] = upcoming
        log_event(project, state["run_id"], "ROLE_STARTED", role=upcoming)
    else:
        state["overall_status"] = "COMPLETED"
        state["current_role"] = ""
        log_event(project, state["run_id"], "RUN_COMPLETED")
    save_state(project, state)


def set_gate(project: Path, state: dict, gate: str, status: str) -> None:
    if gate not in state["gate_status"]:
        raise SystemExit(f"FAIL unknown gate: {gate}")
    state["gate_status"][gate] = status
    event = "GATE_PASSED" if status == "PASSED" else "GATE_BLOCKED"
    log_event(project, state["run_id"], event, gate=gate, status=status)
    save_state(project, state)


def loopback(project: Path, state: dict, from_role: str, to_role: str, reason: str) -> None:
    attempts = state["role_attempts"].get(to_role, 0)
    if attempts >= state["max_role_retries"]:
        state["overall_status"] = "BLOCKED"
        state["blocked_role"] = to_role
        log_event(project, state["run_id"], "ROLE_FAILED", role=to_role, reason="max retries reached")
    else:
        state["loopbacks"].append({"from": from_role, "to": to_role, "reason": reason, "time": now()})
        state["current_role"] = to_role
        state["overall_status"] = "RUNNING"
        log_event(project, state["run_id"], "LOOPBACK", from_role=from_role, to_role=to_role, reason=reason)
    save_state(project, state)


def human(project: Path, state: dict, reason: str) -> None:
    state["overall_status"] = "AWAITING_HUMAN"
    state["human_approval"] = {"required": True, "reason": reason, "time": now()}
    log_event(project, state["run_id"], "HUMAN_APPROVAL_REQUIRED", role=state.get("current_role", ""), reason=reason)
    save_state(project, state)


def cancel(project: Path, state: dict, reason: str) -> None:
    state["overall_status"] = "CANCELLED"
    state["cancellation"] = {"reason": reason, "time": now(), "last_completed_role": state["completed_roles"][-1] if state["completed_roles"] else ""}
    log_event(project, state["run_id"], "RUN_CANCELLED", reason=reason)
    save_state(project, state)


def scaffold_prompt(project: Path, state: dict) -> None:
    role = state["current_role"]
    contract = ROLE_FILES.get(role, "")
    print(f"RUN {state['run_id']}")
    print(f"STATUS {state['overall_status']}")
    print(f"CURRENT_ROLE {role}")
    if contract:
        print(f"ROLE_CONTRACT {contract}")
    print(f"REQUIREMENT {state['requirement_ref']}")
    print("ARTIFACT_REFS")
    for key, value in sorted(state["artifact_refs"].items()):
        print(f"- {key}: {value}")
    print("NEXT_ACTION Complete the current role artifact, then call --complete-role.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--requirement")
    parser.add_argument("--profile", choices=sorted(PROFILES), default="STANDARD")
    parser.add_argument("--resume")
    parser.add_argument("--complete-role")
    parser.add_argument("--artifact", default="")
    parser.add_argument("--gate")
    parser.add_argument("--gate-status", choices=["PASSED", "BLOCKED", "FAILED"], default="PASSED")
    parser.add_argument("--loopback-from")
    parser.add_argument("--loopback-to")
    parser.add_argument("--reason", default="")
    parser.add_argument("--human-approval-required", action="store_true")
    parser.add_argument("--cancel", action="store_true")
    parser.add_argument("--max-role-retries", type=int, default=3)
    args = parser.parse_args()

    project = root(args.project_root)
    if args.resume:
        state = load_state(project, args.resume)
        log_event(project, state["run_id"], "RUN_RESUMED", role=state.get("current_role", ""))
    else:
        if not args.requirement:
            raise SystemExit("FAIL --requirement is required unless --resume is used")
        state = init_run(project, args.requirement, args.profile, args.max_role_retries)

    if args.cancel:
        cancel(project, state, args.reason or "cancelled by operator")
    elif args.human_approval_required:
        human(project, state, args.reason or "human approval required")
    elif args.loopback_from and args.loopback_to:
        loopback(project, state, args.loopback_from, args.loopback_to, args.reason or "loopback requested")
    elif args.gate:
        set_gate(project, state, args.gate, args.gate_status)
    elif args.complete_role:
        complete_role(project, state, args.complete_role, args.artifact)
    else:
        save_state(project, state)

    state = load_state(project, state["run_id"])
    scaffold_prompt(project, state)


if __name__ == "__main__":
    main()
