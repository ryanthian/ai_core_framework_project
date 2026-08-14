# AI-Core Architecture

AI-Core is the Phase 4 integration layer. It coordinates existing project workflow subsystems through one runtime, one canonical run state, and one artifact registry.

## Layers

CLI / future UI
AI-Core Controller
Workflow Engine
Service Adapters
Existing Phase 1-3 subsystems

## Services

- ProjectService owns `.ai/project.json` and `.ai/ai-core.yaml`.
- RunService owns canonical run state in `.ai/runs/<RUN-ID>/run.json`.
- DocumentService wraps Document Intelligence scripts.
- MemoryService wraps memory retrieval, capture, validation, and conflict surfacing.
- DomainService wraps active domain packs and relevant rule retrieval.
- BlindSpotService wraps Blind Spot Pass and Gate A0 inputs.
- SkillService discovers and selects existing skills. It does not install skills.
- AgentService wraps the controlled agent harness and role contracts.
- ValidationService checks artifact integrity and completion semantics.

## State

Project state is stored in `.ai/project.json`.

Runtime configuration is stored in `.ai/ai-core.yaml`.

Each AI-Core run has:

- `.ai/runs/<RUN-ID>/run.json`
- `.ai/runs/<RUN-ID>/artifacts.json`
- `.ai/runs/<RUN-ID>/events.jsonl`
- `.ai/runs/<RUN-ID>/traceability.md`
- `.ai/runs/<RUN-ID>/summary.md`

Subsystem state remains in its existing location and is registered as an artifact.

## Entry Paths

Structured requirement:

REQUIREMENT -> REQUIREMENT_ANALYSIS -> MEMORY_RETRIEVAL -> DOMAIN_RETRIEVAL -> BLIND_SPOT -> GATE_A0 -> SKILL_SELECTION -> PLANNING -> GATE_A -> IMPLEMENTATION -> TESTING -> REVIEW -> VERIFICATION -> GATE_C -> MEMORY_CURATION -> HANDOFF -> GATE_D -> COMPLETE

Source document:

DOCUMENT -> INGEST -> DOCUMENT_ANALYSIS -> REVIEW/PROMOTION -> REQUIREMENT_ANALYSIS -> MEMORY_RETRIEVAL -> DOMAIN_RETRIEVAL -> BLIND_SPOT -> gates and implementation workflow

## Gates

Gate A0 blocks planning when critical blind spots, memory conflicts, document conflicts, or material domain conflicts are unresolved.

Gate A blocks implementation until a plan exists.

Gate C blocks acceptance until tests, review, and verification evidence exist.

Gate D blocks completion until handoff and memory curation are handled.

## Error Handling

AI-Core records structured errors with:

- code
- message
- stage
- severity
- recoverable
- recommended_action

Human approval cases create explicit `.ai/human-actions/HUMAN-*.json` tasks.

## Resume

Resume loads only persisted run state and artifact registry. It does not require chat history.

Cancelled runs are preserved and cannot continue without a future explicit reopen mechanism.

## Project Isolation

Project data lives under the project `.ai/` root. Shared resources are limited to reusable skills and domain pack sources. Memory, documents, decisions, and runs are project-local unless separately marked reusable by the existing memory/domain systems.
