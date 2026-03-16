import tempfile
import unittest
from pathlib import Path

from lib.atlas_validation_contract import load_contract, validate_result, write_contract


class AtlasValidationContractTests(unittest.TestCase):
    def test_valid_contract_round_trip(self):
        payload = {
            "mission_id": "mis_test",
            "dispatch_id": "disp_test",
            "project_id": "proj_test",
            "attempt_id": "atlas-1",
            "run_dir": "/tmp/run",
            "summary_file": "/tmp/run/summary.txt",
            "overall": "PASS",
            "recommendation": "new_test",
        }
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "atlas_validation.json"
            write_contract(path, payload)
            loaded = load_contract(path)
        self.assertEqual(loaded["attempt_id"], "atlas-1")
        self.assertEqual(loaded["overall"], "PASS")

    def test_fail_requires_reason_fields(self):
        with self.assertRaises(ValueError):
            validate_result(
                {
                    "attempt_id": "atlas-1",
                    "run_dir": "/tmp/run",
                    "summary_file": "/tmp/run/summary.txt",
                    "overall": "FAIL",
                    "recommendation": "stop",
                }
            )

    def test_invalid_failure_class_rejected(self):
        with self.assertRaises(ValueError):
            validate_result(
                {
                    "attempt_id": "atlas-1",
                    "run_dir": "/tmp/run",
                    "summary_file": "/tmp/run/summary.txt",
                    "overall": "FAIL",
                    "recommendation": "stop",
                    "reason_code": "atlas_step_failed",
                    "terminal_reason": "atlas_step_failed",
                    "failure_class": "made_up",
                }
            )


if __name__ == "__main__":
    unittest.main()
