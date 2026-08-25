"""Source-level regression checks for HTX fail-closed payload handling."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FILTER = ROOT / "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c"


def _http_payload_body() -> str:
    source = FILTER.read_text(encoding="utf-8")
    match = re.search(
        r"static int haproxy_modsecurity_htx_filter_http_payload\(.*?\n}\n\nstatic int haproxy_modsecurity_htx_finish_request",
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("HTX payload callback is missing")
    return match.group(0)


def _http_headers_body() -> str:
    source = FILTER.read_text(encoding="utf-8")
    match = re.search(
        r"static int haproxy_modsecurity_htx_filter_http_headers\(.*?\n}\n\nstatic int haproxy_modsecurity_htx_filter_http_payload",
        source,
        re.DOTALL,
    )
    if match is None:
        raise AssertionError("HTX headers callback is missing")
    return match.group(0)


class HAProxyHTXFilterSecurityContractTest(unittest.TestCase):
    def test_request_append_failure_cannot_return_forward_length(self) -> None:
        body = _http_payload_body()
        self.assertRegex(
            body,
            r"(?s)haproxy_modsecurity_htx_append_request_payload\(filter, msg, offset, len\) != 0\)\s*\{.*?return -1;",
        )

    def test_response_append_failure_cannot_return_forward_length(self) -> None:
        body = _http_payload_body()
        self.assertRegex(
            body,
            r"(?s)haproxy_modsecurity_htx_append_response_payload\(filter, msg, offset, len\) != 0\)\s*\{.*?return -1;",
        )

    def test_disabled_pass_through_is_distinct_from_append_failure(self) -> None:
        body = _http_payload_body()
        self.assertGreaterEqual(body.count("return (int)len;"), 3)
        self.assertGreaterEqual(body.count("return -1;"), 5)

    def test_missing_transaction_is_not_merged_with_disabled_pass_through(self) -> None:
        body = _http_payload_body()
        self.assertRegex(
            body,
            r"(?s)if \(ctx->disabled\) \{.*?return \(int\)len;.*?if \(!ctx->transaction\) \{.*?return -1;",
        )

    def test_response_payload_without_headers_fails_closed(self) -> None:
        body = _http_payload_body()
        self.assertRegex(
            body,
            r"(?s)if \(!ctx->transaction \|\| !ctx->response_headers_seen\) \{.*?return -1;",
        )

    def test_htx_request_and_response_payloads_have_cumulative_finite_budgets(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        self.assertIn("request_body_limit", source)
        self.assertIn("response_body_limit", source)
        self.assertIn("*body_bytes_seen > body_limit - value.len", source)
        self.assertIn("*body_bytes_seen += value.len", source)
        self.assertIn("body_limit == 0U", source)

    def test_request_setup_failure_aborts_before_a_payload_callback_can_pass(self) -> None:
        body = _http_headers_body()
        self.assertRegex(
            body,
            r"(?s)haproxy_modsecurity_htx_capture_request_headers\(filter, msg\) != 0\s*\|\|\s*"
            r"haproxy_modsecurity_htx_begin_request\(s, filter\) != 0\)\s*\{\s*"
            r"ctx->fail_closed = 1;\s*haproxy_modsecurity_htx_abort_context\(ctx\);\s*return -1;",
        )

    def test_request_setup_uses_only_real_frontend_endpoint_metadata(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        begin = source[source.index(
            "static int haproxy_modsecurity_htx_begin_request("
        ):source.index(
            "static int haproxy_modsecurity_htx_append_payload(",
            source.index("static int haproxy_modsecurity_htx_begin_request("),
        )]
        endpoint_start = source.index(
            "static int haproxy_modsecurity_htx_capture_request_endpoints("
        )
        endpoints = source[endpoint_start:source.index(
            "static int haproxy_modsecurity_htx_begin_request(", endpoint_start
        )]

        self.assertIn("#include <haproxy/sc_strm.h>", source)
        self.assertIn("sc_src(s->scf)", endpoints)
        self.assertIn("sc_dst(s->scf)", endpoints)
        self.assertIn("addr_to_str(client_endpoint, client_address", endpoints)
        self.assertIn("addr_to_str(server_endpoint, server_address", endpoints)
        self.assertIn("get_host_port(client_endpoint)", endpoints)
        self.assertIn("get_host_port(server_endpoint)", endpoints)
        self.assertIn("client_family <= 0 || server_family <= 0", endpoints)
        self.assertNotIn('"127.0.0.1"', endpoints)
        self.assertNotIn("49152", endpoints)
        self.assertRegex(
            begin,
            r"(?s)haproxy_modsecurity_htx_capture_request_endpoints\(s, &request,\s*"
            r"client_address, server_address\) != 0\) \{\s*return -1;",
        )

    def test_setup_failure_marks_context_fail_closed_before_payload_gate(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        headers = _http_headers_body()
        payload = _http_payload_body()
        self.assertIn("int fail_closed;", source)
        self.assertRegex(
            headers,
            r"(?s)if \(haproxy_modsecurity_htx_capture_request_headers\(filter, msg\) != 0 \|\|\s*"
            r"haproxy_modsecurity_htx_begin_request\(s, filter\) != 0\) \{\s*"
            r"ctx->fail_closed = 1;\s*haproxy_modsecurity_htx_abort_context\(ctx\);\s*return -1;",
        )
        self.assertRegex(
            headers,
            r"(?s)haproxy_modsecurity_htx_process_response_headers\(s, filter, msg\) != 0\) \{\s*"
            r"ctx->fail_closed = 1;\s*haproxy_modsecurity_htx_abort_context\(ctx\);\s*return -1;",
        )
        self.assertRegex(
            headers,
            r"(?s)if \(ctx->fail_closed\) \{\s*"
            r"haproxy_modsecurity_htx_abort_context\(ctx\);\s*return -1;\s*\}\s*"
            r"if \(msg->chn->flags & CF_ISRESP\)",
        )
        self.assertRegex(
            payload,
            r"(?s)if \(ctx->fail_closed\) \{.*?return -1;\s*\}\s*if \(ctx->disabled\) \{.*?return \(int\)len;",
        )

    def test_unmappable_request_intervention_fails_closed_instead_of_disabling(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        self.assertRegex(
            source,
            r"(?s)static int haproxy_modsecurity_htx_begin_request\(.*?"
            r"if \(decision\.disruptive\) \{\s*"
            r"if \(!haproxy_modsecurity_htx_apply_precommit_deny\(s, ctx, &decision\)\) \{\s*"
            r"ctx->fail_closed = 1;\s*"
            r"haproxy_modsecurity_htx_abort_context\(ctx\);\s*"
            r"return -1;",
        )

    def test_unmappable_response_intervention_fails_closed_instead_of_disabling(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        self.assertRegex(
            source,
            r"(?s)static int haproxy_modsecurity_htx_process_response_headers\(.*?"
            r"if \(decision\.disruptive\) \{\s*"
            r"if \(!haproxy_modsecurity_htx_apply_precommit_deny\(s, ctx, &decision\)\) \{\s*"
            r"ctx->fail_closed = 1;\s*"
            r"haproxy_modsecurity_htx_abort_context\(ctx\);\s*"
            r"return -1;",
        )

    def test_request_body_finalization_error_latches_fail_closed(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        self.assertRegex(
            source,
            r"(?s)static int haproxy_modsecurity_htx_finish_request\(.*?"
            r"haproxy_modsecurity_transaction_finish_request_body\(\s*"
            r"ctx->transaction, &decision\) != 0\) \{\s*"
            r"ctx->fail_closed = 1;\s*"
            r"haproxy_modsecurity_htx_abort_context\(ctx\);\s*"
            r"return -1;",
        )

    def test_unmappable_precommit_request_body_intervention_latches_fail_closed(self) -> None:
        source = FILTER.read_text(encoding="utf-8")
        self.assertRegex(
            source,
            r"(?s)static int haproxy_modsecurity_htx_finish_request\(.*?"
            r"if \(!ctx->response_headers_seen && !ctx->response_started_before_request_eos &&\s*"
            r"haproxy_modsecurity_htx_apply_precommit_deny\(s, ctx, &decision\)\) \{.*?"
            r"ctx->fail_closed = 1;\s*"
            r"haproxy_modsecurity_htx_abort_context\(ctx\);\s*"
            r"return -1;",
        )


if __name__ == "__main__":
    unittest.main()
