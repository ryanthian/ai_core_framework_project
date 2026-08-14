#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil

from domainlib import domain_root, load_manifest, parse_activation, project_root, today, write_activation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--from-version", required=True)
    parser.add_argument("--to-version", required=True)
    parser.add_argument("--rollback", action="store_true")
    args = parser.parse_args()
    root = project_root(args.project)
    rows = parse_activation(root)
    current = [row for row in rows if row["pack"] == args.pack]
    if not current:
        raise SystemExit(f"FAIL pack is not active: {args.pack}")
    expected = args.to_version if args.rollback else args.from_version
    target = args.from_version if args.rollback else args.to_version
    if current[0]["version"] != expected:
        raise SystemExit(f"FAIL active version is {current[0]['version']}, expected {expected}")
    manifest = load_manifest(root, args.pack, target)
    if manifest["version"] != target:
        raise SystemExit(f"FAIL installed pack version is {manifest['version']}, expected target {target}")
    for row in rows:
        if row["pack"] == args.pack:
            row["version"] = target
            row["activated_at"] = today()
    write_activation(root, rows)
    action = "ROLLED_BACK" if args.rollback else "UPGRADED"
    print(f"{action} {args.pack} {expected}->{target}")


if __name__ == "__main__":
    main()
