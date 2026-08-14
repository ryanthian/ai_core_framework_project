# AI Project Workflow

Use this workflow for non-trivial software work in this project.

Do not create documentation mechanically. Create or update only the artifacts that are relevant to the current task.

## Standard Flow

1. Read the requirement.
2. Retrieve relevant project memory.
3. Read project context.
4. Inspect the repository.
5. Search/select relevant skills.
6. Identify blind spots, unknowns, and risks.
7. Create an implementation plan.
8. Implement.
9. Run tests.
10. Perform self-review.
11. Verify acceptance criteria.
12. Record important decisions when they matter.
13. Capture reusable knowledge when applicable.
14. Produce a handoff.

## Gates

### GATE A: READY TO BUILD

Must have:

- understood requirement
- relevant memory retrieved or confirmed absent
- acceptance criteria
- repository context
- unresolved blockers identified

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

REQUIREMENT -> MEMORY RETRIEVAL -> CONTEXT -> SKILL SELECTION -> BLIND-SPOT IDENTIFICATION -> PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> DECISION -> KNOWLEDGE CAPTURE -> HANDOFF

Do not automatically implement before completing Gate A.
