#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict

from documentlib import extracted_path, load_json, manifest_path, project_root, update_index, write_json
from parsers import parser_for


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", required=True)
    args = parser.parse_args()

    root = project_root(args.project)
    manifest_file = manifest_path(root, args.document_id)
    if not manifest_file.exists():
        raise SystemExit(f"FAIL manifest not found: {manifest_file}")
    manifest = load_json(manifest_file)
    source = root / manifest["source_path"]
    parser_instance = parser_for(source)
    result = parser_instance.parse(source)
    payload = {
        "document_id": args.document_id,
        "source_hash": manifest["source_hash"],
        "parser": result.parser,
        "parser_version": result.parser_version,
        "source_type": result.source_type,
        "parse_status": result.status,
        "language": result.language,
        "page_count": result.page_count,
        "section_count": result.section_count,
        "warnings": result.warnings,
        "sections": [asdict(section) for section in result.sections],
        "items": [],
    }
    write_json(extracted_path(root, args.document_id), payload)
    manifest.update({
        "parser": result.parser,
        "parser_version": result.parser_version,
        "page_count": result.page_count,
        "section_count": result.section_count,
        "language": result.language,
        "status": "EXTRACTED" if result.status == "PARSED" else result.status,
        "extraction_status": result.status,
    })
    write_json(manifest_file, manifest)
    run_path = root / ".ai" / "documents" / "runs" / f"{args.document_id}.json"
    if run_path.exists():
        run = load_json(run_path)
        run.update({"current_stage": "EXTRACTED", "parser_status": result.status, "status": "RUNNING"})
        run["artifacts"]["extracted"] = str(extracted_path(root, args.document_id).relative_to(root))
        write_json(run_path, run)
    update_index(root)
    print(f"EXTRACTED {args.document_id} status={result.status} sections={result.section_count}")


if __name__ == "__main__":
    main()
