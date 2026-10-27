"""Tests for the source-backed logical connector example matrix."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from shutil import copytree


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci/checks/documentation/check-logical-connector-example-matrix.py"
SPEC = importlib.util.spec_from_file_location("logical_connector_example_matrix", CHECKER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class LogicalConnectorExampleMatrixTests(unittest.TestCase):
    def test_repository_has_all_profiles_and_variants(self) -> None:
        self.assertEqual(CHECKER.logical_connector_example_errors(ROOT), [])

    def test_missing_companion_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            copytree(ROOT / "examples", root / "examples")
            (root / "examples/haproxy/spoe-spop/minimal/spoa-agent.conf").unlink()
            errors = CHECKER.logical_connector_example_errors(root)
            matching_errors = [error for error in errors if "haproxy-spoe-spop/minimal" in error]
            self.assertEqual(len(matching_errors), 1)
            self.assertIn("spoa-agent.conf", matching_errors[0])



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
