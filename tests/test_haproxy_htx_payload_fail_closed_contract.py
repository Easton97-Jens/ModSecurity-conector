"""Regression contract for native HAProxy HTX payload-failure handling."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "connectors/haproxy/htx-overlay/haproxy_modsecurity_htx_filter.c").read_text(
    encoding="utf-8",
)


class HAProxyHTXPayloadFailClosedContractTest(unittest.TestCase):
    def test_request_append_failure_returns_negative_before_forwarding(self) -> None:
        request_branch = SOURCE.split("if (!(msg->chn->flags & CF_ISRESP)) {", 1)[1].split(
            "    if (ctx->disabled || !ctx->transaction || !ctx->response_headers_seen", 1,
        )[0]

        self.assertIn("haproxy_modsecurity_htx_append_request_payload", request_branch)
        self.assertIn("haproxy_modsecurity_htx_abort_context(ctx);", request_branch)
        self.assertIn("return -1;", request_branch)
        self.assertIn("return (int)len;", request_branch)
        self.assertLess(
            request_branch.index("haproxy_modsecurity_htx_abort_context(ctx);"),
            request_branch.index("return -1;"),
        )

    def test_response_append_failure_stops_only_affected_stream(self) -> None:
        response_branch = SOURCE.split(
            "if (ctx->disabled || !ctx->transaction || !ctx->response_headers_seen", 1,
        )[1].split("    /* Never hold or delay output", 1)[0]

        self.assertIn("haproxy_modsecurity_htx_append_response_payload", response_branch)
        self.assertIn("haproxy_modsecurity_htx_abort_context(ctx);", response_branch)
        self.assertIn("return -1;", response_branch)
        self.assertIn("ctx->response_headers_committed = 1;", response_branch)


if __name__ == "__main__":
    unittest.main()
