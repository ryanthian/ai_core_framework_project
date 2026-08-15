# AI-Core Installation

## Development Installation

Clone the private framework repository:

```bash
git clone https://github.com/ryanthian/ai_core_framework_project.git
cd ai_core_framework_project
pip install -e .
```

Verify the command:

```bash
ai-core version
```

Expected:

```text
AI-Core 0.5.0
```

## Notes

- Do not hard-code private credentials or tokens.
- The `ai-core` command is a Python console entry point.
- The CLI is the daily control plane; it delegates runtime orchestration to Phase 4.
