# Domain Packs

Domain packs are reusable, versioned knowledge modules independent from project memory.

Projects explicitly activate packs in `.ai/domain-packs.yaml`. No pack is active by default.

## Precedence

1. AUTHORITATIVE CURRENT PROJECT REQUIREMENT
2. PROJECT VERIFIED KNOWLEDGE
3. PROJECT ACCEPTED DECISION
4. APPROVED DOMAIN RULE
5. SUPPORTED PROJECT KNOWLEDGE
6. EXPERIMENTAL DOMAIN GUIDANCE
7. UNVERIFIED

Do not use ranking to hide real contradictions. Surface `DOMAIN_PROJECT_CONFLICT` or `DOMAIN_DOMAIN_CONFLICT`.

## Retrieval Discipline

Retrieve selectively by tags, type, keywords, requirement context, and risk category. Do not inject entire packs.

Prefer the smallest sufficient set of active packs.

## Upgrade Lifecycle

CHECK -> DIFF -> IMPACT ANALYSIS -> CONFLICT CHECK -> UPDATE ACTIVATION -> REVALIDATE MEMORY/BLIND SPOTS -> ACCEPT / ROLLBACK

Projects are version-pinned and never float to latest automatically.

## Candidate Flow

PROJECT KNOWLEDGE -> DOMAIN CANDIDATE -> REVIEW -> DOMAIN PACK

Only reusable, source-backed, reviewed guidance should enter a domain pack. Project-specific facts stay in project memory.
