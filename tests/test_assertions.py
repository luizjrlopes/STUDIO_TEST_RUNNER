import unittest
from pathlib import Path

from studio_test_runner.discovery import discover_tree
from studio_test_runner.assertions import evaluate_assertion

ROOT = Path(__file__).resolve().parents[1]


class AssertionTests(unittest.TestCase):
    def test_valid_fixture_allows_specialist_report(self):
        tree = discover_tree(ROOT / "fixtures" / "valid")
        result = evaluate_assertion(tree, {"id": "scope", "type": "specialist_write_scope"}, 1)
        self.assertTrue(result.passed, result.message)

    def test_invalid_fixture_rejects_specialist_state_write(self):
        tree = discover_tree(ROOT / "fixtures" / "invalid_specialist_write")
        result = evaluate_assertion(tree, {"id": "scope", "type": "specialist_write_scope"}, 1)
        self.assertFalse(result.passed)
        self.assertTrue(any("state/current.json" in (e.path or "") for e in result.evidence))

    def test_super_owner_cross_area_write_is_rejected(self):
        tree = discover_tree(ROOT / "fixtures" / "invalid_owner_cross_area")
        result = evaluate_assertion(tree, {"id": "ownership", "type": "owner_cross_area_write"}, 1)
        self.assertFalse(result.passed)


if __name__ == "__main__":
    unittest.main()
