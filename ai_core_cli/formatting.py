from __future__ import annotations

import json
import os
import sys


PASS = "PASS" if os.environ.get("NO_COLOR") else "✓ PASS"
WARN = "WARNING" if os.environ.get("NO_COLOR") else "⚠ WARNING"
FAIL = "FAIL" if os.environ.get("NO_COLOR") else "✗ FAIL"
RUNNING = "RUNNING" if os.environ.get("NO_COLOR") else "→ RUNNING"
HUMAN = "AWAITING HUMAN" if os.environ.get("NO_COLOR") else "⏸ AWAITING HUMAN"


EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_INVALID = 2
EXIT_VALIDATION = 3
EXIT_BLOCKED = 4
EXIT_VERIFY = 5
EXIT_CONFIG = 6


def emit_json(payload: dict, code: int = 0) -> int:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return code


def print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(str(cell)))
    fmt = "  ".join("{:<" + str(width) + "}" for width in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * width for width in widths]))
    for row in rows:
        print(fmt.format(*[str(cell) for cell in row]))


def status_exit(status: str) -> int:
    if status in {"COMPLETED", "READY", "VERIFIED", "PASS"}:
        return EXIT_SUCCESS
    if status in {"AWAITING_HUMAN", "BLOCKED"}:
        return EXIT_BLOCKED
    if status in {"FAILED"}:
        return EXIT_VERIFY
    return EXIT_SUCCESS
