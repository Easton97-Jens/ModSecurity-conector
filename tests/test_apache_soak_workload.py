#!/usr/bin/env python3
"""Exercise Apache soak workload result-output containment."""

from __future__ import annotations

from collections import Counter
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
WORKLOAD_PATH = ROOT / "connectors" / "apache" / "harness" / "apache_soak_workload.py"
SPEC = importlib.util.spec_from_file_location("apache_soak_workload", WORKLOAD_PATH)
assert SPEC is not None and SPEC.loader is not None
WORKLOAD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = WORKLOAD
SPEC.loader.exec_module(WORKLOAD)


class ApacheSoakWorkloadTests(unittest.TestCase):
    class FakeWorker:
        def __init__(self, alive: bool) -> None:
            self.alive = alive
            self.join_calls = 0

        def join(self, timeout: int) -> None:
            del timeout
            self.join_calls += 1

        def is_alive(self) -> bool:
            return self.alive

    @staticmethod
    def command_line(run_root: Path, result: Path) -> list[str]:
        return [
            str(WORKLOAD_PATH),
            "--port",
            "18080",
            "--launch-pid",
            "1234",
            "--duration-seconds",
            "1",
            "--concurrency",
            "1",
            "--request-timeout-seconds",
            "1",
            "--restart-interval-seconds",
            "1",
            "--run-root",
            str(run_root),
            "--result",
            str(result),
            "--httpd-version",
            "Apache test",
            "--apxs-version",
            "test",
            "--compiler",
            "cc",
            "--mpm",
            "event",
            "--libmodsecurity-path",
            "/external/libmodsecurity.so",
        ]

    def invoke(self, run_root: Path, result: Path) -> int:
        with mock.patch.object(sys, "argv", self.command_line(run_root, result)):
            return WORKLOAD.main()

    def assert_path_rejected(self, run_root: Path, result: Path, message: str) -> None:
        with (
            mock.patch.object(WORKLOAD, "run_soak") as run_soak,
            mock.patch.object(WORKLOAD, "atomic_json") as atomic_json,
        ):
            with self.assertRaisesRegex(SystemExit, message):
                self.invoke(run_root, result)
        run_soak.assert_not_called()
        atomic_json.assert_not_called()

    def test_valid_direct_child_writes_json(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            run_root = Path(temporary) / "run"
            run_root.mkdir(mode=0o700)
            result = run_root / "apache-soak.json"
            outcome = WORKLOAD.SoakOutcome(
                counters=Counter({name: 1 for name, _, _ in WORKLOAD.REQUEST_SHAPES}),
                restart_requests=1,
                restart_count=1,
            )

            with (
                mock.patch.object(WORKLOAD, "run_soak", return_value=outcome),
                mock.patch.object(WORKLOAD, "real_httpd_child", return_value=4321),
            ):
                self.assertEqual(self.invoke(run_root, result), 0)

            document = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "PASS")
            self.assertEqual(document["restart_count"], 1)
            self.assertEqual(document["restart_requests"], 1)
            self.assertEqual(document["real_httpd_pid"], 4321)
            self.assertEqual(document["requests"], {name: 1 for name, _, _ in WORKLOAD.REQUEST_SHAPES})
            self.assertEqual(result.stat().st_mode & 0o777, 0o600)

    def test_shutdown_joins_all_workers_and_preserves_the_timeout_failure(self) -> None:
        soak = WORKLOAD.SoakRun(SimpleNamespace(request_timeout_seconds=1))
        first = self.FakeWorker(alive=True)
        second = self.FakeWorker(alive=False)
        soak.workers = [first, second]

        self.assertEqual(
            soak.stop_and_join(),
            "Apache soak worker did not stop within the request timeout",
        )
        self.assertEqual(first.join_calls, 1)
        self.assertEqual(second.join_calls, 1)

    def test_shutdown_happens_before_worker_error_evaluation(self) -> None:
        soak = WORKLOAD.SoakRun(SimpleNamespace(duration_seconds=1))

        def inject_late_worker_error() -> str:
            soak.errors.append("late worker failure")
            return ""

        with (
            mock.patch.object(soak, "warm_up"),
            mock.patch.object(soak, "start_workers"),
            mock.patch.object(soak, "run_restarts"),
            mock.patch.object(soak, "stop_and_join", side_effect=inject_late_worker_error),
        ):
            with self.assertRaisesRegex(RuntimeError, "late worker failure"):
                soak.run()

    def test_failed_outcome_is_serialized_before_the_nonzero_exit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            run_root = Path(temporary) / "run"
            run_root.mkdir(mode=0o700)
            result = run_root / "apache-soak.json"
            outcome = WORKLOAD.SoakOutcome(failure="bounded simulated failure")

            with mock.patch.object(WORKLOAD, "run_soak", return_value=outcome):
                with self.assertRaisesRegex(SystemExit, "bounded simulated failure"):
                    self.invoke(run_root, result)

            document = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(document["status"], "FAIL")
            self.assertEqual(document["failure"], "bounded simulated failure")

    def test_run_root_is_required(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            command = self.command_line(
                temporary_root / "run", temporary_root / "run" / "apache-soak.json"
            )
            run_root_index = command.index("--run-root")
            del command[run_root_index : run_root_index + 2]
            stderr = io.StringIO()

            with (
                mock.patch.object(sys, "argv", command),
                mock.patch.object(WORKLOAD, "run_soak") as run_soak,
                mock.patch.object(WORKLOAD, "atomic_json") as atomic_json,
                contextlib.redirect_stderr(stderr),
            ):
                with self.assertRaises(SystemExit) as raised:
                    WORKLOAD.main()

            self.assertEqual(raised.exception.code, 2)
            self.assertIn("--run-root", stderr.getvalue())
            run_soak.assert_not_called()
            atomic_json.assert_not_called()

    def test_relative_result_is_rejected_before_workload_or_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "run"
            working_directory = temporary_root / "working"
            run_root.mkdir(mode=0o700)
            working_directory.mkdir(mode=0o700)
            original_directory = Path.cwd()
            try:
                os.chdir(working_directory)
                self.assert_path_rejected(run_root, Path("relative.json"), "--result must be absolute")
            finally:
                os.chdir(original_directory)
            self.assertFalse((working_directory / "relative.json").exists())

    def test_outside_and_traversal_results_are_rejected_before_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "run"
            run_root.mkdir(mode=0o700)
            outside = temporary_root / "outside" / "apache-soak.json"
            traversal = run_root / ".." / run_root.name / "traversal.json"

            with self.subTest(path="outside"):
                self.assert_path_rejected(run_root, outside, "direct child")
                self.assertFalse(outside.exists())
            with self.subTest(path="traversal"):
                self.assert_path_rejected(run_root, traversal, "traversal")
                self.assertFalse((run_root / "traversal.json").exists())

    def test_source_checkout_run_root_is_rejected_before_output(self) -> None:
        result = ROOT / "apache-soak-workload-result.json"
        self.assert_path_rejected(ROOT, result, "outside the source checkout")
        self.assertFalse(result.exists())

    def test_symlinked_run_root_is_rejected_before_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            real_root = temporary_root / "real-run"
            real_root.mkdir(mode=0o700)
            root_alias = temporary_root / "run-alias"
            root_alias.symlink_to(real_root, target_is_directory=True)

            self.assert_path_rejected(root_alias, root_alias / "apache-soak.json", "symlink")
            self.assertFalse((real_root / "apache-soak.json").exists())

    def test_symlinked_result_parent_is_rejected_before_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "run"
            outside_root = temporary_root / "outside"
            run_root.mkdir(mode=0o700)
            outside_root.mkdir(mode=0o700)
            parent_alias = run_root / "result-parent"
            parent_alias.symlink_to(outside_root, target_is_directory=True)

            self.assert_path_rejected(run_root, parent_alias / "apache-soak.json", "symlink")
            self.assertFalse((outside_root / "apache-soak.json").exists())

    def test_symlinked_final_target_is_rejected_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            run_root = temporary_root / "run"
            protected = temporary_root / "protected-result.json"
            run_root.mkdir(mode=0o700)
            protected.write_text("keep\n", encoding="utf-8")
            result = run_root / "apache-soak.json"
            result.symlink_to(protected)

            self.assert_path_rejected(run_root, result, "symlink")
            self.assertEqual(protected.read_text(encoding="utf-8"), "keep\n")

    def test_missing_parent_is_rejected_and_atomic_writer_never_creates_it(self) -> None:
        with tempfile.TemporaryDirectory(prefix="apache-soak-workload-") as temporary:
            temporary_root = Path(temporary)
            missing_root = temporary_root / "missing-run"
            result = missing_root / "apache-soak.json"

            self.assert_path_rejected(missing_root, result, "must exist")
            self.assertFalse(missing_root.exists())

            missing_parent_result = temporary_root / "missing-parent" / "result.json"
            with self.assertRaisesRegex(ValueError, "result parent does not exist"):
                WORKLOAD.atomic_json(missing_parent_result, {"status": "PASS"})
            self.assertFalse(missing_parent_result.parent.exists())


if __name__ == "__main__":
    unittest.main()
