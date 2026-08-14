from __future__ import annotations

from pathlib import Path


def discover(skills_root: Path) -> list[dict]:
    rows = []
    for path in sorted(skills_root.glob("**/SKILL.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        name = path.parent.name
        desc = ""
        for line in text.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            if line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
        rows.append({"name": name, "description": desc, "path": str(path)})
    return rows


def select(skills_root: Path, requirement_text: str) -> list[dict]:
    lower = requirement_text.lower()
    selected = []
    for skill in discover(skills_root):
        name = skill["name"]
        desc = skill["description"].lower()
        if name in {"codex-skill-selector", "codex-engineering-workflow"}:
            selected.append({**skill, "why": "Core controlled workflow and relevant-skill selection guardrails."})
        elif "dashboard" in lower and "frontend" in name:
            selected.append({**skill, "why": "Requirement mentions UI/dashboard work."})
        elif any(term in lower for term in ["ppt", "presentation", "slides"]) and "ppt" in name:
            selected.append({**skill, "why": "Presentation-oriented output requested."})
        elif any(term in lower for term in ["traditional chinese", "zh-tw", "繁體中文"]) and "humanizer" in name:
            selected.append({**skill, "why": "Natural Traditional Chinese rewriting requested."})
    return selected
