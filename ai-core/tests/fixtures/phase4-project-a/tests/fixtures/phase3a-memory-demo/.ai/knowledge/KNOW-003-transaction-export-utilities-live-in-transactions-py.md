---
id: KNOW-003
title: Transaction export utilities live in transactions.py
class: ARCHITECTURE
project: phase3a-memory-demo
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: CODE
source_ref: transactions.py
tags: [export, architecture, python]
related_requirements: []
related_decisions: []
---
# Knowledge

Transaction export behavior is implemented in transactions.py.

# Evidence

transactions.py defines TRANSACTION_FIELDS and export_transactions_csv.

# Applicability

Applies when adding adjacent export formats in this fixture.

# Exceptions

None known.

# Operational Impact

Add JSON export beside the existing CSV utility rather than creating a separate module.

# Revalidation Trigger

Revalidate if the fixture source layout changes.
