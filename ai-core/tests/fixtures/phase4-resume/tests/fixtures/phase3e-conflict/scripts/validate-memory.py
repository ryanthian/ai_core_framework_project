#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from memorylib import (
    CONFIDENCES,
    DECISION_STATUSES,
    KNOWLEDGE_CLASSES,
    KNOWLEDGE_STATUSES,
    SOURCE_TYPES,
    add_common_args,
    body_section,
    decision_files,
    knowledge_files,
    normalize_rule_key,
    parse_frontmatter,
    project_root,
    read_entries,
    update_decision_index,
    update_knowledge_index,
)


K_REQUIRED = [
    "id",
    "title",
    "class",
    "project",
    "scope",
    "confidence",
    "status",
    "created",
    "updated",
    "source_type",
    "source_ref",
]
D_REQUIRED = ["id", "title", "date", "status", "scope"]


def check_ref(root: Path, ref: str) -> bool:
    if not ref:
        return False
    path_ref = ref.split("#", 1)[0]
    return (root / path_ref).exists()


def validate(root: Path) -> tuple[int, int, int]:
    passes = warns = fails = 0
    k_entries = read_entries(knowledge_files(root))
    d_entries = read_entries(decision_files(root))

    seen: dict[str, Path] = {}
    for path, meta, body in k_entries:
        local_fail = False
        for key in K_REQUIRED:
            if not meta.get(key):
                print(f"FAIL {path}: missing {key}")
                fails += 1
                local_fail = True
        kid = meta.get("id", "")
        if kid in seen:
            print(f"FAIL duplicate knowledge id {kid}: {seen[kid]} and {path}")
            fails += 1
            local_fail = True
        seen[kid] = path
        if meta.get("class") and meta["class"] not in KNOWLEDGE_CLASSES:
            print(f"FAIL {path}: invalid class {meta['class']}")
            fails += 1
            local_fail = True
        if meta.get("confidence") and meta["confidence"] not in CONFIDENCES:
            print(f"FAIL {path}: invalid confidence {meta['confidence']}")
            fails += 1
            local_fail = True
        if meta.get("status") and meta["status"] not in KNOWLEDGE_STATUSES:
            print(f"FAIL {path}: invalid status {meta['status']}")
            fails += 1
            local_fail = True
        if meta.get("source_type") and meta["source_type"] not in SOURCE_TYPES:
            print(f"FAIL {path}: invalid source_type {meta['source_type']}")
            fails += 1
            local_fail = True
        if meta.get("confidence") == "VERIFIED" and not check_ref(root, meta.get("source_ref", "")):
            print(f"FAIL {path}: VERIFIED source_ref does not resolve: {meta.get('source_ref', '')}")
            fails += 1
            local_fail = True
        if not body_section(body, "Revalidation Trigger"):
            print(f"WARN {path}: missing Revalidation Trigger body")
            warns += 1
        if not local_fail:
            print(f"PASS knowledge {kid} {path.name}")
            passes += 1

    seen_decisions: dict[str, Path] = {}
    decision_ids = {meta.get("id", "") for _path, meta, _body in d_entries}
    for path, meta, _body in d_entries:
        local_fail = False
        for key in D_REQUIRED:
            if not meta.get(key):
                print(f"FAIL {path}: missing {key}")
                fails += 1
                local_fail = True
        did = meta.get("id", "")
        if did in seen_decisions:
            print(f"FAIL duplicate decision id {did}: {seen_decisions[did]} and {path}")
            fails += 1
            local_fail = True
        seen_decisions[did] = path
        if meta.get("status") and meta["status"] not in DECISION_STATUSES:
            print(f"FAIL {path}: invalid status {meta['status']}")
            fails += 1
            local_fail = True
        supersedes = meta.get("supersedes", "")
        if supersedes and supersedes not in decision_ids:
            print(f"FAIL {path}: supersedes missing decision {supersedes}")
            fails += 1
            local_fail = True
        if not local_fail:
            print(f"PASS decision {did} {path.name}")
            passes += 1

    update_knowledge_index(root)
    update_decision_index(root)

    conflicts = []
    by_key: dict[str, list[tuple[Path, dict[str, str], str]]] = defaultdict(list)
    for entry in k_entries:
        _path, meta, body = entry
        if meta.get("status") == "ACTIVE":
            key = normalize_rule_key(meta, body)
            if key:
                by_key[key].append(entry)
    for key, entries in by_key.items():
        if len(entries) < 2:
            continue
        knowledge_texts = {body_section(body, "Knowledge").lower() for _path, _meta, body in entries}
        if len(knowledge_texts) > 1:
            conflicts.append(entries)

    for entries in conflicts:
        print("WARN MEMORY CONFLICT")
        for path, meta, _body in entries:
            print(
                f"WARN Entry {meta.get('id')} {meta.get('title')} "
                f"source={meta.get('source_type')}:{meta.get('source_ref')} confidence={meta.get('confidence')} path={path}"
            )
        warns += 1

    k_index = root / ".ai" / "knowledge" / "index.md"
    d_index = root / ".ai" / "decisions" / "index.md"
    if k_index.exists():
        print(f"PASS knowledge index {k_index}")
        passes += 1
    else:
        print(f"FAIL missing knowledge index {k_index}")
        fails += 1
    if d_index.exists():
        print(f"PASS decision index {d_index}")
        passes += 1
    else:
        print(f"FAIL missing decision index {d_index}")
        fails += 1

    print(f"SUMMARY pass={passes} warn={warns} fail={fails}")
    return passes, warns, fails


def main() -> None:
    parser = argparse.ArgumentParser()
    add_common_args(parser)
    args = parser.parse_args()
    _passes, _warns, fails = validate(project_root(args.project_root))
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
