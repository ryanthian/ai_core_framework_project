# AI Project Workflow

This workflow turns a project requirement into implemented, tested work plus enough project memory for another AI or developer to continue later.

## Master Command

Use this invocation:

```text
Execute this requirement using the AI Project Workflow.
```

Expected sequence:

REQUIREMENT -> MEMORY RETRIEVAL -> BLIND SPOT PASS -> GATE A0 -> SKILL SELECTION -> PLAN -> GATE A -> IMPLEMENT -> TEST -> REVIEW -> VERIFY -> DECISION -> KNOWLEDGE CAPTURE -> HANDOFF

Do not plan before Gate A0 passes. Do not implement before Gate A passes.

## AI-Core Entry Path

Phase 4 AI-Core coordinates the workflow through one canonical runtime:

SOURCE DOCUMENT or STRUCTURED REQUIREMENT -> AI-Core input router -> document intelligence when applicable -> requirement analysis -> memory retrieval -> domain retrieval -> Blind Spot Pass -> gates -> controlled Agent Harness -> testing/review/verification -> knowledge/decision capture -> handoff.

AI-Core records canonical run state and artifacts, but it does not replace role contracts, project memory rules, domain pack precedence, document review gates, or Codex reasoning.

## Gates

### Gate A0: Ready To Plan

Required before planning:

- requirement identified
- relevant memory retrieved or confirmed absent
- Blind Spot Pass completed
- no unresolved CRITICAL blind spots
- blocking unknowns identified
- assumptions recorded

### Gate A: Ready To Build

Required before implementation:

- implementation plan
- accepted constraints
- risks mapped
- tests identified
- rollback considered

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

Before planning a non-trivial requirement, generate a temporary Memory Brief with project knowledge, accepted decisions, active domain packs, relevant domain rules, domain blind-spot patterns, unverified items, conflicts, and task impact.

Use selective retrieval through the knowledge and decision indexes. Filter by project, class, tags, related requirement, and keywords instead of reading every memory file.

Active domain packs are retrieved selectively from `.ai/domain-packs.yaml`; do not load every pack into every task.

## Blind Spot Pass

After memory retrieval and before planning, create a Blind Spot Report. Skill selection may happen partially before this if a skill assists analysis, but implementation-specific skill selection should happen after risks are understood.

Use QUICK for small low-risk changes, STANDARD by default, and DEEP for security, authorization, billing, finance, external APIs, data migration, bulk changes, deletion, sensitive data, or high uncertainty.

## Controlled Agent Harness

Phase 3C adds controlled role execution:

```text
REQUIREMENT
↓
REQUIREMENT ANALYST
↓
MEMORY RETRIEVER
↓
BLIND SPOT REVIEWER
↓
GATE A0
↓
SKILL SELECTOR
↓
PLANNER
↓
GATE A
↓
IMPLEMENTER
↓
TESTER
↙        ↘
FAIL      PASS
↓           ↓
IMPLEMENTER REVIEWER
↙      ↘
CHANGES      APPROVE
↓           ↓
IMPLEMENTER   VERIFIER
↓
GATE C
↓
MEMORY CURATOR
↓
HANDOFF WRITER
↓
GATE D
```

Role contracts live in `.ai/agents/`. Run state and events live in `.ai/runs/`. Scripts coordinate state and gates; Codex performs reasoning under the current role contract.

## Document Intelligence

Use this path when the input is a source document rather than an already structured requirement:

```text
DOCUMENT
↓
INGEST
↓
PARSE / EXTRACT
↓
DOCUMENT ANALYST
↓
DOCUMENT REVIEWER
↓
APPROVED PROMOTION
↓
REQUIREMENT ANALYST
↓
MEMORY RETRIEVER
↓
BLIND SPOT REVIEWER
↓
...
```

Parsing obtains text and source locations. Document Analyst proposes structured intelligence. Document Reviewer approves, corrects, rejects, flags duplicates, or surfaces conflicts. Promotion requires reviewed items and preserves source traceability.

Do not promote unreviewed extraction directly into VERIFIED memory. Meeting notes are not automatically authoritative. Scanned PDFs without extractable text must be marked `OCR_REQUIRED`.

## Domain Packs

Domain packs provide reusable, version-pinned domain guidance. Codex may recommend packs, but activation must be explicit in `.ai/domain-packs.yaml`.

```text
INPUT
↓
DOCUMENT INTELLIGENCE if needed
↓
REQUIREMENT ANALYST
↓
PROJECT MEMORY + ACTIVE DOMAIN PACKS
↓
MEMORY BRIEF
↓
BLIND SPOT PASS
↓
GATE A0
↓
SKILL SELECTION
↓
PLAN
↓
IMPLEMENT
↓
TEST
↓
REVIEW
↓
VERIFY
↓
PROJECT MEMORY
↓
OPTIONAL DOMAIN CANDIDATE
↓
HANDOFF
```

Project-specific authoritative knowledge takes precedence over generic domain guidance unless there is a material contradiction, which must be surfaced as a conflict.
