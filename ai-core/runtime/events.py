from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def append_event(run_dir: Path, event: str, **data) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    payload = {"time": now(), "event": event, **data}
    with (run_dir / "events.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
