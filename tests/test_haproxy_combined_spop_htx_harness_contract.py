"""Static safety and wiring contracts for the local HAProxy combined harness."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "connectors" / "haproxy" / "harness" / "combined_spop_htx"
RUNNER = HARNESS / "run_combined_spop_htx.sh"
BACKEND = HARNESS / "backend.py"
P3_RULES = HARNESS / "rules-p3-deny.conf"
P4_RULES = HARNESS / "rules-p4-safe.conf"
MRC1_HEADER = ROOT / "common" / "runtime" / "response_companion_transport.h"
MRC1_CLIENT = ROOT / "common" / "runtime" / "response_companion_client.c"
HTX_FILTER = ROOT / "connectors" / "haproxy" / "htx-overlay" / "haproxy_modsecurity_htx_filter.c"


class HaproxyCombinedSpopHtxHarnessContractTests(unittest.TestCase):
    def test_runner_is_shell_syntax_valid(self) -> None:
        result = subprocess.run(
            ["sh", "-n", str(RUNNER)], check=False, capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_current_sources_must_select_mrc1_v2_without_v1_fallback(self) -> None:
        header = MRC1_HEADER.read_text(encoding="utf-8")
        client = MRC1_CLIENT.read_text(encoding="utf-8")
        filter_source = HTX_FILTER.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")

        self.assertIn(
            "#define MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_PROTOCOL_VERSION 2U",
            header,
        )
        self.assertIn("There is deliberately no v1", header)
        self.assertIn(
            "msconnector_response_companion_client_cancel_with_cause", client
        )
        self.assertIn(
            "msconnector_response_companion_client_cancel_with_cause", filter_source
        )
        self.assertIn("assert_mrc1_v2", runner)
        self.assertIn("MRC1 protocol version 2", runner)

    def test_requires_explicit_external_paths_and_distinct_loopback_ports(self) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        for name in (
            "COMBINED_SPOP_HTX_RUNTIME_ROOT",
            "COMBINED_SPOP_HTX_ALLOWED_ROOT",
            "COMBINED_SPOP_HTX_HAPROXY_SOURCE_DIR",
            "COMBINED_SPOP_HTX_MODSECURITY_INCLUDE_DIR",
            "COMBINED_SPOP_HTX_MODSECURITY_LIB_DIR",
            "COMBINED_SPOP_HTX_MODSECURITY_LIBRARY",
            "COMBINED_SPOP_HTX_HAPROXY_PORT",
            "COMBINED_SPOP_HTX_SPOA_PORT",
            "COMBINED_SPOP_HTX_BACKEND_PORT",
        ):
            self.assertIn(name, runner)
        self.assertIn("fresh direct child", runner)
        self.assertIn("selected ports must be distinct", runner)
        self.assertIn("bind 127.0.0.1:$HAPROXY_PORT", runner)
        self.assertIn("server app 127.0.0.1:$BACKEND_PORT", runner)
        self.assertIn("server agent 127.0.0.1:$SPOA_PORT", runner)

    def test_private_uds_and_cleanup_are_owned_and_bounded(self) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertIn('PRIVATE_ROOT="$RUN_ROOT/private"', runner)
        self.assertIn('chmod 700 "$PRIVATE_ROOT"', runner)
        self.assertIn('SOCKET_PATH="$PRIVATE_ROOT/mrc1-v2.sock"', runner)
        self.assertIn('trap cleanup EXIT', runner)
        self.assertIn('stop_process_group', runner)
        self.assertIn('rm -f -- "$SOCKET_PATH"', runner)
        self.assertNotIn("rm -rf", runner)
        self.assertIn("refusing pre-existing MRC1 socket path", runner)
        self.assertIn("SPOP did not remove the MRC1 socket it owned", runner)

    def test_wires_spoe_request_ack_to_native_htx_mrc1_response_path(self) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertIn("filter spoe engine modsecurity config", runner)
        self.assertIn("filter modsecurity-htx response-companion-socket", runner)
        self.assertIn("response-companion=native-htx", runner)
        self.assertIn("register-var-names blocked action status redirect_url rule_id phase error response_handle", runner)
        self.assertIn("http-request send-spoe-group modsecurity request-check", runner)
        self.assertIn("phase4-mode safe", runner)
        self.assertNotIn("http-response send-spoe-group", runner)
        self.assertIn("assert_p2_evidence", runner)
        self.assertIn("run_case p3-deny", runner)
        self.assertIn("run_case p4-safe", runner)

    def test_covers_cancel_ttl_missing_correlation_and_connection_reuse(self) -> None:
        runner = RUNNER.read_text(encoding="utf-8")
        self.assertIn("run_cancel_case", runner)
        self.assertIn("--max-time 1", runner)
        self.assertIn("cancel_status" , runner)
        self.assertIn("run_ttl_case", runner)
        self.assertIn("write_agent_config \"$case_name\" \"$P4_RULES\" 100", runner)
        self.assertIn("ttl_curl_status", runner)
        self.assertIn("TTL expiry expected curl status 18", runner)
        self.assertIn("fail-closed postcommit response-companion body", runner)
        self.assertIn("missing-correlation", runner)
        self.assertIn("run_connection_reuse_case", runner)
        self.assertIn("same_tcp_connection", runner)
        self.assertIn("Connection: keep-alive", runner)

    def test_backend_never_logs_body_payloads_and_fixture_rules_are_phase_specific(self) -> None:
        backend = BACKEND.read_text(encoding="utf-8")
        p3 = P3_RULES.read_text(encoding="utf-8")
        p4 = P4_RULES.read_text(encoding="utf-8")
        compile(backend, str(BACKEND), "exec")
        self.assertIn("self.rfile.read(content_length)", backend)
        self.assertIn('json.dump({"route": path, "slow": bool(delay_seconds)}, log)', backend)
        self.assertNotIn("request_body", backend)
        self.assertIn("ThreadingHTTPSServer", backend)
        self.assertIn("certfile=args.cert_file, keyfile=args.key_file", backend)
        self.assertNotIn("wrap_socket", backend)
        self.assertIn('server app 127.0.0.1:$BACKEND_PORT ssl verify none', RUNNER.read_text(encoding="utf-8"))
        self.assertIn("phase:3,deny,status:403", p3)
        self.assertIn("RESPONSE_HEADERS:X-Combined-Decision", p3)
        self.assertIn("phase:4,deny,status:403", p4)
        self.assertIn("RESPONSE_BODY", p4)


if __name__ == "__main__":
    unittest.main()
