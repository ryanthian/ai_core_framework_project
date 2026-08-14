---
id: KNOW-001
title: Isolation project has separate memory root
class: PROJECT_FACT
project: phase3a-isolation-project
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: DOCUMENT
source_ref: docs/project-overview.md
tags: [isolation, memory]
related_requirements: []
related_decisions: []
---
# Knowledge

The phase3a-isolation-project fixture stores memory in its own .ai directory.

# Evidence

The initializer created a separate .ai tree and project overview document.

# Applicability

Use this fixture for cross-project isolation tests only.

# Exceptions

None known.

# Operational Impact

Do not retrieve phase3a-memory-demo project facts from this project root.

# Revalidation Trigger

Requirement, dependency, schema, policy, or production behavior changes.
