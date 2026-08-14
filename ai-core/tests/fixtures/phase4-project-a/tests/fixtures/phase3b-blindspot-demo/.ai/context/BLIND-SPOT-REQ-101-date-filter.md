---
id: BSP-REQ-101
requirement: .ai/requirements/REQ-101-date-filter.md
project: phase3b-blindspot-demo
created: 2026-08-15
memory_brief: .ai/context/MEMORY-BRIEF-REQ-101-date-filter.md
mode: STANDARD
status: COMPLETE
overall_risk: CRITICAL
---

# Requirement Understanding

# Requirement

# Relevant Memory

- KNOW-101 - Transaction rows contain ISO date strings (DATA_MODEL, VERIFIED, PROJECT)

# Blind Spots

## BS-001

- Category: MEMORY_CONFLICT
- Severity: CRITICAL
- Status: OPEN
- Finding: Relevant memory contains conflicting active guidance.
- Why It Matters: Planning from contradictory memory can encode the wrong rule.
- Evidence: Memory Brief contains MEMORY CONFLICT.
- Assumption: 
- Question: Which source is authoritative?
- Recommended Resolution: Resolve or deprecate the weaker memory record before planning.
- Impact if Ignored: Implementation may follow the wrong project rule.
- Related Knowledge: 
- Related Decision: 
- Accepted Risk Justification: 
- Plan Trace: 
- Verification Trace: 

## BS-002

- Category: AMBIGUITY
- Severity: MEDIUM
- Status: RESOLVED
- Finding: Date bounds must be explicit.
- Why It Matters: Inclusive/exclusive bounds change visible records.
- Evidence: Requirement or plan must define bounds.
- Assumption: 
- Question: 
- Recommended Resolution: Use inclusive start and inclusive end dates.
- Impact if Ignored: Boundary-day records may disappear.
- Related Knowledge: 
- Related Decision: 
- Accepted Risk Justification: 
- Plan Trace: PLAN-BS-001
- Verification Trace: VERIFY-BS-001

## BS-003

- Category: EDGE_CASE
- Severity: MEDIUM
- Status: RESOLVED
- Finding: Start date after end date needs defined behavior.
- Why It Matters: Invalid ranges otherwise produce confusing empty results.
- Evidence: Date range filtering requirement.
- Assumption: 
- Question: 
- Recommended Resolution: Return an empty result for start > end in the fixture.
- Impact if Ignored: Users may misread invalid filters.
- Related Knowledge: 
- Related Decision: 
- Accepted Risk Justification: 
- Plan Trace: PLAN-BS-002
- Verification Trace: VERIFY-BS-002

## BS-004

- Category: TESTABILITY
- Severity: MEDIUM
- Status: RESOLVED
- Finding: Date parsing needs deterministic tests.
- Why It Matters: String comparison can be wrong for malformed dates.
- Evidence: Fixture uses ISO date strings.
- Assumption: 
- Question: 
- Recommended Resolution: Test inclusive bounds, empty range, start > end, and malformed dates.
- Impact if Ignored: Regression risk around boundary values.
- Related Knowledge: 
- Related Decision: 
- Accepted Risk Justification: 
- Plan Trace: PLAN-BS-003
- Verification Trace: VERIFY-BS-003

# Assumption Ledger

## ASM-001

- Statement: Transaction dates use ISO YYYY-MM-DD strings.
- Why assumed: Existing fixture rows use ISO-like dates.
- Evidence: transactions.py and tests use 2026-08-15 style dates.
- Confidence: SUPPORTED
- Impact if false: Parser behavior changes if timestamps or localized dates appear.
- Resolution owner/source: Requirement or schema owner
- Status: RESOLVED

# Unknowns Ledger

## UNK-001

- Statement: Timezone handling is not specified for date-only fixture rows.
- Why unknown: The fixture has dates, not datetimes.
- Impact: Future datetime filters may need timezone rules.
- Resolution owner/source: Future requirement
- Status: DEFERRED

# Open Questions

- Which source is authoritative?

# Blocking Issues

- Relevant memory contains conflicting active guidance.

# Accepted Risks

- None.

# Planning Constraints

- Use inclusive start and inclusive end dates.
- Return an empty result for start > end in the fixture.
- Test inclusive bounds, empty range, start > end, and malformed dates.

# Verdict

BLOCKED
