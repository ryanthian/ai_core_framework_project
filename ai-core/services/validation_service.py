from __future__ import annotations

from pathlib import Path

from artifacts import validate_registry


def validate_artifacts(project_root: Path, run_dir: Path, state: dict) -> tuple[list[str], list[str]]:
    failures, warnings = validate_registry(project_root, run_dir)
    completed = set(state.get("completed_stages", []))
    gates = state.get("gate_status", {})
    if "TESTING" in completed and "VERIFICATION" in completed:
        pass
    if "VERIFICATION" in completed and "TESTING" not in completed:
        failures.append("verification completed before testing")
    if state.get("status") == "COMPLETED":
        for gate in ["A0", "A", "C", "D"]:
            if gates.get(gate) != "PASSED":
                failures.append(f"completed run missing passed Gate {gate}")
        for stage in ["IMPLEMENTATION", "TESTING", "VERIFICATION", "HANDOFF"]:
            if stage not in completed:
                failures.append(f"completed run missing stage {stage}")
    return failures, warnings
