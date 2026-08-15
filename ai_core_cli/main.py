from __future__ import annotations

import argparse
import difflib
import sys

from . import __version__
from .formatting import EXIT_CONFIG, EXIT_FAILURE, EXIT_INVALID, emit_json
from .project import ProjectNotFound
from . import commands


COMMANDS = {
    "init",
    "doctor",
    "status",
    "requirement",
    "analyze",
    "run",
    "resume",
    "cancel",
    "verify",
    "action",
    "runs",
    "ingest",
    "document",
    "memory",
    "domain",
    "validate",
    "snapshot",
    "version",
    "next",
    "explain",
    "open",
    "config",
}


class SuggestingParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        parts = message.split()
        if "invalid choice:" in message and parts:
            bad = message.split("invalid choice:", 1)[1].split("(", 1)[0].strip().strip("'")
            matches = difflib.get_close_matches(bad, sorted(COMMANDS), n=3)
            if matches:
                self.print_usage(sys.stderr)
                self.exit(2, f"Unknown command: {bad}\n\nDid you mean:\n  " + "\n  ".join(matches) + "\n")
        super().error(message)


def add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--project", default=argparse.SUPPRESS, help="Project root. Defaults to auto-detecting .ai/project.json upward from cwd.")
    p.add_argument("--json", action="store_true", default=argparse.SUPPRESS, help="Emit machine-readable JSON.")
    p.add_argument("--quiet", action="store_true", default=argparse.SUPPRESS, help="Reduce human-readable output where supported.")


def build_parser() -> argparse.ArgumentParser:
    parser = SuggestingParser(
        prog="ai-core",
        description="AI-Core CLI & daily control plane.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Command groups:
  Project       init, doctor, status
  Requirements  requirement, analyze, run, resume, cancel, verify
  Documents     ingest, document
  Memory        memory
  Domains       domain
  Runs          runs
  Maintenance   validate, snapshot, version, next, explain, open, config
""",
    )
    add_common(parser)
    parser.set_defaults(project=None, json=False, quiet=False)
    parser.add_argument("--version", action="version", version=f"AI-Core {__version__}")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("init", help="Initialize AI-Core in a project.")
    add_common(p)
    p.add_argument("path", nargs="?")
    p.set_defaults(func=commands.init)

    p = sub.add_parser("doctor", help="Run project health checks.")
    add_common(p)
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=commands.doctor)

    p = sub.add_parser("status", help="Show project or run status.")
    add_common(p)
    p.add_argument("run_id", nargs="?")
    p.set_defaults(func=commands.status)

    req = sub.add_parser("requirement", help="Manage requirements.")
    add_common(req)
    req_sub = req.add_subparsers(dest="req_cmd", required=True)
    p = req_sub.add_parser("new")
    add_common(p)
    p.add_argument("--id")
    p.add_argument("--title")
    p.add_argument("--text")
    p.add_argument("--from-file")
    p.add_argument("--source")
    p.add_argument("--priority")
    p.add_argument("--acceptance")
    p.add_argument("--notes")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=commands.requirement_new)
    p = req_sub.add_parser("list")
    add_common(p)
    p.set_defaults(func=commands.requirement_list)
    p = req_sub.add_parser("show")
    add_common(p)
    p.add_argument("requirement_id")
    p.set_defaults(func=commands.requirement_show)

    p = sub.add_parser("analyze", help="Analyze a requirement through Gate A0.")
    add_common(p)
    p.add_argument("requirement")
    p.add_argument("--profile", default="AUTO")
    p.set_defaults(func=commands.analyze)

    p = sub.add_parser("run", help="Run a requirement through AI-Core.")
    add_common(p)
    p.add_argument("requirement")
    p.add_argument("--profile", default="AUTO")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--demo", choices=["structured", "document", "test-failure", "reviewer-loop"], default="structured")
    p.add_argument("--stop-after", default="")
    p.set_defaults(func=commands.run)

    p = sub.add_parser("resume", help="Resume a run.")
    add_common(p)
    p.add_argument("run_id")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--demo", choices=["structured", "document", "test-failure", "reviewer-loop"], default="structured")
    p.set_defaults(func=commands.resume)

    p = sub.add_parser("cancel", help="Cancel a run and preserve evidence.")
    add_common(p)
    p.add_argument("run_id")
    p.add_argument("--reason")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=commands.cancel)

    p = sub.add_parser("verify", help="Verify a run.")
    add_common(p)
    p.add_argument("run_id")
    p.set_defaults(func=commands.verify)

    act = sub.add_parser("action", help="Manage human actions.")
    add_common(act)
    act_sub = act.add_subparsers(dest="action_cmd", required=True)
    p = act_sub.add_parser("list")
    add_common(p)
    p.set_defaults(func=commands.action_list)
    p = act_sub.add_parser("show")
    add_common(p)
    p.add_argument("action_id")
    p.set_defaults(func=commands.action_show)
    p = act_sub.add_parser("resolve")
    add_common(p)
    p.add_argument("action_id")
    p.add_argument("--decision")
    p.add_argument("--evidence")
    p.set_defaults(func=commands.action_resolve)

    p = sub.add_parser("runs", help="List runs.")
    add_common(p)
    p.add_argument("--active", action="store_true")
    p.add_argument("--blocked", action="store_true")
    p.add_argument("--completed", action="store_true")
    p.set_defaults(func=commands.runs)

    p = sub.add_parser("ingest", help="Ingest and analyze a source document.")
    add_common(p)
    p.add_argument("file")
    p.add_argument("--title")
    p.add_argument("--authority", choices=["AUTHORITATIVE", "APPROVED", "WORKING_DRAFT", "REFERENCE", "UNVERIFIED"], default="UNVERIFIED")
    p.set_defaults(func=commands.ingest)

    doc = sub.add_parser("document", help="Manage documents.")
    add_common(doc)
    doc_sub = doc.add_subparsers(dest="doc_cmd", required=True)
    p = doc_sub.add_parser("list")
    add_common(p)
    p.set_defaults(func=commands.document_list)
    p = doc_sub.add_parser("show")
    add_common(p)
    p.add_argument("document_id")
    p.set_defaults(func=commands.document_show)
    p = doc_sub.add_parser("review")
    add_common(p)
    p.add_argument("document_id")
    p.set_defaults(func=commands.document_review)
    p = doc_sub.add_parser("promote")
    add_common(p)
    p.add_argument("document_id")
    p.set_defaults(func=commands.document_promote)
    p = doc_sub.add_parser("search")
    add_common(p)
    p.add_argument("query")
    p.set_defaults(func=commands.document_search)

    mem = sub.add_parser("memory", help="Search and validate memory.")
    add_common(mem)
    mem_sub = mem.add_subparsers(dest="mem_cmd", required=True)
    p = mem_sub.add_parser("search")
    add_common(p)
    p.add_argument("query")
    p.set_defaults(func=commands.memory_search)
    p = mem_sub.add_parser("show")
    add_common(p)
    p.add_argument("memory_id")
    p.set_defaults(func=commands.memory_show)
    p = mem_sub.add_parser("validate")
    add_common(p)
    p.set_defaults(func=commands.memory_validate)
    p = mem_sub.add_parser("conflicts")
    add_common(p)
    p.set_defaults(func=commands.memory_conflicts)

    dom = sub.add_parser("domain", help="Manage domain packs.")
    add_common(dom)
    dom_sub = dom.add_subparsers(dest="domain_cmd", required=True)
    p = dom_sub.add_parser("list")
    add_common(p)
    p.set_defaults(func=commands.domain_list)
    p = dom_sub.add_parser("active")
    add_common(p)
    p.set_defaults(func=commands.domain_active)
    p = dom_sub.add_parser("recommend")
    add_common(p)
    p.add_argument("requirement")
    p.set_defaults(func=commands.domain_recommend)
    p = dom_sub.add_parser("activate")
    add_common(p)
    p.add_argument("pack")
    p.set_defaults(func=commands.domain_activate)
    p = dom_sub.add_parser("deactivate")
    add_common(p)
    p.add_argument("pack")
    p.set_defaults(func=commands.domain_deactivate)
    p = dom_sub.add_parser("upgrade")
    add_common(p)
    p.add_argument("pack")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=commands.domain_upgrade)

    p = sub.add_parser("validate", help="Run project validations.")
    add_common(p)
    p.add_argument("--all", action="store_true")
    p.set_defaults(func=commands.validate)

    p = sub.add_parser("snapshot", help="Create project or run-state snapshot.")
    add_common(p)
    p.add_argument("run_id", nargs="?")
    p.set_defaults(func=commands.snapshot)

    p = sub.add_parser("version", help="Show framework version.")
    add_common(p)
    p.set_defaults(func=commands.version)

    p = sub.add_parser("next", help="Show next workflow action.")
    add_common(p)
    p.set_defaults(func=commands.next_action)

    p = sub.add_parser("explain", help="Explain a run blocker from evidence.")
    add_common(p)
    p.add_argument("run_id")
    p.set_defaults(func=commands.explain)

    p = sub.add_parser("open", help="Resolve a framework reference to a file path.")
    add_common(p)
    p.add_argument("ref")
    p.set_defaults(func=commands.open_ref)

    cfg = sub.add_parser("config", help="Show or validate config.")
    add_common(cfg)
    cfg_sub = cfg.add_subparsers(dest="config_cmd", required=True)
    p = cfg_sub.add_parser("show")
    add_common(p)
    p.set_defaults(func=commands.config_show)
    p = cfg_sub.add_parser("validate")
    add_common(p)
    p.set_defaults(func=commands.config_validate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except ProjectNotFound:
        if getattr(args, "json", False):
            return emit_json({"error": "PROJECT_NOT_FOUND", "message": "AI-Core project not found. Run: ai-core init"}, EXIT_CONFIG)
        print("AI-Core project not found.\n\nRun:\n  ai-core init", file=sys.stderr)
        return EXIT_CONFIG
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return EXIT_FAILURE
    except Exception as exc:
        if getattr(args, "json", False):
            return emit_json({"error": exc.__class__.__name__, "message": str(exc)}, EXIT_FAILURE)
        print(f"AI-Core error: {exc}", file=sys.stderr)
        return EXIT_FAILURE


if __name__ == "__main__":
    raise SystemExit(main())
