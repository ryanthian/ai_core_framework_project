# Memory Brief

## Relevant Knowledge

- KNOW-003 - Transaction export utilities live in transactions.py (ARCHITECTURE, VERIFIED, PROJECT)
  Source: CODE transactions.py
  Impact: Add JSON export beside the existing CSV utility rather than creating a separate module.
- KNOW-002 - Transaction export columns follow fixed business order (BUSINESS_RULE, VERIFIED, PROJECT)
  Source: REQUIREMENT .ai/requirements/REQ-001-csv-export.md
  Impact: Export implementations must not sort fields alphabetically.
- KNOW-004 - Transaction row fields are id date description amount (DATA_MODEL, VERIFIED, PROJECT)
  Source: CODE transactions.py
  Impact: New export formats should preserve these field names unless a new requirement changes the model.
- KNOW-006 - Table exports share field normalization before serialization (REUSABLE_PATTERN, SUPPORTED, REUSABLE)
  Source: DECISION .ai/decisions/ADR-001-use-csv-dictwriter-for-csv-export.md
  Impact: Add a shared row-normalization helper before implementing additional export formats.
- KNOW-007 - Transaction export columns are alphabetical (BUSINESS_RULE, SUPPORTED, PROJECT)
  Source: DECISION .ai/decisions/ADR-002-export-columns-alphabetically.md
  Impact: If active, this would incorrectly push implementations toward alphabetical field sorting.

## Relevant Decisions

- ADR-001 - Use csv DictWriter for CSV export (ACCEPTED)
  Related requirement: .ai/requirements/REQ-001-csv-export.md
  Why: The standard library handles quoting and deterministic field order without dependencies.
- ADR-003 - Use business-defined fixed export order (ACCEPTED)
  Related requirement: .ai/requirements/REQ-001-csv-export.md
  Why: Requirement and tests are stronger evidence than the earlier convenience decision.

## Unverified Items

- None found.

## Memory Conflicts

MEMORY CONFLICT
- KNOW-002 Transaction export columns follow fixed business order source=REQUIREMENT:.ai/requirements/REQ-001-csv-export.md confidence=VERIFIED
- KNOW-007 Transaction export columns are alphabetical source=DECISION:.ai/decisions/ADR-002-export-columns-alphabetically.md confidence=SUPPORTED
Recommended resolution: compare source strength and date; deprecate or supersede the weaker record without deleting history.

## Impact On Current Requirement

Use retrieved VERIFIED/SUPPORTED records before planning. Treat UNVERIFIED items as questions, not facts.
