from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

CONTRACT_VERSION = "2026-03-08"
OVERALL_VALUES = {"PASS", "INCONCLUSIVE", "FAIL"}
RECOMMENDATION_VALUES = {"stop", "new_test", "more_runs"}
FAILURE_CLASSES = {
    "",
    "contract_failure",
    "execution_failure",
    "protocol_failure",
    "resource_contention",
    "routing_failure",
    "state_conflict",
    "timeout",
    "validation_failure",
}
REASON_CODES = {
    "",
    "terminal_success",
    "atlas_step_failed",
    "duplicate_dispatch_blocked",
    "stale_lock_recovered",
    "stale_lock_failed",
    "artifact_missing",
    "artifact_malformed",
    "contract_invalid",
}


def _norm(value: object) -> str:
    return str(value or "").strip()


def validate_result(payload: dict[str, object]) -> dict[str, object]:
    data = dict(payload)
    normalized: dict[str, object] = {
        "contract_version": data.get("contract_version") or CONTRACT_VERSION,
        "created_at": data.get("created_at") or datetime.now(timezone.utc).isoformat(),
        "mission_id": _norm(data.get("mission_id")),
        "dispatch_id": _norm(data.get("dispatch_id")),
        "project_id": _norm(data.get("project_id")),
        "attempt_id": _norm(data.get("attempt_id")),
        "run_dir": _norm(data.get("run_dir")),
        "summary_file": _norm(data.get("summary_file")),
        "overall": _norm(data.get("overall")),
        "recommendation": _norm(data.get("recommendation")),
        "reason_code": _norm(data.get("reason_code")),
        "terminal_reason": _norm(data.get("terminal_reason")),
        "failure_class": _norm(data.get("failure_class")),
        "stale_lock_recovered": bool(data.get("stale_lock_recovered", False)),
    }
    for key in ("attempt_id", "run_dir", "summary_file", "overall", "recommendation"):
        if not normalized[key]:
            raise ValueError(f"missing required field: {key}")
    if normalized["overall"] not in OVERALL_VALUES:
        raise ValueError("unsupported overall")
    if normalized["recommendation"] not in RECOMMENDATION_VALUES:
        raise ValueError("unsupported recommendation")
    if normalized["mission_id"] and not normalized["dispatch_id"]:
        raise ValueError("dispatch_id required when mission_id is present")
    if normalized["dispatch_id"] and not normalized["mission_id"]:
        raise ValueError("mission_id required when dispatch_id is present")
    if normalized["reason_code"] not in REASON_CODES:
        raise ValueError("unsupported reason_code")
    if normalized["failure_class"] not in FAILURE_CLASSES:
        raise ValueError("unsupported failure_class")
    if normalized["overall"] == "FAIL":
        for key in ("reason_code", "terminal_reason", "failure_class"):
            if not normalized[key]:
                raise ValueError(f"{key} required when overall=FAIL")
    if normalized["overall"] == "PASS" and normalized["failure_class"]:
        raise ValueError("failure_class must be empty when overall=PASS")
    if normalized["overall"] == "PASS" and normalized["reason_code"] == "duplicate_dispatch_blocked":
        raise ValueError("duplicate_dispatch_blocked cannot be PASS")
    return normalized


def write_contract(path: str | Path, payload: dict[str, object]) -> dict[str, object]:
    normalized = validate_result(payload)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return normalized


def load_contract(path: str | Path) -> dict[str, object]:
    target = Path(path)
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("contract must be a JSON object")
    return validate_result(data)
