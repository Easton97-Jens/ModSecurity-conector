import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from copy import deepcopy
from itertools import product
from pathlib import Path
from unittest import mock


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
RECEIPT_PATH = ROOT / "ci/lib/verified_full_matrix_receipt.py"
RECEIPT_SPEC = importlib.util.spec_from_file_location("verified_full_matrix_receipt_test", RECEIPT_PATH)
assert RECEIPT_SPEC is not None and RECEIPT_SPEC.loader is not None
RECEIPT = importlib.util.module_from_spec(RECEIPT_SPEC)
sys.modules[RECEIPT_SPEC.name] = RECEIPT
RECEIPT_SPEC.loader.exec_module(RECEIPT)

CONNECTORS = ("apache", "nginx", "haproxy")
CRS_VARIANTS = ("no-crs", "with-crs")
MRTS_VARIANTS = ("no-mrts", "with-mrts")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def replace_raw_matrix_job(
    rows: list[dict[str, object]], matrix_manifest: Path, job: dict[str, object]
) -> None:
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
                    "return_code": 0,
                    "classification": "success",
                    "runtime_complete": True,
                    "runtime_status": "runtime_completed",
                    "started_at": "2026-07-18T00:00:00Z",
                    "finished_at": "2026-07-18T00:00:01Z",
                }
            ],
        }
        write_json(commands_path, commands)

        rows = []
        matrix_root = build_root / "full-matrix"
        for crs, mrts in product(CRS_VARIANTS, MRTS_VARIANTS):
            for connector in CONNECTORS:
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
        self.raw_matrix_rows = rows
        revisions = {
            "connector_sha": "a" * 40,
            "framework_sha": "b" * 40,
            "mrts_sha": "c" * 40,
        }
        aggregate_path = RECEIPT.seal_full_matrix_aggregate_receipt(
            build_root=build_root,
            verified_run_id=run_id,
            profile="full",
            parent_command=commands["commands"][0],
            revisions=revisions,
        )
        verified_manifest = {
            "verified_run_id": run_id,
            "profile": "full",
            **revisions,
            "command_file": {
                "path": str(commands_path),
                "status": "present",
                "sha256": sha256(commands_path),
                "bytes": commands_path.stat().st_size,
            },
            "full_matrix_aggregate_receipt": {
                "path": str(aggregate_path),
                "status": "present",
                "sha256": sha256(aggregate_path),
                "bytes": aggregate_path.stat().st_size,
            },
            "full_matrix_job_completeness": {"complete_jobs": 12, "missing_jobs": []},
        }
        write_json(
            connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json",
            verified_manifest,
        )
        return connector_root, build_root, run_id

    def raw_matrix_job(self, job_id: str) -> dict[str, object]:
        for row in self.raw_matrix_rows:
            if row["job_id"] == job_id:
                return deepcopy(row)
        raise AssertionError(f"raw matrix job not found: {job_id}")

    def assert_chain_rejected(self, connector_root: Path, build_root: Path, expected: str) -> None:
        errors: list[str] = []
        CHECKER.check_verified_runtime_artifact_chain(
            connector_root,
            errors,
            build_root=build_root,
        )
        self.assertTrue(errors, "expected strict artifact-chain rejection")
        self.assertTrue(any(expected in error for error in errors), errors)

    def reseal_aggregate_receipt(self, connector_root: Path, build_root: Path, run_id: str) -> Path:
        receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
        receipt_path.unlink()
        commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
        parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][-1]
        sealed_path = RECEIPT.seal_full_matrix_aggregate_receipt(
            build_root=build_root,
            verified_run_id=run_id,
            profile="full",
            parent_command=parent_command,
            revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
        )
        manifest_path = connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["full_matrix_aggregate_receipt"].update(
            {"path": str(sealed_path), "sha256": sha256(sealed_path), "bytes": sealed_path.stat().st_size}
        )
        write_json(manifest_path, manifest)
        return sealed_path

    def rewrite_raw_job_row(self, build_root: Path, replacement: dict[str, object]) -> None:
        raw_path = build_root / "full-matrix" / "full-runtime-matrix-runs.jsonl"
        rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line]
        rewritten = [replacement if row.get("job_id") == replacement["job_id"] else row for row in rows]
        raw_path.write_text(
            "".join(json.dumps(row, sort_keys=True) + "\n" for row in rewritten),
            encoding="utf-8",
        )

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

    def test_valid_full_matrix_control_uses_default_runtime_build_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            errors: list[str] = []
            with mock.patch.object(CHECKER, "verified_runtime_paths", return_value={"BUILD_ROOT": str(build_root)}):
                CHECKER.check_verified_runtime_artifact_chain(connector_root, errors)
        self.assertEqual([], errors)

    def test_paired_mutable_result_job_and_raw_forgery_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            results_path = build_root / "full-matrix/no-crs/no-mrts/apache/results/force-all/apache-results.jsonl"
            results_path.write_text(
                '{"connector":"apache","status":"pass","forged":true}\n',
                encoding="utf-8",
            )
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["hashes"]["results_jsonl"] = sha256(results_path)
            write_json(job_path, job)
            self.rewrite_raw_job_row(build_root, job)
            self.assert_chain_rejected(connector_root, build_root, "aggregate receipt")

    def test_post_receipt_validation_artifact_swap_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            original_validate = CHECKER.validate_full_matrix_aggregate_receipt
            validation_calls = 0

            def validate_then_swap(*args: object, **kwargs: object) -> tuple[dict[str, object], list[str]]:
                nonlocal validation_calls
                result = original_validate(*args, **kwargs)
                validation_calls += 1
                if validation_calls == 1:
                    job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
                    log_path = job_path.parent / "run.log"
                    log_path.write_text("forged after initial receipt validation\n", encoding="utf-8")
                    job = json.loads(job_path.read_text(encoding="utf-8"))
                    job["hashes"]["log"] = sha256(log_path)
                    write_json(job_path, job)
                    self.rewrite_raw_job_row(build_root, job)
                return result

            errors: list[str] = []
            with mock.patch.object(CHECKER, "validate_full_matrix_aggregate_receipt", side_effect=validate_then_swap):
                CHECKER.check_verified_runtime_artifact_chain(
                    connector_root,
                    errors,
                    build_root=build_root,
                )
        self.assertEqual(2, validation_calls)
        self.assertTrue(any("final aggregate receipt validation failed" in error for error in errors), errors)

    def test_post_validation_command_receipt_swap_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            original_validate = CHECKER.validate_full_matrix_aggregate_receipt
            validation_calls = 0

            def validate_then_swap_command(*args: object, **kwargs: object) -> tuple[dict[str, object], list[str]]:
                nonlocal validation_calls
                result = original_validate(*args, **kwargs)
                validation_calls += 1
                if validation_calls == 1:
                    commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
                    commands = json.loads(commands_path.read_text(encoding="utf-8"))
                    commands["commands"][0]["return_code"] = 99
                    write_json(commands_path, commands)
                return result

            errors: list[str] = []
            with mock.patch.object(
                CHECKER,
                "validate_full_matrix_aggregate_receipt",
                side_effect=validate_then_swap_command,
            ):
                CHECKER.check_verified_runtime_artifact_chain(
                    connector_root,
                    errors,
                    build_root=build_root,
                )
        self.assertEqual(2, validation_calls)
        self.assertTrue(any("verified command receipt hash mismatch" in error for error in errors), errors)

    def test_paired_mutable_job_and_raw_rewrite_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["untrusted_child_note"] = "forged after the job completed"
            write_json(job_path, job)
            self.rewrite_raw_job_row(build_root, job)
            self.assert_chain_rejected(connector_root, build_root, "aggregate receipt")

    def test_raw_matrix_only_rewrite_is_rejected_by_aggregate_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            raw_path = build_root / "full-matrix/full-runtime-matrix-runs.jsonl"
            rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line]
            raw_path.write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n" for row in reversed(rows)),
                encoding="utf-8",
            )
            self.assert_chain_rejected(connector_root, build_root, "aggregate receipt")

    def test_aggregate_receipt_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, run_id = self.build_valid_run(root)
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            escaped_receipt = root / "escaped-aggregate-receipt.json"
            receipt_path.rename(escaped_receipt)
            receipt_path.symlink_to(escaped_receipt)
            self.assert_chain_rejected(connector_root, build_root, "aggregate receipt")

    def test_intermediate_read_swap_fails_closed_without_hashing_external_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, build_root, run_id = self.build_valid_run(root)
            matrix_root = build_root / "full-matrix"
            external_matrix = root / "external-matrix"
            shutil.copytree(matrix_root, external_matrix)
            external_log = external_matrix / "no-crs/no-mrts/apache/run.log"
            external_log.write_text("external bytes must never be sealed\n", encoding="utf-8")
            external_job_path = external_matrix / "no-crs/no-mrts/apache/job.json"
            external_job = json.loads(external_job_path.read_text(encoding="utf-8"))
            external_job["hashes"]["log"] = sha256(external_log)
            write_json(external_job_path, external_job)
            external_raw_path = external_matrix / "full-runtime-matrix-runs.jsonl"
            external_rows = [
                json.loads(line) for line in external_raw_path.read_text(encoding="utf-8").splitlines() if line
            ]
            for index, row in enumerate(external_rows):
                if row["job_id"] == external_job["job_id"]:
                    external_rows[index] = external_job
                    break
            external_raw_path.write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n" for row in external_rows),
                encoding="utf-8",
            )
            moved_matrix = root / "moved-matrix"
            original_open = RECEIPT.os.open
            swapped = False

            def open_with_read_swap(path: object, flags: int, mode: int = 0o777, *, dir_fd: int | None = None) -> int:
                nonlocal swapped
                if not swapped and Path(path).name == "full-runtime-matrix-runs.jsonl":
                    matrix_root.rename(moved_matrix)
                    matrix_root.symlink_to(external_matrix, target_is_directory=True)
                    swapped = True
                if dir_fd is None:
                    return original_open(path, flags, mode)
                return original_open(path, flags, mode, dir_fd=dir_fd)

            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            with mock.patch.object(RECEIPT.os, "open", side_effect=open_with_read_swap):
                with self.assertRaises(RECEIPT.AggregateReceiptError):
                    RECEIPT.build_full_matrix_aggregate_receipt(
                        build_root=build_root,
                        verified_run_id=run_id,
                        profile="full",
                        parent_command=parent_command,
                        revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
                    )
            self.assertTrue(swapped)
            self.assertEqual("external bytes must never be sealed\n", external_log.read_text(encoding="utf-8"))

    def test_oversized_structured_receipt_input_is_rejected_before_materialization(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, build_root, run_id = self.build_valid_run(Path(temporary))
            raw_path = build_root / "full-matrix/full-runtime-matrix-runs.jsonl"
            raw_path.write_bytes(b" " * (RECEIPT.MAX_STRUCTURED_RECEIPT_BYTES + 1))
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            with self.assertRaisesRegex(RECEIPT.AggregateReceiptError, "receipt limit"):
                RECEIPT.build_full_matrix_aggregate_receipt(
                    build_root=build_root,
                    verified_run_id=run_id,
                    profile="full",
                    parent_command=parent_command,
                    revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
                )

    def test_verified_runs_publication_swap_fails_closed_without_external_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, build_root, run_id = self.build_valid_run(root)
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            verified_runs = build_root / "verified-runs"
            moved_runs = root / "moved-verified-runs"
            external_runs = root / "external-verified-runs"
            (external_runs / run_id).mkdir(parents=True)
            sentinel = external_runs / "sentinel.txt"
            sentinel.write_text("must remain untouched\n", encoding="utf-8")
            original_open = RECEIPT.os.open
            swapped = False

            def open_with_publication_swap(path: object, flags: int, mode: int = 0o777, *, dir_fd: int | None = None) -> int:
                nonlocal swapped
                if not swapped and Path(path).name == RECEIPT.RECEIPT_FILENAME and flags & os.O_CREAT:
                    verified_runs.rename(moved_runs)
                    verified_runs.symlink_to(external_runs, target_is_directory=True)
                    swapped = True
                if dir_fd is None:
                    return original_open(path, flags, mode)
                return original_open(path, flags, mode, dir_fd=dir_fd)

            commands_path = verified_runs / run_id / "verified-commands.json"
            parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            with mock.patch.object(RECEIPT.os, "open", side_effect=open_with_publication_swap):
                with self.assertRaises(RECEIPT.AggregateReceiptError):
                    RECEIPT.seal_full_matrix_aggregate_receipt(
                        build_root=build_root,
                        verified_run_id=run_id,
                        profile="full",
                        parent_command=parent_command,
                        revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
                    )
            self.assertTrue(swapped)
            self.assertFalse((external_runs / run_id / RECEIPT.RECEIPT_FILENAME).exists())
            self.assertEqual("must remain untouched\n", sentinel.read_text(encoding="utf-8"))

    def test_runner_uses_sealed_descriptor_record_without_path_rehash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            record = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            revisions = {"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40}
            with mock.patch.object(RUNNER, "full_matrix_receipt_revisions", return_value=revisions), mock.patch.object(
                RUNNER, "sha256_file", side_effect=AssertionError("aggregate receipt must not be reopened by pathname")
            ):
                self.assertTrue(
                    RUNNER.seal_full_matrix_receipt_for_record(
                        record=record,
                        connector_root=connector_root,
                        framework_root=connector_root / "framework",
                        build_root=build_root,
                        verified_run_id=run_id,
                        profile="full",
                    )
                )
                expected = dict(record["aggregate_receipt"])
                receipt_path.unlink()
                receipt_path.write_text("attacker replacement\n", encoding="utf-8")
                manifest_record = RUNNER.aggregate_receipt_manifest_record(
                    commands=[record],
                    build_root=build_root,
                    verified_run_id=run_id,
                )
            self.assertEqual("present", manifest_record["status"])
            self.assertEqual(expected["sha256"], manifest_record["sha256"])
            self.assertEqual(expected["bytes"], manifest_record["bytes"])

    def test_aggregate_receipt_revision_binding_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            manifest_path = connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["connector_sha"] = "d" * 40
            write_json(manifest_path, manifest)
            self.assert_chain_rejected(connector_root, build_root, "revision binding")

    def test_incomplete_matrix_cannot_be_sealed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job_path.unlink()
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            with self.assertRaises(RECEIPT.AggregateReceiptError):
                RECEIPT.seal_full_matrix_aggregate_receipt(
                    build_root=build_root,
                    verified_run_id=run_id,
                    profile="full",
                    parent_command=parent_command,
                    revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
                )
            self.assert_chain_rejected(connector_root, build_root, "aggregate receipt")

    def test_full_matrix_receipt_seals_only_once_after_completion(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            parent_command = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            parent_command.update({"logical_target": "full-matrix-resume", "phase": "full-matrix-resume"})
            sealed_path = RECEIPT.seal_full_matrix_aggregate_receipt(
                build_root=build_root,
                verified_run_id=run_id,
                profile="full",
                parent_command=parent_command,
                revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
            )
            self.assertEqual(receipt_path, sealed_path)
            with self.assertRaises(RECEIPT.AggregateReceiptError):
                RECEIPT.seal_full_matrix_aggregate_receipt(
                    build_root=build_root,
                    verified_run_id=run_id,
                    profile="full",
                    parent_command=parent_command,
                    revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
                )

    def test_completed_resume_is_accepted_after_an_incomplete_parallel_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            commands = json.loads(commands_path.read_text(encoding="utf-8"))
            commands["commands"][0].update(
                {
                    "return_code": 1,
                    "classification": "failure",
                    "runtime_complete": False,
                    "runtime_status": "runtime_failed",
                    "started_at": "2026-07-17T00:00:00Z",
                    "finished_at": "2026-07-17T00:00:01Z",
                }
            )
            env = {
                "FULL_MATRIX_MANIFEST": str(build_root / "full-matrix/full-runtime-matrix-runs.jsonl"),
                "VERIFIED_RUN_ID": run_id,
            }
            # This is the same append path that main() takes before it runs a
            # new resume command.  Completed resume rows must not rewrite the
            # historic failed parallel attempt.
            commands["commands"] = RUNNER.normalize_existing_command_records(
                commands["commands"],
                env,
                "full",
            )
            self.assertFalse(commands["commands"][0]["runtime_complete"])
            self.assertEqual("runtime_failed", commands["commands"][0]["runtime_status"])
            resumed = RUNNER.apply_command_semantics(
                {
                    "logical_target": "full-matrix-resume",
                    "phase": "full-matrix-resume",
                    "required": True,
                    "return_code": 0,
                    "classification": "success",
                    "started_at": "2026-07-18T02:00:00Z",
                    "finished_at": "2026-07-18T02:00:01Z",
                },
                env,
                "full",
            )
            self.assertTrue(resumed["runtime_complete"])
            commands["commands"].append(resumed)
            completed = [
                command
                for command in commands["commands"]
                if command.get("runtime_complete") is True
                and command.get("runtime_status") in {"runtime_completed", "runtime_completed_with_mismatches"}
            ]
            self.assertEqual(1, len(completed))
            write_json(commands_path, commands)
            receipt_path = RECEIPT.seal_full_matrix_aggregate_receipt(
                build_root=build_root,
                verified_run_id=run_id,
                profile="full",
                parent_command=resumed,
                revisions={"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40},
            )
            manifest_path = connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["command_file"].update({"sha256": sha256(commands_path), "bytes": commands_path.stat().st_size})
            manifest["full_matrix_aggregate_receipt"].update(
                {"sha256": sha256(receipt_path), "bytes": receipt_path.stat().st_size}
            )
            write_json(manifest_path, manifest)
            errors: list[str] = []
            CHECKER.check_verified_runtime_artifact_chain(connector_root, errors, build_root=build_root)
        self.assertEqual([], errors)

    def test_redundant_resume_is_not_a_second_required_full_matrix_producer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            commands = json.loads(commands_path.read_text(encoding="utf-8"))
            redundant_resume = {
                **commands["commands"][0],
                "logical_target": "full-matrix-resume",
                "phase": "full-matrix-resume",
                "required": False,
                "optional": True,
                "return_code": 77,
                "runtime_complete": False,
                "runtime_status": "runtime_not_required",
            }
            commands["commands"].append(redundant_resume)
            write_json(commands_path, commands)
            manifest_path = connector_root / "reports/testing/generated/manifest/verified-run-manifest.generated.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["command_file"].update({"sha256": sha256(commands_path), "bytes": commands_path.stat().st_size})
            write_json(manifest_path, manifest)
            errors: list[str] = []
            CHECKER.check_verified_runtime_artifact_chain(
                connector_root,
                errors,
                build_root=build_root,
            )
        self.assertTrue(RUNNER.has_completed_full_matrix_producer(commands["commands"]))
        self.assertFalse(RUNNER.qualifies_for_full_matrix_receipt(redundant_resume, "full"))
        self.assertEqual([], errors)

    def test_resume_completion_uses_all_and_only_current_run_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, build_root, run_id = self.build_valid_run(Path(temporary))
            raw_path = build_root / "full-matrix/full-runtime-matrix-runs.jsonl"
            record = {"started_at": "2026-07-18T01:00:00Z", "return_code": 0}
            env = {"FULL_MATRIX_MANIFEST": str(raw_path), "VERIFIED_RUN_ID": run_id}
            initial_state = RUNNER.full_matrix_runtime_state(record, env, "full")
            resumed_state = RUNNER.full_matrix_runtime_state(
                record,
                env,
                "full",
                include_existing_run_rows=True,
            )
            self.assertFalse(initial_state["runtime_complete"])
            self.assertTrue(resumed_state["runtime_complete"])
            rows = [json.loads(line) for line in raw_path.read_text(encoding="utf-8").splitlines() if line]
            rows[0]["verified_run_id"] = "foreign-run"
            raw_path.write_text(
                "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
                encoding="utf-8",
            )
            foreign_state = RUNNER.full_matrix_runtime_state(
                record,
                env,
                "full",
                include_existing_run_rows=True,
            )
            self.assertFalse(foreign_state["runtime_complete"])

    def test_parent_runner_seals_only_a_qualified_full_matrix_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt_path.unlink()
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            record = json.loads(commands_path.read_text(encoding="utf-8"))["commands"][0]
            revisions = {"connector_sha": "a" * 40, "framework_sha": "b" * 40, "mrts_sha": "c" * 40}
            self.assertTrue(RUNNER.qualifies_for_full_matrix_receipt(record, "full"))
            self.assertFalse(RUNNER.qualifies_for_full_matrix_receipt(record, "smoke"))
            with mock.patch.object(RUNNER, "full_matrix_receipt_revisions", return_value=revisions):
                self.assertTrue(
                    RUNNER.seal_full_matrix_receipt_for_record(
                        record=record,
                        connector_root=connector_root,
                        framework_root=connector_root / "framework",
                        build_root=build_root,
                        verified_run_id=run_id,
                        profile="full",
                    )
                )
            self.assertEqual("sealed", record["aggregate_receipt"]["status"])
            self.assertTrue(receipt_path.is_file())

    def test_sealed_manifest_rewrite_must_be_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, build_root, run_id = self.build_valid_run(Path(temporary))
            matrix_root = build_root / "full-matrix"
            raw_path = matrix_root / "full-runtime-matrix-runs.jsonl"
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            original = raw_path.read_text(encoding="utf-8")
            jobs = GENERATOR.collect_jobs(matrix_root, raw_path)
            GENERATOR.rewrite_manifest(raw_path, jobs, sealed_receipt_path=receipt_path)
            self.assertEqual(original, raw_path.read_text(encoding="utf-8"))
            job_path = matrix_root / "no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["return_code"] = 1
            write_json(job_path, job)
            with self.assertRaisesRegex(ValueError, "sealed full-matrix manifest"):
                GENERATOR.rewrite_manifest(
                    raw_path,
                    GENERATOR.collect_jobs(matrix_root, raw_path),
                    sealed_receipt_path=receipt_path,
                )

    def test_generator_cannot_select_a_foreign_run_to_rewrite_a_sealed_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, run_id = self.build_valid_run(root)
            raw_path = build_root / "full-matrix/full-runtime-matrix-runs.jsonl"
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            raw_before = raw_path.read_bytes()
            receipt_before = receipt_path.read_bytes()
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            job = json.loads(job_path.read_text(encoding="utf-8"))
            job["return_code"] = 1
            write_json(job_path, job)
            argv = [
                "generate-full-matrix-job-completeness.py",
                "--connector-root",
                str(connector_root),
                "--build-root",
                str(build_root),
                "--output-dir",
                str(root / "generated"),
                "--verified-run-id",
                "foreign-run",
                "--rewrite-manifest",
            ]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    GENERATOR.main()
            self.assertEqual(2, raised.exception.code)
            self.assertEqual(raw_before, raw_path.read_bytes())
            self.assertEqual(receipt_before, receipt_path.read_bytes())

    def test_manifest_writer_cannot_mint_an_aggregate_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root = root / "connector"
            build_root = root / "build"
            build_root.mkdir(parents=True)
            run_id = "verified-run-20260718"
            commands_path = build_root / "verified-runs" / run_id / "verified-commands.json"
            write_json(commands_path, {"verified_run_id": run_id, "commands": []})
            RUNNER.write_verified_manifest(
                connector_root=connector_root,
                framework_root=connector_root / "framework",
                build_root=build_root,
                verified_run_id=run_id,
                started_at="2026-07-18T00:00:00Z",
                finished_at="2026-07-18T00:00:01Z",
                commands=[],
                commands_file=commands_path,
                env={},
                profile="full",
                full_matrix_timeout=1,
                timeout_budgets={},
            )
            self.assertFalse(RECEIPT.aggregate_receipt_path(build_root, run_id).exists())

    def test_aggregate_receipt_has_no_self_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            _, build_root, run_id = self.build_valid_run(Path(temporary))
            receipt_path = RECEIPT.aggregate_receipt_path(build_root, run_id)
            receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertNotIn(RECEIPT.RECEIPT_FILENAME, json.dumps(receipt, sort_keys=True))

    def test_report_without_runtime_manifest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            connector_root, build_root, _ = self.build_valid_run(Path(temporary))
            (build_root / "full-matrix" / "full-runtime-matrix-runs.jsonl").unlink()
            self.assert_chain_rejected(connector_root, build_root, "file is unavailable")

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
            self.assert_chain_rejected(connector_root, build_root, "ended_at is missing or invalid")

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
            self.assert_chain_rejected(connector_root, build_root, "summary_path is not canonical")

    def test_direct_summary_path_is_accepted(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            job_path = build_root / "full-matrix/no-crs/no-mrts/apache/job.json"
            direct_summary_path = job_path.parent / "results/apache-summary.json"
            write_json(direct_summary_path, {"apache": {"cases": {"direct": {"status": "pass"}}}})
            job = self.raw_matrix_job("apache:no-crs:no-mrts")
            job["summary_path"] = str(direct_summary_path)
            job["outputs"]["summary"] = str(direct_summary_path)
            job["hashes"]["summary"] = sha256(direct_summary_path)
            write_json(job_path, job)
            replace_raw_matrix_job(
                self.raw_matrix_rows,
                build_root / "full-matrix/full-runtime-matrix-runs.jsonl",
                job,
            )
            self.reseal_aggregate_receipt(connector_root, build_root, "verified-run-20260718")
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
                job = self.raw_matrix_job("apache:no-crs:no-mrts")
                if location == "direct":
                    direct_summary_path = job_path.parent / "results/apache-summary.json"
                    write_json(direct_summary_path, {"apache": {"cases": {"direct": {"status": "pass"}}}})
                    job["summary_path"] = str(direct_summary_path)
                    job["outputs"]["summary"] = str(direct_summary_path)
                job["hashes"]["summary"] = "a" * 64
                write_json(job_path, job)
                replace_raw_matrix_job(
                    self.raw_matrix_rows,
                    build_root / "full-matrix/full-runtime-matrix-runs.jsonl",
                    job,
                )
                self.assert_chain_rejected(connector_root, build_root, "summary hash mismatch")

    def test_symlinked_result_directory_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            results_dir = build_root / "full-matrix/no-crs/no-mrts/apache/results"
            escaped_results = root / "escaped-results"
            results_dir.rename(escaped_results)
            results_dir.symlink_to(escaped_results, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "directory is unavailable or unsafe")

    def test_intermediate_full_matrix_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            matrix_root = build_root / "full-matrix"
            escaped_matrix = root / "escaped-matrix"
            matrix_root.rename(escaped_matrix)
            matrix_root.symlink_to(escaped_matrix, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "directory is unavailable or unsafe")

    def test_intermediate_verified_runs_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            connector_root, build_root, _ = self.build_valid_run(root)
            verified_runs = build_root / "verified-runs"
            escaped_runs = root / "escaped-verified-runs"
            verified_runs.rename(escaped_runs)
            verified_runs.symlink_to(escaped_runs, target_is_directory=True)
            self.assert_chain_rejected(connector_root, build_root, "verified command receipt is missing or unsafe")

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
