# Phase 5 CLI Tests

## CLI-001

Command: `pip install -e . && ai-core version`
Input: /Users/ryanthian/Documents/Codex_mac/ai_core_framework_project
Expected: entry point works
Actual: AI-Core 0.5.0

Framework Phase
5

Schema
2

Repository
ai_core_framework_project

Commit
a002a18
Result: PASS

## CLI-002

Command: `ai-core version --json`
Input: framework
Expected: version 0.5.0
Actual: {
  "framework_phase": "5",
  "git": {
    "branch": "main",
    "commit": "a002a18",
    "dirty": true,
    "repository": true
  },
  "repository": "ai_core_framework_project",
  "schema": "2",
  "version": "0.5.0"
}

Result: PASS

## CLI-003

Command: `ai-core --help`
Input: framework
Expected: help includes command groups
Actual: usage: ai-core [-h] [--project PROJECT] [--json] [--quiet] [--version]
               {init,doctor,status,requirement,analyze,run,resume,cancel,verify,action,runs,ingest,document,memory,domain,validate,snapshot,version,next,explain,open,config}
               ...

AI-Core CLI & daily control plane.

positional arguments:
  {init,doctor,status,requirement,analyze,run,resume,cancel,verify,action,runs,ingest,document,memory,domain,validate,snapshot,version,next,explain,open,config}
    init                Initialize AI-Core in a project.
    doctor              Run project health checks.
    status              Show project or run status.
    requirement         Manage requirements.
    analyze             Analyze a requirement through Gate A0.
    run                 Run a requirement throug
Result: PASS

## CLI-005

Command: `ai-core init <project> --json`
Input: /tmp/ai-core-cli-tests/project
Expected: initialized
Actual: {
  "checks": {
    "AI workspace": true,
    "Agent Harness": true,
    "Documents": true,
    "Domain configuration": true,
    "Memory": true,
    "Project metadata": true,
    "Runtime configuration": true,
    "Skills": true
  },
  "project": "project",
  "root": "/private/tmp/ai-core-cli-tests/project",
  "status": "initialized"
}

Result: PASS

## CLI-006

Command: `ai-core init <project> --json`
Input: rerun
Expected: safe rerun
Actual: {
  "checks": {
    "AI workspace": true,
    "Agent Harness": true,
    "Documents": true,
    "Domain configuration": true,
    "Memory": true,
    "Project metadata": true,
    "Runtime configuration": true,
    "Skills": true
  },
  "project": "project",
  "root": "/private/tmp/ai-core-cli-tests/project",
  "status": "initialized"
}

Result: PASS

## CLI-004

Command: `cd src/feature && ai-core status --json`
Input: nested project path
Expected: auto-detected project
Actual: {
  "active_runs": 0,
  "awaiting_human": 0,
  "completed": 0,
  "documents": 0,
  "knowledge_entries": 0,
  "latest_run": null,
  "project": "project"
}

Result: PASS

## CLI-007

Command: `ai-core doctor --json`
Input: /tmp/ai-core-cli-tests/project
Expected: overall PASS
Actual: {
  "checks": {
    "Agent Harness": "PASS",
    "Documents": "PASS",
    "Domain Packs": "PASS",
    "Git": "PASS",
    "Memory": "PASS",
    "Project": "PASS",
    "Runtime": "PASS",
    "Skills": "PASS",
    "Validators": "PASS"
  },
  "git": {
    "repository": false
  },
  "messages": [
    "PASS project initialized",
    "PASS memory",
    "PASS blind spot",
    "PASS agent harness",
    "PASS documents",
    "PASS domain registry",
    "PASS skills",
    "PASS agent contracts",
    "PASS memory validator"
  ],
  "overall": "PASS"
}

Result: PASS

## CLI-008

Command: `ai-core status --json`
Input: /tmp/ai-core-cli-tests/project
Expected: project overview
Actual: {
  "active_runs": 0,
  "awaiting_human": 0,
  "completed": 0,
  "documents": 0,
  "knowledge_entries": 0,
  "latest_run": null,
  "project": "project"
}

Result: PASS

## CLI-009

Command: `ai-core requirement new`
Input: REQ-CLI-001
Expected: requirement created
Actual: {
  "id": "REQ-CLI-001",
  "path": ".ai/requirements/REQ-CLI-001-merchant-filter.md"
}

Result: PASS

## CLI-010

Command: `ai-core requirement list/show`
Input: REQ-CLI-001
Expected: list and show include requirement
Actual: ID           Title            Status  Path                                           
-----------  ---------------  ------  -----------------------------------------------
REQ-CLI-001  Merchant filter  ACTIVE  .ai/requirements/REQ-CLI-001-merchant-filter.md
---
id: REQ-CLI-001
title: Merchant filter
status: ACTIVE
created: 2026-08-15
source: cli-test
priority: normal
---

# Requirement

Add transaction merchant filtering.

# Acceptance Criteria

- Behavior is proven by CLI test.

# Notes

- None.


Result: PASS

## CLI-011

Command: `ai-core analyze REQ-CLI-001 --json`
Input: safe requirement
Expected: Gate A0 passed
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-001": ".ai/runs/RUN-REQ-CLI-001.json",
    "DOMAIN-CORE-RUN-001": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-001.md",
    "REQ-ANALYSIS-REQ-CLI-001": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-001.md",
    "REQ-REQ-CLI-001": ".ai/requirements/REQ-CLI-001-merchant-filter.md",
    "SKILL-CORE-RUN-001": ".ai/context/SKILL-SELECTION-CORE-RUN-001.md"
  },
  "blocked_reason": "",
  "completed_stages": [
    "REQUIREMENT_ANALYSIS",
    "MEMORY_RETRIEVAL",
    "DOMAIN_RETRIEVAL",
    "BLIND_SPOT",
    "GATE_A0",
    "SKILL_SELECTION"
  ],
  "current_role": "",
  "current_stage": "PLANNING",
  "document_id": "",
  "domain_refs": [],
  "errors": [],
  "gate_status": {
    "A": "NOT_STARTED",
    "A0": "PASSED",
    "C": "NOT_STARTED",
    "D": "NOT_STARTED"
  },

Result: PASS

## CLI-012

Command: `ai-core analyze REQ-CLI-003 --json`
Input: destructive requirement
Expected: exit 4 awaiting human
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-002": ".ai/runs/RUN-REQ-CLI-003.json",
    "DOMAIN-CORE-RUN-002": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-002.md",
    "REQ-ANALYSIS-REQ-CLI-003": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-002.md",
    "REQ-REQ-CLI-003": ".ai/requirements/REQ-CLI-003-delete-financial-records.md"
  },
  "blocked_reason": "CRITICAL Blind Spot blocks planning.",
  "completed_stages": [
    "REQUIREMENT_ANALYSIS",
    "MEMORY_RETRIEVAL",
    "DOMAIN_RETRIEVAL",
    "BLIND_SPOT",
    "GATE_A0"
  ],
  "current_role": "",
  "current_stage": "GATE_A0",
  "document_id": "",
  "domain_refs": [],
  "errors": [
    {
      "code": "HUMAN_APPROVAL_REQUIRED",
      "message": "CRITICAL Blind Spot blocks planning.",
      "recommended_action": "Clarify or approve risk explicitly; 
Result: PASS

## CLI-013

Command: `ai-core action list/show/resolve`
Input: HUMAN-001
Expected: action resolved independently
Actual: ID         Status  Run           Reason                              
---------  ------  ------------  ------------------------------------
HUMAN-001  OPEN    CORE-RUN-002  CRITICAL Blind Spot blocks planning.
{
  "context_refs": [
    ".ai/context/BLIND-SPOT-CORE-RUN-002.md"
  ],
  "created": "2026-08-15T02:18:10Z",
  "reason": "CRITICAL Blind Spot blocks planning.",
  "required_decision": "Clarify or approve risk explicitly; AI-Core will not simulate approval.",
  "run_id": "CORE-RUN-002",
  "status": "OPEN",
  "task_id": "HUMAN-001"
}
Resolved HUMAN-001

Result: PASS

## CLI-014

Command: `ai-core run REQ-CLI-001 --json`
Input: safe requirement
Expected: completed pass
Actual: {
  "artifact_refs": {
    "DOMAIN-CORE-RUN-003": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-003.md",
    "HANDOFF-CORE-RUN-003": ".ai/handoffs/HANDOFF-CORE-RUN-003.md",
    "IMPL-CORE-RUN-003": ".ai/context/IMPLEMENTATION-SUMMARY-CORE-RUN-003.md",
    "KNOW-CORE-RUN-003": ".ai/context/KNOWLEDGE-CAPTURE-CORE-RUN-003.md",
    "PLAN-CORE-RUN-003": ".ai/plans/PLAN-CORE-RUN-003.md",
    "REQ-ANALYSIS-REQ-CLI-001": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-003.md",
    "REQ-REQ-CLI-001": ".ai/requirements/REQ-CLI-001-merchant-filter.md",
    "REVIEW-CORE-RUN-003": ".ai/verification/REVIEW-REPORT-CORE-RUN-003.md",
    "SKILL-CORE-RUN-003": ".ai/context/SKILL-SELECTION-CORE-RUN-003.md",
    "TEST-CORE-RUN-003": ".ai/verification/TEST-EVIDENCE-CORE-RUN-003.md",
    "VERIFY-CORE-RUN-003": ".ai/verificat
Result: PASS

## CLI-015

Command: `ai-core run REQ-CLI-001 --dry-run --json`
Input: safe requirement
Expected: dry run no implementation
Actual: {
  "dry_run": true,
  "run": {
    "artifact_refs": {
      "DOMAIN-CORE-RUN-004": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-004.md",
      "REQ-ANALYSIS-REQ-CLI-001": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-004.md",
      "REQ-REQ-CLI-001": ".ai/requirements/REQ-CLI-001-merchant-filter.md",
      "SKILL-CORE-RUN-004": ".ai/context/SKILL-SELECTION-CORE-RUN-004.md"
    },
    "blocked_reason": "",
    "completed_stages": [
      "REQUIREMENT_ANALYSIS",
      "MEMORY_RETRIEVAL",
      "DOMAIN_RETRIEVAL",
      "BLIND_SPOT",
      "GATE_A0",
      "SKILL_SELECTION"
    ],
    "current_role": "",
    "current_stage": "PLANNING",
    "document_id": "",
    "domain_refs": [],
    "errors": [],
    "gate_status": {
      "A": "NOT_STARTED",
      "A0": "PASSED",
      "C": "NOT_STARTED",
      "D"
Result: PASS

## CLI-016

Command: `ai-core run REQ-CLI-004 --demo test-failure --json`
Input: test loopback
Expected: completed after loopback
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-005": ".ai/runs/RUN-REQ-CLI-004.json",
    "DOMAIN-CORE-RUN-005": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-005.md",
    "HANDOFF-CORE-RUN-005": ".ai/handoffs/HANDOFF-CORE-RUN-005.md",
    "IMPL-CORE-RUN-005": ".ai/context/IMPLEMENTATION-SUMMARY-CORE-RUN-005.md",
    "KNOW-CORE-RUN-005": ".ai/context/KNOWLEDGE-CAPTURE-CORE-RUN-005.md",
    "PLAN-CORE-RUN-005": ".ai/plans/PLAN-CORE-RUN-005.md",
    "REQ-ANALYSIS-REQ-CLI-004": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-005.md",
    "REQ-REQ-CLI-004": ".ai/requirements/REQ-CLI-004-amount-filter.md",
    "REVIEW-CORE-RUN-005": ".ai/verification/REVIEW-REPORT-CORE-RUN-005.md",
    "SKILL-CORE-RUN-005": ".ai/context/SKILL-SELECTION-CORE-RUN-005.md",
    "TEST-CORE-RUN-005": ".ai/verification/TEST-EVIDENCE-CO
Result: PASS

## CLI-017

Command: `ai-core run REQ-CLI-005 --demo reviewer-loop --json`
Input: reviewer loopback
Expected: reviewer loop recorded
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-006": ".ai/runs/RUN-REQ-CLI-005.json",
    "DOMAIN-CORE-RUN-006": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-006.md",
    "HANDOFF-CORE-RUN-006": ".ai/handoffs/HANDOFF-CORE-RUN-006.md",
    "IMPL-CORE-RUN-006": ".ai/context/IMPLEMENTATION-SUMMARY-CORE-RUN-006.md",
    "KNOW-CORE-RUN-006": ".ai/context/KNOWLEDGE-CAPTURE-CORE-RUN-006.md",
    "PLAN-CORE-RUN-006": ".ai/plans/PLAN-CORE-RUN-006.md",
    "REQ-ANALYSIS-REQ-CLI-005": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-006.md",
    "REQ-REQ-CLI-005": ".ai/requirements/REQ-CLI-005-reviewer-loop.md",
    "REVIEW-CORE-RUN-006": ".ai/verification/REVIEW-REPORT-CORE-RUN-006.md",
    "REVIEW-CORE-RUN-006-v1": ".ai/verification/REVIEW-REPORT-CORE-RUN-006-v1.md",
    "SKILL-CORE-RUN-006": ".ai/context/SKILL-SELE
Result: PASS

## CLI-018

Command: `ai-core resume <run> --yes --json`
Input: CORE-RUN-007
Expected: completed after resume
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-007": ".ai/runs/RUN-REQ-CLI-006.json",
    "DOMAIN-CORE-RUN-007": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-007.md",
    "HANDOFF-CORE-RUN-007": ".ai/handoffs/HANDOFF-CORE-RUN-007.md",
    "IMPL-CORE-RUN-007": ".ai/context/IMPLEMENTATION-SUMMARY-CORE-RUN-007.md",
    "KNOW-CORE-RUN-007": ".ai/context/KNOWLEDGE-CAPTURE-CORE-RUN-007.md",
    "PLAN-CORE-RUN-007": ".ai/plans/PLAN-CORE-RUN-007.md",
    "REQ-ANALYSIS-REQ-CLI-006": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-007.md",
    "REQ-REQ-CLI-006": ".ai/requirements/REQ-CLI-006-resume-run.md",
    "REVIEW-CORE-RUN-007": ".ai/verification/REVIEW-REPORT-CORE-RUN-007.md",
    "SKILL-CORE-RUN-007": ".ai/context/SKILL-SELECTION-CORE-RUN-007.md",
    "TEST-CORE-RUN-007": ".ai/verification/TEST-EVIDENCE-CORE-
Result: PASS

## CLI-019

Command: `ai-core cancel <run> --reason ... --json`
Input: CORE-RUN-008
Expected: cancelled
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-008": ".ai/runs/RUN-REQ-CLI-007.json",
    "DOMAIN-CORE-RUN-008": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-008.md",
    "PLAN-CORE-RUN-008": ".ai/plans/PLAN-CORE-RUN-008.md",
    "REQ-ANALYSIS-REQ-CLI-007": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-008.md",
    "REQ-REQ-CLI-007": ".ai/requirements/REQ-CLI-007-cancel-run.md",
    "SKILL-CORE-RUN-008": ".ai/context/SKILL-SELECTION-CORE-RUN-008.md"
  },
  "blocked_reason": "CLI test cancellation",
  "cancellation": {
    "cancelled_at": "2026-08-15T02:18:12Z",
    "last_stage": "GATE_A",
    "reason": "CLI test cancellation"
  },
  "completed_stages": [
    "REQUIREMENT_ANALYSIS",
    "MEMORY_RETRIEVAL",
    "DOMAIN_RETRIEVAL",
    "BLIND_SPOT",
    "GATE_A0",
    "SKILL_SELECTION",
    "PLANNING",
    
Result: PASS

## CLI-020

Command: `ai-core verify <run> --json`
Input: CORE-RUN-003
Expected: verdict PASS
Actual: {
  "failures": [],
  "gates": {
    "A": "PASSED",
    "A0": "PASSED",
    "C": "PASSED",
    "D": "PASSED"
  },
  "run_id": "CORE-RUN-003",
  "status": "COMPLETED",
  "verdict": "PASS",
  "warnings": []
}

Result: PASS

## CLI-021

Command: `ai-core runs`
Input: /tmp/ai-core-cli-tests/project
Expected: lists runs
Actual: Run ID        Requirement  Profile   Stage     Status          Updated               Human Action
------------  -----------  --------  --------  --------------  --------------------  ------------
CORE-RUN-001  REQ-CLI-001  STANDARD  PLANNING  READY           2026-08-15T02:18:09Z              
CORE-RUN-002  REQ-CLI-003  DEEP      GATE_A0   AWAITING_HUMAN  2026-08-15T02:18:10Z  HUMAN-001   
CORE-RUN-003  REQ-CLI-001  STANDARD  COMPLETE  COMPLETED       2026-08-15T02:18:10Z              
CORE-RUN-004  REQ-CLI-001  STANDARD  PLANNING  READY           2026-08-15T02:18:10Z              
CORE-RUN-005  REQ-CLI-004  STANDARD  COMPLETE  COMPLETED       2026-08-15T02:18:11Z              
CORE-RUN-006  REQ-CLI-005  STANDARD  COMPLETE  COMPLETED       2026-08-15T02:18:11Z              
CORE-RUN-007  RE
Result: PASS

## CLI-022

Command: `ai-core ingest specification.md --json`
Input: document
Expected: DOC created
Actual: {
  "document_id": "DOC-001",
  "duplicate": false,
  "items": 3,
  "requirements": 1,
  "unknowns": 1
}

Result: PASS

## CLI-023

Command: `ai-core document review DOC-001 --json`
Input: DOC-001
Expected: review output
Actual: {
  "document_id": "DOC-001",
  "output": "REVIEWED DOC-001 verdict=APPROVED decisions=3\n"
}

Result: PASS

## CLI-024

Command: `ai-core document promote DOC-001 --json`
Input: DOC-001
Expected: promotion output
Actual: {
  "document_id": "DOC-001",
  "output": "PROMOTED DOC-001 promoted=2 blocked=1 status=PARTIALLY_APPROVED\n"
}

Result: PASS

## CLI-025

Command: `ai-core memory search merchant --json`
Input: query
Expected: memory search JSON
Actual: {
  "ok": true,
  "output": "PASS wrote memory brief /private/tmp/ai-core-cli-tests/project/.ai/context/MEMORY-SEARCH-merchant.md\n# Memory Brief\n\n## Project Knowledge\n\n- None found.\n\n## Project Decisions\n\n- None found.\n\n## Active Domain Packs\n\n- None active.\n\n## Relevant Domain Rules\n\n- None found.\n\n## Domain Blind-Spot Patterns\n\n- None found.\n\n## Unverified Items\n\n- None found.\n\n## Conflicts\n\n- None found.\n\n## Impact On Current Requirement\n\nNo reusable project memory matched; inspect repository evidence before planning.\n",
  "path": ".ai/context/MEMORY-SEARCH-merchant.md"
}

Result: PASS

## CLI-026

Command: `ai-core memory validate --json`
Input: /tmp/ai-core-cli-tests/project
Expected: memory ok
Actual: {
  "ok": true,
  "output": "PASS knowledge KNOW-DOC-001 KNOW-DOC-001-only-approved-users-may-export-their-own-accounts.md\nPASS knowledge index /private/tmp/ai-core-cli-tests/project/.ai/knowledge/index.md\nPASS decision index /private/tmp/ai-core-cli-tests/project/.ai/decisions/index.md\nSUMMARY pass=3 warn=0 fail=0\n"
}

Result: PASS

## CLI-027

Command: `ai-core domain list`
Input: framework packs
Expected: lists packs
Actual: Pack                   Version  Status      
---------------------  -------  ------------
access-control         1.0.0    ACTIVE      
billing                1.0.0    ACTIVE      
data-change            1.0.0    ACTIVE      
external-api           1.0.0    ACTIVE      
financial-calculation  1.0.0    ACTIVE      
test-domain-conflict   1.0.0    EXPERIMENTAL

Result: PASS

## CLI-028

Command: `ai-core domain recommend REQ-CLI-001`
Input: requirement
Expected: recommendations no activation
Actual: RECOMMENDED billing@1.0.0 CONFIDENCE=MEDIUM WHY=Reusable billing guidance for bill/payment distinction, billing lifecycle, adjustments, arrears, historical records, reconciliation, audit, backdating, rollback, and tests.
RECOMMENDED data-change@1.0.0 CONFIDENCE=MEDIUM WHY=Reusable data mutation guidance for create/update/delete, migrations, bulk operations, history, rollback, transactions, and audit.
RECOMMENDED test-domain-conflict@1.0.0 CONFIDENCE=MEDIUM WHY=Disposable pack used only to verify DOMAIN_DOMAIN_CONFLICT behavior.
RECOMMENDED access-control@1.0.0 CONFIDENCE=MEDIUM WHY=Reusable access-control guidance for identity, ownership, role boundaries, tenant boundaries, privilege escalation, and audit.
RECOMMENDED external-api@1.0.0 CONFIDENCE=MEDIUM WHY=Reusable external API integrati
Result: PASS

## CLI-029

Command: `ai-core domain activate external-api@1.1.0`
Input: explicit activation
Expected: activated
Actual: ACTIVATED external-api@1.1.0

Result: PASS

## CLI-030

Command: `ai-core domain active`
Input: active packs
Expected: version pinned
Actual: Pack          Version  Status  Notes
------------  -------  ------  -----
external-api  1.1.0    ACTIVE       

Result: PASS

## CLI-031

Command: `ai-core validate --json`
Input: /tmp/ai-core-cli-tests/project
Expected: overall PASS
Actual: {
  "checks": [
    [
      "Project",
      "PASS"
    ],
    [
      "Memory",
      "PASS"
    ],
    [
      "Documents",
      "PASS"
    ],
    [
      "Domains",
      "PASS"
    ],
    [
      "Agents",
      "PASS"
    ],
    [
      "Runs",
      "PASS"
    ]
  ],
  "overall": "PASS"
}

Result: PASS

## CLI-032

Command: `ai-core snapshot --json`
Input: /tmp/ai-core-cli-tests/project
Expected: snapshot path
Actual: {
  "snapshot": ".ai/snapshots/project-manual-20260815T021813Z"
}

Result: PASS

## CLI-033

Command: `ai-core next --json`
Input: /tmp/ai-core-cli-tests/project
Expected: next action JSON
Actual: {
  "next": "resume",
  "run_id": "CORE-RUN-004"
}

Result: PASS

## CLI-034

Command: `ai-core explain <blocked-run> --json`
Input: CORE-RUN-002
Expected: explains blocker
Actual: {
  "explanation": [
    "Why is this blocked?",
    "",
    "CRITICAL Blind Spot blocks planning.",
    "",
    "Related: HUMAN-001",
    "Required action: Resolve HUMAN-001.",
    ""
  ],
  "run_id": "CORE-RUN-002"
}

Result: PASS

## CLI-035

Command: `ai-core doctor --json`
Input: /tmp/ai-core-cli-tests/project
Expected: parseable JSON
Actual: {
  "checks": {
    "Agent Harness": "PASS",
    "Documents": "PASS",
    "Domain Packs": "PASS",
    "Git": "PASS",
    "Memory": "PASS",
    "Project": "PASS",
    "Runtime": "PASS",
    "Skills": "PASS",
    "Validators": "PASS"
  },
  "git": {
    "repository": false
  },
  "messages": [
    "PASS project initialized",
    "PASS memory",
    "PASS blind spot",
    "PASS agent harness",
    "PASS documents",
    "PASS domain registry",
    "PASS skills",
    "PASS agent contracts",
    "PASS memory validator"
  ],
  "overall": "PASS"
}

Result: PASS

## CLI-036

Command: `ai-core status --json`
Input: /tmp/ai-core-cli-tests/project
Expected: parseable JSON
Actual: {
  "active_runs": 3,
  "awaiting_human": 0,
  "completed": 4,
  "documents": 1,
  "knowledge_entries": 1,
  "latest_run": {
    "artifact_refs": {
      "AGENT-CORE-RUN-008": ".ai/runs/RUN-REQ-CLI-007.json",
      "DOMAIN-CORE-RUN-008": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-008.md",
      "PLAN-CORE-RUN-008": ".ai/plans/PLAN-CORE-RUN-008.md",
      "REQ-ANALYSIS-REQ-CLI-007": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-008.md",
      "REQ-REQ-CLI-007": ".ai/requirements/REQ-CLI-007-cancel-run.md",
      "SKILL-CORE-RUN-008": ".ai/context/SKILL-SELECTION-CORE-RUN-008.md"
    },
    "blocked_reason": "CLI test cancellation",
    "cancellation": {
      "cancelled_at": "2026-08-15T02:18:12Z",
      "last_stage": "GATE_A",
      "reason": "CLI test cancellation"
    },
    "completed_stages": [
Result: PASS

## CLI-037

Command: `ai-core analyze --json`
Input: REQ-CLI-001
Expected: parseable JSON
Actual: {
  "artifact_refs": {
    "DOMAIN-CORE-RUN-009": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-009.md",
    "REQ-ANALYSIS-REQ-CLI-001": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-009.md",
    "REQ-REQ-CLI-001": ".ai/requirements/REQ-CLI-001-merchant-filter.md",
    "SKILL-CORE-RUN-009": ".ai/context/SKILL-SELECTION-CORE-RUN-009.md"
  },
  "blocked_reason": "",
  "completed_stages": [
    "REQUIREMENT_ANALYSIS",
    "MEMORY_RETRIEVAL",
    "DOMAIN_RETRIEVAL",
    "BLIND_SPOT",
    "GATE_A0",
    "SKILL_SELECTION"
  ],
  "current_role": "",
  "current_stage": "PLANNING",
  "document_id": "",
  "domain_refs": [
    "API-RULE-002",
    "API-RULE-001",
    "API-TEST-001"
  ],
  "errors": [],
  "gate_status": {
    "A": "NOT_STARTED",
    "A0": "PASSED",
    "C": "NOT_STARTED",
    "D": "NOT_STARTED"
  
Result: PASS

## CLI-038

Command: `ai-core verify --json`
Input: CORE-RUN-003
Expected: parseable JSON
Actual: {
  "failures": [],
  "gates": {
    "A": "PASSED",
    "A0": "PASSED",
    "C": "PASSED",
    "D": "PASSED"
  },
  "run_id": "CORE-RUN-003",
  "status": "COMPLETED",
  "verdict": "PASS",
  "warnings": []
}

Result: PASS

## CLI-039

Command: `blocked exit code`
Input: REQ-CLI-003
Expected: exit code 4
Actual: rc=4
Result: PASS

## CLI-040

Command: `two projects via ai-core`
Input: project/project-b
Expected: isolated run roots
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-001": ".ai/runs/RUN-REQ-CLI-B01.json",
    "DOMAIN-CORE-RUN-001": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-001.md",
    "HANDOFF-CORE-RUN-001": ".ai/handoffs/HANDOFF-CORE-RUN-001.md",
    "IMPL-CORE-RUN-001": ".ai/context/IMPLEMENTATION-SUMMARY-CORE-RUN-001.md",
    "KNOW-CORE-RUN-001": ".ai/context/KNOWLEDGE-CAPTURE-CORE-RUN-001.md",
    "PLAN-CORE-RUN-001": ".ai/plans/PLAN-CORE-RUN-001.md",
    "REQ-ANALYSIS-REQ-CLI-B01": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-001.md",
    "REQ-REQ-CLI-B01": ".ai/requirements/REQ-CLI-B01-project-b-filter.md",
    "REVIEW-CORE-RUN-001": ".ai/verification/REVIEW-REPORT-CORE-RUN-001.md",
    "SKILL-CORE-RUN-001": ".ai/context/SKILL-SELECTION-CORE-RUN-001.md",
    "TEST-CORE-RUN-001": ".ai/verification/TEST-EVIDENCE
Result: PASS

## CLI-041

Command: `status/doctor/memory search`
Input: production marker
Expected: read-only commands do not mutate marker
Actual: b8ebd423dbfe15b990d89243090d93219352b3c6cf66b89327325fd3a94b6b54 -> b8ebd423dbfe15b990d89243090d93219352b3c6cf66b89327325fd3a94b6b54
Result: PASS

## CLI-042

Command: `ai-core doctor --json`
Input: dirty git project
Expected: Git WARNING
Actual: {
  "checks": {
    "Agent Harness": "PASS",
    "Documents": "PASS",
    "Domain Packs": "PASS",
    "Git": "WARNING",
    "Memory": "PASS",
    "Project": "PASS",
    "Runtime": "PASS",
    "Skills": "PASS",
    "Validators": "PASS"
  },
  "git": {
    "branch": "main",
    "commit": "",
    "dirty": true,
    "repository": true
  },
  "messages": [
    "PASS project initialized",
    "PASS memory",
    "PASS blind spot",
    "PASS agent harness",
    "PASS documents",
    "PASS domain registry",
    "PASS skills",
    "PASS agent contracts",
    "PASS memory validator"
  ],
  "overall": "WARNING"
}

Result: PASS

## CLI-043

Command: `ai-core analyse`
Input: unknown command
Expected: suggest analyze
Actual: usage: ai-core [-h] [--project PROJECT] [--json] [--quiet] [--version]
               {init,doctor,status,requirement,analyze,run,resume,cancel,verify,action,runs,ingest,document,memory,domain,validate,snapshot,version,next,explain,open,config}
               ...
Unknown command: analyse

Did you mean:
  analyze

Result: PASS

## CLI-044

Command: `ai-core status`
Input: missing project
Expected: guidance to init
Actual: AI-Core project not found.

Run:
  ai-core init

Result: PASS

## CLI-045

Command: `requirement workflow CLI only`
Input: REQ-CLI-001
Expected: verified PASS
Actual: Verification

Artifacts               PASS
Traceability            PASS
Gates                   {'A': 'PASSED', 'A0': 'PASSED', 'C': 'PASSED', 'D': 'PASSED'}
Critical Risks          0 OPEN

FINAL VERDICT
PASS

Result: PASS

## CLI-046

Command: `document workflow CLI only`
Input: DOC-001
Expected: promote then analyze generated requirement
Actual: {
  "artifact_refs": {
    "AGENT-CORE-RUN-011": ".ai/runs/RUN-REQ-DOC-001.json",
    "DOMAIN-CORE-RUN-011": ".ai/context/DOMAIN-CONTEXT-CORE-RUN-011.md",
    "REQ-ANALYSIS-REQ-DOC-001": ".ai/context/REQUIREMENT-ANALYSIS-CORE-RUN-011.md",
    "REQ-REQ-DOC-001": ".ai/requirements/REQ-DOC-001-the-system-must-add-account-export.md",
    "SKILL-CORE-RUN-011": ".ai/context/SKILL-SELECTION-CORE-RUN-011.md"
  },
  "blocked_reason": "",
  "completed_stages": [
    "REQUIREMENT_ANALYSIS",
    "MEMORY_RETRIEVAL",
    "DOMAIN_RETRIEVAL",
    "BLIND_SPOT",
    "GATE_A0",
    "SKILL_SELECTION"
  ],
  "current_role": "",
  "current_stage": "PLANNING",
  "document_id": "",
  "domain_refs": [
    "API-RULE-001",
    "API-TEST-001"
  ],
  "errors": [],
  "gate_status": {
    "A": "NOT_STARTED",
    "A0": "
Result: PASS
