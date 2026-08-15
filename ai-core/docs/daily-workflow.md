# Daily AI-Core Workflow

Start with:

```bash
ai-core status
ai-core next
```

If blocked:

```bash
ai-core action list
ai-core action show HUMAN-001
ai-core action resolve HUMAN-001
```

If work is ready:

```bash
ai-core resume CORE-RUN-001 --yes
```

If starting from a requirement:

```bash
ai-core analyze REQ-001
ai-core run REQ-001
```

If starting from a document:

```bash
ai-core ingest specification.md
ai-core document review DOC-001
ai-core document promote DOC-001
```

Normal daily operation should not require direct calls to internal Phase 1-4 scripts.
