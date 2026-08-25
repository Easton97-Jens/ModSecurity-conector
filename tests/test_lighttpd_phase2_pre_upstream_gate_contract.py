from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = ROOT / "connectors" / "lighttpd" / "module" / "mod_msconnector.c"
GATE_HARNESS = ROOT / "connectors" / "lighttpd" / "harness" / "run_phase2_pre_upstream_gate.py"


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
        self.assertIn("if (!ctx->request_body_gate_rejected) {", self.source)

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


if __name__ == "__main__":
    unittest.main()
