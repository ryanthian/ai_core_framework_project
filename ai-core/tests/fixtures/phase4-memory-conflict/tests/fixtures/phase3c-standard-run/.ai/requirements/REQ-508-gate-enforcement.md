---
id: REQ-508
title: Gate enforcement negative control
project: phase3c-standard-run
status: DRAFT
created: 2026-08-15
---

# Requirement

Prove that the orchestrator rejects completion of skill selection before Gate A0 passes.

# Acceptance Criteria

- Attempting to complete `SKILL_SELECTOR` before Gate A0 returns a failure.
- The run remains resumable after the rejected command.
