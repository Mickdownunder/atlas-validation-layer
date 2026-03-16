# Atlas Validation Contract

Canonical artifact: `<run_dir>/atlas_validation.json`

Required fields:
- `overall`: `PASS | INCONCLUSIVE | FAIL`
- `recommendation`
- `attempt_id`
- `run_dir`
- `summary_file`

Optional fields:
- `mission_id`
- `dispatch_id`
- `project_id`
- `reason_code`
- `terminal_reason`
- `failure_class`
- `stale_lock_recovered`

Rules:
- `mission_id` and `dispatch_id` must either both be present or both be absent.
- `FAIL` requires `reason_code`, `terminal_reason`, and `failure_class`.
- `PASS` cannot carry a non-empty `failure_class`.
- The stdout envelope remains backward compatible for upstream consumers.
