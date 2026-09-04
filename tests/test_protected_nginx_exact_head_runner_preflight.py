"""Focused contracts for the protected exact-head runner preflight."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import stat
import sys
import tempfile
import types
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci/runtime/broker/protected_nginx_exact_head_runner_preflight.py"
SHA = "a" * 40


def load_module() -> object:
    spec = importlib.util.spec_from_file_location("exact_head_preflight", MODULE_PATH)
    if spec is None:
        raise AssertionError("module spec is unavailable")
    if spec.loader is None:
        raise AssertionError("module loader is unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


P = load_module()


class RunnerPreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runner_temp = self.root / "runner-temp"
        self.runner_temp.mkdir(mode=0o700)
        self.base = self.root / "base"
        self.base.mkdir(mode=0o755)
        self.environment = {
            "PATH": "/usr/bin:/bin",
            "HOME": "/nonexistent",
            "LANG": "C",
            "LC_ALL": "C",
            "RUNNER_TEMP": str(self.runner_temp),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_rejects_non_allowlisted_or_injected_environment(self) -> None:
        for key in (
            "PYTHONPATH",
            "LD_PRELOAD",
            "LD_LIBRARY_PATH",
            "GITHUB_TOKEN",
            "GITHUB_SHA",
            "GITHUB_REPOSITORY",
            "GITHUB_RUN_ID",
        ):
            environment = dict(self.environment, **{key: "attacker"})
            with mock.patch.dict(os.environ, environment, clear=True):
                with self.assertRaisesRegex(P.PreflightError, "non-allowlisted"):
                    P.require_scrubbed_environment()

    def test_rejects_non_fixed_path_and_task_root_escape(self) -> None:
        environment = dict(self.environment, PATH="/attacker:/usr/bin:/bin")
        with mock.patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(P.PreflightError, "fixed PATH"):
                P.require_scrubbed_environment()
        with mock.patch.dict(os.environ, self.environment, clear=True):
            with self.assertRaisesRegex(P.PreflightError, "below RUNNER_TEMP"):
                P.require_private_task_root(str(self.root / "outside"))

    def test_rejects_symlinked_task_root_and_host_control_entry(self) -> None:
        target = self.root / "target"
        target.mkdir(mode=0o700)
        linked = self.runner_temp / "linked"
        linked.symlink_to(target, target_is_directory=True)
        with mock.patch.dict(os.environ, self.environment, clear=True):
            with self.assertRaisesRegex(P.PreflightError, "symbolic link"):
                P.require_private_task_root(str(linked))
        with mock.patch.object(P, "HOST_CONTROL_PATHS", (self.root / "docker.sock",)):
            (self.root / "docker.sock").write_text("not a socket", encoding="utf-8")
            with self.assertRaisesRegex(P.PreflightError, "host-control"):
                P.reject_host_control_sockets()

    def test_rejects_every_fixed_host_control_location(self) -> None:
        for index, path in enumerate(P.HOST_CONTROL_PATHS):
            with self.subTest(path=path):
                sentinel = self.root / f"host-control-{index}"
                sentinel.write_text("present", encoding="utf-8")
                with mock.patch.object(P, "HOST_CONTROL_PATHS", (sentinel,)):
                    with self.assertRaisesRegex(P.PreflightError, "host-control"):
                        P.reject_host_control_sockets()

    def test_prepare_creates_only_private_directories_after_base_verification(self) -> None:
        task = self.runner_temp / "task"
        with mock.patch.dict(os.environ, self.environment, clear=True), \
             mock.patch.object(P, "reject_host_control_sockets"), \
             mock.patch.object(P, "require_base_checkout", return_value=self.base) as base_check:
            result = P.prepare("candidate-build", str(task), str(self.base), SHA)
        self.assertEqual(result, task)
        self.assertEqual({entry.name for entry in task.iterdir()}, {"candidate", "artifacts", "evidence", "logs"})
        base_check.assert_called_once_with(str(self.base), SHA)
        for child in task.iterdir():
            self.assertEqual(child.stat().st_mode & 0o777, 0o700)

    def test_rejects_invalid_sha_before_checkout_is_accepted(self) -> None:
        with mock.patch.dict(os.environ, self.environment, clear=True), \
             mock.patch.object(P, "reject_host_control_sockets"), \
             mock.patch.object(P, "require_base_checkout") as base_check:
            with self.assertRaisesRegex(P.PreflightError, "lowercase 40-character"):
                P.prepare("privileged", str(self.runner_temp / "task"), str(self.base), "main")
        base_check.assert_not_called()

    def test_privileged_role_requires_root_owned_mode_755_host_gate(self) -> None:
        gate = mock.Mock()
        gate.lstat.return_value = types.SimpleNamespace(
            st_mode=stat.S_IFREG | 0o755, st_uid=0, st_gid=0
        )
        with mock.patch.object(P, "no_symlink_chain", return_value=gate):
            self.assertIs(P.require_host_gate(), gate)
        with mock.patch.dict(os.environ, self.environment, clear=True), \
             mock.patch.object(P, "reject_host_control_sockets"), \
             mock.patch.object(P, "require_base_checkout", return_value=self.base), \
             mock.patch.object(P, "require_host_gate") as require_gate:
            self.assertEqual(
                P.prepare("privileged", str(self.runner_temp / "task"), str(self.base), SHA),
                self.runner_temp / "task",
            )
        require_gate.assert_called_once_with()

    def test_privileged_role_fails_closed_when_host_gate_is_missing_or_writable(self) -> None:
        missing = mock.Mock()
        missing.lstat.side_effect = FileNotFoundError()
        with mock.patch.object(P, "no_symlink_chain", return_value=missing):
            with self.assertRaisesRegex(P.PreflightError, "host gate"):
                P.require_host_gate()
        writable = mock.Mock()
        writable.lstat.return_value = types.SimpleNamespace(
            st_mode=stat.S_IFREG | 0o775, st_uid=0, st_gid=0
        )
        with mock.patch.object(P, "no_symlink_chain", return_value=writable):
            with self.assertRaisesRegex(P.PreflightError, "mode 0755"):
                P.require_host_gate()


if __name__ == "__main__":
    unittest.main()
