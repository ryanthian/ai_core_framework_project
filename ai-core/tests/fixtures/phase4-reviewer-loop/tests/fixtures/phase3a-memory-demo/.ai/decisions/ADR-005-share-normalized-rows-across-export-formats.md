---
id: ADR-005
title: Share normalized rows across export formats
date: 2026-08-15
status: ACCEPTED
scope: PROJECT
related_requirement: .ai/requirements/REQ-002-json-export.md
related_knowledge: [KNOW-006]
related_commit_pr: 
supersedes: 
superseded_by: 
---
# Context

JSON export was added after CSV export and both need the same row shape.

# Problem

Duplicating field normalization would increase drift between export formats.

# Decision

Use normalize_transaction_rows for CSV and JSON export.

# Why

Retrieved KNOW-006 suggested the pattern and tests verified it across both formats.

# Alternatives

Normalize separately in each export function.

# Consequences

Future export formats can reuse the same helper.

# Risks

If one format later needs different behavior, it must document an exception.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
