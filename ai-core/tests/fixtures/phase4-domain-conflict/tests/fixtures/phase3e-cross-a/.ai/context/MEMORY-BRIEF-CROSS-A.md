# Memory Brief

## Project Knowledge

- KNOW-XA-001 - Project A only marker rule (PROJECT_FACT, VERIFIED, PROJECT)
  Source: REQUIREMENT .ai/requirements/README.md
  Impact: Project B retrieval must not include this marker.

## Project Decisions

- None found.

## Active Domain Packs

- access-control@1.0.0 (ACTIVE)

## Relevant Domain Rules

- AC-BS-001 - Role boundary and audit blind spot (access-control@1.0.0, BLIND_SPOT_PATTERN, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/access-control/README.md#blind-spots
  Statement: When staff or support roles access customer records, ask who may access which records, why, with what audit trail, and what masking applies.
  Tags: role, audit, privilege, support, staff
- AC-RULE-001 - User-specific records require identity and ownership checks (access-control@1.0.0, SECURITY_RULE, SUPPORTED)
  Source: DOMAIN_PACK domain-packs/access-control/README.md#identity-ownership
  Statement: Any feature exposing user-specific records should evaluate identity, ownership, privilege, tenant boundary, and auditability.
  Tags: identity, ownership, authorization, statements, records

## Domain Blind-Spot Patterns

- AC-BS-001 (access-control): When staff or support roles access customer records, ask who may access which records, why, with what audit trail, and what masking applies.

## Unverified Items

- None found.

## Conflicts

- None found.

## Impact On Current Requirement

Use retrieved VERIFIED/SUPPORTED records before planning. Treat UNVERIFIED items as questions, not facts.
