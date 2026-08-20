from __future__ import annotations

import http.client
import http.server
import importlib.util
import json
import os
import shutil
import ssl
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
HELPER_PATH = ROOT / "connectors" / "envoy" / "harness" / "envoy_smoke_helper.py"
RUNTIME_PATH = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_ext_proc_runtime.sh"
EXT_AUTHZ_RUNTIME_PATH = ROOT / "connectors" / "envoy" / "harness" / "run_envoy_connector_runtime.sh"
EXT_AUTHZ_START_PATH = ROOT / "connectors" / "envoy" / "harness" / "start_envoy_connector.sh"
EXT_AUTHZ_TEMPLATE = ROOT / "connectors" / "envoy" / "config" / "envoy-ext-authz-smoke.yaml.in"
EXT_PROC_CONFIG_MATERIALIZER = (
    ROOT / "connectors" / "envoy" / "config" / "prepare_envoy_ext_proc_config.sh"
)
TLS_YAML_RENDERER = ROOT / "connectors" / "envoy" / "config" / "lib" / "tls_yaml_render.sh"


def load_helper() -> object:
    specification = importlib.util.spec_from_file_location("envoy_smoke_helper", HELPER_PATH)
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def create_loopback_tls_material(root: Path) -> tuple[Path, Path]:
    certificate = root / "loopback.crt"
    private_key = root / "loopback.key"
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-sha256", "-nodes", "-days", "1",
            "-subj", "/CN=127.0.0.1", "-addext", "subjectAltName=IP:127.0.0.1",
            "-keyout", str(private_key), "-out", str(certificate),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return certificate, private_key


def configure_loopback_tls(server: http.server.ThreadingHTTPServer, root: Path) -> Path:
    certificate, private_key = create_loopback_tls_material(root)
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=certificate, keyfile=private_key)
    server.socket = context.wrap_socket(server.socket, server_side=True)
    return certificate


class EnvoyTransportHardeningContractTest(unittest.TestCase):
    def test_runtime_harness_cleanup_is_bounded_and_pid_identity_bound(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn("owned_process_start_token()", source)
        self.assertIn("owned_process_stat_value()", source)
        self.assertIn('close = line.rfind(")")', source)
        self.assertIn('post_comm[19]', source)
        self.assertNotIn("awk '{ print $22 }'", source)
        self.assertNotIn("awk '{ print $3 }'", source)
        self.assertIn("owned_process_is_current()", source)
        self.assertIn("CHILD_STOP_ATTEMPTS=${ENVOY_CHILD_STOP_ATTEMPTS:-20}", source)
        self.assertIn("CHILD_STOP_DELAY=${ENVOY_CHILD_STOP_DELAY_SECONDS:-0.1}", source)
        self.assertIn('kill -TERM "$owned_pid"', source)
        self.assertIn('kill -KILL "$owned_pid"', source)
        self.assertIn('wait_for_owned_process_stop "$owned_pid" "$expected_token"', source)
        self.assertIn('refusing to signal changed $process_label PID $owned_pid', source)
        self.assertIn('refusing to signal unverified $process_label PID $owned_pid', source)
        self.assertIn('upstream_start_token=$(owned_process_start_token "$upstream_pid")', source)
        self.assertIn('service_start_token=$(owned_process_start_token "$service_pid")', source)
        self.assertIn('envoy_start_token=$(owned_process_start_token "$envoy_pid")', source)

    def test_envoy_v138_template_avoids_deprecated_protocol_and_admin_fields(self) -> None:
        template = (
            ROOT / "connectors" / "envoy" / "config" / "envoy-ext-proc-streaming.yaml.in"
        ).read_text(encoding="utf-8")

        self.assertIn("typed_extension_protocol_options:", template)
        self.assertIn("envoy.extensions.upstreams.http.v3.HttpProtocolOptions:", template)
        self.assertIn(
            "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions",
            template,
        )
        self.assertIn("explicit_http_config:", template)
        self.assertNotIn("\n    http2_protocol_options: {}", template)
        self.assertIn("\n          http2_protocol_options: {}", template)
        self.assertNotIn("access_log_path:", template)
        self.assertIn("envoy.access_loggers.file", template)
        self.assertIn(
            "type.googleapis.com/envoy.extensions.access_loggers.file.v3.FileAccessLog",
            template,
        )
        self.assertIn("path: /dev/null", template)
        self.assertIn("log_format:", template)
        self.assertIn("text_format_source:", template)
        self.assertIn('inline_string: ""', template)
        self.assertIn("type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext", template)
        self.assertIn("validation_context:", template)
        self.assertIn("trusted_ca:", template)
        self.assertIn('filename: "@TLS_CERTIFICATE@"', template)

    def test_first_body_byte_is_read_once_without_header_remainder(self) -> None:
        helper = load_helper()

        class Connection:
            def __init__(self) -> None:
                self.recv_limits: list[int] = []
                self.timeouts: list[float] = []
                self.responses = [
                    b"HTTP/1.1 200 OK\r\nContent-Length: 1\r\n\r\n",
                    b"x",
                ]

            def settimeout(self, timeout: float) -> None:
                self.timeouts.append(timeout)

            def recv(self, limit: int) -> bytes:
                self.recv_limits.append(limit)
                return self.responses.pop(0)

        connection = Connection()

        self.assertEqual(helper._read_chunked_first_body(connection, timeout=1.0), (200, 1))
        self.assertEqual(connection.recv_limits, [4096, 1])
        self.assertTrue(all(timeout > 0 for timeout in connection.timeouts))

    def test_client_cancel_waits_for_one_real_body_byte_then_closes(self) -> None:
        helper = load_helper()

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)

            class FastCancelHandler(helper.UpstreamHandler):
                client_cancel_delay_seconds = 0.05

            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), FastCancelHandler)
            server.handle_error = lambda request, client_address: None
            certificate = configure_loopback_tls(server, root)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                observation = helper.client_cancel(
                    str(root), str(certificate), "127.0.0.1", server.server_port,
                    "/client-cancel", ["X-Request-Id: cancel-test"],
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

        self.assertEqual(observation["http_status"], 200)
        self.assertTrue(observation["first_body_byte_received"])
        self.assertTrue(observation["client_closed"])

    def test_client_cancel_rejects_non_ascii_wire_headers(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            certificate = root / "loopback.crt"
            certificate.write_text("placeholder", encoding="utf-8")
            runtime_root = str(root)
            certificate_path = str(certificate)
            non_ascii_header = ["X-Test: snowman-☃"]
            with self.assertRaises(ValueError):
                helper.client_cancel(
                    runtime_root, certificate_path, "127.0.0.1", 18080,
                    "/client-cancel", non_ascii_header,
                )

    def test_probe_requires_verified_loopback_tls_and_root_confined_evidence(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), helper.UpstreamHandler)
            certificate = configure_loopback_tls(server, root)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            evidence = root / "probe.json"
            try:
                self.assertEqual(
                    helper.probe(
                        str(root), str(certificate), f"https://127.0.0.1:{server.server_port}/allowed",
                        [], "GET", None, False, str(evidence),
                    ),
                    0,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

            self.assertEqual(json.loads(evidence.read_text(encoding="utf-8"))["http_status"], 200)
            for unsafe_url in (
                f"http://127.0.0.1:{server.server_port}/allowed",
                f"https://example.invalid:{server.server_port}/allowed",
                f"https://user@127.0.0.1:{server.server_port}/allowed",
            ):
                with self.assertRaises(ValueError):
                    helper.checked_loopback_https_url(unsafe_url)

            outside = root.parent / "envoy-probe-outside.json"
            with self.assertRaises(ValueError):
                helper.runtime_artifact(root, outside, "probe evidence output")
            escaped_parent = root / "escaped"
            escaped_parent.symlink_to(root.parent, target_is_directory=True)
            with self.assertRaises(ValueError):
                helper.runtime_artifact(root, escaped_parent / "probe.json", "probe evidence output")

    def test_upstream_fixture_requires_runtime_confined_tls_files(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            certificate, private_key = create_loopback_tls_material(root)
            server = mock.MagicMock()
            with mock.patch.object(helper.http.server, "ThreadingHTTPSServer", return_value=server) as constructor:
                self.assertEqual(
                    helper.serve_upstream(
                        18081, 5.0, str(root), str(certificate), str(private_key),
                    ),
                    0,
                )

            arguments, keywords = constructor.call_args
            self.assertEqual(arguments[0], (helper.LOOPBACK_HOST, 18081))
            self.assertTrue(issubclass(arguments[1], helper.UpstreamHandler))
            self.assertEqual(keywords["certfile"], str(certificate))
            self.assertEqual(keywords["keyfile"], str(private_key))
            self.assertEqual(server.socket.context.minimum_version, ssl.TLSVersion.TLSv1_2)
            server.serve_forever.assert_called_once_with()
            server.server_close.assert_called_once_with()

            outside_key = root.parent / "outside-loopback.key"
            outside_key.write_text("not a key", encoding="utf-8")
            private_key.unlink()
            private_key.symlink_to(outside_key)
            with self.assertRaisesRegex(ValueError, "below the runtime root|private key must be a regular file"):
                helper.loopback_tls_server_files(root, str(certificate), str(private_key))

    def test_phase4_marker_default_and_plain_text_headers_remain_stable(self) -> None:
        helper = load_helper()
        with mock.patch.object(sys, "argv", [
            "envoy_smoke_helper.py",
            "phase4-first-byte",
            "--host", "127.0.0.1",
            "--port", "18080",
            "--runtime-root", "/var/tmp/envoy-phase4-runtime",
            "--tls-certificate", "/var/tmp/envoy-phase4-runtime/loopback.crt",
            "--barrier-dir", "/tmp/phase4-barrier",
        ]):
            arguments = helper.parse_args()

        self.assertEqual(helper.PHASE4_MARKER_PATH, "/phase4-marker")
        self.assertEqual(arguments.path, "/phase4-marker")
        self.assertEqual(helper.TEXT_PLAIN_CONTENT_TYPE, "text/plain")

        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), helper.UpstreamHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=2)
        try:
            connection.request("GET", arguments.path)
            response = connection.getresponse()
            self.assertEqual(response.status, 200)
            self.assertEqual(response.getheader("content-type"), "text/plain")
            self.assertEqual(response.read(), b"no-crs-response-body-marker\n")
        finally:
            connection.close()
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

        source = HELPER_PATH.read_text(encoding="utf-8")
        self.assertEqual(
            source.count('self.send_header("content-type", TEXT_PLAIN_CONTENT_TYPE)'), 3,
        )

    def test_phase4_barrier_confirms_first_byte_before_upstream_eos(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            barrier_dir = Path(temporary) / "phase4-barrier"
            root = Path(temporary)

            class BarrierHandler(helper.UpstreamHandler):
                phase4_barrier_timeout_seconds = 2.0

            BarrierHandler.phase4_barrier_dir = barrier_dir
            BarrierHandler.runtime_root = root
            server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), BarrierHandler)
            certificate = configure_loopback_tls(server, root)
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                observation = helper.phase4_first_byte(
                    str(root),
                    str(certificate),
                    "127.0.0.1",
                    server.server_port,
                    "/phase4-marker",
                    ["X-Request-Id: phase4-first-byte-test"],
                    str(barrier_dir),
                    2.0,
                )
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=2)

            self.assertEqual(observation["http_status"], 200)
            self.assertTrue(observation["client_first_byte_received"])
            self.assertTrue(observation["first_byte_before_response_end"])
            self.assertGreater(observation["first_chunk_size"], 0)
            self.assertTrue(observation["upstream_paused"])
            self.assertFalse(observation["upstream_eos_sent_at_first_byte"])
            self.assertFalse(observation["upstream_response_finished_at_first_byte"])
            self.assertTrue(observation["upstream_eos_sent_after_release"])
            self.assertFalse(observation["body_payload_persisted"])

            paused = json.loads((barrier_dir / "upstream-paused.json").read_text(encoding="utf-8"))
            completed = json.loads(
                (barrier_dir / "upstream-completed.json").read_text(encoding="utf-8")
            )
            self.assertTrue(paused["upstream_paused"])
            self.assertFalse(paused["upstream_eos_sent"])
            self.assertTrue(completed["upstream_eos_sent"])
            self.assertNotIn("no-crs-response-body-marker", json.dumps(observation))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(paused))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(completed))

    def test_phase4_first_byte_evidence_binds_to_the_common_safe_event(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            observation_path = root / "observation.json"
            event_path = root / "events.jsonl"
            evidence_path = root / "first-byte-evidence.json"
            helper.write_json_atomic(root, observation_path,
                {
                    "schema_version": 1,
                    "evidence_type": "envoy_phase4_first_byte_observation",
                    "http_status": 200,
                    "client_first_byte_received": True,
                    "first_byte_before_response_end": True,
                    "first_chunk_size": 17,
                    "upstream_paused": True,
                    "upstream_eos_sent_at_first_byte": False,
                    "upstream_response_finished_at_first_byte": False,
                    "upstream_eos_sent_after_release": True,
                    "body_payload_persisted": False,
                    "transport_protocol": "http1",
                    "outcome": "PASS",
                }, "phase-4 first-byte observation",
            )
            common_safe_event = {
                "connector": "envoy",
                "integration_mode": "ext_proc",
                "event": "MSCONN_EVENT_RULE",
                "message_id": "MSCONN_EVENT_RULE",
                "transaction_id": "envoy-ext-proc-phase4-safe",
                "rule_id": "1100301",
                "phase": "response_body",
                "status": "blocked",
                "http_status": 403,
                "original_http_status": 200,
                "visible_http_status": 200,
                "requested_action": "deny",
                "actual_action": "log_only",
                "late_intervention": True,
                "late_intervention_mode": "safe",
                "headers_sent": True,
                "body_started": True,
                "response_committed": True,
                "connection_aborted": False,
                "transport_result": "log_only",
                "body_bytes_seen": 42,
                "body_bytes_inspected": 42,
            }
            event_path.write_text(json.dumps(common_safe_event) + "\n", encoding="utf-8")

            result = helper.write_phase4_first_byte_evidence(
                runtime_root=str(root),
                event_log=str(event_path),
                observation_path=str(observation_path),
                transaction_id="envoy-ext-proc-phase4-safe",
                evidence_output=str(evidence_path),
                run_id="run-phase4-first-byte",
            )

            self.assertTrue(result["event_appended"])
            self.assertTrue(result["evidence_written"])
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            self.assertEqual(evidence["evidence_type"], "synchronized_first_byte")
            self.assertEqual(evidence["evidence_origin"], "real_host")
            self.assertTrue(evidence["promotion_eligible"])
            self.assertTrue(evidence["first_byte_before_response_end"])
            self.assertTrue(evidence["no_full_response_buffering"])
            self.assertFalse(evidence["connector_owned_full_response_buffer"])
            self.assertEqual(evidence["transport_protocol"], "http1")

            records = [json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines()]
            barrier_event = records[-1]
            self.assertEqual(barrier_event["event"], "phase4_first_byte_barrier")
            self.assertEqual(barrier_event["transaction_id"], "envoy-ext-proc-phase4-safe")
            self.assertEqual(barrier_event["rule_id"], "1100301")
            self.assertEqual(barrier_event["phase"], 4)
            self.assertEqual(barrier_event["late_intervention_mode"], "safe")
            self.assertEqual(barrier_event["actual_action"], "log_only")
            self.assertTrue(barrier_event["end_of_stream_evaluation"])
            self.assertTrue(barrier_event["eos_seen"])
            self.assertEqual(barrier_event["cleanup_reason"], "normal")
            self.assertTrue(barrier_event["first_byte_before_response_end"])
            self.assertFalse(barrier_event["upstream_eos_sent_at_first_byte"])
            self.assertTrue(barrier_event["no_full_response_buffering"])
            self.assertNotIn("no-crs-response-body-marker", json.dumps(evidence))
            self.assertNotIn("no-crs-response-body-marker", json.dumps(barrier_event))

            repeated = helper.write_phase4_first_byte_evidence(
                runtime_root=str(root),
                event_log=str(event_path),
                observation_path=str(observation_path),
                transaction_id="envoy-ext-proc-phase4-safe",
                evidence_output=str(evidence_path),
                run_id="run-phase4-first-byte",
            )
            self.assertFalse(repeated["event_appended"])
            self.assertEqual(len(event_path.read_text(encoding="utf-8").splitlines()), 2)

    def test_allow_event_binds_client_http200_to_one_normal_ext_proc_completion(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "allow-probe.json"
            completions = root / "completion-events.jsonl"
            events.write_text(
                json.dumps({
                    "connector": "envoy",
                    "integration_mode": "ext_proc",
                    "event": "phase4_first_byte_barrier",
                    "message_id": "MSCONN_EVENT_P4_FIRST_BYTE_BARRIER",
                    "transaction_id": "envoy-ext-proc-phase4-safe",
                    "rule_id": "1100301",
                    "phase": 4,
                    "status": "observed",
                    "http_status": 403,
                    "visible_http_status": 200,
                    "requested_action": "deny",
                    "actual_action": "log_only",
                    "late_intervention": True,
                    "late_intervention_mode": "safe",
                    "headers_sent": True,
                    "body_started": True,
                    "response_committed": True,
                    "connection_aborted": False,
                    "transport_result": "log_only",
                    "end_of_stream_evaluation": True,
                    "eos_seen": True,
                }) + "\n",
                encoding="utf-8",
            )
            helper.write_json_atomic(root, probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 200,
                "response_bytes": 27,
                "body_payload_persisted": False,
            }, "allow probe evidence")
            completions.write_text(
                json.dumps({
                    "event": "ext_proc_stream_complete",
                    "integration_mode": "ext_proc",
                    "evaluation_mode": "common_libmodsecurity_nonpromoted",
                    "rule_evaluation": "libmodsecurity",
                    "transaction_id": "envoy-ext-proc-allow-1",
                    "response_body_bytes": 27,
                    "late_action": "none",
                    "close_reason": "response_end_of_stream",
                }) + "\n",
                encoding="utf-8",
            )

            result = helper.write_allow_event(
                runtime_root=str(root),
                event_log=str(events),
                probe_evidence_path=str(probe),
                completion_log=str(completions),
                transaction_id="envoy-ext-proc-allow-1",
            )

            self.assertTrue(result["event_appended"])
            allow_event = json.loads(events.read_text(encoding="utf-8").splitlines()[-1])
            self.assertEqual(allow_event["message_id"], "ENVOY_EXT_PROC_NATIVE_P1_ALLOW")
            self.assertEqual(allow_event["transaction_id"], "envoy-ext-proc-allow-1")
            self.assertEqual(allow_event["phase"], 1)
            self.assertEqual(allow_event["visible_http_status"], 200)
            self.assertNotIn("requested_action", allow_event)
            self.assertNotIn("actual_action", allow_event)
            self.assertNotIn("no-crs-response-body-marker", json.dumps(allow_event))

    def test_allow_event_rejects_noncausal_client_or_completion_metadata(self) -> None:
        helper = load_helper()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "allow-probe.json"
            completions = root / "completion-events.jsonl"
            events.write_text("{}\n", encoding="utf-8")
            helper.write_json_atomic(root, probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 403,
                "response_bytes": 27,
                "body_payload_persisted": False,
            }, "allow probe evidence")
            completions.write_text(
                json.dumps({
                    "event": "ext_proc_stream_complete",
                    "integration_mode": "ext_proc",
                    "evaluation_mode": "common_libmodsecurity_nonpromoted",
                    "rule_evaluation": "libmodsecurity",
                    "transaction_id": "envoy-ext-proc-allow-1",
                    "response_body_bytes": 27,
                    "late_action": "none",
                    "close_reason": "response_end_of_stream",
                }) + "\n",
                encoding="utf-8",
            )
            event_log = str(events)
            probe_evidence_path = str(probe)
            completion_log = str(completions)
            runtime_root = str(root)
            with self.assertRaisesRegex(ValueError, "HTTP 200"):
                helper.write_allow_event(
                    runtime_root=runtime_root,
                    event_log=event_log,
                    probe_evidence_path=probe_evidence_path,
                    completion_log=completion_log,
                    transaction_id="envoy-ext-proc-allow-1",
                )

            helper.write_json_atomic(root, probe, {
                "schema_version": 1,
                "evidence_type": "envoy_http_client_probe",
                "http_status": 200,
                "response_bytes": 27,
                "body_payload_persisted": False,
            }, "allow probe evidence")
            completions.write_text("\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "exactly one ext_proc completion"):
                helper.write_allow_event(
                    runtime_root=runtime_root,
                    event_log=event_log,
                    probe_evidence_path=probe_evidence_path,
                    completion_log=completion_log,
                    transaction_id="envoy-ext-proc-allow-1",
                )

    def test_tls_path_materializer_keeps_paths_data_in_yaml_and_sed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "generated.yaml"
            marker = root / "unexpected-command-marker"
            injected_certificate = (
                f"{root}/benign|; s|{root}/benign|touch {marker}|e; #"
            )
            private_key = root / 'key with spaces&pipe|quote"backslash\\.key'
            environment = dict(os.environ)
            environment.update({
                "TLS_CERTIFICATE": injected_certificate,
                "TLS_PRIVATE_KEY": str(private_key),
                "OUTPUT_CONFIG": str(output),
            })

            completed = subprocess.run(
                ["sh", str(EXT_PROC_CONFIG_MATERIALIZER)],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(marker.exists())
            rendered = output.read_text(encoding="utf-8")
            self.assertIn(f'filename: "{injected_certificate}"', rendered)
            self.assertIn(
                "type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext",
                rendered,
            )
            self.assertGreaterEqual(rendered.count(f'filename: "{injected_certificate}"'), 2)
            expected_private_key = str(private_key).replace("\\", "\\\\").replace('"', '\\"')
            self.assertIn(f'filename: "{expected_private_key}"', rendered)

            newline_output = root / "newline-generated.yaml"
            environment["TLS_CERTIFICATE"] = f"{root}/certificate\nwith-newline.crt"
            environment["OUTPUT_CONFIG"] = str(newline_output)
            rejected = subprocess.run(
                ["sh", str(EXT_PROC_CONFIG_MATERIALIZER)],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(rejected.returncode, 2, rejected.stderr)
            self.assertIn("TLS certificate path contains an unsupported control character", rejected.stderr)
            self.assertFalse(newline_output.exists())

    def test_tls_renderer_explicitly_accepts_control_free_paths(self) -> None:
        renderer = TLS_YAML_RENDERER.read_text(encoding="utf-8")

        self.assertIn('        *) : ;;\n', renderer)

    def test_ext_authz_compat_runtime_uses_private_loopback_tls(self) -> None:
        source = EXT_AUTHZ_RUNTIME_PATH.read_text(encoding="utf-8")
        start_source = EXT_AUTHZ_START_PATH.read_text(encoding="utf-8")
        template = EXT_AUTHZ_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn("prepare-runtime-root --runtime-root \"$RUNTIME_ROOT\"", source)
        self.assertIn("serve-upstream --port \"$upstream_port\" \\", source)
        self.assertIn("--runtime-root \"$RUNTIME_ROOT\"", source)
        self.assertIn("--tls-certificate \"$TLS_CERTIFICATE\"", source)
        self.assertIn("--tls-private-key \"$TLS_PRIVATE_KEY\"", source)
        self.assertEqual(
            source.count("--runtime-root \"$RUNTIME_ROOT\" --tls-certificate \"$TLS_CERTIFICATE\""),
            2,
        )
        self.assertEqual(source.count("https://127.0.0.1:$listen_port"), 2)
        self.assertNotIn("http://127.0.0.1:$listen_port", source)
        self.assertIn('rm -f "$TLS_CERTIFICATE" "$TLS_PRIVATE_KEY"', source)
        self.assertIn("prepare-runtime-root --runtime-root \"$START_ROOT\"", start_source)
        self.assertIn("create_private_loopback_tls", start_source)
        self.assertIn('rm -f "$TLS_CERTIFICATE" "$TLS_PRIVATE_KEY"', start_source)
        self.assertIn("name: envoy.transport_sockets.tls", template)
        self.assertIn('filename: "@TLS_CERTIFICATE@"', template)
        self.assertIn('filename: "@TLS_PRIVATE_KEY@"', template)
        self.assertIn("type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext", template)
        self.assertIn("trusted_ca:", template)
        self.assertIn("uri: http://127.0.0.1:@AUTHZ_PORT@", template)
        self.assertNotIn("access_log_path:", template)
        self.assertIn("failure_mode_allow: false\n              allowed_headers:", template)
        self.assertNotIn("authorization_request:", template)

    def test_envoy_smokes_reject_unsafe_root_without_tls_cleanup(self) -> None:
        true_binary = shutil.which("true")
        self.assertIsNotNone(true_binary)

        cases = (
            (
                EXT_AUTHZ_START_PATH,
                "START_ROOT",
                {
                    "ENVOY_BIN": true_binary,
                    "SERVICE_BIN": true_binary,
                },
                "START_ROOT is unsafe for private runtime artifacts",
            ),
            (
                EXT_AUTHZ_RUNTIME_PATH,
                "RUNTIME_ROOT",
                {
                    "ENVOY_BIN": true_binary,
                    "SERVICE_BIN": true_binary,
                },
                "RUNTIME_ROOT is unsafe for private runtime artifacts",
            ),
            (
                RUNTIME_PATH,
                "RUNTIME_ROOT",
                {
                    "ENVOY_BIN": true_binary,
                    "EXT_PROC_BIN": true_binary,
                    "MSCONNECTOR_RULES_FILE": str(
                        ROOT / "common" / "rules" / "modsecurity_targeted_smoke.conf"
                    ),
                },
                "RUNTIME_ROOT is unsafe for private runtime artifacts",
            ),
        )

        for script, root_variable, extra_environment, expected_error in cases:
            with self.subTest(script=script.name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                target = root / "target"
                target.mkdir()
                certificate = target / "envoy-loopback.crt"
                private_key = target / "envoy-loopback.key"
                certificate.write_text("certificate marker", encoding="utf-8")
                private_key.write_text("private key marker", encoding="utf-8")
                unsafe_root = root / "unsafe-root"
                unsafe_root.symlink_to(target, target_is_directory=True)
                environment = dict(os.environ)
                environment.update(extra_environment)
                environment.update({
                    root_variable: str(unsafe_root),
                    "PYTHON": sys.executable,
                })

                completed = subprocess.run(
                    ["sh", str(script)],
                    cwd=ROOT,
                    env=environment,
                    text=True,
                    capture_output=True,
                    check=False,
                )

                self.assertEqual(completed.returncode, 1, completed.stderr)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual(certificate.read_text(encoding="utf-8"), "certificate marker")
                self.assertEqual(private_key.read_text(encoding="utf-8"), "private key marker")

    def test_runtime_probe_keeps_cancellation_unattributed_and_nonpromoting(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        self.assertIn("ENVOY_TRANSPORT_CANCEL_PROBE", source)
        self.assertIn("grpc_context_canceled_unattributed", source)
        self.assertIn("grpc_peer_eof", source)
        self.assertIn("expected exactly one unattributed ext_proc terminal completion", source)
        self.assertIn("client_disconnect_after_first_response_chunk", source)
        self.assertIn("transport-observations.diagnostic.json", source)
        self.assertIn('"capability_promotion": "not_permitted"', source)
        self.assertIn('"state": "NOT_EXECUTED"', source)
        self.assertIn('"diagnostic_only": True', source)
        self.assertNotIn('"transport_case_id":', source)
        self.assertIn("client-cancel", source)
        self.assertIn("FULL_LIFECYCLE_EVIDENCE_OUTPUT", source)
        self.assertIn("phase4-first-byte", source)
        self.assertIn("phase4_first_byte_before_response_end_status", source)
        self.assertIn("phase4_no_full_response_buffering_status", source)
        self.assertIn("phase4_end_of_stream_evaluation_status", source)
        self.assertIn("phase4_rule_observed_status", source)
        self.assertIn("write-allow-event", source)
        self.assertIn("prepare-runtime-root", source)
        self.assertIn("envoy.transport_sockets.tls", source)
        self.assertIn('https://127.0.0.1:$listen_port', source)

    def test_runtime_uses_an_unambiguous_allow_transaction(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")

        self.assertIn("READINESS_TRANSACTION_ID=envoy-ext-proc-readiness-1", source)
        self.assertIn("ALLOW_TRANSACTION_ID=envoy-ext-proc-allow-1", source)
        self.assertIn('X-Request-Id: $READINESS_TRANSACTION_ID', source)
        self.assertIn('X-Request-Id: $ALLOW_TRANSACTION_ID', source)
        self.assertIn('READINESS_PROBE_EVIDENCE="$RUNTIME_ROOT/readiness-probe.json"', source)
        self.assertIn('ALLOW_PROBE_EVIDENCE="$RUNTIME_ROOT/allow-probe.json"', source)
        executor_start = source.index('\"$PYTHON_BIN\" \"$MRTS_RUNTIME_EXECUTOR\"')
        executor_end = source.index("    mrts_executor_rc=$?", executor_start)
        executor_source = source[executor_start:executor_end]
        self.assertIn('--runtime-root \"$VERIFIED_RUN_ROOT\"', executor_source)
        self.assertIn('--plan-sha256 \"$MRTS_RUNTIME_PLAN_SHA256\"', executor_source)
        self.assertNotIn('--runtime-root \"$RUNTIME_ROOT\"', executor_source)

    def test_mrts_rule_match_evidence_is_after_sealed_plan_validation(self) -> None:
        source = RUNTIME_PATH.read_text(encoding="utf-8")
        validation = source.index("validate_mrts_runtime_inputs\ntrap cleanup")
        materializer = source.index('OUTPUT_CONFIG="$EXT_PROC_RUNTIME_CONFIG"')
        self.assertLess(validation, materializer)
        self.assertIn("transaction_id_header=x-mrts-transaction-id", source)
        self.assertIn("emit_rule_match_evidence=on", source)
        self.assertIn("transaction_id_header=x-request-id", source)
        self.assertIn("emit_rule_match_evidence=off", source)
        self.assertIn("MRTS_RUNTIME_PLAN_SHA256", source)
        self.assertIn('--plan-sha256 \"$MRTS_RUNTIME_PLAN_SHA256\"', source)


if __name__ == "__main__":
    unittest.main()
