---
name: codex-skill-selector
description: Use before non-trivial Codex work to decide whether an existing skill is relevant. Helps discover, select, or skip skills without treating installed skills as mandatory.
---

# Codex Skill Selector

Use this skill when a task is non-trivial, spans multiple files, affects UI, creates documents/slides/content, touches production workflows, or has meaningful verification risk.

## Process

1. Restate the requirement in one sentence.
2. Inspect the repository or available context enough to identify the work type.
3. Check available skills by name and description.
4. Select only skills that directly reduce risk or improve output quality.
5. Explicitly skip skills that are adjacent but not needed.
6. Continue with the selected task workflow.

## Selection Rules

- Skills are capabilities, not required ceremony.
- Do not invoke a skill only because it is installed.
- Prefer project instructions and user instructions over skill defaults.
- Prefer first-party project patterns over third-party advice when they conflict.
- If a skill requires network, credentials, destructive changes, or broad permissions, stop and ask before using that part.

## Output

For substantial tasks, include a compact line before work begins:

```text
Skills selected: <skill names or none>. Reason: <short reason>.
```

For small tasks, keep the selection internal unless a skill changes the workflow.
