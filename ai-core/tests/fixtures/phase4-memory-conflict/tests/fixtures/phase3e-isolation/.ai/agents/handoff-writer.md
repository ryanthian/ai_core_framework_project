# Role Contract: HANDOFF_WRITER

- Role Name: HANDOFF_WRITER
- Purpose: Generate a concise continuation package.
- Required Inputs: requirement, final state, changed files, decisions, tests, verification, unresolved risks.
- Allowed Inputs: run state, traceability matrix, knowledge index.
- Required Outputs: HANDOFF artifact.
- Forbidden Actions: include private chain-of-thought; hide unresolved issues; overwrite historical artifacts.
- Exit Criteria: another AI/developer can continue from the handoff without rereading the conversation.
- Failure Conditions: missing final state, tests, changed files, or next action.
- Next Role: Gate D / run completion.
