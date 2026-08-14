---
id: KNOW-BS-301
title: Bulk deletion requires recovery and audit design before implementation
class: KNOWN_PITFALL
project: phase3b-blindspot-demo
scope: REUSABLE
confidence: SUPPORTED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: DECISION
source_ref: .ai/decisions/ADR-301-use-soft-delete-with-per-item-results-for-bulk-user-removal.md
tags: [bulk, deletion, audit, rollback]
related_requirements: [.ai/requirements/REQ-202-bulk-delete-users-resolved.md]
related_decisions: [ADR-301]
---
# Knowledge

Bulk deletion should not be planned until authorization, audit, partial failure, and rollback behavior are defined.

# Evidence

ADR-301 records the resolution of DEEP blind spots for bulk user removal.

# Applicability

Applies to high-impact bulk deletion workflows.

# Exceptions

None known.

# Operational Impact

Use DEEP Blind Spot Pass and map deletion risks into plan, tests, and decisions.

# Revalidation Trigger

Revalidate when deletion policy, retention rules, or data model changes.
