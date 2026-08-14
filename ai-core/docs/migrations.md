# AI-Core Migration Rules

AI-Core uses `schema_version` fields for:

- `.ai/project.json`
- `.ai/ai-core.yaml`
- `.ai/runs/<RUN-ID>/run.json`
- `.ai/runs/<RUN-ID>/artifacts.json`

## Current Version

Current runtime schema: `2`.

## Demonstrated Migration

The Phase 4 migration adapter supports converting a simple v1 agent-harness-like run state into canonical v2 AI-Core run state:

```bash
python3 ai-core/runtime/ai_core.py migrate --project <project> --old-state <old-run.json>
```

The migration:

- preserves run id
- preserves requirement and artifact references where available
- maps old status fields into canonical status
- creates `.ai/runs/<RUN-ID>/run.json`
- creates an empty v2 artifact registry
- records `SCHEMA_MIGRATED` in the event log

## Migration Safety Rules

- Snapshot before migration where practical.
- Do not delete old subsystem artifacts.
- Do not rewrite historical evidence.
- Do not silently drop unknown fields when they may contain operational evidence.
- Validate artifacts after migration.
