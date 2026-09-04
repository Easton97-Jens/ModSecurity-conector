"""Controlled /proc contract tests for Apache ownership cleanup."""

from __future__ import annotations

import json
import os
from pathlib import Path
import stat
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
        self.assertNotIn('APACHE_GUARD_ARTIFACT_ROOT="${APACHE_GUARD_ARTIFACT_ROOT:-', source)
        self.assertNotIn('while kill -0 "$stale_pid"', source)


if __name__ == "__main__":
    unittest.main()
