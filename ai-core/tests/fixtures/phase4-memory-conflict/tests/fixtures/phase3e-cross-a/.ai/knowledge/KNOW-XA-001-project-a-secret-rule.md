---
id: KNOW-XA-001
title: Project A only marker rule
class: PROJECT_FACT
project: phase3e-cross-a
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: REQUIREMENT
source_ref: .ai/domain-packs.yaml
tags: [PROJECT_A_ONLY, domain-isolation]
related_requirements: []
related_decisions: []
---

# Knowledge

PROJECT_A_ONLY domain isolation marker belongs only to Project A.

# Evidence

Disposable Phase 3E isolation fixture.

# Applicability

Only phase3e-cross-a.

# Exceptions

None.

# Operational Impact

Project B retrieval must not include this marker.

# Revalidation Trigger

If project memory scoping changes.
