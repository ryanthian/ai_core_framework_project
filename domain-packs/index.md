# Domain Pack Registry

| Pack ID | Name | Version | Status | Scope | Tags | Dependencies | Last Validated |
|---|---|---|---|---|---|---|---|
| access-control | Access Control | 1.0.0 | ACTIVE | reusable | identity, authorization, ownership, audit | [] | 2026-08-15 |
| external-api | External API | 1.0.0 | ACTIVE | reusable | api, timeout, retry, idempotency, reconciliation | [] | 2026-08-15 |
| data-change | Data Change | 1.0.0 | ACTIVE | reusable | data, migration, rollback, audit | [] | 2026-08-15 |
| financial-calculation | Financial Calculation | 1.0.0 | ACTIVE | reusable | currency, rounding, precision, reconciliation | [] | 2026-08-15 |
| billing | Billing | 1.0.0 | ACTIVE | reusable | billing, payment, adjustment, arrears, reconciliation | [financial-calculation, access-control] | 2026-08-15 |
| test-domain-conflict | Test Domain Conflict | 1.0.0 | EXPERIMENTAL | test | test, delete, history | [] | 2026-08-15 |
