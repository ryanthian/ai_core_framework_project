# AI-Core Framework Project

Private framework repository for the phased AI-assisted development foundation.

## Current Foundation

TOOLS -> SKILLS -> PROJECT WORKFLOW -> KNOWLEDGE + DECISION MEMORY -> BLIND SPOT PASS -> CONTROLLED AGENT HARNESS -> DOCUMENT INTELLIGENCE -> DOMAIN KNOWLEDGE PACKS -> AI-CORE INTEGRATION

## Main Directories

- `codex-skills/` - reusable Codex skills toolbox, source lock, smoke tests, rollback docs.
- `ai-project-template/` - reusable project workflow, memory, document intelligence, domain activation, blind spots, and agent harness scripts/templates.
- `domain-packs/` - reusable domain knowledge packs.
- `ai-core/` - Phase 4 runtime/controller, adapters, services, docs, tests, and disposable verification fixtures.
- `docs/` - workspace-level registries.

## Verification

Core Phase 4 verification:

```bash
PYTHONPYCACHEPREFIX=/tmp/codex-pycache-phase4 python3 -m py_compile ai-core/runtime/*.py ai-core/services/*.py ai-core/tests/run-core-tests.py
python3 ai-core/tests/run-core-tests.py
```

Expected:

```text
SUMMARY pass=30 fail=0
```

## CLI Installation

```bash
pip install -e .
ai-core version
```

Daily entry point:

```bash
ai-core status
ai-core next
```

## Scope

This repository stores the framework itself. It does not include production application code.
