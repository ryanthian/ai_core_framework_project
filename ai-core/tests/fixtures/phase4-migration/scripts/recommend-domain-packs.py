#!/usr/bin/env python3
from __future__ import annotations

import argparse

from domainlib import domain_root, load_json, project_root, score_terms


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    root = project_root(args.project)
    matches = []
    for path in domain_root(root).iterdir():
        if not path.is_dir():
            continue
        manifest = load_json(path / "manifest.json")
        haystack = " ".join([manifest["name"], manifest["description"], " ".join(manifest["tags"]), " ".join(manifest["activation_conditions"])])
        score = score_terms(args.query, haystack)
        if score:
            confidence = "HIGH" if score >= 3 else "MEDIUM"
            matches.append((score, manifest, confidence))
    for _score, manifest, confidence in sorted(matches, key=lambda item: (-item[0], item[1]["id"])):
        print(f"RECOMMENDED {manifest['id']}@{manifest['version']} CONFIDENCE={confidence} WHY={manifest['description']}")
    print(f"RESULTS {len(matches)}")


if __name__ == "__main__":
    main()
