"""Parent-owned regression coverage for HAProxy HTX transaction-ID bounds."""

from __future__ import annotations

import importlib.util
import http.server
import json
import os
from pathlib import Path
import signal
import ssl
import subprocess
import tempfile
import threading
import time
import unittest
import urllib.parse


HELPER_PATH = (
    Path(__file__).resolve().parents[1]
    / "connectors/haproxy/harness/haproxy_htx_smoke_helper.py"
)
RUNTIME_PATH = HELPER_PATH.with_name("run_haproxy_htx_runtime.sh")
SPEC = importlib.util.spec_from_file_location("haproxy_htx_smoke_helper", HELPER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class _LoopbackTLSHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = b"tls-ok\n"
        self.send_response(200)
        self.send_header("content-type", "text/plain")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        del fmt, args


class HAProxyHTXTransactionIdTest(unittest.TestCase):
    def test_owned_child_identity_handles_a_whitespace_process_name(self) -> None:
        """The built-in /proc parser must ignore whitespace in the comm field."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        parser_start = source.index("read_owned_process_stat_field() {")
        parser_end = source.index("\nwait_for_owned_child_stop()", parser_start)
        parser_setup = source[parser_start:parser_end]
        self.assertNotIn("awk", parser_setup)

        with tempfile.TemporaryDirectory(prefix="haproxy-htx-proc-") as temporary:
            worker = Path(temporary) / "worker with space"
            worker.write_text("#!/bin/sh\nexec /bin/sleep 600\n", encoding="utf-8")
            worker.chmod(0o755)
            process = subprocess.Popen([str(worker)])
            try:
                completed = subprocess.run(
                    [
                        "/bin/sh",
                        "-c",
                        "\n".join(
                            (
                                "set -eu",
                                parser_setup,
                                "token=$(owned_child_start_token \"$HAPROXY_HTX_CHILD_PID\")",
                                "state=$(owned_child_stat_field \"$HAPROXY_HTX_CHILD_PID\" 1)",
                                "printf '%s %s\\n' \"$token\" \"$state\"",
                            )
                        ),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                    env={
                        **os.environ,
                        "HAPROXY_HTX_CHILD_PID": str(process.pid),
                        "PATH": "",
                    },
                )
            finally:
                process.kill()
                process.wait(timeout=5)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        token, state = completed.stdout.strip().split()
        self.assertTrue(token.isdecimal())
        self.assertNotEqual(state, "Z")

    def test_background_helper_execs_the_tracked_worker(self) -> None:
        """A tracked background helper PID must be its worker, not a shell wrapper."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        helper_start = source.index("start_helper() {")
        helper_end = source.index("\nread_owned_process_stat_field()", helper_start)
        start_helper = source[helper_start:helper_end]

        with tempfile.TemporaryDirectory(prefix="haproxy-htx-helper-") as temporary:
            root = Path(temporary)
            worker = root / "worker.sh"
            worker_pid_path = root / "worker.pid"
            wrapper_pid_path = root / "wrapper.pid"
            worker.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$$\" > \"$HAPROXY_HTX_WORKER_PID_PATH\"\n"
                "exec sleep 600\n",
                encoding="utf-8",
            )
            worker.chmod(0o755)
            process = subprocess.Popen(
                [
                    "/bin/sh",
                    "-c",
                    "\n".join(
                        (
                            "set -eu",
                            start_helper,
                            "start_helper serve-upstream >/dev/null 2>&1 &",
                            "helper_pid=$!",
                            "printf '%s\\n' \"$helper_pid\" > \"$HAPROXY_HTX_WRAPPER_PID_PATH\"",
                            "wait \"$helper_pid\"",
                        )
                    ),
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={
                    **os.environ,
                    "PYTHON_BIN": "/bin/sh",
                    "HELPER": str(worker),
                    "RUNTIME_ROOT": str(root / "runtime"),
                    "HAPROXY_HTX_WORKER_PID_PATH": str(worker_pid_path),
                    "HAPROXY_HTX_WRAPPER_PID_PATH": str(wrapper_pid_path),
                },
            )
            try:
                deadline = time.monotonic() + 5
                while (
                    not (worker_pid_path.is_file() and wrapper_pid_path.is_file())
                    and process.poll() is None
                    and time.monotonic() < deadline
                ):
                    time.sleep(0.01)
                self.assertTrue(worker_pid_path.is_file(), "worker did not start")
                self.assertTrue(wrapper_pid_path.is_file(), "wrapper PID was not recorded")
                worker_pid = int(worker_pid_path.read_text(encoding="utf-8").strip())
                wrapper_pid = int(wrapper_pid_path.read_text(encoding="utf-8").strip())
                self.assertEqual(wrapper_pid, worker_pid)
                os.kill(wrapper_pid, signal.SIGTERM)
                stdout, stderr = process.communicate(timeout=5)
                self.assertEqual(process.returncode, 143, stdout + stderr)
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=5)

    def test_runtime_signal_cleanup_bounds_term_ignoring_child(self) -> None:
        """Cleanup escalates, reaps its child, and preserves the first signal status."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        cleanup_start = source.index("read_owned_process_stat_field() {")
        cleanup_end = source.index("\ngenerate_loopback_tls_certificate()", cleanup_start)
        cleanup_setup = source[cleanup_start:cleanup_end]
        script = "\n".join(
            (
                "set -eu",
                "HAPROXY_HTX_CHILD_STOP_ATTEMPTS=5",
                "HAPROXY_HTX_CHILD_STOP_DELAY_SECONDS=1",
                "upstream_pid=",
                "upstream_pid_token=",
                "haproxy_pid=",
                "haproxy_pid_token=",
                "haproxy_command_pid=",
                "haproxy_command_pid_token=",
                "sync_upstream_pid=",
                "sync_upstream_pid_token=",
                "streaming_client_pid=",
                "streaming_client_pid_token=",
                "owned_launch_pending=",
                "owned_launch_pid=",
                "owned_launch_token=",
                "owned_launch_label=",
                "owned_launch_signal_status=",
                cleanup_setup,
                "( trap '' TERM; exec sleep 600 ) >/dev/null 2>&1 &",
                "streaming_client_pid=$!",
                "capture_owned_child_token \"$streaming_client_pid\" \"test child\"",
                "streaming_client_pid_token=$owned_child_captured_token",
                "printf '%s\\n' \"$streaming_client_pid\" > \"$HAPROXY_HTX_CHILD_PID_PATH\"",
                "runner_pid=$$",
                "( sleep 1; kill -INT \"$runner_pid\" 2>/dev/null || true ) >/dev/null 2>&1 &",
                "kill -TERM \"$$\"",
            )
        )
        with tempfile.TemporaryDirectory(prefix="haproxy-htx-cleanup-") as temporary:
            child_pid_path = Path(temporary) / "stubborn-child.pid"
            process = subprocess.Popen(
                ["/bin/sh", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={**os.environ, "HAPROXY_HTX_CHILD_PID_PATH": str(child_pid_path)},
            )
            try:
                stdout, stderr = process.communicate(timeout=8)
                self.assertTrue(child_pid_path.is_file(), "fixture did not record its child PID")
                child_pid = int(child_pid_path.read_text(encoding="utf-8").strip())
                try:
                    os.kill(child_pid, 0)
                except ProcessLookupError:
                    child_is_alive = False
                else:
                    child_is_alive = True
                self.assertFalse(child_is_alive, "signal cleanup left a TERM-ignoring child alive")
                self.assertEqual(process.returncode, 143, stdout + stderr)
            except subprocess.TimeoutExpired:
                self.fail("signal cleanup did not bound a TERM-ignoring owned child")
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=5)

    def test_signal_cleanup_reaps_direct_child_before_token_capture(self) -> None:
        """A signal in the pending-token window must not orphan its direct child."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        cleanup_start = source.index("read_owned_process_stat_field() {")
        cleanup_end = source.index("\ngenerate_loopback_tls_certificate()", cleanup_start)
        cleanup_setup = source[cleanup_start:cleanup_end]
        script = "\n".join(
            (
                "set -eu",
                "HAPROXY_HTX_CHILD_STOP_ATTEMPTS=1",
                "HAPROXY_HTX_CHILD_STOP_DELAY_SECONDS=0",
                "upstream_pid=",
                "upstream_pid_token=",
                "haproxy_pid=",
                "haproxy_pid_token=",
                "haproxy_command_pid=",
                "haproxy_command_pid_token=",
                "sync_upstream_pid=",
                "sync_upstream_pid_token=",
                "streaming_client_pid=",
                "streaming_client_pid_token=",
                "owned_launch_pending=",
                "owned_launch_pid=",
                "owned_launch_token=",
                "owned_launch_label=",
                "owned_launch_signal_status=",
                cleanup_setup,
                "( trap '' TERM; exec /bin/sleep 600 ) >/dev/null 2>&1 &",
                "streaming_client_pid=$!",
                "printf '%s\\n' \"$streaming_client_pid\" > \"$HAPROXY_HTX_CHILD_PID_PATH\"",
                "kill -TERM \"$$\"",
            )
        )
        with tempfile.TemporaryDirectory(prefix="haproxy-htx-pending-token-") as temporary:
            child_pid_path = Path(temporary) / "pending-child.pid"
            process = subprocess.Popen(
                ["/bin/sh", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={**os.environ, "HAPROXY_HTX_CHILD_PID_PATH": str(child_pid_path)},
            )
            try:
                stdout, stderr = process.communicate(timeout=5)
                self.assertTrue(child_pid_path.is_file(), "fixture did not record its pending child PID")
                child_pid = int(child_pid_path.read_text(encoding="utf-8").strip())
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
                self.assertEqual(process.returncode, 143, stdout + stderr)
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=5)

    def test_owned_haproxy_command_cleanup_reaps_signal_resistant_child(self) -> None:
        """Synchronous HAProxy commands are tracked while the runner waits for them."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        command_start = source.index("start_haproxy_command() {")
        command_end = source.index("\nread_owned_process_stat_field()", command_start)
        command_setup = source[command_start:command_end]
        cleanup_start = source.index("read_owned_process_stat_field() {")
        cleanup_end = source.index("\ngenerate_loopback_tls_certificate()", cleanup_start)
        cleanup_setup = source[cleanup_start:cleanup_end]
        self.assertIn('run_owned_haproxy_command "HAProxy version probe" -vv', source)
        self.assertEqual(
            source.count('run_owned_haproxy_command "HAProxy configuration check" -c -f "$config_file"'),
            2,
        )

        with tempfile.TemporaryDirectory(prefix="haproxy-htx-command-") as temporary:
            root = Path(temporary)
            fake_haproxy = root / "haproxy"
            child_pid_path = root / "command-child.pid"
            fake_haproxy.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$$\" > \"$HAPROXY_HTX_COMMAND_PID_PATH\"\n"
                "trap '' HUP INT TERM\n"
                "exec /bin/sleep 600\n",
                encoding="utf-8",
            )
            fake_haproxy.chmod(0o755)
            script = "\n".join(
                (
                    "set -eu",
                    "HAPROXY_HTX_CHILD_STOP_ATTEMPTS=1",
                "HAPROXY_HTX_CHILD_STOP_DELAY_SECONDS=0",
                "upstream_pid=",
                "upstream_pid_token=",
                "haproxy_pid=",
                "haproxy_pid_token=",
                "haproxy_command_pid=",
                "haproxy_command_pid_token=",
                "sync_upstream_pid=",
                "sync_upstream_pid_token=",
                "streaming_client_pid=",
                "streaming_client_pid_token=",
                "owned_launch_pending=",
                "owned_launch_pid=",
                "owned_launch_token=",
                "owned_launch_label=",
                "owned_launch_signal_status=",
                    "HAPROXY_BIN=$HAPROXY_HTX_FAKE_HAPROXY",
                    command_setup,
                    cleanup_setup,
                    "run_owned_haproxy_command \"HAProxy configuration check\" -c -f ignored",
                )
            )
            process = subprocess.Popen(
                ["/bin/sh", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={
                    **os.environ,
                    "HAPROXY_HTX_FAKE_HAPROXY": str(fake_haproxy),
                    "HAPROXY_HTX_COMMAND_PID_PATH": str(child_pid_path),
                },
            )
            try:
                deadline = time.monotonic() + 5
                while not child_pid_path.is_file() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(child_pid_path.is_file(), "fixture did not start the owned HAProxy command")
                process.send_signal(signal.SIGTERM)
                stdout, stderr = process.communicate(timeout=5)
                child_pid = int(child_pid_path.read_text(encoding="utf-8").strip())
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
                self.assertEqual(process.returncode, 143, stdout + stderr)
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=5)

    def test_signal_before_pid_assignment_is_deferred_until_child_cleanup(self) -> None:
        """A cancellation while `$!` is unavailable must still reap the new child."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        command_start = source.index("start_haproxy_command() {")
        command_end = source.index("\nread_owned_process_stat_field()", command_start)
        command_setup = source[command_start:command_end]
        cleanup_start = source.index("read_owned_process_stat_field() {")
        cleanup_end = source.index("\ngenerate_loopback_tls_certificate()", cleanup_start)
        cleanup_setup = source[cleanup_start:cleanup_end]
        self.assertIn("owned_launch_pending=yes\n    owned_launch_pid=", cleanup_setup)
        self.assertIn(
            'if [ "$owned_launch_pending" = yes ] && [ -z "$owned_launch_pid" ]; then',
            cleanup_setup,
        )

        with tempfile.TemporaryDirectory(prefix="haproxy-htx-pre-assignment-") as temporary:
            root = Path(temporary)
            fake_haproxy = root / "haproxy"
            child_pid_path = root / "pre-assignment-child.pid"
            fake_haproxy.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$$\" > \"$HAPROXY_HTX_PRE_ASSIGNMENT_PID_PATH\"\n"
                "kill -STOP \"$PPID\"\n"
                "trap '' HUP INT TERM\n"
                "exec /bin/sleep 600\n",
                encoding="utf-8",
            )
            fake_haproxy.chmod(0o755)
            script = "\n".join(
                (
                    "set -eu",
                    "HAPROXY_HTX_CHILD_STOP_ATTEMPTS=1",
                    "HAPROXY_HTX_CHILD_STOP_DELAY_SECONDS=0",
                    "upstream_pid=",
                    "upstream_pid_token=",
                    "haproxy_pid=",
                    "haproxy_pid_token=",
                    "haproxy_command_pid=",
                    "haproxy_command_pid_token=",
                    "sync_upstream_pid=",
                    "sync_upstream_pid_token=",
                    "streaming_client_pid=",
                    "streaming_client_pid_token=",
                    "owned_launch_pending=",
                    "owned_launch_pid=",
                    "owned_launch_token=",
                    "owned_launch_label=",
                    "owned_launch_signal_status=",
                    "HAPROXY_BIN=$HAPROXY_HTX_FAKE_HAPROXY",
                    command_setup,
                    cleanup_setup,
                    "start_owned_child \"pre-assignment fixture\" start_haproxy_command -vv",
                    "printf 'unexpected spawn return\\n' >&2",
                    "exit 1",
                )
            )
            process = subprocess.Popen(
                ["/bin/sh", "-c", script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                start_new_session=True,
                env={
                    **os.environ,
                    "HAPROXY_HTX_FAKE_HAPROXY": str(fake_haproxy),
                    "HAPROXY_HTX_PRE_ASSIGNMENT_PID_PATH": str(child_pid_path),
                },
            )
            try:
                deadline = time.monotonic() + 5
                while not child_pid_path.is_file() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(child_pid_path.is_file(), "fixture did not enter the pre-assignment window")
                process.send_signal(signal.SIGTERM)
                process.send_signal(signal.SIGCONT)
                stdout, stderr = process.communicate(timeout=5)
                child_pid = int(child_pid_path.read_text(encoding="utf-8").strip())
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
                self.assertEqual(process.returncode, 143, stdout + stderr)
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.communicate(timeout=5)

    def test_capture_refuses_non_child_pid_without_signalling_it(self) -> None:
        """A captured PID must be a direct child before cleanup can signal it."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        cleanup_start = source.index("read_owned_process_stat_field() {")
        cleanup_end = source.index("\ngenerate_loopback_tls_certificate()", cleanup_start)
        cleanup_setup = source[cleanup_start:cleanup_end]
        script = "\n".join(
            (
                "set -eu",
                "HAPROXY_HTX_CHILD_STOP_ATTEMPTS=1",
                "HAPROXY_HTX_CHILD_STOP_DELAY_SECONDS=0",
                "upstream_pid=",
                "upstream_pid_token=",
                "haproxy_pid=",
                "haproxy_pid_token=",
                "haproxy_command_pid=",
                "haproxy_command_pid_token=",
                "sync_upstream_pid=",
                "sync_upstream_pid_token=",
                "streaming_client_pid=",
                "streaming_client_pid_token=",
                "owned_launch_pending=",
                "owned_launch_pid=",
                "owned_launch_token=",
                "owned_launch_label=",
                "owned_launch_signal_status=",
                cleanup_setup,
                "if capture_owned_child_token \"$HAPROXY_HTX_NON_CHILD_PID\" \"non-child fixture\"; then",
                "    printf 'unexpected capture success\\n' >&2",
                "    exit 1",
                "fi",
                "kill -0 \"$HAPROXY_HTX_NON_CHILD_PID\"",
            )
        )
        non_child = subprocess.Popen(["/bin/sleep", "600"])
        try:
            completed = subprocess.run(
                ["/bin/sh", "-c", script],
                check=False,
                capture_output=True,
                text=True,
                env={**os.environ, "HAPROXY_HTX_NON_CHILD_PID": str(non_child.pid)},
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertIsNone(non_child.poll(), "non-child PID was signalled during capture refusal")
            self.assertIn("refusing to signal unbound non-child fixture PID", completed.stderr)
        finally:
            non_child.kill()
            non_child.wait(timeout=5)

    def test_runtime_exit_trap_remains_active_for_normal_exit(self) -> None:
        """The ordinary EXIT path keeps its single cleanup after the split traps."""
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        setup_start = source.index("cleanup_on_signal() {")
        setup_end = source.index("\ngenerate_loopback_tls_certificate()", setup_start)
        signal_setup = source[setup_start:setup_end]

        completed = subprocess.run(
            [
                "/bin/sh",
                "-c",
                "\n".join(
                    (
                        "set -eu",
                        "cleanup() { printf 'cleanup\\n'; }",
                        signal_setup,
                        "printf 'normal\\n'",
                    )
                ),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "normal\ncleanup\n")

    def test_runtime_signal_traps_terminate_before_host_start(self) -> None:
        """HUP/INT/TERM must not resume the runner after process cleanup.

        The fake binary is interrupted during its version probe.  That point is
        after the real runner has installed its traps, but before it creates an
        upstream or HAProxy listener, so the regression control is host-free.
        """
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        self.assertNotIn("trap cleanup EXIT HUP INT TERM", source)
        self.assertIn("cleanup_on_signal()", source)
        self.assertIn("trap cleanup EXIT", source)
        signal_cases = (
            (signal.SIGHUP, 129, "HUP"),
            (signal.SIGINT, 130, "INT"),
            (signal.SIGTERM, 143, "TERM"),
        )

        for received_signal, expected_status, signal_name in signal_cases:
            with self.subTest(signal=signal_name), tempfile.TemporaryDirectory(
                prefix="haproxy-htx-signal-"
            ) as temporary:
                root = Path(temporary)
                framework_root = root / "framework"
                synchronized_upstream = framework_root / "tests/runners/synchronized_upstream.py"
                canonical_rules = framework_root / "tests/rules/no-crs-baseline.conf"
                synchronized_upstream.parent.mkdir(parents=True)
                canonical_rules.parent.mkdir(parents=True)
                synchronized_upstream.write_text("# fixture is not executed\n", encoding="utf-8")
                canonical_rules.write_text("SecRuleEngine On\n", encoding="utf-8")

                marker = root / "version-probe-entered"
                child_pid_path = root / "version-probe-child.pid"
                fake_haproxy = root / "haproxy"
                fake_haproxy.write_text(
                    "#!/bin/sh\n"
                    "printf 'entered\\n' > \"$HAPROXY_HTX_SIGNAL_MARKER\"\n"
                    "printf '%s\\n' \"$$\" > \"$HAPROXY_HTX_SIGNAL_CHILD_PID_PATH\"\n"
                    "trap '' HUP INT TERM\n"
                    "exec /bin/sleep 600\n",
                    encoding="utf-8",
                )
                fake_haproxy.chmod(0o755)
                provenance = root / "overlay-build.env"
                provenance.write_text("fixture=true\n", encoding="utf-8")
                runtime_root = root / "runtime"
                environment = {
                    **os.environ,
                    "FRAMEWORK_ROOT": str(framework_root),
                    "HAPROXY_BIN": str(fake_haproxy),
                    "HAPROXY_HTX_BUILD_PROVENANCE": str(provenance),
                    "HAPROXY_HTX_CANONICAL_RULES_FILE": str(canonical_rules),
                    "HAPROXY_HTX_SIGNAL_MARKER": str(marker),
                    "HAPROXY_HTX_SIGNAL_CHILD_PID_PATH": str(child_pid_path),
                    "RUNTIME_ROOT": str(runtime_root),
                    "EVENT_LOG_PATH": str(runtime_root / "events.jsonl"),
                    "HAPROXY_HTX_HOST_EVIDENCE_LOG_PATH": str(
                        runtime_root / "host-runtime-evidence.jsonl"
                    ),
                    "FULL_LIFECYCLE_EVIDENCE_OUTPUT": str(
                        runtime_root / "first-byte-evidence.json"
                    ),
                    "NO_CRS_RUN_ID": "signal-contract",
                }
                process = subprocess.Popen(
                    [str(RUNTIME_PATH)],
                    cwd=RUNTIME_PATH.parents[3],
                    env=environment,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True,
                )
                try:
                    deadline = time.monotonic() + 5
                    while not marker.exists() and process.poll() is None and time.monotonic() < deadline:
                        time.sleep(0.01)
                    self.assertTrue(marker.is_file(), "runner did not reach the pre-host version probe")
                    process.send_signal(received_signal)
                    stdout, stderr = process.communicate(timeout=8)
                    self.assertEqual(process.returncode, expected_status, stdout + stderr)
                    self.assertTrue(child_pid_path.is_file(), "fixture did not record the version-probe PID")
                    child_pid = int(child_pid_path.read_text(encoding="utf-8").strip())
                    with self.assertRaises(ProcessLookupError):
                        os.kill(child_pid, 0)
                    self.assertNotIn("patched binary is not HAProxy", stderr)
                    self.assertFalse((runtime_root / "upstream-requests.jsonl").exists())
                    self.assertFalse((runtime_root / "runtime-summary.txt").exists())
                finally:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.communicate(timeout=5)

    def test_runtime_artifacts_stay_in_private_root_and_clients_stay_loopback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = root / "canonical.conf"
            canonical.write_text(
                "\n".join(HELPER.CANONICAL_RULE_SNIPPETS) + "\n",
                encoding="utf-8",
            )
            certificate = root / "loopback-tls.pem"
            certificate.write_text("private test certificate", encoding="utf-8")
            config = root / "haproxy.cfg"
            outside = root.parent / f"{root.name}-outside.conf"
            runtime_root = str(root)
            outside_path = str(outside)
            canonical_path = str(canonical)
            certificate_path = str(certificate)
            with self.assertRaisesRegex(ValueError, "below the runtime root"):
                HELPER.write_rules(runtime_root, outside_path, canonical_path)
            self.assertFalse(outside.exists())

            redirected = root / "redirected.conf"
            redirected.symlink_to(outside)
            redirected_path = str(redirected)
            with self.assertRaisesRegex(ValueError, "below the runtime root|symbolic link"):
                HELPER.write_rules(runtime_root, redirected_path, canonical_path)
            self.assertFalse(outside.exists())

            self.assertEqual(
                HELPER.checked_loopback_https_url("https://127.0.0.1:18080/no-crs/allow"),
                ("127.0.0.1", 18080, "/no-crs/allow"),
            )
            non_loopback_url = "https://example.invalid/"
            with self.assertRaisesRegex(ValueError, "127.0.0.1"):
                HELPER.checked_loopback_https_url(non_loopback_url)
            credential_url = "https://user@127.0.0.1:18080/"
            with self.assertRaisesRegex(ValueError, "credential-free"):
                HELPER.checked_loopback_https_url(credential_url)
            plaintext_url = urllib.parse.urlunsplit(("http", "127.0.0.1:18080", "/", "", ""))
            with self.assertRaisesRegex(ValueError, "https"):
                HELPER.checked_loopback_https_url(plaintext_url)

            self.assertEqual(
                HELPER.write_config(
                    runtime_root, str(config), 18080, 18081, canonical_path, certificate_path,
                ),
                0,
            )
            self.assertIn("bind 127.0.0.1:18080 ssl crt", config.read_text(encoding="utf-8"))

        runtime = (
            Path(__file__).resolve().parents[1]
            / "connectors/haproxy/harness/run_haproxy_htx_runtime.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("helper prepare-runtime-root", runtime)
        self.assertIn('"$@" --runtime-root "$RUNTIME_ROOT"', runtime)
        self.assertIn("generate_loopback_tls_certificate", runtime)
        self.assertIn('--tls-certificate "$TLS_CA_CERTIFICATE_PATH"', runtime)

    def test_probe_requires_verified_loopback_tls_certificate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            key = root / "loopback.key"
            certificate = root / "loopback.crt"
            subprocess.run(
                [
                    "openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-sha256", "-days", "1",
                    "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1",
                    "-keyout", str(key), "-out", str(certificate),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _LoopbackTLSHandler)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile=str(certificate), keyfile=str(key))
            server.socket = context.wrap_socket(server.socket, server_side=True)
            worker = threading.Thread(target=server.serve_forever, daemon=True)
            worker.start()
            try:
                url = f"https://127.0.0.1:{server.server_port}/tls"
                runtime_root = str(root)
                certificate_path = str(certificate)
                self.assertEqual(HELPER.probe(runtime_root, url, [], "GET", None, certificate_path), 0)
            finally:
                server.shutdown()
                worker.join()
                server.server_close()

    def test_native_128_byte_buffer_limit_applies_to_allow_and_evidence_writers(self) -> None:
        accepted = "a" * HELPER.HTX_TRANSACTION_ID_MAX_LENGTH
        rejected = "b" * (HELPER.HTX_TRANSACTION_ID_MAX_LENGTH + 1)
        self.assertEqual(HELPER.safe_htx_transaction_id(accepted), accepted)
        with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
            HELPER.safe_htx_transaction_id(rejected)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "client-probe.json"
            upstream = root / "upstream-requests.jsonl"
            host_evidence = root / "host-runtime-evidence.jsonl"
            decision_log = root / "haproxy.stderr.log"
            events_path = str(events)
            probe_path = str(probe)
            upstream_path = str(upstream)
            host_evidence_path = str(host_evidence)
            decision_log_path = str(decision_log)
            runtime_root = str(root)
            probe.write_text(
                json.dumps({"status": 200, "response_bytes": 24, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            upstream.write_text(
                json.dumps({"profile": "ordinary", "request_id": accepted}) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_allow_event(
                    str(root), events_path, probe_path, upstream_path, accepted,
                ),
                0,
            )
            self.assertEqual(
                json.loads(events.read_text(encoding="utf-8"))["transaction_id"],
                accepted,
            )
            with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
                HELPER.write_allow_event(
                    runtime_root, events_path, probe_path, upstream_path, rejected,
                )

            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                f"transaction_id={accepted} phase=1 status=403 rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_host_evidence(
                    str(root), host_evidence_path, "phase1_403", 1, 1100001, probe_path, 0,
                    "enforced_reply", decision_log_path,
                ),
                0,
            )
            self.assertEqual(
                json.loads(host_evidence.read_text(encoding="utf-8"))["transaction_id"],
                accepted,
            )
            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                f"transaction_id={rejected} phase=1 status=403 rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
                HELPER.write_host_evidence(
                    runtime_root, host_evidence_path, "phase1_403", 1, 1100001, probe_path, 0,
                    "enforced_reply", decision_log_path,
                )


if __name__ == "__main__":
    unittest.main()
