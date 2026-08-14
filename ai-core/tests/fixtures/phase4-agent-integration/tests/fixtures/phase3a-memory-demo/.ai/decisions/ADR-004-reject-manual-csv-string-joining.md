---
id: ADR-004
title: Reject manual CSV string joining
date: 2026-08-15
status: REJECTED
scope: PROJECT
related_requirement: .ai/requirements/REQ-001-csv-export.md
related_knowledge: []
related_commit_pr: 
supersedes: 
superseded_by: 
---
# Context

CSV export must quote comma-containing descriptions correctly.

# Problem

Manual joins are easy to get wrong.

# Decision

Do not use manual CSV string concatenation for transaction exports.

# Why

The csv module has tested quoting behavior.

# Alternatives

Use manual string joins.

# Consequences

The implementation stays slightly more verbose but safer.

# Risks

None for this fixture.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
