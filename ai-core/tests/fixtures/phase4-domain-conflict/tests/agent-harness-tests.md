# Phase 3C Agent Harness Tests

Tested: 2026-08-15

Fixture root: `ai-project-template/tests/fixtures/phase3c-standard-run`

## AGENT-001 - Role contract validation

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template --check-contracts --check-templates`
- Input: Template role contracts and artifact templates.
- Expected: All role contracts exist and include forbidden actions.
- Actual: `SUMMARY pass=20 warn=0 fail=0`
- Result: PASS

## AGENT-002 - Artifact contract validation

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template --check-contracts --check-templates`
- Input: `.ai/templates/*`.
- Expected: Required artifact templates exist.
- Actual: `SUMMARY pass=20 warn=0 fail=0`
- Result: PASS

## AGENT-003 - Sequence enforcement

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-501 --expect-status COMPLETED --expect-profile STANDARD --require-gate D=PASSED --require-artifact REQUIREMENT_ANALYST --require-artifact MEMORY_RETRIEVER --require-artifact BLIND_SPOT_REVIEWER --require-artifact SKILL_SELECTOR --require-artifact PLANNER --require-artifact IMPLEMENTER --require-artifact TESTER --require-artifact REVIEWER --require-artifact VERIFIER --require-artifact MEMORY_CURATOR --require-artifact HANDOFF_WRITER --traceability .ai/runs/RUN-REQ-501-traceability.md`
- Command: `python3 ai-project-template/scripts/run-agent-workflow.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --resume RUN-REQ-508 --complete-role SKILL_SELECTOR`
- Input: Complete standard run `RUN-REQ-501` and negative-control run `RUN-REQ-508`.
- Expected: Required artifacts exist, dependency ordering passes, and skill selection cannot complete before Gate A0.
- Actual: Complete-run validation returned `SUMMARY pass=17 warn=0 fail=0`; negative-control command returned `FAIL Gate A0 must pass before skill selection/planning can complete`.
- Result: PASS

## AGENT-004 - Gate A0 enforcement

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-504 --expect-status AWAITING_HUMAN --expect-profile DEEP --require-gate A0=BLOCKED --require-event HUMAN_APPROVAL_REQUIRED --require-artifact BLIND_SPOT_REVIEWER`
- Input: Critical blocker requirement `REQ-504`.
- Expected: Gate A0 blocked and human approval required.
- Actual: `SUMMARY pass=7 warn=0 fail=0`
- Result: PASS

## AGENT-005 - Gate A enforcement

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-501 --require-gate A=PASSED`
- Input: Complete standard run `RUN-REQ-501`.
- Expected: Gate A passed before implementation evidence.
- Actual: `SUMMARY pass=3 warn=0 fail=0`
- Result: PASS

## AGENT-006 - Tester loopback

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-502 --require-loopback TESTER:IMPLEMENTER --require-event LOOPBACK`
- Input: Amount range filtering run with failing first test evidence.
- Expected: Tester loops back to Implementer.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-007 - Reviewer loopback

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-503 --require-loopback REVIEWER:IMPLEMENTER --require-event LOOPBACK`
- Input: Reviewer rejection run.
- Expected: Reviewer loops back to Implementer.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-008 - Retry limit

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-507 --expect-status BLOCKED --expect-profile STANDARD --require-event ROLE_FAILED`
- Input: Retry-limit run with `--max-role-retries 0`.
- Expected: Run blocks instead of looping forever.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-009 - Human approval pause

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-504 --expect-status AWAITING_HUMAN --expect-profile DEEP --require-gate A0=BLOCKED --require-event HUMAN_APPROVAL_REQUIRED --require-artifact BLIND_SPOT_REVIEWER`
- Input: Support-agent access to all financial transactions.
- Expected: Workflow pauses and does not simulate approval.
- Actual: `SUMMARY pass=7 warn=0 fail=0`
- Result: PASS

## AGENT-010 - Artifact revisioning

- Command: `find ai-project-template/tests/fixtures/phase3c-standard-run/.ai -name '*REQ-502-v*.md' -o -name '*REQ-503-v*.md'`
- Input: Tester and reviewer loopback runs.
- Expected: `v1` and `v2` artifacts are preserved.
- Actual: Versioned `IMPLEMENTATION-SUMMARY`, `TEST-EVIDENCE`, and `REVIEW` artifacts exist for loopback runs.
- Result: PASS

## AGENT-011 - Traceability matrix

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-501 --traceability .ai/runs/RUN-REQ-501-traceability.md`
- Input: `RUN-REQ-501-traceability.md`.
- Expected: Matrix includes acceptance criterion, blind spot, plan step, implementation, test, review, and verification columns.
- Actual: `SUMMARY pass=3 warn=0 fail=0`
- Result: PASS

## AGENT-012 - Run resume

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-505 --expect-status RUNNING --expect-profile STANDARD --expect-current-role IMPLEMENTER --require-event RUN_RESUMED --require-artifact PLANNER`
- Input: Paused resume demo run.
- Expected: Resume reconstructs current role from run state and artifacts.
- Actual: `SUMMARY pass=7 warn=0 fail=0`
- Result: PASS

## AGENT-013 - Run cancellation

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-506 --expect-status CANCELLED --expect-profile LEAN --require-event RUN_CANCELLED`
- Input: Cancelled disposable run.
- Expected: Run status is `CANCELLED` and event log preserves cancellation.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-014 - Cross-project isolation

- Command: `python3 ai-project-template/tests/fixtures/phase3c-isolation-b/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-isolation-b --run-id RUN-REQ-601 --expect-status RUNNING --expect-profile LEAN --expect-current-role REQUIREMENT_ANALYST --expect-no-cross-project PROJECT_A_ONLY`
- Input: Two initialized disposable projects.
- Expected: Project B does not contain Project A marker memory.
- Actual: `SUMMARY pass=5 warn=0 fail=0`
- Result: PASS

## AGENT-015 - LEAN profile

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-506 --expect-status CANCELLED --expect-profile LEAN --require-event RUN_CANCELLED`
- Input: Cancellation demo initialized with `--profile LEAN`.
- Expected: Run state records `LEAN`.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-016 - STANDARD profile

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-501 --expect-status COMPLETED --expect-profile STANDARD`
- Input: Complete category filter demo.
- Expected: Run state records `STANDARD`.
- Actual: Profile assertion passed in complete-run validation.
- Result: PASS

## AGENT-017 - DEEP profile

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run --run-id RUN-REQ-504 --expect-status AWAITING_HUMAN --expect-profile DEEP`
- Input: Critical blocker demo.
- Expected: Run state records `DEEP`.
- Actual: Profile assertion passed in critical-blocker validation.
- Result: PASS

## AGENT-018 - Role contamination prevention

- Command: `rg -n "silently|rewrite another role|Forbidden Actions|revision" ai-project-template/.ai/agents ai-project-template/docs/agent-harness.md ai-project-template/docs/ai-project-workflow.md`
- Input: Role contracts and harness docs.
- Expected: Contracts forbid silent rewrite and require revision/loopback.
- Actual: Matches found in role contracts and `docs/agent-harness.md`.
- Result: PASS

## AGENT-019 - Memory Curator evidence enforcement

- Command: `python3 ai-project-template/scripts/validate-memory.py --project-root ai-project-template/tests/fixtures/phase3c-standard-run`
- Input: Memory created during `RUN-REQ-501`.
- Expected: Knowledge entries validate and include source references.
- Actual: `SUMMARY pass=4 warn=0 fail=0`
- Result: PASS

## AGENT-020 - Complete run verification

- Command: `python3 -m unittest discover -s ai-project-template/tests/fixtures/phase3c-standard-run -p 'test_*.py' -v`
- Input: Disposable transaction filtering implementation and tests.
- Expected: Fixture behavior tests pass.
- Actual: `Ran 9 tests in 0.001s` and `OK`.
- Result: PASS
