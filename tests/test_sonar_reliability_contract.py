#!/usr/bin/env python3
"""Focused source contracts for current Sonar reliability repairs."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SonarReliabilityContractTests(unittest.TestCase):
    def test_traefik_result_payload_never_copies_a_null_optional_field(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        self.assertIn("transaction_id != NULL && transaction_id_size > 0U", source)
        self.assertIn("rule_id != NULL && rule_id_size > 0U", source)
        self.assertIn("redirect != NULL && redirect_size > 0U", source)

    def test_authorization_listener_initializes_peer_and_local_socket_state(self) -> None:
        source = (
            ROOT / "common" / "runtime" / "http_authorization_service.c"
        ).read_text(encoding="utf-8")
        self.assertIn("struct sockaddr_in local = {0};", source)
        self.assertIn("struct sockaddr_in peer = {0};", source)

    def test_traefik_runtime_lock_pairs_keep_stable_service_references(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        destroy_start = source.index("static void traefik_engine_session_destroy")
        destroy_end = source.index(
            "\n}\n\nstatic int traefik_engine_handle_begin", destroy_start
        )
        destroy = source[destroy_start:destroy_end]
        begin_start = destroy_end
        begin_end = source.index(
            "\n}\n\nstatic int traefik_engine_handle_request_chunk", begin_start
        )
        begin = source[begin_start:begin_end]

        self.assertNotIn("traefik_engine_lock_runtime", source)
        self.assertNotIn("traefik_engine_unlock_runtime", source)
        self.assertIn("traefik_engine_service *service;", destroy)
        self.assertIn("service = session->service;", destroy)
        self.assertIn("pthread_mutex_lock(&service->runtime_lock)", destroy)
        self.assertIn("pthread_mutex_unlock(&service->runtime_lock)", destroy)
        self.assertNotIn("session->service->runtime_lock", destroy)
        self.assertEqual(destroy.count("session->service"), 1)
        self.assertIn("traefik_engine_service *service;", begin)
        self.assertIn("service = session->service;", begin)
        self.assertIn("pthread_mutex_lock(&service->runtime_lock)", begin)
        self.assertIn("pthread_mutex_unlock(&service->runtime_lock)", begin)
        self.assertIn(
            "msconnector_runtime_transaction_begin(service->runtime,", begin
        )
        self.assertNotIn("session->service->runtime_lock", begin)
        self.assertEqual(begin.count("session->service"), 1)

    def test_oracle_handles_a_missing_optional_json_string_without_dereference(self) -> None:
        source = (ROOT / "ci" / "tools" / "native_modsecurity_oracle.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("if (value == NULL)", source)
        self.assertIn('fputs("\\\"\\\"", out);', source)
        self.assertIn("cursor = (const unsigned char *)value;", source)
        self.assertIn("json_string(out, whoami);", source)
        self.assertNotIn('json_string(out, whoami ? whoami : "");', source)

    def test_haproxy_startup_diagnostics_guard_the_standard_error_stream(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(source.count("if (stderr != NULL)"), 2)

    def test_haproxy_append_bytes_checks_the_source_extent_before_copying(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        append_bytes = source[
            source.index("static int append_bytes")
            : source.index("static int append_uint32")
        ]
        self.assertIn(
            "const void *data, size_t data_len, size_t len",
            append_bytes,
        )
        self.assertIn("if (len > data_len ||", append_bytes)
        self.assertLess(append_bytes.index("len > data_len"), append_bytes.index("memcpy("))
        self.assertIn(
            "append_bytes(buf, &net, sizeof(net), sizeof(net))",
            source,
        )
        self.assertIn("append_bytes(buf, value, len, len)", source)
        self.assertIn(
            "append_bytes(frame, payload->data, sizeof(payload->data), payload->len)",
            source,
        )

    def test_haproxy_accept_loop_retries_only_interrupted_accepts(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        accept_loop_start = source.index("static int accept_loop(")
        accept_loop_end = source.index(
            "\n}\n\nstatic int client_expect_frame", accept_loop_start
        )
        accept_loop = source[accept_loop_start:accept_loop_end]
        failed_accept_start = accept_loop.index("if (fd < 0) {")
        success_start = accept_loop.index("handle_connection(", failed_accept_start)
        failed_accept = accept_loop[failed_accept_start:success_start]
        terminal_error_start = failed_accept.index("if (errno != EINTR) {")
        interrupted_stop_start = failed_accept.index("if (stop_requested) {")
        terminal_error = failed_accept[
            terminal_error_start:interrupted_stop_start
        ]
        interrupted_accept = failed_accept[interrupted_stop_start:]

        self.assertNotIn("if (errno == EINTR)", failed_accept)
        self.assertIn(
            'log_line(log, "accept failed errno=%d", errno);', terminal_error
        )
        self.assertIn("return 1;", terminal_error)
        self.assertLess(
            terminal_error.index('log_line(log, "accept failed errno=%d", errno);'),
            terminal_error.index("return 1;"),
        )
        self.assertNotIn("if (stop_requested)", terminal_error)
        self.assertIn("break;", interrupted_accept)
        self.assertIn("continue;", interrupted_accept)
        self.assertLess(
            interrupted_accept.index("break;"), interrupted_accept.index("continue;")
        )
        self.assertNotIn("return 1;", interrupted_accept)
        self.assertNotIn("handle_connection(", failed_accept)
        self.assertNotIn("close(fd);", failed_accept)
        self.assertNotIn("handled++;", failed_accept)

        success_path = accept_loop[success_start:]
        self.assertLess(
            success_path.index("handle_connection("), success_path.index("close(fd);")
        )
        self.assertLess(
            success_path.index("close(fd);"), success_path.index("handled++;"),
        )


if __name__ == "__main__":
    unittest.main()
