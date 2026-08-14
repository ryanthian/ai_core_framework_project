#!/usr/bin/env python3
from __future__ import annotations

import argparse

from memorylib import (
    DECISION_STATUSES,
    add_common_args,
    decision_files,
    existing_ids,
    format_list,
    parse_frontmatter,
    project_root,
    read_entries,
    slugify,
    today,
    update_decision_index,
    write_frontmatter,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    parser.add_argument("--id")
    parser.add_argument("--title", required=True)
    parser.add_argument("--status", required=True, choices=sorted(DECISION_STATUSES))
    parser.add_argument("--scope", default="PROJECT", choices=["PROJECT", "WORKSPACE", "REUSABLE"])
    parser.add_argument("--related-requirement", default="")
    parser.add_argument("--related-knowledge", nargs="*", default=[])
    parser.add_argument("--related-commit-pr", default="")
    parser.add_argument("--supersedes", default="")
    parser.add_argument("--context", required=True)
    parser.add_argument("--problem", required=True)
    parser.add_argument("--decision", required=True)
    parser.add_argument("--why", required=True)
    parser.add_argument("--alternatives", default="")
    parser.add_argument("--consequences", default="")
    parser.add_argument("--risks", default="")
    parser.add_argument("--revisit-trigger", default="Requirement, architecture, policy, or production evidence changes.")
    args = parser.parse_args()

    root = project_root(args.project_root)
    entries = read_entries(decision_files(root))
    ids = existing_ids(entries)
    did = args.id or __import__("memorylib").next_id(ids, "ADR")
    if did in ids:
        raise SystemExit(f"FAIL duplicate decision id: {did}")

    path = root / ".ai" / "decisions" / f"{did}-{slugify(args.title)}.md"
    if path.exists():
        raise SystemExit(f"FAIL refusing to overwrite: {path}")

    if args.supersedes:
        superseded = [item for item in entries if item[1].get("id") == args.supersedes]
        if not superseded:
            raise SystemExit(f"FAIL supersedes target not found: {args.supersedes}")
        old_path, old_meta, old_body = superseded[0]
        old_meta["status"] = "SUPERSEDED"
        old_meta["superseded_by"] = did
        write_frontmatter(old_path, old_meta, old_body)

    meta = {
        "id": did,
        "title": args.title,
        "date": today(),
        "status": args.status,
        "scope": args.scope,
        "related_requirement": args.related_requirement,
        "related_knowledge": format_list(args.related_knowledge),
        "related_commit_pr": args.related_commit_pr,
        "supersedes": args.supersedes,
        "superseded_by": "",
    }
    body = f"""# Context

{args.context}

# Problem

{args.problem}

# Decision

{args.decision}

# Why

{args.why}

# Alternatives

{args.alternatives}

# Consequences

{args.consequences}

# Risks

{args.risks}

# Revisit Trigger

{args.revisit_trigger}
"""
    write_frontmatter(path, meta, body)
    update_decision_index(root)
    print(f"PASS created {did} {path}")
    if args.supersedes:
        print(f"PASS superseded {args.supersedes} by {did}")


if __name__ == "__main__":
    main()
