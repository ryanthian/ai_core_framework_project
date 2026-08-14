# AI-Core Rollback

Rollback should remove or disable the integration layer without deleting Phase 1-3 evidence.

## Disable AI-Core for One Project

Edit the project config:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path("<project>/.ai/ai-core.yaml")
text = p.read_text()
text = text.replace("agent_harness_enabled: true", "agent_harness_enabled: false")
p.write_text(text)
PY
```

Prefer restoring from a snapshot when one exists.

## Cancel One Run

```bash
python3 ai-core/runtime/ai_core.py cancel --project <project> --run-id <RUN-ID> --reason "rollback requested"
```

This preserves artifacts and records the cancellation.

## Remove One Run From Active Use

Do not delete the run directory unless it is disposable test data. Mark it cancelled first and leave evidence in place.

## Restore Run State From Snapshot

1. Inspect `.ai/snapshots/`.
2. Copy only explicit files back:

```bash
cp <snapshot>/run.json <project>/.ai/runs/<RUN-ID>/run.json
cp <snapshot>/artifacts.json <project>/.ai/runs/<RUN-ID>/artifacts.json
```

3. Run AI-Core health and status checks.

## Revert Project Metadata

Restore `.ai/project.json` and `.ai/ai-core.yaml` from the prior snapshot. Do not remove memory, document, decision, or agent harness artifacts.

## Recover From Broken Artifact Registry

1. Inspect `.ai/runs/<RUN-ID>/events.jsonl`.
2. Recreate only missing artifact entries that point to existing files.
3. Run status/resume. If validation still fails, cancel the run and create a replacement run.

## Remove Runtime Integration

Remove references to AI-Core config and leave subsystem scripts intact:

```bash
rm <project>/.ai/ai-core.yaml
rm <project>/.ai/project.json
```

Only use this for disposable fixtures or after confirming no active AI-Core run depends on the files.
