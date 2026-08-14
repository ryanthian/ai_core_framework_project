#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

from memorylib import add_common_args, project_root, today


CATEGORIES = {
    "REQUIREMENT_GAP",
    "AMBIGUITY",
    "ASSUMPTION",
    "DEPENDENCY",
    "DATA_IMPACT",
    "API_IMPACT",
    "SECURITY",
    "PRIVACY",
    "AUTHORIZATION",
    "PERFORMANCE",
    "CONCURRENCY",
    "TRANSACTIONALITY",
    "ERROR_HANDLING",
    "EDGE_CASE",
    "BACKWARD_COMPATIBILITY",
    "MIGRATION",
    "ROLLBACK",
    "OBSERVABILITY",
    "OPERATIONS",
    "UI_UX",
    "ACCESSIBILITY",
    "TESTABILITY",
    "COMPLIANCE",
    "EXTERNAL_INTEGRATION",
    "UNKNOWN",
    "MEMORY_CONFLICT",
}
SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
STATUSES = {"OPEN", "RESOLVED", "ACCEPTED_RISK", "NOT_APPLICABLE", "DEFERRED"}


def read_optional(root: Path, rel: str) -> str:
    if not rel:
        return ""
    path = root / rel
    return path.read_text(encoding="utf-8") if path.exists() else ""


def req_id(requirement: str) -> str:
    match = re.search(r"Requirement ID:\s*([A-Za-z0-9_.-]+)", requirement)
    if match:
        return match.group(1)
    match = re.search(r"(REQ-[0-9A-Za-z_.-]+)", requirement)
    return match.group(1) if match else "REQ-UNKNOWN"


def slug(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")[:80] or "REQ"


def mode_for(text: str, requested: str) -> str:
    if requested != "AUTO":
        return requested
    lower = text.lower()
    deep_terms = [
        "billing",
        "payment",
        "authentication",
        "authorization",
        "permission",
        "external api",
        "bulk",
        "migration",
        "delete",
        "financial",
        "sensitive",
        "privacy",
        "user records",
    ]
    quick_terms = ["copy", "label", "css", "spacing", "documentation"]
    if any(term in lower for term in deep_terms):
        return "DEEP"
    if any(term in lower for term in quick_terms):
        return "QUICK"
    return "STANDARD"


def issue(category, severity, status, finding, why, evidence, assumption="", question="", resolution="", impact="", knowledge="", decision="", accepted="", plan="", verify=""):
    return {
        "category": category,
        "severity": severity,
        "status": status,
        "finding": finding,
        "why": why,
        "evidence": evidence,
        "assumption": assumption,
        "question": question,
        "resolution": resolution,
        "impact": impact,
        "knowledge": knowledge,
        "decision": decision,
        "accepted": accepted,
        "plan": plan,
        "verify": verify,
    }


def analyze(requirement: str, memory: str, repo_context: str, mode: str) -> tuple[list[dict], list[dict], list[dict]]:
    lower = "\n".join([requirement, memory, repo_context]).lower()
    req_lower = requirement.lower()
    issues = []
    assumptions = []
    unknowns = []

    has_memory_conflict = any(line.strip() == "MEMORY CONFLICT" for line in memory.splitlines())
    if has_memory_conflict:
        issues.append(
            issue(
                "MEMORY_CONFLICT",
                "CRITICAL",
                "OPEN",
                "Relevant memory contains conflicting active guidance.",
                "Planning from contradictory memory can encode the wrong rule.",
                "Memory Brief contains MEMORY CONFLICT.",
                question="Which source is authoritative?",
                resolution="Resolve or deprecate the weaker memory record before planning.",
                impact="Implementation may follow the wrong project rule.",
            )
        )

    if "date range" in req_lower or ("filter" in req_lower and "date" in req_lower):
        issues.extend(
            [
                issue("AMBIGUITY", "MEDIUM", "RESOLVED", "Date bounds must be explicit.", "Inclusive/exclusive bounds change visible records.", "Requirement or plan must define bounds.", resolution="Use inclusive start and inclusive end dates.", impact="Boundary-day records may disappear.", plan="PLAN-BS-001", verify="VERIFY-BS-001"),
                issue("EDGE_CASE", "MEDIUM", "RESOLVED", "Start date after end date needs defined behavior.", "Invalid ranges otherwise produce confusing empty results.", "Date range filtering requirement.", resolution="Return an empty result for start > end in the fixture.", impact="Users may misread invalid filters.", plan="PLAN-BS-002", verify="VERIFY-BS-002"),
                issue("TESTABILITY", "MEDIUM", "RESOLVED", "Date parsing needs deterministic tests.", "String comparison can be wrong for malformed dates.", "Fixture uses ISO date strings.", resolution="Test inclusive bounds, empty range, start > end, and malformed dates.", impact="Regression risk around boundary values.", plan="PLAN-BS-003", verify="VERIFY-BS-003"),
            ]
        )
        assumptions.append({"id": "ASM-001", "statement": "Transaction dates use ISO YYYY-MM-DD strings.", "why": "Existing fixture rows use ISO-like dates.", "evidence": "transactions.py and tests use 2026-08-15 style dates.", "confidence": "SUPPORTED", "impact": "Parser behavior changes if timestamps or localized dates appear.", "owner": "Requirement or schema owner", "status": "RESOLVED"})
        unknowns.append({"id": "UNK-001", "statement": "Timezone handling is not specified for date-only fixture rows.", "why": "The fixture has dates, not datetimes.", "impact": "Future datetime filters may need timezone rules.", "owner": "Future requirement", "status": "DEFERRED"})

    if "bulk" in req_lower and "delete" in req_lower and "user" in req_lower:
        has_auth_resolution = "authorization" in lower or "authorized" in lower
        resolved = all(term in lower for term in ["soft delete", "audit", "confirmation", "rollback"]) and has_auth_resolution
        status = "RESOLVED" if resolved else "OPEN"
        issues.extend(
            [
                issue("AUTHORIZATION", "CRITICAL", status, "Bulk user deletion needs explicit admin authorization.", "Without authorization rules this can become privilege escalation.", "Requirement mentions administrators and user records.", question="Which admin role may delete which users?", resolution="Require explicit admin authorization and scope checks.", impact="Unauthorized account deletion.", plan="PLAN-BS-DEL-AUTH", verify="VERIFY-BS-DEL-AUTH"),
                issue("DATA_IMPACT", "CRITICAL", status, "Bulk deletion risks irreversible data loss.", "Deleting user records can remove linked records and personal data.", "Requirement says bulk delete user records.", question="Hard delete or soft delete?", resolution="Use soft delete with rollback window.", impact="Permanent accidental loss.", plan="PLAN-BS-DEL-DATA", verify="VERIFY-BS-DEL-DATA"),
                issue("OBSERVABILITY", "HIGH", "RESOLVED" if "audit" in lower else "OPEN", "Bulk deletion requires audit trail.", "Support and compliance need to know who deleted what.", "Deletion operation affects user records.", resolution="Record actor, timestamp, reason, and affected IDs.", impact="No accountability or troubleshooting path.", plan="PLAN-BS-DEL-AUDIT", verify="VERIFY-BS-DEL-AUDIT"),
                issue("TRANSACTIONALITY", "HIGH", "RESOLVED" if resolved else "OPEN", "Partial failure semantics must be defined.", "Bulk operations can partially succeed.", "Bulk operation requirement.", resolution="Use per-item result semantics and retry-safe handling.", impact="Inconsistent user state.", plan="PLAN-BS-DEL-PARTIAL", verify="VERIFY-BS-DEL-PARTIAL"),
            ]
        )
        unknowns.append({"id": "UNK-001", "statement": "Retention/compliance rules for deleted users are not known.", "why": "No policy source was provided.", "impact": "Hard deletion may violate retention policy.", "owner": "Policy owner", "status": "OPEN" if not resolved else "RESOLVED"})

    if "external" in req_lower and "api" in req_lower:
        issues.extend(
            [
                issue("EXTERNAL_INTEGRATION", "HIGH", "OPEN", "External fulfillment API failure behavior is unspecified.", "Timeouts and outages affect order state.", "Requirement mentions external fulfillment API.", question="What are timeout and retry rules?", resolution="Define timeout, retry, backoff, and reconciliation strategy.", impact="Orders may be stuck or duplicated."),
                issue("API_IMPACT", "HIGH", "OPEN", "Idempotency requirements are unknown.", "Retries can duplicate fulfillment requests.", "External send operation.", question="Does the API support idempotency keys?", resolution="Require idempotency key or local outbox dedupe.", impact="Duplicate shipments."),
                issue("AUTHORIZATION", "HIGH", "OPEN", "External API authentication and secret handling are unspecified.", "Secrets must not leak into logs or memory.", "External API requirement.", question="How are credentials stored and rotated?", resolution="Use managed secret storage and redacted logs.", impact="Secret exposure."),
                issue("OBSERVABILITY", "MEDIUM", "OPEN", "Audit/reconciliation path is missing.", "Support needs to reconcile partial sends.", "External order flow.", resolution="Record request IDs, statuses, and reconciliation checks.", impact="Support cannot diagnose failures."),
            ]
        )
        unknowns.append({"id": "UNK-001", "statement": "We do not know whether the external API supports idempotency keys.", "why": "No API documentation was supplied.", "impact": "Retry design cannot be completed.", "owner": "Integration/API owner", "status": "OPEN"})

    if "statement lookup" in req_lower or "account statement" in req_lower:
        if "only account owners" in memory.lower() or "account owners may view private transaction details" in memory.lower():
            issues.append(
                issue(
                    "AUTHORIZATION",
                    "CRITICAL",
                    "OPEN",
                    "Statement lookup must enforce account ownership.",
                    "Memory says only account owners may view private transaction details.",
                    "Relevant memory contains account ownership rule.",
                    question="How will ownership be checked for lookup?",
                    resolution="Require owner check before returning statement details.",
                    impact="Private transaction details may leak across users.",
                    knowledge="KNOW-OWN-001",
                )
            )

    if not issues:
        issues.append(
            issue(
                "TESTABILITY",
                "LOW",
                "RESOLVED",
                "No high-risk blind spots identified by scaffold.",
                "Even small changes need at least one verification path.",
                "Requirement and memory review.",
                resolution="Include a targeted test or inspection in the plan.",
                impact="Completion claim may be unproven.",
                plan="PLAN-BS-001",
                verify="VERIFY-BS-001",
            )
        )

    return issues, assumptions, unknowns


def verdict(issues: list[dict]) -> str:
    if any(item["severity"] == "CRITICAL" and item["status"] == "OPEN" for item in issues):
        return "BLOCKED"
    if any(item["status"] == "ACCEPTED_RISK" for item in issues):
        return "READY_WITH_ACCEPTED_RISK"
    return "READY_FOR_PLAN"


def risk(issues: list[dict]) -> str:
    order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    for severity in order:
        if any(item["severity"] == severity for item in issues):
            return severity
    return "LOW"


def render(report_id: str, project: str, requirement_ref: str, memory_ref: str, mode: str, requirement: str, memory: str, issues: list[dict], assumptions: list[dict], unknowns: list[dict]) -> str:
    lines = [
        "---",
        f"id: {report_id}",
        f"requirement: {requirement_ref}",
        f"project: {project}",
        f"created: {today()}",
        f"memory_brief: {memory_ref}",
        f"mode: {mode}",
        "status: COMPLETE",
        f"overall_risk: {risk(issues)}",
        "---",
        "",
        "# Requirement Understanding",
        "",
        requirement.strip().splitlines()[0] if requirement.strip() else "Requirement supplied by reference.",
        "",
        "# Relevant Memory",
        "",
    ]
    memory_refs = [line for line in memory.splitlines() if line.startswith("- KNOW") or line.startswith("- ADR") or "MEMORY CONFLICT" in line]
    lines.extend(memory_refs or ["- None found or memory brief unavailable."])
    lines.extend(["", "# Blind Spots", ""])
    for idx, item in enumerate(issues, 1):
        lines.extend(
            [
                f"## BS-{idx:03d}",
                "",
                f"- Category: {item['category']}",
                f"- Severity: {item['severity']}",
                f"- Status: {item['status']}",
                f"- Finding: {item['finding']}",
                f"- Why It Matters: {item['why']}",
                f"- Evidence: {item['evidence']}",
                f"- Assumption: {item['assumption']}",
                f"- Question: {item['question']}",
                f"- Recommended Resolution: {item['resolution']}",
                f"- Impact if Ignored: {item['impact']}",
                f"- Related Knowledge: {item['knowledge']}",
                f"- Related Decision: {item['decision']}",
                f"- Accepted Risk Justification: {item['accepted']}",
                f"- Plan Trace: {item['plan']}",
                f"- Verification Trace: {item['verify']}",
                "",
            ]
        )
    lines.extend(["# Assumption Ledger", ""])
    for item in assumptions or [{"id": "ASM-001", "statement": "No significant implementation assumption recorded by scaffold.", "why": "Requirement appears direct.", "evidence": "Blind Spot Pass scaffold.", "confidence": "LOW", "impact": "Codex should still review before planning.", "owner": "Implementer", "status": "NOT_APPLICABLE"}]:
        lines.extend([f"## {item['id']}", "", f"- Statement: {item['statement']}", f"- Why assumed: {item['why']}", f"- Evidence: {item['evidence']}", f"- Confidence: {item['confidence']}", f"- Impact if false: {item['impact']}", f"- Resolution owner/source: {item['owner']}", f"- Status: {item['status']}", ""])
    lines.extend(["# Unknowns Ledger", ""])
    for item in unknowns or [{"id": "UNK-001", "statement": "No blocking unknown recorded by scaffold.", "why": "Requirement/memory did not expose one.", "impact": "None known.", "owner": "Implementer", "status": "NOT_APPLICABLE"}]:
        lines.extend([f"## {item['id']}", "", f"- Statement: {item['statement']}", f"- Why unknown: {item['why']}", f"- Impact: {item['impact']}", f"- Resolution owner/source: {item['owner']}", f"- Status: {item['status']}", ""])
    lines.extend(["# Open Questions", ""])
    qs = [item["question"] for item in issues if item["question"] and item["status"] == "OPEN"]
    lines.extend([f"- {q}" for q in qs] or ["- None."])
    lines.extend(["", "# Blocking Issues", ""])
    blockers = [item for item in issues if item["severity"] == "CRITICAL" and item["status"] == "OPEN"]
    lines.extend([f"- {item['finding']}" for item in blockers] or ["- None."])
    lines.extend(["", "# Accepted Risks", ""])
    accepted = [item for item in issues if item["status"] == "ACCEPTED_RISK"]
    lines.extend([f"- {item['finding']}: {item['accepted']}" for item in accepted] or ["- None."])
    lines.extend(["", "# Planning Constraints", ""])
    constraints = [item["resolution"] for item in issues if item["resolution"] and item["status"] in {"RESOLVED", "ACCEPTED_RISK", "DEFERRED"}]
    lines.extend([f"- {item}" for item in constraints] or ["- Resolve blockers before planning."])
    lines.extend(["", "# Verdict", "", verdict(issues), ""])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    parser.add_argument("--project", required=True)
    parser.add_argument("--requirement", required=True)
    parser.add_argument("--memory-brief", default="")
    parser.add_argument("--repo-context", default="")
    parser.add_argument("--selected-skills", default="")
    parser.add_argument("--mode", choices=["AUTO", "QUICK", "STANDARD", "DEEP"], default="AUTO")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    root = project_root(args.project_root)
    requirement = read_optional(root, args.requirement)
    memory = read_optional(root, args.memory_brief)
    repo_context = read_optional(root, args.repo_context)
    mode = mode_for("\n".join([requirement, memory, repo_context]), args.mode)
    rid = req_id(requirement)
    report_id = f"BSP-{rid}"
    issues, assumptions, unknowns = analyze(requirement, memory, repo_context, mode)
    output = render(report_id, args.project, args.requirement, args.memory_brief, mode, requirement, memory, issues, assumptions, unknowns)
    out_rel = args.output or f".ai/context/BLIND-SPOT-{slug(rid)}.md"
    out_path = root / out_rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        raise SystemExit(f"FAIL refusing to overwrite existing report: {out_path}")
    out_path.write_text(output, encoding="utf-8")
    print(f"PASS wrote blind spot report {out_path}")
    print(f"VERDICT {verdict(issues)}")
    print(f"MODE {mode}")


if __name__ == "__main__":
    main()
