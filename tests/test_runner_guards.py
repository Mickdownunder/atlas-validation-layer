import os
import subprocess
import time
import unittest
from pathlib import Path

from lib.atlas_validation_contract import load_contract

ATLAS_ROOT = Path(__file__).resolve().parents[1]
ATLAS_BIN = str(ATLAS_ROOT / "bin" / "atlas-sandbox-run")
LOCK_DIR = ATLAS_ROOT / "logs" / "dispatch"


def parse_envelope(text: str) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data


class AtlasRunnerGuardTests(unittest.TestCase):
    def test_invalid_project_binding_writes_valid_contract(self):
        env = os.environ.copy()
        env["ATLAS_OPERATOR_PROJECT_ID"] = "bad"
        env["ATLAS_WORKSPACE_ROOT"] = str(ATLAS_ROOT)
        proc = subprocess.run([ATLAS_BIN, "status"], text=True, capture_output=True, env=env)
        self.assertNotEqual(proc.returncode, 0)
        envelope = parse_envelope(proc.stdout)
        self.assertEqual(envelope["REASON_CODE"], "contract_invalid")
        contract = load_contract(envelope["RESULT_JSON"])
        self.assertEqual(contract["failure_class"], "contract_failure")

    def test_duplicate_dispatch_blocked_before_execution(self):
        dispatch_id = f"disp-test-{os.getpid()}"
        lock_path = LOCK_DIR / f"{dispatch_id}.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.write_text(f"pid={os.getpid()}\nts={int(time.time())}\nattempt_id=test-attempt\n", encoding="utf-8")
        env = os.environ.copy()
        env["ATLAS_DISPATCH_ID"] = dispatch_id
        env["ATLAS_MISSION_ID"] = "mis_test"
        env["ATLAS_WORKSPACE_ROOT"] = str(ATLAS_ROOT)
        try:
            proc = subprocess.run([ATLAS_BIN, "status"], text=True, capture_output=True, env=env)
        finally:
            lock_path.unlink(missing_ok=True)
        self.assertNotEqual(proc.returncode, 0)
        envelope = parse_envelope(proc.stdout)
        self.assertEqual(envelope["REASON_CODE"], "duplicate_dispatch_blocked")
        contract = load_contract(envelope["RESULT_JSON"])
        self.assertEqual(contract["failure_class"], "resource_contention")


if __name__ == "__main__":
    unittest.main()
