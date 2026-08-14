# Knowledge Entry

- Title: Use standard CSV writer for deterministic transaction exports
- Source: REQ-001 disposable workflow demonstration
- Date: 2026-08-14
- Confidence: High for Python CSV fixtures; lower for production financial exports.
- Project Scope: sample-transactions disposable fixture

## Knowledge

For Python transaction export utilities, prefer `csv.DictWriter` with an explicit field list over manual string joining. It preserves deterministic column order and handles comma quoting.

## Applies When

- Rows are dictionary-like records.
- Output can be built in memory.
- Standard CSV dialect is acceptable.

## Does Not Apply When

- Export size requires streaming.
- A product needs custom spreadsheet dialects.
- Formula-injection hardening is required.

## Evidence

Unit tests cover stable header/order, comma quoting, empty input, and missing values.

