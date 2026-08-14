# Codex Skills Source Lock

Last updated: 2026-08-14

This file records the reconstructable source state for third-party skills installed under `codex-skills/third-party/`. Third-party skills must remain commit-pinned. Do not update from floating `main` without reviewing the diff, rerunning validation, and updating this lock.

## Third-Party Skills

### frontend-design

- Skill name: `frontend-design`
- Source repository: `anthropics/skills`
- Repository URL: `https://github.com/anthropics/skills`
- Installed commit SHA: `f6656c1256d5a8adfa37db9110046ef20bac644c`
- Branch/tag: source commit from upstream repository; local install is an extracted skill folder, not a retained checkout
- Installation date: 2026-08-14
- Local installation path: `codex-skills/third-party/anthropics-frontend-design`
- License: Apache-2.0, from local `LICENSE.txt`
- License confidence: VERIFIED
- Nested `.git` retained: No
- `.git` decision: REMOVE/ABSENT. The local folder is a copied skill subset. Provenance is retained through this source lock instead of a nested checkout.
- Update method: clone or fetch `https://github.com/anthropics/skills` to a temporary review directory, inspect the README/source diff for `skills/frontend-design`, copy only the reviewed skill files into `codex-skills/third-party/anthropics-frontend-design`, rerun validation and smoke tests, then update this commit record.
- Rollback method: restore the folder from `https://github.com/anthropics/skills` at commit `f6656c1256d5a8adfa37db9110046ef20bac644c`, or from a recorded local backup, then rerun `python3 codex-skills/tests/validate-skills.py codex-skills`.
- Known risks: no nested checkout means reconstruction depends on this lock; design guidance can conflict with an existing product design system and must be selected only when relevant.

### guizang-ppt-skill

- Skill name: `guizang-ppt-skill`
- Source repository: `op7418/guizang-ppt-skill`
- Repository URL: `https://github.com/op7418/guizang-ppt-skill.git`
- Installed commit SHA: `c91369c449d34755d320a8b81d0734000d99d1ab`
- Branch/tag: `main`
- Installation date: 2026-08-14
- Local installation path: `codex-skills/third-party/guizang-ppt-skill`
- License: AGPL-3.0, from local `LICENSE` and README license section
- License confidence: VERIFIED
- Nested `.git` retained: Yes
- `.git` decision: KEEP. The skill contains templates, references, and validator scripts; retaining the checkout materially improves provenance, diff review, and exact commit rollback.
- Update method: run `git -C codex-skills/third-party/guizang-ppt-skill fetch origin`, review `git -C codex-skills/third-party/guizang-ppt-skill diff c91369c449d34755d320a8b81d0734000d99d1ab..origin/main`, inspect changed scripts/templates before execution, update only after validation passes, then update this lock.
- Rollback method: run `git -C codex-skills/third-party/guizang-ppt-skill checkout c91369c449d34755d320a8b81d0734000d99d1ab`, then rerun Guizang validation and registry checks.
- Known risks: AGPL-3.0 obligations may matter if derivative templates are redistributed; generated decks currently reference Google Fonts, Lucide via unpkg, and Motion via jsDelivr, so they are not fully offline portable by default; Swiss validation uses Playwright/Chromium and may require local browser permissions.

### humanizer-zh-tw

- Skill name: `humanizer-zh-tw`
- Source repository: `kevintsai1202/Humanizer-zh-TW`
- Repository URL: `https://github.com/kevintsai1202/Humanizer-zh-TW.git`
- Installed commit SHA: `ef82d8c8eba3509d0830e8793ceb641b0fd8a174`
- Branch/tag: `main`
- Installation date: 2026-08-14
- Local installation path: `codex-skills/third-party/humanizer-zh-tw`
- License: MIT, from local `LICENSE`
- License confidence: VERIFIED
- Nested `.git` retained: Yes
- `.git` decision: KEEP. The retained checkout gives exact provenance and low-friction diff review/rollback for a compact text-oriented skill.
- Update method: run `git -C codex-skills/third-party/humanizer-zh-tw fetch origin`, review the diff from `ef82d8c8eba3509d0830e8793ceb641b0fd8a174` before accepting changes, rerun validation and humanizer smoke tests, then update this lock.
- Rollback method: run `git -C codex-skills/third-party/humanizer-zh-tw checkout ef82d8c8eba3509d0830e8793ceb641b0fd8a174`, then rerun `python3 codex-skills/tests/validate-skills.py codex-skills`.
- Known risks: guidance is editorial and may not fit every Traditional Chinese audience; it includes Claude-style metadata that Codex ignores unless translated into local operating behavior.

## Legacy / Unmanaged Workspace Skill

### tiktok-product-video-automation

- Skill name: `tiktok-product-video-automation`
- Local path: `codex-skills/tiktok-product-video-automation`
- Source repository: not proven in this hardening pass
- Installed commit SHA: not proven
- License: not proven
- License confidence: UNCLEAR
- Nested `.git` retained: No nested `.git` found
- Status: tracked in `docs/skills-registry.md` as LEGACY, not part of the managed third-party source lock
- Known risks: provenance is incomplete; do not promote or reuse across projects until source, license, and version are established.
