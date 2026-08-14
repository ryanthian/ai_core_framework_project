# Memory Rules

## Knowledge Classes

- PROJECT_FACT
- BUSINESS_RULE
- ARCHITECTURE
- INTEGRATION
- DATA_MODEL
- API_BEHAVIOR
- SECURITY_RULE
- UI_RULE
- OPERATIONAL_RULE
- KNOWN_PITFALL
- REUSABLE_PATTERN
- GLOSSARY
- CONSTRAINT

## Confidence

- VERIFIED: Confirmed by code, tests, authoritative project documentation, or trusted system evidence.
- SUPPORTED: Strong supporting evidence exists but not fully verified.
- UNVERIFIED: Captured for follow-up and must not be treated as fact.
- DEPRECATED: Previously valid but no longer applicable.

Codex must never silently promote UNVERIFIED knowledge to VERIFIED.

## Sources

Supported source types:

- CODE
- TEST
- REQUIREMENT
- DECISION
- DOCUMENT
- API_RESPONSE
- USER_CONFIRMED
- SYSTEM_OBSERVATION
- HANDOFF

Each knowledge record must store source type, source reference, date captured, project, and confidence. If a source cannot be traced, the knowledge must not be VERIFIED.

## Operating Rules

1. Existing VERIFIED knowledge should be reused before asking the same question again.
2. UNVERIFIED knowledge must be clearly marked.
3. New implementation evidence can upgrade knowledge confidence.
4. Conflicting knowledge must not be silently overwritten.
5. If two records conflict, surface the conflict, compare newer/stronger evidence, then deprecate or supersede appropriately.
6. Decisions are immutable history. Changes create new decisions or safe status updates.
7. Secrets and credentials must never enter knowledge memory.
8. Personal conversational details unrelated to the project must not enter project memory.

## Retrieval Workflow

Before planning a non-trivial requirement, retrieve selectively:

1. relevant project context
2. knowledge index
3. matching knowledge entries
4. decision index
5. relevant accepted decisions
6. current requirement
7. repository evidence

Filter by project, class, tags, related requirement, and keywords. Do not read every knowledge file when the index can narrow the search.

## Memory Brief

Before Gate A, generate a temporary task-level Memory Brief with:

- relevant knowledge
- relevant decisions
- unverified items
- conflicts
- impact on the current requirement

The brief does not need to become permanent unless it is useful evidence.
