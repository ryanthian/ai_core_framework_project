# Codex Skills Environment Audit

Date: 2026-08-14

## Current Environment

- Working directory: `/Users/ryanthian/Documents/Codex_mac`.
- OS: macOS Darwin 24.5.0 arm64.
- Codex config: `/Users/ryanthian/.codex/config.toml`.
- Enabled plugins: documents, spreadsheets, presentations, Google Drive, GitHub, Notion, Chrome, computer-use, PDF, template-creator, Sites, visualize, browser.
- Workspace trust: `/Users/ryanthian/Documents/Codex_mac` is trusted.
- Global instructions: `/Users/ryanthian/.codex/AGENTS.md` exists but is empty.
- Workspace root before this setup: no `AGENTS.md`; created one for operating rules.
- Git: available, `git version 2.39.5`.
- GitHub CLI: available, `gh version 2.97.0`.
- Default `node`, `npm`, `npx`, `yarn`, `bun`, `deno`: not on PATH.
- Bundled Node: `/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`, version `v24.19.0`.
- Bundled pnpm: `/Users/ryanthian/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/fallback/pnpm`, version `11.19.0`.
- Python: `python3` version `3.9.6`; `python` not on PATH.
- pip: `pip3` version `21.2.4`.
- Homebrew, uv, pipx: not on PATH.
- Workspace root Git: not a Git repository; several child projects are Git repositories.

## Existing Skills

Global skills in `/Users/ryanthian/.codex/skills`:

- `screenshot`
- `hatch-pet`
- `security-best-practices`
- `pdf`
- `playwright`
- `speech`
- `tiktok-product-video-automation`
- `cloudflare-deploy`
- `render-deploy`
- `transcribe`

System skills include `skill-installer`, `skill-creator`, `plugin-creator`, `openai-docs`, `imagegen`, and `review-agent`.

Workspace legacy skill folder:

- `codex-skills/tiktok-product-video-automation`

## Missing Dependencies

- Default shell lacks `node`, `npm`, and `npx`; use the bundled runtime paths or add Node to PATH before running npm-based skill tooling.
- Homebrew is not available.
- `uv` and `pipx` are not available.
- Project-level `.agents` was read-only under the sandbox and required approval to create `.agents/skills` links.

## Risks / Conflicts

- Full Superpowers conflicts with the local operating rule because it says skills must be used if there is even a small chance they apply.
- Vercel `web-design-guidelines` fetches latest rules from a remote URL every use; useful, but not ideal for a stable offline toolbox.
- Vercel `skills` CLI is a tool, not a skill; it also requires Node >=22.20 and includes telemetry unless disabled.
- Guizang source has a license inconsistency: GitHub API reported AGPL-3.0, while the cloned `LICENSE` file at the installed commit is MIT.
- Guizang generated templates can load CDN resources; offline or privacy-sensitive decks should be adjusted before use.
- Anthropic document/PDF/PPT/XLSX skills overlap with already enabled first-party documents, presentations, spreadsheets, and PDF plugins, so they were not installed.

## Candidate Evaluation

### `vercel-labs/skills`

- Purpose: CLI for installing, finding, updating, and removing agent skills.
- Installation method: `npx skills ...`.
- Permissions: network and filesystem writes to project or global skill directories.
- Dependencies: Node >=22.20, npm/npx.
- Files modified: agent skill directories selected by CLI.
- Commands/scripts: TypeScript CLI with network fetch, git/auth fallback, telemetry, update/remove operations.
- Compatibility: supports Codex paths, but not itself a reusable skill.
- Maintenance: active; inspected commit `c6f69c631292444cc541ac6d91e2226b0ff247da`.
- Security concerns: network fetches, telemetry by default, broad installer behavior.
- Overlap: duplicates existing manual install ability.
- Usefulness: useful later as a tool once Node/npx is normalized.
- Classification: DO NOT INSTALL.

### `vercel-labs/agent-skills`

- Purpose: Vercel skill collection for deployment, UI guidelines, writing guidelines, React, composition, and optimization.
- Installation method: `npx skills add vercel-labs/agent-skills --skill <name> -a codex`.
- Permissions: network and filesystem writes.
- Dependencies: varies by skill; `web-design-guidelines` fetches remote guidelines at use time.
- Files modified: selected skill folders.
- Commands/scripts: some skills include scripts, especially Vercel optimization/deploy flows.
- Compatibility: Codex-compatible skill format.
- Maintenance: active; inspected commit `b8caa260a420a73042e35521de4b5c8baf6446cc`.
- Security concerns: deploy/optimize skills can touch credentials and remote services; guideline skills can fetch remote instructions.
- Overlap: frontend/design guidance overlaps with current instructions and installed `frontend-design`.
- Usefulness: good later for Vercel/React-heavy work.
- Classification: OPTIONAL.

### `anthropics/skills`

- Purpose: Example and production-style skills for design, testing, docs, documents, PDFs, PPTX, XLSX, and development tasks.
- Installation method: copy selected skill folders or use compatible skill installer.
- Permissions: filesystem writes only for selected source-only skills.
- Dependencies: `frontend-design` has no runtime dependencies.
- Files modified: selected skill folders.
- Commands/scripts: not used for `frontend-design`.
- Compatibility: `frontend-design` uses standard `SKILL.md` frontmatter and works in Codex.
- Maintenance: active; inspected commit `f6656c1256d5a8adfa37db9110046ef20bac644c`.
- Security concerns: repository has source-available/non-open-source document skills, but `frontend-design` itself is Apache 2.0.
- Overlap: design guidance complements existing frontend rules; document skills overlap existing plugins.
- Usefulness: high for UI quality.
- Classification: INSTALL, only `skills/frontend-design`.

### `op7418/guizang-ppt-skill`

- Purpose: Generate single-file HTML decks with presentation runtime, speaker notes, and visual systems.
- Installation method: copy or clone skill folder into Codex skills path.
- Permissions: filesystem writes; optional update checks use GitHub network.
- Dependencies: optional Node for validator scripts; generated decks may use CDN fonts/scripts.
- Files modified: skill folder; generated deck output when used.
- Commands/scripts: validation scripts in `scripts/*.mjs`; not executed during install.
- Compatibility: explicit Codex guidance in `SKILL.md`.
- Maintenance: active; inspected commit `c91369c449d34755d320a8b81d0734000d99d1ab`.
- Security concerns: license mismatch between GitHub API and cloned `LICENSE`; CDN usage in templates; optional update check.
- Overlap: presentation plugin can create standard slides, but Guizang provides HTML web-deck style.
- Usefulness: high for presentation-oriented output.
- Classification: INSTALL as EXPERIMENTAL.

### `kevintsai1202/Humanizer-zh-TW`

- Purpose: Natural Traditional Chinese rewriting and AI-writing cleanup.
- Installation method: copy or clone repository into Codex skills path.
- Permissions: filesystem writes.
- Dependencies: none.
- Files modified: skill folder only.
- Commands/scripts: none.
- Compatibility: `SKILL.md` format is usable in Codex; `allowed-tools` names are Claude-style but harmless as metadata.
- Maintenance: moderate; inspected commit `ef82d8c8eba3509d0830e8793ceb641b0fd8a174`.
- Security concerns: fork of another repo; no scripts or dependencies.
- Overlap: complements existing Chinese content instructions.
- Usefulness: high for Traditional Chinese copy.
- Classification: INSTALL.

### Superpowers / `obra/superpowers`

- Purpose: Complete engineering workflow methodology for planning, TDD, debugging, subagents, review, and verification.
- Installation method: Codex plugin marketplace or clone/symlink.
- Permissions: plugin install or filesystem writes; some workflows use worktrees, subagents, and destructive cleanup after approval.
- Dependencies: none for markdown skills; optional tests/scripts for repository maintenance.
- Files modified: plugin/skill installation paths.
- Commands/scripts: many repository test scripts; not needed for basic skill use.
- Compatibility: has Codex plugin manifest and Codex tool references.
- Maintenance: active; inspected commit `b36e0829c6d0140e93cfef2ca599b1b07d4a7797`, plugin version `6.3.0`.
- Security concerns: `using-superpowers` requires skill invocation before any response and treats skill usage as non-optional, conflicting with this toolbox rule.
- Overlap: useful concepts overlap with the custom `codex-engineering-workflow`.
- Usefulness: high as reference; too forceful as a default install.
- Classification: DO NOT INSTALL full plugin; adapt only the verification discipline into local custom workflow.

## Recommended Installation Plan

1. Use project-level `.agents/skills` for this workspace and keep canonical source under `codex-skills/`.
2. Install only:
   - `frontend-design`
   - `humanizer-zh-tw`
   - `guizang-ppt-skill` as experimental
   - local `codex-skill-selector`
   - local `codex-engineering-workflow`
3. Defer Vercel agent skills until a Vercel/React-specific project needs them.
4. Do not install full Superpowers unless you explicitly want a stricter always-on methodology later.
5. Revisit global installation only after confirming this project-level toolbox works well.
