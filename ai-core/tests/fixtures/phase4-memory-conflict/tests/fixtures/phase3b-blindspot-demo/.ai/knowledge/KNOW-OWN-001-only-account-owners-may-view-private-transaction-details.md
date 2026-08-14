---
id: KNOW-OWN-001
title: Only account owners may view private transaction details
class: BUSINESS_RULE
project: phase3b-blindspot-demo
scope: PROJECT
confidence: VERIFIED
status: ACTIVE
created: 2026-08-15
updated: 2026-08-15
source_type: REQUIREMENT
source_ref: .ai/requirements/REQ-401-account-statement-lookup.md
tags: [account, ownership, authorization, statements]
related_requirements: []
related_decisions: []
---
# Knowledge

Only account owners may view private transaction details.

# Evidence

REQ-401 requires statement details only when access is allowed; this fixture records owner_id with transactions.

# Applicability

Applies to account statement lookup and private transaction detail access in this fixture.

# Exceptions

None known.

# Operational Impact

Statement lookup must include an ownership check before returning private transaction details.

# Revalidation Trigger

Revalidate if account sharing, admin impersonation, or statement access rules change.
