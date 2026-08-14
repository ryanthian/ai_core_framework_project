# Codex_mac Operating Rules

Before implementing a non-trivial task:

1. Read the relevant requirement.
2. Retrieve relevant project memory.
3. Run Blind Spot Pass.
4. Pass Gate A0: Ready To Plan.
5. Read project context.
6. Inspect the repository.
7. Check whether an existing skill can help.
8. Select only relevant skills.
9. Create an implementation plan.
10. Pass Gate A: Ready To Build.
11. Implement.
12. Run tests.
13. Perform self-review.
14. Verify acceptance criteria and blind-spot traceability.
15. Record important decisions when needed.
16. Capture reusable knowledge when applicable.
17. Produce a handoff when the work should be resumable.

Never use a skill merely because it is installed. Skills are capabilities, not mandatory steps.

For the reusable skills toolbox, see `codex-skills/` and `docs/skills-registry.md`.

For the reusable project operating workflow, see `ai-project-template/`.

Do not create documentation mechanically. Only create project workflow artifacts that are relevant to the current task.

When using the controlled Agent Harness, follow role contracts in `.ai/agents/`: roles may reference prior artifacts but must not silently rewrite another role's evidence. Corrections require a revision or a recorded loopback.

When using Document Intelligence, source documents must be ingested, parsed, analyzed, reviewed, and only then promoted. Extracted text is evidence, not automatically truth. Do not promote unreviewed extraction into VERIFIED memory, and never store secrets or credentials in knowledge memory.

When using Domain Packs, only retrieve packs explicitly activated in the project `.ai/domain-packs.yaml`. Domain guidance is reusable context, not project fact; do not load unrelated packs or silently override authoritative project requirements.

When using AI-Core, treat it as the coordinating runtime over the existing workflow, memory, document, domain, blind-spot, skill, agent, verification, knowledge-capture, and handoff subsystems. AI-Core owns canonical project/run state and artifact registration; it must not replace Codex reasoning, bypass gates, auto-accept human approval cases, or silently overwrite conflicting evidence.

## Memory Rules

Existing VERIFIED knowledge should be reused before asking the same question again. UNVERIFIED knowledge must be clearly marked. New implementation evidence can upgrade knowledge confidence, but assumptions must not be promoted to VERIFIED without traceable evidence.

Conflicting knowledge must not be silently overwritten. If two records conflict, surface the conflict, determine newer or stronger evidence, and deprecate or supersede appropriately.

Decisions are immutable history. Changes create new decisions or safe status changes; do not delete decision history.

Secrets, credentials, and personal conversational details unrelated to the project must never enter project memory.

## Workflow Gates

GATE A0 — READY TO PLAN requires: requirement identified, relevant memory retrieved, Blind Spot Pass completed, no unresolved CRITICAL blind spots, blocking unknowns identified, and assumptions recorded.

GATE A — READY TO BUILD requires: implementation plan, accepted constraints, risks mapped, tests identified, and rollback considered.

GATE B — READY TO TEST requires: implementation completed, changed files identified, and tests identified.

GATE C — READY TO ACCEPT requires: tests executed, acceptance criteria checked, review completed, and unresolved risks disclosed.

GATE D — READY TO HANDOFF requires: final state documented, decisions recorded if needed, handoff generated, and reusable knowledge captured if applicable.

Master invocation:

```text
Execute this requirement using the AI Project Workflow.
```

Codex should REQUIREMENT -> MEMORY RETRIEVAL -> BLIND SPOT PASS -> GATE A0 -> SKILL SELECTION -> PLAN -> GATE A -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> DECISION -> KNOWLEDGE CAPTURE -> HANDOFF, and must not plan before Gate A0 or implement before Gate A.
