#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re

from domainlib import project_root, today


def slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")[:60] or "candidate"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--source-knowledge", required=True)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--statement", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--why-reusable", required=True)
    parser.add_argument("--decision", choices=["APPROVE", "REJECT", "NEEDS_MORE_EVIDENCE"], default="NEEDS_MORE_EVIDENCE")
    args = parser.parse_args()
    root = project_root(args.project)
    path = root / ".ai" / "domain-candidates" / f"{args.candidate_id}-{slug(args.statement)}.md"
    if path.exists():
        raise SystemExit(f"FAIL candidate already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Domain Candidate\n\nCandidate ID: {args.candidate_id}\nSource Project: {root.name}\nSource Knowledge: {args.source_knowledge}\nProposed Domain: {args.domain}\nProposed Type: {args.type}\nStatement: {args.statement}\n\n## Evidence\n\n{args.evidence}\n\n## Why Reusable\n\n{args.why_reusable}\n\n## Known Exceptions\n\nNone captured.\n\n## Confidence\n\nSUPPORTED\n\n## Reviewer Decision\n\nDecision: {args.decision}\nDate: {today()}\n",
        encoding="utf-8",
    )
    print(f"CANDIDATE {args.candidate_id} {path.relative_to(root)}")


if __name__ == "__main__":
    main()
