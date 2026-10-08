"""Pure E-adapter controls; no native host or listener is started."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EventDriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("event_driver", ROOT / "ci/runtime/lifecycle/run-nginx-event-boundary-cases.py")
        cls.driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.driver)

    def test_two_separate_fixed_boundary_variants_and_no_invented_directive(self):
        self.assertEqual(self.driver.variants_for("event_json_limit"), ("at255", "over256"))
        self.assertEqual(self.driver.variants_for("event_metadata_truncation"), ("long-query",))
        text = self.driver.configuration(Path("/var/tmp/codex/owned"), 123, 124, "projection",
                                         "/no-crs/events/long-query/xxx?probe=non-sensitive", "safe", "unit-long-query")
        self.assertIn('modsecurity_transaction_id "unit-long-query-$connection-$connection_requests";', text)
        self.assertIn('modsecurity_phase4_log "/var/tmp/codex/owned/phase4-events.jsonl";', text)
        self.assertNotIn("event_json_limit", text)
        self.assertIn("location /no-crs/events/", text)

    def test_unknown_or_injected_inputs_rejected(self):
        with self.assertRaises(ValueError):
            self.driver.variants_for("foreign")
        for path, mode, run in (("/foreign", "safe", "unit"),
                                ("/no-crs/events/at255/xxx", "off", "unit"),
                                ("/no-crs/events/at255/xxx", "safe", 'unit";bad')):
            with self.assertRaises(ValueError):
                self.driver.configuration(Path("/var/tmp/codex/owned"), 123, 124, "projection", path, mode, run)

    def test_only_actual_phase1_rule_callback_is_selected(self):
        row = b'{"event":"request_rule_match","connector":"nginx","phase":"request_headers","integration_mode":"native-nginx-http-module","method":"GET","rule_id":"1100402","action":"pass"}\n'
        self.assertEqual(len(self.driver.native_callbacks(row, "/actual")), 1)
        self.assertEqual(self.driver.native_callbacks(row.replace(b"1100402", b"1100401"), "/actual"), [])
        with self.assertRaises(ValueError):
            self.driver.native_callbacks(b"[]\n", "/actual")


if __name__ == "__main__":
    unittest.main()
