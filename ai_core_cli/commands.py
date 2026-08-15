from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from . import FRAMEWORK_PHASE, SCHEMA_VERSION, __version__
from .formatting import EXIT_BLOCKED, EXIT_CONFIG, EXIT_FAILURE, EXIT_INVALID, EXIT_SUCCESS, EXIT_VALIDATION, EXIT_VERIFY, FAIL, HUMAN, PASS, WARN, emit_json, print_table, status_exit
from .project import FRAMEWORK_ROOT, TEMPLATE_ROOT, ProjectNotFound, framework_git_info, git_info, resolve_project, run_subprocess

from controller import analyze as runtime_analyze
from controller import cancel as runtime_cancel
from controller import health as runtime_health
from controller import resume as runtime_resume
from controller import run as runtime_run
from controller import snapshot as runtime_snapshot
from project_service import ensure_project
from run_service import load_run, run_dir, snapshot as run_snapshot
import document_service
import domain_service
import memory_service
import validation_service


def now_date() -> str:
    return datetime.utcnow().date().isoformat()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def project_or_error(args, require: bool = True) -> Path:
    return resolve_project(getattr(args, "project", None), require=require)


def init(args) -> int:
    target = Path(args.path or os.getcwd()).resolve()
    target.mkdir(parents=True, exist_ok=True)
    script = TEMPLATE_ROOT / "scripts" / "init-ai-project.sh"
    cmd = [str(script), str(target), "--skills-root", str(FRAMEWORK_ROOT / "codex-skills")]
    if not script.exists():
        print(f"{FAIL} initializer not found: {script}")
        return EXIT_CONFIG
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return EXIT_FAILURE
    ensure_project(target, FRAMEWORK_ROOT)
    checks = [
        ("Project metadata", target / ".ai" / "project.json"),
        ("AI workspace", target / ".ai"),
        ("Memory", target / ".ai" / "knowledge" / "index.md"),
        ("Documents", target / ".ai" / "documents" / "index.md"),
        ("Agent Harness", target / ".ai" / "agents"),
        ("Domain configuration", target / ".ai" / "domain-packs.yaml"),
        ("Runtime configuration", target / ".ai" / "ai-core.yaml"),
        ("Skills", target / ".agents" / "skills"),
    ]
    if args.json:
        return emit_json({"status": "initialized", "project": target.name, "root": str(target), "checks": {name: path.exists() for name, path in checks}})
    print("AI-Core initialized\n")
    print(f"Project: {target.name}")
    print(f"Root: {target}\n")
    for name, path in checks:
        print(f"✓ {name}" if path.exists() else f"✗ {name}")
    print("\nNext:\n  ai-core doctor")
    return EXIT_SUCCESS


def doctor(args) -> int:
    project = project_or_error(args)
    verdict, messages = runtime_health(project)
    g = git_info(project)
    rows = [
        ["Project", "PASS" if (project / ".ai" / "project.json").exists() else "FAIL"],
        ["Runtime", "PASS" if (project / ".ai" / "ai-core.yaml").exists() else "FAIL"],
        ["Skills", "PASS" if (FRAMEWORK_ROOT / "codex-skills").exists() else "FAIL"],
        ["Memory", "PASS" if any("memory validator" in m and m.startswith("PASS") for m in messages) else "WARN"],
        ["Documents", "PASS" if (project / ".ai" / "documents").exists() else "FAIL"],
        ["Domain Packs", "PASS" if (FRAMEWORK_ROOT / "domain-packs").exists() else "FAIL"],
        ["Agent Harness", "PASS" if any("agent contracts" in m and m.startswith("PASS") for m in messages) else "FAIL"],
        ["Validators", verdict],
        ["Git", "PASS" if not g.get("repository") or not g.get("dirty") else "WARNING"],
    ]
    overall = "FAIL" if any(row[1] == "FAIL" for row in rows) else ("WARNING" if any(row[1] == "WARNING" for row in rows) or verdict == "WARN" else "PASS")
    if args.json:
        return emit_json({"overall": overall, "checks": {row[0]: row[1] for row in rows}, "messages": messages, "git": g}, 0 if overall != "FAIL" else EXIT_CONFIG)
    print("AI-Core Doctor\n")
    print_table(["Check", "Result"], rows + [["Overall", overall]])
    if args.verbose:
        print("\nDetails")
        for message in messages:
            print(f"- {message}")
        if g.get("repository"):
            print(f"- Git branch: {g.get('branch')} dirty={g.get('dirty')}")
    return 0 if overall != "FAIL" else EXIT_CONFIG


def list_run_states(project: Path) -> list[dict]:
    rows = []
    for path in sorted((project / ".ai" / "runs").glob("CORE-RUN-*/run.json")):
        try:
            rows.append(load_json(path))
        except Exception:
            continue
    return rows


def latest_run(project: Path) -> dict | None:
    rows = list_run_states(project)
    return sorted(rows, key=lambda item: item.get("updated_at", ""), reverse=True)[0] if rows else None


def status(args) -> int:
    project = project_or_error(args)
    if args.run_id:
        state = load_run(project, args.run_id)
        if args.json:
            return emit_json(state, status_exit(state["status"]))
        print(f"AI-Core Status\n\nProject: {state['project_id']}\nRun: {state['run_id']}\nRequirement: {state.get('requirement_id', '')}\nStage: {state.get('current_stage', '')}\nProfile: {state.get('profile', '')}\nStatus: {state.get('status', '')}\nGate Status: {state.get('gate_status', {})}\nHuman Action: {state.get('human_approval', {}).get('task_id', 'None')}\n")
        return status_exit(state["status"])
    runs = list_run_states(project)
    actions = action_rows(project, only_open=True)
    docs = list((project / ".ai" / "documents" / "manifests").glob("DOC-*.json")) if (project / ".ai" / "documents" / "manifests").exists() else []
    knowledge = list((project / ".ai" / "knowledge").glob("KNOW-*.md")) if (project / ".ai" / "knowledge").exists() else []
    active = [r for r in runs if r.get("status") in {"NEW", "ANALYZING", "READY", "RUNNING", "AWAITING_HUMAN", "BLOCKED"}]
    latest = latest_run(project)
    payload = {"project": project.name, "active_runs": len(active), "awaiting_human": len(actions), "completed": sum(1 for r in runs if r.get("status") == "COMPLETED"), "knowledge_entries": len(knowledge), "documents": len(docs), "latest_run": latest}
    if args.json:
        return emit_json(payload)
    print("AI-Core Status\n")
    print(f"Project\n{project.name}\n")
    print(f"Active Runs\n{len(active)}\n")
    print(f"Awaiting Human\n{len(actions)}\n")
    print(f"Completed Recently\n{payload['completed']}\n")
    print(f"Knowledge\n{len(knowledge)} active entries\n")
    print(f"Documents\n{len(docs)} manifests\n")
    if latest:
        print(f"Latest Run\n{latest['run_id']}\n\nRequirement\n{latest.get('requirement_id', '')}\n\nStage\n{latest.get('current_stage', '')}\n\nProfile\n{latest.get('profile', '')}\n\nHuman Action\n{latest.get('human_approval', {}).get('task_id', 'None')}")
    return EXIT_SUCCESS


def next_requirement_id(project: Path, prefix: str = "REQ") -> str:
    nums = []
    for path in (project / ".ai" / "requirements").glob("REQ-*.md"):
        stem = path.stem
        parts = stem.split("-")
        if len(parts) >= 2 and parts[1].isdigit():
            nums.append(int(parts[1]))
    return f"{prefix}-{(max(nums) + 1) if nums else 1:03d}"


def requirement_new(args) -> int:
    project = project_or_error(args)
    title = args.title or input("Title: ").strip()
    if args.from_file:
        requirement = Path(args.from_file).read_text(encoding="utf-8").strip()
    else:
        requirement = args.text or input("Requirement: ").strip()
    source = args.source or ("" if args.yes else input("Source: ").strip())
    priority = args.priority or ("" if args.yes else input("Priority: ").strip())
    acceptance = args.acceptance or ""
    rid = args.id or next_requirement_id(project)
    path = project / ".ai" / "requirements" / f"{rid}-{slug(title)}.md"
    if path.exists():
        print(f"{FAIL} requirement already exists: {path}")
        return EXIT_INVALID
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\nid: {rid}\ntitle: {title}\nstatus: ACTIVE\ncreated: {now_date()}\nsource: {source}\npriority: {priority}\n---\n\n# Requirement\n\n{requirement}\n\n# Acceptance Criteria\n\n{acceptance or '- Not specified.'}\n\n# Notes\n\n{args.notes or '- None.'}\n", encoding="utf-8")
    if args.json:
        return emit_json({"id": rid, "path": str(path.relative_to(project))})
    print(f"Created requirement {rid}\n{path.relative_to(project)}")
    return EXIT_SUCCESS


def slug(text: str) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "-", text.lower()).strip("-")[:70] or "requirement"


def requirement_list(args) -> int:
    project = project_or_error(args)
    rows = []
    for path in sorted((project / ".ai" / "requirements").glob("REQ-*.md")):
        meta = parse_frontmatter(path)
        rows.append([meta.get("id", path.stem), meta.get("title", path.stem), meta.get("status", ""), str(path.relative_to(project))])
    if args.json:
        return emit_json({"requirements": rows})
    print_table(["ID", "Title", "Status", "Path"], rows)
    return EXIT_SUCCESS


def requirement_show(args) -> int:
    project = project_or_error(args)
    path = find_id_file(project / ".ai" / "requirements", args.requirement_id)
    if not path:
        print(f"{FAIL} {args.requirement_id} not found.\n\nRun:\n  ai-core requirement list")
        return EXIT_INVALID
    if args.json:
        return emit_json({"id": args.requirement_id, "path": str(path.relative_to(project)), "content": path.read_text(encoding="utf-8")})
    print(path.read_text(encoding="utf-8"))
    return EXIT_SUCCESS


def parse_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta


def find_id_file(folder: Path, item_id: str) -> Path | None:
    if not folder.exists():
        return None
    for path in sorted(folder.glob("*.md")):
        meta = parse_frontmatter(path)
        if meta.get("id") == item_id or path.stem.startswith(item_id):
            return path
    for path in sorted(folder.glob("*.json")):
        try:
            data = load_json(path)
        except Exception:
            continue
        if item_id in {data.get("run_id"), data.get("task_id"), data.get("document_id")}:
            return path
    return None


def requirement_to_ref(project: Path, rid: str) -> str | None:
    path = find_id_file(project / ".ai" / "requirements", rid)
    return str(path.relative_to(project)) if path else None


def analyze(args) -> int:
    project = project_or_error(args)
    input_ref = requirement_to_ref(project, args.requirement) or args.requirement
    if not (project / input_ref).exists():
        print(f"{FAIL} {args.requirement} not found.\n\nRun:\n  ai-core requirement list")
        return EXIT_INVALID
    state = runtime_analyze(project, input_ref, "STRUCTURED_REQUIREMENT", args.profile)
    if args.json:
        return emit_json(state, status_exit(state["status"]))
    print("AI-Core Analysis\n")
    print(f"Requirement\n{state.get('requirement_id')}\n")
    print(f"Recommended Profile\n{state.get('profile')}\n")
    print(f"Gate A0\n{state.get('gate_status', {}).get('A0')}\n")
    if state.get("human_actions"):
        print("Human Action Required\n")
        for action in state["human_actions"]:
            print(f"- {action}")
    print(f"\nRun:\n{state['run_id']}")
    return status_exit(state["status"])


def run(args) -> int:
    project = project_or_error(args)
    input_ref = requirement_to_ref(project, args.requirement) or args.requirement
    if args.dry_run:
        state = runtime_analyze(project, input_ref, "STRUCTURED_REQUIREMENT", args.profile)
        if args.json:
            return emit_json({"dry_run": True, "run": state}, status_exit(state["status"]))
        print("AI-Core Dry Run\n")
        print(f"Requirement: {state.get('requirement_id')}")
        print(f"Memory: {', '.join(state.get('memory_refs', [])) or 'None'}")
        print(f"Domains: {', '.join(state.get('domain_refs', [])) or 'None'}")
        print(f"Skills: {', '.join(state.get('skill_refs', [])) or 'None'}")
        print(f"Gate A0: {state.get('gate_status', {}).get('A0')}")
        print(f"Human Actions: {', '.join(state.get('human_actions', [])) or 'None'}")
        return status_exit(state["status"])
    if git_info(project).get("dirty"):
        print(f"{WARN} Git working tree is dirty. AI-Core will not commit, stash, reset, or push.")
    state = runtime_run(project, input_ref, "STRUCTURED_REQUIREMENT", args.profile, args.demo, args.stop_after)
    if args.json:
        return emit_json(state, status_exit(state["status"]))
    print("AI-Core Run\n")
    print(state["run_id"])
    for stage in state.get("completed_stages", []):
        print(f"✓ {stage}")
    events = read_events(project, state["run_id"])
    loops = [e for e in events if e.get("event") == "LOOPBACK"]
    for loop in loops:
        print(f"\nLoopback:\n{loop.get('from_role')} → {loop.get('to_role')}")
    print(f"\nRESULT: {state.get('result') or state.get('status')}")
    return status_exit(state["status"])


def read_events(project: Path, run_id: str) -> list[dict]:
    path = project / ".ai" / "runs" / run_id / "events.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def resume(args) -> int:
    project = project_or_error(args)
    state = load_run(project, args.run_id)
    if state.get("status") == "CANCELLED":
        print(f"{FAIL} {args.run_id} is CANCELLED and will not be resumed silently.")
        return EXIT_BLOCKED
    if not args.yes:
        print(f"Resuming {args.run_id}\n\nLast completed:\n{(state.get('completed_stages') or ['None'])[-1]}\n\nNext:\n{state.get('current_stage')}\n")
        answer = input("Continue? [y/N] ").strip().lower()
        if answer != "y":
            return EXIT_SUCCESS
    state = runtime_resume(project, args.run_id, args.demo)
    if args.json:
        return emit_json(state, status_exit(state["status"]))
    print(f"Resumed {state['run_id']}: {state['status']} {state.get('result', '')}")
    return status_exit(state["status"])


def cancel(args) -> int:
    project = project_or_error(args)
    reason = args.reason or input("Reason: ").strip()
    state = load_run(project, args.run_id)
    if state.get("status") == "RUNNING" and not args.yes:
        answer = input("Run is active. Cancel and preserve evidence? [y/N] ").strip().lower()
        if answer != "y":
            return EXIT_SUCCESS
    state = runtime_cancel(project, args.run_id, reason)
    if args.json:
        return emit_json(state)
    print(f"Cancelled {args.run_id}\nReason: {reason}")
    return EXIT_SUCCESS


def verify(args) -> int:
    project = project_or_error(args)
    state = load_run(project, args.run_id)
    rdir = run_dir(project, args.run_id)
    failures, warnings = validation_service.validate_artifacts(project, rdir, state)
    verdict = "PASS" if not failures and state.get("status") == "COMPLETED" and state.get("gate_status", {}).get("C") == "PASSED" else "FAIL"
    payload = {"run_id": args.run_id, "verdict": verdict, "failures": failures, "warnings": warnings, "gates": state.get("gate_status", {}), "status": state.get("status")}
    if args.json:
        return emit_json(payload, EXIT_SUCCESS if verdict == "PASS" else EXIT_VERIFY)
    print("Verification\n")
    print(f"Artifacts               {'PASS' if not failures else 'FAIL'}")
    print(f"Traceability            {'PASS' if (rdir / 'traceability.md').exists() else 'FAIL'}")
    print(f"Gates                   {state.get('gate_status')}")
    print(f"Critical Risks          {'0 OPEN' if not state.get('human_actions') else 'OPEN'}")
    print("\nFINAL VERDICT")
    print(verdict)
    return EXIT_SUCCESS if verdict == "PASS" else EXIT_VERIFY


def action_rows(project: Path, only_open: bool = False) -> list[dict]:
    rows = []
    for path in sorted((project / ".ai" / "human-actions").glob("HUMAN-*.json")):
        data = load_json(path)
        if only_open and data.get("status") != "OPEN":
            continue
        data["_path"] = path
        rows.append(data)
    return rows


def action_list(args) -> int:
    project = project_or_error(args)
    rows = action_rows(project)
    if args.json:
        return emit_json({"actions": [{k: str(v) if k == "_path" else v for k, v in row.items()} for row in rows]})
    print_table(["ID", "Status", "Run", "Reason"], [[r["task_id"], r["status"], r["run_id"], r["reason"][:70]] for r in rows])
    return EXIT_SUCCESS


def action_show(args) -> int:
    project = project_or_error(args)
    path = project / ".ai" / "human-actions" / f"{args.action_id}.json"
    if not path.exists():
        print(f"{FAIL} action not found: {args.action_id}")
        return EXIT_INVALID
    data = load_json(path)
    if args.json:
        return emit_json(data)
    print(json.dumps(data, indent=2, sort_keys=True))
    return EXIT_SUCCESS


def action_resolve(args) -> int:
    project = project_or_error(args)
    path = project / ".ai" / "human-actions" / f"{args.action_id}.json"
    if not path.exists():
        print(f"{FAIL} action not found: {args.action_id}")
        return EXIT_INVALID
    decision = args.decision or input("Decision / clarification: ").strip()
    evidence = args.evidence or input("Evidence or source: ").strip()
    if decision.lower().strip() in {"approve everything", "approve all"}:
        print(f"{FAIL} broad approval is not allowed for individual critical actions.")
        return EXIT_INVALID
    data = load_json(path)
    history = data.setdefault("resolution_history", [])
    history.append({"resolved_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z", "decision": decision, "evidence": evidence})
    data["status"] = "RESOLVED"
    write_json(path, data)
    if args.json:
        return emit_json(data)
    print(f"Resolved {args.action_id}")
    return EXIT_SUCCESS


def runs(args) -> int:
    project = project_or_error(args)
    rows = list_run_states(project)
    if args.active:
        rows = [r for r in rows if r.get("status") in {"NEW", "ANALYZING", "READY", "RUNNING", "AWAITING_HUMAN", "BLOCKED"}]
    if args.blocked:
        rows = [r for r in rows if r.get("status") in {"AWAITING_HUMAN", "BLOCKED"}]
    if args.completed:
        rows = [r for r in rows if r.get("status") == "COMPLETED"]
    if args.json:
        return emit_json({"runs": rows})
    print_table(["Run ID", "Requirement", "Profile", "Stage", "Status", "Updated", "Human Action"], [[r["run_id"], r.get("requirement_id", ""), r.get("profile", ""), r.get("current_stage", ""), r.get("status", ""), r.get("updated_at", ""), r.get("human_approval", {}).get("task_id", "")] for r in rows])
    return EXIT_SUCCESS


def ingest(args) -> int:
    project = project_or_error(args)
    file_path = Path(args.file).resolve()
    if not file_path.exists():
        print(f"{FAIL} file not found: {file_path}")
        return EXIT_INVALID
    target_rel = file_path.name
    if file_path.parent != project:
        target = project / ".ai" / "documents" / "inbox" / file_path.name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)
        target_rel = str(target.relative_to(project))
    try:
        doc_id, _out, duplicate = document_service.ingest(project, target_rel, args.title or file_path.stem, args.authority)
        if not duplicate:
            document_service.extract(project, doc_id)
            document_service.analyze(project, doc_id)
    except Exception as exc:
        print(f"{FAIL} {exc}")
        return EXIT_FAILURE
    refs = document_service.refs(project, doc_id)
    extracted = load_json(project / refs["extracted"]) if (project / refs["extracted"]).exists() else {"items": []}
    items = extracted.get("items", [])
    payload = {"document_id": doc_id, "duplicate": duplicate, "items": len(items), "unknowns": sum(1 for i in items if i.get("type") == "UNKNOWN"), "requirements": sum(1 for i in items if i.get("type") == "REQUIREMENT")}
    if args.json:
        return emit_json(payload)
    print(f"Document\n{doc_id}\n\nExtraction\nCOMPLETE\n\nRequirement Candidates\n{payload['requirements']}\n\nUnknowns\n{payload['unknowns']}\n\nReview\nREQUIRED\n\nNext:\nai-core document review {doc_id}")
    return EXIT_SUCCESS


def document_list(args) -> int:
    project = project_or_error(args)
    rows = []
    for path in sorted((project / ".ai" / "documents" / "manifests").glob("DOC-*.json")):
        data = load_json(path)
        rows.append([data["document_id"], data.get("title", ""), data.get("source_type", ""), data.get("status", ""), data.get("review_status", ""), data.get("promotion_status", "")])
    if args.json:
        return emit_json({"documents": rows})
    print_table(["ID", "Title", "Type", "Status", "Review", "Promotion"], rows)
    return EXIT_SUCCESS


def document_show(args) -> int:
    project = project_or_error(args)
    refs = document_service.refs(project, args.document_id)
    manifest = refs["manifest_data"]
    if args.json:
        return emit_json(manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    report = project / refs["intelligence"]
    if report.exists() and not args.quiet:
        print("\n" + "\n".join(report.read_text(encoding="utf-8").splitlines()[:80]))
    return EXIT_SUCCESS


def document_review(args) -> int:
    project = project_or_error(args)
    out = document_service.review(project, args.document_id)
    if args.json:
        return emit_json({"document_id": args.document_id, "output": out})
    print(out.strip())
    return EXIT_SUCCESS


def document_promote(args) -> int:
    project = project_or_error(args)
    out = document_service.promote(project, args.document_id)
    if args.json:
        return emit_json({"document_id": args.document_id, "output": out})
    print(out.strip())
    return EXIT_SUCCESS


def document_search(args) -> int:
    project = project_or_error(args)
    result = subprocess.run([sys.executable, str(project / "scripts" / "search-document-intelligence.py"), "--project", str(project), "--query", args.query], text=True, capture_output=True)
    if args.json:
        return emit_json({"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}, result.returncode)
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def memory_search(args) -> int:
    project = project_or_error(args)
    out = project / ".ai" / "context" / f"MEMORY-SEARCH-{slug(args.query)}.md"
    ok, text = memory_service.retrieve(project, project.name, args.query, str(out.relative_to(project)))
    if args.json:
        return emit_json({"ok": ok, "output": text, "path": str(out.relative_to(project))}, 0 if ok else EXIT_FAILURE)
    print("PROJECT KNOWLEDGE / PROJECT DECISION / DOMAIN RULE / DOCUMENT INTELLIGENCE\n")
    if out.exists():
        print(out.read_text(encoding="utf-8"))
    else:
        print(text)
    return 0 if ok else EXIT_FAILURE


def memory_show(args) -> int:
    project = project_or_error(args)
    path = find_id_file(project / ".ai" / "knowledge", args.memory_id) or find_id_file(project / ".ai" / "decisions", args.memory_id)
    if not path:
        print(f"{FAIL} memory/decision not found: {args.memory_id}")
        return EXIT_INVALID
    print(path.read_text(encoding="utf-8"))
    return EXIT_SUCCESS


def memory_validate(args) -> int:
    project = project_or_error(args)
    ok, out = memory_service.validate(project)
    if args.json:
        return emit_json({"ok": ok, "output": out}, 0 if ok else EXIT_VALIDATION)
    print(out)
    return 0 if ok else EXIT_VALIDATION


def memory_conflicts(args) -> int:
    project = project_or_error(args)
    ok, out = memory_service.validate(project)
    conflicts = [line for line in out.splitlines() if "MEMORY CONFLICT" in line or line.startswith("WARN Entry")]
    if args.json:
        return emit_json({"conflicts": conflicts}, 0 if ok else EXIT_VALIDATION)
    print("\n".join(conflicts) if conflicts else "No memory conflicts found.")
    return EXIT_SUCCESS if not conflicts else EXIT_VALIDATION


def domain_list(args) -> int:
    packs = []
    for manifest in sorted((FRAMEWORK_ROOT / "domain-packs").glob("*/manifest.json")):
        data = load_json(manifest)
        packs.append([data["id"], data["version"], data.get("status", "")])
    if args.json:
        return emit_json({"packs": packs})
    print_table(["Pack", "Version", "Status"], packs)
    return EXIT_SUCCESS


def domain_active(args) -> int:
    project = project_or_error(args)
    rows = []
    for row in domain_service.active(project):
        rows.append([row["manifest"]["id"], row["activation"]["version"], row["manifest"].get("status", ""), "VERSION_MISMATCH" if row.get("version_mismatch") else ""])
    if args.json:
        return emit_json({"active": rows})
    print_table(["Pack", "Version", "Status", "Notes"], rows)
    return EXIT_SUCCESS


def domain_recommend(args) -> int:
    project = project_or_error(args)
    req = requirement_to_ref(project, args.requirement) or args.requirement
    text = (project / req).read_text(encoding="utf-8") if (project / req).exists() else req
    result = subprocess.run([sys.executable, str(project / "scripts" / "recommend-domain-packs.py"), "--project", str(project), "--query", text], text=True, capture_output=True, env=framework_env())
    if args.json:
        return emit_json({"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}, result.returncode)
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def domain_activate(args) -> int:
    project = project_or_error(args)
    pack, version = parse_pack_version(args.pack)
    result = subprocess.run([sys.executable, str(project / "scripts" / "activate-domain-pack.py"), "--project", str(project), "--pack", pack, "--version", version], text=True, capture_output=True, env=framework_env())
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def domain_deactivate(args) -> int:
    project = project_or_error(args)
    path = project / ".ai" / "domain-packs.yaml"
    text = path.read_text(encoding="utf-8") if path.exists() else "active: []\n"
    lines = text.splitlines()
    out = []
    skip = 0
    for idx, line in enumerate(lines):
        if line.strip() == f"- pack: {args.pack}" or line.strip() == f"- pack: {args.pack.split('@')[0]}":
            skip = 3
            continue
        if skip:
            skip -= 1
            continue
        out.append(line)
    path.write_text("\n".join(out).strip() + "\n", encoding="utf-8")
    print(f"Deactivated {args.pack}")
    return EXIT_SUCCESS


def domain_upgrade(args) -> int:
    if not args.yes:
        answer = input("Domain upgrade may affect planning guidance. Continue? [y/N] ").strip().lower()
        if answer != "y":
            return EXIT_SUCCESS
    return domain_activate(args)


def parse_pack_version(value: str) -> tuple[str, str]:
    if "@" not in value:
        return value, "1.0.0"
    pack, version = value.split("@", 1)
    return pack, version


def validate(args) -> int:
    project = project_or_error(args)
    doctor_status, _messages = runtime_health(project)
    mem_ok, _ = memory_service.validate(project)
    agent_ok = (project / ".ai" / "agents").exists()
    runs_ok = True
    for state in list_run_states(project):
        failures, _warnings = validation_service.validate_artifacts(project, run_dir(project, state["run_id"]), state)
        runs_ok = runs_ok and not failures
    rows = [["Project", "PASS"], ["Memory", "PASS" if mem_ok else "FAIL"], ["Documents", "PASS" if (project / ".ai" / "documents").exists() else "FAIL"], ["Domains", "PASS" if (FRAMEWORK_ROOT / "domain-packs").exists() else "FAIL"], ["Agents", "PASS" if agent_ok else "FAIL"], ["Runs", "PASS" if runs_ok else "FAIL"]]
    overall = "PASS" if all(r[1] == "PASS" for r in rows) and doctor_status != "FAIL" else "FAIL"
    if args.json:
        return emit_json({"overall": overall, "checks": rows}, EXIT_SUCCESS if overall == "PASS" else EXIT_VALIDATION)
    print("Validation\n")
    print_table(["Area", "Result"], rows)
    print(f"\nSUMMARY\n{overall}")
    return EXIT_SUCCESS if overall == "PASS" else EXIT_VALIDATION


def snapshot(args) -> int:
    project = project_or_error(args)
    if args.run_id:
        state = load_run(project, args.run_id)
        snap = run_snapshot(project, state, "manual")
    else:
        target = project / ".ai" / "snapshots" / f"project-manual-{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
        target.mkdir(parents=True, exist_ok=False)
        for rel in [".ai/project.json", ".ai/ai-core.yaml", ".ai/knowledge/index.md", ".ai/decisions/index.md", ".ai/documents/index.md", ".ai/domain-packs.yaml"]:
            src = project / rel
            if src.exists():
                shutil.copy2(src, target / rel.replace("/", "__"))
        snap = str(target.relative_to(project))
    if args.json:
        return emit_json({"snapshot": snap})
    print(f"Snapshot created: {snap}")
    return EXIT_SUCCESS


def version(args) -> int:
    info = framework_git_info()
    payload = {"version": __version__, "framework_phase": FRAMEWORK_PHASE, "schema": SCHEMA_VERSION, "repository": "ai_core_framework_project", "git": info}
    if args.json:
        return emit_json(payload)
    print(f"AI-Core {__version__}\n\nFramework Phase\n{FRAMEWORK_PHASE}\n\nSchema\n{SCHEMA_VERSION}\n\nRepository\nai_core_framework_project")
    if info.get("repository"):
        print(f"\nCommit\n{info.get('commit')}")
    return EXIT_SUCCESS


def next_action(args) -> int:
    project = project_or_error(args)
    actions = action_rows(project, only_open=True)
    if actions:
        action = actions[0]
        if args.json:
            return emit_json({"next": "resolve_action", "action": action["task_id"], "reason": action["reason"]}, EXIT_BLOCKED)
        print(f"NEXT ACTION\n\nResolve {action['task_id']}\n\nReason:\n{action['reason']}\n\nRun:\nai-core action show {action['task_id']}")
        return EXIT_BLOCKED
    active = [r for r in list_run_states(project) if r.get("status") in {"READY", "RUNNING"}]
    if active:
        run = sorted(active, key=lambda r: r.get("updated_at", ""), reverse=True)[0]
        if args.json:
            return emit_json({"next": "resume", "run_id": run["run_id"]})
        print(f"NEXT ACTION\n\nResume {run['run_id']}\n\nCurrent stage:\n{run.get('current_stage')}\n\nRun:\nai-core resume {run['run_id']}")
        return EXIT_SUCCESS
    if args.json:
        return emit_json({"next": "none"})
    print("No active work.\n\nPossible next actions:\n- create requirement\n- ingest document")
    return EXIT_SUCCESS


def explain(args) -> int:
    project = project_or_error(args)
    state = load_run(project, args.run_id)
    lines = ["Why is this blocked?", ""]
    if state.get("blocked_reason"):
        lines.extend([state["blocked_reason"], ""])
    for action in state.get("human_actions", []):
        path = project / action
        if path.exists():
            data = load_json(path)
            lines.extend([f"Related: {data['task_id']}", f"Required action: Resolve {data['task_id']}.", ""])
    if not state.get("human_actions") and not state.get("blocked_reason"):
        lines.append("No blocker recorded.")
    if args.json:
        return emit_json({"run_id": args.run_id, "explanation": lines})
    print("\n".join(lines))
    return EXIT_SUCCESS


def open_ref(args) -> int:
    project = project_or_error(args)
    target = args.ref
    path = None
    if target.startswith("REQ-"):
        path = find_id_file(project / ".ai" / "requirements", target)
    elif target.startswith("RUN") or target.startswith("CORE-RUN"):
        path = project / ".ai" / "runs" / target / "run.json"
    elif target.startswith("KNOW"):
        path = find_id_file(project / ".ai" / "knowledge", target)
    elif target.startswith("DOC"):
        path = project / ".ai" / "documents" / "manifests" / f"{target}.json"
    if not path or not path.exists():
        print(f"{FAIL} reference not found: {target}")
        return EXIT_INVALID
    print(path)
    return EXIT_SUCCESS


def config_show(args) -> int:
    project = project_or_error(args)
    path = project / ".ai" / "ai-core.yaml"
    print(path.read_text(encoding="utf-8") if path.exists() else "")
    return EXIT_SUCCESS


def config_validate(args) -> int:
    project = project_or_error(args)
    path = project / ".ai" / "ai-core.yaml"
    ok = path.exists() and "schema_version:" in path.read_text(encoding="utf-8")
    if args.json:
        return emit_json({"valid": ok}, EXIT_SUCCESS if ok else EXIT_CONFIG)
    print("PASS" if ok else "FAIL")
    return EXIT_SUCCESS if ok else EXIT_CONFIG


def framework_env() -> dict:
    env = os.environ.copy()
    env.setdefault("AI_CORE_FRAMEWORK_ROOT", str(FRAMEWORK_ROOT))
    return env
