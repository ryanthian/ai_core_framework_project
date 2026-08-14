#!/usr/bin/env python3
from __future__ import annotations

import argparse

from documentlib import doc_run_path, load_json, project_root, write_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--cancel", action="store_true")
    parser.add_argument("--reprocess", action="store_true")
    parser.add_argument("--reason", default="")
    args = parser.parse_args()
    root = project_root(args.project)
    path = doc_run_path(root, args.document_id)
    if not path.exists():
        raise SystemExit(f"FAIL document run not found: {path}")
    run = load_json(path)
    if args.cancel:
        run["status"] = "CANCELLED"
        run["cancel_reason"] = args.reason or "cancelled by operator"
    elif args.reprocess:
        run["current_stage"] = "INGESTED"
        run["parser_status"] = "REPROCESS_REQUESTED"
        run["status"] = "RUNNING"
    elif args.resume:
        pass
    write_json(path, run)
    print(f"DOCUMENT_RUN {args.document_id} status={run.get('status')} stage={run.get('current_stage')} parser={run.get('parser_status')} review={run.get('review_status')} promotion={run.get('promotion_status')}")


if __name__ == "__main__":
    main()
