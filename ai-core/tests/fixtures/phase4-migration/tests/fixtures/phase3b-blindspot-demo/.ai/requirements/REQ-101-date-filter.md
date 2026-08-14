# Requirement

- Requirement ID: REQ-101
- Title: Allow filtering transactions by date range
- Source: Phase 3B STANDARD Blind Spot demo
- Date: 2026-08-15

## Objective

Add a reusable function that filters transaction rows by date range.

## Acceptance Criteria

- Start and end bounds are inclusive.
- Dates use ISO `YYYY-MM-DD` strings.
- A range with no matches returns an empty list.
- If start date is after end date, return an empty list.
- Invalid date input raises `ValueError`.
- Unit tests cover boundary, empty, invalid, and reversed ranges.

