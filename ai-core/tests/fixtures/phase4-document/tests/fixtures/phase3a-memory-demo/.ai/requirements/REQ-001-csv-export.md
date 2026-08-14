# Requirement

- Requirement ID: REQ-001
- Title: CSV export for transaction rows
- Source: Phase 3A memory fixture
- Date: 2026-08-15

## Acceptance Criteria

- Export columns in fixed order: `id`, `date`, `description`, `amount`.
- Include a header row.
- Quote comma-containing values correctly.
- Return only the header for empty input.

