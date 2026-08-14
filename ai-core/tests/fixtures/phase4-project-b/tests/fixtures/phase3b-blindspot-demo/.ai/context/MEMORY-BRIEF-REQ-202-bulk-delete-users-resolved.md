# Memory Brief

## Relevant Knowledge

- KNOW-OWN-001 - Only account owners may view private transaction details (BUSINESS_RULE, VERIFIED, PROJECT)
  Source: REQUIREMENT .ai/requirements/REQ-401-account-statement-lookup.md
  Impact: Statement lookup must include an ownership check before returning private transaction details.
- KNOW-OWN-002 - Any support user may view private transaction details (BUSINESS_RULE, SUPPORTED, PROJECT)
  Source: DOCUMENT docs/known-issues.md
  Impact: If used, this could bypass the ownership rule.

## Relevant Decisions

- None found.

## Unverified Items

- None found.

## Memory Conflicts

- None found.

## Impact On Current Requirement

Use retrieved VERIFIED/SUPPORTED records before planning. Treat UNVERIFIED items as questions, not facts.
