#!/usr/bin/env python3
from __future__ import annotations

import argparse

from documentlib import extracted_path, load_json, manifest_path, project_root, review_path, update_index, write_json


def default_decision(item: dict) -> str:
    if item.get("sensitive_content_warning"):
        return "REJECT"
    if item.get("status") == "CONFLICT":
        return "CONFLICT"
    if item.get("extraction_confidence") == "LOW":
        return "NEEDS_CLARIFICATION"
    return "APPROVE"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--approve-all-safe", action="store_true")
    args = parser.parse_args()

    root = project_root(args.project)
    manifest = load_json(manifest_path(root, args.document_id))
    extracted = load_json(extracted_path(root, args.document_id))
    decisions = []
    for item in extracted.get("items", []):
        decision = default_decision(item) if args.approve_all_safe else "NEEDS_CLARIFICATION"
        item["review_decision"] = decision
        if decision == "APPROVE":
            item["status"] = "APPROVED"
        elif decision == "REJECT":
            item["status"] = "REJECTED"
        elif decision == "CONFLICT":
            item["status"] = "CONFLICT"
        else:
            item["status"] = "NEEDS_CLARIFICATION"
        decisions.append({
            "item_id": item["item_id"],
            "decision": decision,
            "reason": "safe automatic review scaffold; human/Codex review still authoritative",
            "source_location": item.get("source_location", ""),
        })
    write_json(extracted_path(root, args.document_id), extracted)
    review = {
        "document_id": args.document_id,
        "reviewer": "DOCUMENT_REVIEWER",
        "decisions": decisions,
        "verdict": "PARTIALLY_APPROVED" if any(d["decision"] != "APPROVE" for d in decisions) else "APPROVED",
        "notes": "Review decisions are item-level and preserve conflicts/unknowns.",
    }
    write_json(review_path(root, args.document_id), review)
    manifest.update({"status": review["verdict"], "review_status": review["verdict"]})
    write_json(manifest_path(root, args.document_id), manifest)
    run_path = root / ".ai" / "documents" / "runs" / f"{args.document_id}.json"
    if run_path.exists():
        run = load_json(run_path)
        run.update({"current_stage": "REVIEWED", "review_status": review["verdict"]})
        run["artifacts"]["review"] = str(review_path(root, args.document_id).relative_to(root))
        write_json(run_path, run)
    update_index(root)
    print(f"REVIEWED {args.document_id} verdict={review['verdict']} decisions={len(decisions)}")


if __name__ == "__main__":
    main()
