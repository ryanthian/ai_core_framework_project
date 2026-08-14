#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from domainlib import CONFIDENCES, ITEM_TYPES, PACK_STATUSES, active_packs, domain_root, load_json, project_root


REQUIRED_MANIFEST = ["id", "name", "version", "status", "description", "scope", "maintainer", "created", "updated", "source_authority", "license", "dependencies", "compatible_schema_version", "tags", "activation_conditions", "known_limitations", "conflict_policy"]
REQUIRED_RULE = ["id", "title", "type", "class", "domain", "scope", "confidence", "status", "source_type", "source_ref", "version", "tags", "statement", "revalidation_trigger"]


def validate_pack(root: Path, pack_id: str) -> tuple[int, int, int]:
    passes = warns = fails = 0
    folder = domain_root(root) / pack_id
    manifest_path = folder / "manifest.json"
    rules_path = folder / "rules.json"
    if not manifest_path.exists() or not rules_path.exists():
        print(f"FAIL missing manifest/rules for {pack_id}")
        return 0, 0, 1
    manifest = load_json(manifest_path)
    missing = [field for field in REQUIRED_MANIFEST if field not in manifest]
    if missing:
        print(f"FAIL {pack_id} missing manifest fields {missing}")
        fails += 1
    elif manifest["status"] not in PACK_STATUSES:
        print(f"FAIL {pack_id} invalid status {manifest['status']}")
        fails += 1
    else:
        print(f"PASS manifest {pack_id}@{manifest['version']}")
        passes += 1
    ids = set()
    for item in load_json(rules_path).get("items", []):
        missing = [field for field in REQUIRED_RULE if field not in item]
        if missing:
            print(f"FAIL {pack_id} item missing fields {missing}")
            fails += 1
            continue
        if item["id"] in ids:
            print(f"FAIL duplicate item id {item['id']}")
            fails += 1
        ids.add(item["id"])
        if item["type"] not in ITEM_TYPES:
            print(f"FAIL {item['id']} invalid type {item['type']}")
            fails += 1
        elif item["confidence"] not in CONFIDENCES:
            print(f"FAIL {item['id']} invalid confidence {item['confidence']}")
            fails += 1
        elif item["confidence"] == "VERIFIED" and not item.get("source_ref"):
            print(f"FAIL {item['id']} VERIFIED lacks source_ref")
            fails += 1
        else:
            print(f"PASS rule {item['id']}")
            passes += 1
    for dep in manifest.get("dependencies", []):
        if not (domain_root(root) / dep / "manifest.json").exists():
            print(f"FAIL {pack_id} missing dependency {dep}")
            fails += 1
    if not (folder / "CHANGELOG.md").exists():
        print(f"WARN {pack_id} missing CHANGELOG.md")
        warns += 1
    return passes, warns, fails


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--pack", default="")
    parser.add_argument("--check-activation", action="store_true")
    args = parser.parse_args()
    root = project_root(args.project)
    packs = [args.pack] if args.pack else sorted(path.name for path in domain_root(root).iterdir() if path.is_dir())
    passes = warns = fails = 0
    for pack in packs:
        p, w, f = validate_pack(root, pack)
        passes += p; warns += w; fails += f
    if args.check_activation:
        for active in active_packs(root):
            if active["version_mismatch"]:
                print(f"FAIL activation version mismatch {active['activation']['pack']}")
                fails += 1
            else:
                print(f"PASS activation {active['activation']['pack']}@{active['activation']['version']}")
                passes += 1
    index = domain_root(root) / "index.md"
    if index.exists():
        print("PASS domain registry")
        passes += 1
    else:
        print("FAIL missing domain registry")
        fails += 1
    print(f"SUMMARY pass={passes} warn={warns} fail={fails}")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
