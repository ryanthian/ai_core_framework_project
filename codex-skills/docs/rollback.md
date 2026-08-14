# Codex Skills Rollback Procedure

Use targeted commands only. Do not use broad destructive commands against `codex-skills/` or `.agents/skills/`.

## Remove One Project Skill Link

This disables discovery for the current project while preserving source files.

```bash
unlink /Users/ryanthian/Documents/Codex_mac/.agents/skills/frontend-design
```

Verify:

```bash
find -L /Users/ryanthian/Documents/Codex_mac/.agents/skills -maxdepth 2 -name SKILL.md -print
```

## Disable One Skill Without Deleting It

Move only the project link out of the active `.agents/skills` path.

```bash
mkdir -p /Users/ryanthian/Documents/Codex_mac/.agents/skills-disabled
mv /Users/ryanthian/Documents/Codex_mac/.agents/skills/guizang-ppt-skill /Users/ryanthian/Documents/Codex_mac/.agents/skills-disabled/guizang-ppt-skill
```

Restore later:

```bash
mv /Users/ryanthian/Documents/Codex_mac/.agents/skills-disabled/guizang-ppt-skill /Users/ryanthian/Documents/Codex_mac/.agents/skills/guizang-ppt-skill
```

## Remove One Skill Source Folder

First disable the project link. Then move the source into a dated quarantine folder instead of deleting it.

```bash
mkdir -p /Users/ryanthian/Documents/Codex_mac/codex-skills/disabled/2026-08-14
mv /Users/ryanthian/Documents/Codex_mac/codex-skills/third-party/humanizer-zh-tw /Users/ryanthian/Documents/Codex_mac/codex-skills/disabled/2026-08-14/humanizer-zh-tw
```

## Restore A Previous Third-Party Commit

For retained nested checkouts:

```bash
git -C /Users/ryanthian/Documents/Codex_mac/codex-skills/third-party/guizang-ppt-skill checkout c91369c449d34755d320a8b81d0734000d99d1ab
python3 /Users/ryanthian/Documents/Codex_mac/codex-skills/tests/validate-skills.py /Users/ryanthian/Documents/Codex_mac/codex-skills
```

For extracted folders without nested `.git`, reconstruct from `codex-skills/docs/source-lock.md` by checking out the recorded upstream commit in a temporary directory, reviewing the target skill folder, then replacing only that local skill folder.

## Remove Project-Level Skill Links

Remove explicit links only:

```bash
unlink /Users/ryanthian/Documents/Codex_mac/.agents/skills/codex-skill-selector
unlink /Users/ryanthian/Documents/Codex_mac/.agents/skills/codex-engineering-workflow
```

## Revert Registry Changes

If the parent workspace is under Git, inspect and restore only the registry file:

```bash
git -C /Users/ryanthian/Documents/Codex_mac diff -- docs/skills-registry.md
```

If a known-good copy exists, replace only this file from that backup. Then rerun validation and smoke checks.

## Recover From A Broken Skill

1. Disable discovery first:

```bash
unlink /Users/ryanthian/Documents/Codex_mac/.agents/skills/<skill-name>
```

2. Confirm discovery no longer includes the broken project link:

```bash
find -L /Users/ryanthian/Documents/Codex_mac/.agents/skills -maxdepth 2 -name SKILL.md -print
```

3. Restore source from the exact commit recorded in `codex-skills/docs/source-lock.md`.
4. Rerun:

```bash
python3 /Users/ryanthian/Documents/Codex_mac/codex-skills/tests/validate-skills.py /Users/ryanthian/Documents/Codex_mac/codex-skills
```

## Restore From Source Lock

Use `codex-skills/docs/source-lock.md` as the authority for:

- source repository URL
- installed commit SHA
- license confidence
- nested `.git` decision
- update and rollback method

After any restore, update `docs/skills-registry.md` only if lifecycle status or verification status changed.
