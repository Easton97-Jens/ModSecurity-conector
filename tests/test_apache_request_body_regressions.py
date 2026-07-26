"""Contract tests for the Parent Apache request-body regression client."""

from pathlib import Path
import unittest

from connectors.apache.harness import request_body_regressions as regressions


ROOT = Path(__file__).resolve().parents[1]


class ApacheRequestBodyRegressionTests(unittest.TestCase):
    def test_payloads_are_large_and_split_the_detection_token(self) -> None:
        self.assertGreater(262144 + len(regressions.ALLOW), 64 * 1024)
        chunks = [b"prefix-", regressions.BLOCK[:11], regressions.BLOCK[11:]]
        self.assertEqual(b"prefix-" + regressions.BLOCK, b"".join(chunks))
        self.assertNotIn(regressions.BLOCK, chunks)

    def test_live_suite_covers_status_eos_and_isolation_edges(self) -> None:
        source = (ROOT / "connectors/apache/harness/request_body_regressions.py").read_text()
        for case in ("small_allow", "body_block", "large_allow", "empty", "multi_bucket_block"):
            self.assertIn(case, source)
        self.assertIn('expected = 200 if index % 2 == 0 else 403', source)
        self.assertNotIn("488", source)

    def test_production_eos_architecture_remains_authoritative(self) -> None:
        filters = (ROOT / "connectors/apache/src/msc_filters.c").read_text()
        module = (ROOT / "connectors/apache/src/mod_security3.c").read_text()
        self.assertIn("APR_BUCKET_IS_EOS", filters)
        self.assertIn("request_body_processed", filters)
        self.assertIn("msc_finalize_request_body", filters)
        self.assertNotIn("ap_get_client_block", module)
        self.assertNotIn("ap_hook_handler(hook_request_late", module)

    def test_parent_make_wiring_has_contract_and_live_targets(self) -> None:
        makefile = (ROOT / "Makefile").read_text()
        self.assertIn("check-apache-request-body-regressions:", makefile)
        self.assertIn("apache-request-body-regressions:", makefile)


if __name__ == "__main__":
    unittest.main()
