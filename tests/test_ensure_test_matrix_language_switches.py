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
assert SPEC is not None
assert SPEC.loader is not None
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
            report.chmod(0o640)
            with (
                patch.object(CHECKER, "REPOSITORY_ROOT", root),
                patch.object(CHECKER, "GENERATED_TEST_MATRIX_REPORTS", (relative,)),
            ):
                self.assertEqual(CHECKER.trusted_report_path(relative), report)
                self.assertEqual(1, CHECKER.rewrite_selected_reports())
            self.assertIn("**Language:** English", report.read_text(encoding="utf-8"))
            self.assertEqual(0o640, report.stat().st_mode & 0o777)

    def test_switch_rendering_preserves_a_single_current_marker(self) -> None:
        rendered = CHECKER.switched_report_text(
            "# Report\n\n**Language:** stale\n\nBody\n",
            "**Language:** English | [Deutsch](report.de.md)",
            "**Language:**",
        )
        self.assertEqual(
            "# Report\n\n**Language:** English | [Deutsch](report.de.md)\n\nBody\n",
            rendered,
        )

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
            with (
                patch.object(CHECKER, "REPOSITORY_ROOT", root),
                patch.object(CHECKER, "GENERATED_TEST_MATRIX_REPORTS", (relative,)),
            ):
                self.assertIsNone(CHECKER.trusted_report_path(relative))
                self.assertEqual(0, CHECKER.rewrite_selected_reports())
            self.assertEqual("# Outside\n", outside.read_text(encoding="utf-8"))

    def test_descriptor_replace_does_not_follow_a_swapped_final_symlink(self) -> None:
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
                CHECKER._replace_selected_report(relative, "# Replacement\n", 0o640)
            self.assertEqual("# Outside\n", outside.read_text(encoding="utf-8"))
            self.assertFalse(candidate.is_symlink())
            self.assertEqual("# Replacement\n", candidate.read_text(encoding="utf-8"))

    def test_descriptor_replace_rejects_traversal_before_opening_a_parent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "checkout"
            with patch.object(CHECKER, "REPOSITORY_ROOT", root):
                with self.assertRaises(ValueError):
                    CHECKER._replace_selected_report(Path("../outside.generated.md"), "# Outside\n", 0o640)

    def test_outside_report_is_not_rewritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root = base / "checkout"
            outside = base / "outside.generated.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            with (
                patch.object(CHECKER, "REPOSITORY_ROOT", root),
                patch.object(CHECKER, "GENERATED_TEST_MATRIX_REPORTS", (Path("../outside.generated.md"),)),
            ):
                self.assertIsNone(CHECKER.trusted_report_path(Path("../outside.generated.md")))
                self.assertEqual(0, CHECKER.rewrite_selected_reports())
            self.assertEqual("# Outside\n", outside.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
