#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from documentlib import ensure_document_dirs, find_by_hash, load_json, manifest_path, next_document_id, now, project_root, safe_copy_source, sha256, update_index, write_json
from parsers import source_type_for


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--file", required=True)
    parser.add_argument("--title", default="")
    parser.add_argument("--authority", choices=["AUTHORITATIVE", "APPROVED", "WORKING_DRAFT", "REFERENCE", "UNVERIFIED"], default="UNVERIFIED")
    parser.add_argument("--classification", default="project_document")
    parser.add_argument("--confidentiality", default="internal")
    parser.add_argument("--new-version-of", default="")
    parser.add_argument("--force-new-version", action="store_true")
    args = parser.parse_args()

    root = project_root(args.project)
    ensure_document_dirs(root)
    source = Path(args.file).resolve()
    if not source.exists() or not source.is_file():
        raise SystemExit(f"FAIL source file not found: {source}")
    source_type = source_type_for(source)
    source_hash = sha256(source)
    duplicate = find_by_hash(root, source_hash)
    if duplicate and not args.force_new_version:
        print(f"DUPLICATE document_id={duplicate['document_id']} source_hash={source_hash}")
        raise SystemExit(2)

    document_id = next_document_id(root)
    managed_source = safe_copy_source(root, source, document_id)
    version = "v1"
    if args.new_version_of:
        version = f"supersedes:{args.new_version_of}"
    manifest = {
        "document_id": document_id,
        "title": args.title or source.stem,
        "project": root.name,
        "source_type": source_type,
        "source_path": str(managed_source.relative_to(root)),
        "original_source_path": str(source),
        "source_hash": source_hash,
        "ingested_at": now(),
        "parser": "",
        "parser_version": "",
        "page_count": 0,
        "section_count": 0,
        "language": "unknown",
        "status": "INGESTED",
        "classification": args.classification,
        "authority": args.authority,
        "confidentiality": args.confidentiality,
        "extraction_status": "NOT_STARTED",
        "review_status": "NOT_STARTED",
        "promotion_status": "NOT_STARTED",
        "version": version,
        "supersedes": args.new_version_of,
        "superseded_by": "",
    }
    write_json(manifest_path(root, document_id), manifest)
    if args.new_version_of:
        old_manifest_path = manifest_path(root, args.new_version_of)
        if old_manifest_path.exists():
            old_manifest = load_json(old_manifest_path)
            old_manifest["status"] = "SUPERSEDED"
            old_manifest["superseded_by"] = document_id
            write_json(old_manifest_path, old_manifest)
    write_json(root / ".ai" / "documents" / "runs" / f"{document_id}.json", {
        "document_id": document_id,
        "current_stage": "INGESTED",
        "parser_status": "NOT_STARTED",
        "analyst_status": "NOT_STARTED",
        "review_status": "NOT_STARTED",
        "promotion_status": "NOT_STARTED",
        "errors": [],
        "artifacts": {"manifest": str(manifest_path(root, document_id).relative_to(root))},
        "timestamps": {"ingested_at": manifest["ingested_at"]},
        "status": "RUNNING",
    })
    update_index(root)
    print(f"INGESTED {document_id} {source_type} {source_hash}")


if __name__ == "__main__":
    main()
