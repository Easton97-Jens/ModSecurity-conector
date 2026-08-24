"""Regression contracts for stateful HAProxy SPOP response processing."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"
).read_text(encoding="utf-8")


class HAProxySPOPTransactionCacheContractTests(unittest.TestCase):
    """Keep a cache eviction/mismatch from becoming an implicit allow."""

    def test_missing_stateful_response_transaction_is_fail_closed(self) -> None:
        response = SOURCE.split(
            "static void process_production_response_notify", 1
        )[1].split("static void build_modsecurity_request_from_notify", 1)[0]

        self.assertIn("transaction = transaction_cache_take(state, request->request_id)", response)
        self.assertIn(
            "set_missing_response_transaction_failure(decision, phase)", response
        )
        self.assertIn('"stateful response transaction missing"', SOURCE)
        self.assertIn('"stateful_response_transaction_missing_closed"', SOURCE)
        self.assertIn('"deny", 503', SOURCE)
        self.assertIn('return "fail-closed";', SOURCE)
        self.assertNotIn('"pass", 200, "transaction_resumed=false"', response)

    def test_response_processing_remains_bound_to_a_live_cache_entry(self) -> None:
        response = SOURCE.split(
            "static void process_production_response_notify", 1
        )[1].split("static void build_modsecurity_request_from_notify", 1)[0]

        # Legitimate controls must still process response headers/body and
        # finish or re-store the same transaction after successful processing.
        self.assertIn(
            "haproxy_modsecurity_transaction_process_response_headers(", response
        )
        self.assertIn(
            "haproxy_modsecurity_transaction_process_response_body(", response
        )
        self.assertIn("transaction_cache_store(state, request->request_id, transaction)", response)
        self.assertIn("haproxy_modsecurity_transaction_finish(transaction)", response)


if __name__ == "__main__":
    unittest.main()
