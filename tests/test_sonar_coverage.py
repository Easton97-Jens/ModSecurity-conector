"""Coverage provenance fails closed before an incomplete report can be imported."""

from __future__ import annotations

from contextlib import redirect_stderr
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sonar_coverage", ROOT / "ci/checks/analysis/run-sonar-coverage.py")
assert SPEC is not None
assert SPEC.loader is not None
COVERAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COVERAGE)


class SonarCoverageTests(unittest.TestCase):
    def write_report(self, directory: str, *, filename: str, hits: str = "1") -> Path:
        report = Path(directory) / "coverage.xml"
        report.write_text(
            f'<coverage><sources><source>.</source></sources><packages><package><classes>'
            f'<class filename="{filename}"><lines><line number="1" hits="{hits}"/></lines>'
            '</class></classes></package></packages></coverage>', encoding="utf-8",
        )
        return report

    def test_accepts_a_measured_repository_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self.write_report(directory, filename="ci/checks/analysis/check-sonar-scope.py")
            self.assertEqual(COVERAGE.validate_python_report(report), 1)

    def test_rejects_external_paths_even_with_execution_counts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self.write_report(directory, filename="../outside.py")
            with self.assertRaisesRegex(ValueError, "not a repository file"):
                COVERAGE.validate_python_report(report)

    def test_rejects_a_report_without_actual_execution(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = self.write_report(directory, filename="ci/checks/analysis/check-sonar-scope.py", hits="0")
            with self.assertRaisesRegex(ValueError, "no measured execution"):
                COVERAGE.validate_python_report(report)

    def test_rejects_stale_report_directory_before_starting_tests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "python").mkdir()
            stale = Path(directory) / "python/python.xml"
            stale.write_text("old revision\n", encoding="utf-8")
            arguments = ["coverage", "--language", "python", "--output-root", directory,
                         "--temp-root", directory]
            with (mock.patch("sys.argv", arguments), mock.patch.object(COVERAGE, "run") as run,
                  redirect_stderr(io.StringIO())):
                self.assertEqual(COVERAGE.main(), 1)
            run.assert_not_called()
            self.assertEqual(stale.read_text(encoding="utf-8"), "old revision\n")

    def test_native_notes_without_execution_counters_are_not_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build = output / "build/common-helper-smoke"
            build.mkdir(parents=True)
            (build / "stale.gcno").write_bytes(b"compile notes without execution")
            with mock.patch.object(COVERAGE, "run"):
                with self.assertRaisesRegex(ValueError, "no execution counters"):
                    COVERAGE.native_coverage(output, {})

    def test_finalization_rejects_other_revision_before_combining_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for language in ("python", "go", "native"):
                (root / language).mkdir()
                (root / language / "manifest.json").write_text(
                    json.dumps({"revision": "a" * 40, "uncommitted_changes": False}),
                    encoding="utf-8",
                )
            with mock.patch.object(COVERAGE, "publish_python_report") as publish:
                with self.assertRaisesRegex(ValueError, "revision does not match"):
                    COVERAGE.finalize_python(root, {}, "b" * 40)
            publish.assert_not_called()


if __name__ == "__main__":
    unittest.main()
