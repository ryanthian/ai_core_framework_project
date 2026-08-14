from __future__ import annotations

import sys
from pathlib import Path


def _load_domainlib(project_root: Path):
    scripts = project_root / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    import domainlib  # type: ignore

    return domainlib


def active(project_root: Path) -> list[dict]:
    domainlib = _load_domainlib(project_root)
    return domainlib.active_packs(project_root)


def relevant(project_root: Path, query: str) -> list[dict]:
    domainlib = _load_domainlib(project_root)
    rows = []
    for score, manifest, rule in domainlib.relevant_domain_rules(project_root, query):
        rows.append({"score": score, "pack": manifest["id"], "version": manifest["version"], "rule": rule})
    return rows
