import json
import tempfile
import unittest
from pathlib import Path

from studio_test_runner.regression import compare_snapshots


class RegressionTests(unittest.TestCase):
    def test_detects_pass_to_fail_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = root / "baseline.json"
            candidate = root / "candidate.json"
            baseline.write_text(json.dumps({"results":[{"assertion_id":"a","passed":True}]}), encoding="utf-8")
            candidate.write_text(json.dumps({"results":[{"assertion_id":"a","passed":False}]}), encoding="utf-8")
            result = compare_snapshots(baseline, candidate)
            self.assertEqual(["a"], result["regressions"])
            self.assertFalse(result["passed"])


if __name__ == "__main__":
    unittest.main()
