# AI Project Template

This template gives a real software project a lightweight project-memory layer for AI-assisted development.

It is intentionally separate from the reusable Codex skills toolbox. Skills provide capabilities; this template provides operating memory, gates, and evidence.

## Structure

- `.ai/context/`: current project facts, constraints, and environment notes
- `.ai/requirements/`: approved requirements and acceptance criteria
- `.ai/plans/`: implementation plans created before development
- `.ai/decisions/`: meaningful technical or product decisions
- `.ai/handoffs/`: concise continuation packs
- `.ai/verification/`: test, review, and acceptance reports
- `.ai/knowledge/`: stable reusable project knowledge
- `.ai/templates/`: reusable artifact templates
- `docs/`: human-facing project overview, architecture, glossary, and known issues

## Initialize A Project

```bash
ai-project-template/scripts/init-ai-project.sh /path/to/project
```

Optional skill linking:

```bash
CODEX_SKILLS_ROOT=/Users/ryanthian/Documents/Codex_mac/codex-skills \
  ai-project-template/scripts/init-ai-project.sh /path/to/project \
  --link-skill codex-skill-selector \
  --link-skill codex-engineering-workflow
```

The initializer is safe to rerun. It creates missing directories/files, skips existing files, and reports exactly what it changed.

