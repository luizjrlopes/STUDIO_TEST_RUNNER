import tempfile
import unittest
from pathlib import Path

from studio_test_runner.discovery import discover_tree


class DiscoveryTests(unittest.TestCase):
    def test_discovers_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".studio").mkdir()
            (root / ".studio" / "x.json").write_text("{}", encoding="utf-8")
            tree = discover_tree(root)
            self.assertIn(".studio", tree.directories)
            self.assertIn(".studio/x.json", tree.files)


if __name__ == "__main__":
    unittest.main()
