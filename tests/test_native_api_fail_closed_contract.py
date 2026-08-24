"""Regression contracts for libmodsecurity's boolean C API result handling."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMMON_RUNTIME = (ROOT / "common" / "runtime" / "msconnector_runtime.c").read_text(encoding="utf-8")
HAPROXY = (ROOT / "connectors" / "haproxy" / "src" / "haproxy_modsecurity_binding.c").read_text(encoding="utf-8")
APACHE_FILTERS = (ROOT / "connectors" / "apache" / "src" / "msc_filters.c").read_text(encoding="utf-8")


def requires_success(source: str, operation: str) -> bool:
    return re.search(rf"{operation}\([^;]*?\)\s*!=\s*1", source, re.DOTALL) is not None


class NativeAPIFailClosedContractTests(unittest.TestCase):
    def test_common_runtime_rejects_every_boolean_native_failure(self) -> None:
        for operation in ("msc_process_connection", "msc_process_uri", "msc_set_request_hostname", "msc_add_n_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_add_n_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(COMMON_RUNTIME, operation))

    def test_haproxy_rejects_zero_from_legacy_and_streaming_body_paths(self) -> None:
        for operation in ("msc_process_connection", "msc_add_request_header", "msc_process_request_headers", "msc_append_request_body", "msc_process_request_body", "msc_process_uri", "msc_add_response_header", "msc_process_response_headers"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(HAPROXY, operation))
        self.assertIn("phase->append_body(transaction->transaction, body, (size_t)body_len) != 1", HAPROXY)
        self.assertIn("phase->finish_body(transaction->transaction) != 1", HAPROXY)

    def test_apache_response_mapping_and_body_paths_reject_zero(self) -> None:
        for operation in ("msc_process_request_body", "msc_append_request_body", "msc_add_response_header", "msc_process_response_headers", "msc_append_response_body", "msc_process_response_body"):
            with self.subTest(operation=operation):
                self.assertTrue(requires_success(APACHE_FILTERS, operation))


if __name__ == "__main__":
    unittest.main()
