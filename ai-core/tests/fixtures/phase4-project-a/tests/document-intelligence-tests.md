# Phase 3D Document Intelligence Tests

Tested: 2026-08-15

Primary fixture: `ai-project-template/tests/fixtures/phase3d-doc-intel`

## DOC-001 - Manifest validation

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001`
- Input: `DOC-001` manifest and managed source.
- Expected: Manifest fields and source hash pass.
- Actual: Manifest/source/extracted checks passed in `SUMMARY pass=9 warn=0 fail=0`.
- Result: PASS

## DOC-002 - Duplicate hash detection

- Command: `python3 ai-project-template/scripts/ingest-document.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --file ai-project-template/tests/fixtures/phase3d-doc-intel/source-docs/requirements-demo.md --title "Statement Export Requirements Duplicate" --authority AUTHORITATIVE`
- Input: Same file as `DOC-001`.
- Expected: Duplicate detected and no new document created.
- Actual: `DUPLICATE document_id=DOC-001 source_hash=3c71a22710a4536d0006067bc0fc40ad2ce8526f32e5b7e1de09a53f58f02212`
- Result: PASS

## DOC-003 - TXT/MD ingestion

- Command: `python3 ai-project-template/scripts/ingest-document.py ... requirements-demo.md` and `python3 ai-project-template/scripts/ingest-document.py ... sensitive-note.txt`
- Input: Markdown requirements and TXT sensitive note.
- Expected: MD and TXT manifests created.
- Actual: `INGESTED DOC-001 MD ...` and `INGESTED DOC-006 TXT ...`
- Result: PASS

## DOC-004 - Structured extraction

- Command: `python3 ai-project-template/scripts/extract-document.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001`
- Input: `DOC-001`.
- Expected: Parsed sections written to `.ai/documents/extracted/DOC-001.json`.
- Actual: `EXTRACTED DOC-001 status=PARSED sections=1`
- Result: PASS

## DOC-005 - Source traceability

- Command: `python3 ai-project-template/scripts/search-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --query "account owner"`
- Input: Extracted document items.
- Expected: Results include source locations.
- Actual: Results included locations such as `heading:Statement Export Requirements|lines:1-11|part:2`.
- Result: PASS

## DOC-006 - Authority enforcement

- Command: `python3 ai-project-template/scripts/promote-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001`
- Input: AUTHORITATIVE requirements document.
- Expected: Reviewed clear items may promote; unknown remains blocked.
- Actual: `PROMOTED DOC-001 promoted=4 blocked=1 status=PARTIALLY_APPROVED`
- Result: PASS

## DOC-007 - Review workflow

- Command: `python3 ai-project-template/scripts/review-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-003 --approve-all-safe`
- Input: Meeting notes.
- Expected: Item-level review decisions written.
- Actual: `REVIEWED DOC-003 verdict=PARTIALLY_APPROVED decisions=4`
- Result: PASS

## DOC-008 - Promotion gating

- Command: `python3 ai-project-template/scripts/promote-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001`
- Input: Reviewed requirements document with one UNKNOWN.
- Expected: Reviewed promotable items promote; UNKNOWN does not become memory/requirement.
- Actual: `promoted=4 blocked=1`
- Result: PASS

## DOC-009 - Requirement candidate extraction

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001 --require-item-type REQUIREMENT`
- Input: `requirements-demo.md`.
- Expected: Requirement item exists.
- Actual: `PASS item type REQUIREMENT`
- Result: PASS

## DOC-010 - Business rule extraction

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001 --require-item-type BUSINESS_RULE`
- Input: `requirements-demo.md`.
- Expected: Business rule item exists.
- Actual: `PASS item type BUSINESS_RULE`
- Result: PASS

## DOC-011 - Unknown preservation

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-001 --require-item-type UNKNOWN`
- Input: `requirements-demo.md`.
- Expected: Unknown remains an UNKNOWN item.
- Actual: `PASS item type UNKNOWN`
- Result: PASS

## DOC-012 - API contract extraction

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-002 --require-item-type API_CONTRACT --require-item-type UNKNOWN`
- Input: `orders-api.md`.
- Expected: API contract and unknown timeout/idempotency items exist.
- Actual: `SUMMARY pass=6 warn=0 fail=0`
- Result: PASS

## DOC-013 - Meeting-note classification

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-003 --require-item-type DECISION_CANDIDATE --require-item-type ACTION_ITEM --require-item-type UNKNOWN`
- Input: `meeting-notes.md`.
- Expected: Agreed/proposed/unresolved content remains distinguishable.
- Actual: `SUMMARY pass=7 warn=0 fail=0`
- Result: PASS

## DOC-014 - Memory conflict detection

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-005 --require-conflict`
- Input: Authoritative v2 spec conflicting with `KNOW-701`.
- Expected: Conflict marker exists.
- Actual: `PASS conflict marker`
- Result: PASS

## DOC-015 - Document superseding

- Command: Python manifest inspection for `DOC-004` and `DOC-005`.
- Input: v1 and v2 statement access specifications.
- Expected: `DOC-004` preserved and marked `SUPERSEDED`; `DOC-005` supersedes `DOC-004`.
- Actual: `DOC-004 SUPERSEDED superseded_by= DOC-005`; `DOC-005 ... supersedes= DOC-004`.
- Result: PASS

## DOC-016 - Change impact

- Command: `test -f ai-project-template/tests/fixtures/phase3d-doc-intel/.ai/documents/processed/DOC-005-change-impact.json`
- Input: `DOC-005` conflict.
- Expected: Change impact artifact records affected knowledge.
- Actual: Artifact contains `type: DOCUMENT_CHANGE_IMPACT` and `affected_knowledge: ["KNOW-701"]`.
- Result: PASS

## DOC-017 - Blind Spot integration

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3d-doc-intel --report .ai/context/BLIND-SPOT-DOC-002-v2.md`
- Input: API document intelligence report.
- Expected: Timeout and idempotency unknowns appear as blind spots.
- Actual: `SUMMARY pass=5 warn=1 fail=0`; warning is expected because HIGH blind spots remain OPEN.
- Result: PASS

## DOC-018 - Agent Harness integration

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3d-doc-intel --run-id RUN-DOC --expect-status RUNNING --expect-profile DOCUMENT_STANDARD --expect-current-role REQUIREMENT_ANALYST --require-artifact DOCUMENT_ANALYST --require-artifact DOCUMENT_REVIEWER`
- Input: Document-entry agent run.
- Expected: Document Analyst and Reviewer complete before Requirement Analyst.
- Actual: `SUMMARY pass=7 warn=0 fail=0`
- Result: PASS

## DOC-019 - Resume

- Command: `python3 ai-project-template/scripts/document-run.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-006 --resume`
- Input: Document run stopped after extraction.
- Expected: Resume reports current stage without redoing extraction.
- Actual: `DOCUMENT_RUN DOC-006 status=RUNNING stage=EXTRACTED parser=PARSED review=NOT_STARTED promotion=NOT_STARTED`
- Result: PASS

## DOC-020 - Cancellation

- Command: `python3 ai-project-template/scripts/document-run.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-007 --cancel --reason "Phase 3D cancellation test"`
- Input: Cancellation demo document.
- Expected: Run and index show cancellation.
- Actual: `DOCUMENT_RUN DOC-007 status=CANCELLED ...`; index row shows `DOC-007 ... CANCELLED`.
- Result: PASS

## DOC-021 - Cross-project isolation

- Command: `python3 ai-project-template/scripts/search-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-isolation-b --query PROJECT_A_DOC_ONLY`
- Input: Project A document intelligence marker.
- Expected: Project B returns no Project A results.
- Actual: `RESULTS 0`
- Result: PASS

## DOC-022 - Sensitive content warning

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --document-id DOC-006 --require-warning SENSITIVE_CONTENT_WARNING --require-reviewed`
- Input: TXT note containing an API-key-like value.
- Expected: Sensitive warning is present and item is not approved.
- Actual: `SUMMARY pass=5 warn=0 fail=0`
- Result: PASS

## DOC-023 - Search/retrieval

- Command: `python3 ai-project-template/scripts/search-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --query "account owner"`
- Input: Extracted document intelligence.
- Expected: Keyword search returns matching structured items with source locations.
- Actual: `RESULTS 5`
- Result: PASS

## DOC-024 - Document index generation

- Command: `python3 ai-project-template/scripts/validate-document-intelligence.py --project ai-project-template/tests/fixtures/phase3d-doc-intel --require-index`
- Input: Document manifests and extracted items.
- Expected: `.ai/documents/index.md` exists and summarizes documents.
- Actual: `SUMMARY pass=24 warn=1 fail=0`; warning is expected for cancelled `DOC-007` having no extracted file.
- Result: PASS

## Notes

During testing, a parallel ingest attempt created a disposable `DOC-007` ID race. The conflicted fixture files were removed and the tests were rerun sequentially. Current limitation: the file-based ID allocator is intended for controlled sequential CLI use, not concurrent ingestion.

Repeated promotion also exposed duplicate candidate requirement creation. The duplicate fixture requirements were removed, and `promote-document-intelligence.py` now checks existing requirement bodies and blocks future repeats with `POSSIBLE_DUPLICATE_REQUIREMENT`.
