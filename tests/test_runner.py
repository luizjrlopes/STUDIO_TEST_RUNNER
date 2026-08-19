import unittest
from pathlib import Path

from studio_test_runner.scenarios import load_suite, run_suite

ROOT = Path(__file__).resolve().parents[1]


class RunnerTests(unittest.TestCase):
    def test_orchestration_suite_passes_valid_fixture(self):
        suite = load_suite(ROOT / "suites" / "orchestration-core.json")
        result = run_suite(ROOT / "fixtures" / "valid", suite)
        self.assertTrue(result.passed, [x.message for x in result.results if not x.passed])

    def test_scope_suite_fails_invalid_fixture(self):
        suite = load_suite(ROOT / "suites" / "specialist-scope.json")
        result = run_suite(ROOT / "fixtures" / "invalid_specialist_write", suite)
        self.assertFalse(result.passed)


if __name__ == "__main__":
    unittest.main()
