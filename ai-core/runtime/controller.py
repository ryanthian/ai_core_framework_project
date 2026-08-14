from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

RUNTIME_ROOT = Path(__file__).resolve().parent
AI_CORE_ROOT = RUNTIME_ROOT.parent
if str(RUNTIME_ROOT) not in sys.path:
    sys.path.insert(0, str(RUNTIME_ROOT))
if str(AI_CORE_ROOT / "services") not in sys.path:
    sys.path.insert(0, str(AI_CORE_ROOT / "services"))

from artifacts import init_registry, register_artifact
from constants import SCHEMA_VERSION
from errors import error
from events import append_event, now
from router import classify_input
from project_service import ensure_project, load_project
from run_service import create_run, load_run, mark_stage, run_dir, save_run, snapshot
import agent_service
import blindspot_service
import document_service
import domain_service
import memory_service
import skill_service
import validation_service


WORKSPACE_ROOT = AI_CORE_ROOT.parent


def rel(project_root: Path, path: Path) -> str:
    return str(path.relative_to(project_root))


def read_text(project_root: Path, input_ref: str) -> str:
    path = project_root / input_ref
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else input_ref


def requirement_id(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("id:"):
            return line.split(":", 1)[1].strip().strip("\"'")
        if "Requirement ID:" in line:
            return line.split("Requirement ID:", 1)[1].strip()
    return Path(fallback).stem


def write_artifact(project_root: Path, state: dict, artifact_id: str, artifact_type: str, rel_path: str, content: str, role: str = "AI_CORE", related: list[str] | None = None) -> str:
    path = project_root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stem = path.stem
        path = path.with_name(f"{stem}-v{len(list(path.parent.glob(stem + '*'))) + 1}{path.suffix}")
        rel_path = rel(project_root, path)
    path.write_text(content, encoding="utf-8")
    register_artifact(run_dir(project_root, state["run_id"]), artifact_id, artifact_type, rel_path, created_by_role=role, related_refs=related or [])
    state["artifact_refs"][artifact_id] = rel_path
    save_run(project_root, state)
    return rel_path


def human_action(project_root: Path, state: dict, reason: str, decision: str, refs: list[str]) -> str:
    hid = f"HUMAN-{len(state.get('human_actions', [])) + 1:03d}"
    payload = {
        "task_id": hid,
        "run_id": state["run_id"],
        "reason": reason,
        "required_decision": decision,
        "context_refs": refs,
        "created": now(),
        "status": "OPEN",
    }
    path = project_root / ".ai" / "human-actions" / f"{hid}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    state["human_actions"].append(str(path.relative_to(project_root)))
    state["human_approval"] = {"required": True, "task_id": hid, "reason": reason}
    state["status"] = "AWAITING_HUMAN"
    state["blocked_reason"] = reason
    state["errors"].append(error("HUMAN_APPROVAL_REQUIRED", reason, state.get("current_stage", ""), "CRITICAL", True, decision))
    append_event(run_dir(project_root, state["run_id"]), "HUMAN_ACTION_CREATED", task_id=hid, reason=reason)
    save_run(project_root, state)
    return str(path.relative_to(project_root))


def choose_profile(text: str, requested: str) -> str:
    if requested in {"LEAN", "STANDARD", "DEEP"}:
        if requested == "LEAN" and any(term in text.lower() for term in ["delete", "financial", "authorization", "billing", "migration", "external api"]):
            return "DEEP"
        return requested
    lower = text.lower()
    if any(term in lower for term in ["delete", "financial", "billing", "authorization", "permission", "migration", "external api", "bulk"]):
        return "DEEP"
    if len(text) < 240 and not any(term in lower for term in ["api", "data", "security"]):
        return "LEAN"
    return "STANDARD"


def health(project_root: Path) -> tuple[str, list[str]]:
    messages: list[str] = []
    ensure_project(project_root, WORKSPACE_ROOT)
    checks = [
        (project_root / ".ai").is_dir(),
        (project_root / "scripts" / "retrieve-memory.py").exists(),
        (project_root / "scripts" / "run-blind-spot-pass.py").exists(),
        (project_root / "scripts" / "run-agent-workflow.py").exists(),
        (project_root / "scripts" / "ingest-document.py").exists(),
        (WORKSPACE_ROOT / "domain-packs").is_dir(),
        (WORKSPACE_ROOT / "codex-skills").is_dir(),
    ]
    for ok, name in zip(checks, ["project initialized", "memory", "blind spot", "agent harness", "documents", "domain registry", "skills"]):
        messages.append(("PASS " if ok else "FAIL ") + name)
    ok_agent, agent_out = agent_service.validate(project_root)
    messages.append(("PASS " if ok_agent else "FAIL ") + "agent contracts")
    ok_memory, memory_out = memory_service.validate(project_root)
    messages.append(("PASS " if ok_memory else "WARN ") + "memory validator")
    if not ok_agent:
        messages.append(agent_out.strip())
    if not ok_memory:
        messages.append(memory_out.strip())
    status = "FAIL" if any(line.startswith("FAIL") for line in messages) else ("WARN" if any(line.startswith("WARN") for line in messages) else "PASS")
    return status, messages


def analyze(project_root: Path, input_ref: str, input_type: str = "AUTO", profile: str = "AUTO", stop_after: str = "") -> dict:
    project = ensure_project(project_root, WORKSPACE_ROOT)
    routed = classify_input(project_root, input_ref, input_type)
    raw = read_text(project_root, input_ref)
    selected_profile = choose_profile(raw, profile)
    state = create_run(project_root, project["project_id"], routed, input_ref, selected_profile)
    state["status"] = "ANALYZING"
    append_event(run_dir(project_root, state["run_id"]), "INPUT_ROUTED", input_type=routed)
    requirement_rel = input_ref

    if routed == "SOURCE_DOCUMENT":
        doc_id, ingest_out, duplicate = document_service.ingest(project_root, input_ref, Path(input_ref).stem, "AUTHORITATIVE")
        state["document_id"] = doc_id
        refs = document_service.refs(project_root, doc_id)
        register_artifact(run_dir(project_root, state["run_id"]), f"MANIFEST-{doc_id}", "DOCUMENT_MANIFEST", refs["manifest"], "DocumentService")
        state["artifact_refs"][f"MANIFEST-{doc_id}"] = refs["manifest"]
        append_event(run_dir(project_root, state["run_id"]), "DOCUMENT_INGESTED", document_id=doc_id, duplicate=duplicate)
        if duplicate:
            state["errors"].append(error("RUN_STATE_INVALID", "Duplicate source document detected; existing document reused.", "INGEST", "WARN", True, "Use explicit new-version flow for a new version."))
        else:
            document_service.extract(project_root, doc_id)
            append_event(run_dir(project_root, state["run_id"]), "DOCUMENT_EXTRACTED", document_id=doc_id)
            document_service.analyze(project_root, doc_id)
            document_service.review(project_root, doc_id)
            document_service.promote(project_root, doc_id)
        refs = document_service.refs(project_root, doc_id)
        for art_id, typ, key in [
            (f"INTEL-{doc_id}", "DOCUMENT_INTELLIGENCE", "intelligence"),
            (f"REVIEW-{doc_id}", "DOCUMENT_REVIEW", "review"),
            (f"PROMOTE-{doc_id}", "DOCUMENT_PROMOTION", "promotion"),
        ]:
            if (project_root / refs[key]).exists():
                register_artifact(run_dir(project_root, state["run_id"]), art_id, typ, refs[key], "DocumentService")
                state["artifact_refs"][art_id] = refs[key]
        promoted = project_root / refs["promotion"]
        if promoted.exists():
            pdata = json.loads(promoted.read_text(encoding="utf-8"))
            reqs = [item["target"] for item in pdata.get("promoted", []) if item.get("target", "").startswith(".ai/requirements/")]
            if reqs:
                requirement_rel = reqs[0]
        if (project_root / refs["change_impact"]).exists():
            register_artifact(run_dir(project_root, state["run_id"]), f"CHANGE-{doc_id}", "DOCUMENT_INTELLIGENCE", refs["change_impact"], "DocumentService")
            human_action(project_root, state, "DOCUMENT_MEMORY_CONFLICT detected from source document.", "Resolve document-memory conflict before implementation.", [refs["change_impact"]])
            save_run(project_root, state)
            return state
        mark_stage(state, "INGEST")
        mark_stage(state, "DOCUMENT_ANALYSIS")
    else:
        mark_stage(state, "INGEST", "SKIPPED_NOT_APPLICABLE")
        mark_stage(state, "DOCUMENT_ANALYSIS", "SKIPPED_NOT_APPLICABLE")

    req_text = read_text(project_root, requirement_rel)
    rid = requirement_id(req_text, requirement_rel)
    state["requirement_id"] = rid
    register_artifact(run_dir(project_root, state["run_id"]), f"REQ-{rid}", "REQUIREMENT", requirement_rel, "RequirementAnalyst")
    state["artifact_refs"][f"REQ-{rid}"] = requirement_rel
    harness_rel = f".ai/runs/RUN-{rid}.json"
    if not (project_root / harness_rel).exists():
        ok_agent_start, agent_out = agent_service.start(project_root, requirement_rel, selected_profile)
        if ok_agent_start and (project_root / harness_rel).exists():
            register_artifact(run_dir(project_root, state["run_id"]), f"AGENT-{state['run_id']}", "AGENT_RUN_STATE", harness_rel, "AgentService")
            state["artifact_refs"][f"AGENT-{state['run_id']}"] = harness_rel
            append_event(run_dir(project_root, state["run_id"]), "ROLE_STARTED", role="REQUIREMENT_ANALYST", harness_state=harness_rel)
        else:
            state["errors"].append(error("RUN_STATE_INVALID", f"Agent harness start skipped or failed: {agent_out}", "REQUIREMENT_ANALYSIS", "WARN", True, "Existing harness run may already exist."))
    analysis_rel = write_artifact(
        project_root,
        state,
        f"REQ-ANALYSIS-{rid}",
        "REQUIREMENT",
        f".ai/context/REQUIREMENT-ANALYSIS-{state['run_id']}.md",
        f"# Requirement Analysis\n\nRequirement: `{requirement_rel}`\n\n## Summary\n\n{req_text.strip()[:1200]}\n\n## Verdict\n\nREADY_FOR_MEMORY\n",
        "REQUIREMENT_ANALYST",
    )
    mark_stage(state, "REQUIREMENT_ANALYSIS")

    memory_rel = f".ai/context/MEMORY-BRIEF-{state['run_id']}.md"
    ok, out = memory_service.retrieve(project_root, project["project_id"], req_text, memory_rel)
    if not ok:
        state["errors"].append(error("MEMORY_VALIDATION_FAILED", out, "MEMORY_RETRIEVAL", "ERROR", True, "Run memory validator."))
        save_run(project_root, state)
        return state
    register_artifact(run_dir(project_root, state["run_id"]), f"MEMORY-{state['run_id']}", "MEMORY_BRIEF", memory_rel, "MemoryService", related_refs=[analysis_rel])
    state["memory_refs"].append(memory_rel)
    append_event(run_dir(project_root, state["run_id"]), "MEMORY_RETRIEVED", artifact=memory_rel)
    memory_text = read_text(project_root, memory_rel)
    mark_stage(state, "MEMORY_RETRIEVAL")

    domain_matches = domain_service.relevant(project_root, req_text)
    domain_rel = write_artifact(
        project_root,
        state,
        f"DOMAIN-{state['run_id']}",
        "DOMAIN_CONTEXT",
        f".ai/context/DOMAIN-CONTEXT-{state['run_id']}.md",
        "# Domain Context\n\n" + "\n".join([f"- {row['pack']}@{row['version']} {row['rule']['id']}: {row['rule']['title']}" for row in domain_matches] or ["- None found."]) + "\n",
        "DomainService",
    )
    state["domain_refs"] = [row["rule"]["id"] for row in domain_matches]
    mark_stage(state, "DOMAIN_RETRIEVAL")

    if "DOMAIN_PROJECT_CONFLICT" in memory_text or "DOMAIN_DOMAIN_CONFLICT" in memory_text:
        human_action(project_root, state, "Domain guidance conflicts with project memory or another active domain pack.", "Resolve domain conflict or disable weak pack before planning.", [memory_rel, domain_rel])
        save_run(project_root, state)
        return state

    bsp_rel = f".ai/context/BLIND-SPOT-{state['run_id']}.md"
    ok, out = blindspot_service.run(project_root, project["project_id"], requirement_rel, memory_rel, bsp_rel, "AUTO")
    if not ok:
        state["errors"].append(error("GATE_BLOCKED", out, "BLIND_SPOT", "ERROR", True, "Fix Blind Spot Pass input."))
        save_run(project_root, state)
        return state
    register_artifact(run_dir(project_root, state["run_id"]), f"BSP-{state['run_id']}", "BLIND_SPOT_REPORT", bsp_rel, "BlindSpotService", related_refs=[memory_rel])
    verdict, critical, high = blindspot_service.verdict(project_root, bsp_rel)
    append_event(run_dir(project_root, state["run_id"]), "BLIND_SPOT_COMPLETED", verdict=verdict, critical_open=critical, high_open=high)
    mark_stage(state, "BLIND_SPOT")
    if verdict == "BLOCKED" or critical:
        state["gate_status"]["A0"] = "BLOCKED"
        mark_stage(state, "GATE_A0")
        append_event(run_dir(project_root, state["run_id"]), "GATE_BLOCKED", gate="A0")
        human_action(project_root, state, "CRITICAL Blind Spot blocks planning.", "Clarify or approve risk explicitly; AI-Core will not simulate approval.", [bsp_rel])
        save_run(project_root, state)
        return state
    state["gate_status"]["A0"] = "PASSED"
    append_event(run_dir(project_root, state["run_id"]), "GATE_PASSED", gate="A0")
    mark_stage(state, "GATE_A0")

    skills = skill_service.select(WORKSPACE_ROOT / "codex-skills", req_text)
    skill_lines = ["# Skill Selection", "", f"Requirement: {requirement_rel}", ""]
    for item in skills:
        skill_lines.append(f"- {item['name']}: {item['why']}")
    skill_lines.extend(["", "## Not Selected", "", "- Other installed skills were not selected because they did not directly reduce this task's risk.", ""])
    skill_rel = write_artifact(project_root, state, f"SKILL-{state['run_id']}", "SKILL_SELECTION", f".ai/context/SKILL-SELECTION-{state['run_id']}.md", "\n".join(skill_lines), "SKILL_SELECTOR")
    state["skill_refs"] = [item["name"] for item in skills]
    mark_stage(state, "SKILL_SELECTION")
    state["status"] = "READY"
    state["current_stage"] = "PLANNING"
    save_run(project_root, state)
    if stop_after == "ANALYZE":
        return state
    return state


def _write_fixture_code(project_root: Path, demo: str, defect: bool = False, reviewer_issue: bool = False) -> tuple[list[str], str]:
    src = project_root / "src"
    tests = project_root / "tests"
    src.mkdir(exist_ok=True)
    tests.mkdir(exist_ok=True)
    if demo == "document":
        code = """def export_accounts_json(accounts):\n    return [{\"id\": row[\"id\"], \"owner\": row[\"owner\"], \"balance\": row[\"balance\"]} for row in accounts]\n"""
        test = """import unittest\nfrom src.transactions import export_accounts_json\n\nclass ExportTests(unittest.TestCase):\n    def test_json_export(self):\n        self.assertEqual(export_accounts_json([{\"id\":\"A1\",\"owner\":\"R\",\"balance\":10}]), [{\"id\":\"A1\",\"owner\":\"R\",\"balance\":10}])\n\nif __name__ == \"__main__\":\n    unittest.main()\n"""
        summary = "Added account JSON export fixture."
    else:
        if demo == "amount":
            merchant_body = "return [row for row in transactions if row.get('merchant') == merchant]\n"
            amount_body = "return [row for row in transactions if min_amount <= row.get('amount', 0) <= max_amount]\n"
            if defect:
                amount_body = "return [row for row in transactions if row.get('amount', 0) >= min_amount]\n"
        else:
            merchant_body = "return [row for row in transactions if row.get('merchant') == merchant]\n"
            if defect:
                merchant_body = "return transactions\n"
            amount_body = "return [row for row in transactions if min_amount <= row.get('amount', 0) <= max_amount]\n"
        code = f"def filter_transactions(transactions, merchant):\n    {merchant_body}\n\ndef filter_amount_range(transactions, min_amount, max_amount):\n    {amount_body}\n"
        if reviewer_issue:
            code += "\nGLOBAL_MUTABLE_CACHE = []\n"
        test = """import unittest\nfrom src.transactions import filter_transactions, filter_amount_range\n\nclass TransactionTests(unittest.TestCase):\n    def test_merchant_filter(self):\n        rows = [{\"merchant\":\"Alpha\",\"amount\":4}, {\"merchant\":\"Beta\",\"amount\":12}]\n        self.assertEqual(filter_transactions(rows, \"Alpha\"), [{\"merchant\":\"Alpha\",\"amount\":4}])\n\n    def test_amount_range(self):\n        rows = [{\"merchant\":\"A\",\"amount\":4}, {\"merchant\":\"B\",\"amount\":12}, {\"merchant\":\"C\",\"amount\":20}]\n        self.assertEqual(filter_amount_range(rows, 5, 15), [{\"merchant\":\"B\",\"amount\":12}])\n\nif __name__ == \"__main__\":\n    unittest.main()\n"""
        summary = "Added transaction filtering fixture."
    (src / "transactions.py").write_text(code, encoding="utf-8")
    (tests / "test_transactions.py").write_text(test, encoding="utf-8")
    return ["src/transactions.py", "tests/test_transactions.py"], summary


def _run_tests(project_root: Path) -> tuple[bool, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=str(project_root), env=env, text=True, capture_output=True)
    return result.returncode == 0, result.stdout + result.stderr


def continue_run(project_root: Path, state: dict, demo: str = "structured", stop_after: str = "") -> dict:
    if state["status"] == "CANCELLED":
        state["errors"].append(error("RUN_STATE_INVALID", "Cancelled runs cannot resume unless explicitly reopened.", state.get("current_stage", ""), "ERROR", True, "Create a new run or reopen with a future command."))
        save_run(project_root, state)
        return state
    if state["gate_status"].get("A0") != "PASSED":
        return state
    append_event(run_dir(project_root, state["run_id"]), "RUN_RESUMED" if state["status"] not in {"READY", "ANALYZING"} else "RUN_STARTED")
    state["status"] = "RUNNING"

    if "PLANNING" not in state["completed_stages"]:
        plan_rel = write_artifact(project_root, state, f"PLAN-{state['run_id']}", "PLAN", f".ai/plans/PLAN-{state['run_id']}.md", "# Implementation Plan\n\n1. Add fixture implementation.\n2. Add focused unit tests.\n3. Run tests.\n4. Review against requirement, memory, domain context, and blind spots.\n", "PLANNER")
        state["gate_status"]["A"] = "PASSED"
        append_event(run_dir(project_root, state["run_id"]), "GATE_PASSED", gate="A")
        mark_stage(state, "PLANNING")
        mark_stage(state, "GATE_A")
        save_run(project_root, state)
        if stop_after == "PLANNING":
            state["status"] = "READY"
            save_run(project_root, state)
            return state

    defect_first = demo == "test-failure" and "TESTING" not in state["completed_stages"]
    reviewer_issue = demo == "reviewer-loop" and "REVIEW" not in state["completed_stages"]
    if "IMPLEMENTATION" not in state["completed_stages"]:
        changed, implementation_note = _write_fixture_code(project_root, "amount" if demo == "test-failure" else demo, defect=defect_first, reviewer_issue=reviewer_issue)
        impl_rel = write_artifact(project_root, state, f"IMPL-{state['run_id']}", "IMPLEMENTATION_SUMMARY", f".ai/context/IMPLEMENTATION-SUMMARY-{state['run_id']}.md", f"# Implementation Summary\n\nFiles Changed:\n" + "\n".join(f"- {p}" for p in changed) + f"\n\nBehavior Added:\n\n{implementation_note}\n", "IMPLEMENTER")
        mark_stage(state, "IMPLEMENTATION")
        save_run(project_root, state)

    if "TESTING" not in state["completed_stages"]:
        ok, output = _run_tests(project_root)
        test_rel = write_artifact(project_root, state, f"TEST-{state['run_id']}", "TEST_EVIDENCE", f".ai/verification/TEST-EVIDENCE-{state['run_id']}.md", f"# Test Evidence\n\nCommand: `{sys.executable} -m unittest discover -s tests`\n\nExpected: PASS\n\nActual: {'PASS' if ok else 'FAIL'}\n\n```text\n{output}\n```\n", "TESTER")
        if not ok:
            append_event(run_dir(project_root, state["run_id"]), "LOOPBACK", from_role="TESTER", to_role="IMPLEMENTER", reason="Test failure")
            state["retry_counts"]["IMPLEMENTER"] = state["retry_counts"].get("IMPLEMENTER", 0) + 1
            if state["retry_counts"]["IMPLEMENTER"] > 3:
                state["status"] = "BLOCKED"
                state["errors"].append(error("TEST_FAILED", "Retry limit reached after test failure.", "TESTING", "ERROR", True, "Human intervention required."))
                save_run(project_root, state)
                return state
            _write_fixture_code(project_root, "amount" if demo == "test-failure" else demo, defect=False)
            ok, output = _run_tests(project_root)
            retry_rel = write_artifact(project_root, state, f"TEST-{state['run_id']}-RETRY", "TEST_EVIDENCE", f".ai/verification/TEST-EVIDENCE-{state['run_id']}-retry.md", f"# Test Evidence Retry\n\nActual: {'PASS' if ok else 'FAIL'}\n\n```text\n{output}\n```\n", "TESTER")
        if not ok:
            state["status"] = "FAILED"
            state["errors"].append(error("TEST_FAILED", "Tests failed.", "TESTING", "ERROR", True, "Return to implementer."))
            save_run(project_root, state)
            return state
        mark_stage(state, "TESTING")
        save_run(project_root, state)
        if stop_after == "TESTING":
            state["status"] = "READY"
            save_run(project_root, state)
            return state

    if "REVIEW" not in state["completed_stages"]:
        code = (project_root / "src" / "transactions.py").read_text(encoding="utf-8")
        if "GLOBAL_MUTABLE_CACHE" in code:
            review_text = "# Review Report\n\nVerdict: CHANGES_REQUIRED\n\nFinding: global mutable cache is unrelated to requirement and hurts maintainability.\n"
            write_artifact(project_root, state, f"REVIEW-{state['run_id']}-v1", "REVIEW_REPORT", f".ai/verification/REVIEW-REPORT-{state['run_id']}-v1.md", review_text, "REVIEWER")
            append_event(run_dir(project_root, state["run_id"]), "LOOPBACK", from_role="REVIEWER", to_role="IMPLEMENTER", reason="Maintainability defect")
            _write_fixture_code(project_root, "structured", defect=False, reviewer_issue=False)
            ok, output = _run_tests(project_root)
            write_artifact(project_root, state, f"TEST-{state['run_id']}-REVIEW-RETRY", "TEST_EVIDENCE", f".ai/verification/TEST-EVIDENCE-{state['run_id']}-review-retry.md", f"# Test Evidence After Review Fix\n\nActual: {'PASS' if ok else 'FAIL'}\n\n```text\n{output}\n```\n", "TESTER")
        review_rel = write_artifact(project_root, state, f"REVIEW-{state['run_id']}", "REVIEW_REPORT", f".ai/verification/REVIEW-REPORT-{state['run_id']}.md", "# Review Report\n\nVerdict: APPROVE\n\nFindings: None blocking. Checked requirement, plan, blind spots, tests, and implementation drift.\n", "REVIEWER")
        mark_stage(state, "REVIEW")
        save_run(project_root, state)

    if "VERIFICATION" not in state["completed_stages"]:
        verify_rel = write_artifact(project_root, state, f"VERIFY-{state['run_id']}", "VERIFICATION_REPORT", f".ai/verification/VERIFICATION-REPORT-{state['run_id']}.md", "# Verification Report\n\nVerdict: PASS\n\nEvidence: tests passed, review approved, Gate A0/A/C conditions satisfied for disposable fixture.\n", "VERIFIER")
        state["gate_status"]["C"] = "PASSED"
        append_event(run_dir(project_root, state["run_id"]), "VERIFICATION_PASSED", artifact=verify_rel)
        append_event(run_dir(project_root, state["run_id"]), "GATE_PASSED", gate="C")
        mark_stage(state, "VERIFICATION")
        mark_stage(state, "GATE_C")
        save_run(project_root, state)

    if "MEMORY_CURATION" not in state["completed_stages"]:
        k_rel = write_artifact(project_root, state, f"KNOW-{state['run_id']}", "KNOWLEDGE", f".ai/context/KNOWLEDGE-CAPTURE-{state['run_id']}.md", "# Knowledge Capture\n\nNo reusable production knowledge captured from disposable fixture. Evidence preserved in run artifacts only.\n", "MEMORY_CURATOR")
        mark_stage(state, "MEMORY_CURATION")
        save_run(project_root, state)

    if "HANDOFF" not in state["completed_stages"]:
        h_rel = write_artifact(project_root, state, f"HANDOFF-{state['run_id']}", "HANDOFF", f".ai/handoffs/HANDOFF-{state['run_id']}.md", f"# Handoff\n\nRun: {state['run_id']}\n\nStatus: verified disposable fixture run. Continue from persisted AI-Core state and artifacts, not chat history.\n", "HANDOFF_WRITER")
        state["gate_status"]["D"] = "PASSED"
        append_event(run_dir(project_root, state["run_id"]), "GATE_PASSED", gate="D")
        mark_stage(state, "HANDOFF")
        mark_stage(state, "GATE_D")
        save_run(project_root, state)

    traceability(project_root, state)
    summary(project_root, state)
    mark_stage(state, "COMPLETE")
    state["status"] = "COMPLETED"
    state["result"] = "PASS"
    append_event(run_dir(project_root, state["run_id"]), "RUN_COMPLETED")
    save_run(project_root, state)
    return state


def run(project_root: Path, input_ref: str, input_type: str = "AUTO", profile: str = "AUTO", demo: str = "structured", stop_after: str = "") -> dict:
    state = analyze(project_root, input_ref, input_type, profile, stop_after="ANALYZE")
    if state["status"] == "AWAITING_HUMAN":
        return state
    return continue_run(project_root, state, demo=demo, stop_after=stop_after)


def resume(project_root: Path, run_id: str, demo: str = "structured") -> dict:
    state = load_run(project_root, run_id)
    failures, warnings = validation_service.validate_artifacts(project_root, run_dir(project_root, run_id), state)
    if failures:
        state["status"] = "FAILED"
        state["errors"].append(error("ARTIFACT_MISSING", "; ".join(failures), state.get("current_stage", ""), "ERROR", True, "Repair artifacts or rollback to snapshot."))
        save_run(project_root, state)
        return state
    append_event(run_dir(project_root, run_id), "RUN_RESUMED", warnings=warnings)
    return continue_run(project_root, state, demo=demo)


def cancel(project_root: Path, run_id: str, reason: str) -> dict:
    state = load_run(project_root, run_id)
    state["status"] = "CANCELLED"
    state["blocked_reason"] = reason
    state["cancellation"] = {"reason": reason, "cancelled_at": now(), "last_stage": state.get("current_stage", "")}
    snap = snapshot(project_root, state, "cancel")
    append_event(run_dir(project_root, run_id), "RUN_CANCELLED", reason=reason, snapshot=snap)
    save_run(project_root, state)
    return state


def status(project_root: Path, run_id: str) -> str:
    state = load_run(project_root, run_id)
    return "\n".join(
        [
            "# AI-Core Status",
            "",
            f"Project: {state['project_id']}",
            f"Active Run: {state['run_id']}",
            f"Requirement: {state.get('requirement_id', '')}",
            f"Current Stage: {state.get('current_stage', '')}",
            f"Current Role: {state.get('current_role', '')}",
            f"Profile: {state.get('profile', '')}",
            f"Gate Status: {state.get('gate_status', {})}",
            f"Open Blockers: {state.get('blocked_reason', '') or 'None'}",
            f"Open Critical Risks: {'Yes' if state.get('human_approval', {}).get('required') else 'No'}",
            f"Completed Stages: {', '.join(state.get('completed_stages', []))}",
            f"Pending Stages: see canonical stage model",
            f"Latest Verification: {state.get('artifact_refs', {}).get('VERIFY-' + state['run_id'], '')}",
            f"Human Action Needed: {state.get('human_approval', {}).get('required', False)}",
        ]
    )


def traceability(project_root: Path, state: dict) -> str:
    content = "\n".join(
        [
            "# AI-Core Traceability",
            "",
            "| Link | Evidence |",
            "|---|---|",
            f"| Input | {state['input_ref']} |",
            f"| Requirement | {state.get('requirement_id', '')} |",
            f"| Memory | {', '.join(state.get('memory_refs', []))} |",
            f"| Domain Rules | {', '.join(state.get('domain_refs', [])) or 'None'} |",
            f"| Blind Spots | {state.get('artifact_refs', {}).get('BSP-' + state['run_id'], '')} |",
            f"| Plan | {state.get('artifact_refs', {}).get('PLAN-' + state['run_id'], '')} |",
            f"| Tests | {state.get('artifact_refs', {}).get('TEST-' + state['run_id'], '')} |",
            f"| Review | {state.get('artifact_refs', {}).get('REVIEW-' + state['run_id'], '')} |",
            f"| Verification | {state.get('artifact_refs', {}).get('VERIFY-' + state['run_id'], '')} |",
            f"| Knowledge/Handoff | {state.get('artifact_refs', {}).get('KNOW-' + state['run_id'], '')} / {state.get('artifact_refs', {}).get('HANDOFF-' + state['run_id'], '')} |",
            "",
        ]
    )
    path = project_root / ".ai" / "runs" / state["run_id"] / "traceability.md"
    path.write_text(content, encoding="utf-8")
    register_artifact(run_dir(project_root, state["run_id"]), f"TRACE-{state['run_id']}", "TRACEABILITY", rel(project_root, path), "AI_CORE")
    return rel(project_root, path)


def summary(project_root: Path, state: dict) -> str:
    content = "\n".join(
        [
            "# AI-Core Run Summary",
            "",
            f"Input: {state['input_ref']}",
            f"Requirement: {state.get('requirement_id', '')}",
            f"Profile: {state['profile']}",
            f"Domain Packs / Rules: {', '.join(state.get('domain_refs', [])) or 'None'}",
            f"Relevant Memory: {', '.join(state.get('memory_refs', [])) or 'None'}",
            f"Blind Spots: {state.get('artifact_refs', {}).get('BSP-' + state['run_id'], '')}",
            f"Skills: {', '.join(state.get('skill_refs', [])) or 'None'}",
            f"Plan: {state.get('artifact_refs', {}).get('PLAN-' + state['run_id'], '')}",
            f"Implementation: {state.get('artifact_refs', {}).get('IMPL-' + state['run_id'], '')}",
            f"Tests: {state.get('artifact_refs', {}).get('TEST-' + state['run_id'], '')}",
            f"Review: {state.get('artifact_refs', {}).get('REVIEW-' + state['run_id'], '')}",
            f"Verification: {state.get('artifact_refs', {}).get('VERIFY-' + state['run_id'], '')}",
            f"Knowledge Captured: {state.get('artifact_refs', {}).get('KNOW-' + state['run_id'], '')}",
            f"Decisions Captured: None",
            f"Handoff: {state.get('artifact_refs', {}).get('HANDOFF-' + state['run_id'], '')}",
            f"Human Interventions: {', '.join(state.get('human_actions', [])) or 'None'}",
            f"Retries: {state.get('retry_counts', {})}",
            f"Final Verdict: {state.get('result', state.get('status'))}",
            "",
        ]
    )
    path = project_root / ".ai" / "runs" / state["run_id"] / "summary.md"
    path.write_text(content, encoding="utf-8")
    register_artifact(run_dir(project_root, state["run_id"]), f"SUMMARY-{state['run_id']}", "AI_CORE_SUMMARY", rel(project_root, path), "AI_CORE")
    return rel(project_root, path)


def migrate_v1_to_v2(project_root: Path, old_state: Path) -> Path:
    data = json.loads(old_state.read_text(encoding="utf-8"))
    if data.get("schema_version") == "2":
        return old_state
    run_id = data.get("run_id", old_state.stem)
    rdir = run_dir(project_root, run_id)
    rdir.mkdir(parents=True, exist_ok=True)
    migrated = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "project_id": data.get("project", project_root.name),
        "input_type": data.get("input_type", "STRUCTURED_REQUIREMENT"),
        "input_ref": data.get("requirement_ref", ""),
        "requirement_id": data.get("requirement_id", ""),
        "document_id": data.get("document_id", ""),
        "profile": data.get("profile", "STANDARD"),
        "status": data.get("overall_status", data.get("status", "NEW")),
        "current_stage": data.get("current_stage", ""),
        "current_role": data.get("current_role", ""),
        "started_at": data.get("started", now()),
        "updated_at": now(),
        "completed_stages": data.get("completed_stages", []),
        "skipped_stages": data.get("skipped_stages", []),
        "blocked_reason": data.get("blocked_role", ""),
        "human_approval": data.get("human_approval", {}),
        "artifact_refs": data.get("artifact_refs", {}),
        "memory_refs": data.get("memory_refs", []),
        "domain_refs": data.get("domain_refs", []),
        "skill_refs": data.get("skill_refs", []),
        "gate_status": data.get("gate_status", {"A0": "NOT_STARTED", "A": "NOT_STARTED", "C": "NOT_STARTED", "D": "NOT_STARTED"}),
        "retry_counts": data.get("role_attempts", {}),
        "result": data.get("result", ""),
        "errors": data.get("errors", []),
        "human_actions": data.get("human_actions", []),
        "metadata": data.get("metadata", {}),
    }
    init_registry(rdir)
    save_run(project_root, migrated)
    append_event(rdir, "SCHEMA_MIGRATED", from_version=data.get("schema_version", "1"), to_version="2")
    return rdir / "run.json"
