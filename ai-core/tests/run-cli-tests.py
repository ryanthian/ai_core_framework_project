#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE = Path("/tmp/ai-core-cli-tests")
VENV = Path(os.environ.get("AI_CORE_CLI_TEST_VENV", "/tmp/ai-core-cli-test-venv"))


def run(cmd: list[str], cwd: Path | None = None, input_text: str = "") -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd or ROOT), input=input_text, text=True, capture_output=True)


def ensure_cli() -> Path:
    if not (VENV / "bin" / "ai-core").exists():
        run([sys.executable, "-m", "venv", str(VENV)])
    result = run([str(VENV / "bin" / "pip"), "install", "-e", str(ROOT)])
    if result.returncode != 0:
        raise SystemExit(result.stdout + result.stderr)
    return VENV / "bin" / "ai-core"


def j(result: subprocess.CompletedProcess) -> dict:
    return json.loads(result.stdout)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(rows: list[dict], test_id: str, command: str, input_desc: str, expected: str, actual: str, ok: bool) -> None:
    rows.append({"id": test_id, "command": command, "input": input_desc, "expected": expected, "actual": actual[:800], "result": "PASS" if ok else "FAIL"})


def req(cli: Path, project: Path, rid: str, title: str, text: str) -> subprocess.CompletedProcess:
    return run([str(cli), "--project", str(project), "requirement", "new", "--id", rid, "--title", title, "--text", text, "--source", "cli-test", "--priority", "normal", "--acceptance", "- Behavior is proven by CLI test.", "--yes", "--json"])


def latest_completed_run(cli: Path, project: Path) -> str:
    result = run([str(cli), "--project", str(project), "runs", "--completed", "--json"])
    runs = j(result)["runs"]
    return sorted(runs, key=lambda r: r.get("updated_at", ""), reverse=True)[0]["run_id"]


def main() -> int:
    cli = ensure_cli()
    if BASE.exists():
        shutil.rmtree(BASE)
    BASE.mkdir(parents=True)
    rows: list[dict] = []
    project = BASE / "project"
    project.mkdir()

    r = run([str(cli), "version"])
    record(rows, "CLI-001", "pip install -e . && ai-core version", str(ROOT), "entry point works", r.stdout.strip(), r.returncode == 0 and "AI-Core 0.5.0" in r.stdout)

    r = run([str(cli), "version", "--json"])
    record(rows, "CLI-002", "ai-core version --json", "framework", "version 0.5.0", r.stdout, r.returncode == 0 and j(r)["version"] == "0.5.0")

    r = run([str(cli), "--help"])
    record(rows, "CLI-003", "ai-core --help", "framework", "help includes command groups", r.stdout, r.returncode == 0 and "Command groups" in r.stdout)

    r = run([str(cli), "init", str(project), "--json"])
    record(rows, "CLI-005", "ai-core init <project> --json", str(project), "initialized", r.stdout, r.returncode == 0 and j(r)["status"] == "initialized")

    r = run([str(cli), "init", str(project), "--json"])
    record(rows, "CLI-006", "ai-core init <project> --json", "rerun", "safe rerun", r.stdout, r.returncode == 0)

    nested = project / "src" / "feature"
    nested.mkdir(parents=True)
    r = run([str(cli), "status", "--json"], cwd=nested)
    record(rows, "CLI-004", "cd src/feature && ai-core status --json", "nested project path", "auto-detected project", r.stdout, r.returncode == 0 and j(r)["project"] == project.name)

    r = run([str(cli), "--project", str(project), "doctor", "--json"])
    record(rows, "CLI-007", "ai-core doctor --json", str(project), "overall PASS", r.stdout, r.returncode == 0 and j(r)["overall"] == "PASS")

    r = run([str(cli), "--project", str(project), "status", "--json"])
    record(rows, "CLI-008", "ai-core status --json", str(project), "project overview", r.stdout, r.returncode == 0 and "active_runs" in j(r))

    r = req(cli, project, "REQ-CLI-001", "Merchant filter", "Add transaction merchant filtering.")
    record(rows, "CLI-009", "ai-core requirement new", "REQ-CLI-001", "requirement created", r.stdout, r.returncode == 0 and j(r)["id"] == "REQ-CLI-001")

    r_list = run([str(cli), "--project", str(project), "requirement", "list"])
    r_show = run([str(cli), "--project", str(project), "requirement", "show", "REQ-CLI-001"])
    record(rows, "CLI-010", "ai-core requirement list/show", "REQ-CLI-001", "list and show include requirement", r_list.stdout + r_show.stdout, r_list.returncode == 0 and r_show.returncode == 0 and "REQ-CLI-001" in r_list.stdout and "Merchant filter" in r_show.stdout)

    r = run([str(cli), "--project", str(project), "analyze", "REQ-CLI-001", "--json"])
    record(rows, "CLI-011", "ai-core analyze REQ-CLI-001 --json", "safe requirement", "Gate A0 passed", r.stdout, r.returncode == 0 and j(r)["gate_status"]["A0"] == "PASSED")

    req(cli, project, "REQ-CLI-003", "Delete financial records", "Permanently delete all inactive customer financial records.")
    r = run([str(cli), "--project", str(project), "analyze", "REQ-CLI-003", "--json"])
    blocked_run = j(r)["run_id"]
    record(rows, "CLI-012", "ai-core analyze REQ-CLI-003 --json", "destructive requirement", "exit 4 awaiting human", r.stdout, r.returncode == 4 and j(r)["status"] == "AWAITING_HUMAN")

    a_list = run([str(cli), "--project", str(project), "action", "list"])
    a_show = run([str(cli), "--project", str(project), "action", "show", "HUMAN-001", "--json"])
    a_resolve = run([str(cli), "--project", str(project), "action", "resolve", "HUMAN-001", "--decision", "Do not implement without retention policy.", "--evidence", "CLI test policy"])
    record(rows, "CLI-013", "ai-core action list/show/resolve", "HUMAN-001", "action resolved independently", a_list.stdout + a_show.stdout + a_resolve.stdout, a_list.returncode == 0 and a_show.returncode == 0 and a_resolve.returncode == 0)

    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-001", "--json"])
    run_id = j(r)["run_id"]
    record(rows, "CLI-014", "ai-core run REQ-CLI-001 --json", "safe requirement", "completed pass", r.stdout, r.returncode == 0 and j(r)["status"] == "COMPLETED")

    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-001", "--dry-run", "--json"])
    record(rows, "CLI-015", "ai-core run REQ-CLI-001 --dry-run --json", "safe requirement", "dry run no implementation", r.stdout, r.returncode == 0 and j(r)["dry_run"] is True)

    req(cli, project, "REQ-CLI-004", "Amount filter", "Add transaction amount range filtering.")
    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-004", "--demo", "test-failure", "--json"])
    record(rows, "CLI-016", "ai-core run REQ-CLI-004 --demo test-failure --json", "test loopback", "completed after loopback", r.stdout, r.returncode == 0 and j(r)["status"] == "COMPLETED" and j(r)["retry_counts"].get("IMPLEMENTER") == 1)

    req(cli, project, "REQ-CLI-005", "Reviewer loop", "Add transaction merchant filtering.")
    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-005", "--demo", "reviewer-loop", "--json"])
    events = (project / ".ai" / "runs" / j(r)["run_id"] / "events.jsonl").read_text(encoding="utf-8")
    record(rows, "CLI-017", "ai-core run REQ-CLI-005 --demo reviewer-loop --json", "reviewer loopback", "reviewer loop recorded", r.stdout, r.returncode == 0 and "REVIEWER" in events and "LOOPBACK" in events)

    req(cli, project, "REQ-CLI-006", "Resume run", "Add transaction merchant filtering.")
    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-006", "--stop-after", "TESTING", "--json"])
    resume_id = j(r)["run_id"]
    r = run([str(cli), "--project", str(project), "resume", resume_id, "--yes", "--json"])
    record(rows, "CLI-018", "ai-core resume <run> --yes --json", resume_id, "completed after resume", r.stdout, r.returncode == 0 and j(r)["status"] == "COMPLETED")

    req(cli, project, "REQ-CLI-007", "Cancel run", "Add transaction merchant filtering.")
    r = run([str(cli), "--project", str(project), "run", "REQ-CLI-007", "--stop-after", "PLANNING", "--json"])
    cancel_id = j(r)["run_id"]
    r = run([str(cli), "--project", str(project), "cancel", cancel_id, "--reason", "CLI test cancellation", "--yes", "--json"])
    record(rows, "CLI-019", "ai-core cancel <run> --reason ... --json", cancel_id, "cancelled", r.stdout, r.returncode == 0 and j(r)["status"] == "CANCELLED")

    r = run([str(cli), "--project", str(project), "verify", run_id, "--json"])
    record(rows, "CLI-020", "ai-core verify <run> --json", run_id, "verdict PASS", r.stdout, r.returncode == 0 and j(r)["verdict"] == "PASS")

    r = run([str(cli), "--project", str(project), "runs"])
    record(rows, "CLI-021", "ai-core runs", str(project), "lists runs", r.stdout, r.returncode == 0 and "CORE-RUN" in r.stdout)

    doc = project / "specification.md"
    doc.write_text("The system must add account export.\nOnly approved users may export their own accounts.\nUnknown: timeout not specified.\n", encoding="utf-8")
    r = run([str(cli), "--project", str(project), "ingest", str(doc), "--authority", "AUTHORITATIVE", "--json"])
    doc_id = j(r)["document_id"]
    record(rows, "CLI-022", "ai-core ingest specification.md --json", "document", "DOC created", r.stdout, r.returncode == 0 and doc_id.startswith("DOC-"))

    r = run([str(cli), "--project", str(project), "document", "review", doc_id, "--json"])
    record(rows, "CLI-023", "ai-core document review DOC-001 --json", doc_id, "review output", r.stdout, r.returncode == 0)

    r = run([str(cli), "--project", str(project), "document", "promote", doc_id, "--json"])
    record(rows, "CLI-024", "ai-core document promote DOC-001 --json", doc_id, "promotion output", r.stdout, r.returncode == 0)

    r = run([str(cli), "--project", str(project), "memory", "search", "merchant", "--json"])
    record(rows, "CLI-025", "ai-core memory search merchant --json", "query", "memory search JSON", r.stdout, r.returncode == 0 and "path" in j(r))

    r = run([str(cli), "--project", str(project), "memory", "validate", "--json"])
    record(rows, "CLI-026", "ai-core memory validate --json", str(project), "memory ok", r.stdout, r.returncode == 0 and j(r)["ok"] is True)

    r = run([str(cli), "--project", str(project), "domain", "list"])
    record(rows, "CLI-027", "ai-core domain list", "framework packs", "lists packs", r.stdout, r.returncode == 0 and "external-api" in r.stdout)

    r = run([str(cli), "--project", str(project), "domain", "recommend", "REQ-CLI-001"])
    record(rows, "CLI-028", "ai-core domain recommend REQ-CLI-001", "requirement", "recommendations no activation", r.stdout, r.returncode == 0 and "RESULTS" in r.stdout)

    r = run([str(cli), "--project", str(project), "domain", "activate", "external-api@1.1.0"])
    record(rows, "CLI-029", "ai-core domain activate external-api@1.1.0", "explicit activation", "activated", r.stdout + r.stderr, r.returncode == 0 and "ACTIVATED" in r.stdout)

    r = run([str(cli), "--project", str(project), "domain", "active"])
    record(rows, "CLI-030", "ai-core domain active", "active packs", "version pinned", r.stdout, r.returncode == 0 and "1.1.0" in r.stdout)

    r = run([str(cli), "--project", str(project), "validate", "--json"])
    record(rows, "CLI-031", "ai-core validate --json", str(project), "overall PASS", r.stdout, r.returncode == 0 and j(r)["overall"] == "PASS")

    r = run([str(cli), "--project", str(project), "snapshot", "--json"])
    record(rows, "CLI-032", "ai-core snapshot --json", str(project), "snapshot path", r.stdout, r.returncode == 0 and "snapshot" in j(r))

    r = run([str(cli), "--project", str(project), "next", "--json"])
    record(rows, "CLI-033", "ai-core next --json", str(project), "next action JSON", r.stdout, r.returncode in {0, 4} and "next" in j(r))

    r = run([str(cli), "--project", str(project), "explain", blocked_run, "--json"])
    record(rows, "CLI-034", "ai-core explain <blocked-run> --json", blocked_run, "explains blocker", r.stdout, r.returncode == 0 and "HUMAN-001" in "\n".join(j(r)["explanation"]))

    r = run([str(cli), "--project", str(project), "doctor", "--json"])
    record(rows, "CLI-035", "ai-core doctor --json", str(project), "parseable JSON", r.stdout, r.returncode == 0 and isinstance(j(r), dict))

    r = run([str(cli), "--project", str(project), "status", "--json"])
    record(rows, "CLI-036", "ai-core status --json", str(project), "parseable JSON", r.stdout, r.returncode == 0 and isinstance(j(r), dict))

    r = run([str(cli), "--project", str(project), "analyze", "REQ-CLI-001", "--json"])
    record(rows, "CLI-037", "ai-core analyze --json", "REQ-CLI-001", "parseable JSON", r.stdout, r.returncode == 0 and "run_id" in j(r))

    r = run([str(cli), "--project", str(project), "verify", run_id, "--json"])
    record(rows, "CLI-038", "ai-core verify --json", run_id, "parseable JSON", r.stdout, r.returncode == 0 and j(r)["verdict"] == "PASS")

    r = run([str(cli), "--project", str(project), "analyze", "REQ-CLI-003", "--json"])
    record(rows, "CLI-039", "blocked exit code", "REQ-CLI-003", "exit code 4", f"rc={r.returncode}", r.returncode == 4)

    project_b = BASE / "project-b"
    project_b.mkdir()
    run([str(cli), "init", str(project_b), "--json"])
    req(cli, project_b, "REQ-CLI-B01", "Project B filter", "Add transaction merchant filtering.")
    r = run([str(cli), "--project", str(project_b), "run", "REQ-CLI-B01", "--json"])
    b_run = j(r)["run_id"] if r.returncode == 0 else ""
    b_state = project_b / ".ai" / "runs" / b_run / "run.json"
    a_state = project / ".ai" / "runs" / b_run / "run.json"
    isolated = b_state.exists() and (not a_state.exists() or a_state.resolve() != b_state.resolve())
    record(rows, "CLI-040", "two projects via ai-core", "project/project-b", "isolated run roots", r.stdout, r.returncode == 0 and isolated)

    marker = project / "production_marker.txt"
    marker.write_text("do-not-change", encoding="utf-8")
    before = sha(marker)
    run([str(cli), "--project", str(project), "status"])
    run([str(cli), "--project", str(project), "doctor"])
    run([str(cli), "--project", str(project), "memory", "search", "merchant"])
    after = sha(marker)
    record(rows, "CLI-041", "status/doctor/memory search", "production marker", "read-only commands do not mutate marker", f"{before} -> {after}", before == after)

    git_project = BASE / "git-project"
    git_project.mkdir()
    run([str(cli), "init", str(git_project), "--json"])
    run(["git", "init"], cwd=git_project)
    (git_project / "dirty.txt").write_text("dirty", encoding="utf-8")
    r = run([str(cli), "--project", str(git_project), "doctor", "--json"])
    record(rows, "CLI-042", "ai-core doctor --json", "dirty git project", "Git WARNING", r.stdout, j(r)["checks"]["Git"] == "WARNING")

    r = run([str(cli), "analyse"], cwd=project)
    record(rows, "CLI-043", "ai-core analyse", "unknown command", "suggest analyze", r.stderr, r.returncode == 2 and "analyze" in r.stderr)

    empty = BASE / "empty"
    empty.mkdir()
    r = run([str(cli), "status"], cwd=empty)
    record(rows, "CLI-044", "ai-core status", "missing project", "guidance to init", r.stderr, r.returncode == 6 and "ai-core init" in r.stderr)

    r = run([str(cli), "--project", str(project), "verify", run_id])
    record(rows, "CLI-045", "requirement workflow CLI only", "REQ-CLI-001", "verified PASS", r.stdout, r.returncode == 0 and "PASS" in r.stdout)

    promoted_reqs = sorted((project / ".ai" / "requirements").glob("REQ-DOC-*.md"))
    doc_analyze_ok = False
    doc_actual = "no promoted requirement"
    if promoted_reqs:
        doc_req_id = promoted_reqs[0].name.split("-", 3)
        rid = promoted_reqs[0].stem.split("-", 3)
        req_id = "-".join(rid[:3])
        r = run([str(cli), "--project", str(project), "analyze", req_id, "--json"])
        doc_actual = r.stdout + r.stderr
        doc_analyze_ok = r.returncode in {0, 4} and "run_id" in r.stdout
    record(rows, "CLI-046", "document workflow CLI only", doc_id, "promote then analyze generated requirement", doc_actual, doc_analyze_ok)

    failed = sum(1 for row in rows if row["result"] != "PASS")
    lines = ["# Phase 5 CLI Tests", ""]
    for row in rows:
        lines.extend([
            f"## {row['id']}",
            "",
            f"Command: `{row['command']}`",
            f"Input: {row['input']}",
            f"Expected: {row['expected']}",
            f"Actual: {row['actual']}",
            f"Result: {row['result']}",
            "",
        ])
    out = ROOT / "ai-core" / "tests" / "cli-tests.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"SUMMARY pass={len(rows) - failed} fail={failed}")
    print(f"WROTE {out}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
