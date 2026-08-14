---
id: ADR-001
title: Use csv DictWriter for CSV export
date: 2026-08-15
status: ACCEPTED
scope: PROJECT
related_requirement: .ai/requirements/REQ-001-csv-export.md
related_knowledge: []
related_commit_pr: 
supersedes: 
superseded_by: 
---
# Context

Transaction export must quote CSV values correctly in the fixture.

# Problem

Manual CSV construction risks broken quoting and unstable output.

# Decision

Use Python csv.DictWriter with a fixed field list.

# Why

The standard library handles quoting and deterministic field order without dependencies.

# Alternatives

Manual string joining; third-party export package.

# Consequences

CSV line endings follow Python csv writer behavior.

# Risks

Production exports may need formula-injection hardening.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
