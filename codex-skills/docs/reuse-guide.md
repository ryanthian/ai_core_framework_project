# Codex Skills Reuse Guide

This toolbox supports reuse without installing new skills globally by default. Prefer project-level linking until a skill has proven stable across multiple projects.

## Model A: Project-Level Linking

Use this when another project needs only selected skills from this toolbox.

Example:

```bash
mkdir -p /path/to/another-project/.agents/skills
ln -s /Users/ryanthian/Documents/Codex_mac/codex-skills/custom/codex-skill-selector /path/to/another-project/.agents/skills/codex-skill-selector
ln -s /Users/ryanthian/Documents/Codex_mac/codex-skills/custom/codex-engineering-workflow /path/to/another-project/.agents/skills/codex-engineering-workflow
find -L /path/to/another-project/.agents/skills -maxdepth 2 -name SKILL.md -print
```

Absolute symlinks are clear and work from any checkout location, but they depend on the toolbox staying at `/Users/ryanthian/Documents/Codex_mac/codex-skills`.

Relative symlinks are more portable when the toolbox and target project move together, but they are easier to break if either directory is moved independently.

Contained verification example used in this repository:

```bash
mkdir -p codex-skills/tests/fixtures/reuse-target/.agents/skills
ln -s ../../../../../custom/codex-skill-selector codex-skills/tests/fixtures/reuse-target/.agents/skills/codex-skill-selector
find -L codex-skills/tests/fixtures/reuse-target/.agents/skills -maxdepth 2 -name SKILL.md -print
```

## Model B: User-Level Promotion

Use this only for stable skills that should be available in every Codex project.

Example:

```bash
mkdir -p ~/.codex/skills
ln -s /Users/ryanthian/Documents/Codex_mac/codex-skills/custom/codex-engineering-workflow ~/.codex/skills/codex-engineering-workflow
ln -s /Users/ryanthian/Documents/Codex_mac/codex-skills/custom/codex-skill-selector ~/.codex/skills/codex-skill-selector
```

Verify:

```bash
find -L ~/.codex/skills -maxdepth 2 -name SKILL.md -print
```

Rollback:

```bash
unlink ~/.codex/skills/codex-engineering-workflow
unlink ~/.codex/skills/codex-skill-selector
```

Conflict handling:

- If `~/.codex/skills/<skill-name>` already exists, inspect it before linking.
- Do not overwrite a global skill with a different source or lifecycle status.
- Prefer project-level links when a skill is experimental, project-specific, license-sensitive, or still being validated.

When not to use global installation:

- The skill is EXPERIMENTAL or LEGACY.
- The skill has unresolved license/provenance questions.
- The skill is useful only for one project or one content workflow.
- The skill may conflict with project-local instructions.

No user-level promotion was performed during this hardening task.
