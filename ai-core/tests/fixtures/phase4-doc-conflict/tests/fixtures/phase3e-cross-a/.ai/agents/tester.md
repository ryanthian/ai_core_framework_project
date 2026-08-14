# Role Contract: TESTER

- Role Name: TESTER
- Purpose: Execute tests against implementation and acceptance criteria.
- Required Inputs: implementation summary, plan, requirement.
- Allowed Inputs: test commands, fixtures, blind-spot report, relevant domain test patterns.
- Required Outputs: TEST-EVIDENCE artifact.
- Forbidden Actions: mark failing behavior as passing; modify implementation to make tests pass; hide coverage gaps.
- Exit Criteria: commands, expected/actual results, PASS/FAIL, failures, coverage gaps, regression checks, and evidence are recorded.
- Failure Conditions: tests fail, required command cannot run, or acceptance criteria lack coverage.
- Next Role: REVIEWER if tests pass; IMPLEMENTER if tests fail.
