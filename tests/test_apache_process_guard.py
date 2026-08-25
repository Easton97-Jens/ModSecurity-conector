"""Controlled /proc contract tests for Apache ownership cleanup."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
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
        line = "0: 0100007F:1F90 00000000:0000 0A 0 0 0 0 0 0 4242\n"
        (self.proc / "net" / "tcp").write_text(header + line, encoding="ascii")
        (self.proc / "net" / "tcp6").write_text(header, encoding="ascii")
        self.old_proc = guard.PROC
        guard.PROC = self.proc

    def tearDown(self) -> None:
        guard.PROC = self.old_proc
        self.tmp.cleanup()

    def _record(self) -> dict[str, object]:
        output = Path(self.tmp.name) / "evidence.json"
        guard.record(123, str(self.executable), 8080, output)
        return json.loads(output.read_text(encoding="utf-8"))

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
            "0: 0100007F:1F90 00000000:0000 0A 0 0 0 0 0 0 9999\n",
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
        output = Path(self.tmp.name) / "evidence.json"
        guard.record(123, str(self.executable), 8080, output)
        with self.assertRaises(guard.GuardError):
            guard.record(123, str(self.executable), 8080, output)

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
        self.assertNotIn('while kill -0 "$stale_pid"', source)


if __name__ == "__main__":
    unittest.main()
