---
id: REQ-507
title: Retry limit demo
project: phase3c-standard-run
status: DRAFT
created: 2026-08-15
---

# Requirement

Demonstrate that the controlled agent harness blocks a loopback after the configured retry limit is reached.

# Acceptance Criteria

- A loopback attempt is recorded.
- Run status becomes `BLOCKED` when retry budget is exhausted.
- The event log records a role failure or blocker.
