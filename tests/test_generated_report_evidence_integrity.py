import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "ci/checks/documentation/check-generated-report-layout.py"
SPEC = importlib.util.spec_from_file_location("generated_report_layout", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
GENERATOR_PATH = ROOT / "ci/evidence/reports/generate-full-matrix-job-completeness.py"
GENERATOR_SPEC = importlib.util.spec_from_file_location("full_matrix_completeness", GENERATOR_PATH)
assert GENERATOR_SPEC is not None and GENERATOR_SPEC.loader is not None
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(GENERATOR)
REFRESH_PATH = ROOT / "ci/evidence/reports/refresh-connector-reports.py"
REFRESH_SPEC = importlib.util.spec_from_file_location("refresh_connector_reports", REFRESH_PATH)
assert REFRESH_SPEC is not None and REFRESH_SPEC.loader is not None
REFRESH = importlib.util.module_from_spec(REFRESH_SPEC)
sys.modules[REFRESH_SPEC.name] = REFRESH
REFRESH_SPEC.loader.exec_module(REFRESH)
RUNNER_PATH = ROOT / "ci/runtime/lifecycle/run-verified-report-run.py"
RUNNER_SPEC = importlib.util.spec_from_file_location("verified_report_runner", RUNNER_PATH)
assert RUNNER_SPEC is not None and RUNNER_SPEC.loader is not None
RUNNER = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(RUNNER)

CONNECTORS = ("apache", "nginx", "haproxy")
CRS_VARIANTS = ("no-crs", "with-crs")
MRTS_VARIANTS = ("no-mrts", "with-mrts")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def replace_raw_matrix_job(matrix_manifest: Path, job: dict[str, object]) -> None:
    rows = [json.loads(line) for line in matrix_manifest.read_text(encoding="utf-8").splitlines() if line]
    for index, row in enumerate(rows):
        if row.get("job_id") == job["job_id"]:
            rows[index] = job
            matrix_manifest.write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )
            return
    raise AssertionError(f"raw matrix job not found: {job['job_id']}")


class GeneratedReportEvidenceIntegrityTests(unittest.TestCase):
    def build_valid_run(self, root: Path) -> tuple[Path, Path, str]:
        connector_root = root / "connector"
        build_root = root / "build"
        run_id = "verified-run-20260718"
        commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
        commands = {
            "verified_run_id": run_id,
            "commands": [
                {
                    "logical_target": "full-matrix-parallel",
                    "phase": "runtime-producers",
                    "required": True,
                    "runtime_complete": True,
                    "runtime_status": "runtime_completed",
                }
            ],
        }
        write_json(commands_path, commands)

        rows = []
        matrix_root = build_root / "full-matrix"
        for connector, crs, mrts in product(CONNECTORS, CRS_VARIANTS, MRTS_VARIANTS):
            job_root = matrix_root / crs / mrts / connector
            log_path = job_root / "run.log"
            build_manifest = job_root / "build-manifest.json"
            summary_path = job_root / "results" / "force-all" / f"{connector}-summary.json"
            results_jsonl = job_root / "results" / "force-all" / f"{connector}-results.jsonl"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text("runtime process and traffic receipt\n", encoding="utf-8")
            write_json(build_manifest, {"connector": connector, "verified_run_id": run_id})
            write_json(summary_path, {connector: {"cases": {"control": {"status": "pass"}}}})
            results_jsonl.write_text(
                json.dumps({"connector": connector, "verified_run_id": run_id, "status": "pass"}) + "\n",
                encoding="utf-8",
            )
            job_path = job_root / "job.json"
            job = {
                "connector": connector,
                "job_id": f"{connector}:{crs}:{mrts}",
                "verified_run_id": run_id,
                "test_variant": crs,
                "mrts_variant": mrts,
                "return_code": 0,
                "status": "completed",
                "started_at": "2026-07-18T00:00:00Z",
                "ended_at": "2026-07-18T00:00:01Z",
                "duration_seconds": 1,
                "results_dir": str(job_root / "results"),
                "summary_path": str(summary_path),
                "log_path": str(log_path),
                "hashes": {
                    "log": sha256(log_path),
                    "summary": sha256(summary_path),
                    "build_manifest": sha256(build_manifest),
                    "results_jsonl": sha256(results_jsonl),
                },
                "inputs": {"build_manifest": str(build_manifest)},
                "outputs": {
                    "job_json": str(job_path),
                    "log": str(log_path),
                    "summary": str(summary_path),
                    "results_dir": str(job_root / "results"),
                    "results_jsonl": str(results_jsonl),
                },
            }
            write_json(job_path, job)
            rows.append(job)

        raw_manifest = matrix_root / "full-runtime-matrix-runs.jsonl"
        raw_manifest.parent.mkdir(parents=True, exist_ok=True)
        raw_manifest.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
            encoding="utf-8",
        )
        verified_manifest = {
            "verified_run_id": run_id,
            "profile": "full",
            "command_file": {
                "path": str(commands_path),
                "status": "present",
                "sha256": sha256(commands_path),
                "bytes": commands_path.stat().st_size,
            },
            "full_matrix_job_completeness": {"complete_jobs": 12, "missing_jobs": []},
        }
        write_json(
            connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json",
            verified_manifest,
        )
        return connector_root, build_root, run_id

    def assert_chain_rejected(self, connector_root: Path, build_root: Path, expected: str) -> None:
        errors: list[str] = []
        CHECKER.check_verified_runtime_artifact_chain(
            connector_root,
            errors,
            build_root=build_root,
        )
        self.assertTrue(errors, "expected strict artifact-chain rejection")
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_valid_full_matrix_control_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            errors: list[str] = []
            CHECKER.check_verified_runtime_artifact_chain(
                connector_root,
                errors,
                build_root=build_root,
            )
        self.assertEqual([], errors)

    def test_report_without_runtime_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            (build_root / "full-matrix" / "full-runtime-matrix-runs.jsonl").unlink()
            self.assert_chain_rejected(connector_root, build_root, "full runtime matrix manifest is missing")

    def test_tampered_result_file_checksum_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            results = build_root / "full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl"
            results.write_text('{"connector":"apache","status":"pass"}\nforged\n', encoding="utf-8")
            self.assert_chain_rejected(connector_root, build_root, "results_jsonl hash mismatch")

    def test_incomplete_run_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job.pop("ended_at")
            write_json(job_path, job)
            self.assert_chain_rejected(connector_root, build_root, "missing ended_at")

    def test_foreign_run_id_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["verified_run_id"] = "foreign-run"
            write_json(job_path, job)
            self.assert_chain_rejected(connector_root, build_root, "verified_run_id")

    def test_copied_connector_result_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["connector"] = "nginx"
            write_json(job_path, job)
            self.assert_chain_rejected(connector_root, build_root, "connector mismatch")

    def test_copied_profile_result_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["test_variant"] = "with-crs"
            write_json(job_path, job)
            self.assert_chain_rejected(connector_root, build_root, "test_variant mismatch")

    def test_path_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            escaped = root / "escaped-summary.json"
            write_json(escaped, {"apache": {"cases": {"control": {"status": "pass"}}}})
            job["summary_path"] = str(escaped)
            job["outputs"]["summary"] = str(escaped)
            job["hashes"]["summary"] = sha256(escaped)
            write_json(job_path, job)
            self.assert_chain_rejected(connector_root, build_root, "summary path is not canonical")

    def test_direct_summary_path_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            direct_summary_path = job_path.parent / "results/apache-summary.json"
            write_json(direct_summary_path, {"apache": {"cases": {"direct": {"status": "pass"}}}})
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["summary_path"] = str(direct_summary_path)
            job["outputs"]["summary"] = str(direct_summary_path)
            job["hashes"]["summary"] = sha256(direct_summary_path)
            write_json(job_path, job)
            replace_raw_matrix_job(build_root / "full-matrix/full-runtime-matrix-runs.jsonl", job)
            errors: list[str] = []
            CHECKER.check_verified_runtime_artifact_chain(
                connector_root,
                errors,
                build_root=build_root,
            )
        self.assertEqual([], errors)

    def test_force_all_summary_is_selected_when_direct_summary_exists(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            direct_summary_path = build_root / "full-matrix/no-crs/no-mrts/apache/results/apache-summary.json"
            write_json(direct_summary_path, {"apache": {"cases": {}}})
            errors: list[str] = []
            CHECKER.check_verified_runtime_artifact_chain(
                connector_root,
                errors,
                build_root=build_root,
            )
        self.assertEqual([], errors)

    def test_summary_hash_mismatch_is_rejected_for_each_canonical_path(self) -> None:
        for location in ("direct", "force-all"):
            with self.subTest(location=location), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                connector_root, build_root, _ = self.build_valid_run(root)
                job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
                job = json.loads(job_path.read_text(encoding="utf-8"))
                if location == "direct":
                    direct_summary_path = job_path.parent / "results/apache-summary.json"
                    write_json(direct_summary_path, {"apache": {"cases": {"direct": {"status": "pass"}}}})
                    job["summary_path"] = str(direct_summary_path)
                    job["outputs"]["summary"] = str(direct_summary_path)
                job["hashes"]["summary"] = "a" * 64
                write_json(job_path, job)
                replace_raw_matrix_job(build_root / "full-matrix/full-runtime-matrix-runs.jsonl", job)
                self.assert_chain_rejected(connector_root, build_root, "summary hash mismatch")

    def test_symlinked_result_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            results_dir = build_root / "full-matrix/no-crs/no-mrts/apache/results"
            escaped_results = root / "escaped-results"
            results_dir.rename(escaped_results)
            results_dir.symlink_to(escaped_results, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "results_dir is not canonical")

    def test_intermediate_full_matrix_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            matrix_root = build_root / "full-matrix"
            escaped_matrix = root / "escaped-matrix"
            matrix_root.rename(escaped_matrix)
            matrix_root.symlink_to(escaped_matrix, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "full runtime matrix manifest is missing or not regular")

    def test_intermediate_verified_runs_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            verified_runs = build_root / "verified-runs"
            escaped_runs = root / "escaped-verified-runs"
            verified_runs.rename(escaped_runs)
            verified_runs.symlink_to(escaped_runs, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "verified command receipt is missing or not regular")

    def test_critical_missing_report_input_is_rejected_in_strict_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "missing",
                        "inputs": [],
                        "missing_inputs": ["full-runtime-matrix-runs.jsonl"],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("has missing input_status" in error for error in errors), errors)

    def test_critical_unrecognized_report_input_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "forged-success",
                        "inputs": [],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("forged-success input_status" in error for error in errors), errors)

    def test_critical_manifest_unrecognized_input_record_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [{"path": "forged.json", "status": "forged-success"}],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("critical report input is forged-success" in error for error in errors), errors)

    def test_critical_manifest_present_input_record_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            input_path = connector_root / "runtime.json"
            write_json(input_path, {"runtime": "receipt"})
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [{"path": "runtime.json", "status": "present", "sha256": sha256(input_path)}],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertEqual([], errors)

    def test_critical_manifest_parent_traversal_receipts_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            build_root = root / "build"
            framework_root = root / "framework"
            external_input = root / "outside-runtime.json"
            connector_root.mkdir()
            build_root.mkdir()
            framework_root.mkdir()
            write_json(external_input, {"runtime": "outside trusted roots"})
            for input_reference in (
                "BUILD_ROOT:../outside-runtime.json",
                "framework:../outside-runtime.json",
                "../outside-runtime.json",
            ):
                with self.subTest(input_reference=input_reference):
                    refresh_manifest = {
                        "reports": [
                            {
                                "report_name": "full_runtime_matrix",
                                "status": "generated",
                                "output_files": [],
                                "category": "runtime",
                                "kind": "report",
                                "owner": "parent",
                                "severity": "critical",
                                "input_status": "complete",
                                "inputs": [
                                    {
                                        "path": input_reference,
                                        "status": "present",
                                        "sha256": sha256(external_input),
                                    }
                                ],
                                "missing_inputs": [],
                                "empty_inputs": [],
                                "unknown_inputs": [],
                                "stale_inputs": [],
                            }
                        ]
                    }
                    write_json(
                        connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                        refresh_manifest,
                    )
                    errors: list[str] = []
                    CHECKER.check_manifest(
                        connector_root,
                        errors,
                        strict_evidence=True,
                        build_root=build_root,
                        framework_root=framework_root,
                    )
                    self.assertTrue(
                        any("input is not a trusted regular file" in error for error in errors),
                        errors,
                    )

    def test_critical_manifest_present_input_hash_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            input_path = connector_root / "runtime.json"
            write_json(input_path, {"runtime": "original receipt"})
            declared_hash = sha256(input_path)
            write_json(input_path, {"runtime": "substituted receipt"})
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [{"path": "runtime.json", "status": "present", "sha256": declared_hash}],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("critical report input hash mismatch: runtime.json" in error for error in errors), errors)

    def test_critical_manifest_missing_present_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [{"path": "missing-runtime.json", "status": "present", "sha256": "a" * 64}],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("input is not a trusted regular file" in error for error in errors), errors)

    def test_critical_manifest_empty_input_receipts_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("has no direct input receipts" in error for error in errors), errors)

    def test_critical_manifest_symlinked_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary) / "connector"
            external_input = Path(temporary) / "external-runtime.json"
            write_json(external_input, {"runtime": "receipt"})
            connector_root.mkdir(parents=True)
            (connector_root / "runtime.json").symlink_to(external_input)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [{"path": "runtime.json", "status": "present", "sha256": sha256(external_input)}],
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("input is not a trusted regular file" in error for error in errors), errors)

    def test_critical_manifest_non_list_inputs_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": {"path": "forged.json", "status": "forged-success"},
                        "missing_inputs": [],
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("inputs must be a list" in error for error in errors), errors)

    def test_critical_manifest_non_list_aggregate_input_array_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            refresh_manifest = {
                "reports": [
                    {
                        "report_name": "full_runtime_matrix",
                        "status": "generated",
                        "output_files": [],
                        "category": "runtime",
                        "kind": "report",
                        "owner": "parent",
                        "severity": "critical",
                        "input_status": "complete",
                        "inputs": [],
                        "missing_inputs": {"forged": True},
                        "empty_inputs": [],
                        "unknown_inputs": [],
                        "stale_inputs": [],
                    }
                ]
            }
            write_json(
                connector_root / "reports/testing/generated/manifest/report-refresh-manifest.generated.json",
                refresh_manifest,
            )
            errors: list[str] = []
            CHECKER.check_manifest(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("missing_inputs must be a list" in error for error in errors), errors)

    def test_critical_metadata_unrecognized_input_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            report_path = CHECKER.report_path(connector_root, "full_runtime_matrix", "json")
            write_json(
                report_path,
                {
                    "metadata": {
                        "verified_run_id": "verified-run-20260718",
                        "connector_sha": "a" * 40,
                        "framework_sha": "b" * 40,
                        "input_status": "forged-success",
                        "inputs": [],
                    }
                },
            )
            errors: list[str] = []
            CHECKER.check_critical_report_run_consistency(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("metadata.input_status is forged-success" in error for error in errors), errors)

    def test_critical_metadata_unrecognized_input_record_status_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            report_path = CHECKER.report_path(connector_root, "full_runtime_matrix", "json")
            write_json(
                report_path,
                {
                    "metadata": {
                        "verified_run_id": "verified-run-20260718",
                        "connector_sha": "a" * 40,
                        "framework_sha": "b" * 40,
                        "input_status": "complete",
                        "inputs": [{"path": "runtime-receipt.json", "status": "forged-success"}],
                    }
                },
            )
            errors: list[str] = []
            CHECKER.check_critical_report_run_consistency(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("critical report input is forged-success" in error for error in errors), errors)

    def test_critical_metadata_present_input_record_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            input_path = connector_root / "runtime-receipt.json"
            write_json(input_path, {"runtime": "receipt"})
            report_path = CHECKER.report_path(connector_root, "full_runtime_matrix", "json")
            write_json(
                report_path,
                {
                    "metadata": {
                        "verified_run_id": "verified-run-20260718",
                        "connector_sha": "a" * 40,
                        "framework_sha": "b" * 40,
                        "input_status": "complete",
                        "inputs": [{"path": "runtime-receipt.json", "status": "present", "sha256": sha256(input_path)}],
                    }
                },
            )
            errors: list[str] = []
            CHECKER.check_critical_report_run_consistency(connector_root, errors, strict_evidence=True)
        self.assertEqual([], errors)

    def test_critical_metadata_input_hash_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            input_path = connector_root / "runtime-receipt.json"
            write_json(input_path, {"runtime": "receipt"})
            report_path = CHECKER.report_path(connector_root, "full_runtime_matrix", "json")
            write_json(
                report_path,
                {
                    "metadata": {
                        "verified_run_id": "verified-run-20260718",
                        "connector_sha": "a" * 40,
                        "framework_sha": "b" * 40,
                        "input_status": "complete",
                        "inputs": [{"path": "runtime-receipt.json", "status": "present", "sha256": "a" * 64}],
                    }
                },
            )
            errors: list[str] = []
            CHECKER.check_critical_report_run_consistency(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("input hash mismatch" in error for error in errors), errors)

    def test_critical_metadata_non_list_inputs_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            report_path = CHECKER.report_path(connector_root, "full_runtime_matrix", "json")
            write_json(
                report_path,
                {
                    "metadata": {
                        "verified_run_id": "verified-run-20260718",
                        "connector_sha": "a" * 40,
                        "framework_sha": "b" * 40,
                        "input_status": "complete",
                        "inputs": {"path": "forged.json", "status": "forged-success"},
                    }
                },
            )
            errors: list[str] = []
            CHECKER.check_critical_report_run_consistency(connector_root, errors, strict_evidence=True)
        self.assertTrue(any("critical report metadata: inputs must be a list" in error for error in errors), errors)

    def test_self_generated_refresh_status_is_the_only_non_complete_exception(self) -> None:
        self.assertFalse(
            CHECKER.is_unverified_critical_input_status(
                "self_generated_no_direct_input",
                report_name="report_refresh_manifest",
            )
        )
        self.assertTrue(
            CHECKER.is_unverified_critical_input_status(
                "self_generated_no_direct_input",
                report_name="full_runtime_matrix",
            )
        )

    def test_full_matrix_job_counts_prefer_summary_and_fall_back_to_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            summary_path = root / "apache-summary.json"
            jsonl_path = root / "apache-results.jsonl"
            write_json(summary_path, {"apache": {"attempted": 1, "cases": {"control": {"status": "pass"}}}})
            jsonl_path.write_text(json.dumps({"status": "fail"}) + "\n", encoding="utf-8")
            summary_counts, selected_summary = GENERATOR.job_case_counts(summary_path, jsonl_path, "apache")
            summary_path.unlink()
            jsonl_counts, selected_jsonl = GENERATOR.job_case_counts(summary_path, jsonl_path, "apache")

        self.assertEqual(summary_path, selected_summary)
        self.assertEqual("summary_json", summary_counts["source"])
        self.assertEqual(jsonl_path, selected_jsonl)
        self.assertEqual("results_jsonl", jsonl_counts["source"])

    def test_rewritten_raw_manifest_preserves_identity_and_artifact_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            manifest_path = Path(temporary) / "full-runtime-matrix-runs.jsonl"
            job = {
                "connector": "apache",
                "job_id": "apache:no-crs:no-mrts",
                "verified_run_id": "verified-run-20260718",
                "crs": "no-crs",
                "mrts": "no-mrts",
                "status": "completed",
                "return_code": 0,
                "started_at": "2026-07-18T00:00:00Z",
                "ended_at": "2026-07-18T00:00:01Z",
                "duration_seconds": 1,
                "job_path": str(Path(temporary) / "no-crs/no-mrts/apache/job.json"),
                "summary_path": str(Path(temporary) / "no-crs/no-mrts/apache/results/force-all/apache-summary.json"),
                "log_path": str(Path(temporary) / "no-crs/no-mrts/apache/run.log"),
                "hashes": {"log": "log", "summary": "summary", "build_manifest": "build", "results_jsonl": "results"},
                "inputs": {"build_manifest": str(Path(temporary) / "build-manifest.json")},
                "outputs": {"results_jsonl": str(Path(temporary) / "results.jsonl")},
            }
            GENERATOR.rewrite_manifest(manifest_path, [job])
            row = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertEqual("verified-run-20260718", row["verified_run_id"])
        self.assertEqual("apache:no-crs:no-mrts", row["job_id"])
        self.assertEqual(job["hashes"], row["hashes"])
        self.assertEqual(job["inputs"], row["inputs"])
        self.assertEqual(job["outputs"], row["outputs"])
        self.assertEqual("completed", row["status"])

    def test_governance_record_emits_typed_input_status_arrays(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            input_path = connector_root / "runtime-input.json"
            input_path.write_text("{}\n", encoding="utf-8")
            record = REFRESH.build_governance_record(
                "full_runtime_matrix",
                connector_root,
                connector_root,
                connector_root / "build",
                "2026-07-18T00:00:00Z",
                (str(input_path),),
            )

        self.assertEqual("complete", record["input_status"])
        for key in ("missing_inputs", "empty_inputs", "unknown_inputs", "stale_inputs"):
            self.assertIsInstance(record[key], list)

    def test_verified_manifest_does_not_hash_its_own_overwritten_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root = Path(temporary)
            generated = connector_root / "reports/testing/generated"
            manifest = generated / "manifest"
            manifest.mkdir(parents=True)
            (manifest / "verified-run-manifest.generated.json").write_text("{}\n", encoding="utf-8")
            (manifest / "verified-run-manifest.generated.md").write_text("# stale self record\n", encoding="utf-8")
            detached = generated / "canonical/full-runtime-matrix.generated.json"
            detached.parent.mkdir(parents=True)
            detached.write_text("{}\n", encoding="utf-8")
            records = RUNNER.generated_output_records(connector_root)

        recorded_names = {Path(str(record["path"])).name for record in records}
        self.assertIn("full-runtime-matrix.generated.json", recorded_names)
        self.assertNotIn("verified-run-manifest.generated.json", recorded_names)
        self.assertNotIn("verified-run-manifest.generated.md", recorded_names)


if __name__ == "__main__":
    unittest.main()
