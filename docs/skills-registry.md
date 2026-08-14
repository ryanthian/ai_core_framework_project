# Codex Skills Registry

Last tested: 2026-08-14

This registry records every `SKILL.md` currently present in the workspace under `codex-skills/`, including managed, experimental, and legacy skills.

## ACTIVE

### codex-skill-selector

- Name: `codex-skill-selector`
- Purpose: Select relevant skills before non-trivial work without treating installed skills as mandatory.
- Source: Local custom skill.
- Version / commit: 2026-08-14 local custom.
- Location: `codex-skills/custom/codex-skill-selector`; project link `.agents/skills/codex-skill-selector`.
- Trigger / intended use: Use before non-trivial Codex work to decide whether any existing skill applies.
- Dependencies: None.
- Permissions: Reads available skill metadata and local instructions; no external service or elevated permission required.
- Verification status: PASS. Frontmatter validator passed; current Codex session discovered it through the real skill list; used for this hardening task.
- Last tested: 2026-08-14.
- Lifecycle status: ACTIVE.
- Notes: Stable project workflow skill.

### codex-engineering-workflow

- Name: `codex-engineering-workflow`
- Purpose: Enforce disciplined PLAN -> IMPLEMENT -> TEST -> REVIEW -> VERIFY behavior for non-trivial engineering work.
- Source: Local custom skill.
- Version / commit: 2026-08-14 local custom.
- Location: `codex-skills/custom/codex-engineering-workflow`; project link `.agents/skills/codex-engineering-workflow`.
- Trigger / intended use: Use for non-trivial software changes, UI changes, deployments, imports, correctness-sensitive tasks, or testable engineering requests.
- Dependencies: None.
- Permissions: Reads repository files and may write code/tests when invoked for implementation tasks; no external service required.
- Verification status: PASS. Frontmatter validator passed; current Codex session discovered it; contained workflow demo implemented and passed unit tests.
- Last tested: 2026-08-14.
- Lifecycle status: ACTIVE.
- Notes: Required operating discipline for the toolbox itself.

### frontend-design

- Name: `frontend-design`
- Purpose: Improve UI/frontend design review, visual hierarchy, layout, typography, responsive behavior, and accessibility critique.
- Source: `anthropics/skills`, path `skills/frontend-design`.
- Version / commit: `f6656c1256d5a8adfa37db9110046ef20bac644c`.
- Location: `codex-skills/third-party/anthropics-frontend-design`; project link `.agents/skills/frontend-design`.
- Trigger / intended use: Use when building or reshaping frontend UI where visual quality matters.
- Dependencies: None for the skill itself.
- Permissions: Reads UI requirements and relevant project files; may guide code edits when a UI task requires changes.
- Verification status: PASS. Frontmatter validator passed; current Codex session discovered it; explicit design-review smoke test produced concrete recommendations.
- Last tested: 2026-08-14.
- Lifecycle status: ACTIVE.
- Notes: Third-party source is extracted without nested `.git`; provenance is pinned in `codex-skills/docs/source-lock.md`.

### humanizer-zh-tw

- Name: `humanizer-zh-tw`
- Purpose: Rewrite AI-sounding Chinese into natural Traditional Chinese while preserving meaning.
- Source: `kevintsai1202/Humanizer-zh-TW`.
- Version / commit: `ef82d8c8eba3509d0830e8793ceb641b0fd8a174`.
- Location: `codex-skills/third-party/humanizer-zh-tw`; project link `.agents/skills/humanizer-zh-tw`.
- Trigger / intended use: Use when asked to edit, humanize, or review Traditional Chinese copy.
- Dependencies: None.
- Permissions: Reads and rewrites user-provided text; no external service or elevated permission required.
- Verification status: PASS. Frontmatter validator passed; current Codex session discovered it; explicit rewrite smoke test preserved meaning while reducing AI cadence.
- Last tested: 2026-08-14.
- Lifecycle status: ACTIVE.
- Notes: Retains nested `.git` for provenance and update rollback.

## EXPERIMENTAL

### guizang-ppt-skill

- Name: `guizang-ppt-skill`
- Purpose: Generate single-file HTML presentations with magazine-style or Swiss-style layouts, speaker notes, and validation helpers.
- Source: `op7418/guizang-ppt-skill`.
- Version / commit: `c91369c449d34755d320a8b81d0734000d99d1ab`.
- Location: `codex-skills/third-party/guizang-ppt-skill`; project link `.agents/skills/guizang-ppt-skill`.
- Trigger / intended use: Use for web PPT, horizontal swipe decks, magazine-style decks, Swiss-style decks, and presentation covers.
- Dependencies: Node for validation scripts; Playwright/Chromium for Swiss visual validation; generated decks may use Google Fonts, Lucide CDN, and Motion CDN.
- Permissions: Reads templates/references; writes generated deck files when invoked; visual validation may require local browser permissions.
- Verification status: PASS with warnings. Frontmatter validator passed; current Codex session discovered it; generated a five-slide test deck; presenter validator passed; Swiss validator passed with layout warnings.
- Last tested: 2026-08-14.
- Lifecycle status: EXPERIMENTAL.
- Notes: Retains nested `.git`; not fully offline portable by default because generated HTML references external CDNs.

## LEGACY

### tiktok-product-video-automation

- Name: `tiktok-product-video-automation`
- Purpose: Produce TikTok product video planning assets, including Bahasa Melayu scene overviews, short dialogue scripts, realistic image prompts, and Flow AI video prompts.
- Source: Local pre-existing workspace skill; upstream source not proven in this hardening pass.
- Version / commit: UNCLEAR.
- Location: `codex-skills/tiktok-product-video-automation`.
- Trigger / intended use: Legacy content workflow for TikTok/product-video automation.
- Dependencies: None proven from this hardening pass; may depend on image/video generation workflows when used.
- Permissions: Reads product details and emits copy/prompts; no elevated permissions proven.
- Verification status: LIMITED. Frontmatter validator passed. It is not linked from `.agents/skills` as part of the new managed toolbox, though a global skill with the same name is visible in the broader Codex environment.
- Last tested: 2026-08-14 frontmatter only.
- Lifecycle status: LEGACY.
- Notes: Classified LEGACY because it predates the managed toolbox, has incomplete source/license/version provenance, and is not part of the new reusable engineering skill set. It is documented here so no workspace skill remains unmanaged.

## DISABLED

No workspace skill is currently classified DISABLED.
