---
id: KNOW-502
title: Category filters should not mutate source transaction rows
class: REUSABLE_PATTERN
project: phase3c-standard-run
scope: REUSABLE
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: TEST
source_ref: test_transactions.py
tags: [category, filter, immutability]
related_requirements: [.ai/requirements/REQ-501-category-filter.md]
related_decisions: []
---
# Knowledge

Transaction category filters should return filtered rows without mutating the source row list.

# Evidence

REQ-501 tests include mutation safety and pass in the disposable fixture.

# Applicability

Small in-memory transaction filter utilities.

# Exceptions

None known.

# Operational Impact

Future filters should preserve input rows and test mutation safety.

# Revalidation Trigger

Revalidate if filtering changes to in-place mutation for performance reasons.
