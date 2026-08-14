---
id: ADR-003
title: Use business-defined fixed export order
date: 2026-08-15
status: ACCEPTED
scope: PROJECT
related_requirement: .ai/requirements/REQ-001-csv-export.md
related_knowledge: []
related_commit_pr: 
supersedes: ADR-002
superseded_by: 
---
# Context

REQ-001 and tests define the exact transaction export field order.

# Problem

Alphabetical ordering conflicts with the approved acceptance criteria.

# Decision

Use the fixed business-defined order id, date, description, amount.

# Why

Requirement and tests are stronger evidence than the earlier convenience decision.

# Alternatives

Keep alphabetical order.

# Consequences

Exports remain stable and match downstream expectations.

# Risks

Future schema changes must update the requirement, tests, and knowledge entry together.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
