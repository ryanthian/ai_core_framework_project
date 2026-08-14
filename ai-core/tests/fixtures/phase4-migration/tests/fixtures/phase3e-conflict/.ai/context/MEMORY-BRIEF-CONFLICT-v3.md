# Memory Brief

## Project Knowledge

- None found.

## Project Decisions

- None found.

## Active Domain Packs

- data-change@1.0.0 (ACTIVE)
- test-domain-conflict@1.0.0 (EXPERIMENTAL)

## Relevant Domain Rules

- DATA-RULE-001 - Bulk data changes need rollback and partial failure semantics (data-change@1.0.0, DATA_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/data-change/README.md#bulk
  Statement: Bulk data changes should define transactionality, partial-failure semantics, rollback, history retention, and audit trail.
  Tags: bulk, delete, rollback, partial-failure, audit
- TDC-RULE-001 - Test conflicting deletion rule (test-domain-conflict@1.0.0, DATA_RULE, UNVERIFIED)
  Source: DOMAIN_PACK domain-packs/test-domain-conflict/README.md#conflict
  Statement: Test-only guidance says bulk deletion should not retain history.
  Tags: bulk, delete, history, test

## Domain Blind-Spot Patterns

- None found.

## Unverified Items

- None found.

## Conflicts

- None found.
DOMAIN_PROJECT_CONFLICT
- Domain: DATA-RULE-001 Bulk data changes need rollback and partial failure semantics source=DOMAIN_PACK:domain-packs/data-change/README.md#bulk confidence=SUPPORTED
- Project: current requirement requires permanent deletion
Recommended resolution: compare authority; do not silently override the project requirement.
DOMAIN_DOMAIN_CONFLICT
- Domain A: DATA-RULE-001 Bulk data changes need rollback and partial failure semantics (data-change@1.0.0)
- Domain B: TDC-RULE-001 Test conflicting deletion rule (test-domain-conflict@1.0.0)
Recommended resolution: disable or remove the test/weak pack; do not silently merge contradictory domain guidance.

## Impact On Current Requirement

No reusable project memory matched; inspect repository evidence before planning.
