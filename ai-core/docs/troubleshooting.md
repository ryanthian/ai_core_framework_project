# AI-Core Troubleshooting

## Command Not Found

Run:

```bash
pip install -e .
```

Then:

```bash
ai-core version
```

## Project Not Initialized

Run:

```bash
ai-core init
```

## Broken Skill Link

Run:

```bash
ai-core doctor --verbose
```

Recreate links through the initializer or the documented skills reuse process.

## Missing Domain Pack

Run:

```bash
ai-core domain list
ai-core domain active
```

Domain recommendations do not activate packs automatically.

## Invalid Memory

Run:

```bash
ai-core memory validate
ai-core memory conflicts
```

Preserve conflicting entries and resolve by source strength.

## Blocked Gate A0

Run:

```bash
ai-core next
ai-core action list
ai-core explain <RUN-ID>
```

Do not bypass critical risks.

## Cancelled Run

Cancelled runs preserve evidence. Start a new run or restore from snapshot.

## Corrupted Run State

Run:

```bash
ai-core validate
ai-core snapshot <RUN-ID>
```

Repair explicit files or roll back from `.ai/snapshots/`.

## Document Parser Unavailable

Run:

```bash
ai-core document show DOC-001
```

If extraction is incomplete, record the limitation and avoid promotion.

## Schema Mismatch

Use documented migration procedures. Do not delete historical run state.

## Dirty Git Workspace

AI-Core reports dirty worktrees but does not commit, reset, stash, push, merge, or checkout application repositories.

## Validation Failure

Run:

```bash
ai-core validate --all
```

Fix evidence-preserving failures before tagging or advancing phases.
