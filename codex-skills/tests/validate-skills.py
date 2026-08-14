#!/usr/bin/env python3
"""Validate Codex skill frontmatter for this workspace.

This script is intentionally dependency-free. It performs a conservative
frontmatter check for the fields Codex needs to discover a skill: `name` and
`description`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    problems: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover - exercised by filesystem errors
        return {}, [f"FAIL unreadable: {exc}"]

    if not text.startswith("---\n"):
        return {}, ["FAIL missing opening frontmatter delimiter"]

    lines = text.splitlines()
    close_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            close_index = index
            break

    if close_index is None:
        return {}, ["FAIL missing closing frontmatter delimiter"]

    raw = lines[1:close_index]
    data: dict[str, str] = {}
    current_multiline_key: str | None = None

    for line_number, line in enumerate(raw, start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if current_multiline_key and (line.startswith(" ") or line.startswith("\t") or stripped.startswith("- ")):
            continue
        current_multiline_key = None
        if stripped.startswith("- "):
            continue
        if ":" not in line:
            problems.append(f"FAIL malformed frontmatter line {line_number}: {line}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            problems.append(f"FAIL empty frontmatter key at line {line_number}")
            continue
        data[key] = value.strip("'\"")
        if value in {"|", ">"}:
            current_multiline_key = key

    return data, problems


def validate_skill(path: Path) -> tuple[str, str, list[str]]:
    data, problems = parse_frontmatter(path)
    name = data.get("name", "")
    description = data.get("description", "")

    if not name:
        problems.append("FAIL missing required field: name")
    elif not NAME_RE.match(name):
        problems.append(f"WARN non-standard skill name: {name}")

    if not description:
        problems.append("FAIL missing required field: description")

    status = "PASS"
    if any(item.startswith("FAIL") for item in problems):
        status = "FAIL"
    elif problems:
        status = "WARN"

    return status, name or "<missing>", problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex SKILL.md frontmatter.")
    parser.add_argument("root", nargs="?", default="codex-skills", help="Root directory to scan")
    parser.add_argument(
        "--include-agents",
        action="store_true",
        help="Also scan .agents/skills discovery links",
    )
    args = parser.parse_args()

    roots = [Path(args.root)]
    if args.include_agents:
        roots.append(Path(".agents/skills"))

    skill_files: list[Path] = []
    for root in roots:
        if not root.exists():
            print(f"FAIL root missing: {root}")
            return 1
        skill_files.extend(sorted(root.rglob("SKILL.md")))

    seen_names: dict[str, Path] = {}
    duplicate_failures: list[str] = []
    rows: list[tuple[str, Path, str, list[str]]] = []

    for path in skill_files:
        status, name, problems = validate_skill(path)
        resolved = path.resolve()
        if name != "<missing>":
            previous = seen_names.get(name)
            if previous and previous.resolve() != resolved:
                status = "FAIL"
                message = f"FAIL duplicate skill identifier '{name}' also in {previous}"
                problems.append(message)
                duplicate_failures.append(message)
            else:
                seen_names[name] = path
        rows.append((status, path, name, problems))

    for status, path, name, problems in rows:
        print(f"{status} {path} name={name}")
        for problem in problems:
            print(f"  {problem}")

    pass_count = sum(1 for status, *_ in rows if status == "PASS")
    warn_count = sum(1 for status, *_ in rows if status == "WARN")
    fail_count = sum(1 for status, *_ in rows if status == "FAIL")
    print(f"SUMMARY skills={len(rows)} pass={pass_count} warn={warn_count} fail={fail_count}")

    return 1 if fail_count or duplicate_failures else 0


if __name__ == "__main__":
    sys.exit(main())
