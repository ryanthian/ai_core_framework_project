# Memory Brief

## Project Knowledge

- None found.

## Project Decisions

- None found.

## Active Domain Packs

- data-change@1.0.0 (ACTIVE)

## Relevant Domain Rules

- DATA-RULE-001 - Bulk data changes need rollback and partial failure semantics (data-change@1.0.0, DATA_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/data-change/README.md#bulk
  Statement: Bulk data changes should define transactionality, partial-failure semantics, rollback, history retention, and audit trail.
  Tags: bulk, delete, rollback, partial-failure, audit

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

## Impact On Current Requirement

No reusable project memory matched; inspect repository evidence before planning.
