from __future__ import annotations

import importlib.util
import json
import re
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = ROOT / "connectors" / "lighttpd" / "module" / "mod_msconnector.c"
GATE_HARNESS = ROOT / "connectors" / "lighttpd" / "harness" / "run_phase2_pre_upstream_gate.py"
RUNTIME_SOURCE = ROOT / "common" / "runtime" / "msconnector_runtime.c"
RUNTIME_HEADER = ROOT / "common" / "runtime" / "msconnector_runtime.h"


def load_gate_harness() -> object:
    spec = importlib.util.spec_from_file_location("phase2_pre_upstream_gate", GATE_HARNESS)
    if spec is None or spec.loader is None:
        raise AssertionError("could not import the Phase-2 gate harness")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


GATE_RUNNER = load_gate_harness()


def function_body(source: str, name: str, next_name: str) -> str:
    match = re.search(
        rf"static handler_t {name}\([\s\S]*?\n}}\n\nstatic [\s\S]*? {next_name}\(",
        source,
    )
    if match is None:
        raise AssertionError(f"could not locate {name}")
    return match.group(0)


class LighttpdPhase2PreUpstreamGateContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = MODULE_SOURCE.read_text(encoding="utf-8")
        cls.harness = GATE_HARNESS.read_text(encoding="utf-8")
        cls.runtime_source = RUNTIME_SOURCE.read_text(encoding="utf-8")
        cls.runtime_header = RUNTIME_HEADER.read_text(encoding="utf-8")
        cls.prepare = function_body(
            cls.source,
            "mod_msconnector_prepare_request_body",
            "mod_msconnector_handle_request_body",
        )
        cls.request_body_hook = function_body(
            cls.source,
            "mod_msconnector_handle_request_body",
            "mod_msconnector_response_body_committed",
        )

    def test_prepare_keeps_active_request_streaming_disabled_before_body_read(self) -> None:
        clear_active_streaming = (
            "r->conf.stream_request_body &=\n"
            "      ~(FDEVENT_STREAM_REQUEST | FDEVENT_STREAM_REQUEST_BUFMIN);"
        )
        self.assertIn(clear_active_streaming, self.prepare)
        self.assertLess(
            self.prepare.index(clear_active_streaming),
            self.prepare.index("rc = r->con->reqbody_read(r);"),
        )
        self.assertNotIn("|= FDEVENT_STREAM_REQUEST", self.prepare)

    def test_prepare_rejects_all_known_alternate_stream_activation_paths(self) -> None:
        active_streaming = "FDEVENT_STREAM_REQUEST | FDEVENT_STREAM_REQUEST_BUFMIN"
        self.assertIn(active_streaming, self.prepare)
        self.assertIn("HTTP_HEADER_INCREMENTAL", self.prepare)
        self.assertIn('CONST_STR_LEN("Incremental")', self.prepare)
        self.assertIn("HTTP_HEADER_UPGRADE", self.prepare)
        self.assertIn('CONST_STR_LEN("Upgrade")', self.prepare)
        self.assertGreaterEqual(
            self.prepare.count("mod_msconnector_reject_request_body_gate_conflict("),
            3,
        )
        self.assertIn(
            "msconnector_runtime_body_limit_action(p->runtime)", self.source
        )
        self.assertIn("MSCONNECTOR_BODY_LIMIT_ACTION_REJECT", self.source)
        self.assertIn(
            "requires body_limit_action=reject to retain a bounded pre-upstream request-body buffer",
            self.source,
        )

    def test_body_hook_fails_closed_if_streaming_is_reactivated_before_eos(self) -> None:
        active_streaming = "FDEVENT_STREAM_REQUEST | FDEVENT_STREAM_REQUEST_BUFMIN"
        self.assertIn(active_streaming, self.request_body_hook)
        self.assertIn(
            '"streaming became active before Phase-2 completion"',
            self.request_body_hook,
        )
        self.assertLess(
            self.request_body_hook.index(active_streaming),
            self.request_body_hook.index("if (stream_offset != ctx->request_body_next_offset)"),
        )

    def test_conflict_response_is_explicitly_fail_closed(self) -> None:
        self.assertIn(
            "static handler_t mod_msconnector_reject_request_body_gate_conflict(",
            self.source,
        )
        self.assertIn("return http_status_set_err(r, 501);", self.source)
        self.assertIn("int request_body_gate_rejected;", self.source)
        self.assertIn("ctx->request_body_gate_rejected = 1;", self.source)
        self.assertIn(
            "ctx->request_intervened || ctx->request_body_gate_rejected",
            self.source,
        )
        self.assertIn(
            "msconnector_runtime_transaction_finish_host_rejected_request_body(",
            self.source,
        )

    def test_body_limit_rejections_mark_the_host_rejected_p2_cleanup_path(self) -> None:
        declared_start = self.prepare.index("if (p->request_body_limit == 0U")
        declared_end = self.prepare.index("if (r->conf.stream_request_body", declared_start)
        declared = self.prepare[declared_start:declared_end]
        streamed_start = self.request_body_hook.index("if (length < 0 ||")
        streamed_end = self.request_body_hook.index("append.ctx = ctx;", streamed_start)
        streamed = self.request_body_hook[streamed_start:streamed_end]

        for limit_path in (declared, streamed):
            with self.subTest(limit_path=limit_path[:32]):
                marker = limit_path.index("ctx->request_body_gate_rejected = 1;")
                error_response = limit_path.index("mod_msconnector_error_response(")
                self.assertLess(marker, error_response)
                self.assertIn("MSCONNECTOR_ERROR_BODY_TOO_LARGE", limit_path)
        self.assertIn("if (ctx->request_body_gate_rejected) {", self.source)
        self.assertIn(
            "msconnector_runtime_transaction_finish_host_rejected_request_body(",
            self.source,
        )

    def test_gate_rejection_logs_without_synthesizing_request_body_eos(self) -> None:
        logging_start = self.runtime_source.index(
            "static int finish_transaction_with_logging("
        )
        start = self.runtime_source.index(
            "int msconnector_runtime_transaction_finish_host_rejected_request_body("
        )
        logging_finish = self.runtime_source[logging_start:start]
        end = self.runtime_source.index(
            "int msconnector_runtime_transaction_finish(", start
        )
        rejected_finish = self.runtime_source[start:end]
        self.assertIn(
            "msconnector_modsecurity_process_logging(&transaction->modsecurity, error)",
            logging_finish,
        )
        self.assertIn("transaction->finish_attempted = 1;", logging_finish)
        self.assertIn("transaction->finished = 1;", logging_finish)
        self.assertIn("return finish_transaction_with_logging(transaction, error);", rejected_finish)
        self.assertNotIn(
            "msconnector_runtime_transaction_finish_request_body(", rejected_finish
        )
        self.assertNotIn("MSCONNECTOR_PHASE_REQUEST_BODY", rejected_finish)
        self.assertIn("transaction->request_body.finished", rejected_finish)
        self.assertIn("transaction->response_headers_processed", rejected_finish)
        self.assertIn(
            "msconnector_runtime_transaction_finish_host_rejected_request_body(",
            self.runtime_header,
        )
        reset_start = self.source.index("REQUEST_FUNC(mod_msconnector_handle_request_reset)")
        reset = self.source[reset_start:]
        self.assertIn("if (ctx->request_body_gate_rejected) {", reset)
        self.assertIn(
            "msconnector_runtime_transaction_finish_host_rejected_request_body(",
            reset,
        )

    def test_normal_finish_keeps_its_request_and_response_eos_guards(self) -> None:
        start = self.runtime_source.index("int msconnector_runtime_transaction_finish(")
        end = self.runtime_source.index("const char *msconnector_runtime_transaction_id(", start)
        normal_finish = self.runtime_source[start:end]
        self.assertIn(
            "streaming request body reached transaction finish without end-of-stream",
            normal_finish,
        )
        self.assertIn(
            "response reached transaction finish without response-body end-of-stream",
            normal_finish,
        )
        self.assertIn(
            "return finish_transaction_with_logging(transaction, error);", normal_finish
        )

    def test_repository_owned_runtime_harness_covers_the_gate_and_alternate_paths(self) -> None:
        self.assertIn('"delayed_chunked_phase2_marker"', self.harness)
        self.assertIn('"delayed_chunked_phase2_allow"', self.harness)
        self.assertIn('"incremental-request-stream"', self.harness)
        self.assertIn('"body-bearing-upgrade-enabled"', self.harness)
        self.assertIn('"configured-request-stream"', self.harness)
        self.assertIn('"gw.upgrade-with-request-body" => "enable"', self.harness)
        self.assertIn('"upgrade" => "enable"', self.harness)
        self.assertIn('"process_partial_body_limit_action"', self.harness)
        self.assertIn('body_limit_action="process_partial"', self.harness)
        self.assertIn('"body_payload_persisted": False', self.harness)

    def test_delayed_allow_requires_content_length_reframing(self) -> None:
        allowed_size = 32
        valid_record = {
            "content_length_present": True,
            "declared_content_length": allowed_size,
            "received_body_wire_bytes": allowed_size,
            "transfer_encoding_chunked": False,
            "upstream_response_sent": True,
        }
        inputs = SimpleNamespace(host_endpoint=object())
        upstream = mock.Mock()
        upstream.accepted_connections.side_effect = [0, 1]
        summary: dict[str, object] = {"cases": []}
        with (
            mock.patch.object(
                GATE_RUNNER,
                "send_delayed_chunked",
                return_value=(200, {"accepted_connections": 0}),
            ),
            mock.patch.object(
                GATE_RUNNER,
                "await_completed_upstream",
                return_value=valid_record,
            ),
        ):
            GATE_RUNNER.run_delayed_allow_case(inputs, summary, upstream)
        delivery = summary["cases"][0]["upstream_delivery"]
        self.assertEqual(allowed_size, delivery["declared_content_length"])
        self.assertTrue(delivery["content_length_present"])
        self.assertFalse(delivery["transfer_encoding_chunked"])

    def test_delayed_allow_rejects_wrong_reframing_despite_correct_byte_count(self) -> None:
        valid_record = {
            "content_length_present": True,
            "declared_content_length": 32,
            "received_body_wire_bytes": 32,
            "transfer_encoding_chunked": False,
            "upstream_response_sent": True,
        }
        inputs = SimpleNamespace(host_endpoint=object())
        for key, value in (
            ("content_length_present", False),
            ("declared_content_length", 31),
            ("transfer_encoding_chunked", True),
        ):
            with self.subTest(key=key, value=value):
                record = {**valid_record, key: value}
                upstream = mock.Mock()
                upstream.accepted_connections.side_effect = [0, 1]
                with (
                    mock.patch.object(
                        GATE_RUNNER,
                        "send_delayed_chunked",
                        return_value=(200, {"accepted_connections": 0}),
                    ),
                    mock.patch.object(
                        GATE_RUNNER,
                        "await_completed_upstream",
                        return_value=record,
                    ),
                ):
                    with self.assertRaises(GATE_RUNNER.GateFailure):
                        GATE_RUNNER.run_delayed_allow_case(
                            inputs, {"cases": []}, upstream
                        )

    def test_runner_owns_distinct_numeric_loopback_ports_without_cli_port_inputs(self) -> None:
        endpoints = GATE_RUNNER.allocate_private_loopback_endpoints()
        ports = {endpoint.port for endpoint in endpoints}
        self.assertEqual(3, len(ports))
        self.assertTrue(all(1024 <= port <= 65535 for port in ports))
        self.assertNotIn("--host-port", self.harness)
        self.assertNotIn("--configured-host-port", self.harness)
        self.assertNotIn("--upstream-port", self.harness)
        self.assertNotIn("socket.create_connection", self.harness)
        self.assertIn('LOOPBACK_HOST = "127.0.0.1"', self.harness)

    def test_listener_probe_reads_tcp_listeners_without_running_ss(self) -> None:
        endpoint = GATE_RUNNER.LoopbackEndpoint.allocate()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind((GATE_RUNNER.LOOPBACK_HOST, endpoint.port))
            listener.listen(1)
            self.assertEqual(
                [f"{GATE_RUNNER.LOOPBACK_HOST}:{endpoint.port}"],
                GATE_RUNNER.listener_rows(endpoint),
            )
        self.assertEqual([], GATE_RUNNER.listener_rows(endpoint))
        self.assertNotIn('["ss",', self.harness)
        self.assertIn('Path("/proc/net/tcp")', self.harness)

    def test_runtime_root_rejects_a_symlink_and_persists_summary_by_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            target = base / "target"
            target.mkdir()
            link = base / "runtime-link"
            link.symlink_to(target, target_is_directory=True)
            with self.assertRaises(GATE_RUNNER.GateFailure):
                GATE_RUNNER.ensure_runtime_root(link)

            outside = base / "outside"
            outside.mkdir()
            for summary_name in GATE_RUNNER.SUMMARY_NAMES:
                summary_link = target / summary_name
                summary_link.symlink_to(outside / summary_name)
                with self.assertRaises(GATE_RUNNER.GateFailure):
                    GATE_RUNNER.ensure_runtime_root(target)
                summary_link.unlink()

            root = GATE_RUNNER.ensure_runtime_root(target)
            try:
                GATE_RUNNER.write_summary(root, {"result": "passed"})
            finally:
                root.close()
            self.assertEqual({"result": "passed"}, json.loads((target / "summary.json").read_text()))
            self.assertEqual(0o600, (target / "summary.json").stat().st_mode & 0o777)
        self.assertIn("os.O_NOFOLLOW", self.harness)
        self.assertIn("src_dir_fd=root.directory_fd", self.harness)
        self.assertIn('SUMMARY_TEMPORARY_NAME = "summary.json.tmp"', self.harness)
        self.assertEqual(1, self.harness.count('"summary.json.tmp"'))

    def test_runtime_root_rejects_group_writable_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "runtime-root"
            root.mkdir()
            root.chmod(0o770)
            with self.assertRaises(GATE_RUNNER.GateFailure):
                GATE_RUNNER.ensure_runtime_root(root)
        self.assertIn("stat.S_IWGRP | stat.S_IWOTH", self.harness)

    def test_runtime_child_creation_stays_on_the_pinned_root_descriptor(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            root_path = base / "runtime-root"
            outside = base / "outside"
            root_path.mkdir()
            outside.mkdir()
            root = GATE_RUNNER.ensure_runtime_root(root_path)
            try:
                (root_path / "normal").symlink_to(outside, target_is_directory=True)
                with self.assertRaises(GATE_RUNNER.GateFailure):
                    root.child("normal")
                (root_path / "normal").unlink()

                original_root = base / "pinned-runtime-root"
                root_path.rename(original_root)
                root_path.symlink_to(outside, target_is_directory=True)
                child = root.child("normal")
                try:
                    child.write_text("marker.txt", "pinned")
                    self.assertEqual(
                        "pinned",
                        (original_root / "normal" / "marker.txt").read_text(encoding="utf-8"),
                    )
                    self.assertFalse((outside / "normal" / "marker.txt").exists())
                    self.assertEqual(
                        f"/proc/self/fd/{child.directory_fd}/marker.txt",
                        child.runtime_path("marker.txt"),
                    )
                finally:
                    child.close()
            finally:
                root.close()
        self.assertIn("os.mkdir(name, 0o700, dir_fd=self.directory_fd)", self.harness)
        self.assertIn("pass_fds=root.inherited_fds()", self.harness)
        self.assertNotIn("root.mkdir(parents=True)", self.harness)


if __name__ == "__main__":
    unittest.main()
