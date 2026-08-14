# Document Intelligence

Document Intelligence converts source documents into structured, traceable, reviewable project intelligence.

It does not treat extraction as truth. Parsing produces source text and locations; analysis proposes intelligence; review approves, corrects, rejects, or flags conflicts; promotion creates requirements, knowledge, context, decisions, or handoffs only after review.

## Pipeline

```text
SOURCE DOCUMENT
-> INGEST
-> PARSE / EXTRACT
-> NORMALIZE
-> CLASSIFY
-> STRUCTURE
-> TRACE TO SOURCE
-> REVIEW
-> APPROVE / REJECT / CORRECT
-> PROMOTE
-> REQUIREMENT / MEMORY / DECISION / CONTEXT
```

## Workspace

```text
.ai/documents/
  inbox/       managed copies of original source documents
  extracted/   parsed sections and proposed intelligence JSON
  reviews/     intelligence reports and review decisions
  manifests/   source metadata, hash, parser, authority, status
  processed/   promotion outputs and change-impact records
  rejected/    rejected document records when needed
  runs/        resumable document processing state
  index.md     operational dashboard
```

Original source documents are not modified.

## Supported Source Types

- TXT
- MD
- HTML
- JSON
- CSV
- DOCX through standard OOXML text extraction
- PDF only when a local text parser is available; scanned or empty-text PDFs are `OCR_REQUIRED`

No OCR engine or vector database is included in this phase.

## Authority Levels

- AUTHORITATIVE: signed or approved source that can support VERIFIED memory after review.
- APPROVED: approved technical/product source that normally supports SUPPORTED or VERIFIED only when clear.
- WORKING_DRAFT: meeting notes or draft specs; normally SUPPORTED or UNVERIFIED.
- REFERENCE: external or supporting source.
- UNVERIFIED: copied or untrusted text.

Authority influences promotion confidence but does not replace review.

## Extracted Intelligence Types

REQUIREMENT, BUSINESS_RULE, PROJECT_FACT, CONSTRAINT, GLOSSARY, API_CONTRACT, DATA_RULE, SECURITY_RULE, PROCESS_STEP, ACCEPTANCE_CRITERION, DEPENDENCY, ASSUMPTION, UNKNOWN, RISK, DECISION_CANDIDATE, ACTION_ITEM, CONTACT_OR_ROLE, DATE_OR_DEADLINE.

## Extraction Confidence

- HIGH: explicit statement in source.
- MEDIUM: reasonable interpretation requiring review.
- LOW: ambiguous or incomplete extraction.

LOW items require review before promotion.

## Promotion Rules

- Unreviewed items cannot be promoted.
- ASSUMPTION never becomes VERIFIED without later evidence.
- UNKNOWN remains unresolved until answered.
- DECISION_CANDIDATE does not become ACCEPTED automatically.
- Sensitive content warnings block promotion.
- Document-memory conflicts are surfaced as `DOCUMENT_MEMORY_CONFLICT` and not resolved silently.
- Superseded documents and prior promoted records are preserved.

## Workflow Entry Paths

### Path A - Structured Requirement

```text
REQUIREMENT
-> REQUIREMENT_ANALYST
-> MEMORY_RETRIEVER
-> BLIND_SPOT_REVIEWER
-> ...
```

### Path B - Document Input

```text
DOCUMENT
-> INGEST
-> PARSE
-> DOCUMENT_ANALYST
-> DOCUMENT_REVIEWER
-> APPROVED PROMOTION
-> REQUIREMENT_ANALYST
-> MEMORY_RETRIEVER
-> BLIND_SPOT_REVIEWER
-> ...
```

Document roles may be skipped for direct structured requirements.
