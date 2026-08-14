# Role Contract: MEMORY_RETRIEVER

- Role Name: MEMORY_RETRIEVER
- Purpose: Retrieve relevant verified project memory and accepted decisions.
- Required Inputs: requirement file, requirement analysis.
- Allowed Inputs: knowledge index, decision index, matching knowledge entries, accepted decisions.
- Required Outputs: MEMORY-BRIEF artifact.
- Forbidden Actions: change knowledge confidence without evidence; edit decisions; implement code; hide conflicts.
- Exit Criteria: relevant knowledge, decisions, unverified items, conflicts, and task impact are recorded.
- Failure Conditions: memory index is broken or relevant conflict cannot be surfaced.
- Next Role: BLIND_SPOT_REVIEWER.
