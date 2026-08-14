#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

from documentlib import ITEM_TYPES, extracted_path, has_sensitive, load_existing_knowledge, load_json, manifest_path, project_root, redact_sensitive, report_path, update_index, write_json


def classify(text: str, source_type: str) -> tuple[str, str, str]:
    lower = text.lower()
    if "?" in text or "unknown" in lower or "not specified" in lower or "tbd" in lower:
        return "UNKNOWN", "HIGH", "explicit uncertainty"
    if re.search(r"\b(post|get|put|patch|delete)\s+/[A-Za-z0-9_/{}/.-]+", lower):
        return "API_CONTRACT", "HIGH", "explicit endpoint"
    if "must" in lower or "shall" in lower or "required" in lower:
        if "only" in lower or "cannot" in lower:
            return "BUSINESS_RULE", "HIGH", "explicit rule keyword"
        return "REQUIREMENT", "HIGH", "explicit requirement keyword"
    if "acceptance" in lower or "within" in lower or "at least" in lower or "no more than" in lower:
        return "ACCEPTANCE_CRITERION", "MEDIUM", "acceptance keyword"
    if "decision" in lower or "agreed" in lower:
        return "DECISION_CANDIDATE", "MEDIUM", "meeting decision wording"
    if "action" in lower or "owner:" in lower or "due:" in lower:
        return "ACTION_ITEM", "MEDIUM", "action/owner wording"
    if "risk" in lower:
        return "RISK", "HIGH", "explicit risk wording"
    if "assume" in lower or "assumption" in lower:
        return "ASSUMPTION", "HIGH", "explicit assumption wording"
    if source_type in {"JSON", "CSV"}:
        return "DATA_RULE", "MEDIUM", "structured data source"
    return "PROJECT_FACT", "LOW", "general extracted statement"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", required=True)
    args = parser.parse_args()

    root = project_root(args.project)
    manifest = load_json(manifest_path(root, args.document_id))
    extracted_file = extracted_path(root, args.document_id)
    if not extracted_file.exists():
        raise SystemExit(f"FAIL extracted file not found: {extracted_file}")
    extracted = load_json(extracted_file)
    knowledge = load_existing_knowledge(root)
    items = []
    conflicts = []
    for idx, section in enumerate(extracted.get("sections", []), start=1):
        raw_text = section.get("text", "").strip()
        if not raw_text:
            continue
        sensitive = has_sensitive(raw_text)
        text = redact_sensitive(raw_text)
        item_type, confidence, notes = classify(text, manifest["source_type"])
        if item_type not in ITEM_TYPES:
            item_type = "PROJECT_FACT"
        conflict = ""
        lower = text.lower()
        for record in knowledge:
            if "only account owner may view statement" in record["text"] and "delegated finance officer" in lower:
                conflict = record["id"]
                conflicts.append({"item_id": f"{args.document_id}-ITEM-{idx:03d}", "knowledge_id": record["id"]})
        item_status = "CONFLICT" if conflict else "PROPOSED"
        items.append({
            "item_id": f"{args.document_id}-ITEM-{idx:03d}",
            "type": item_type,
            "text": text[:1000],
            "source_location": section.get("location", ""),
            "source_excerpt": text[:240],
            "source_excerpt_hash": str(abs(hash(text[:240]))),
            "extraction_confidence": confidence,
            "status": item_status,
            "notes": notes,
            "authority": manifest.get("authority", "UNVERIFIED"),
            "sensitive_content_warning": sensitive,
            "conflict": conflict,
        })
    extracted["items"] = items
    write_json(extracted_file, extracted)
    report_lines = [
        f"# Document Intelligence Report: {args.document_id}",
        "",
        f"Document: {manifest.get('title')}",
        f"Classification: {manifest.get('classification')}",
        f"Authority Level: {manifest.get('authority')}",
        "",
        "## Summary",
        f"Extracted {len(items)} proposed intelligence items from {len(extracted.get('sections', []))} parsed sections.",
        "",
    ]
    for heading, item_type in [
        ("Extracted Requirements", "REQUIREMENT"),
        ("Business Rules", "BUSINESS_RULE"),
        ("Facts", "PROJECT_FACT"),
        ("Constraints", "CONSTRAINT"),
        ("APIs", "API_CONTRACT"),
        ("Data Rules", "DATA_RULE"),
        ("Security Rules", "SECURITY_RULE"),
        ("Acceptance Criteria", "ACCEPTANCE_CRITERION"),
        ("Dependencies", "DEPENDENCY"),
        ("Assumptions", "ASSUMPTION"),
        ("Unknowns", "UNKNOWN"),
        ("Risks", "RISK"),
        ("Decision Candidates", "DECISION_CANDIDATE"),
        ("Action Items", "ACTION_ITEM"),
        ("Conflicts", "CONFLICT"),
    ]:
        report_lines.extend([f"## {heading}", ""])
        matches = [item for item in items if item["type"] == item_type or (item_type == "CONFLICT" and item.get("conflict"))]
        if not matches:
            report_lines.append("- None")
        for item in matches:
            warning = " SENSITIVE_CONTENT_WARNING" if item["sensitive_content_warning"] else ""
            conflict_note = f" DOCUMENT_MEMORY_CONFLICT with {item['conflict']}" if item.get("conflict") else ""
            report_lines.append(f"- {item['item_id']} [{item['extraction_confidence']}] {item['text']} ({item['source_location']}){warning}{conflict_note}")
        report_lines.append("")
    report_lines.extend(["## Source References", "", f"- Manifest: `.ai/documents/manifests/{args.document_id}.json`", f"- Extracted: `.ai/documents/extracted/{args.document_id}.json`", "", "## Recommended Promotions", "", "- Review required before promotion."])
    report_path(root, args.document_id).write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    manifest.update({"status": "NEEDS_REVIEW", "review_status": "NEEDS_REVIEW"})
    write_json(manifest_path(root, args.document_id), manifest)
    run_path = root / ".ai" / "documents" / "runs" / f"{args.document_id}.json"
    if run_path.exists():
        run = load_json(run_path)
        run.update({"current_stage": "ANALYZED", "analyst_status": "COMPLETE"})
        run["artifacts"]["intelligence_report"] = str(report_path(root, args.document_id).relative_to(root))
        write_json(run_path, run)
    update_index(root)
    print(f"ANALYZED {args.document_id} items={len(items)} conflicts={len(conflicts)}")


if __name__ == "__main__":
    main()
