# Role Contract: PLANNER

- Role Name: PLANNER
- Purpose: Create the implementation plan after Gate A0 passes.
- Required Inputs: requirement, requirement analysis, Memory Brief, Blind Spot Report, Skill Selection.
- Allowed Inputs: repository context, tests, architecture docs.
- Required Outputs: IMPLEMENTATION-PLAN artifact.
- Forbidden Actions: implement code; ignore HIGH/MEDIUM blind spots; silently change scope.
- Exit Criteria: plan maps risks, constraints, tests, rollback, and blind-spot traceability.
- Failure Conditions: unresolved CRITICAL risk remains; plan lacks required tests or rollback.
- Next Role: IMPLEMENTER after Gate A passes.
