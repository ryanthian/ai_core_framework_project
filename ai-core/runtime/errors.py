from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class CoreError:
    code: str
    message: str
    stage: str
    severity: str = "ERROR"
    recoverable: bool = True
    recommended_action: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


ERRORS = {
    "PROJECT_NOT_INITIALIZED",
    "INVALID_REQUIREMENT",
    "DOCUMENT_PARSE_FAILED",
    "MEMORY_VALIDATION_FAILED",
    "DOMAIN_CONFLICT",
    "MEMORY_CONFLICT",
    "CRITICAL_BLIND_SPOT",
    "GATE_BLOCKED",
    "SKILL_NOT_FOUND",
    "TEST_FAILED",
    "REVIEW_CHANGES_REQUIRED",
    "HUMAN_APPROVAL_REQUIRED",
    "ARTIFACT_MISSING",
    "RUN_STATE_INVALID",
}


def error(code: str, message: str, stage: str, severity: str = "ERROR", recoverable: bool = True, recommended_action: str = "") -> dict:
    if code not in ERRORS:
        code = "RUN_STATE_INVALID"
    return CoreError(code, message, stage, severity, recoverable, recommended_action).to_dict()
