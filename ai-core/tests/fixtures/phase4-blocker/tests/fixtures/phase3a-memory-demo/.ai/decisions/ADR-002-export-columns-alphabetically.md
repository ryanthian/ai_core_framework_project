---
id: ADR-002
title: Export columns alphabetically
date: 2026-08-15
status: SUPERSEDED
scope: PROJECT
related_requirement: .ai/requirements/REQ-001-csv-export.md
related_knowledge: []
related_commit_pr: 
supersedes: 
superseded_by: ADR-003
---
# Context

An early fixture idea preferred predictable alphabetical fields.

# Problem

A default field order was needed before business order was confirmed.

# Decision

Export columns alphabetically.

# Why

Alphabetical order is easy to reproduce but was not yet checked against the requirement.

# Alternatives

Use requirement-defined order.

# Consequences

This may conflict with business-defined export order.

# Risks

Consumers may receive columns in an order that fails acceptance criteria.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
