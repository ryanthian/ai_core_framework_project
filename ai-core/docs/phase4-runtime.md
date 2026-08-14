# Phase 4 Runtime Notes

AI-Core is an internal runtime proof, not the Phase 5 user-facing CLI.

Supported internal commands:

```bash
python3 ai-core/runtime/ai_core.py health --project <project>
python3 ai-core/runtime/ai_core.py analyze --project <project> --input <path>
python3 ai-core/runtime/ai_core.py run --project <project> --input <path>
python3 ai-core/runtime/ai_core.py resume --project <project> --run-id <RUN-ID>
python3 ai-core/runtime/ai_core.py status --project <project> --run-id <RUN-ID>
python3 ai-core/runtime/ai_core.py cancel --project <project> --run-id <RUN-ID> --reason "<reason>"
python3 ai-core/runtime/ai_core.py migrate --project <project> --old-state <path>
```

These commands are intentionally minimal. Phase 5 can build a friendlier control plane on top of this runtime.
