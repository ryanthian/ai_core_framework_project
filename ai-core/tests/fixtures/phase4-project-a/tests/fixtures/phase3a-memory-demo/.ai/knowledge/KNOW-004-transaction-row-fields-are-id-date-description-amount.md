---
id: KNOW-004
title: Transaction row fields are id date description amount
class: DATA_MODEL
project: phase3a-memory-demo
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: CODE
source_ref: transactions.py
tags: [transactions, data-model, fields]
related_requirements: []
related_decisions: []
---
# Knowledge

A transaction row uses the fields id, date, description, and amount.

# Evidence

TRANSACTION_FIELDS in transactions.py contains those four fields.

# Applicability

Applies to fixture export serialization.

# Exceptions

None known.

# Operational Impact

New export formats should preserve these field names unless a new requirement changes the model.

# Revalidation Trigger

Revalidate when TRANSACTION_FIELDS changes.
