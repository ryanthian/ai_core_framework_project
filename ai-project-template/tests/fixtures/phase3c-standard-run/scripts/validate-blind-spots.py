#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from memorylib import add_common_args, parse_frontmatter, project_root
from run_blind_spot_constants import CATEGORIES, SEVERITIES, STATUSES


VERDICTS = {"READY_FOR_PLAN", "BLOCKED", "READY_WITH_ACCEPTED_RISK"}
MODES = {"QUICK", "STANDARD", "DEEP"}


def field(block: str, name: str) -> str:
    match = re.search(rf"^- {re.escape(name)}:\s*(.*)$", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def sections(text: str, prefix: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(rf"^## ({prefix}-\d+)\s*$", text, re.MULTILINE))
    result = []
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        result.append((match.group(1), text[match.end() : end]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    parser.add_argument("--report", required=True)
    parser.add_argument("--plan", default="")
    parser.add_argument("--verification", default="")
    args = parser.parse_args()

    root = project_root(args.project_root)
    report = root / args.report
    if not report.exists():
        raise SystemExit(f"FAIL report not found: {report}")
    meta, body = parse_frontmatter(report)
    fails = warns = passes = 0

    for key in ["id", "requirement", "project", "created", "memory_brief", "mode", "status", "overall_risk"]:
        if not meta.get(key):
            print(f"FAIL missing metadata {key}")
            fails += 1
    if meta.get("mode") and meta["mode"] not in MODES:
        print(f"FAIL invalid mode {meta['mode']}")
        fails += 1
    req = meta.get("requirement", "")
    if req and not (root / req).exists():
        print(f"FAIL requirement reference does not exist: {req}")
        fails += 1

    bs_blocks = sections(body, "BS")
    seen = set()
    open_critical = []
    high_open = []
    required_traces = []
    for bsid, block in bs_blocks:
        if bsid in seen:
            print(f"FAIL duplicate blind spot id {bsid}")
            fails += 1
        seen.add(bsid)
        category = field(block, "Category")
        severity = field(block, "Severity")
        status = field(block, "Status")
        if category not in CATEGORIES:
            print(f"FAIL {bsid} invalid category {category}")
            fails += 1
        if severity not in SEVERITIES:
            print(f"FAIL {bsid} invalid severity {severity}")
            fails += 1
        if status not in STATUSES:
            print(f"FAIL {bsid} invalid status {status}")
            fails += 1
        if severity == "CRITICAL" and status == "OPEN":
            open_critical.append(bsid)
        if severity == "HIGH" and status == "OPEN":
            high_open.append(bsid)
        if status == "ACCEPTED_RISK" and not field(block, "Accepted Risk Justification"):
            print(f"FAIL {bsid} accepted risk lacks justification")
            fails += 1
        if severity in {"HIGH", "MEDIUM"} and status in {"RESOLVED", "ACCEPTED_RISK"}:
            required_traces.append(bsid)
        print(f"PASS blind spot {bsid}")
        passes += 1

    if not bs_blocks:
        print("FAIL no blind spot entries found")
        fails += 1

    assumption_blocks = sections(body, "ASM")
    for aid, block in assumption_blocks:
        if not field(block, "Impact if false"):
            print(f"FAIL {aid} missing impact-if-false")
            fails += 1
        else:
            print(f"PASS assumption {aid}")
            passes += 1
    if not assumption_blocks:
        print("FAIL missing assumption ledger")
        fails += 1

    unknown_blocks = sections(body, "UNK")
    for uid, block in unknown_blocks:
        if not field(block, "Statement"):
            print(f"FAIL {uid} missing statement")
            fails += 1
        else:
            print(f"PASS unknown {uid}")
            passes += 1
    if not unknown_blocks:
        print("FAIL missing unknown ledger")
        fails += 1

    verdict_match = re.search(r"^# Verdict\s*\n+\s*([A-Z_]+)", body, re.MULTILINE)
    verdict = verdict_match.group(1) if verdict_match else ""
    if verdict not in VERDICTS:
        print(f"FAIL invalid verdict {verdict}")
        fails += 1
    if open_critical and verdict != "BLOCKED":
        print("FAIL OPEN CRITICAL blind spot with non-BLOCKED verdict")
        fails += 1
    if not open_critical and verdict == "BLOCKED":
        print("WARN BLOCKED verdict without OPEN CRITICAL")
        warns += 1
    if high_open:
        print(f"WARN HIGH blind spots remain OPEN: {', '.join(high_open)}")
        warns += 1
    if "MEMORY CONFLICT" in body and verdict != "BLOCKED" and any("MEMORY_CONFLICT" in block for _id, block in bs_blocks):
        print("WARN memory conflict present; confirm it is resolved before planning")
        warns += 1

    if args.plan:
        plan_text = (root / args.plan).read_text(encoding="utf-8")
        for bsid in required_traces:
            if bsid not in plan_text:
                print(f"FAIL plan does not reference required blind spot {bsid}")
                fails += 1
        print(f"PASS plan traceability checked {args.plan}")
        passes += 1
    if args.verification:
        verification_text = (root / args.verification).read_text(encoding="utf-8")
        for bsid in required_traces:
            if bsid not in verification_text:
                print(f"FAIL verification does not reference required blind spot {bsid}")
                fails += 1
        print(f"PASS verification traceability checked {args.verification}")
        passes += 1

    print(f"SUMMARY pass={passes} warn={warns} fail={fails}")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
