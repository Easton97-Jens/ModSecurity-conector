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

    def test_traefik_runtime_lock_pair_is_visible_at_each_call_site(self) -> None:
        source = (
            ROOT / "connectors" / "traefik" / "src" / "traefik_engine_service.c"
        ).read_text(encoding="utf-8")
        self.assertNotIn("traefik_engine_lock_runtime", source)
        self.assertNotIn("traefik_engine_unlock_runtime", source)
        self.assertGreaterEqual(
            source.count("pthread_mutex_lock(&session->service->runtime_lock)"), 10
        )
        self.assertGreaterEqual(
            source.count("pthread_mutex_unlock(&session->service->runtime_lock)"), 10
        )

    def test_oracle_handles_a_missing_optional_json_string_without_dereference(self) -> None:
        source = (ROOT / "ci" / "tools" / "native_modsecurity_oracle.c").read_text(
            encoding="utf-8"
        )
        self.assertIn("if (value == NULL)", source)
        self.assertIn('fputs("\\\"\\\"", out);', source)
        self.assertIn("cursor = (const unsigned char *)value;", source)

    def test_haproxy_startup_diagnostics_guard_the_standard_error_stream(self) -> None:
        source = (
            ROOT
            / "connectors"
            / "haproxy"
            / "src"
            / "haproxy_spop_diagnostic_runtime.c"
        ).read_text(encoding="utf-8")
        self.assertGreaterEqual(source.count("if (stderr != NULL)"), 2)


if __name__ == "__main__":
    unittest.main()
