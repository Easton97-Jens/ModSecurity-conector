"""Regression contracts for Apache native request-processing failures."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"


def function_body(source: str, signature: str) -> str:
    start = source.index(signature)
    while True:
        opening = source.find("{", start + len(signature))
        semicolon = source.find(";", start + len(signature), opening)
        if opening >= 0 and (semicolon < 0 or opening < semicolon):
            break
        start = source.index(signature, start + len(signature))
    depth = 0
    for index in range(opening, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise AssertionError(f"unterminated function: {signature}")


class ApacheFailClosedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MODULE.read_text(encoding="utf-8")
        self.headers = function_body(self.source, "static int process_request_headers(request_rec *r, msc_t *msr)")
        self.late_hook = function_body(self.source, "static int hook_request_late(request_rec *r)")

    def test_each_native_failure_returns_before_intervention_or_handler(self) -> None:
        for operation in ("msc_process_uri", "msc_add_request_header", "msc_process_request_headers"):
            with self.subTest(operation=operation):
                call = self.headers.index(f"{operation}(")
                failure = self.headers.index(f'return apache_fail_closed(r, "{operation}");', call)
                self.assertLess(call, failure)

    def test_connection_failure_is_fail_closed_in_the_late_hook(self) -> None:
        call = self.late_hook.index("msc_process_connection(")
        failure = self.late_hook.index('return apache_fail_closed(r, "msc_process_connection");', call)
        self.assertLess(call, failure)
        self.assertLess(failure, self.late_hook.index("process_request_headers"))

    def test_all_checked_native_api_calls_require_the_success_value(self) -> None:
        for operation in ("msc_process_connection", "msc_process_uri", "msc_add_request_header", "msc_process_request_headers"):
            with self.subTest(operation=operation):
                self.assertRegex(self.source, re.compile(rf"{operation}\([^;]*?\)\s*!=\s*1", re.DOTALL))

    def test_fail_closed_keeps_connection_close_and_owner_cleanup_contract(self) -> None:
        helper = function_body(self.source, "static int apache_fail_closed(")
        self.assertIn("return HTTP_INTERNAL_SERVER_ERROR;", helper)
        self.assertIn("r->connection->keepalive = AP_CONN_CLOSE;", helper)
        self.assertIn("apr_pool_cleanup_register(r->pool, msr,", self.source)
        self.assertIn("msc_cleanup_request_transaction, apr_pool_cleanup_null);", self.source)


if __name__ == "__main__":
    unittest.main()
