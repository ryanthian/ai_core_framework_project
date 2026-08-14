# Implementation Plan

- Requirement: REQ-002
- Date: 2026-08-15

## Memory Retrieval

Memory brief: `.ai/context/MEMORY-BRIEF-REQ-002-json-export.md`

Retrieved:

- KNOW-002 fixed business column order.
- KNOW-003 export utilities live in `transactions.py`.
- KNOW-004 transaction row fields.
- KNOW-006 shared field-normalization pattern.
- ADR-003 fixed export order supersedes ADR-002.

## Repository Context

The fixture has `transactions.py` with CSV export and `test_transactions.py` with CSV tests.

## Files Expected To Change

- `transactions.py`
- `test_transactions.py`
- `.ai/verification/VERIFY-REQ-002-json-export.md`
- `.ai/handoffs/HANDOFF-REQ-002-json-export.md`

## Selected Skills

- `codex-skill-selector`
- `codex-engineering-workflow`

## Implementation Approach

Add `normalize_transaction_rows(rows)` and reuse it from both CSV and JSON export. Add `export_transactions_json(rows)` using Python standard library `json.dumps`.

## Data Impact

No persistent data changes.

## API Impact

Adds local function `export_transactions_json(rows)`.

## Security Impact

No credentials, filesystem writes, or network calls.

## Migration Impact

None.

## Testing Strategy

Add unit tests for row normalization and deterministic JSON output.

## Rollback Strategy

Remove `export_transactions_json`, `normalize_transaction_rows`, and related tests/artifacts from this disposable fixture.

## Risks

Production JSON APIs may require pretty formatting, content-type handling, or schema versioning; out of scope for this fixture.

## Open Questions

None.

## Gate A: Ready To Build

- Requirement understood: yes.
- Memory retrieved: yes.
- Acceptance criteria present: yes.
- Repository context inspected: yes.
- Blockers identified: none.
- Verdict: PASS.

