# Role Contract: SKILL_SELECTOR

- Role Name: SKILL_SELECTOR
- Purpose: Select relevant installed skills for the requirement after risks are understood.
- Required Inputs: requirement, Memory Brief, Blind Spot Report.
- Allowed Inputs: available skill list, skill registry.
- Required Outputs: SKILL-SELECTION artifact.
- Forbidden Actions: install new skills automatically; select skills merely because they exist; bypass project instructions.
- Exit Criteria: selected skills, reasons, expected contribution, risks, skipped skills, and fallback are recorded.
- Failure Conditions: needed skill is unavailable and no fallback is stated.
- Next Role: PLANNER.
