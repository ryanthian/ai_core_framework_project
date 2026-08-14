---
id: KNOW-006
title: Table exports share field normalization before serialization
class: REUSABLE_PATTERN
project: phase3a-memory-demo
scope: REUSABLE
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: DECISION
source_ref: .ai/decisions/ADR-001-use-csv-dictwriter-for-csv-export.md
tags: [export, pattern, serialization]
related_requirements: []
related_decisions: [ADR-001]
---
# Knowledge

Normalize rows to the approved field list before passing them to an export serializer.

# Evidence

ADR-001 chose DictWriter with a fixed field list; JSON export has not yet implemented the pattern.

Update 2026-08-15: REQ-002 implementation added normalize_transaction_rows and both CSV/JSON tests passed on 2026-08-15.

# Applicability

Applies to small in-memory table export utilities.

# Exceptions

None known.

# Operational Impact

Add a shared row-normalization helper before implementing additional export formats.

# Revalidation Trigger

Revalidate after a second export format is implemented and tested.
