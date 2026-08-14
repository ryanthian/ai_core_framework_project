#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROLES = [
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
ROLE_FILES = [
    ".ai/agents/requirement-analyst.md",
    ".ai/agents/memory-retriever.md",
    ".ai/agents/blind-spot-reviewer.md",
    ".ai/agents/skill-selector.md",
    ".ai/agents/planner.md",
    ".ai/agents/implementer.md",
    ".ai/agents/tester.md",
    ".ai/agents/reviewer.md",
    ".ai/agents/verifier.md",
    ".ai/agents/memory-curator.md",
    ".ai/agents/handoff-writer.md",
]
TEMPLATES = [
    ".ai/templates/requirement-analysis.md",
    ".ai/templates/skill-selection.md",
    ".ai/templates/implementation-summary.md",
    ".ai/templates/test-evidence.md",
    ".ai/templates/review-report.md",
    ".ai/templates/verification-report.md",
    ".ai/templates/handoff.md",
    ".ai/templates/run-state.json",
    ".ai/templates/traceability.md",
]
VALID_STATUSES = {"NOT_STARTED", "RUNNING", "BLOCKED", "FAILED", "COMPLETED", "CANCELLED", "AWAITING_HUMAN"}


def load_state(root: Path, run_id: str) -> dict:
    path = root / ".ai" / "runs" / f"{run_id}.json"
    if not path.exists():
        raise SystemExit(f"FAIL run state not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_file(root: Path, rel: str, label: str) -> tuple[int, int]:
    if (root / rel).exists():
        print(f"PASS {label} {rel}")
        return 1, 0
    print(f"FAIL missing {label} {rel}")
    return 0, 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--run-id")
    parser.add_argument("--check-contracts", action="store_true")
    parser.add_argument("--check-templates", action="store_true")
    parser.add_argument("--expect-status")
    parser.add_argument("--expect-profile")
    parser.add_argument("--expect-current-role")
    parser.add_argument("--require-gate")
    parser.add_argument("--require-artifact", action="append", default=[])
    parser.add_argument("--require-loopback", action="append", default=[])
    parser.add_argument("--require-event", action="append", default=[])
    parser.add_argument("--traceability")
    parser.add_argument("--expect-no-cross-project", default="")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    passes = warns = fails = 0

    if args.check_contracts:
        for rel in ROLE_FILES:
            p, f = check_file(root, rel, "role contract")
            passes += p
            fails += f
            if p and "Forbidden Actions" not in (root / rel).read_text(encoding="utf-8"):
                print(f"FAIL role contract lacks Forbidden Actions: {rel}")
                fails += 1
    if args.check_templates:
        for rel in TEMPLATES:
            p, f = check_file(root, rel, "artifact template")
            passes += p
            fails += f

    state = None
    if args.run_id:
        state = load_state(root, args.run_id)
        if state.get("overall_status") in VALID_STATUSES:
            print(f"PASS run status {state.get('overall_status')}")
            passes += 1
        else:
            print(f"FAIL invalid run status {state.get('overall_status')}")
            fails += 1
        if args.expect_status:
            if state.get("overall_status") == args.expect_status:
                print(f"PASS expected status {args.expect_status}")
                passes += 1
            else:
                print(f"FAIL expected status {args.expect_status}, got {state.get('overall_status')}")
                fails += 1
        if args.expect_profile:
            if state.get("profile") == args.expect_profile:
                print(f"PASS expected profile {args.expect_profile}")
                passes += 1
            else:
                print(f"FAIL expected profile {args.expect_profile}, got {state.get('profile')}")
                fails += 1
        if args.expect_current_role:
            if state.get("current_role") == args.expect_current_role:
                print(f"PASS expected current role {args.expect_current_role}")
                passes += 1
            else:
                print(f"FAIL expected current role {args.expect_current_role}, got {state.get('current_role')}")
                fails += 1
        if args.require_gate:
            gate, expected = args.require_gate.split("=", 1)
            actual = state.get("gate_status", {}).get(gate)
            if actual == expected:
                print(f"PASS gate {gate}={expected}")
                passes += 1
            else:
                print(f"FAIL gate {gate} expected {expected}, got {actual}")
                fails += 1
        for role in args.require_artifact:
            ref = state.get("artifact_refs", {}).get(role)
            if ref and (root / ref).exists():
                print(f"PASS artifact {role} {ref}")
                passes += 1
            else:
                print(f"FAIL missing artifact for {role}")
                fails += 1
        for role, ref in sorted(state.get("artifact_refs", {}).items()):
            if not (root / ref).exists():
                print(f"FAIL artifact ref for {role} points to missing file: {ref}")
                fails += 1
        completed = state.get("completed_roles", [])
        dependency_checks = {
            "PLANNER": ["REQUIREMENT_ANALYST", "MEMORY_RETRIEVER", "BLIND_SPOT_REVIEWER", "SKILL_SELECTOR"],
            "IMPLEMENTER": ["PLANNER"],
            "TESTER": ["IMPLEMENTER"],
            "REVIEWER": ["TESTER"],
            "VERIFIER": ["TESTER", "REVIEWER"],
            "MEMORY_CURATOR": ["VERIFIER"],
            "HANDOFF_WRITER": ["MEMORY_CURATOR"],
        }
        for role, deps in dependency_checks.items():
            if role in completed:
                missing = [dep for dep in deps if dep not in completed]
                if missing:
                    print(f"FAIL completed {role} before dependencies: {', '.join(missing)}")
                    fails += 1
        if completed:
            print("PASS role dependency ordering")
            passes += 1
        for item in args.require_loopback:
            source, target = item.split(":", 1)
            if any(loop.get("from") == source and loop.get("to") == target for loop in state.get("loopbacks", [])):
                print(f"PASS loopback {source}->{target}")
                passes += 1
            else:
                print(f"FAIL missing loopback {source}->{target}")
                fails += 1
        event_path = root / ".ai" / "runs" / f"{args.run_id}-events.jsonl"
        events = event_path.read_text(encoding="utf-8") if event_path.exists() else ""
        for event in args.require_event:
            if f'"event": "{event}"' in events:
                print(f"PASS event {event}")
                passes += 1
            else:
                print(f"FAIL missing event {event}")
                fails += 1

    if args.traceability:
        text = (root / args.traceability).read_text(encoding="utf-8")
        required = ["Acceptance Criterion", "Blind Spot", "Plan Step", "Implementation", "Test", "Review", "Verification"]
        missing = [item for item in required if item not in text]
        if missing:
            print(f"FAIL traceability missing {', '.join(missing)}")
            fails += 1
        else:
            print(f"PASS traceability {args.traceability}")
            passes += 1

    if args.expect_no_cross_project:
        needle = args.expect_no_cross_project
        combined = ""
        for path in (root / ".ai").rglob("*"):
            if path.is_file():
                combined += path.read_text(encoding="utf-8", errors="ignore")
        if needle in combined:
            print(f"FAIL cross-project leak found: {needle}")
            fails += 1
        else:
            print(f"PASS no cross-project leak: {needle}")
            passes += 1

    print(f"SUMMARY pass={passes} warn={warns} fail={fails}")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
