# Decision Record

- Decision ID: ADR-001
- Date: 2026-08-14
- Related Requirement: REQ-001
- Related Commit / PR: Not applicable; workspace fixture only.

## Context

The requirement needs CSV serialization for a small transaction table in a disposable fixture.

## Decision

Use Python standard library `csv.DictWriter` instead of hand-building CSV strings.

## Alternatives Considered

- Manual string joining.
- Third-party CSV/export package.

## Why Chosen

`csv.DictWriter` handles quoting and column order without adding dependencies.

## Consequences

Output uses standard CSV line endings from Python's CSV writer.

## Risks

Tests must assert the expected `\r\n` output so line-ending behavior is explicit.

## Rollback / Revisit Conditions

Revisit if a real project needs streaming, localization, custom dialects, or spreadsheet formula-injection hardening.

