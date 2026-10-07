"""Contracts for the native Apache qualification runner; no httpd is started."""
import importlib.util
from concurrent.futures import ThreadPoolExecutor
import http.client
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch

RUNNER = Path(__file__).resolve().parents[1] / "connectors/apache/harness/apache_qualification.py"
SPEC = importlib.util.spec_from_file_location("apache_qualification", RUNNER)
qualification = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qualification)
TEMP_ROOT = "/var/tmp/codex/ModSecurity-conector/tmp"


def temporary_directory():
    return tempfile.TemporaryDirectory(dir=TEMP_ROOT)


def valid_decision(rule="991001", phase="request_headers", status=403, body_limit=False):
    result = {"connector": "apache", "integration_mode": "native-httpd-module",
              "rule_id": "" if body_limit else rule, "phase": phase, "action": "deny",
              "requested_action": "deny", "actual_action": "deny", "status": "blocked",
              "http_status": status, "visible_http_status": status, "transport_result": "http_status",
              "response_committed": False, "late_intervention": False, "headers_sent": False,
              "connection_aborted": False, "truncated": False,
              "body_truncated": body_limit and phase == "response_body"}
    if body_limit:
        result.update(event="body_limit", body_limit_outcome="reject")
    return result


def valid_safe_p4():
    return {"connector": "apache", "integration_mode": "native-httpd-module",
            "event": "phase4_intervention", "phase": "response_body", "rule_id": "991004",
            "status": "blocked", "requested_action": "deny", "action": "log_only",
            "actual_action": "log_only", "http_status": 403, "original_http_status": 200,
            "visible_http_status": 200, "transport_result": "log_only", "reason": "response_committed_safe",
            "late_intervention_mode": "safe", "late_intervention": True, "response_started": True,
            "response_committed": True, "headers_sent": True, "body_started": True, "eos_seen": True,
            "body_bytes_seen": 21, "body_bytes_inspected": 21, "body_truncated": False,
            "connection_aborted": False, "client_disconnected": False, "upstream_disconnected": False,
            "cancelled": False, "redacted": False, "truncated": False}


def valid_overlimit():
    value = valid_safe_p4()
    value.update(message_id="MSCONN_EVENT_BODY_LIMIT", event="body_limit", rule_id="",
                 action="abort_connection", actual_action="abort_connection", http_status=500,
                 transport_result="connection_aborted", reason="request_body_limit_exceeded",
                 uri="/response/1025", method="GET", content_type="text/plain",
                 body_bytes_seen=1025, body_bytes_inspected=0, body_limit_outcome="reject",
                 body_truncated=True, connection_aborted=True)
    return value


def valid_precommit_overlimit():
    value = valid_overlimit()
    value.update(action="deny", actual_action="deny", visible_http_status=500,
                 transport_result="http_status", late_intervention=False, response_started=False,
                 response_committed=False, headers_sent=False, body_started=False, connection_aborted=False)
    del value["late_intervention_mode"]
    return value


class ApacheQualificationTest(unittest.TestCase):
    def test_security_module_load_precedes_external_include_and_duplicate_is_fatal(self):
        text = qualification.config(Path("/run/owned"), Path("/mod_security3.so"), Path("/modules.conf"), 8000, 8001)
        self.assertLess(text.index("LoadModule security3_module"), text.index("Include "))
        qualification.reject_security_module_preload(b"Syntax OK\n")
        with self.assertRaises(RuntimeError):
            qualification.reject_security_module_preload(b"AH01574: module security3_module is already loaded, skipping\n")

    def test_mapped_module_requires_exact_path_device_inode_and_live_hash(self):
        with temporary_directory() as directory:
            module = Path(directory) / "mod_security3.so"
            module.write_bytes(b"pinned module")
            pin = qualification.input_identity(module)
            info = module.stat()
            line = f"1000-2000 r-xp 00000000 {os.major(info.st_dev):x}:{os.minor(info.st_dev):x} {info.st_ino} {module}\n"
            qualification.assert_mapped_module(line, module, pin)
            for changed in ("", line.replace(str(info.st_ino), str(info.st_ino + 1)),
                            line.replace(str(module), str(module) + " (deleted)"),
                            line.replace(str(module), str(module.parent / "other.so")),
                            line.replace(f"{os.major(info.st_dev):x}:{os.minor(info.st_dev):x}", "ff:ff"),
                            line + line.replace(str(module), str(module.parent / "alternate_security3.so"))):
                with self.subTest(maps=changed), self.assertRaises(RuntimeError):
                    qualification.assert_mapped_module(changed, module, pin)
            module.write_bytes(b"changed module")
            with self.assertRaises(RuntimeError):
                qualification.assert_mapped_module(line, module, pin)

    def test_input_pin_rejects_identical_byte_replacement_between_starts(self):
        with temporary_directory() as directory:
            path = Path(directory) / "module.so"
            path.write_bytes(b"same bytes")
            pin = qualification.input_identity(path)
            replacement = path.with_name("replacement.so")
            replacement.write_bytes(b"same bytes")
            replacement.replace(path)
            with self.assertRaises(RuntimeError):
                qualification.verify_input_identity(path, pin)

    def test_external_include_preload_is_rejected_before_host_launch(self):
        host = object.__new__(qualification.Host)
        host.root, host.port = Path("/run/owned"), 19000
        host.args = Mock(module=Path("/mod_security3.so"), modules_config=Path("/modules.conf"),
                         httpd=Path("/httpd"))
        host.origin = Mock(server_port=19001)
        host.env = {}
        syntax = subprocess.CompletedProcess([], 0, b"", b"AH01574: module security3_module is already loaded, skipping\nSyntax OK\n")
        with patch.object(qualification, "verify_inputs") as verify, \
                patch.object(qualification, "private_mkdir"), \
                patch.object(qualification, "private_write"), \
                patch.object(qualification.subprocess, "run", return_value=syntax), \
                patch.object(qualification.subprocess, "Popen") as launch:
            with self.assertRaisesRegex(RuntimeError, "loaded more than once"):
                host.start()
            verify.assert_called_once_with(host.args)
            launch.assert_not_called()

    def test_disjoint_overlimit_timing_branches_reject_every_mixed_event(self):
        qualification.assert_response_overlimit([valid_precommit_overlimit()], "before_commit")
        qualification.assert_response_overlimit([valid_overlimit()], "after_commit")
        for event, branch in ((valid_precommit_overlimit(), "after_commit"),
                              (valid_overlimit(), "before_commit")):
            with self.subTest(branch=branch), self.assertRaises(RuntimeError):
                qualification.assert_response_overlimit([event], branch)
        before, after = valid_precommit_overlimit(), valid_overlimit()
        for field in ("action", "actual_action", "visible_http_status", "transport_result",
                      "late_intervention", "response_started", "response_committed",
                      "headers_sent", "body_started", "connection_aborted"):
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                qualification.assert_response_overlimit([{**before, field: after[field]}], "before_commit")

    def test_aftercommit_wire_receipt_and_log_are_bound_together(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.resource_lock = threading.Lock()
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 1
        for event, allowed in ((valid_overlimit(), True), (valid_precommit_overlimit(), False)):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 200 OK\r\nContent-Length: 1025\r\n\r\n"))))
            response.begin()
            client = Mock()
            client.getresponse.return_value = response
            with patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                    patch.object(qualification, "events", return_value=[event]):
                if allowed:
                    case = host.request("response-body-1025", None, path="/response/1025", response_overlimit=True)
                    self.assertEqual(case["status"], 200)
                    self.assertEqual(case["response_overlimit_branch"], "after_commit")
                    self.assertEqual(case["response_remaining_bytes"], 1025)
                    self.assertFalse(case["response_framing_complete"])
                else:
                    with self.assertRaises(RuntimeError):
                        host.request("response-body-1025", None, path="/response/1025", response_overlimit=True)
        message = ("ModSecurity: Phase 4 response gate failed after response commit: "
                   "response body exceeds modsecurity_phase4_body_limit")
        with patch.object(Path, "glob", return_value=[Path("/run/error.log")]):
            with patch.object(qualification, "bounded_read", return_value=message.encode()):
                qualification.reconcile_logs(host.root, [case])
                for changed in ({"response_overlimit_branch": "before_commit"}, {"status": 500},
                                {"response_framing_complete": True}, {"response_body_bytes": 1},
                                {"events": [valid_precommit_overlimit()]}):
                    with self.subTest(changed=changed), self.assertRaises(RuntimeError):
                        qualification.reconcile_logs(host.root, [{**case, **changed}])
            for wire in (message.replace("after response commit", "before response commit"),
                         message + "\n" + message, message + " trailing"):
                with patch.object(qualification, "bounded_read", return_value=wire.encode()), \
                        self.assertRaises(RuntimeError):
                    qualification.reconcile_logs(host.root, [case])

    def test_deterministic_local_error_document_is_full_bounded_500(self):
        wanted = b"qualification-apache-local-error-500"
        for body, allowed in ((wanted, True), (b"", False), (wanted[:-1], False),
                              (b"x" * len(wanted), False), (b"<html>dynamic page</html>", False)):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: " +
                str(len(wanted)).encode() + b"\r\n\r\n" + body))))
            response.begin()
            with self.subTest(body=body):
                if allowed:
                    self.assertEqual(qualification.bounded_overlimit_body(response, "local-error"), wanted)
                else:
                    with self.assertRaises(RuntimeError):
                        qualification.bounded_overlimit_body(response, "local-error")
                self.assertEqual(response.qualification_wire["status"], 500)
        generated = qualification.config(Path("/run/owned"), Path("/module.so"), Path("/modules.conf"), 8000, 8001)
        self.assertIn('ErrorDocument 500 "qualification-apache-local-error-500"', generated)

    def test_failed_attempt_receipts_reconcile_without_accepting_unknown_records(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.resource_lock = threading.Lock()
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 1
        response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
            b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: 4\r\n\r\nnope"))))
        response.begin()
        client = Mock()
        client.getresponse.return_value = response
        with patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                patch.object(qualification, "events", return_value=[valid_precommit_overlimit()]):
            with self.assertRaisesRegex(RuntimeError, "ErrorDocument"):
                host.request("response-body-1025", None, path="/response/1025", response_overlimit=True)
        self.assertEqual(host.case_results, [])
        self.assertEqual(len(host.probe_failures), 1)
        attempt = host.probe_failures[0]
        self.assertEqual(attempt["wire"]["body_bytes"], 4)
        self.assertEqual(attempt["wire"]["body_sha256"], hashlib.sha256(b"nope").hexdigest())
        data = json.dumps(attempt["events"][0]).encode() + b"\n"
        with patch.object(Path, "exists", return_value=True), \
                patch.object(qualification, "bounded_read", return_value=data):
            qualification.reconcile_final(host.root, host.probe_failures, {attempt["token"]: 1}, [])
            for receipts in ({attempt["token"]: 1, "unknown": 1}, {attempt["token"]: 2}):
                with self.assertRaises(RuntimeError):
                    qualification.reconcile_final(host.root, host.probe_failures, receipts, [])
        with patch.object(Path, "exists", return_value=True), \
                patch.object(qualification, "bounded_read", return_value=data + b'{"transaction_id":"unknown"}\n'), \
                self.assertRaises(RuntimeError):
            qualification.reconcile_final(host.root, host.probe_failures, {attempt["token"]: 1}, [])
    def test_overlimit_200_abort_requires_zero_body_and_exact_internal_events(self):
        for body in (b"", b"x", b"x" * 1025):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 200 OK\r\nContent-Length: 1025\r\n\r\n" + body))))
            response.begin()
            with self.subTest(body_bytes=len(body)):
                if not body:
                    self.assertEqual(qualification.bounded_overlimit_body(response, "overlimit"), b"")
                    self.assertEqual(response.qualification_wire["branch"], "after_commit")
                else:
                    with self.assertRaises(RuntimeError):
                        qualification.bounded_overlimit_body(response, "overlimit")
        qualification.assert_response_overlimit([valid_overlimit()])
        for field, value in valid_overlimit().items():
            if field in ("transaction_id", "timestamp", "message", "level"):
                continue
            replacement = not value if type(value) is bool else value + 1 if type(value) is int else "wrong"
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                qualification.assert_response_overlimit([{**valid_overlimit(), field: replacement}])
        for observed in ([], [valid_overlimit(), valid_overlimit()], [valid_safe_p4()]):
            with self.subTest(event_count=len(observed)), self.assertRaises(RuntimeError):
                qualification.assert_response_overlimit(observed)

    def test_overlimit_rejects_wrong_status_ambiguous_headers_timeout_and_reset(self):
        for headers, status in ((b"Content-Length: 1024\r\n", 200),
                                (b"Content-Length: 1025\r\n", 500),
                                (b"Content-Length: 1025\r\nContent-Length: 1025\r\n", 200),
                                (b"Content-Length: 1025\r\nTransfer-Encoding: chunked\r\n", 200),
                                (b"Transfer-Encoding: chunked\r\n", 200),
                                (b"Connection: close\r\n", 200)):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                f"HTTP/1.1 {status} Status\r\n".encode() + headers + b"\r\n"))))
            response.begin()
            with self.subTest(headers=headers, status=status), self.assertRaises(RuntimeError):
                qualification.bounded_overlimit_body(response, "overlimit")
        for error in (TimeoutError("timeout"), ConnectionResetError("reset")):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 200 OK\r\nContent-Length: 1025\r\n\r\n"))))
            response.begin()
            with patch.object(response, "read", side_effect=error), self.assertRaises(type(error)):
                qualification.bounded_overlimit_body(response, "overlimit")
            self.assertEqual(response.qualification_wire["termination"],
                             "timeout" if isinstance(error, TimeoutError) else "reset")
            response.close()

    def test_primary_probe_and_cleanup_failures_both_survive(self):
        host = Mock()
        probe, cleanup = RuntimeError("original framing probe"), RuntimeError("secondary cleanup log")
        host.stop.side_effect = cleanup
        with patch.object(qualification, "exercise", side_effect=probe):
            with self.assertRaises(ExceptionGroup) as caught:
                qualification.run_host_campaign(host, True)
        self.assertEqual(caught.exception.exceptions, (probe, cleanup))
        description = qualification.describe_failure(caught.exception)
        self.assertIn("original framing probe", description)
        self.assertIn("secondary cleanup log", description)
        host.stop.assert_called_once()

    def test_overlimit_dispatch_records_exact_local_500_and_followup(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.resource_lock = threading.Lock()
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 1
        wanted = qualification.LOCAL_ERROR_BODY
        for body, allowed in ((wanted, True), (b"x" * len(wanted), False)):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 500 Internal Server Error\r\nContent-Length: " +
                str(len(wanted)).encode() + b"\r\n\r\n" + body))))
            response.begin()
            client = Mock()
            client.getresponse.return_value = response
            with patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                    patch.object(qualification, "events", return_value=[valid_precommit_overlimit()]):
                if allowed:
                    result = host.request("response-body-1025", None, path="/response/1025", response_overlimit=True)
                    self.assertEqual(result["status"], 500)
                    self.assertEqual(result["response_body_bytes"], len(wanted))
                    self.assertEqual(result["response_declared_bytes"], len(wanted))
                    self.assertEqual(result["response_remaining_bytes"], 0)
                    self.assertTrue(result["response_framing_complete"])
                    self.assertEqual(result["response_termination"], "local_error_document_complete")
                else:
                    with self.assertRaises(RuntimeError):
                        host.request("response-body-1025", None, path="/response/1025", response_overlimit=True)
                    self.assertEqual(host.probe_failures[-1]["wire"]["body_bytes"], len(wanted))
                    self.assertEqual(host.probe_failures[-1]["backend_delta"], 1)
                    self.assertEqual(host.probe_failures[-1]["events"], [valid_precommit_overlimit()])
        host = Mock()
        host.request.side_effect = lambda *_args, **_kwargs: {}
        host.origin.parallel_peak, host.origin.parallel_errors = 4, []
        with patch.object(qualification, "exercise_keepalive", return_value=[]):
            qualification.exercise(host, True)
        names = [call.args[0] for call in host.request.call_args_list]
        overlimit = host.request.call_args_list[names.index("response-body-1025")]
        self.assertIsNone(overlimit.args[1])
        self.assertTrue(overlimit.kwargs["response_overlimit"])
        self.assertEqual(names[names.index("response-body-1025") + 1], "response-error-followup-allow")
    def test_header_parser_400_requires_empty_correlated_events(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.resource_lock = threading.Lock()
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 0
        candidates = ([], [valid_decision()],
                      [valid_decision(phase="request_body", status=413, body_limit=True)],
                      [{"event": "connector_error"}], [{"event": "unknown"}],
                      [valid_decision(), valid_decision()])
        for observed in candidates:
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\n\r\n"))))
            response.begin()
            client = Mock()
            client.getresponse.return_value = response
            with self.subTest(events=observed), \
                    patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                    patch.object(qualification, "events", return_value=observed):
                if observed:
                    with self.assertRaisesRegex(RuntimeError, "unexpectedly emitted an intervention"):
                        host.request("header-line-258", 400, 0)
                else:
                    result = host.request("header-line-258", 400, 0)
                    self.assertEqual(result["events"], [])
                    self.assertEqual(result["backend_delta"], 0)
        self.assertEqual(len(host.case_results), 1)

    def test_strict_wire_rejects_malformed_names_fold_and_parser_defects(self):
        headers = (b"malformed\r\nContent-Length: 2\r\n", b"Content-Length : 1\r\n",
                   b" Content-Length: 1\r\n", b"X-Test: x\r\n folded\r\n",
                   b"X Test: value\r\n", b"Content-Length: 1\r\nContent-Length: 2\r\n",
                   b"Content-Length: 1\r\nTransfer-Encoding: chunked\r\n")
        for selected in headers:
            with self.subTest(headers=selected), self.assertRaises(RuntimeError):
                response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                    b"HTTP/1.1 200 OK\r\n" + selected + b"\r\nx"))))
                response.begin()
                qualification.bounded_response_body(response, "wire")
        response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
            b"HTTP/1.1 200 OK\r\nContent-Length: 1\r\nX-Test: valid\tvalue\r\n\r\nx"))))
        response.begin()
        self.assertEqual(qualification.bounded_response_body(response, "wire"), b"x")
        response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(b""))))
        response.headers = http.client.HTTPMessage()
        response.headers.defects.append(ValueError("defect"))
        with patch.object(http.client.HTTPResponse, "begin"), self.assertRaisesRegex(RuntimeError, "defective"):
            response.begin()

    def test_exact_expected_response_limit_log_only_once(self):
        message = ("ModSecurity: Phase 4 response gate failed before response commit: "
                   "response body exceeds modsecurity_phase4_body_limit")
        case = {"case": "response-body-1025", "status": 500, "backend_delta": 1,
                "events": [valid_precommit_overlimit()], "response_body_bytes": len(qualification.LOCAL_ERROR_BODY),
                "response_body_sha256": hashlib.sha256(qualification.LOCAL_ERROR_BODY).hexdigest(),
                "response_declared_bytes": len(qualification.LOCAL_ERROR_BODY), "response_remaining_bytes": 0,
                "response_framing_complete": True, "response_termination": "local_error_document_complete",
                "response_overlimit_branch": "before_commit"}
        prefix = "[Thu Oct 01 00:00:00.000 2026] [modsecurity:error] [pid 123] [client 127.0.0.1:1] "
        with patch.object(Path, "glob", return_value=[Path("/run/error.log")]):
            with patch.object(qualification, "bounded_read", return_value=(prefix + message + "\n").encode()):
                qualification.reconcile_logs(Path("/run"), [case])
                for cases in ([], [case, case], [{**case, "status": 200}],
                              [{**case, "backend_delta": 0}], [{**case, "case": "unexpected"}],
                              [{**case, "response_body_bytes": 1}], [{**case, "response_framing_complete": False}],
                              [{**case, "response_termination": "timeout"}],
                              [{**case, "events": [valid_safe_p4()]}]):
                    with self.subTest(cases=cases), self.assertRaises(RuntimeError):
                        qualification.reconcile_logs(Path("/run"), cases)
            for wire in (message + " trailing", message.replace("body exceeds", "engine failed"),
                         message + "\n" + message, "[core:crit] " + message, "",
                         message.replace("before response commit", "after response commit")):
                with self.subTest(wire=wire), patch.object(qualification, "bounded_read", return_value=wire.encode()), \
                        self.assertRaises(RuntimeError):
                    qualification.reconcile_logs(Path("/run"), [case])

    def test_strict_real_httpresponse_chunk_wires(self):
        prefix = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n"
        invalid = (b"0\r\n", b"0\n\n", b"1\r\nxXX0\r\n\r\n",
                   b"1\r\nx\r\n0\r\n", b"1\nx\n0\n\n", b"q\r\n",
                   b"3\r\nx\r\n", b"0\r\nX-Trailer: value\r\n\r\n")
        for body in invalid:
            with self.subTest(wire=body), self.assertRaises(RuntimeError):
                response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(prefix + body))))
                response.begin()
                qualification.bounded_response_body(response, "probe")
        for wire, wanted in ((b"0\r\n\r\n", b""),
                             (b"1\r\nx\r\n2\r\nyz\r\n0\r\n\r\n", b"xyz")):
            response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(prefix + wire))))
            response.begin()
            self.assertEqual(qualification.bounded_response_body(response, "probe"), wanted)
            self.assertTrue(response.isclosed())

    def test_wire_header_lf_and_metadata_bound_rejected(self):
        for wire in (b"HTTP/1.1 200 OK\nContent-Length: 0\n\n",
                     b"HTTP/1.1 200 OK\r\nContent-Length: 0\n\r\n",
                     b"HTTP/1.1 200 OK\r\nX: " + b"x" * 65536 + b"\r\n\r\n"):
            with self.subTest(wire_bytes=len(wire)), self.assertRaises(RuntimeError):
                response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(wire))))
                response.begin()

    def test_controlled_httpd_reap_rejects_early_exit_and_sigkill(self):
        valid = {"pid": 123, "exit_status": 0, "signals": [15], "reaped": True}
        qualification.assert_controlled_exit(valid, 123)
        qualification.assert_controlled_exit({**valid, "exit_status": -15}, 123)
        for changed in ({"signals": []}, {"signals": [15, 9]}, {"exit_status": -9},
                        {"exit_status": 1}, {"exit_status": None}, {"reaped": False},
                        {"pid": 124}, {"exit_status": False}):
            with self.subTest(changed=changed), self.assertRaises(RuntimeError):
                qualification.assert_controlled_exit({**valid, **changed}, 123)

    def test_guard_observer_publishes_actual_httpd_status_and_signals(self):
        for status, signals in ((0, [15]), (-15, [15]), (-9, [15, 9]), (0, [])):
            with self.subTest(status=status, signals=signals):
                child = Mock(pid=123, returncode=status)
                child.poll.return_value = status
                guard = Mock()

                def session(target, *_args):
                    for sig in signals:
                        guard._send_child_signal(77, target, sig)
                    return 0

                guard._run_supervisor_session = session
                guard.supervise.side_effect = lambda *_args: guard._run_supervisor_session(child)
                with patch.object(qualification, "private_write") as publish:
                    qualification.observed_supervise(guard, Path("/httpd"), Path("/run"),
                                                      Path("/run/state"), Path("/run/pid"))
                actual = json.loads(publish.call_args.args[1])
                self.assertEqual(actual, {"pid": 123, "exit_status": status,
                                          "signals": signals, "reaped": True})

    def test_stop_checks_identity_before_signal_and_rejects_early_exit(self):
        host = object.__new__(qualification.Host)
        host.root, host.pid = Path("/run"), 123
        host.monitor_stop = threading.Event()
        host.monitor_failures = []
        host.process = Mock()
        host.process.poll.return_value = 0
        host.process.wait.return_value = 0
        host.control = Mock()
        host.guard = Mock()
        exit_data = b'{"pid":123,"exit_status":0,"signals":[15],"reaped":true}'
        with patch.object(Path, "exists", return_value=True), \
                patch.object(qualification, "bounded_read", return_value=exit_data), \
                self.assertRaisesRegex(RuntimeError, "liveness/identity"):
            host.stop()
        host.control.sendall.assert_called_once_with(b"stop\n")
        host.process.wait.assert_called_once()
        host.guard.assert_called_once_with("verify-stopped", "--evidence", "/run/identity.json")

    def test_response_boundaries_require_exact_body_and_eos(self):
        host = Mock()
        host.request.side_effect = lambda *_args, **_kwargs: {}
        host.origin.parallel_peak, host.origin.parallel_errors = 4, []
        with patch.object(qualification, "exercise_keepalive", return_value=[]):
            qualification.exercise(host, True)
        calls = {call.args[0]: call for call in host.request.call_args_list}
        for size in (1023, 1024):
            self.assertEqual(calls[f"response-body-{size}"].kwargs["expected_body"], b"x" * size)
            for body in (b"x" * size, b"y" + b"x" * (size - 1), b"x" * (size - 1)):
                response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                    b"HTTP/1.1 200 OK\r\nContent-Length: " + str(size).encode() + b"\r\n\r\n" + body))))
                response.begin()
                if len(body) != size:
                    with self.assertRaises(RuntimeError):
                        qualification.bounded_response_body(response, "boundary")
                else:
                    actual = qualification.bounded_response_body(response, "boundary")
                    self.assertEqual(actual == b"x" * size, body == b"x" * size)

    def test_boundary_dispatch_rejects_equal_length_body_mutation(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.resource_lock = threading.Lock()
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 1
        for size in (1023, 1024):
            for mutated in (False, True):
                body = (b"y" if mutated else b"x") + b"x" * (size - 1)
                response = qualification.StrictHTTPResponse(Mock(makefile=Mock(return_value=io.BytesIO(
                    b"HTTP/1.1 200 OK\r\nContent-Length: " + str(size).encode() + b"\r\n\r\n" + body))))
                response.begin()
                client = Mock()
                client.getresponse.return_value = response
                with self.subTest(size=size, mutated=mutated), \
                        patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                        patch.object(qualification, "events", return_value=[]):
                    if mutated:
                        with self.assertRaisesRegex(RuntimeError, "unexpected response body"):
                            host.request("boundary", expected_body=b"x" * size)
                    else:
                        result = host.request("boundary", expected_body=b"x" * size)
                        self.assertEqual(result["response_body_bytes"], size)
                        self.assertTrue(result["response_framing_complete"])

    def test_stop_requires_running_identity_before_controlled_signal(self):
        host = object.__new__(qualification.Host)
        host.root, host.pid = Path("/run"), 123
        host.monitor_stop = threading.Event()
        host.monitor_failures, host.case_results, host.probe_failures = [], [], []
        host.process = Mock()
        host.process.poll.return_value = None
        host.process.wait.return_value = 0
        host.control, host.guard = Mock(), Mock()
        host.sample = Mock()
        host.args = Mock()
        ordering = Mock()
        ordering.attach_mock(host.guard, "guard")
        ordering.attach_mock(host.control, "control")
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts, host.origin.errors = {}, []
        host.origin_baseline, host.origin_error_baseline = {}, 0
        exit_data = b'{"pid":123,"exit_status":0,"signals":[15],"reaped":true}'
        with patch.object(Path, "exists", return_value=True), \
                patch.object(qualification, "bounded_read", return_value=exit_data), \
                patch.object(qualification, "reconcile_logs"), \
                patch.object(qualification, "verify_inputs"), \
                patch.object(qualification, "reconcile_final"):
            host.stop()
        self.assertEqual(ordering.mock_calls[0].args,
                         ("verify-running", "--evidence", "/run/identity.json"))
        self.assertEqual(ordering.mock_calls[1].args, (b"stop\n",))

    def test_final_reconciliation_rejects_late_partial_and_unknown_events_origin(self):
        event = {"transaction_id": "known", "rule_id": "991001"}
        cases = [{"token": "known", "backend_delta": 0, "events": [event]},
                 {"token": "allow", "backend_delta": 1, "events": []}]
        data = json.dumps(event).encode() + b"\n"
        with patch.object(qualification, "bounded_read", return_value=data), \
                patch.object(Path, "exists", return_value=True):
            qualification.reconcile_final(Path("/run"), cases, {"allow": 1}, [])
            for receipts, errors in (({"allow": 2}, []), ({"allow": 1, "late": 1}, []),
                                      ({"allow": 1}, ["partial body"])):
                with self.subTest(receipts=receipts, errors=errors), self.assertRaises(RuntimeError):
                    qualification.reconcile_final(Path("/run"), cases, receipts, errors)
        for wire in (data + data, data.rstrip(b"\n"), data + b'{"transaction_id":"late"}\n'):
            with self.subTest(wire=wire), patch.object(qualification, "bounded_read", return_value=wire), \
                    patch.object(Path, "exists", return_value=True), self.assertRaises(RuntimeError):
                qualification.reconcile_final(Path("/run"), cases, {"allow": 1}, [])

    def test_final_logs_reject_crash_critical_panic_and_native_engine_errors(self):
        for line in ("[core:crit] failure", "Segmentation fault (core dumped)",
                     "panic in worker", "fatal shutdown", "modsecurity internal error",
                     "native engine error"):
            with self.subTest(line=line), patch.object(Path, "glob", return_value=[Path("/run/error.log")]), \
                    patch.object(qualification, "bounded_read", return_value=line.encode()), \
                    self.assertRaises(RuntimeError):
                qualification.reconcile_logs(Path("/run"))
        with patch.object(Path, "glob", return_value=[Path("/run/error.log")]), \
                patch.object(qualification, "bounded_read", return_value=b"ModSecurity: Access denied with code 403 (phase 1). [id 991001]"):
            qualification.reconcile_logs(Path("/run"))

    def test_raw_http_response_framing_headers_are_strict(self):
        invalid = (b"Content-Length: invalid\r\n", b"Content-Length: -1\r\n",
                   b"Content-Length: 00\r\n", b"Content-Length: +0\r\n",
                   b"Content-Length: 0\r\nContent-Length: 0\r\n",
                   b"Content-Length: 0\r\nTransfer-Encoding: chunked\r\n",
                   b"Transfer-Encoding: gzip\r\n",
                   b"Transfer-Encoding: gzip, chunked\r\n",
                   b"Transfer-Encoding: chunked\r\nTransfer-Encoding: chunked\r\n")
        for headers in invalid:
            with self.subTest(headers=headers):
                body = b"0\r\n\r\n" if b"Transfer-Encoding: chunked\r\n" in headers else b""
                stream = io.BytesIO(b"HTTP/1.1 200 OK\r\n" + headers + b"\r\n" + body)
                response = http.client.HTTPResponse(Mock(makefile=Mock(return_value=stream)))
                response.begin()
                with self.assertRaisesRegex(RuntimeError, "framing"):
                    qualification.bounded_response_body(response, "probe")
        for headers, body in ((b"Connection: close\r\n", b""),
                               (b"Connection: close\r\n", b"close-delimited"),
                               (b"Transfer-Encoding: chunked\r\n", b"0\r\n\r\n")):
            with self.subTest(valid=headers, body=body):
                stream = io.BytesIO(b"HTTP/1.1 200 OK\r\n" + headers + b"\r\n" + body)
                response = http.client.HTTPResponse(Mock(makefile=Mock(return_value=stream)))
                response.begin()
                received = qualification.bounded_response_body(response, "probe")
                self.assertEqual(received, b"" if b"chunked" in headers else body)
                qualification.assert_response_complete(response, "probe")

    def test_real_http_response_rejects_declared_body_truncation(self):
        for declared, body, accepted in ((0, b"", True), (1, b"", False),
                                         (21, b"qualification-p4-deny", True),
                                         (22, b"qualification-p4-deny", False)):
            with self.subTest(declared=declared, body_bytes=len(body)):
                stream = io.BytesIO(b"HTTP/1.1 200 OK\r\nContent-Length: " +
                                    str(declared).encode("ascii") + b"\r\n\r\n" + body)
                response = http.client.HTTPResponse(Mock(makefile=Mock(return_value=stream)))
                response.begin()
                self.assertEqual(response.read(qualification.LIMIT + 4097), body)
                self.assertEqual(response.isclosed(), declared in (0, 1, 21))
                if accepted:
                    qualification.assert_response_complete(response, "probe")
                else:
                    self.assertGreater(response.length, 0)
                    with self.assertRaisesRegex(RuntimeError, "incomplete framing"):
                        qualification.assert_response_complete(response, "probe")

    def test_safe_p4_requires_single_exact_rule_action_commit_and_eos_receipt(self):
        valid = valid_safe_p4()
        qualification.assert_phase4_safe([valid])
        for field, value in valid.items():
            changed = not value if type(value) is bool else value + 1 if type(value) is int else "wrong"
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                qualification.assert_phase4_safe([{**valid, field: changed}])
            with self.subTest(missing=field), self.assertRaises(RuntimeError):
                qualification.assert_phase4_safe([{key: val for key, val in valid.items() if key != field}])
        for receipts in ([], [valid, valid]):
            with self.subTest(count=len(receipts)), self.assertRaises(RuntimeError):
                qualification.assert_phase4_safe(receipts)
        with self.assertRaises(RuntimeError):
            qualification.assert_phase4_safe([{**valid, "http_status": True}])

    def test_exercise_safe_case_and_empty_response_have_exact_distinct_contracts(self):
        host = Mock()
        host.request.side_effect = lambda *_args, **_kwargs: {}
        host.origin.parallel_peak = 4
        host.origin.parallel_errors = []
        with patch.object(qualification, "exercise_keepalive", return_value=[]):
            qualification.exercise(host, True)
        calls = {call.args[0]: call for call in host.request.call_args_list}
        self.assertNotIn("p4-safe-precommit", calls)
        safe = calls["p4-safe-postcommit"]
        self.assertEqual(safe.args[1:3], (200, 1))
        self.assertTrue(safe.kwargs["safe_postcommit"])
        self.assertEqual(safe.kwargs["expected_body"], b"qualification-p4-deny")
        empty = calls["response-body-0"]
        self.assertEqual(empty.args[1], 200)
        self.assertEqual(empty.kwargs["expected_body"], b"")
        self.assertEqual(empty.kwargs["path"], "/response/0")

    def test_safe_response_dispatch_does_not_use_allow_or_accept_wrong_body(self):
        host = object.__new__(qualification.Host)
        host.port, host.pid, host.root = 19000, 123, Path("/run/owned")
        host.guard, host.sample = Mock(), Mock()
        host.monitor_failures = []
        host.resource_lock = threading.Lock()
        host.case_results = []
        host.origin = Mock()
        host.origin.lock = threading.Lock()
        host.origin.receipts.get.return_value = 1
        response = Mock(status=200, length=0, chunked=False)
        response.headers = http.client.HTTPMessage()
        response.headers.add_header("Content-Length", "21")
        response.isclosed.return_value = True
        client = Mock()
        client.getresponse.return_value = response
        with patch.object(qualification.http.client, "HTTPConnection", return_value=client), \
                patch.object(qualification, "events", return_value=[valid_safe_p4()]), \
                patch.object(qualification, "assert_decision") as generic:
            response.read.return_value = b"qualification-p4-deny"
            result = host.request("p4-safe-postcommit", safe_postcommit=True,
                                  expected_body=b"qualification-p4-deny")
            self.assertEqual(result["response_body_bytes"], 21)
            self.assertTrue(result["response_framing_complete"])
            generic.assert_not_called()
            for wrong in (b"", b"qualification-p4-deny-extra"):
                response.read.return_value = wrong
                with self.subTest(body=wrong), self.assertRaisesRegex(RuntimeError, "body or incomplete"):
                    host.request("p4-safe-postcommit", safe_postcommit=True,
                                 expected_body=b"qualification-p4-deny")
            response.read.return_value = b"qualification-p4-deny"
            response.isclosed.return_value = False
            with self.assertRaisesRegex(RuntimeError, "incomplete framing"):
                host.request("p4-safe-postcommit", safe_postcommit=True,
                             expected_body=b"qualification-p4-deny")

    def test_httpd_2468_header_boundary_wire_lengths_and_exact_statuses(self):
        host = Mock()
        host.request.side_effect = lambda *_args, **_kwargs: {}
        host.origin.parallel_peak = 4
        host.origin.parallel_errors = []
        with patch.object(qualification, "exercise_keepalive", return_value=[]):
            results = qualification.exercise(host, True)
        calls = [call for call in host.request.call_args_list if call.args[0].startswith("header-line-")]
        self.assertEqual([call.args[0] for call in calls],
                         ["header-line-256", "header-line-257", "header-line-258"])
        for call, line_bytes, status, backend in zip(calls, (256, 257, 258), (200, 200, 400), (1, 1, 0)):
            self.assertEqual(call.args[1:3], (status, backend))
            wire = ("X-Boundary: " + call.kwargs["headers"]["X-Boundary"] + "\r\n").encode("ascii")
            self.assertEqual(len(wire), line_bytes + 2)
        metadata = [result for result in results if "header_line_bytes_before_crlf" in result]
        self.assertEqual([result["header_line_bytes_before_crlf"] for result in metadata], [256, 257, 258])
        self.assertEqual([result["header_line_bytes_with_crlf"] for result in metadata], [258, 259, 260])

    def test_supervisor_controller_uses_one_parent_for_start_and_stop(self):
        parent, child = socket.socketpair()
        guard = Mock()
        guard._runner_configured_path.return_value = Path("/run/owned")
        guard.supervise.return_value = 0
        guard.stop_supervisor.return_value = None
        parent.sendall(b"stop\n")
        with patch.object(qualification.os, "fork", side_effect=[123, 124]), \
                patch.object(qualification.os, "waitpid", side_effect=[(124, 0), (123, 0)]), \
                patch.object(qualification, "load_guard", return_value=guard), \
                patch.object(qualification.signal, "signal"):
            self.assertEqual(qualification.supervisor_controller(child.detach()), 0)
        parent.close()

    def test_supervisor_controller_rejects_unknown_control_command(self):
        parent, child = socket.socketpair()
        guard = Mock()
        guard._runner_configured_path.return_value = Path("/run/owned")
        parent.sendall(b"arbitrary-pid\n")
        with patch.object(qualification.os, "fork", return_value=123), \
                patch.object(qualification.os, "kill") as kill, \
                patch.object(qualification.os, "waitpid", return_value=(123, 0)), \
                patch.object(qualification, "load_guard", return_value=guard), \
                patch.object(qualification.signal, "signal"):
            with self.assertRaisesRegex(RuntimeError, "control command"):
                qualification.supervisor_controller(child.detach())
        kill.assert_called_once_with(123, qualification.signal.SIGTERM)
        parent.close()

    def test_rtk_preserves_explicit_private_control_descriptor(self):
        parent, child = socket.socketpair()
        process = subprocess.Popen(["rtk", "proxy", "/usr/bin/python3", "-I", "-c",
                                    "import socket,sys; s=socket.socket(fileno=int(sys.argv[1])); s.sendall(b'ACK')",
                                    str(child.fileno())], pass_fds=(child.fileno(),))
        child.close()
        parent.settimeout(3)
        try:
            self.assertEqual(parent.recv(8), b"ACK")
            self.assertEqual(process.wait(timeout=3), 0)
        finally:
            parent.close()
            if process.poll() is None:
                process.kill()
                process.wait(timeout=3)

    def test_controller_eof_performs_guarded_stop(self):
        parent, child = socket.socketpair()
        parent.close()
        guard = Mock()
        guard._runner_configured_path.return_value = Path("/run/owned")
        with patch.object(qualification.os, "fork", side_effect=[123, 124]) as fork, \
                patch.object(qualification.os, "waitpid", side_effect=[(124, 0), (123, 0)]), \
                patch.object(qualification, "load_guard", return_value=guard), \
                patch.object(qualification.signal, "signal"):
            self.assertEqual(qualification.supervisor_controller(child.detach()), 0)
        self.assertEqual(fork.call_count, 2)

    def test_controller_guard_rejection_terminates_only_its_unreaped_child(self):
        parent, child = socket.socketpair()
        parent.sendall(b"stop\n")
        guard = Mock()
        guard._runner_configured_path.return_value = Path("/run/owned")
        with patch.object(qualification.os, "fork", side_effect=[123, 124]), \
                patch.object(qualification.os, "waitpid", side_effect=[(124, 77 << 8), (123, 0)]), \
                patch.object(qualification.os, "kill") as kill, \
                patch.object(qualification, "load_guard", return_value=guard), \
                patch.object(qualification.signal, "signal"):
            with self.assertRaisesRegex(RuntimeError, "guard rejected"):
                qualification.supervisor_controller(child.detach())
        kill.assert_called_once_with(123, qualification.signal.SIGTERM)
        parent.close()

    def test_controller_rejects_changed_launcher_before_fork(self):
        parent, child = socket.socketpair()
        guard = Mock()
        guard._runner_configured_path.return_value = Path("/run/owned")
        with patch.object(qualification.os, "getppid", side_effect=[10, 11]), \
                patch.object(qualification.os, "fork") as fork, \
                patch.object(qualification, "load_guard", return_value=guard), \
                patch.object(qualification.signal, "signal"):
            with self.assertRaisesRegex(RuntimeError, "launcher disappeared"):
                qualification.supervisor_controller(child.detach())
        fork.assert_not_called()
        parent.close()

    def test_duplicate_decision_rejected(self):
        decision = valid_decision()
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            qualification.assert_decision([decision, decision], "991001", "request_headers")

    def test_wrong_phase_rule_action_and_truncation_rejected(self):
        valid = valid_decision("991004", "response_body")
        qualification.assert_decision([valid], "991004", "response_body")
        qualification.assert_decision(
            [{**valid, "late_intervention_mode": "safe"}], "991004", "response_body"
        )
        for change in ({"rule_id": "991003"}, {"phase": "request_body"},
                       {"actual_action": "log_only"}, {"requested_action": "pass"},
                       {"http_status": 200}, {"visible_http_status": 200}, {"http_status": True},
                       {"connector": "nginx"}, {"integration_mode": "mock"},
                       {"response_committed": True}, {"late_intervention": True},
                       {"headers_sent": True}, {"connection_aborted": True},
                       {"late_intervention_mode": "strict"}, {"late_intervention_mode": "off"},
                       {"late_intervention_mode": None}, {"late_intervention_mode": True},
                       {"truncated": True}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                qualification.assert_decision([{**valid, **change}], "991004", "response_body")

    def test_allow_rejects_intervention(self):
        qualification.assert_decision([], None, None)
        with self.assertRaises(RuntimeError):
            qualification.assert_decision([{"actual_action": "deny"}], None, None)

    def test_correlation_does_not_accept_other_transaction(self):
        with temporary_directory() as directory:
            path = Path(directory) / "events.jsonl"
            qualification.private_write(path, json.dumps({"transaction_id": "other"}) + "\n")
            self.assertEqual(qualification.events(path, "expected"), [])

    def test_bounded_evidence_reader(self):
        with temporary_directory() as directory:
            path = Path(directory) / "events.jsonl"
            qualification.private_write(path, "12345")
            with self.assertRaisesRegex(RuntimeError, "exceeds bound"):
                qualification.bounded_read(path, 4)

    def test_private_writer_refuses_existing_and_symlink(self):
        with temporary_directory() as directory:
            path = Path(directory) / "value"
            qualification.private_write(path, "original")
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError):
                qualification.private_write(path, "replacement")
            link = Path(directory) / "link"
            link.symlink_to(path)
            with self.assertRaises(FileExistsError):
                qualification.private_write(link, "replacement")
            self.assertEqual(path.read_text(), "original")

    def test_trust_rejects_symlink_and_writable_input(self):
        with temporary_directory() as directory:
            path = Path(directory) / "input"
            qualification.private_write(path, "value")
            self.assertEqual(qualification.trusted_file(str(path)), path)
            link = Path(directory) / "link"
            link.symlink_to(path)
            with self.assertRaises(ValueError):
                qualification.trusted_file(str(link))
            os.chmod(path, 0o666)
            with self.assertRaises(ValueError):
                qualification.trusted_file(str(path))

    def test_body_limit_requires_reject_event_and_exact_status_flags(self):
        for phase, status in (("request_body", 413), ("response_body", 500)):
            valid = valid_decision(phase=phase, status=status, body_limit=True)
            qualification.assert_decision([valid], None, phase, status, True)
            for field, replacement in (("event", "connector_error"), ("body_limit_outcome", "partial"),
                                       ("rule_id", "991001"), ("actual_action", "pass"),
                                       ("requested_action", "log_only"), ("http_status", 200),
                                       ("visible_http_status", 200), ("response_committed", True),
                                       ("late_intervention", True), ("connector", "mock"),
                                       ("integration_mode", "mock"), ("body_truncated", not valid["body_truncated"])):
                with self.subTest(phase=phase, field=field), self.assertRaises(RuntimeError):
                    qualification.assert_decision([{**valid, field: replacement}], None, phase, status, True)
            for field in valid:
                missing = {key: value for key, value in valid.items() if key != field}
                with self.subTest(phase=phase, missing=field), self.assertRaises(RuntimeError):
                    qualification.assert_decision([missing], None, phase, status, True)

    def test_config_paths_reject_apache_expansion_and_metacharacters(self):
        for marker in ("$VALUE", "${VALUE}", '"', "\n", "\\"):
            value = "/build/" + marker
            with self.subTest(marker=marker):
                with self.assertRaises(ValueError):
                    qualification.trusted_file(value)
                for index in range(3):
                    paths = [Path("/run/owned"), Path("/build/module"), Path("/build/modules")]
                    paths[index] = Path(value)
                    with self.subTest(slot=index), self.assertRaises(ValueError):
                        qualification.config(*paths, 1, 2)

    def test_evidence_rejects_fifo_symlink_hardlink_and_bad_mode(self):
        with temporary_directory() as directory:
            root = Path(directory)
            value = root / "value"
            qualification.private_write(value, "ok")
            link = root / "link"
            link.symlink_to(value)
            fifo = root / "fifo"
            os.mkfifo(fifo, 0o600)
            for rejected in (link, fifo):
                with self.subTest(path=rejected), self.assertRaises((OSError, ValueError)):
                    qualification.bounded_read(rejected)
            hard = root / "hard"
            os.link(value, hard)
            with self.assertRaises(ValueError):
                qualification.bounded_read(value)
            hard.unlink()
            os.chmod(value, 0o644)
            with self.assertRaises(ValueError):
                qualification.bounded_read(value)

    def test_evidence_rejects_unsafe_or_symlinked_ancestor(self):
        with temporary_directory() as directory:
            root = Path(directory)
            child = root / "child"
            qualification.private_mkdir(child)
            qualification.private_write(child / "value", "ok")
            alias = root / "alias"
            alias.symlink_to(child, target_is_directory=True)
            with self.assertRaises(OSError):
                qualification.bounded_read(alias / "value")
            os.chmod(child, 0o777)
            with self.assertRaises(ValueError):
                qualification.bounded_read(child / "value")
            os.chmod(child, 0o700)

    def test_private_root_requires_owner_only_mode(self):
        with temporary_directory() as directory:
            root = Path(directory)
            os.close(qualification.directory_fd(root, private=True))
            os.chmod(root, 0o755)
            with self.assertRaises(ValueError):
                qualification.directory_fd(root, private=True)

    def test_evidence_rejects_foreign_owner_metadata(self):
        with temporary_directory() as directory:
            path = Path(directory) / "value"
            qualification.private_write(path, "ok")
            original_fstat = os.fstat

            def foreign_file(fd):
                info = original_fstat(fd)
                if qualification.stat.S_ISREG(info.st_mode):
                    values = list(info)
                    values[4] = os.geteuid() + 10000
                    return os.stat_result(values)
                return info

            with patch.object(qualification.os, "fstat", side_effect=foreign_file):
                with self.assertRaisesRegex(ValueError, "owned"):
                    qualification.bounded_read(path)

    def test_serving_identity_rejects_root_mismatched_ids_and_capabilities(self):
        status = "Uid:\t1001\t1001\t1001\t1001\nGid:\t1002\t1002\t1002\t1002\nCapEff:\t0000000000000000\nGroups:\t1002\n"
        value = qualification.serving_identity(status, 1001, 1002)
        self.assertEqual(value["uid"][1], 1001)
        for changed, uid, gid in ((status, 0, 0), (status, 1003, 1002),
                                  (status.replace("1001\t1001\t1001\t1001", "1001\t0\t1001\t1001"), 1001, 1002),
                                  (status.replace("0000000000000000", "0000000000000001"), 1001, 1002),
                                  (status.replace("Groups:\t1002", "Groups:\t0 1002"), 1001, 1002)):
            with self.subTest(changed=changed, uid=uid), self.assertRaises(RuntimeError):
                qualification.serving_identity(changed, uid, gid)

    def test_origin_waiting_handler_is_closed_and_joined(self):
        origin = qualification.Origin()
        worker = threading.Thread(target=origin.serve_forever, daemon=True)
        worker.start()
        client = socket.create_connection(origin.server_address, timeout=1)
        try:
            deadline = time.monotonic() + 1
            while not origin.handlers and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue(origin.handlers)
            origin.shutdown()
            origin.close_handlers(timeout=1)
            self.assertTrue(all(not thread.is_alive() and sock.fileno() == -1
                                for thread, sock in origin.handlers))
        finally:
            client.close()
            origin.server_close()
            worker.join(timeout=1)

    def test_origin_cleanup_failure_is_rejected(self):
        origin = qualification.Origin()
        stop = threading.Event()
        worker = threading.Thread(target=stop.wait, daemon=True)
        client, peer = socket.socketpair()
        worker.start()
        origin.handlers.append((worker, client))
        try:
            with self.assertRaisesRegex(RuntimeError, "cleanup"):
                origin.close_handlers(timeout=0.01)
        finally:
            stop.set()
            worker.join(timeout=1)
            peer.close()
            client.close()
            origin.server_close()

    def test_origin_proves_four_requests_overlap(self):
        origin = qualification.Origin()
        origin.parallel_barrier = threading.Barrier(4)
        worker = threading.Thread(target=origin.serve_forever, daemon=True)
        worker.start()

        def send(index):
            connection = http.client.HTTPConnection(*origin.server_address, timeout=3)
            try:
                connection.request("GET", "/parallel", headers={
                    "X-Qualification-ID": "q-" + f"{index:024x}",
                    "X-Qualification-Parallel": origin.parallel_secret})
                response = connection.getresponse()
                response.read()
                return response.status
            finally:
                connection.close()

        try:
            with ThreadPoolExecutor(max_workers=4) as pool:
                self.assertEqual(list(pool.map(send, range(4))), [200] * 4)
            self.assertEqual(origin.parallel_peak, 4)
            self.assertEqual(origin.parallel_errors, [])
        finally:
            origin.shutdown()
            origin.close_handlers()
            origin.server_close()
            worker.join(timeout=1)

    def test_origin_single_request_cannot_claim_overlap(self):
        origin = qualification.Origin()
        origin.parallel_barrier = threading.Barrier(4)
        worker = threading.Thread(target=origin.serve_forever, daemon=True)
        worker.start()
        connection = http.client.HTTPConnection(*origin.server_address, timeout=3)
        try:
            connection.request("GET", "/parallel", headers={
                "X-Qualification-ID": "q-" + "0" * 24,
                "X-Qualification-Parallel": origin.parallel_secret})
            response = connection.getresponse()
            response.read()
            self.assertEqual(response.status, 503)
            self.assertEqual(origin.parallel_peak, 1)
            self.assertEqual(origin.parallel_errors, ["origin overlap barrier failed"])
        finally:
            connection.close()
            origin.shutdown()
            origin.close_handlers()
            origin.server_close()
            worker.join(timeout=1)

    def test_keepalive_runs_deny_recovery_sequence_on_original_socket(self):
        connection = Mock()
        connection.sock.fileno.return_value = 12
        host = Mock(port=19000)
        host.request.return_value = {}
        with patch.object(qualification.http.client, "HTTPConnection", return_value=connection):
            qualification.exercise_keepalive(host)
        calls = host.request.call_args_list
        self.assertEqual([call.args[0] for call in calls], [
            "keepalive-allow-before", "keepalive-p1-deny", "keepalive-allow-after-p1",
            "keepalive-p2-deny", "keepalive-allow-after-p2"])
        self.assertTrue(all(call.kwargs["connection"] is connection for call in calls))
        for call, phase, rule in ((calls[1], "request_headers", "991001"),
                                  (calls[3], "request_body", "991002")):
            self.assertEqual(call.kwargs["expected"], 403)
            self.assertEqual(call.kwargs["delta"], 0)
            self.assertEqual(call.kwargs["phase"], phase)
            self.assertEqual(call.kwargs["rule"], rule)
        connection.close.assert_called_once()

    def test_keepalive_reconnection_cannot_be_published_as_pass(self):
        connection = Mock()
        connection.sock.fileno.return_value = 12
        host = Mock(port=19000)

        def request(name, **_kwargs):
            if name == "keepalive-p1-deny":
                connection.sock = Mock()
                connection.sock.fileno.return_value = 13
            return {}

        host.request.side_effect = request
        with patch.object(qualification.http.client, "HTTPConnection", return_value=connection):
            with self.assertRaisesRegex(RuntimeError, "reconnected"):
                qualification.exercise_keepalive(host)
        self.assertEqual(host.request.call_count, 2)
        connection.close.assert_called_once()

    def test_config_uses_native_module_safe_bounded_request_and_response(self):
        value = qualification.config(Path("/run/owned"), Path("/build/mod_security3.so"),
                                     Path("/build/modules.conf"), 18001, 18002)
        self.assertIn('LoadModule security3_module "/build/mod_security3.so"', value)
        self.assertIn('modsecurity_transaction_id_expr "%{req:X-Qualification-ID}"', value)
        self.assertIn("modsecurity_phase4_mode safe", value)
        self.assertIn("modsecurity_phase4_body_limit 1024", value)
        self.assertIn("ProxyPass / http://127.0.0.1:18002/", value)
        self.assertIn("SecRequestBodyLimitAction Reject", qualification.RULES)
        self.assertIn("SecResponseBodyLimitAction Reject", qualification.RULES)


if __name__ == "__main__":
    unittest.main()
