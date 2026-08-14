# Phase 3B Blind Spot Test Evidence

Last tested: 2026-08-15

All tests use disposable projects under `ai-project-template/tests/fixtures/`.

## BS-001 - Report Schema Validation

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md`
- Input: STANDARD date-filter report.
- Expected: required metadata, blind spots, assumption ledger, unknown ledger, and verdict validate.
- Actual: `SUMMARY pass=5 warn=0 fail=0`
- PASS/FAIL: PASS

## BS-002 - Category Validation

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-202-bulk-delete-users-ready-v3.md`
- Input: DEEP report with `AUTHORIZATION`, `DATA_IMPACT`, `OBSERVABILITY`, and `TRANSACTIONALITY`.
- Expected: all categories are accepted taxonomy values.
- Actual: `SUMMARY pass=6 warn=0 fail=0`
- PASS/FAIL: PASS

## BS-003 - Severity Validation

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-201-bulk-delete-users-blocked.md`
- Input: DEEP blocked report with `CRITICAL` and `HIGH` severities.
- Expected: valid severity values; HIGH open issues warn; OPEN CRITICAL forces BLOCKED.
- Actual: `SUMMARY pass=7 warn=1 fail=0`
- PASS/FAIL: PASS

## BS-004 - Critical Blocker Enforcement

- Command: `python3 ai-project-template/scripts/run-blind-spot-pass.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --requirement .ai/requirements/REQ-201-bulk-delete-users.md --memory-brief .ai/context/MEMORY-BRIEF-REQ-201-bulk-delete-users.md --mode DEEP --output .ai/context/BLIND-SPOT-REQ-201-bulk-delete-users-blocked.md`
- Input: underspecified bulk delete user records requirement.
- Expected: `VERDICT BLOCKED`.
- Actual: `VERDICT BLOCKED`.
- PASS/FAIL: PASS

## BS-005 - High Risk Handling

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-301-fulfillment-api-v2.md`
- Input: external fulfillment API DEEP report.
- Expected: HIGH open risks produce warnings, not hidden success.
- Actual: `WARN HIGH blind spots remain OPEN: BS-001, BS-002, BS-003`; `SUMMARY pass=6 warn=1 fail=0`.
- PASS/FAIL: PASS

## BS-006 - Assumption Ledger

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md`
- Input: date-filter report.
- Expected: assumption ledger contains impact-if-false.
- Actual: `PASS assumption ASM-001`.
- PASS/FAIL: PASS

## BS-007 - Unknown Ledger

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md`
- Input: date-filter report.
- Expected: unknown ledger validates.
- Actual: `PASS unknown UNK-001`.
- PASS/FAIL: PASS

## BS-008 - Memory-Assisted Detection

- Command: `python3 ai-project-template/scripts/run-blind-spot-pass.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --requirement .ai/requirements/REQ-401-account-statement-lookup.md --memory-brief .ai/context/MEMORY-BRIEF-REQ-401-account-statement-lookup.md --mode DEEP --output .ai/context/BLIND-SPOT-REQ-401-account-statement-lookup.md`
- Input: statement lookup requirement plus memory containing `KNOW-OWN-001`.
- Expected: authorization/ownership risk surfaces and references `KNOW-OWN-001`.
- Actual: `VERDICT BLOCKED`; validator `SUMMARY pass=3 warn=0 fail=0`.
- PASS/FAIL: PASS

## BS-009 - Memory Conflict Handling

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --query "account statement lookup private transaction details ownership authorization" --tags account ownership authorization statements --output .ai/context/MEMORY-BRIEF-REQ-401-account-statement-lookup-conflict.md`
- Input: conflicting active ownership records `KNOW-OWN-001` and `KNOW-OWN-002`.
- Expected: Memory Brief reports `MEMORY CONFLICT`; Blind Spot Pass blocks.
- Actual: Memory Brief reports `MEMORY CONFLICT`; `BLIND-SPOT-REQ-401-account-statement-conflict.md` validates with `SUMMARY pass=4 warn=0 fail=0`.
- PASS/FAIL: PASS

## BS-010 - Blind Spot To Plan Traceability

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md --plan .ai/plans/PLAN-REQ-101-date-filter.md`
- Input: date-filter report and plan.
- Expected: HIGH/MEDIUM resolved blind spots are referenced in the plan.
- Actual: `PASS plan traceability checked .ai/plans/PLAN-REQ-101-date-filter.md`.
- PASS/FAIL: PASS

## BS-011 - Blind Spot To Verification Traceability

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md --verification .ai/verification/VERIFY-REQ-101-date-filter.md`
- Input: date-filter report and verification report.
- Expected: relevant BS IDs are checked in verification.
- Actual: `PASS verification traceability checked .ai/verification/VERIFY-REQ-101-date-filter.md`.
- PASS/FAIL: PASS

## BS-012 - STANDARD Mode Demonstration

- Command: `python3 ai-project-template/scripts/run-blind-spot-pass.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --requirement .ai/requirements/REQ-101-date-filter.md --memory-brief .ai/context/MEMORY-BRIEF-REQ-101-date-filter.md --mode STANDARD --output .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md`
- Input: date-filter requirement.
- Expected: STANDARD report includes date bounds, reversed range, parsing/testability, assumptions, and unknowns.
- Actual: `VERDICT READY_FOR_PLAN`; mode `STANDARD`; unit tests pass.
- PASS/FAIL: PASS

## BS-013 - DEEP Mode Demonstration

- Command: `python3 ai-project-template/scripts/run-blind-spot-pass.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --requirement .ai/requirements/REQ-201-bulk-delete-users.md --memory-brief .ai/context/MEMORY-BRIEF-REQ-201-bulk-delete-users.md --mode DEEP --output .ai/context/BLIND-SPOT-REQ-201-bulk-delete-users-blocked.md`
- Input: high-risk bulk delete requirement.
- Expected: DEEP report finds authorization, data loss, audit, partial failure, rollback/compliance issues and blocks.
- Actual: `VERDICT BLOCKED`; resolved requirement later produced `VERDICT READY_FOR_PLAN`.
- PASS/FAIL: PASS

## BS-014 - External Integration Demonstration

- Command: `python3 ai-project-template/scripts/run-blind-spot-pass.py --project-root ai-project-template/tests/fixtures/phase3b-blindspot-demo --project phase3b-blindspot-demo --requirement .ai/requirements/REQ-301-fulfillment-api.md --memory-brief .ai/context/MEMORY-BRIEF-REQ-301-fulfillment-api.md --mode DEEP --output .ai/context/BLIND-SPOT-REQ-301-fulfillment-api-v2.md`
- Input: external fulfillment API requirement.
- Expected: identifies timeout, retry, idempotency, auth/secret, rate limit/outage, audit/reconciliation style risks; no implementation.
- Actual: HIGH risks surfaced and validator reports `SUMMARY pass=6 warn=1 fail=0`.
- PASS/FAIL: PASS

## BS-015 - Cross-Project Isolation

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3b-isolation-project --project phase3b-isolation-project --query "account statement lookup private transaction details ownership authorization" --tags account ownership authorization statements`
- Input: second disposable project with no ownership knowledge.
- Expected: no Project A knowledge IDs are retrieved.
- Actual: `Relevant Knowledge - None found`; isolation Blind Spot report validates with `SUMMARY pass=3 warn=0 fail=0`.
- PASS/FAIL: PASS

## Supporting Commands

```bash
PYTHONPYCACHEPREFIX=/tmp/codex-pycache-phase3b python3 -m py_compile ai-project-template/scripts/memorylib.py ai-project-template/scripts/run_blind_spot_constants.py ai-project-template/scripts/run-blind-spot-pass.py ai-project-template/scripts/validate-blind-spots.py ai-project-template/scripts/retrieve-memory.py ai-project-template/scripts/validate-memory.py
bash -n ai-project-template/scripts/init-ai-project.sh
python3 -m unittest discover -s ai-project-template/tests/fixtures/phase3b-blindspot-demo -p 'test_*.py' -v
```

Supporting results:

- Python scripts compile with redirected bytecode cache.
- Initializer shell syntax passes.
- Date-filter fixture tests pass: `Ran 4 tests in 0.000s`, `OK`.
