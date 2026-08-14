#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from documentlib import AUTHORITIES, DOCUMENT_STATUSES, EXTRACTION_CONFIDENCES, ITEM_STATUSES, ITEM_TYPES, SOURCE_TYPES, documents_dir, extracted_path, load_json, manifest_path, project_root, review_path, sha256


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", default="")
    parser.add_argument("--require-warning", default="")
    parser.add_argument("--require-item-type", action="append", default=[])
    parser.add_argument("--require-conflict", action="store_true")
    parser.add_argument("--require-reviewed", action="store_true")
    parser.add_argument("--require-promoted", action="store_true")
    parser.add_argument("--require-index", action="store_true")
    args = parser.parse_args()

    root = project_root(args.project)
    manifest_files = [manifest_path(root, args.document_id)] if args.document_id else sorted((documents_dir(root) / "manifests").glob("DOC-*.json"))
    passes = warns = fails = 0
    seen = set()
    for path in manifest_files:
        if not path.exists():
            print(f"FAIL manifest missing {path}")
            fails += 1
            continue
        manifest = load_json(path)
        document_id = manifest.get("document_id", "")
        if document_id in seen:
            print(f"FAIL duplicate document_id {document_id}")
            fails += 1
        seen.add(document_id)
        required = ["document_id", "title", "project", "source_type", "source_path", "source_hash", "ingested_at", "status", "authority", "extraction_status", "review_status", "promotion_status"]
        missing = [field for field in required if not manifest.get(field)]
        if missing:
            print(f"FAIL {document_id} missing manifest fields: {', '.join(missing)}")
            fails += 1
        elif manifest.get("source_type") not in SOURCE_TYPES:
            print(f"FAIL {document_id} invalid source_type {manifest.get('source_type')}")
            fails += 1
        elif manifest.get("status") not in DOCUMENT_STATUSES and manifest.get("status") not in {"OCR_REQUIRED", "UNSUPPORTED_PARSER_MISSING"}:
            print(f"FAIL {document_id} invalid status {manifest.get('status')}")
            fails += 1
        elif manifest.get("authority") not in AUTHORITIES:
            print(f"FAIL {document_id} invalid authority {manifest.get('authority')}")
            fails += 1
        else:
            print(f"PASS manifest {document_id}")
            passes += 1
        source = root / manifest.get("source_path", "")
        if not source.exists():
            print(f"FAIL {document_id} source link broken {source}")
            fails += 1
        elif sha256(source) != manifest.get("source_hash"):
            print(f"FAIL {document_id} source hash mismatch")
            fails += 1
        else:
            print(f"PASS source hash {document_id}")
            passes += 1
        extracted_file = extracted_path(root, document_id)
        item_types = set()
        conflict_found = False
        warning_found = False
        if extracted_file.exists():
            extracted = load_json(extracted_file)
            for item in extracted.get("items", []):
                item_required = ["item_id", "type", "text", "source_location", "extraction_confidence", "status"]
                missing_item = [field for field in item_required if not item.get(field)]
                if missing_item:
                    print(f"FAIL {item.get('item_id', document_id)} missing item fields: {', '.join(missing_item)}")
                    fails += 1
                    continue
                if item["type"] not in ITEM_TYPES:
                    print(f"FAIL {item['item_id']} invalid type {item['type']}")
                    fails += 1
                elif item["extraction_confidence"] not in EXTRACTION_CONFIDENCES:
                    print(f"FAIL {item['item_id']} invalid confidence {item['extraction_confidence']}")
                    fails += 1
                elif item["status"] not in ITEM_STATUSES:
                    print(f"FAIL {item['item_id']} invalid status {item['status']}")
                    fails += 1
                else:
                    item_types.add(item["type"])
                    if item.get("conflict") or item.get("status") == "CONFLICT":
                        conflict_found = True
                    if item.get("sensitive_content_warning"):
                        warning_found = True
            print(f"PASS extracted {document_id} items={len(extracted.get('items', []))}")
            passes += 1
        else:
            print(f"WARN extracted file missing {document_id}")
            warns += 1
        for expected_type in args.require_item_type:
            if expected_type in item_types:
                print(f"PASS item type {expected_type}")
                passes += 1
            else:
                print(f"FAIL missing item type {expected_type}")
                fails += 1
        if args.require_conflict:
            if conflict_found:
                print("PASS conflict marker")
                passes += 1
            else:
                print("FAIL missing conflict marker")
                fails += 1
        if args.require_warning:
            if args.require_warning == "SENSITIVE_CONTENT_WARNING" and warning_found:
                print("PASS SENSITIVE_CONTENT_WARNING")
                passes += 1
            else:
                print(f"FAIL missing warning {args.require_warning}")
                fails += 1
        if args.require_reviewed:
            if review_path(root, document_id).exists():
                print(f"PASS review {document_id}")
                passes += 1
            else:
                print(f"FAIL review missing {document_id}")
                fails += 1
        if args.require_promoted:
            promotion = documents_dir(root) / "processed" / f"{document_id}-promotion.json"
            if promotion.exists():
                print(f"PASS promotion {document_id}")
                passes += 1
            else:
                print(f"FAIL promotion missing {document_id}")
                fails += 1
    if args.require_index:
        index = documents_dir(root) / "index.md"
        if index.exists() and "Document ID" in index.read_text(encoding="utf-8"):
            print("PASS document index")
            passes += 1
        else:
            print("FAIL document index missing")
            fails += 1
    print(f"SUMMARY pass={passes} warn={warns} fail={fails}")
    raise SystemExit(1 if fails else 0)


if __name__ == "__main__":
    main()
