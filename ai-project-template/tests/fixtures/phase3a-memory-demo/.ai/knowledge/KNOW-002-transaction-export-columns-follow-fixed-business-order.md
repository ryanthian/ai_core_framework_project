---
id: KNOW-002
title: Transaction export columns follow fixed business order
class: BUSINESS_RULE
project: phase3a-memory-demo
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: REQUIREMENT
source_ref: .ai/requirements/REQ-001-csv-export.md
tags: [export, columns, transactions]
related_requirements: [.ai/requirements/REQ-001-csv-export.md]
related_decisions: [ADR-003]
---
# Knowledge

Transaction exports use the fixed column order id, date, description, amount.

# Evidence

REQ-001 acceptance criteria define this exact order.

# Applicability

Applies to CSV and related transaction exports in this fixture.

# Exceptions

Future requirements may add fields, but must update tests and memory.

# Operational Impact

Export implementations must not sort fields alphabetically.

# Revalidation Trigger

Revalidate when the transaction export requirement or schema changes.
