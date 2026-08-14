#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from memorylib import (
    CONFIDENCES,
    KNOWLEDGE_CLASSES,
    KNOWLEDGE_STATUSES,
    SOURCE_TYPES,
    add_common_args,
    body_section,
    existing_ids,
    format_list,
    knowledge_files,
    parse_frontmatter,
    project_root,
    read_entries,
    slugify,
    today,
    update_knowledge_index,
    write_frontmatter,
)


def create(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    if args.knowledge_class not in KNOWLEDGE_CLASSES:
        raise SystemExit(f"FAIL invalid class: {args.knowledge_class}")
    if args.confidence not in CONFIDENCES:
        raise SystemExit(f"FAIL invalid confidence: {args.confidence}")
    if args.status not in KNOWLEDGE_STATUSES:
        raise SystemExit(f"FAIL invalid status: {args.status}")
    if args.source_type not in SOURCE_TYPES:
        raise SystemExit(f"FAIL invalid source type: {args.source_type}")
    if args.confidence == "VERIFIED" and not args.source_ref:
        raise SystemExit("FAIL VERIFIED knowledge requires source-ref")

    entries = read_entries(knowledge_files(root))
    ids = existing_ids(entries)
    kid = args.id or __import__("memorylib").next_id(ids, "KNOW")
    if kid in ids:
        raise SystemExit(f"FAIL duplicate knowledge id: {kid}")

    filename = f"{kid}-{slugify(args.title)}.md"
    path = root / ".ai" / "knowledge" / filename
    if path.exists():
        raise SystemExit(f"FAIL refusing to overwrite: {path}")

    now = today()
    meta = {
        "id": kid,
        "title": args.title,
        "class": args.knowledge_class,
        "project": args.project,
        "scope": args.scope,
        "confidence": args.confidence,
        "status": args.status,
        "created": now,
        "updated": now,
        "source_type": args.source_type,
        "source_ref": args.source_ref,
        "tags": format_list(args.tags),
        "related_requirements": format_list(args.related_requirements),
        "related_decisions": format_list(args.related_decisions),
    }
    body = f"""# Knowledge

{args.knowledge}

# Evidence

{args.evidence}

# Applicability

{args.applicability}

# Exceptions

{args.exceptions}

# Operational Impact

{args.operational_impact}

# Revalidation Trigger

{args.revalidation_trigger}
"""
    write_frontmatter(path, meta, body)
    update_knowledge_index(root)
    print(f"PASS created {kid} {path}")


def update(args: argparse.Namespace) -> None:
    root = project_root(args.project_root)
    matches = []
    for path in knowledge_files(root):
        meta, body = parse_frontmatter(path)
        if meta.get("id") == args.update_id:
            matches.append((path, meta, body))
    if not matches:
        raise SystemExit(f"FAIL knowledge id not found: {args.update_id}")
    if len(matches) > 1:
        raise SystemExit(f"FAIL duplicate knowledge id: {args.update_id}")
    path, meta, body = matches[0]
    if args.confidence:
        if args.confidence not in CONFIDENCES:
            raise SystemExit(f"FAIL invalid confidence: {args.confidence}")
        if meta.get("confidence") == "UNVERIFIED" and args.confidence == "VERIFIED" and not args.evidence:
            raise SystemExit("FAIL upgrading UNVERIFIED to VERIFIED requires evidence")
        meta["confidence"] = args.confidence
    if args.status:
        if args.status not in KNOWLEDGE_STATUSES:
            raise SystemExit(f"FAIL invalid status: {args.status}")
        meta["status"] = args.status
        if args.status == "DEPRECATED" and meta.get("confidence") != "DEPRECATED":
            meta["confidence"] = "DEPRECATED"
    meta["updated"] = today()
    if args.evidence:
        existing = body_section(body, "Evidence")
        body = body.replace(existing, existing + f"\n\nUpdate {today()}: {args.evidence}", 1)
    write_frontmatter(path, meta, body)
    update_knowledge_index(root)
    print(f"PASS updated {args.update_id} {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    parser.add_argument("--update-id")
    parser.add_argument("--id")
    parser.add_argument("--class", dest="knowledge_class")
    parser.add_argument("--title")
    parser.add_argument("--project", default="sample-transactions")
    parser.add_argument("--scope", default="PROJECT", choices=["PROJECT", "WORKSPACE", "REUSABLE"])
    parser.add_argument("--confidence")
    parser.add_argument("--status", default="ACTIVE")
    parser.add_argument("--source-type")
    parser.add_argument("--source-ref", default="")
    parser.add_argument("--tags", nargs="*", default=[])
    parser.add_argument("--related-requirements", nargs="*", default=[])
    parser.add_argument("--related-decisions", nargs="*", default=[])
    parser.add_argument("--knowledge", default="")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--applicability", default="")
    parser.add_argument("--exceptions", default="None known.")
    parser.add_argument("--operational-impact", default="")
    parser.add_argument("--revalidation-trigger", default="Requirement, dependency, schema, policy, or production behavior changes.")
    args = parser.parse_args()

    if args.update_id:
        update(args)
    else:
        required = ["knowledge_class", "title", "confidence", "source_type", "source_ref", "knowledge", "evidence"]
        missing = [name for name in required if not getattr(args, name)]
        if missing:
            raise SystemExit("FAIL missing required fields: " + ", ".join(missing))
        create(args)


if __name__ == "__main__":
    main()
