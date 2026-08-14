# Phase 3A Memory Test Evidence

Last tested: 2026-08-15

All tests use disposable projects under `ai-project-template/tests/fixtures/`.

## MEM-001 - Knowledge Schema Validation

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo`
- Expected result: all knowledge records pass required metadata, valid class, confidence, status, and source checks.
- Actual result: `SUMMARY pass=14 warn=0 fail=0`
- PASS/FAIL: PASS

## MEM-002 - Decision Schema Validation

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo`
- Expected result: all decision records pass required metadata and valid status checks.
- Actual result: ADR-001 through ADR-005 passed; `SUMMARY pass=14 warn=0 fail=0`
- PASS/FAIL: PASS

## MEM-003 - Knowledge Index Generation

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo`
- Expected result: `.ai/knowledge/index.md` is regenerated from knowledge files.
- Actual result: `PASS knowledge index .../.ai/knowledge/index.md`
- PASS/FAIL: PASS

## MEM-004 - Decision Index Generation

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo`
- Expected result: `.ai/decisions/index.md` is regenerated from decision files.
- Actual result: `PASS decision index .../.ai/decisions/index.md`
- PASS/FAIL: PASS

## MEM-005 - Relevant Memory Retrieval

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo --project phase3a-memory-demo --query "Add JSON export alongside CSV export transactions deterministic fields" --tags export transactions`
- Expected result: Memory Brief includes CSV design knowledge, deterministic column decision, test-backed export pattern, and related accepted decisions.
- Actual result: retrieved KNOW-002, KNOW-003, KNOW-004, KNOW-006 and ADR-001, ADR-003, ADR-005.
- PASS/FAIL: PASS

## MEM-006 - Project Isolation

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3a-isolation-project --project phase3a-isolation-project --query "transaction export CSV JSON deterministic fields" --tags export transactions`
- Expected result: Project B does not retrieve Project A transaction/export memory.
- Actual result: `Relevant Knowledge - None found`; `Relevant Decisions - None found`.
- PASS/FAIL: PASS

## MEM-007 - Conflict Detection

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo` before deprecating KNOW-007.
- Expected result: validator reports `MEMORY CONFLICT` for active alphabetical-order and fixed-order export rules.
- Actual result: validator reported `WARN MEMORY CONFLICT` for KNOW-002 and KNOW-007, including sources and confidence.
- PASS/FAIL: PASS

Resolution command:

```bash
python3 ai-project-template/scripts/capture-knowledge.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo --update-id KNOW-007 --status DEPRECATED --evidence "Resolved on 2026-08-15: REQ-001 and ADR-003 are stronger evidence than superseded ADR-002, so alphabetical ordering is deprecated."
```

Post-resolution validation: `SUMMARY pass=14 warn=0 fail=0`

## MEM-008 - Confidence Evolution

- Command: `python3 ai-project-template/scripts/capture-knowledge.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo --update-id KNOW-006 --confidence VERIFIED --evidence "REQ-002 implementation added normalize_transaction_rows and both CSV/JSON tests passed on 2026-08-15."`
- Expected result: KNOW-006 moves from SUPPORTED to VERIFIED with evidence history.
- Actual result: `PASS updated KNOW-006 ...`
- PASS/FAIL: PASS

## MEM-009 - Decision Superseding

- Command: `python3 ai-project-template/scripts/capture-decision.py ... --id ADR-003 ... --supersedes ADR-002`
- Expected result: ADR-003 is created and ADR-002 is preserved with `status: SUPERSEDED` and `superseded_by: ADR-003`.
- Actual result: `PASS created ADR-003 ...`; `PASS superseded ADR-002 by ADR-003`.
- PASS/FAIL: PASS

## MEM-010 - Memory Brief Generation

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3a-memory-demo --project phase3a-memory-demo --query "Add JSON export alongside CSV export transactions deterministic fields" --tags export transactions --output .ai/context/MEMORY-BRIEF-REQ-002-json-export.md`
- Expected result: Memory Brief is written before planning REQ-002.
- Actual result: `PASS wrote memory brief .../.ai/context/MEMORY-BRIEF-REQ-002-json-export.md`
- PASS/FAIL: PASS

## Supporting Commands

```bash
PYTHONPYCACHEPREFIX=/tmp/codex-pycache-phase3a python3 -m py_compile ai-project-template/scripts/memorylib.py ai-project-template/scripts/capture-knowledge.py ai-project-template/scripts/capture-decision.py ai-project-template/scripts/validate-memory.py ai-project-template/scripts/retrieve-memory.py
bash -n ai-project-template/scripts/init-ai-project.sh
python3 -m unittest discover -s ai-project-template/tests/fixtures/phase3a-memory-demo -p 'test_*.py' -v
```

Supporting results:

- Python scripts compile with redirected bytecode cache.
- Initializer shell syntax passes.
- JSON/CSV fixture tests pass: `Ran 5 tests in 0.000s`, `OK`.
