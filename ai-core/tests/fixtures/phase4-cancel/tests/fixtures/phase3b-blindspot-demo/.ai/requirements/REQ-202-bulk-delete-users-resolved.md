# Requirement

- Requirement ID: REQ-202
- Title: Allow authorized administrators to soft delete user records
- Source: Phase 3B DEEP resolved demo
- Date: 2026-08-15

## Objective

Allow authorized administrators to bulk soft delete user records with explicit confirmation, audit trail, per-item results, and a rollback window.

## Acceptance Criteria

- Only explicitly authorized administrators can perform the action.
- The operation uses soft delete, not hard delete.
- The request requires confirmation with the exact number of affected users.
- Each item returns a result status.
- An audit trail records actor, timestamp, reason, and affected IDs.
- Deleted users can be restored during the rollback window.

