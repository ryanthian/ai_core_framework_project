# Memory Brief

## Project Knowledge

- None found.

## Project Decisions

- None found.

## Active Domain Packs

- billing@1.0.0 (ACTIVE)
- access-control@1.0.0 (ACTIVE)

## Relevant Domain Rules

- BILL-DOC-001 - Billing document extraction terms (billing@1.0.0, DOCUMENT_EXTRACTION_HINT, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#document-hints
  Statement: Billing document analysis should treat account, bill, payment, adjustment, arrears, meter, billing cycle, and reconciliation terms as extraction hints, not final classification.
  Tags: document, account, bill, payment, adjustment, arrears, meter, billing-cycle, reconciliation
- BILL-TEST-001 - Billing test pattern (billing@1.0.0, TEST_PATTERN, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#tests
  Statement: Billing tests should include bill creation, partial payment, adjustment, arrears, backdating, historical statement view, and reconciliation checks.
  Tags: partial-payment, adjustment, arrears, reconciliation, test
- BILL-RULE-001 - Historical billing records need traceability (billing@1.0.0, BUSINESS_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#history
  Statement: Historical account statements and payment history should preserve source period, adjustments, backdating, reconciliation status, and audit trail.
  Tags: historical, statement, payment-history, audit, reconciliation
- BILL-GLOSS-001 - Bill and payment are distinct concepts (billing@1.0.0, GLOSSARY, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/billing/README.md#glossary
  Statement: A bill/invoice records an amount due; a payment records value received against one or more obligations.
  Tags: bill, payment, statement, billing

## Domain Blind-Spot Patterns

- None found.

## Unverified Items

- None found.

## Conflicts

- None found.

## Impact On Current Requirement

No reusable project memory matched; inspect repository evidence before planning.
