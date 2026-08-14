# AI Project Workflow

This workflow turns a project requirement into implemented, tested work plus enough project memory for another AI or developer to continue later.

## Master Command

Use this invocation:

```text
Execute this requirement using the AI Project Workflow.
```

Expected sequence:

REQUIREMENT -> MEMORY RETRIEVAL -> CONTEXT -> SKILL SELECTION -> BLIND-SPOT IDENTIFICATION -> PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> DECISION -> KNOWLEDGE CAPTURE -> HANDOFF

Do not implement before Gate A passes.

## Gates

### Gate A: Ready To Build

Required before implementation:

- requirement understood
- relevant memory retrieved or confirmed absent
- acceptance criteria identified
- repository context inspected
- unresolved blockers identified

### Gate B: Ready To Test

Required before testing:

- implementation completed
- changed files identified
- tests identified

### Gate C: Ready To Accept

Required before acceptance:

- tests executed
- acceptance criteria checked
- self-review completed
- unresolved risks disclosed

### Gate D: Ready To Handoff

Required before handoff:

- final state documented
- meaningful decisions recorded if needed
- handoff generated
- reusable knowledge captured if applicable

## Artifact Rules

- Requirement: create for approved work with acceptance criteria.
- Plan: create before non-trivial implementation.
- Decision record: create only for meaningful technical/product choices.
- Verification report: create after tests/review.
- Handoff: create when work should be resumable.
- Knowledge entry: create only for stable reusable facts.

Do not create artifacts only to satisfy a checklist.

## Memory Retrieval

Before planning a non-trivial requirement, generate a temporary Memory Brief with relevant knowledge, accepted decisions, unverified items, conflicts, and task impact.

Use selective retrieval through the knowledge and decision indexes. Filter by project, class, tags, related requirement, and keywords instead of reading every memory file.
