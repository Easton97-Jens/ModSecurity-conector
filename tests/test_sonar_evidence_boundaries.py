"""Protect evidence consumers from paths selected by stored JSON records."""

from __future__ import annotations

import importlib.util
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "ci/runtime/lifecycle" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


RUNNER = load("sonar_verified_report_boundaries", "run-verified-report-run.py")
NATIVE = load("sonar_native_report_boundaries", "run-native-case-comparison.py")
TARGET = "full-matrix-job:apache:no-crs:no-mrts"


class SonarEvidenceBoundaryTests(unittest.TestCase):
    def job(self, temporary: str) -> tuple[Path, Path, Path]:
        base = Path(temporary)
        matrix = base / "matrix"
        job = matrix / "no-crs/no-mrts/apache"
        results = job / "results/force-all"
        results.mkdir(parents=True)
        summary = results / "apache-summary.json"
        summary.write_text(json.dumps({"apache": {"cases": {"control": {}}}}), encoding="utf-8")
        (results / "apache-results.jsonl").write_text("{}\n", encoding="utf-8")
        self.write_job(job, summary)
        return matrix, job, summary

    def write_job(self, job: Path, summary: Path) -> None:
        (job / "job.json").write_text(json.dumps({
            "summary_path": str(summary), "ended_at": "2026-10-25T00:00:00Z",
            "status": "completed", "return_code": 0,
        }), encoding="utf-8")

    def test_private_job_summary_still_proves_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            matrix, _, summary = self.job(temporary)
            result = RUNNER.full_matrix_job_artifacts({"MATRIX_ROOT": str(matrix)}, TARGET)
            self.assertTrue(result["complete"])
            self.assertEqual(result["summary_cases"], 1)
            self.assertEqual(result["summary_path"], str(summary))

    def test_stored_summary_cannot_read_outside_private_job(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            matrix, job, _ = self.job(temporary)
            outside = Path(temporary) / "outside.json"
            outside.write_text('{"apache":{"cases":{"forged":{}}}}', encoding="utf-8")
            self.write_job(job, outside)
            with self.assertRaises(ValueError):
                RUNNER.full_matrix_job_artifacts({"MATRIX_ROOT": str(matrix)}, TARGET)

    def test_stored_summary_cannot_follow_a_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            matrix, job, summary = self.job(temporary)
            outside = Path(temporary) / "outside.json"
            outside.write_text('{"apache":{"cases":{"forged":{}}}}', encoding="utf-8")
            summary.unlink()
            summary.symlink_to(outside)
            with self.assertRaises(ValueError):
                RUNNER.full_matrix_job_artifacts({"MATRIX_ROOT": str(matrix)}, TARGET)

    def test_refresh_uses_only_the_invocations_log_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            logs = root / "logs"
            logs.mkdir()
            inside = logs / "refresh.log"
            outside = root / "other.log"
            inside.write_text("SKIPPED_STALE_INPUT\n", encoding="utf-8")
            outside.write_text("SKIPPED_STALE_INPUT\n", encoding="utf-8")
            env = {"VERIFIED_RUN_LOG_ROOT": str(logs)}
            def result(path):
                return RUNNER.apply_command_semantics({
                    "logical_target": "refresh-all-reports", "return_code": 1,
                    "log_path": str(path),
                }, env, "full")["refresh_status"]
            self.assertEqual(result(inside), "consumer_stale")
            self.assertEqual(result(outside), "refresh_failed")

    def test_latest_native_record_retains_its_actual_loaded_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "native-case-runs/20261025-control"
            run.mkdir(parents=True)
            (run / NATIVE.NATIVE_CASE_RUN_FILENAME).write_text(json.dumps({
                "case": "control", "run_dir": "/untrusted/location", "status": "blocked",
            }), encoding="utf-8")
            result = NATIVE.latest_case_runs(root, ("control",))
            self.assertEqual(result[0]["run_dir"], str(run))

    def test_supplied_native_records_cannot_authorize_external_metadata_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            verified = root / "verified"
            verified.mkdir()
            outside = root / "outside"
            outside.mkdir()
            (outside / NATIVE.NATIVE_CASE_RUN_FILENAME).write_text("{}", encoding="utf-8")
            report = {"case": "control", "run_dir": str(outside), "status": "blocked"}
            with mock.patch.object(NATIVE, "refresh_official_context", side_effect=lambda _, rows: rows):
                with self.assertRaises(ValueError):
                    NATIVE.write_summary_report(ROOT, root / "framework", verified,
                                                ("control",), [report], root / "summary")

    def test_native_metadata_uses_fixture_identity_and_confined_record_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            framework = root / "framework"
            fixture = framework / "tests/cases/control.yaml"
            fixture.parent.mkdir(parents=True)
            fixture.write_text("name: control\n", encoding="utf-8")
            verified = root / "verified"
            run = verified / "native-case-runs/20261025-control"
            run.mkdir(parents=True)
            contents = b'{"case":"control","status":"blocked"}\r\n'
            run_json = run / NATIVE.NATIVE_CASE_RUN_FILENAME
            run_json.write_bytes(contents)
            reports = [{"case": "control", "case_path": "/untrusted/fixture.yaml",
                        "run_dir": str(run), "status": "blocked"}]
            with (
                mock.patch.object(NATIVE, "refresh_official_context", side_effect=lambda _, rows: rows),
                mock.patch.object(NATIVE, "build_metadata", wraps=NATIVE.build_metadata) as build,
            ):
                result = NATIVE.write_summary_report(ROOT, framework, verified, ("control",),
                                                     reports, root / "summary")
            self.assertTrue(Path(result["json"]).is_file())
            self.assertIn(fixture, build.call_args.kwargs["inputs"])
            self.assertNotIn("/untrusted/fixture.yaml", build.call_args.kwargs["inputs"])
            metadata = json.loads(Path(result["json"]).read_text(encoding="utf-8"))["metadata"]
            record = next(item for item in metadata["inputs"] if item["path"] == str(run_json))
            self.assertEqual(record["sha256"], hashlib.sha256(contents).hexdigest())

    def test_latest_native_record_does_not_follow_a_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "native-case-runs/20261025-control"
            run.mkdir(parents=True)
            outside = root / "outside.json"
            outside.write_text('{"case":"control"}', encoding="utf-8")
            (run / NATIVE.NATIVE_CASE_RUN_FILENAME).symlink_to(outside)
            with self.assertRaises(ValueError):
                NATIVE.latest_case_runs(root, ("control",))


if __name__ == "__main__":
    unittest.main()
