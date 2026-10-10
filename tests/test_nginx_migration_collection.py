"""Strict projection of regular removed-API fixture metadata, not runtime proof."""
from tests.test_nginx_configtest_collection import collector
import unittest


class MigrationCollectionTest(unittest.TestCase):
    def test_regular_fixture_digest_survives_only_for_two_closed_cases(self):
        for case_id, leaf in (("phase4_invalid_scope_file", "invalid-content-type-scope.txt"),
                              ("phase4_wildcard_scope_rejected", "wildcard-content-type-scope.txt")):
            receipt = {"operation": "configtest", "case_id": case_id, "fixture_leaf": leaf,
                       "fixture_state": "regular", "fixture_sha256": "1" * 64}
            row = {"case_id": case_id, "configtest_receipt": receipt}
            self.assertEqual(collector.configtest_source_fields(row, 0)["configtest_receipt"], receipt)
            for unrelated in ("invalid_status", "missing_rules_file", "unsafe_event_path"):
                with self.subTest(unrelated=unrelated), self.assertRaises(ValueError):
                    collector.configtest_source_fields({**row, "case_id": unrelated}, 0)


if __name__ == "__main__":
    unittest.main()
