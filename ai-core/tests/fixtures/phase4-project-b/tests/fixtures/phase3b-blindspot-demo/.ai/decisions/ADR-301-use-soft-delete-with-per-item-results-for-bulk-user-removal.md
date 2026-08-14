---
id: ADR-301
title: Use soft delete with per-item results for bulk user removal
date: 2026-08-15
status: ACCEPTED
scope: PROJECT
related_requirement: .ai/requirements/REQ-202-bulk-delete-users-resolved.md
related_knowledge: []
related_commit_pr: 
supersedes: 
superseded_by: 
---
# Context

DEEP Blind Spot Pass found irreversible deletion and partial failure risks.

# Problem

Bulk user removal can cause data loss and inconsistent state if hard deleted all at once.

# Decision

Use soft delete, explicit authorization, audit trail, confirmation, rollback window, and per-item results.

# Why

This resolves CRITICAL deletion risks while preserving recovery and support evidence.

# Alternatives

Hard delete all users in one operation; reject bulk delete entirely.

# Consequences

Implementation must store deletion state and audit metadata.

# Risks

Retention rules still need policy confirmation in a real system.

# Revisit Trigger

Requirement, architecture, policy, or production evidence changes.
