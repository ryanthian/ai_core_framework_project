---
id: KNOW-007
title: Transaction export columns are alphabetical
class: BUSINESS_RULE
project: phase3a-memory-demo
scope: PROJECT
confidence: DEPRECATED
status: DEPRECATED
created: 2026-08-15
updated: 2026-08-15
source_type: DECISION
source_ref: .ai/decisions/ADR-002-export-columns-alphabetically.md
tags: [export, columns, transactions]
related_requirements: []
related_decisions: [ADR-002]
---
# Knowledge

Transaction exports use alphabetical column order.

# Evidence

ADR-002 accepted alphabetical order before REQ-001 and tests were treated as stronger evidence.

Update 2026-08-15: Resolved on 2026-08-15: REQ-001 and ADR-003 are stronger evidence than superseded ADR-002, so alphabetical ordering is deprecated.

# Applicability

Historical record only; this intentionally conflicts before resolution.

# Exceptions

None known.

# Operational Impact

If active, this would incorrectly push implementations toward alphabetical field sorting.

# Revalidation Trigger

Revalidate when compared with REQ-001 or ADR-003.
