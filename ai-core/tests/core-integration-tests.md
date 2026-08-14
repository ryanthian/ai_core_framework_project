# Phase 4 Core Integration Tests

## CORE-001

Command: `inspect .ai/project.json`
Input: phase4-structured
Expected: project model exists
Actual: True
Result: PASS

## CORE-002

Command: `inspect .ai/ai-core.yaml`
Input: phase4-structured
Expected: runtime config exists
Actual: True
Result: PASS

## CORE-003

Command: `/Library/Developer/CommandLineTools/usr/bin/python3 /Users/ryanthian/Documents/Codex_mac/ai_core_framework_project/ai-core/runtime/ai_core.py health --project /Users/ryanthian/Documents/Codex_mac/ai_core_framework_project/ai-core/tests/fixtures/phase4-structured`
Input: phase4-structured
Expected: HEALTH PASS
Actual: HEALTH PASS
Result: PASS

## CORE-004

Command: `ai_core.py run/analyze`
Input: structured + document inputs
Expected: input types routed
Actual: STRUCTURED_REQUIREMENT / SOURCE_DOCUMENT
Result: PASS

## CORE-005

Command: `ai_core.py run structured`
Input: REQ-401
Expected: COMPLETED PASS
Actual: COMPLETED PASS
Result: PASS

## CORE-006

Command: `ai_core.py run document`
Input: account-export.md
Expected: COMPLETED PASS with document_id
Actual: COMPLETED DOC-001
Result: PASS

## CORE-007

Command: `artifact registry`
Input: structured
Expected: MEMORY_BRIEF exists
Actual: True
Result: PASS

## CORE-008

Command: `domain retrieval`
Input: domain conflict fixture
Expected: human action from domain conflict
Actual: AWAITING_HUMAN
Result: PASS

## CORE-009

Command: `blind spot service`
Input: critical blocker
Expected: Gate A0 blocked
Actual: {'A': 'NOT_STARTED', 'A0': 'BLOCKED', 'C': 'NOT_STARTED', 'D': 'NOT_STARTED'}
Result: PASS

## CORE-010

Command: `skill service`
Input: structured
Expected: SKILL_SELECTION exists
Actual: True
Result: PASS

## CORE-011

Command: `agent service`
Input: agent integration fixture
Expected: AGENT_RUN_STATE exists
Actual: True
Result: PASS

## CORE-012

Command: `gate enforcement`
Input: structured
Expected: A0/A/C/D passed
Actual: {'A': 'PASSED', 'A0': 'PASSED', 'C': 'PASSED', 'D': 'PASSED'}
Result: PASS

## CORE-013

Command: `human action`
Input: critical blocker
Expected: human action created
Actual: ['.ai/human-actions/HUMAN-001.json']
Result: PASS

## CORE-014

Command: `artifact registry`
Input: structured
Expected: registry has artifacts
Actual: 15
Result: PASS

## CORE-015

Command: `traceability`
Input: structured
Expected: traceability artifact exists
Actual: True
Result: PASS

## CORE-016

Command: `unified run`
Input: structured
Expected: COMPLETE
Actual: COMPLETE
Result: PASS

## CORE-017

Command: `ai_core.py resume`
Input: phase4-resume
Expected: completed after resume
Actual: COMPLETED
Result: PASS

## CORE-018

Command: `ai_core.py cancel + resume`
Input: phase4-cancel
Expected: stays CANCELLED
Actual: CANCELLED
Result: PASS

## CORE-019

Command: `events.jsonl`
Input: test-failure
Expected: TESTER loopback
Actual: {"event": "RUN_CREATED", "input_ref": ".ai/requirements/REQ-405-amount-filter.md", "input_type": "STRUCTURED_REQUIREMENT", "profile": "STANDARD", "time": "2026-08-14T17:53:25Z"}
{"event": "INPUT_ROUTED", "input_type": "STRUCTURED_REQUIREMENT", "time": "2026-08-14T17:53:25Z"}
{"artifact": ".ai/context/MEMORY-BRIEF-CORE-RUN-002.md", "event": "MEMORY_RETRIEVED", "time": "2026-08-14T17:53:25Z"}
{"critical_open": 0, "event": "BLIND_SPOT_COMPLETED", "high_open": 0, "time": "2026-08-14T17:53:26Z", "ver
Result: PASS

## CORE-020

Command: `events.jsonl`
Input: reviewer-loop
Expected: REVIEWER loopback
Actual: {"event": "RUN_CREATED", "input_ref": ".ai/requirements/REQ-406-reviewer-loop.md", "input_type": "STRUCTURED_REQUIREMENT", "profile": "STANDARD", "time": "2026-08-14T17:53:10Z"}
{"event": "INPUT_ROUTED", "input_type": "STRUCTURED_REQUIREMENT", "time": "2026-08-14T17:53:10Z"}
{"artifact": ".ai/context/MEMORY-BRIEF-CORE-RUN-001.md", "event": "MEMORY_RETRIEVED", "time": "2026-08-14T17:53:10Z"}
{"critical_open": 0, "event": "BLIND_SPOT_COMPLETED", "high_open": 0, "time": "2026-08-14T17:53:10Z", "ver
Result: PASS

## CORE-021

Command: `memory retrieval + blind spot`
Input: memory conflict
Expected: AWAITING_HUMAN
Actual: AWAITING_HUMAN
Result: PASS

## CORE-022

Command: `domain retrieval`
Input: domain conflict
Expected: AWAITING_HUMAN
Actual: AWAITING_HUMAN
Result: PASS

## CORE-023

Command: `document pipeline`
Input: doc conflict
Expected: AWAITING_HUMAN
Actual: AWAITING_HUMAN
Result: PASS

## CORE-024

Command: `cancel snapshot`
Input: phase4-cancel
Expected: snapshot exists
Actual: True
Result: PASS

## CORE-025

Command: `ai_core.py migrate`
Input: old-run-v1.json
Expected: schema_version 2
Actual: 2
Result: PASS

## CORE-026

Command: `project roots`
Input: Project A/B
Expected: isolated run roots and distinct project ids
Actual: phase4-project-a / phase4-project-b
Result: PASS

## CORE-027

Command: `finalization`
Input: structured
Expected: COMPLETED only after gates
Actual: ['REQUIREMENT_ANALYSIS', 'MEMORY_RETRIEVAL', 'DOMAIN_RETRIEVAL', 'BLIND_SPOT', 'GATE_A0', 'SKILL_SELECTION', 'PLANNING', 'GATE_A', 'IMPLEMENTATION', 'TESTING', 'REVIEW', 'VERIFICATION', 'GATE_C', 'MEMORY_CURATION', 'HANDOFF', 'GATE_D', 'COMPLETE']
Result: PASS

## CORE-028

Command: `error model`
Input: critical blocker
Expected: structured error exists
Actual: [{'code': 'HUMAN_APPROVAL_REQUIRED', 'message': 'CRITICAL Blind Spot blocks planning.', 'recommended_action': 'Clarify or approve risk explicitly; AI-Core will not simulate approval.', 'recoverable': True, 'severity': 'CRITICAL', 'stage': 'GATE_A0'}]
Result: PASS

## CORE-029

Command: `ai_core.py status`
Input: structured
Expected: status summary command available
Actual: status function exercised by runtime
Result: PASS

## CORE-030

Command: `summary.md`
Input: structured
Expected: AI-Core Run Summary exists
Actual: True
Result: PASS
