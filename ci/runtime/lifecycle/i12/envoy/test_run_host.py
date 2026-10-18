"""Bounded controller cleanup controls; no Envoy, listener or namespace is started."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import signal
import subprocess
import tempfile
import unittest
from unittest import mock


SPEC = importlib.util.spec_from_file_location("envoy_run_host_controls", Path(__file__).with_name("run_host.py"))
HOST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HOST)


def process_control(*effects, returncode=0, wait_error=None):
    process = mock.Mock(pid=12345, returncode=returncode)
    process.communicate.side_effect = effects
    process.stdout = io.BytesIO()
    process.stderr = io.BytesIO()
    if wait_error is not None:
        process.wait.side_effect = wait_error
    return process


def timeout(seconds, stdout=None, stderr=None):
    return subprocess.TimeoutExpired("synthetic-controller", seconds, output=stdout, stderr=stderr)


class CommunicationControls(unittest.TestCase):
    def test_normal_exit_has_no_cleanup_signal_or_unbounded_wait(self):
        process = process_control((b"finished", b"diagnostic"))
        with mock.patch.object(HOST, "signal_owned_group") as send:
            out, err, state = HOST.communicate_bounded(process, "start-control")
        self.assertEqual((b"finished", b"diagnostic"), (out, err))
        self.assertFalse(state["outer_timeout"])
        self.assertFalse(state["cleanup_requires_review"])
        process.communicate.assert_called_once_with(timeout=300)
        process.wait.assert_not_called()
        send.assert_not_called()

    def test_first_timeout_remains_timeout_when_child_exits_zero_during_grace(self):
        process = process_control(timeout(300, b"partial", b"initial"), (b"complete", b"final"))
        with mock.patch.object(HOST, "signal_owned_group", return_value=True) as send:
            out, err, state = HOST.communicate_bounded(process, "owned-start")
        self.assertEqual((b"complete", b"final"), (out, err))
        self.assertTrue(state["outer_timeout"])
        self.assertTrue(state["term_sent_to_owned_group"])
        self.assertFalse(state["cleanup_grace_timeout"])
        self.assertEqual(0, process.returncode)
        self.assertEqual([mock.call(timeout=300), mock.call(timeout=30)],
                         process.communicate.call_args_list)
        process.wait.assert_not_called()
        send.assert_called_once_with(process, "owned-start", signal.SIGTERM)

    def test_second_timeout_preserves_latest_cumulative_output_and_bounded_reap(self):
        process = process_control(timeout(300, b"first-out", b"first-err"),
                                  timeout(30, b"first-out\nlast-out", b"first-err\nlast-err"), returncode=-9)
        with mock.patch.object(HOST, "signal_owned_group", return_value=True) as send:
            out, err, state = HOST.communicate_bounded(process, "owned-start")
        self.assertEqual((b"first-out\nlast-out", b"first-err\nlast-err"), (out, err))
        self.assertTrue(state["outer_timeout"])
        self.assertTrue(state["cleanup_grace_timeout"])
        self.assertTrue(state["cleanup_requires_review"])
        self.assertTrue(state["direct_child_reaped"])
        self.assertEqual([mock.call(process, "owned-start", signal.SIGTERM),
                                               mock.call(process, "owned-start", signal.SIGKILL)], send.call_args_list)
        process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(2, process.communicate.call_count)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_second_timeout_falls_back_independently_for_each_pipe(self):
        for second_out, second_err, expected in ((None, b"new-err", (b"first-out", b"new-err")),
                                               (b"new-out", None, (b"new-out", b"first-err")),
                                               (None, None, (b"first-out", b"first-err"))):
            with self.subTest(second_out=second_out, second_err=second_err):
                process = process_control(timeout(300, b"first-out", b"first-err"),
                                          timeout(30, second_out, second_err))
                with mock.patch.object(HOST, "signal_owned_group", return_value=False):
                    out, err, state = HOST.communicate_bounded(process, None)
                self.assertEqual(expected, (out, err))
                self.assertFalse(state["kill_sent_to_owned_group"])
                self.assertTrue(state["cleanup_requires_review"])

    def test_unreaped_child_is_explicit_unknown_cleanup_and_does_not_block(self):
        process = process_control(timeout(300), timeout(30), returncode=None,
                                  wait_error=timeout(5))
        with mock.patch.object(HOST, "signal_owned_group", return_value=False):
            out, err, state = HOST.communicate_bounded(process, None)
        self.assertEqual((b"", b""), (out, err))
        self.assertFalse(state["direct_child_reaped"])
        self.assertTrue(state["cleanup_requires_review"])
        self.assertIsNone(process.returncode)
        process.wait.assert_called_once_with(timeout=5)
        self.assertEqual(2, process.communicate.call_count)
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)


class OwnedProcessGroupControls(unittest.TestCase):
    def test_missing_or_changed_start_identity_never_signals(self):
        for started, current in ((None, "known"), ("original", None), ("original", "replacement")):
            with self.subTest(started=started, current=current):
                process = mock.Mock(pid=12345)
                with mock.patch.object(HOST, "identity", return_value=current), \
                     mock.patch.object(HOST.os, "getpgid") as pgid, \
                     mock.patch.object(HOST.os, "killpg") as kill:
                    self.assertFalse(HOST.signal_owned_group(process, started, signal.SIGKILL))
                pgid.assert_not_called()
                kill.assert_not_called()

    def test_nonleader_pgid_cannot_signal_another_process_group(self):
        process = mock.Mock(pid=12345)
        with mock.patch.object(HOST, "identity", return_value="owned-start"), \
             mock.patch.object(HOST.os, "getpgid", return_value=999), \
             mock.patch.object(HOST.os, "killpg") as kill:
            self.assertFalse(HOST.signal_owned_group(process, "owned-start", signal.SIGTERM))
        kill.assert_not_called()

    def test_owned_leader_is_the_only_signal_target(self):
        process = mock.Mock(pid=12345)
        with mock.patch.object(HOST, "identity", return_value="owned-start"), \
             mock.patch.object(HOST.os, "getpgid", return_value=12345), \
             mock.patch.object(HOST.os, "killpg") as kill:
            self.assertTrue(HOST.signal_owned_group(process, "owned-start", signal.SIGKILL))
        kill.assert_called_once_with(12345, signal.SIGKILL)

    def test_disappearing_process_before_group_lookup_or_signal_is_safe(self):
        process = mock.Mock(pid=12345)
        for step in ("getpgid", "killpg"):
            with self.subTest(step=step), \
                 mock.patch.object(HOST, "identity", return_value="owned-start"), \
                 mock.patch.object(HOST.os, "getpgid", return_value=12345) as pgid, \
                 mock.patch.object(HOST.os, "killpg") as kill:
                (pgid if step == "getpgid" else kill).side_effect = ProcessLookupError()
                self.assertFalse(HOST.signal_owned_group(process, "owned-start", signal.SIGTERM))
                if step == "getpgid":
                    kill.assert_not_called()


class ControllerPacketControls(unittest.TestCase):
    def test_malformed_packet_does_not_discard_prior_or_subsequent_complete_packet(self):
        first = {"attempt": "first", "exitcode": 0}
        last = {"attempt": "last", "exitcode": 1}
        lines = ["ordinary diagnostic", json.dumps(first, separators=(",", ":")),
                 '{"attempt":"truncated', json.dumps(last, separators=(",", ":"))]
        packets, errors = HOST.controller_packets("\n".join(lines))
        self.assertEqual([first, last], packets)
        self.assertEqual(1, errors)

    def test_ordinary_diagnostics_never_become_controller_packets(self):
        self.assertEqual(([], 0), HOST.controller_packets("diagnostic\nnot JSON\n"))


class TimeoutRecordControls(unittest.TestCase):
    def setUp(self):
        external = Path("/var/tmp/codex/ModSecurity-conector")
        temp = tempfile.TemporaryDirectory(prefix="envoy-run-host-control-",
                                           dir=external if external.is_dir() else None)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        controller = self.root / "controller.py"
        controller.write_text("# Inert synthetic control; never executed\n")
        self.matrix = self.root / "matrix.json"
        self.matrix.write_text(json.dumps({"parent_sha": "control-parent",
            "controller": str(controller), "controller_sha256": hashlib.sha256(controller.read_bytes()).hexdigest(),
            "scenarios": [{"label": "bounded-control", "spec": "synthetic-unused-spec"}]}))
        self.output = self.root / "result.json"

    def run_main(self, process):
        argv = ["run-host-control", "--matrix", str(self.matrix), "--output", str(self.output)]
        with mock.patch("sys.argv", argv), mock.patch.object(HOST.subprocess, "Popen", return_value=process), \
             mock.patch.object(HOST, "identity", return_value="owned-start"), \
             mock.patch.object(HOST, "signal_owned_group", return_value=False), \
             contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as stopped:
            HOST.main()
        self.assertEqual(1, stopped.exception.code)
        result = json.loads(self.output.read_text())
        self.assertEqual("unreviewed_host_measurements", result["qualification"])
        self.assertEqual(1, len(result["runs"]))
        return result["runs"][0]

    def test_outer_timeout_cannot_be_pass_even_with_zero_child_and_controller_results(self):
        complete = b'{"attempt":"control-attempt","exitcode":0,"timeout":false}\n'
        process = process_control(timeout(300), (complete, b"diagnostic"), returncode=0)
        record = self.run_main(process)
        self.assertEqual(124, record["exit_code"])
        self.assertEqual(0, record["process_exit_code"])
        self.assertEqual(0, record["controller_result"]["exitcode"])
        self.assertTrue(record["timeout_state"]["outer_timeout"])
        self.assertNotIn("PASS", json.dumps(record))

    def test_second_timeout_retains_bytes_hashes_and_unknown_cleanup_record(self):
        out, err = b"partial-controller-output\n", b"partial-controller-error\n"
        process = process_control(timeout(300, out, err), timeout(30), returncode=None,
                                  wait_error=timeout(5))
        record = self.run_main(process)
        self.assertEqual(124, record["exit_code"])
        self.assertIsNone(record["process_exit_code"])
        self.assertIsNone(record["controller_result"])
        self.assertTrue(record["timeout_state"]["cleanup_requires_review"])
        self.assertFalse(record["timeout_state"]["direct_child_reaped"])
        self.assertEqual(hashlib.sha256(out).hexdigest(), record["stdout_sha256"])
        self.assertEqual(hashlib.sha256(err).hexdigest(), record["stderr_sha256"])
        self.assertEqual(out, (self.root / "result-bounded-control.stdout").read_bytes())
        self.assertEqual(err, (self.root / "result-bounded-control.stderr").read_bytes())
        process.wait.assert_called_once_with(timeout=5)

    def test_malformed_packet_with_zero_process_exit_is_nonzero125(self):
        out = b'{"attempt":"unfinished-controller'
        record = self.run_main(process_control((out, b"diagnostic"), returncode=0))
        self.assertEqual(125, record["exit_code"])
        self.assertEqual(0, record["process_exit_code"])
        self.assertFalse(record["timeout_state"]["outer_timeout"])
        self.assertEqual(1, record["controller_packet_parse_errors"])
        self.assertIsNone(record["controller_result"])

    def test_partial_non_utf8_output_is_retained_byte_exact_with_matching_hash(self):
        out, err = b"partial\xffcontroller\n", b"partial\xfeerror\n"
        process = process_control(timeout(300, out, err), timeout(30), returncode=None,
                                  wait_error=timeout(5))
        record = self.run_main(process)
        self.assertEqual(124, record["exit_code"])
        stdout = (self.root / "result-bounded-control.stdout").read_bytes()
        stderr = (self.root / "result-bounded-control.stderr").read_bytes()
        self.assertEqual(out, stdout)
        self.assertEqual(err, stderr)
        self.assertEqual(hashlib.sha256(stdout).hexdigest(), record["stdout_sha256"])
        self.assertEqual(hashlib.sha256(stderr).hexdigest(), record["stderr_sha256"])

    def test_truncated_controller_json_keeps_timeout_record_and_raw_output(self):
        out = b'{"attempt":"unfinished-controller'
        process = process_control(timeout(300, out, b"diagnostic"), timeout(30), returncode=None,
                                  wait_error=timeout(5))
        record = self.run_main(process)
        self.assertEqual(124, record["exit_code"])
        self.assertIsNone(record["controller_result"])
        self.assertEqual(1, record["controller_packet_parse_errors"])
        self.assertTrue(record["timeout_state"]["cleanup_requires_review"])
        self.assertEqual(out, (self.root / "result-bounded-control.stdout").read_bytes())


if __name__ == "__main__":
    unittest.main()
