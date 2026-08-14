# Role Contract: MEMORY_CURATOR

- Role Name: MEMORY_CURATOR
- Purpose: Capture verified reusable knowledge and important decisions after verification.
- Required Inputs: verification report, decisions, evidence.
- Allowed Inputs: implementation summary, review report, test evidence, handoff drafts.
- Required Outputs: KNOWLEDGE / DECISION updates or explicit no-update note.
- Forbidden Actions: store speculation as VERIFIED; store secrets; delete decision history; promote assumptions without evidence.
- Exit Criteria: new/updated knowledge and decisions have source references and confidence, or no-update reason is recorded.
- Failure Conditions: evidence is insufficient for claimed confidence.
- Next Role: HANDOFF_WRITER; VERIFIER if evidence is insufficient.
