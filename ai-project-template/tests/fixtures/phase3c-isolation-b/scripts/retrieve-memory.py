#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict

from memorylib import (
    add_common_args,
    body_section,
    decision_files,
    knowledge_files,
    normalize_rule_key,
    parse_frontmatter,
    parse_list,
    project_root,
    read_entries,
)


def score_text(terms: list[str], text: str) -> int:
    lower = text.lower()
    return sum(1 for term in terms if term and term.lower() in lower)


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    parser.add_argument("--project", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--class", dest="knowledge_class", action="append", default=[])
    parser.add_argument("--tags", nargs="*", default=[])
    parser.add_argument("--related-requirement", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    root = project_root(args.project_root)
    terms = [part for part in args.query.replace(",", " ").split() if len(part) > 2]
    tag_filter = set(args.tags)

    relevant_knowledge = []
    unverified = []
    for path, meta, body in read_entries(knowledge_files(root)):
        if meta.get("status") != "ACTIVE":
            continue
        scope = meta.get("scope", "PROJECT")
        if scope == "PROJECT" and meta.get("project") != args.project:
            continue
        if args.knowledge_class and meta.get("class") not in args.knowledge_class:
            continue
        tags = set(parse_list(meta.get("tags")))
        if tag_filter and not (tag_filter & tags):
            continue
        if args.related_requirement and args.related_requirement not in parse_list(meta.get("related_requirements")):
            continue
        haystack = " ".join([meta.get("title", ""), meta.get("tags", ""), body])
        score = score_text(terms, haystack)
        if tag_filter:
            score += 2
        if score or args.knowledge_class or args.related_requirement:
            row = (score, path, meta, body)
            if meta.get("confidence") == "UNVERIFIED":
                unverified.append(row)
            else:
                relevant_knowledge.append(row)

    accepted_decisions = []
    for path, meta, body in read_entries(decision_files(root)):
        if meta.get("status") != "ACCEPTED":
            continue
        if meta.get("scope") == "PROJECT" and args.project not in body and args.project not in meta.get("title", ""):
            if args.related_requirement and meta.get("related_requirement") != args.related_requirement:
                continue
        haystack = " ".join([meta.get("title", ""), meta.get("related_requirement", ""), meta.get("related_knowledge", ""), body])
        score = score_text(terms, haystack)
        if score or args.related_requirement == meta.get("related_requirement"):
            accepted_decisions.append((score, path, meta, body))

    conflicts = []
    by_key = defaultdict(list)
    for path, meta, body in read_entries(knowledge_files(root)):
        if meta.get("status") == "ACTIVE":
            scope = meta.get("scope", "PROJECT")
            if scope == "PROJECT" and meta.get("project") != args.project:
                continue
            by_key[normalize_rule_key(meta, body)].append((path, meta, body))
    active_entries = [entry for entries in by_key.values() for entry in entries]
    for idx, left in enumerate(active_entries):
        for right in active_entries[idx + 1 :]:
            _lpath, lmeta, _lbody = left
            _rpath, rmeta, _rbody = right
            if lmeta.get("class") != rmeta.get("class"):
                continue
            shared_tags = set(parse_list(lmeta.get("tags"))) & set(parse_list(rmeta.get("tags")))
            if len(shared_tags) >= 3:
                by_key["tags:" + ",".join(sorted(shared_tags))].extend([left, right])
    for entries in by_key.values():
        unique_entries = []
        seen_paths = set()
        for entry in entries:
            if entry[0] not in seen_paths:
                unique_entries.append(entry)
                seen_paths.add(entry[0])
        entries = unique_entries
        if len(entries) > 1:
            statements = {body_section(body, "Knowledge").lower() for _path, _meta, body in entries}
            if len(statements) > 1:
                conflicts.append(entries)

    lines = ["# Memory Brief", "", "## Relevant Knowledge", ""]
    for _score, path, meta, body in sorted(relevant_knowledge, key=lambda item: (-item[0], item[2].get("id", "")))[:10]:
        lines.extend(
            [
                f"- {meta.get('id')} - {meta.get('title')} ({meta.get('class')}, {meta.get('confidence')}, {meta.get('scope')})",
                f"  Source: {meta.get('source_type')} {meta.get('source_ref')}",
                f"  Impact: {body_section(body, 'Operational Impact') or body_section(body, 'Knowledge')}",
            ]
        )
    if not relevant_knowledge:
        lines.append("- None found.")

    lines.extend(["", "## Relevant Decisions", ""])
    for _score, path, meta, body in sorted(accepted_decisions, key=lambda item: (-item[0], item[2].get("id", "")))[:10]:
        lines.extend(
            [
                f"- {meta.get('id')} - {meta.get('title')} ({meta.get('status')})",
                f"  Related requirement: {meta.get('related_requirement')}",
                f"  Why: {body_section(body, 'Why')}",
            ]
        )
    if not accepted_decisions:
        lines.append("- None found.")

    lines.extend(["", "## Unverified Items", ""])
    for _score, path, meta, body in sorted(unverified, key=lambda item: (-item[0], item[2].get("id", "")))[:10]:
        lines.append(f"- {meta.get('id')} - {meta.get('title')} ({meta.get('confidence')})")
    if not unverified:
        lines.append("- None found.")

    lines.extend(["", "## Memory Conflicts", ""])
    for entries in conflicts:
        lines.append("MEMORY CONFLICT")
        for path, meta, _body in entries:
            lines.append(
                f"- {meta.get('id')} {meta.get('title')} source={meta.get('source_type')}:{meta.get('source_ref')} confidence={meta.get('confidence')}"
            )
        lines.append("Recommended resolution: compare source strength and date; deprecate or supersede the weaker record without deleting history.")
    if not conflicts:
        lines.append("- None found.")

    lines.extend(["", "## Impact On Current Requirement", ""])
    if relevant_knowledge or accepted_decisions:
        lines.append("Use retrieved VERIFIED/SUPPORTED records before planning. Treat UNVERIFIED items as questions, not facts.")
    else:
        lines.append("No reusable project memory matched; inspect repository evidence before planning.")

    output = "\n".join(lines) + "\n"
    if args.output:
        out_path = root / args.output
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output, encoding="utf-8")
        print(f"PASS wrote memory brief {out_path}")
    print(output, end="")


if __name__ == "__main__":
    main()
