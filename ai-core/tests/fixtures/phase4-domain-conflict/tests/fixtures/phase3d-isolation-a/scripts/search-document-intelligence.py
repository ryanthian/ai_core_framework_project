#!/usr/bin/env python3
from __future__ import annotations

import argparse

from documentlib import documents_dir, load_json, project_root


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--query", required=True)
    parser.add_argument("--type", default="")
    args = parser.parse_args()
    root = project_root(args.project)
    terms = [term.lower() for term in args.query.split() if term.strip()]
    hits = []
    for path in sorted((documents_dir(root) / "extracted").glob("DOC-*.json")):
        data = load_json(path)
        for item in data.get("items", []):
            if args.type and item.get("type") != args.type:
                continue
            haystack = " ".join([item.get("item_id", ""), item.get("type", ""), item.get("text", ""), item.get("source_location", "")]).lower()
            if all(term in haystack for term in terms):
                hits.append(item)
    for item in hits:
        print(f"{item['item_id']} {item['type']} {item['source_location']} {item['text'][:160]}")
    print(f"RESULTS {len(hits)}")


if __name__ == "__main__":
    main()
