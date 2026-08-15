# Phase 5 Regression Tests

## REG-001

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 codex-skills/tests/validate-skills.py codex-skills`
Input: Phase 1 skills
Expected: skill validator exits 0
Actual: PASS codex-skills/custom/codex-engineering-workflow/SKILL.md name=codex-engineering-workflow
PASS codex-skills/custom/codex-skill-selector/SKILL.md name=codex-skill-selector
PASS codex-skills/third-party/anthropics-frontend-design/SKILL.md name=frontend-design
PASS codex-skills/third-party/guizang-ppt-skill/SKILL.md name=guizang-ppt-skill
PASS codex-skills/third-party/humanizer-zh-tw/SKILL.md name=humanizer-zh-tw
PASS codex-skills/tiktok-product-video-automation/SKILL.md name=tiktok-product-video-automation
SUMMARY skills=6 pass=6 warn=0 fail=0

Result: PASS

## REG-002

Command: `inspect workflow docs`
Input: Phase 2 workflow
Expected: workflow docs exist and include memory retrieval
Actual: ai-project-template/docs/ai-project-workflow.md
AGENTS.md
Result: PASS

## REG-003

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/validate-memory.py --project-root tests/fixtures/phase3a-memory-demo`
Input: Phase 3A memory fixture
Expected: memory validator exits 0
Actual: PASS knowledge KNOW-001 KNOW-001-phase-3a-memory-demo-is-disposable.md
PASS knowledge KNOW-002 KNOW-002-transaction-export-columns-follow-fixed-business-order.md
PASS knowledge KNOW-003 KNOW-003-transaction-export-utilities-live-in-transactions-py.md
PASS knowledge KNOW-004 KNOW-004-transaction-row-fields-are-id-date-description-amount.md
PASS knowledge KNOW-005 KNOW-005-manual-csv-joining-can-break-comma-quoting.md
PASS knowledge KNOW-006 KNOW-006-table-exports-share-field-normalization-before-serialization.md
PASS knowledge KNOW-007 KNOW-007-transaction-export-columns-are-alphabetical.md
PASS decision ADR-001 ADR-001-use-csv-dictwriter-for-csv-export.md
PASS decision ADR-002 ADR-002-export-columns-alphabetically.md
PASS decision ADR-003 ADR-003-use-business-defined-fixed-export-order.md
PASS decision ADR-004 ADR-004-reject-manual-csv-string-joining.md
PASS decision ADR-005 ADR-005-shar
Result: PASS

## REG-004

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/validate-blind-spots.py --project-root tests/fixtures/phase3b-blindspot-demo --report .ai/context/BLIND-SPOT-REQ-101-date-filter-ready.md`
Input: Phase 3B blind spot fixture
Expected: blind spot validator exits 0
Actual: PASS blind spot BS-001
PASS blind spot BS-002
PASS blind spot BS-003
PASS assumption ASM-001
PASS unknown UNK-001
SUMMARY pass=5 warn=0 fail=0

Result: PASS

## REG-005

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/validate-agent-run.py --project-root . --check-contracts --check-templates`
Input: Phase 3C agent harness fixture
Expected: agent validator exits 0
Actual: PASS role contract .ai/agents/document-analyst.md
PASS role contract .ai/agents/document-reviewer.md
PASS role contract .ai/agents/requirement-analyst.md
PASS role contract .ai/agents/memory-retriever.md
PASS role contract .ai/agents/blind-spot-reviewer.md
PASS role contract .ai/agents/skill-selector.md
PASS role contract .ai/agents/planner.md
PASS role contract .ai/agents/implementer.md
PASS role contract .ai/agents/tester.md
PASS role contract .ai/agents/reviewer.md
PASS role contract .ai/agents/verifier.md
PASS role contract .ai/agents/memory-curator.md
PASS role contract .ai/agents/handoff-writer.md
PASS artifact template .ai/templates/document-intelligence-report.md
PASS artifact template .ai/templates/document-review-report.md
PASS artifact template .ai/templates/document-manifest.json
PASS artifact template .ai/templates/domain-candidate.md
PASS artifact template .ai/templates/req
Result: PASS

## REG-006

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/validate-document-intelligence.py --project tests/fixtures/phase3d-doc-intel --document-id DOC-001 --require-item-type REQUIREMENT --require-item-type BUSINESS_RULE --require-reviewed --require-promoted --require-index`
Input: Phase 3D document fixture
Expected: document validator exits 0
Actual: PASS manifest DOC-001
PASS source hash DOC-001
PASS extracted DOC-001 items=5
PASS item type REQUIREMENT
PASS item type BUSINESS_RULE
PASS review DOC-001
PASS promotion DOC-001
PASS document index
SUMMARY pass=8 warn=0 fail=0

Result: PASS

## REG-007

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 scripts/validate-domain-pack.py --project tests/fixtures/phase3e-access --check-activation`
Input: Phase 3E domain pack fixture
Expected: domain validator exits 0
Actual: PASS manifest access-control@1.0.0
PASS rule AC-RULE-001
PASS rule AC-BS-001
PASS manifest billing@1.0.0
PASS rule BILL-GLOSS-001
PASS rule BILL-RULE-001
PASS rule BILL-TEST-001
PASS rule BILL-DOC-001
PASS manifest data-change@1.0.0
PASS rule DATA-RULE-001
PASS manifest external-api@1.0.0
PASS rule API-RULE-001
PASS rule API-TEST-001
PASS version manifest external-api@1.1.0
PASS version rule API-RULE-001@1.1.0
PASS version rule API-TEST-001@1.1.0
PASS version rule API-RULE-002@1.1.0
PASS manifest financial-calculation@1.0.0
PASS rule FIN-RULE-001
PASS manifest test-domain-conflict@1.0.0
PASS rule TDC-RULE-001
PASS activation access-control@1.0.0
PASS domain registry
SUMMARY pass=23 warn=0 fail=0

Result: PASS

## REG-008

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 ai-core/tests/run-core-tests.py`
Input: Phase 4 AI-Core runtime
Expected: core integration tests pass
Actual: SUMMARY pass=30 fail=0
WROTE /Users/ryanthian/Documents/Codex_mac/ai_core_framework_project/ai-core/tests/core-integration-tests.md

Result: PASS
