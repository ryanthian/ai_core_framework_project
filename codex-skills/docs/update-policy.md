# Codex Skills Update Policy

Third-party skills are commit-pinned. No automatic floating-`main` updates are allowed.

Before adopting an update:

- Review the upstream README and source diff.
- Inspect scripts before running them.
- Recheck dependencies, permissions, external network references, and license status.
- Record the current commit and rollback path before changing source files.
- Rerun frontmatter validation and all relevant smoke tests.
- Update `codex-skills/docs/source-lock.md` and `docs/skills-registry.md`.

## Update Lifecycle

1. CHECK
   - Identify the current local commit and upstream target commit.
   - Confirm the skill is still needed.

2. REVIEW DIFF
   - Review changed `SKILL.md`, README, scripts, templates, assets, and license files.
   - Do not execute new or changed scripts until reviewed.

3. BACKUP / RECORD CURRENT COMMIT
   - Record the current commit in `source-lock.md`.
   - For extracted folders, make a targeted backup of the skill folder before replacing it.

4. UPDATE
   - Update only the intended skill folder.
   - Do not mix third-party source changes with custom skill changes.

5. VALIDATE
   - Run `python3 codex-skills/tests/validate-skills.py codex-skills`.

6. SMOKE TEST
   - Rerun the smoke test for the changed skill.
   - Rerun discovery checks if project links changed.

7. ACCEPT / ROLLBACK
   - Accept only when validation and smoke tests pass.
   - Roll back using `codex-skills/docs/rollback.md` if the update changes behavior unexpectedly.
