"""Controlled /proc contract tests for Apache ownership cleanup."""

from __future__ import annotations

import json
import os
from pathlib import Path
import signal
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

    def _write_fake_httpd(self, port: int) -> tuple[Path, Path, Path]:
        httpd = Path(self.tmp.name) / "httpd"
        config = Path(self.tmp.name) / "httpd.conf"
        ready = Path(self.tmp.name) / "httpd.ready"
        ready.unlink(missing_ok=True)
        httpd.write_text(
            "#!/usr/bin/env python3\n"
            "import os, signal, socket, time\n"
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)\n"
            f"listener = socket.socket(); listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); listener.bind(('127.0.0.1', {port})); listener.listen(1)\n"
            f"open({str(ready)!r}, 'x').close()\n"
            "while True: time.sleep(0.05)\n",
            encoding="utf-8",
        )
        httpd.chmod(0o700)
        config.write_text("fake-httpd\n", encoding="ascii")
        config.chmod(0o600)
        return httpd, config, ready

    def _supervisor_env(self) -> dict[str, str]:
        return {**os.environ, guard.RUNNER_ARTIFACT_ROOT_ENV: str(self.artifact_root), "PYTHONDONTWRITEBYTECODE": "1"}

    def _launch_fake_supervisor(self, *, fail_pidfd: bool = False, run_name: str = "run") -> tuple[subprocess.Popen[bytes], Path, Path, int]:
        port = self._reserve_loopback_port()
        httpd, config, ready = self._write_fake_httpd(port)
        run_dir = self.artifact_root / run_name
        run_dir.mkdir(mode=0o700, exist_ok=True)
        state = run_dir / "supervisor-state.json"
        pid_output = run_dir / "supervisor.pid"
        code = (
            "from pathlib import Path\n"
            "from connectors.apache.harness import apache_process_guard as g\n"
            + ("import os, time; _pidfd_open = os.pidfd_open\n"
               "def _wait_then_fail(_pid):\n"
               f"    deadline = time.monotonic() + 5.0\n"
               f"    while time.monotonic() < deadline and not Path({str(ready)!r}).exists(): time.sleep(0.01)\n"
               f"    if not Path({str(ready)!r}).exists(): raise OSError('fake httpd did not become ready')\n"
               "    raise OSError('injected')\n"
               "os.pidfd_open = _wait_then_fail\n" if fail_pidfd else "")
            + f"raise SystemExit(g.supervise(Path({str(httpd)!r}), Path({str(config)!r}), Path({str(state)!r}), Path({str(pid_output)!r})))\n"
        )
        env = {**os.environ, guard.RUNNER_ARTIFACT_ROOT_ENV: str(self.artifact_root), "PYTHONDONTWRITEBYTECODE": "1"}
        log = open(self.artifact_root / "supervisor.log", "wb")
        try:
            process = subprocess.Popen([sys.executable, "-c", code], cwd=Path(__file__).parents[1], env=env,
                                       stdout=subprocess.DEVNULL, stderr=log)
        finally:
            log.close()
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and not pid_output.exists() and process.poll() is None:
            time.sleep(0.02)
        return process, state, pid_output, port

    def _wait_for_fake_ready(self, port: int, timeout: float = 5.0) -> None:
        ready = Path(self.tmp.name) / "httpd.ready"
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if ready.exists():
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                    if probe.connect_ex(("127.0.0.1", port)) == 0:
                        return
            time.sleep(0.02)
        log = self.artifact_root / "supervisor.log"
        detail = log.read_text(encoding="utf-8", errors="replace") if log.exists() else ""
        self.fail(f"fake Apache listener did not become ready on port {port}: {detail}")

    @staticmethod
    def _wait_pid_gone(pid: int, timeout: float = 5.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not Path(f"/proc/{pid}").exists():
                return
            time.sleep(0.02)
        raise AssertionError(f"process {pid} remained after bounded cleanup")

    @staticmethod
    def _assert_port_free(port: int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            probe.settimeout(0.2)
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                raise AssertionError(f"Apache listener remained on port {port}")
            probe.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                probe.bind(("127.0.0.1", port))
            except OSError as exc:
                raise AssertionError(f"Apache port could not be rebound: {exc}") from exc

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

    def test_pid_output_partial_failure_retains_replacement_inode(self) -> None:
        output = self.artifact_root / "run" / "supervisor.pid"
        real_write = os.write
        calls = 0

        def replace_then_fail(fd: int, payload: bytes | memoryview) -> int:
            nonlocal calls
            calls += 1
            if calls == 1:
                written = real_write(fd, bytes(payload[:2]))
                output.unlink()
                output.write_text("replacement\n", encoding="ascii")
                return written
            raise OSError("simulated PID publication failure")

        with mock.patch.object(guard.os, "write", side_effect=replace_then_fail):
            with self.assertRaises(guard.GuardError):
                guard._write_pid_output(output, 123, self.artifact_root)
        self.assertEqual(output.read_text(encoding="ascii"), "replacement\n")

    def test_pid_output_delayed_close_error_closes_published_fd_exactly_once(self) -> None:
        output = self.artifact_root / "run" / "supervisor.pid"
        real_close = os.close
        close_calls: list[int] = []
        regular_close_calls: list[int] = []

        def close_once_with_delayed_error(fd: int) -> None:
            close_calls.append(fd)
            is_regular = stat.S_ISREG(os.fstat(fd).st_mode)
            real_close(fd)
            if is_regular:
                regular_close_calls.append(fd)
                raise OSError("simulated delayed close error")

        with mock.patch.object(guard.os, "close", side_effect=close_once_with_delayed_error):
            with self.assertRaisesRegex(guard.GuardError, "delayed close error"):
                guard._write_pid_output(output, 123, self.artifact_root)
        self.assertFalse(output.exists())
        self.assertEqual(len(close_calls), 3)
        self.assertEqual(len(regular_close_calls), 1)

    def test_pid_output_close_then_path_replacement_is_rejected_and_retained(self) -> None:
        output = self.artifact_root / "run" / "supervisor-race.pid"
        real_close = os.close
        replaced = False

        def close_then_replace(fd: int) -> None:
            nonlocal replaced
            is_regular = stat.S_ISREG(os.fstat(fd).st_mode)
            real_close(fd)
            if is_regular and not replaced:
                replaced = True
                output.unlink()
                output.write_text("replacement\n", encoding="ascii")

        with mock.patch.object(guard.os, "close", side_effect=close_then_replace):
            with self.assertRaisesRegex(guard.GuardError, "inode changed"):
                guard._write_pid_output(output, 123, self.artifact_root)
        self.assertTrue(replaced)
        self.assertEqual(output.read_text(encoding="ascii"), "replacement\n")
        self.assertFalse(list(self.artifact_root.glob(".apache-process-guard-*.tmp")))

    def test_supervisor_state_requires_typed_versioned_record(self) -> None:
        state = self.artifact_root / "run" / "supervisor-state.json"
        state.write_text(json.dumps({"address": "msconnector-apache-test"}), encoding="utf-8")
        with self.assertRaisesRegex(guard.GuardError, "kind/version"):
            guard.stop_supervisor(state, self.artifact_root)

    def test_supervisor_state_replacement_inode_is_retained(self) -> None:
        state = self.artifact_root / "run" / "supervisor-state.json"
        real_link = os.link

        def link_then_replace(src: str, dst: str, **kwargs: object) -> None:
            real_link(src, dst, **kwargs)
            state.unlink()
            state.write_text("replacement\n", encoding="ascii")

        with mock.patch.object(guard.os, "link", side_effect=link_then_replace):
            with self.assertRaisesRegex(guard.GuardError, "inode changed"):
                guard._publish_supervisor_state(
                    {"kind": "apache-supervisor-session", "version": 1},
                    state,
                    self.artifact_root,
                )
        self.assertEqual(state.read_text(encoding="ascii"), "replacement\n")
        self.assertFalse(list(self.artifact_root.glob(".apache-process-guard-*.tmp")))

    def test_shell_never_blindly_removes_supervisor_pid_output(self) -> None:
        source = (Path(__file__).parents[1] / "connectors/apache/harness/run_apache_smoke.sh").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('rm -f "$HTTPD_SUPERVISOR_PID_OUTPUT"', source)
        self.assertIn("supervisor PID output remains after cleanup", source)

    def test_pidfd_open_failure_kills_term_ignoring_child_and_frees_port(self) -> None:
        supervisor, state, pid_output, port = self._launch_fake_supervisor(fail_pidfd=True)
        try:
            ready = Path(self.tmp.name) / "httpd.ready"
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline and not ready.exists():
                time.sleep(0.02)
            self.assertTrue(ready.exists(), "pidfd failure was not injected after listener readiness")
            supervisor.wait(timeout=5)
            self.assertFalse(pid_output.exists())
            self.assertFalse(state.exists())
            self._assert_port_free(port)
        finally:
            if supervisor.poll() is None:
                supervisor.kill()
                supervisor.wait(timeout=3)

    def test_term_ignoring_child_ack_reaps_and_followup_launch_succeeds(self) -> None:
        supervisor, state, pid_output, port = self._launch_fake_supervisor()
        try:
            self._wait_for_fake_ready(port)
            started = time.monotonic()
            result = subprocess.run(
                [sys.executable, str(Path(guard.__file__)), "stop-supervisor", "--state", str(state)],
                cwd=Path(__file__).parents[1], env=self._supervisor_env(), check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
            )
            elapsed = time.monotonic() - started
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertGreaterEqual(elapsed, guard.SUPERVISOR_TERM_TIMEOUT * 0.8)
            supervisor.wait(timeout=5)
            self.assertFalse(state.exists())
            self.assertFalse(pid_output.exists())
            with socket.socket() as probe:
                self.assertNotEqual(probe.connect_ex(("127.0.0.1", port)), 0)
        finally:
            if supervisor.poll() is None:
                supervisor.kill()
                supervisor.wait(timeout=3)

        follow_up, follow_state, follow_pid, follow_port = self._launch_fake_supervisor()
        try:
            self._wait_for_fake_ready(follow_port)
            result = subprocess.run(
                [sys.executable, str(Path(guard.__file__)), "stop-supervisor", "--state", str(follow_state)],
                cwd=Path(__file__).parents[1], env=self._supervisor_env(), check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            follow_up.wait(timeout=5)
            self.assertFalse(follow_state.exists())
            self.assertFalse(follow_pid.exists())
            with socket.socket() as probe:
                self.assertNotEqual(probe.connect_ex(("127.0.0.1", follow_port)), 0)
        finally:
            if follow_up.poll() is None:
                follow_up.kill()
                follow_up.wait(timeout=3)

    def test_same_uid_foreign_lineage_cannot_stop_live_supervisor(self) -> None:
        supervisor, state, pid_output, port = self._launch_fake_supervisor()
        try:
            self._wait_for_fake_ready(port)
            stop_args = [sys.executable, str(Path(guard.__file__)), "stop-supervisor", "--state", str(state)]
            result = subprocess.run(
                [sys.executable, "-c", "import subprocess; raise SystemExit(subprocess.run(" + repr(stop_args) + ", check=False).returncode)"],
                cwd=Path(__file__).parents[1], env=self._supervisor_env(), check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIsNone(supervisor.poll())
            self.assertTrue(state.exists())
            self.assertTrue(pid_output.exists())
            result = subprocess.run(
                [sys.executable, str(Path(guard.__file__)), "stop-supervisor", "--state", str(state)],
                cwd=Path(__file__).parents[1], env=self._supervisor_env(), check=False,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            supervisor.wait(timeout=5)
            self._assert_port_free(port)
        finally:
            if supervisor.poll() is None:
                supervisor.kill()
                supervisor.wait(timeout=3)

    def test_same_uid_foreign_lineage_cannot_retire_then_legitimate_retire_succeeds(self) -> None:
        supervisor, state, pid_output, port = self._launch_fake_supervisor()
        foreign: subprocess.Popen[bytes] | None = None
        original_proc = guard.PROC
        guard.PROC = Path("/proc")
        try:
            self._wait_for_fake_ready(port)
            evidence = json.loads(state.read_text(encoding="utf-8"))
            supervisor.kill()
            supervisor.wait(timeout=5)
            self._wait_pid_gone(int(evidence["child_pid"]))
            self._assert_port_free(port)
            foreign = subprocess.Popen(["sleep", "5"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            foreign_identity = guard._stat(foreign.pid)
            evidence["parent_pid"] = foreign.pid
            evidence["parent_pid_starttime"] = foreign_identity["starttime"]
            state.write_text(json.dumps(evidence) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(guard.GuardError, "lineage"):
                guard.retire_supervisor_session(state, pid_output, self.artifact_root)
            evidence["parent_pid"] = os.getpid()
            evidence["parent_pid_starttime"] = guard._stat(os.getpid())["starttime"]
            state.write_text(json.dumps(evidence) + "\n", encoding="utf-8")
            guard.retire_supervisor_session(state, pid_output, self.artifact_root)
            self.assertFalse(state.exists())
            self.assertFalse(pid_output.exists())
        finally:
            guard.PROC = original_proc
            if foreign is not None and foreign.poll() is None:
                foreign.kill()
                foreign.wait(timeout=3)
            if supervisor.poll() is None:
                supervisor.kill()
                supervisor.wait(timeout=3)

    def test_supervisor_sigkill_reaps_exact_child_and_artifacts_are_retirable(self) -> None:
        original_proc = guard.PROC
        guard.PROC = Path("/proc")
        for attempt in range(5):
            with self.subTest(attempt=attempt):
                supervisor, state, pid_output, port = self._launch_fake_supervisor()
                try:
                    self._wait_for_fake_ready(port)
                    evidence = json.loads(state.read_text(encoding="utf-8"))
                    supervisor.kill()
                    supervisor.wait(timeout=5)
                    self._wait_pid_gone(int(evidence["child_pid"]))
                    self._assert_port_free(port)
                    if state.exists() or pid_output.exists():
                        guard.retire_supervisor_session(state, pid_output, self.artifact_root)
                    self.assertFalse(state.exists())
                    self.assertFalse(pid_output.exists())
                finally:
                    if supervisor.poll() is None:
                        supervisor.kill()
                        supervisor.wait(timeout=3)
        guard.PROC = original_proc

    def test_runner_parent_sigkill_reaps_supervisor_and_exact_child(self) -> None:
        for attempt in range(5):
            with self.subTest(attempt=attempt):
                port = self._reserve_loopback_port()
                httpd, config, ready = self._write_fake_httpd(port)
                run_dir = self.artifact_root / f"parent-run-{attempt}"
                run_dir.mkdir(mode=0o700)
                state = run_dir / "supervisor-state.json"
                pid_output = run_dir / "supervisor.pid"
                code = (
                    "from pathlib import Path\n"
                    "from connectors.apache.harness import apache_process_guard as g\n"
                    f"raise SystemExit(g.supervise(Path({str(httpd)!r}), Path({str(config)!r}), Path({str(state)!r}), Path({str(pid_output)!r})))\n"
                )
                runner = subprocess.Popen(
                    [sys.executable, "-c", code], cwd=Path(__file__).parents[1],
                    env=self._supervisor_env(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                try:
                    deadline = time.monotonic() + 5
                    while time.monotonic() < deadline and not ready.exists():
                        self.assertIsNone(runner.poll())
                        time.sleep(0.02)
                    self.assertTrue(ready.exists())
                    self._wait_for_fake_ready(port)
                    evidence = json.loads(state.read_text(encoding="utf-8"))
                    runner.kill()
                    runner.wait(timeout=5)
                    self._wait_pid_gone(int(evidence["supervisor_pid"]))
                    self._wait_pid_gone(int(evidence["child_pid"]))
                    self._assert_port_free(port)
                    if state.exists():
                        residual = json.loads(state.read_text(encoding="utf-8"))
                        self.assertEqual(residual["kind"], "apache-supervisor-session")
                        self.assertFalse(Path(f"/proc/{int(residual['supervisor_pid'])}").exists())
                        self.assertFalse(Path(f"/proc/{int(residual['child_pid'])}").exists())
                    if pid_output.exists():
                        self.assertEqual(pid_output.read_text(encoding="ascii").strip(), str(evidence["child_pid"]))
                finally:
                    if runner.poll() is None:
                        runner.kill()
                        runner.wait(timeout=3)

    def test_runner_death_during_blocked_popen_window_cleans_supervisor_and_child(self) -> None:
        port = self._reserve_loopback_port()
        httpd, config, ready = self._write_fake_httpd(port)
        run_dir = self.artifact_root / "popen-window"
        run_dir.mkdir(mode=0o700)
        state = run_dir / "supervisor-state.json"
        pid_output = run_dir / "supervisor.pid"
        marker = run_dir / "popen-marker.json"
        supervisor_code = (
            "import json, os, subprocess, time\n"
            "from pathlib import Path\n"
            "from connectors.apache.harness import apache_process_guard as g\n"
            "original_popen = g.subprocess.Popen\n"
            "def wrapped_popen(*args, **kwargs):\n"
            "    child = original_popen(*args, **kwargs)\n"
            f"    marker = Path({str(marker)!r})\n"
            "    temporary_marker = marker.with_name(marker.name + '.tmp')\n"
            "    temporary_marker.write_text(json.dumps({'supervisor_pid': os.getpid(), 'child_pid': child.pid}), encoding='ascii')\n"
            "    os.replace(temporary_marker, marker)\n"
            "    while True: time.sleep(0.05)\n"
            "g.subprocess.Popen = wrapped_popen\n"
            f"raise SystemExit(g.supervise(Path({str(httpd)!r}), Path({str(config)!r}), Path({str(state)!r}), Path({str(pid_output)!r})))\n"
        )
        runner_code = (
            "import subprocess, sys\n"
            f"child = subprocess.Popen([sys.executable, '-c', {supervisor_code!r}], cwd={str(Path(__file__).parents[1])!r})\n"
            "child.wait()\n"
        )
        evidence: dict[str, object] | None = None
        owned_processes: list[tuple[int, int]] = []
        runner = subprocess.Popen(
            [sys.executable, "-c", runner_code], cwd=Path(__file__).parents[1],
            env=self._supervisor_env(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        try:
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline and not marker.exists():
                self.assertIsNone(runner.poll())
                time.sleep(0.02)
            self.assertTrue(marker.exists(), "Popen wrapper did not observe a real child launch")
            evidence = json.loads(marker.read_text(encoding="ascii"))
            self.assertGreater(int(evidence["supervisor_pid"]), 1)
            self.assertGreater(int(evidence["child_pid"]), 1)
            owned_processes = [
                (pid, os.pidfd_open(pid))
                for pid in (int(evidence["supervisor_pid"]), int(evidence["child_pid"]))
            ]
            self._wait_for_fake_ready(port)
            runner.kill()
            runner.wait(timeout=5)
            self._wait_pid_gone(int(evidence["supervisor_pid"]))
            self._wait_pid_gone(int(evidence["child_pid"]))
            self._assert_port_free(port)
        finally:
            if runner.poll() is None:
                runner.kill()
                runner.wait(timeout=5)
            for pid, pidfd in owned_processes:
                try:
                    signal.pidfd_send_signal(pidfd, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                finally:
                    os.close(pidfd)
                if Path(f"/proc/{pid}").exists():
                    try:
                        self._wait_pid_gone(pid, timeout=2)
                    except AssertionError:
                        pass

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
        self.assertIn('"$PYTHON_BIN" "$APACHE_PROCESS_GUARD" supervise', source)
        self.assertIn('"$PYTHON_BIN" "$APACHE_PROCESS_GUARD" stop-supervisor', source)
        self.assertIn('HTTPD_SUPERVISOR_STATE=', source)
        self.assertIn('[ "$httpd_wait_safe" -eq 1 ]', source)
        self.assertIn('[ ! -f "${HTTPD_GUARD_EVIDENCE:-}" ]', source)
        self.assertNotIn('APACHE_GUARD_ARTIFACT_ROOT="${APACHE_GUARD_ARTIFACT_ROOT:-', source)
        self.assertNotIn('while kill -0 "$stale_pid"', source)

    def test_supervisor_is_launch_bound_and_bounded(self) -> None:
        source = (Path(__file__).parents[1] / "connectors/apache/harness/apache_process_guard.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('start_new_session=True', source)
        self.assertIn('os.pidfd_open(child.pid)', source)
        self.assertIn('PR_SET_PDEATHSIG', source)
        self.assertIn('SUPERVISOR_CONTROL_TIMEOUT', source)
        self.assertIn('SUPERVISOR_TERM_TIMEOUT', source)
        self.assertIn('SUPERVISOR_KILL_TIMEOUT', source)
        self.assertIn('"-X", "-f"', source)
        self.assertIn('pass_fds=(httpd_fd, config_fd)', source)
        self.assertIn('O_EXCL', source)

    def test_shell_exit_handler_propagates_cleanup_failure(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "connectors/apache/harness/run_apache_smoke.sh"
        ).read_text(encoding="utf-8")
        handler = source.split("on_exit() {", 1)[1].split("\n}\n", 1)[0]
        for initial_status, cleanup_status, expected_status in (
            (0, 0, 0),
            (0, 77, 77),
            (1, 0, 1),
            (1, 77, 1),
        ):
            with self.subTest(
                initial_status=initial_status,
                cleanup_status=cleanup_status,
            ):
                result = subprocess.run(
                    [
                        "sh",
                        "-c",
                        "cleanup() { return \"$CLEANUP_STATUS\"; }\n"
                        f"on_exit() {{{handler}\n}}\n"
                        "trap on_exit EXIT\n"
                        "exit \"$INITIAL_STATUS\"\n",
                    ],
                    env={
                        **os.environ,
                        "CLEANUP_STATUS": str(cleanup_status),
                        "INITIAL_STATUS": str(initial_status),
                    },
                    check=False,
                )
                self.assertEqual(result.returncode, expected_status)

    def test_shell_signal_handlers_cleanup_once_and_exit_for_signal(self) -> None:
        source = (
            Path(__file__).parents[1]
            / "connectors/apache/harness/run_apache_smoke.sh"
        ).read_text(encoding="utf-8")
        exit_handler = source.split("on_exit() {", 1)[1].split("\n}\n", 1)[0]
        signal_handler = source.split("on_signal() {", 1)[1].split("\n}\n", 1)[0]
        self.assertIn("trap on_exit EXIT", source)
        self.assertIn("trap 'on_signal 129' HUP", source)
        self.assertIn("trap 'on_signal 130' INT", source)
        self.assertIn("trap 'on_signal 143' TERM", source)
        self.assertIn("trap - EXIT HUP INT TERM", source)

        for signal_name, expected_status in (("HUP", 129), ("INT", 130), ("TERM", 143)):
            with self.subTest(signal_name=signal_name), tempfile.TemporaryDirectory() as tmp:
                count_file = Path(tmp) / "cleanup-count"
                result = subprocess.run(
                    [
                        "sh",
                        "-c",
                        "cleanup() {\n"
                        "  count=0\n"
                        "  if [ -f \"$COUNT_FILE\" ]; then count=$(cat \"$COUNT_FILE\"); fi\n"
                        "  count=$((count + 1))\n"
                        "  printf '%s\\n' \"$count\" > \"$COUNT_FILE\"\n"
                        "}\n"
                        f"on_exit() {{{exit_handler}\n}}\n"
                        f"on_signal() {{{signal_handler}\n}}\n"
                        "trap on_exit EXIT\n"
                        "trap 'on_signal 129' HUP\n"
                        "trap 'on_signal 130' INT\n"
                        "trap 'on_signal 143' TERM\n"
                        f"kill -{signal_name} \"$$\"\n"
                        "exit 99\n",
                    ],
                    env={**os.environ, "COUNT_FILE": str(count_file)},
                    check=False,
                )
                self.assertEqual(result.returncode, expected_status)
                self.assertEqual(count_file.read_text(encoding="ascii"), "1\n")


if __name__ == "__main__":
    unittest.main()
