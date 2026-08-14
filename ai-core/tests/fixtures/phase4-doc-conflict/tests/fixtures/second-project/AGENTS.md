# AI Project Workflow

Use this workflow for non-trivial software work in this project.

Do not create documentation mechanically. Create or update only the artifacts that are relevant to the current task.

## Standard Flow

1. Read project context.
2. Read the relevant requirement.
3. Inspect the repository.
4. Search/select relevant skills.
5. Identify unknowns and risks.
6. Create an implementation plan.
7. Implement.
8. Run tests.
9. Perform self-review.
10. Verify acceptance criteria.
11. Record important decisions when they matter.
12. Produce a handoff.
13. Capture reusable knowledge when applicable.

## Gates

### GATE A: READY TO BUILD

Must have:

- understood requirement
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

## Master Invocation

When the user says:

```text
Execute this requirement using the AI Project Workflow.
```

Codex should:

READ -> SELECT SKILLS -> PLAN -> BUILD -> TEST -> REVIEW -> VERIFY -> RECORD -> HANDOFF

Do not automatically implement before completing Gate A.

