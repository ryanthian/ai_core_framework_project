---
name: codex-engineering-workflow
description: Use for non-trivial software engineering changes that need disciplined planning, implementation, testing, review, and verification before completion claims.
---

# Codex Engineering Workflow

Use this skill for feature work, bug fixes, refactors, UI changes, deployments, imports, data flows, or any change where correctness matters.

## Workflow

1. Understand the requirement and success condition.
2. Inspect the repository, instructions, current state, and relevant files before editing.
3. Check whether a specific skill can help; select only relevant skills.
4. Plan the smallest coherent change.
5. Implement within the existing architecture and style.
6. Test with the narrowest command that proves the behavior, then broader checks when risk requires it.
7. Review the diff for regressions, unrelated churn, secrets, broken UX, and missing tests.
8. Verify the final state with fresh evidence before claiming completion.
9. Summarize changed files, verification run, unresolved risks, and rollback path.

## Verification Gate

Before saying work is complete, fixed, passing, published, or ready:

1. Identify the command, artifact, screenshot, readback, or inspection that proves the claim.
2. Run or perform that verification in the current turn.
3. Read the output or inspect the artifact.
4. State the result accurately, including gaps.

If verification cannot run, say exactly why and what remains unverified.

## Guardrails

- Do not rewrite architecture unless the requirement demands it.
- Do not touch unrelated files for cleanup.
- Do not hide uncertainty behind confident wording.
- Do not claim external writes, deployments, imports, or UI completion without readback or status evidence.
