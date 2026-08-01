#!/usr/bin/env python3
"""Regression tests for generated test-matrix report path validation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "ci/checks/documentation/ensure-test-matrix-language-switches.py"
SPEC = importlib.util.spec_from_file_location("ensure_test_matrix_language_switches", SCRIPT)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class EnsureTestMatrixLanguageSwitchesTests(unittest.TestCase):
    def test_regular_in_tree_report_is_selected_and_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            relative = Path("reports/testing/generated/coverage/report.generated.md")
            report = root / relative
            report.parent.mkdir(parents=True)
            report.write_text("# Report\n\nBody\n", encoding="utf-8")
            with patch.object(CHECKER, "REPOSITORY_ROOT", root):
                self.assertEqual(CHECKER.trusted_report_path(relative), report)
                self.assertTrue(CHECKER.ensure_switch(report, "**Language:** English", "**Language:**"))
            self.assertIn("**Language:** English", report.read_text(encoding="utf-8"))

    def test_symlink_report_is_not_selected_or_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "checkout"
            outside = base / "outside.generated.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            relative = Path("reports/testing/generated/coverage/report.generated.md")
            candidate = root / relative
            candidate.parent.mkdir(parents=True)
            candidate.symlink_to(outside)
            with patch.object(CHECKER, "REPOSITORY_ROOT", root):
                self.assertIsNone(CHECKER.trusted_report_path(relative))
                with self.assertRaises(ValueError):
                    CHECKER.ensure_switch(candidate, "**Language:** English", "**Language:**")

    def test_outside_report_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "checkout"
            outside = base / "outside.generated.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            with patch.object(CHECKER, "REPOSITORY_ROOT", root):
                with self.assertRaises(ValueError):
                    CHECKER.ensure_switch(outside, "**Language:** English", "**Language:**")


if __name__ == "__main__":
    unittest.main()
