# Controlled Agent Harness

The harness is a controlled orchestration layer, not an autonomous swarm.

Scripts handle state, artifact paths, IDs, validation, gate enforcement, sequencing, traceability, resume, cancellation, and event logging.

Codex handles requirement analysis, blind-spot reasoning, planning, implementation, review, and verification under role contracts.

## Default Sequence

REQUIREMENT_ANALYST
-> MEMORY_RETRIEVER
-> BLIND_SPOT_REVIEWER
-> GATE A0
-> SKILL_SELECTOR
-> PLANNER
-> GATE A
-> IMPLEMENTER
-> TESTER
-> REVIEWER
-> VERIFIER
-> GATE C
-> MEMORY_CURATOR
-> HANDOFF_WRITER
-> GATE D

## Profiles

- LEAN: combines low-risk analysis roles and tester/verifier checks.
- STANDARD: default controlled workflow.
- DEEP: full separation for billing, permissions, payments, financial systems, migration, external APIs, bulk operations, and security-sensitive work.

## Loopbacks

- BLIND_SPOT_REVIEWER -> REQUIREMENT_ANALYST when clarification is needed.
- PLANNER -> BLIND_SPOT_REVIEWER when planning exposes new critical risk.
- TESTER -> IMPLEMENTER when tests fail.
- REVIEWER -> IMPLEMENTER when defects are found.
- VERIFIER -> TESTER / IMPLEMENTER when acceptance criteria fail.
- MEMORY_CURATOR -> VERIFIER when evidence is insufficient to mark knowledge VERIFIED.

Default retry limit: 3 attempts per role. After that the run is BLOCKED and requires human intervention.

## Human Approval Required

Stop with `AWAITING_HUMAN` for:

- CRITICAL risk acceptance
- scope expansion
- destructive data action
- security-sensitive behavior
- production migration
- permission model change
- irreversible action
- unclear authoritative requirement
- new external dependency not already approved

Do not simulate approval.

## Role Contamination

A role may reference prior artifacts but must not rewrite another role's artifact silently. Corrections require a revision or loopback to the responsible role.

Reviewer raises findings; Implementer fixes. Verifier verifies; it does not rewrite test evidence.

## Artifact Dependency Graph

```text
REQ
├── Requirement Analysis
├── Memory Brief
├── Blind Spot Report
├── Skill Selection
└── Plan
    ↓
Implementation Summary
    ↓
Test Evidence
    ↓
Review Report
    ↓
Verification Report
    ↓
Decision / Knowledge
    ↓
Handoff
```

The orchestrator rejects impossible ordering, such as verifier before test evidence.

## Revisioning

Use versioned IDs for material revisions, such as `PLAN-REQ-001-v1` and `PLAN-REQ-001-v2`. Preserve previous versions.

