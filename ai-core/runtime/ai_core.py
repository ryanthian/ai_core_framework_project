#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from controller import analyze, cancel, health, migrate_v1_to_v2, resume, run, status


def main() -> None:
    parser = argparse.ArgumentParser(description="Internal AI-Core runtime command surface.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_project(p):
        p.add_argument("--project", default=".")

    p = sub.add_parser("health")
    add_project(p)

    p = sub.add_parser("analyze")
    add_project(p)
    p.add_argument("--input", required=True)
    p.add_argument("--input-type", default="AUTO")
    p.add_argument("--profile", default="AUTO")

    p = sub.add_parser("run")
    add_project(p)
    p.add_argument("--input", required=True)
    p.add_argument("--input-type", default="AUTO")
    p.add_argument("--profile", default="AUTO")
    p.add_argument("--demo", choices=["structured", "document", "test-failure", "reviewer-loop"], default="structured")
    p.add_argument("--stop-after", default="")

    p = sub.add_parser("resume")
    add_project(p)
    p.add_argument("--run-id", required=True)
    p.add_argument("--demo", choices=["structured", "document", "test-failure", "reviewer-loop"], default="structured")

    p = sub.add_parser("cancel")
    add_project(p)
    p.add_argument("--run-id", required=True)
    p.add_argument("--reason", required=True)

    p = sub.add_parser("status")
    add_project(p)
    p.add_argument("--run-id", required=True)

    p = sub.add_parser("migrate")
    add_project(p)
    p.add_argument("--old-state", required=True)

    args = parser.parse_args()
    project = Path(args.project).resolve()

    if args.cmd == "health":
        verdict, messages = health(project)
        print(f"HEALTH {verdict}")
        print("\n".join(messages))
        raise SystemExit(0 if verdict != "FAIL" else 1)
    if args.cmd == "analyze":
        state = analyze(project, args.input, args.input_type, args.profile)
        print(json.dumps({"run_id": state["run_id"], "status": state["status"], "gate_status": state["gate_status"], "current_stage": state["current_stage"]}, indent=2, sort_keys=True))
        return
    if args.cmd == "run":
        state = run(project, args.input, args.input_type, args.profile, args.demo, args.stop_after)
        print(json.dumps({"run_id": state["run_id"], "status": state["status"], "result": state.get("result", ""), "gate_status": state["gate_status"], "current_stage": state["current_stage"]}, indent=2, sort_keys=True))
        return
    if args.cmd == "resume":
        state = resume(project, args.run_id, args.demo)
        print(json.dumps({"run_id": state["run_id"], "status": state["status"], "result": state.get("result", ""), "current_stage": state["current_stage"]}, indent=2, sort_keys=True))
        return
    if args.cmd == "cancel":
        state = cancel(project, args.run_id, args.reason)
        print(json.dumps({"run_id": state["run_id"], "status": state["status"], "reason": state["blocked_reason"]}, indent=2, sort_keys=True))
        return
    if args.cmd == "status":
        print(status(project, args.run_id))
        return
    if args.cmd == "migrate":
        print(f"MIGRATED {migrate_v1_to_v2(project, Path(args.old_state).resolve())}")
        return


if __name__ == "__main__":
    main()
