# Phase 3E Domain Pack Tests

Tested: 2026-08-15

## DOMAIN-001 - Manifest validation

- Command: `python3 ai-project-template/scripts/validate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-access`
- Input: All domain packs.
- Expected: Required manifest fields and rules validate.
- Actual: `SUMMARY pass=18 warn=0 fail=0`
- Result: PASS

## DOMAIN-002 - Registry validation

- Command: `python3 ai-project-template/scripts/validate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-access`
- Input: `domain-packs/index.md`.
- Expected: Registry exists.
- Actual: `PASS domain registry`
- Result: PASS

## DOMAIN-003 - Activation

- Command: `python3 ai-project-template/scripts/activate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-access --pack access-control --version 1.0.0`
- Input: `access-control@1.0.0`.
- Expected: Activation file records pinned pack.
- Actual: `ACTIVATED access-control@1.0.0`
- Result: PASS

## DOMAIN-004 - Deactivation

- Command: `python3 ai-project-template/scripts/activate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-deactivate --pack access-control --version 1.0.0 --deactivate`
- Input: Active access-control pack.
- Expected: `.ai/domain-packs.yaml` returns to `active: []`.
- Actual: `DEACTIVATED access-control@1.0.0 removed=1`
- Result: PASS

## DOMAIN-005 - Version pinning

- Command: `python3 ai-project-template/scripts/validate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-api --pack external-api --check-activation`
- Input: `external-api@1.0.0` activation.
- Expected: Active version matches installed pack.
- Actual: `PASS activation external-api@1.0.0`
- Result: PASS

## DOMAIN-006 - Project retrieval

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-access --project phase3e-access --query "Allow staff to view user account statements"`
- Input: Access-control activation.
- Expected: Relevant domain rules appear.
- Actual: `AC-RULE-001` and `AC-BS-001` retrieved.
- Result: PASS

## DOMAIN-007 - Pack isolation

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-isolation --project phase3e-isolation --query "Send package status to logistics API"` plus `rg "BILL-|billing@"`.
- Input: Only external-api activated.
- Expected: Billing rules are absent.
- Actual: `PASS_NO_BILLING_LEAK`
- Result: PASS

## DOMAIN-008 - Project precedence

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-cross-a --project phase3e-cross-a --query "staff account statements PROJECT_A_ONLY"`
- Input: Project A VERIFIED memory plus access-control domain pack.
- Expected: Project knowledge appears separately before active domain rules.
- Actual: `KNOW-XA-001` appears under Project Knowledge; `AC-RULE-001` appears under Relevant Domain Rules.
- Result: PASS

## DOMAIN-009 - Domain-project conflict

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-conflict --project phase3e-conflict --query "Permanent deletion required by approved policy bulk delete rollback history retention"`
- Input: Data-change pack and conflicting requirement text.
- Expected: `DOMAIN_PROJECT_CONFLICT`.
- Actual: `DOMAIN_PROJECT_CONFLICT` with `DATA-RULE-001`.
- Result: PASS

## DOMAIN-010 - Domain-domain conflict

- Command: same as DOMAIN-009 after activating `test-domain-conflict@1.0.0`.
- Input: `data-change` and `test-domain-conflict`.
- Expected: `DOMAIN_DOMAIN_CONFLICT`.
- Actual: `DOMAIN_DOMAIN_CONFLICT` between `DATA-RULE-001` and `TDC-RULE-001`.
- Result: PASS

## DOMAIN-011 - Blind Spot integration

- Command: `python3 ai-project-template/scripts/validate-blind-spots.py --project-root ai-project-template/tests/fixtures/phase3e-access --report .ai/context/BLIND-SPOT-ACCESS.md`
- Input: Access-control Memory Brief.
- Expected: Blind Spot Report traces access-control rule.
- Actual: `SUMMARY pass=3 warn=1 fail=0`; warning is expected for open HIGH blind spot.
- Result: PASS

## DOMAIN-012 - Agent Harness integration

- Command: `python3 ai-project-template/scripts/validate-agent-run.py --project-root ai-project-template/tests/fixtures/phase3e-access --run-id RUN-REQ-DOMAIN-001 --expect-status RUNNING --expect-profile STANDARD --expect-current-role BLIND_SPOT_REVIEWER --require-artifact MEMORY_RETRIEVER`
- Input: Domain-aware Memory Brief artifact.
- Expected: Harness carries Memory Retriever output into Blind Spot Reviewer.
- Actual: `SUMMARY pass=6 warn=0 fail=0`
- Result: PASS

## DOMAIN-013 - Document Intelligence hints

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-billing --project phase3e-billing --query "billing cycle adjustment arrears meter reconciliation document extraction"`
- Input: Billing pack.
- Expected: `DOCUMENT_EXTRACTION_HINT` appears.
- Actual: `BILL-DOC-001` retrieved.
- Result: PASS

## DOMAIN-014 - Access-control demo

- Command: Access-control retrieval and Blind Spot Pass for `Allow staff to view user account statements`.
- Input: `access-control@1.0.0`.
- Expected: ownership/authorization/audit blind spots.
- Actual: `AC-RULE-001`, `AC-BS-001`, and `BLIND-SPOT-ACCESS.md`.
- Result: PASS

## DOMAIN-015 - External API demo

- Command: External API retrieval and Blind Spot Pass for approved applications API.
- Input: `external-api@1.0.0`.
- Expected: timeout, retry, idempotency, auth, rate limit, reconciliation.
- Actual: `API-RULE-001`, `API-TEST-001`, and `BLIND-SPOT-API.md`.
- Result: PASS

## DOMAIN-016 - Financial calculation demo

- Command: Financial retrieval and Blind Spot Pass for expense + 8% net profit.
- Input: `financial-calculation@1.0.0`.
- Expected: rounding, precision, ordering, negative values, reconciliation.
- Actual: `FIN-RULE-001` and `BLIND-SPOT-FINANCE.md`.
- Result: PASS

## DOMAIN-017 - Billing demo

- Command: Billing/access-control retrieval and Blind Spot Pass for historical statements/payment history.
- Input: `billing@1.0.0` and `access-control@1.0.0`.
- Expected: combined rules with separate namespaces.
- Actual: `BILL-RULE-001`, `BILL-TEST-001`, `BILL-GLOSS-001`, `AC-RULE-001`, `AC-BS-001`.
- Result: PASS

## DOMAIN-018 - Version upgrade

- Command: `python3 ai-project-template/scripts/upgrade-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-api --pack external-api --from-version 1.0.0 --to-version 1.1.0`
- Input: `external-api@1.0.0`.
- Expected: Activation updates to 1.1.0 and retrieves new compatible rule.
- Actual: `UPGRADED external-api 1.0.0->1.1.0`; `API-RULE-002` retrieved.
- Result: PASS

## DOMAIN-019 - Rollback

- Command: `python3 ai-project-template/scripts/upgrade-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-api --pack external-api --from-version 1.0.0 --to-version 1.1.0 --rollback`
- Input: Active `external-api@1.1.0`.
- Expected: Activation returns to 1.0.0.
- Actual: `ROLLED_BACK external-api 1.1.0->1.0.0`
- Result: PASS

## DOMAIN-020 - Domain candidate promotion

- Command: `python3 ai-project-template/scripts/create-domain-candidate.py --project ai-project-template/tests/fixtures/phase3e-finance --candidate-id DOM-CAND-001 ... --decision APPROVE`
- Input: Disposable financial calculation candidate.
- Expected: Candidate artifact is created; pack is not modified automatically.
- Actual: `.ai/domain-candidates/DOM-CAND-001-...md` created with `Decision: APPROVE`.
- Result: PASS

## DOMAIN-021 - Cross-project reuse

- Command: retrieve memory in `phase3e-cross-a` and `phase3e-cross-b`.
- Input: Both activate `access-control@1.0.0`.
- Expected: Both retrieve the same `AC-RULE-001`.
- Actual: `AC-RULE-001` appears in both Memory Briefs.
- Result: PASS

## DOMAIN-022 - Project isolation

- Command: Project B retrieval for `PROJECT_A_ONLY`.
- Input: Project A-only memory marker.
- Expected: Project B does not retrieve Project A memory.
- Actual: `PASS_PROJECT_ISOLATION`
- Result: PASS

## DOMAIN-023 - Memory Brief domain section

- Command: `python3 ai-project-template/scripts/retrieve-memory.py --project-root ai-project-template/tests/fixtures/phase3e-access --project phase3e-access --query "Allow staff to view user account statements"`
- Input: Active access-control pack.
- Expected: Domain sections exist.
- Actual: Memory Brief contains `Active Domain Packs`, `Relevant Domain Rules`, and `Domain Blind-Spot Patterns`.
- Result: PASS

## DOMAIN-024 - Domain rule provenance

- Command: `python3 ai-project-template/scripts/validate-domain-pack.py --project ai-project-template/tests/fixtures/phase3e-access --pack external-api`
- Input: Base and versioned external-api rules.
- Expected: Rules have source references and valid confidence/status.
- Actual: `SUMMARY pass=8 warn=0 fail=0`
- Result: PASS

## Notes

`test-domain-conflict` is an EXPERIMENTAL disposable pack used only to prove `DOMAIN_DOMAIN_CONFLICT`; it should not be activated in real projects.
