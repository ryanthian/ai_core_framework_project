#!/usr/bin/env python3
from __future__ import annotations

import argparse

from domainlib import load_manifest, parse_activation, project_root, today, write_activation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--deactivate", action="store_true")
    args = parser.parse_args()
    root = project_root(args.project)
    manifest = load_manifest(root, args.pack, args.version)
    if manifest["version"] != args.version:
        raise SystemExit(f"FAIL version mismatch: requested {args.version}, pack has {manifest['version']}")
    if manifest["status"] not in {"ACTIVE", "EXPERIMENTAL"}:
        raise SystemExit(f"FAIL pack status is not activatable: {manifest['status']}")
    rows = parse_activation(root)
    before = len(rows)
    rows = [row for row in rows if not (row["pack"] == args.pack and row["version"] == args.version)]
    if args.deactivate:
        write_activation(root, rows)
        print(f"DEACTIVATED {args.pack}@{args.version} removed={before - len(rows)}")
        return
    rows.append({"pack": args.pack, "version": args.version, "activated_at": today()})
    write_activation(root, rows)
    print(f"ACTIVATED {args.pack}@{args.version}")


if __name__ == "__main__":
    main()
