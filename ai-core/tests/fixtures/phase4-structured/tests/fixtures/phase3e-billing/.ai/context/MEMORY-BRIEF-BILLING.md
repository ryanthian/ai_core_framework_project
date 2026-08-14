# Memory Brief

## Project Knowledge

- None found.

## Project Decisions

- None found.

## Active Domain Packs

- billing@1.0.0 (ACTIVE)
- access-control@1.0.0 (ACTIVE)

## Relevant Domain Rules

- BILL-RULE-001 - Historical billing records need traceability (billing@1.0.0, BUSINESS_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#history
  Statement: Historical account statements and payment history should preserve source period, adjustments, backdating, reconciliation status, and audit trail.
  Tags: historical, statement, payment-history, audit, reconciliation
- BILL-TEST-001 - Billing test pattern (billing@1.0.0, TEST_PATTERN, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#tests
  Statement: Billing tests should include bill creation, partial payment, adjustment, arrears, backdating, historical statement view, and reconciliation checks.
  Tags: partial-payment, adjustment, arrears, reconciliation, test
- AC-RULE-001 - User-specific records require identity and ownership checks (access-control@1.0.0, SECURITY_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/access-control/README.md#identity-ownership
  Statement: Any feature exposing user-specific records should evaluate identity, ownership, privilege, tenant boundary, and auditability.
  Tags: identity, ownership, authorization, statements, records
- BILL-GLOSS-001 - Bill and payment are distinct concepts (billing@1.0.0, GLOSSARY, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#glossary
  Statement: A bill/invoice records an amount due; a payment records value received against one or more obligations.
  Tags: bill, payment, statement, billing
- AC-BS-001 - Role boundary and audit blind spot (access-control@1.0.0, BLIND_SPOT_PATTERN, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/access-control/README.md#blind-spots
  Statement: When staff or support roles access customer records, ask who may access which records, why, with what audit trail, and what masking applies.
  Tags: role, audit, privilege, support, staff

## Domain Blind-Spot Patterns

- AC-BS-001 (access-control): When staff or support roles access customer records, ask who may access which records, why, with what audit trail, and what masking applies.

## Unverified Items

- None found.

## Conflicts

- None found.

## Impact On Current Requirement

No reusable project memory matched; inspect repository evidence before planning.
