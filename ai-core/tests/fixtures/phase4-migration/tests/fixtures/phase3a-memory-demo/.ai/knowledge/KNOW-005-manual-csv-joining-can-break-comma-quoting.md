---
id: KNOW-005
title: Manual CSV joining can break comma quoting
class: KNOWN_PITFALL
project: phase3a-memory-demo
scope: REUSABLE
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: TEST
source_ref: test_transactions.py
tags: [csv, quoting, testing]
related_requirements: []
related_decisions: []
---
# Knowledge

Manual CSV string joining is risky because comma-containing values require proper quoting.

# Evidence

test_transactions.py verifies that a description containing a comma is quoted.

# Applicability

Applies to Python CSV export utilities and similar table serialization tasks.

# Exceptions

None known.

# Operational Impact

Use a CSV library or equivalent tested encoder instead of joining fields manually.

# Revalidation Trigger

Revalidate if export requirements or serialization library behavior changes.
