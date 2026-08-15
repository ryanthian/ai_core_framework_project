# AI-Core Quick Start

From a project directory:

```bash
ai-core init
ai-core doctor
ai-core requirement new --title "Date range filter" --text "Add date range filtering." --source "user request" --priority "normal" --yes
ai-core analyze REQ-001
ai-core run REQ-001
ai-core verify CORE-RUN-001
```

What happens:

- `init` creates `.ai/`, templates, scripts, indexes, config, and project metadata without overwriting existing files.
- `doctor` checks framework readiness.
- `requirement new` creates a structured requirement.
- `analyze` retrieves memory/domain context and runs Blind Spot Pass through Gate A0.
- `run` executes the controlled workflow through implementation, tests, review, verification, memory, and handoff.
- `verify` validates gates, artifacts, risks, traceability, and final evidence.
