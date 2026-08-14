# Memory Rollback And Repair

Preserve history whenever possible. Do not delete decisions to hide past reasoning.

## Remove One Knowledge Record From Active Use

Prefer deprecation over deletion:

```bash
python3 scripts/capture-knowledge.py --update-id KNOW-001 --status DEPRECATED --evidence "Deprecated because newer evidence replaced it."
```

## Correct Knowledge Metadata

Edit only the frontmatter field that is wrong, then rebuild and validate indexes:

```bash
python3 scripts/validate-memory.py
```

## Reverse A Confidence Change

Use a new evidence note:

```bash
python3 scripts/capture-knowledge.py --update-id KNOW-001 --confidence SUPPORTED --evidence "Reversed VERIFIED status because the source no longer proves the claim."
```

Do not silently downgrade or upgrade confidence without evidence.

## Supersede A Decision

Create a new decision that names the old one:

```bash
python3 scripts/capture-decision.py --id ADR-010 --title "New decision" --status ACCEPTED --supersedes ADR-002 --context "..." --problem "..." --decision "..." --why "..."
```

The old decision remains on disk and is marked `SUPERSEDED`.

## Rebuild Indexes

Run validation. It regenerates both indexes from entry files:

```bash
python3 scripts/validate-memory.py
```

## Recover From Broken Indexes

1. Keep all individual knowledge and decision files.
2. Delete only the broken generated index file if needed.
3. Run:

```bash
python3 scripts/validate-memory.py
```

## Recover From A Broken Entry

1. Move the broken entry out of active use by setting `status: DEPRECATED` or `status: ARCHIVED`.
2. Add evidence explaining why.
3. Create a corrected entry with a new ID when the statement changed materially.
4. Rebuild indexes with `validate-memory.py`.

