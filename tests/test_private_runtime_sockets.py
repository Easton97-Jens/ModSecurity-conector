from __future__ import annotations

import os
import importlib.util
from pathlib import Path
import signal
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "ci/runtime/lifecycle/with-private-sockets.py"


class PrivateRuntimeSocketsTest(unittest.TestCase):
    def environment(self, parent: Path) -> dict[str, str]:
        return dict(os.environ, RUNNER_TEMP=str(parent), TMPDIR=str(parent))

    def test_long_evidence_paths_use_bindable_private_sockets_and_cleanup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="uds-") as temporary:
            parent = Path(temporary)
            evidence = parent / ("a" * 40) / ("b" * 40) / "evidence"
            code = """
import os, pathlib, socket, stat, sys
root = pathlib.Path(os.environ['MSCONNECTOR_PRIVATE_SOCKET_ROOT'])
assert stat.S_IMODE(root.stat().st_mode) == 0o700
assert root.stat().st_uid == os.geteuid()
for name in ('envoy-response-observer.sock', 'envoy-ext-authz-companion.sock', 'traefik-forwardauth-companion.sock'):
    path = root / name
    assert len(os.fsencode(path)) < 108
    with socket.socket(socket.AF_UNIX) as sock:
        sock.bind(str(path))
print(root)
pathlib.Path(sys.argv[1]).mkdir(parents=True)
"""
            result = subprocess.run(
                [sys.executable, str(WRAPPER), sys.executable, "-c", code, str(evidence)],
                env=self.environment(parent), capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(Path(result.stdout.strip()).exists())
            self.assertTrue(evidence.is_dir())

    def test_unsafe_or_overlong_parents_are_rejected_before_child_execution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="uds-") as temporary:
            parent = Path(temporary)
            target = parent / "target"
            target.mkdir(mode=0o700)
            alias = parent / "alias"
            alias.symlink_to(target, target_is_directory=True)
            writable = parent / "writable"
            writable.mkdir()
            writable.chmod(0o777)
            long_parent = parent / ("x" * 90)
            long_parent.mkdir(mode=0o700)
            for invalid in (alias, writable, long_parent, Path("relative")):
                result = subprocess.run(
                    [sys.executable, str(WRAPPER), sys.executable, "-c", "print('CHILD EXECUTED')"],
                    env=self.environment(invalid), capture_output=True, text=True, timeout=10,
                )
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn("CHILD EXECUTED", result.stdout)
            self.assertEqual(list(target.iterdir()), [])

    def test_sigterm_reaches_child_and_socket_root_is_cleaned(self) -> None:
        with tempfile.TemporaryDirectory(prefix="uds-") as temporary:
            process = subprocess.Popen(
                [sys.executable, str(WRAPPER), sys.executable, "-u", "-c",
                 "import os,time; print(os.environ['MSCONNECTOR_PRIVATE_SOCKET_ROOT'], flush=True); time.sleep(60)"],
                env=self.environment(Path(temporary)), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            try:
                assert process.stdout is not None
                socket_root = Path(process.stdout.readline().strip())
                self.assertTrue(socket_root.is_dir())
                process.send_signal(signal.SIGTERM)
                _, stderr = process.communicate(timeout=5)
                self.assertEqual(process.returncode, 128 + signal.SIGTERM, stderr)
                self.assertFalse(socket_root.exists())
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()

    def test_envoy_harnesses_pass_socket_length_gate_with_deep_artifact_roots(self) -> None:
        true_binary = shutil.which("true")
        assert true_binary is not None
        for script, root_variable in (("start_envoy_connector.sh", "START_ROOT"),
                                      ("run_envoy_connector_runtime.sh", "RUNTIME_ROOT")):
            with self.subTest(script=script), tempfile.TemporaryDirectory(prefix="uds-") as temporary:
                parent = Path(temporary)
                artifact_root = parent / ("a" * 40) / ("b" * 40) / "runtime"
                environment = self.environment(parent)
                environment.update({root_variable: str(artifact_root), "PYTHON": sys.executable,
                                    "ENVOY_BIN": true_binary, "SERVICE_BIN": true_binary,
                                    "RESPONSE_OBSERVER_BIN": true_binary,
                                    "MSCONNECTOR_NO_CRS_BASELINE": "0"})
                result = subprocess.run(
                    [sys.executable, str(WRAPPER), "sh",
                     str(ROOT / "connectors/envoy/harness" / script)],
                    env=environment, capture_output=True, text=True, timeout=15,
                )
                # Dummy host stops at readiness; this verifies path preflight,
                # not a hosted Envoy runtime result.
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("response observer exited", result.stderr)
                self.assertNotIn("socket path is too long", result.stderr)
                self.assertTrue(artifact_root.is_dir())
                self.assertEqual(list(parent.glob("mcs.*")), [])

    def test_envoy_direct_harness_fallback_creates_private_socket_directory(self) -> None:
        true_binary = shutil.which("true")
        assert true_binary is not None
        for script, root_variable in (("start_envoy_connector.sh", "START_ROOT"),
                                      ("run_envoy_connector_runtime.sh", "RUNTIME_ROOT")):
            with self.subTest(script=script), tempfile.TemporaryDirectory(prefix="uds-") as temporary:
                artifact_root = Path(temporary) / "r"
                environment = dict(os.environ, MSCONNECTOR_PRIVATE_SOCKET_ROOT="")
                environment.update({root_variable: str(artifact_root), "PYTHON": sys.executable,
                                    "ENVOY_BIN": true_binary, "SERVICE_BIN": true_binary,
                                    "RESPONSE_OBSERVER_BIN": true_binary,
                                    "MSCONNECTOR_NO_CRS_BASELINE": "0"})
                result = subprocess.run(
                    ["sh", str(ROOT / "connectors/envoy/harness" / script)],
                    env=environment, capture_output=True, text=True, timeout=15,
                )
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("response observer exited", result.stderr)
                self.assertEqual((artifact_root / "mrc").stat().st_mode & 0o777, 0o700)

    def test_successful_stage_with_live_grandchild_fails_and_cleans_processes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="uds-") as temporary:
            code = """
import os, subprocess, sys
child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
print(os.environ['MSCONNECTOR_PRIVATE_SOCKET_ROOT'], flush=True)
print(child.pid, flush=True)
"""
            result = subprocess.run(
                [sys.executable, str(WRAPPER), sys.executable, "-c", code],
                env=self.environment(Path(temporary)), capture_output=True, text=True, timeout=10,
            )
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertIn("left live processes", result.stderr)
            root, grandchild = result.stdout.splitlines()
            self.assertFalse(Path(root).exists())
            stat_path = Path("/proc") / grandchild / "stat"
            if stat_path.exists():
                record = stat_path.read_text()
                state = record[record.rfind(")") + 2:].split()[0]
                self.assertIn(state, {"Z", "X"})

    def test_process_readback_failure_retains_socket_root(self) -> None:
        spec = importlib.util.spec_from_file_location("private_socket_wrapper", WRAPPER)
        assert spec is not None and spec.loader is not None
        wrapper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wrapper)
        for failure in (OSError("process readback failed"), ValueError("invalid process record")):
            with self.subTest(failure=type(failure).__name__), tempfile.TemporaryDirectory(prefix="uds-") as temporary:
                parent = Path(temporary)
                with mock.patch.dict(os.environ, self.environment(parent)), mock.patch.object(
                    wrapper, "stop_group", side_effect=failure
                ), self.assertRaises(type(failure)):
                    wrapper.run([sys.executable, "-c", "pass"])
                retained = list(parent.glob("mcs.*"))
                self.assertEqual(len(retained), 1)
                self.assertTrue(retained[0].is_dir())
                self.assertEqual(retained[0].stat().st_mode & 0o777, 0o700)


if __name__ == "__main__":
    unittest.main()
