#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

from documentlib import extracted_path, load_existing_knowledge, load_json, manifest_path, now, project_root, update_index, write_json


KNOWLEDGE_TYPES = {"BUSINESS_RULE", "PROJECT_FACT", "CONSTRAINT", "API_CONTRACT", "DATA_RULE", "SECURITY_RULE"}


def slug(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return value[:60] or "document-item"


def next_req_id(root) -> str:
    nums = []
    for path in (root / ".ai" / "requirements").glob("REQ-DOC-*.md"):
        match = re.search(r"REQ-DOC-(\d+)", path.name)
        if match:
            nums.append(int(match.group(1)))
    return f"REQ-DOC-{(max(nums) + 1) if nums else 1:03d}"


def next_know_id(root) -> str:
    nums = []
    for path in (root / ".ai" / "knowledge").glob("KNOW-DOC-*.md"):
        match = re.search(r"KNOW-DOC-(\d+)", path.name)
        if match:
            nums.append(int(match.group(1)))
    return f"KNOW-DOC-{(max(nums) + 1) if nums else 1:03d}"


def existing_requirement_texts(root) -> list[str]:
    texts = []
    for path in (root / ".ai" / "requirements").glob("*.md"):
        body = path.read_text(encoding="utf-8", errors="ignore").lower()
        texts.append(body)
    return texts


def knowledge_confidence(authority: str, item: dict) -> str:
    if item.get("type") == "ASSUMPTION":
        return "UNVERIFIED"
    if authority == "AUTHORITATIVE" and item.get("extraction_confidence") == "HIGH":
        return "VERIFIED"
    if authority in {"AUTHORITATIVE", "APPROVED", "WORKING_DRAFT"}:
        return "SUPPORTED"
    return "UNVERIFIED"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", default=".")
    parser.add_argument("--document-id", required=True)
    parser.add_argument("--target", choices=["all", "requirements", "knowledge", "context"], default="all")
    args = parser.parse_args()

    root = project_root(args.project)
    manifest = load_json(manifest_path(root, args.document_id))
    extracted = load_json(extracted_path(root, args.document_id))
    existing = load_existing_knowledge(root)
    existing_requirements = existing_requirement_texts(root)
    promoted = []
    blocked = []
    for item in extracted.get("items", []):
        if item.get("review_decision") != "APPROVE":
            blocked.append({"item_id": item["item_id"], "reason": f"not approved: {item.get('review_decision', item.get('status'))}"})
            continue
        if item.get("sensitive_content_warning"):
            blocked.append({"item_id": item["item_id"], "reason": "SENSITIVE_CONTENT_WARNING"})
            continue
        if item.get("conflict"):
            blocked.append({"item_id": item["item_id"], "reason": f"DOCUMENT_MEMORY_CONFLICT {item['conflict']}"})
            continue
        if any(item["text"].lower()[:80] in record["text"] for record in existing):
            blocked.append({"item_id": item["item_id"], "reason": "POSSIBLE_DUPLICATE"})
            continue
        if item["type"] == "REQUIREMENT" and args.target in {"all", "requirements"}:
            if any(item["text"].lower()[:80] in body for body in existing_requirements):
                blocked.append({"item_id": item["item_id"], "reason": "POSSIBLE_DUPLICATE_REQUIREMENT"})
                continue
            rid = next_req_id(root)
            path = root / ".ai" / "requirements" / f"{rid}-{slug(item['text'])}.md"
            path.write_text(
                f"---\nid: {rid}\ntitle: {item['text'][:80]}\nproject: {root.name}\nstatus: CANDIDATE\ncreated: {now()[:10]}\nsource_type: DOCUMENT\nsource_ref: .ai/documents/extracted/{args.document_id}.json#{item['item_id']}\n---\n\n# Requirement\n\n{item['text']}\n\n# Acceptance Criteria\n\n- Review and approve before implementation.\n\n# Open Questions\n\n- None captured at promotion time.\n",
                encoding="utf-8",
            )
            existing_requirements.append(path.read_text(encoding="utf-8", errors="ignore").lower())
            promoted.append({"item_id": item["item_id"], "target": str(path.relative_to(root))})
        elif item["type"] in KNOWLEDGE_TYPES and args.target in {"all", "knowledge"}:
            kid = next_know_id(root)
            confidence = knowledge_confidence(manifest.get("authority", "UNVERIFIED"), item)
            path = root / ".ai" / "knowledge" / f"{kid}-{slug(item['text'])}.md"
            path.write_text(
                f"---\nid: {kid}\ntitle: {item['text'][:80]}\nclass: {item['type'] if item['type'] != 'API_CONTRACT' else 'API_BEHAVIOR'}\nproject: {root.name}\nscope: PROJECT\nconfidence: {confidence}\nstatus: ACTIVE\ncreated: {now()[:10]}\nupdated: {now()[:10]}\nsource_type: DOCUMENT\nsource_ref: .ai/documents/extracted/{args.document_id}.json#{item['item_id']}\ntags: [document-intelligence]\nrelated_requirements: []\nrelated_decisions: []\n---\n\n# Knowledge\n\n{item['text']}\n\n# Evidence\n\nExtracted from `{args.document_id}` at `{item['source_location']}` with `{item['extraction_confidence']}` extraction confidence and reviewed as APPROVE.\n\n# Applicability\n\nProject-local unless later promoted to reusable scope.\n\n# Exceptions\n\nNone captured.\n\n# Operational Impact\n\nConsider this record during planning and Blind Spot Pass.\n\n# Revalidation Trigger\n\nDocument superseded, source changes, or implementation evidence contradicts the extracted item.\n",
                encoding="utf-8",
            )
            promoted.append({"item_id": item["item_id"], "target": str(path.relative_to(root))})
        else:
            blocked.append({"item_id": item["item_id"], "reason": f"no promotion target for type {item['type']}"})
    manifest.update({
        "promotion_status": "PARTIALLY_APPROVED" if blocked and promoted else ("APPROVED" if promoted else "REJECTED"),
        "status": "PARTIALLY_APPROVED" if blocked and promoted else ("APPROVED" if promoted else manifest.get("status")),
    })
    write_json(manifest_path(root, args.document_id), manifest)
    promotion = {"document_id": args.document_id, "promoted": promoted, "blocked": blocked}
    write_json(root / ".ai" / "documents" / "processed" / f"{args.document_id}-promotion.json", promotion)
    run_path = root / ".ai" / "documents" / "runs" / f"{args.document_id}.json"
    if run_path.exists():
        run = load_json(run_path)
        run.update({"current_stage": "PROMOTED", "promotion_status": manifest["promotion_status"]})
        run["artifacts"]["promotion"] = f".ai/documents/processed/{args.document_id}-promotion.json"
        write_json(run_path, run)
    update_index(root)
    print(f"PROMOTED {args.document_id} promoted={len(promoted)} blocked={len(blocked)} status={manifest['promotion_status']}")


if __name__ == "__main__":
    main()
