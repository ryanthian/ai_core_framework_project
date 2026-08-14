# Codex Skills Smoke Test Evidence

Last tested: 2026-08-14

These records are evidence from this hardening pass. They are not illustrative examples.

## SKILL-001

## Skill

All workspace `SKILL.md` files.

## Purpose

Validate readable skill files, required frontmatter, malformed YAML-like frontmatter, and duplicate identifiers.

## Preconditions

Run from `/Users/ryanthian/Documents/Codex_mac`.

## Exact Prompt / Command

```bash
python3 codex-skills/tests/validate-skills.py codex-skills
```

## Expected Result

All six workspace skills report `PASS`; no `FAIL`; no duplicate skill identifiers.

## Actual Result

```text
PASS codex-skills/custom/codex-engineering-workflow/SKILL.md name=codex-engineering-workflow
PASS codex-skills/custom/codex-skill-selector/SKILL.md name=codex-skill-selector
PASS codex-skills/third-party/anthropics-frontend-design/SKILL.md name=frontend-design
PASS codex-skills/third-party/guizang-ppt-skill/SKILL.md name=guizang-ppt-skill
PASS codex-skills/third-party/humanizer-zh-tw/SKILL.md name=humanizer-zh-tw
PASS codex-skills/tiktok-product-video-automation/SKILL.md name=tiktok-product-video-automation
SUMMARY skills=6 pass=6 warn=0 fail=0
```

## Evidence

Validator script: `codex-skills/tests/validate-skills.py`.

## PASS / FAIL

PASS

## Notes

This validates workspace source files, not Codex runtime discovery.

## SKILL-002

## Skill

Codex project skill discovery.

## Purpose

Verify that Codex discovers project-linked skills through the real skill mechanism, not merely by checking symlinks.

## Preconditions

Fresh Codex context/session opened in `/Users/ryanthian/Documents/Codex_mac`.

## Exact Prompt / Command

Manual procedure performed in the current Codex session:

1. Start or refresh a Codex session in `/Users/ryanthian/Documents/Codex_mac`.
2. Inspect the system-provided `Available skills` list for project skills loaded from `r12 = /Users/ryanthian/Documents/Codex_mac/.agents/skills`.
3. Compare discovered names against expected ACTIVE skills.

## Expected Result

Expected ACTIVE skills:

- `codex-skill-selector`
- `codex-engineering-workflow`
- `frontend-design`
- `humanizer-zh-tw`

Expected EXPERIMENTAL skill:

- `guizang-ppt-skill`

## Actual Result

Current Codex runtime listed these project skills:

- `codex-engineering-workflow`
- `codex-skill-selector`
- `frontend-design`
- `guizang-ppt-skill`
- `humanizer-zh-tw`

Missing expected ACTIVE skills: none.

Unexpected project skills: none.

Additional global/plugin skills were also visible, which is expected for the broader Codex environment. `tiktok-product-video-automation` was visible as a global skill from `~/.codex/skills`, not as a managed project link.

## Evidence

The current Codex session exposed the skill list before task execution and showed all project-linked skills from `/Users/ryanthian/Documents/Codex_mac/.agents/skills`.

## PASS / FAIL

PASS

## Notes

This is runtime discovery evidence. A fully automated fresh-session CLI probe was not available, so the manual procedure and observed runtime list are recorded.

## SKILL-003

## Skill

`frontend-design`

## Purpose

Verify that the skill can be explicitly loaded and used for a concrete dashboard UI review.

## Preconditions

Skill discovered in current Codex runtime; full `SKILL.md` read from `codex-skills/third-party/anthropics-frontend-design/SKILL.md`.

## Exact Prompt / Command

```text
Use frontend-design to review this isolated dashboard spec:

Affiliate import monitoring dashboard with four KPI cards (Revenue, Expense with 8% adjustment, Profit, Exceptions), a date filter, a conversions table with source/campaign/status/profit columns, and a primary CTA "Import CSV". Mobile concern: the table is too wide. Accessibility concern: status colors may be the only signal.

Return hierarchy issues, spacing/layout issues, typography issues, responsive issues, accessibility issues, and concrete recommended changes.
```

## Expected Result

Concrete UI recommendations derived from the dashboard spec and design workflow, not generic statements.

## Actual Result

Hierarchy issues:

- The primary CTA should not visually compete with the four KPIs. Put `Import CSV` in the top-right action slot, while the dashboard title, date range, and data freshness form the scanning header.
- KPI order should match operating decisions: Profit, Revenue, Expense + 8% adjustment, Exceptions. Exceptions should use alert treatment only when non-zero.
- The table needs a clear default sort, likely profit impact or import time, so users immediately know what changed.

Spacing/layout issues:

- Keep the date filter close to the title but visually separate from the CTA; filters are context, import is an action.
- Use a compact dashboard grid, not marketing-style cards. KPI cards should share consistent height, aligned number baselines, and restrained 8px radius.
- Give the table more horizontal space than the KPIs after the first row; it is the working surface.

Typography issues:

- Use tabular numerals for KPI values and money columns.
- Keep headings compact; avoid hero-scale type inside a dashboard.
- Use a utility/mono treatment only for IDs or import references, not for every label.

Responsive issues:

- On mobile, collapse KPI cards into a 2x2 grid and turn the table into priority rows: campaign, status, profit, with secondary fields in an expandable detail row.
- Date filters should become full-width segmented or stacked controls with stable tap targets.
- The CTA should remain visible after filters, but not sticky unless imports are frequent.

Accessibility issues:

- Status must include text or icon+text, not color alone.
- Date inputs need explicit labels and keyboard focus states.
- Exception states need contrast-checked foreground/background pairs and should not rely on red/green alone.
- Import completion should announce result text near the CTA, with an accessible live status if implemented.

Concrete recommended changes:

- Header: title + last imported timestamp on the left, date range and `Import CSV` on the right.
- KPI row: four equal cards, tabular numbers, small comparison label, no nested cards.
- Table: sticky header, right-aligned money columns, visible sort affordance, status chips with text.
- Mobile: render a card-like row list only for table rows, not the entire page.

## Evidence

Skill was selected, its `SKILL.md` was loaded in the current turn, and the output directly addresses KPI cards, date filter, table, CTA, mobile layout, and accessibility.

## PASS / FAIL

PASS

## Notes

The output is a review artifact, not production UI code.

## SKILL-004

## Skill

`humanizer-zh-tw`

## Purpose

Verify that the skill can be explicitly loaded and used to rewrite AI-like Traditional Chinese while preserving meaning.

## Preconditions

Skill discovered in current Codex runtime; full `SKILL.md` read from `codex-skills/third-party/humanizer-zh-tw/SKILL.md`.

## Exact Prompt / Command

```text
Use humanizer-zh-tw to rewrite this deliberately AI-like Traditional Chinese paragraph into natural Traditional Chinese. Preserve the meaning, remove AI cadence, and include a before/after assessment.

此外，本系統不僅能顯著提升團隊效率，也能在快速變化的市場環境中發揮至關重要的作用。透過無縫、直觀且強大的功能，使用者可以更有效地完成任務。總而言之，這是一個值得期待的解決方案，將為未來工作流程帶來前所未有的價值。
```

## Expected Result

Meaning is preserved while repetitive transitions, inflated wording, and obvious AI cadence are reduced.

## Actual Result

Original issues:

- Uses stock AI transitions: `此外`, `不僅`, `總而言之`.
- Inflated claims: `至關重要`, `無縫、直觀且強大`, `前所未有的價值`.
- Sounds promotional without concrete human rhythm.

Rewritten output:

```text
這套系統主要是把重複工作收起來，讓團隊先看清楚問題，再決定下一步。市場變動快時，它的用途會更明顯：少一點整理資料的時間，多一點時間判斷要不要調整。它不是萬能解法，但能讓日常流程少卡幾個地方。
```

Before/after comparison:

- Meaning preserved: the system improves team workflow efficiency and helps in fast-changing conditions.
- Tone improved: less promotional, more concrete, more natural Traditional Chinese.
- AI cadence reduced: formulaic connectors and exaggerated claims removed.

## Evidence

Skill was selected, its full `SKILL.md` was loaded, and the output applies the skill's listed AI-writing smell checks to a Traditional Chinese sample.

## PASS / FAIL

PASS

## Notes

This verifies rewriting behavior, not grammar tooling.

## SKILL-005

## Skill

`guizang-ppt-skill`

## Purpose

Verify that the skill can generate and validate a minimal 5-slide HTML presentation in an isolated test directory.

## Preconditions

Skill discovered in current Codex runtime; `SKILL.md` and relevant Swiss/presenter references read. Node runtime available at `/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`.

## Exact Prompt / Command

Prompt:

```text
Use guizang-ppt-skill to create a minimal 5-slide Swiss-style HTML presentation in codex-skills/tests/fixtures/guizang-ppt titled "AI-Assisted Software Development Workflow" with slides: Title, Problem, Workflow, Verification, Conclusion. Use no confidential project data. Run available validation/help/build checks and record external CDN dependencies.
```

Commands:

```bash
/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --version
/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node codex-skills/tests/fixtures/generate-guizang-test-deck.mjs
/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node codex-skills/third-party/guizang-ppt-skill/scripts/validate-presenter-mode.mjs codex-skills/tests/fixtures/guizang-ppt/index.html --target-minutes 5
/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node codex-skills/third-party/guizang-ppt-skill/scripts/validate-swiss-deck.mjs codex-skills/tests/fixtures/guizang-ppt/index.html
rg -n "https://|http://|cdn|unpkg|fonts.googleapis|fonts.gstatic|jsdelivr" codex-skills/tests/fixtures/guizang-ppt/index.html
```

## Expected Result

Generated `index.html`; presenter validator passes; Swiss validator passes or reports actionable layout warnings; external dependencies are identified.

## Actual Result

Node:

```text
v24.19.0
```

Generation:

```text
Generated /Users/ryanthian/Documents/Codex_mac/codex-skills/tests/fixtures/guizang-ppt/index.html
```

Presenter validation:

```text
Presenter validation: 5 slides, 5 notes, 3.3 planned minutes, 0 errors, 0 warnings.
```

Swiss validation:

```text
Warnings:
- Slide 1 (SWISS-COVER-ASCII): M1 content reaches 860px; nav-safe line is 837px. Lift the lowest block or add .nav-safe-bottom.
- Slide 2 (S03): M1 bottom whitespace 327px; active content height 58%. Restore spacing/content instead of over-correcting overflow.
- Slide 2 (S03): M2 .h-statement "Work gets risky when output looks finish" has 27px gap before .lead "The failure mode is not lack of effort. " (min 32px).
- Slide 3 (S03): M1 bottom whitespace 341px; active content height 57%. Restore spacing/content instead of over-correcting overflow.
- Slide 3 (S03): M2 .h-statement "Understand → inspect → select skills → p" has 27px gap before .lead "The loop is intentionally simple so it s" (min 32px).
Swiss deck validation passed: 5 slide(s).
- Slide 4 (S03): M1 bottom whitespace 309px; active content height 60%. Restore spacing/content instead of over-correcting overflow.
- Slide 4 (S03): M2 .h-statement "A claim is only accepted after the comma" has 27px gap before .lead "This is the boundary between a nice-look" (min 32px).
- Slide 5 (SWISS-CLOSING-ASCII): M1 content reaches 900px; nav-safe line is 837px. Lift the lowest block or add .nav-safe-bottom.
```

External dependency scan:

```text
7:<link rel="preconnect" href="https://fonts.googleapis.com">
8:<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
9:<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700;800;900&family=JetBrains+Mono:wght@300;400;500;600&family=Noto+Sans+SC:wght@200;300;400;500;700;900&display=swap" rel="stylesheet">
44:       参考: https://carbondesignsystem.com/elements/2x-grid/overview/
59:       https://carbondesignsystem.com/guidelines/motion/overview/
1025:    -webkit-mask-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 22 22'><g stroke='black' stroke-width='1.4' stroke-linecap='round' fill='none'><line x1='8' y1='8' x2='14' y2='14'/><line x1='14' y1='8' x2='8' y2='14'/></g></svg>");
1026:            mask-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 22 22'><g stroke='black' stroke-width='1.4' stroke-linecap='round' fill='none'><line x1='8' y1='8' x2='14' y2='14'/><line x1='14' y1='8' x2='8' y2='14'/></g></svg>");
2061:<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
2071:    motion = await import('https://cdn.jsdelivr.net/npm/motion@11.11.17/+esm');
```

## Evidence

Generated file: `codex-skills/tests/fixtures/guizang-ppt/index.html`.

## PASS / FAIL

PASS

## Notes

Initial non-escalated Swiss validation failed because Chromium could not launch under the macOS sandbox. It was rerun with approved local browser permission and passed with warnings. Generated decks should not be described as fully offline portable unless CDN references are removed.

## SKILL-006

## Skill

`codex-engineering-workflow`

## Purpose

Verify that the workflow can be demonstrated with distinct PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY stages.

## Preconditions

Disposable test fixture only; no production application code.

## Exact Prompt / Command

Prompt:

```text
Use codex-engineering-workflow for a contained demo task: Add a small utility function with unit tests. Show PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY with evidence for each stage.
```

Test command:

```bash
python3 -m unittest discover -s codex-skills/tests/fixtures/workflow-demo -p 'test_*.py' -v
```

## Expected Result

Distinct workflow stages and passing tests.

## Actual Result

PLAN:

- Requirement interpretation: add a tiny utility function with unit tests in an isolated fixture.
- Files expected to change: `skill_math.py`, `test_skill_math.py`.
- Risks: avoid production code, keep imports simple, test both positive and negative deltas.

IMPLEMENT:

```python
def add_points(current, delta):
    """Return the updated points total."""
    return current + delta
```

TEST:

```text
test_add_points_adds_positive_delta (test_skill_math.SkillMathTest) ... ok
test_add_points_preserves_negative_adjustments (test_skill_math.SkillMathTest) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

REVIEW:

- Scope is contained under `codex-skills/tests/fixtures/workflow-demo`.
- Function behavior is direct and covered by positive and negative adjustment tests.
- No external dependency, network access, or production code touched.

VERIFY:

- Unit tests passed.
- Fixture files exist in the expected isolated directory.
- No unresolved issue for this demo.

## Evidence

Files:

- `codex-skills/tests/fixtures/workflow-demo/skill_math.py`
- `codex-skills/tests/fixtures/workflow-demo/test_skill_math.py`

## PASS / FAIL

PASS

## Notes

The stages are backed by an actual code change and executed test command.

## SKILL-007

## Skill

Cross-project reuse procedure.

## Purpose

Verify that selected skills can be linked into another project structure without global promotion.

## Preconditions

Contained target directory under `codex-skills/tests/fixtures/reuse-target`.

## Exact Prompt / Command

```bash
mkdir -p codex-skills/tests/fixtures/reuse-target/.agents/skills
ln -s ../../../../../custom/codex-skill-selector codex-skills/tests/fixtures/reuse-target/.agents/skills/codex-skill-selector
find -L codex-skills/tests/fixtures/reuse-target/.agents/skills -maxdepth 2 -name SKILL.md -print
```

## Expected Result

The linked skill resolves to a readable `SKILL.md`.

## Actual Result

```text
codex-skills/tests/fixtures/reuse-target/.agents/skills/codex-skill-selector/SKILL.md
```

## Evidence

Documentation: `codex-skills/docs/reuse-guide.md`.

## PASS / FAIL

PASS

## Notes

No global promotion to `~/.codex/skills` was performed.

## SKILL-008

## Skill

Rollback procedure review.

## Purpose

Verify that rollback instructions are operational and target explicit paths.

## Preconditions

Rollback documentation exists at `codex-skills/docs/rollback.md`.

## Exact Prompt / Command

```bash
rg -n "Remove One Project Skill Link|Disable One Skill Without Deleting It|Restore A Previous Third-Party Commit|Recover From A Broken Skill|Restore From Source Lock" codex-skills/docs/rollback.md
```

## Expected Result

Rollback document contains procedures for removing one skill, disabling one skill, restoring a previous third-party commit, recovering from a broken skill, and restoring from source-lock information.

## Actual Result

```text
5:## Remove One Project Skill Link
19:## Disable One Skill Without Deleting It
43:## Restore A Previous Third-Party Commit
73:## Recover From A Broken Skill
94:## Restore From Source Lock
```

## Evidence

Documentation: `codex-skills/docs/rollback.md`.

## PASS / FAIL

PASS

## Notes

This is a review of rollback procedure completeness. It intentionally does not execute destructive rollback commands.
