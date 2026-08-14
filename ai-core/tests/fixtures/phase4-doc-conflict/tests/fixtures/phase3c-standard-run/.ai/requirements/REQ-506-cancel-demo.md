---
id: REQ-506
title: Cancellation demo
project: phase3c-standard-run
status: DRAFT
created: 2026-08-15
---

# Requirement

Start a disposable harness run and cancel it before implementation.

# Acceptance Criteria

- Run state preserves the cancellation reason.
- Existing artifacts are not deleted.
- Event log records `RUN_CANCELLED`.
