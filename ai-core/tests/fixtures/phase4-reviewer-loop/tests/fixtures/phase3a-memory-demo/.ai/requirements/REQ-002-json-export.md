# Requirement

- Requirement ID: REQ-002
- Title: Add JSON export alongside existing CSV export
- Source: Phase 3A retrieval demonstration
- Date: 2026-08-15

## Background

- FACT: CSV export already exists in `transactions.py`.
- FACT: Transaction field order is defined by existing project memory.
- UNKNOWN: No production API contract exists for JSON export in this fixture.

## Objective

Add JSON export that reuses the transaction export field normalization pattern.

## Acceptance Criteria

- JSON export uses the same fixed transaction field order as CSV.
- Missing values become empty strings.
- Extra input keys are ignored.
- Output is deterministic.
- Unit tests pass.

