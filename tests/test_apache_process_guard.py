"""Controlled /proc contract tests for Apache ownership cleanup."""

from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from connectors.apache.harness import apache_process_guard as guard


class ApacheProcessGuardTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.proc = Path(self.tmp.name) / "proc"
        (self.proc / "123" / "fd").mkdir(parents=True)
        (self.proc / "net").mkdir()
        self.executable = Path(self.tmp.name) / "httpd"
        self.executable.write_text("binary", encoding="ascii")
        (self.proc / "123" / "exe").symlink_to(self.executable)
        fields = ["S", "1", "123", "123"] + ["0"] * 15 + ["999"]
        (self.proc / "123" / "stat").write_text(
            "123 (httpd) " + " ".join(fields) + "\n", encoding="ascii"
        )
        (self.proc / "123" / "fd" / "7").symlink_to("socket:[4242]")
        header = "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n"
        line = "0: 0100007F:1F90 00000000:0000 0A 0 0 0 0 0 4242\n"
        (self.proc / "net" / "tcp").write_text(header + line, encoding="ascii")
        (self.proc / "net" / "tcp6").write_text(header, encoding="ascii")
        self.old_proc = guard.PROC
        guard.PROC = self.proc
        self.artifact_root = Path(self.tmp.name) / "artifacts"
        self.artifact_root.mkdir(mode=0o700)
        (self.artifact_root / "run").mkdir(mode=0o700)

    def tearDown(self) -> None:
        guard.PROC = self.old_proc
        self.tmp.cleanup()

    def _record(self) -> dict[str, object]:
        output = self.artifact_root / "run" / "evidence.json"
        guard.record(123, str(self.executable), 8080, output, self.artifact_root)
        return json.loads(output.read_text(encoding="utf-8"))

    @staticmethod
    def _reserve_loopback_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            return int(listener.getsockname()[1])

    def _start_loopback_server(self, port: int) -> subprocess.Popen[bytes]:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "http.server",
                str(port),
                "--bind",
                "127.0.0.1",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        deadline = time.monotonic() + 5.0
        while time.monotonic() < deadline:
            if process.poll() is not None:
                self.fail(f"test HTTP server exited with {process.returncode}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                if probe.connect_ex(("127.0.0.1", port)) == 0:
                    return process
            time.sleep(0.02)
        process.kill()
        process.wait(timeout=2)
        self.fail("test HTTP server did not become ready")

    def test_normal_ownership_records_identity_and_listener(self) -> None:
        evidence = self._record()
        self.assertEqual(evidence["pid"], 123)
        self.assertEqual(evidence["starttime"], 999)
        self.assertEqual(evidence["session"], 123)
        self.assertEqual(evidence["pgrp"], 123)
        self.assertEqual(evidence["listener_inodes"], [4242])
        guard.verify_running(evidence)

    def test_pid_reuse_or_session_mismatch_is_rejected(self) -> None:
        evidence = self._record()
        stat = self.proc / "123" / "stat"
        stat.write_text(
            "123 (httpd) " + " ".join(["S", "1", "456", "456"] + ["0"] * 15 + ["999"]) + "\n",
            encoding="ascii",
        )
        with self.assertRaises(guard.GuardError):
            guard.verify_running(evidence)

    def test_missing_proc_is_fail_closed(self) -> None:
        evidence = self._record()
        (self.proc / "123" / "stat").unlink()
        with self.assertRaises(guard.GuardError):
            guard.verify_running(evidence)

    def test_listener_mismatch_is_fail_closed(self) -> None:
        evidence = self._record()
        (self.proc / "123" / "fd" / "7").unlink()
        with self.assertRaises(guard.GuardError):
            guard.verify_running(evidence)

    def test_foreign_replacement_listener_is_not_accepted(self) -> None:
        evidence = self._record()
        (self.proc / "123" / "stat").unlink()
        (self.proc / "net" / "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n"
            "0: 0100007F:1F90 00000000:0000 0A 0 0 0 0 0 9999\n",
            encoding="ascii",
        )
        with self.assertRaises(guard.GuardError):
            guard.verify_stopped(evidence)

    def test_pidfile_pid_mismatch_is_rejected_before_signal(self) -> None:
        evidence = self._record()
        with self.assertRaises(guard.GuardError):
            guard.verify_pidfile(evidence, 124)

    def test_pidfd_open_precedes_identity_verification_and_signal(self) -> None:
        order: list[str] = []
        with mock.patch.object(guard, "_open_verified_pidfd", side_effect=lambda _: (order.append("open") or 9, 123, str(self.executable), {})), \
             mock.patch.object(guard, "verify_running", side_effect=lambda _: order.append("verify")), \
             mock.patch.object(guard.signal, "pidfd_send_signal", side_effect=lambda *_: order.append("signal")), \
             mock.patch.object(guard.os, "close"):
            guard.signal_verified({"pid": 123}, 15)
        self.assertEqual(order, ["open", "verify", "signal"])

    def test_pidfd_unavailability_fails_closed(self) -> None:
        with mock.patch.object(guard.os, "pidfd_open", None), mock.patch.object(
            guard.signal, "pidfd_send_signal", None
        ):
            with self.assertRaises(guard.GuardError):
                guard.signal_verified({"pid": 123}, 15)

    def test_pidfd_fdinfo_guard_error_closes_pidfd_once(self) -> None:
        evidence = {
            "pid": 123,
            "executable": str(self.executable),
            "starttime": 999,
            "session": 123,
            "pgrp": 123,
        }
        with mock.patch.object(guard.os, "pidfd_open", return_value=9), \
             mock.patch.object(
                 guard, "_pidfd_bound_pid", side_effect=guard.GuardError("missing Pid")
             ), \
             mock.patch.object(guard.os, "close") as close:
            with self.assertRaisesRegex(guard.GuardError, "missing Pid"):
                guard._open_verified_pidfd(evidence)
        close.assert_called_once_with(9)

    def test_proc_scan_is_bounded(self) -> None:
        evidence = self._record()
        (self.proc / "123" / "stat").unlink()
        (self.proc / "net" / "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n",
            encoding="ascii",
        )
        with mock.patch.object(guard, "MAX_PROC_ENTRIES", 0):
            with self.assertRaises(guard.GuardError):
                guard.verify_stopped(evidence)

    def test_fd_scan_is_bounded(self) -> None:
        with mock.patch.object(guard, "MAX_FD_ENTRIES", 0):
            with self.assertRaises(guard.GuardError):
                guard._fd_inodes(123)

    def test_listener_scan_is_bounded_without_materializing_rows(self) -> None:
        with mock.patch.object(guard, "MAX_NET_ROWS", 0):
            with self.assertRaises(guard.GuardError):
                guard._listener_inodes(8080)

    def test_malformed_listener_row_fails_closed(self) -> None:
        (self.proc / "net" / "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n"
            "malformed\n",
            encoding="ascii",
        )
        with self.assertRaises(guard.GuardError):
            guard._listener_inodes(8080)

    def test_listener_inode_is_not_the_timeout_field(self) -> None:
        self.proc.joinpath("net", "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n"
            "0: 0100007F:1F90 00000000:0000 0A 0 0 0 0 4242 7777\n",
            encoding="ascii",
        )
        listeners = guard._listener_inodes(8080)
        self.assertEqual(listeners, {7777})
        self.assertNotIn(4242, listeners)

    def test_preflight_checks_self_pidfd_binding_and_signal_zero(self) -> None:
        calls: list[tuple[str, int]] = []
        with mock.patch.object(guard.os, "pidfd_open", return_value=9), \
             mock.patch.object(guard, "_pidfd_bound_pid", return_value=guard.os.getpid()), \
             mock.patch.object(guard, "_pidfd_send_signal", side_effect=lambda fd, sig: calls.append(("signal", sig))), \
             mock.patch.object(guard.os, "close"):
            guard.preflight()
        self.assertEqual(calls, [("signal", 0)])

    def test_preflight_rejects_wrong_self_pidfd_binding(self) -> None:
        with mock.patch.object(guard.os, "pidfd_open", return_value=9), \
             mock.patch.object(guard, "_pidfd_bound_pid", return_value=guard.os.getpid() + 1), \
             mock.patch.object(guard.os, "close"):
            with self.assertRaises(guard.GuardError):
                guard.preflight()

    def test_preflight_rejects_missing_or_oversized_net_header(self) -> None:
        (self.proc / "net" / "tcp").write_text("x" * (guard.MAX_NET_LINE + 1), encoding="ascii")
        with mock.patch.object(guard.os, "pidfd_open", return_value=9), \
             mock.patch.object(guard, "_pidfd_bound_pid", return_value=guard.os.getpid()), \
             mock.patch.object(guard, "_pidfd_send_signal"), \
             mock.patch.object(guard.os, "close"):
            with self.assertRaises(guard.GuardError):
                guard.preflight()

    def test_evidence_is_non_overwriting_and_symlink_safe(self) -> None:
        output = self.artifact_root / "evidence.json"
        guard.record(123, str(self.executable), 8080, output, self.artifact_root)
        with self.assertRaises(guard.GuardError):
            guard.record(123, str(self.executable), 8080, output, self.artifact_root)

    def test_evidence_record_completes_short_writes(self) -> None:
        output = self.artifact_root / "short-writes.json"
        real_write = os.write
        writes: list[bytes] = []
        opened: list[int] = []

        def short_write(fd: int, payload: bytes | memoryview) -> int:
            if not opened:
                opened.append(fd)
            chunk = bytes(payload[:7])
            writes.append(chunk)
            return real_write(fd, chunk)

        with mock.patch.object(guard.os, "write", side_effect=short_write), \
             mock.patch.object(guard.os, "close", wraps=os.close) as close:
            guard.record(123, str(self.executable), 8080, output, self.artifact_root)
        self.assertGreater(len(writes), 1)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["pid"], 123)
        self.assertEqual([call.args[0] for call in close.call_args_list].count(opened[-1]), 1)

    def test_evidence_record_rejects_zero_progress_and_closes_fd(self) -> None:
        output = self.artifact_root / "zero-write.json"
        opened: list[int] = []

        def zero_write(fd: int, _payload: bytes | memoryview) -> int:
            if not opened:
                opened.append(fd)
            return 0

        with mock.patch.object(guard.os, "write", side_effect=zero_write), \
             mock.patch.object(guard.os, "close", wraps=os.close) as close:
            with self.assertRaisesRegex(guard.GuardError, "no progress"):
                guard.record(123, str(self.executable), 8080, output, self.artifact_root)
        self.assertEqual([call.args[0] for call in close.call_args_list].count(opened[-1]), 1)
        self.assertFalse(output.exists())
        self.assertFalse(list(self.artifact_root.glob(".apache-process-guard-*.tmp")))

    def test_partial_evidence_write_rolls_back_before_reporting_failure(self) -> None:
        output = self.artifact_root / "partial-write.json"
        real_write = os.write
        calls = 0

        def partial_then_error(fd: int, payload: bytes | memoryview) -> int:
            nonlocal calls
            calls += 1
            if calls == 1:
                return real_write(fd, bytes(payload[:7]))
            raise OSError("simulated evidence I/O failure")

        with mock.patch.object(guard.os, "write", side_effect=partial_then_error), \
             mock.patch.object(guard, "_terminate_after_record_failure") as terminate:
            with self.assertRaisesRegex(guard.RecordFailureCleaned, "cleanup completed"):
                guard.record(123, str(self.executable), 8080, output, self.artifact_root)
        terminate.assert_called_once()
        self.assertFalse(output.exists())
        self.assertFalse(list(self.artifact_root.glob(".apache-process-guard-*.tmp")))

    def test_failed_evidence_write_terminates_real_server_and_allows_follow_up(self) -> None:
        if not guard._pidfd_available():
            self.skipTest("Linux pidfd support is unavailable")

        port = self._reserve_loopback_port()
        output = self.artifact_root / "real-record.json"
        original_proc = guard.PROC
        first: subprocess.Popen[bytes] | None = None
        follow_up: subprocess.Popen[bytes] | None = None
        guard.PROC = Path("/proc")
        try:
            first = self._start_loopback_server(port)
            with mock.patch.object(guard.os, "write", return_value=0):
                with self.assertRaises(guard.RecordFailureCleaned):
                    guard.record(
                        first.pid,
                        sys.executable,
                        port,
                        output,
                        self.artifact_root,
                    )
            first.wait(timeout=5)
            self.assertFalse(output.exists())

            follow_up = self._start_loopback_server(port)
            guard.record(
                follow_up.pid,
                sys.executable,
                port,
                output,
                self.artifact_root,
            )
            evidence = guard._load(output, self.artifact_root)
            guard.terminate_verified(evidence)
            follow_up.wait(timeout=5)
            guard.verify_stopped(evidence)
        finally:
            guard.PROC = original_proc
            for process in (first, follow_up):
                if process is not None and process.poll() is None:
                    process.kill()
                    process.wait(timeout=5)

    def test_transient_process_inspection_failures_terminate_verified_server(self) -> None:
        if not guard._pidfd_available():
            self.skipTest("Linux pidfd support is unavailable")

        original_proc = guard.PROC
        guard.PROC = Path("/proc")
        try:
            for helper_name in ("_stat", "_exe", "_fd_inodes", "_listener_inodes"):
                with self.subTest(helper=helper_name):
                    port = self._reserve_loopback_port()
                    output = self.artifact_root / f"unstable-{helper_name}.json"
                    process = self._start_loopback_server(port)
                    original = getattr(guard, helper_name)
                    failed = False

                    def fail_once(*args: object) -> object:
                        nonlocal failed
                        if not failed:
                            failed = True
                            raise OSError("simulated transient process inspection failure")
                        return original(*args)

                    try:
                        with mock.patch.object(guard, helper_name, side_effect=fail_once):
                            with self.assertRaises(guard.RecordFailureCleaned):
                                guard.record(
                                    process.pid,
                                    sys.executable,
                                    port,
                                    output,
                                    self.artifact_root,
                                )
                        process.wait(timeout=5)
                        self.assertFalse(output.exists())
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                            probe.bind(("127.0.0.1", port))
                    finally:
                        if process.poll() is None:
                            process.kill()
                            process.wait(timeout=5)
        finally:
            guard.PROC = original_proc

    def test_artifact_paths_must_be_absolute_and_private(self) -> None:
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(Path("relative/evidence.json"), self.artifact_root)
        public = Path(self.tmp.name) / "public"
        public.mkdir()
        public.chmod(0o755)
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(public / "evidence.json", self.artifact_root)

    def test_artifact_paths_reject_symlinked_parent(self) -> None:
        real = Path(self.tmp.name) / "real"
        real.mkdir()
        link = Path(self.tmp.name) / "link"
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(link / "evidence.json", self.artifact_root)

    def test_artifact_paths_reject_parent_traversal(self) -> None:
        private = Path(self.tmp.name) / "private"
        private.mkdir(mode=0o700)
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(private / "nested" / ".." / "evidence.json", self.artifact_root)

    def test_artifact_paths_reject_nested_symlink(self) -> None:
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir(mode=0o700)
        nested = self.artifact_root / "nested"
        nested.mkdir(mode=0o700)
        link = nested / "linked"
        link.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(link / "evidence.json", self.artifact_root)

    def test_artifact_root_rejects_symlink_alias(self) -> None:
        root_link = Path(self.tmp.name) / "artifact-root-link"
        root_link.symlink_to(self.artifact_root, target_is_directory=True)
        with self.assertRaises(guard.GuardError):
            guard._validated_artifact_path(root_link / "evidence.json", root_link)

    def test_evidence_loader_rejects_symlinked_file(self) -> None:
        evidence = self._record()
        target = Path(self.tmp.name) / "target.json"
        target.write_text(json.dumps(evidence), encoding="utf-8")
        link = Path(self.tmp.name) / "link.json"
        link.symlink_to(target)
        with self.assertRaises(guard.GuardError):
            guard._load(link, self.artifact_root)

    def test_evidence_loader_rejects_nonregular_fifo_without_blocking(self) -> None:
        fifo = self.artifact_root / "evidence.pipe"
        os.mkfifo(fifo, mode=0o600)
        with self.assertRaises(guard.GuardError):
            guard._load(fifo, self.artifact_root)

    def test_evidence_loader_rejects_oversized_regular_file(self) -> None:
        evidence = self.artifact_root / "oversized.json"
        evidence.write_bytes(b"{" + b"a" * guard.MAX_EVIDENCE_BYTES + b"}")
        with self.assertRaises(guard.GuardError):
            guard._load(evidence, self.artifact_root)

    def test_evidence_loader_accepts_valid_regular_file(self) -> None:
        evidence = self._record()
        loaded = guard._load(self.artifact_root / "run" / "evidence.json", self.artifact_root)
        self.assertEqual(loaded, evidence)

    def test_runtime_directory_creation_is_descriptor_relative_and_private(self) -> None:
        target = self.artifact_root / "created" / "nested"
        guard.prepare_runtime_directory(target, "test runtime directory", True)
        self.assertTrue(target.is_dir())
        self.assertFalse(target.is_symlink())
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o700)

    def test_runtime_directory_preserves_nonprivate_output_root_contract(self) -> None:
        target = self.artifact_root / "output-root"
        target.mkdir(mode=0o755)
        target.chmod(0o755)
        guard.prepare_runtime_directory(target, "test output root", False)
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o755)

    def test_guard_cli_requires_runner_configuration_and_rejects_generic_path_flags(self) -> None:
        script = str(Path(guard.__file__).resolve())
        target = self.artifact_root / "runner-created"
        environment = os.environ.copy()
        environment.pop(guard.RUNNER_DIRECTORY_ENV, None)
        environment.pop(guard.RUNNER_ARTIFACT_ROOT_ENV, None)

        missing = subprocess.run(
            [
                sys.executable,
                script,
                "prepare-directory",
                "--label",
                "test runtime directory",
                "--private",
            ],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(missing.returncode, 77)
        self.assertIn("must be supplied by the Apache smoke runner", missing.stdout)
        self.assertFalse(target.exists())

        legacy = subprocess.run(
            [
                sys.executable,
                script,
                "prepare-directory",
                "--directory",
                str(target),
                "--label",
                "test runtime directory",
                "--private",
            ],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(legacy.returncode, 2)
        self.assertFalse(target.exists())

        configured = environment.copy()
        configured[guard.RUNNER_DIRECTORY_ENV] = str(target)
        accepted = subprocess.run(
            [
                sys.executable,
                script,
                "prepare-directory",
                "--label",
                "test runtime directory",
                "--private",
            ],
            env=configured,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(accepted.returncode, 0, accepted.stderr)
        self.assertTrue(target.is_dir())

        legacy_artifact_root = subprocess.run(
            [sys.executable, script, "preflight", "--artifact-root", str(self.artifact_root)],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(legacy_artifact_root.returncode, 2)

    def test_runtime_directory_rejects_foreign_owned_ancestor_metadata(self) -> None:
        metadata = mock.Mock(
            st_mode=stat.S_IFDIR | 0o755,
            st_uid=os.geteuid() + 1,
        )
        with self.assertRaises(guard.GuardError):
            guard._safe_runtime_ancestor(metadata, Path("/trusted/ancestor"))

    def test_runtime_directory_rejects_symlink_inserted_during_create(self) -> None:
        root = self.artifact_root / "race-root"
        root.mkdir(mode=0o700)
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir(mode=0o700)
        target = root / "inserted" / "nested"
        real_mkdir = os.mkdir
        injected = False

        def insert_symlink(
            component: str | bytes,
            mode: int = 0o777,
            *,
            dir_fd: int | None = None,
        ) -> None:
            nonlocal injected
            descriptor_path = (
                Path(os.readlink(f"/proc/self/fd/{dir_fd}")) if dir_fd is not None else None
            )
            if component == "inserted" and descriptor_path == root:
                injected = True
                (root / "inserted").symlink_to(outside, target_is_directory=True)
                raise FileExistsError("simulated concurrent directory replacement")
            real_mkdir(component, mode, dir_fd=dir_fd)

        with mock.patch.object(guard.os, "mkdir", side_effect=insert_symlink):
            with self.assertRaises(guard.GuardError):
                guard.prepare_runtime_directory(target, "test runtime directory", True)
        self.assertTrue(injected)
        self.assertFalse((outside / "nested").exists())

    def test_cleanup_requires_absent_process_and_listener_and_is_idempotent(self) -> None:
        evidence = self._record()
        (self.proc / "123" / "stat").unlink()
        (self.proc / "net" / "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n",
            encoding="ascii",
        )
        guard.verify_stopped(evidence)
        guard.verify_stopped(evidence)

    def test_cleanup_rejects_remaining_session_or_process_group_member(self) -> None:
        evidence = self._record()
        member = self.proc / "124"
        member.mkdir()
        fields = ["S", "1", "123", "123"] + ["0"] * 15 + ["1000"]
        (member / "stat").write_text(
            "124 (worker) " + " ".join(fields) + "\n", encoding="ascii"
        )
        (self.proc / "123" / "stat").unlink()
        (self.proc / "net" / "tcp").write_text(
            "sl local_address rem_address st tx_queue tr tm->when retrnsmt uid timeout inode\n",
            encoding="ascii",
        )
        with self.assertRaises(guard.GuardError):
            guard.verify_stopped(evidence)

    def test_shell_guard_has_no_broad_process_or_port_cleanup(self) -> None:
        source = (Path(__file__).parents[1] / "connectors/apache/harness/run_apache_smoke.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("apache_process_guard.py", source)
        self.assertIn("verify-running", source)
        self.assertIn("verify-stopped", source)
        self.assertNotIn("pkill", source)
        self.assertNotIn("pgrep", source)
        self.assertNotIn("lsof", source)
        self.assertNotIn("kill \"$stale_pid\"", source)
        self.assertNotIn("kill \"$HTTPD_PID\"", source)
        self.assertIn('"$PYTHON_BIN" "$APACHE_PROCESS_GUARD" terminate', source)
        self.assertIn('"$PYTHON_BIN" "$APACHE_PROCESS_GUARD" verify-pid', source)
        self.assertIn('APACHE_GUARD_ARTIFACT_ROOT="$RUNTIME_ROOT"', source)
        self.assertIn("record_server_ownership() {", source)
        self.assertIn('HTTPD_RECORD_FAILURE_CLEANED=1', source)
        self.assertIn('[ "$httpd_wait_safe" -eq 1 ]', source)
        self.assertIn('[ ! -f "${HTTPD_GUARD_EVIDENCE:-}" ]', source)
        self.assertNotIn('APACHE_GUARD_ARTIFACT_ROOT="${APACHE_GUARD_ARTIFACT_ROOT:-', source)
        self.assertNotIn('while kill -0 "$stale_pid"', source)


if __name__ == "__main__":
    unittest.main()
