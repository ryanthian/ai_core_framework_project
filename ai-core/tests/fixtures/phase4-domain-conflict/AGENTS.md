# AI Project Workflow

Use this workflow for non-trivial software work in this project.

Do not create documentation mechanically. Create or update only the artifacts that are relevant to the current task.

Use the controlled role contracts in `.ai/agents/` when a task is executed through the Agent Harness. A role may reference prior artifacts but must not rewrite another role's artifact silently. Corrections require a revision or a loopback to the responsible role.

When a task begins from a source document, use Document Intelligence first: ingest, parse, analyze, review, then promote only reviewed items into requirements, memory, decisions, context, or handoff artifacts. Do not treat meeting notes as automatically authoritative, and do not promote unreviewed extraction into VERIFIED memory.

When a task uses Domain Packs, only use packs explicitly activated in `.ai/domain-packs.yaml`. Keep domain guidance separate from project facts and surface conflicts instead of silently resolving them.

## Standard Flow

1. Read the requirement.
2. Retrieve relevant project memory.
3. Run Blind Spot Pass.
4. Pass Gate A0: Ready To Plan.
5. Read project context.
6. Inspect the repository.
7. Search/select relevant skills.
8. Create an implementation plan.
9. Pass Gate A: Ready To Build.
10. Implement.
11. Run tests.
12. Perform self-review.
13. Verify acceptance criteria and blind-spot traceability.
14. Record important decisions when they matter.
15. Capture reusable knowledge when applicable.
16. Produce a handoff.

## Gates

### GATE A0: READY TO PLAN

Must have:

- requirement identified
- relevant memory retrieved or confirmed absent
- Blind Spot Pass completed
- no unresolved CRITICAL blind spots
- blocking unknowns identified
- assumptions recorded

If any CRITICAL blind spot remains OPEN, Gate A0 fails and planning must not proceed.

### GATE A: READY TO BUILD

Must have:

- implementation plan
- accepted constraints
- risks mapped
- tests identified
- rollback considered

Do not implement before Gate A passes.

### GATE B: READY TO TEST

Must have:

- implementation completed
- changed files identified
- tests identified

### GATE C: READY TO ACCEPT

Must have:

- tests executed
- acceptance criteria checked
- review completed
- unresolved risks disclosed

### GATE D: READY TO HANDOFF

Must have:

- final state documented
- decisions recorded if needed
- handoff generated
- reusable knowledge captured if applicable

## Memory Rules

- Existing VERIFIED knowledge should be reused before asking the same question again.
- UNVERIFIED knowledge must be clearly marked.
- New implementation evidence can upgrade knowledge confidence.
- Conflicting knowledge must not be silently overwritten.
- If two records conflict, surface the conflict, compare newer or stronger evidence, then deprecate or supersede appropriately.
- Decisions are immutable history; changes create new decisions or safe status changes.
- Secrets and credentials must never enter knowledge memory.
- Personal conversational details unrelated to the project must not enter project memory.

## Master Invocation

When the user says:

```text
Execute this requirement using the AI Project Workflow.
```

Codex should:

REQUIREMENT -> MEMORY RETRIEVAL -> BLIND SPOT PASS -> GATE A0 -> SKILL SELECTION -> PLAN -> GATE A -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> DECISION -> KNOWLEDGE CAPTURE -> HANDOFF

Do not automatically implement before completing Gate A.
