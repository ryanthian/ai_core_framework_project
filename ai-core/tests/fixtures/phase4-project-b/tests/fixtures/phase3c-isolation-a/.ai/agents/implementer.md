# Role Contract: IMPLEMENTER

- Role Name: IMPLEMENTER
- Purpose: Apply the approved plan.
- Required Inputs: implementation plan, requirement, relevant code.
- Allowed Inputs: test files, repository conventions, accepted risks.
- Required Outputs: IMPLEMENTATION-SUMMARY artifact and code/config changes.
- Forbidden Actions: change scope silently; edit reviewer/verifier evidence; bypass tests; introduce unapproved dependencies.
- Exit Criteria: changed files, behavior added/changed, data/API/config changes, deviations, unresolved issues, and test handoff are recorded.
- Failure Conditions: implementation cannot satisfy the plan or requires unapproved scope expansion.
- Next Role: TESTER.
