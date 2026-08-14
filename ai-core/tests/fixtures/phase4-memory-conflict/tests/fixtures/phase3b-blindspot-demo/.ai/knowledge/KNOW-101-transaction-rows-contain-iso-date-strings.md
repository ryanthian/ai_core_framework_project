---
id: KNOW-101
title: Transaction rows contain ISO date strings
class: DATA_MODEL
project: phase3b-blindspot-demo
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: CODE
source_ref: transactions.py
tags: [transactions, date, filter]
related_requirements: []
related_decisions: []
---
# Knowledge

Transaction rows in this fixture store date values as ISO YYYY-MM-DD strings.

# Evidence

transactions.py defines fixture rows with date values such as 2026-08-01.

# Applicability

Applies to date filtering in the Phase 3B transaction fixture.

# Exceptions

None known.

# Operational Impact

Date filtering should parse ISO dates and test invalid non-ISO input.

# Revalidation Trigger

Revalidate if transaction date storage changes.
