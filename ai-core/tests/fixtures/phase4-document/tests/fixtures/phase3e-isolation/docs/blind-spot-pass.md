# Blind Spot Pass

The Blind Spot Pass runs after memory retrieval and before implementation planning.

It is a structured reasoning step, not a keyword-only checker. Scripts can scaffold and validate reports, but Codex must reason over the requirement, memory brief, repository context, dependencies, relevant decisions, and relevant knowledge.

## Categories

- REQUIREMENT_GAP
- AMBIGUITY
- ASSUMPTION
- DEPENDENCY
- DATA_IMPACT
- API_IMPACT
- SECURITY
- PRIVACY
- AUTHORIZATION
- PERFORMANCE
- CONCURRENCY
- TRANSACTIONALITY
- ERROR_HANDLING
- EDGE_CASE
- BACKWARD_COMPATIBILITY
- MIGRATION
- ROLLBACK
- OBSERVABILITY
- OPERATIONS
- UI_UX
- ACCESSIBILITY
- TESTABILITY
- COMPLIANCE
- EXTERNAL_INTEGRATION
- UNKNOWN
- MEMORY_CONFLICT

`MEMORY_CONFLICT` is added because Phase 3A memory can contain contradictory active records; conflicts must be surfaced rather than silently resolved.

## Severity

- CRITICAL: implementation must not proceed until resolved.
- HIGH: material risk. Prefer resolution before implementation unless explicitly accepted.
- MEDIUM: should be addressed in the plan or tests.
- LOW: minor consideration; document but does not block work.

## Resolution Status

- OPEN
- RESOLVED
- ACCEPTED_RISK
- NOT_APPLICABLE
- DEFERRED

Critical blind spots cannot be automatically accepted as risk. A human or authoritative requirement must explicitly accept them.

## Analysis Modes

### QUICK

Use for low-risk changes such as copy changes, CSS spacing, labels, and non-functional documentation.

Approximate checks:

- requirement clarity
- acceptance criteria
- obvious edge cases
- rollback
- testability

### STANDARD

Default mode for normal product and engineering work.

Covers requirement clarity, users/authorization, data, API, security, error handling, UI/UX, performance, operations, rollback, and tests.

### DEEP

Use for security-sensitive, financial, billing, permissions, external APIs, data migration, bulk operations, enterprise integrations, high-impact workflows, deletion, personally sensitive data, and high uncertainty.

DEEP mode must aggressively examine authorization, privacy, data loss, transactionality, concurrency, audit, rollback, compliance, external failure, partial success, and operational support.

## Automatic Mode Recommendation

- Simple text/UI copy: QUICK
- CSS spacing or simple label: QUICK
- Normal CRUD/filter/UI feature: STANDARD
- Billing/payment: DEEP
- Authentication/authorization: DEEP
- External API integration: DEEP
- Bulk data change: DEEP
- Migration: DEEP
- Deletion: DEEP
- Financial calculations: DEEP
- Personally sensitive data: DEEP

Codex may recommend a higher level when uncertainty is high.

## Core Questions

### Requirement

- What exactly is requested?
- What is not specified?
- What does done mean?
- Are acceptance criteria measurable?
- Are there conflicting requirements?

### Users And Authorization

- Who can perform the action?
- Who cannot?
- Does ownership matter?
- Are tenant/project/user boundaries involved?
- Could data from one user be exposed to another?

### Data

- What records are created, updated, deleted, or derived?
- Does historical data behave differently?
- Is migration required?
- Could null, duplicate, stale, malformed, or missing data occur?

### Integration

- What external systems are involved?
- What happens on failure, timeout, retry, idempotency gap, partial success, or rate limiting?

### API

- Does the API contract change?
- Are existing consumers affected?
- Is versioning needed?
- Are errors stable and useful?

### Security

- Could this create authorization bypass, injection, data exposure, unsafe file handling, secret leakage, privilege escalation, or unsafe external execution?

### Transactionality

- Can partial failure leave inconsistent state?
- Is rollback possible?
- Are operations idempotent?
- Could concurrent requests conflict?

### UI/UX

- Loading state?
- Empty state?
- Error state?
- Permission denied?
- Partial success?
- Long-running action?
- Mobile?
- Accessibility?

### Performance

- Expected data volume?
- Pagination?
- N+1 queries?
- Large exports?
- Long-running jobs?
- Memory usage?

### Operations

- Logging?
- Audit trail?
- Metrics?
- Alerting?
- Support troubleshooting?
- Feature flag?
- Rollback?

### Testing

- Happy path?
- Boundary values?
- Invalid input?
- Permissions?
- Concurrency?
- Integration failure?
- Regression?
- Rollback?

## Gate A0: Ready To Plan

Must have:

- requirement identified
- relevant memory retrieved
- Blind Spot Pass completed
- no unresolved CRITICAL blind spots
- blocking unknowns identified
- assumptions recorded

If any CRITICAL blind spot remains OPEN, verdict must be BLOCKED.

## Traceability

The implementation plan must include:

- Blind Spot Report
- Resolved Blind Spots
- Accepted Risks
- Planning Constraints
- Security Considerations
- Data Considerations
- Operational Considerations
- Required Tests

Each HIGH/MEDIUM blind spot that affects implementation must map to an implementation step, test, decision, or explicitly documented accepted risk.

Verification must check each relevant BS ID as FIXED, TESTED, ACCEPTED_RISK, NOT_APPLICABLE, or UNRESOLVED.

