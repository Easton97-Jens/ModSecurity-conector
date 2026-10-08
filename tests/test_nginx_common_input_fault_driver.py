"""Driver shape controls do not prove a real native injected operation."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InputFaultDriverTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("input_fault_driver", ROOT / "ci/runtime/lifecycle/run-nginx-common-input-fault.py")
        cls.driver = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.driver)

    def test_config_binds_true_transaction_and_actual_native_sink(self):
        text = self.driver.fault_config(Path("/var/tmp/codex/owned"), 32123, "/var/tmp/codex/projection/child", "a" * 32)
        self.assertIn('modsecurity_transaction_id "' + "a" * 32 + '";', text)
        self.assertIn('"transaction_id":"' + "a" * 32 + '"', text)
        self.assertIn('user nobody nogroup;', text)
        self.assertIn('modsecurity_phase4_log "/var/tmp/codex/owned/phase1-events.jsonl";', text)
        self.assertIn('access_log "/var/tmp/codex/owned/native-access.jsonl" input_fault;', text)

    def test_mismatch_never_equals_true_transaction(self):
        for transaction in ("a" * 32, "0" * 32, "1" * 32):
            actual = self.driver.mismatch_transaction(transaction)
            self.assertNotEqual(actual, transaction)
            self.assertRegex(actual, r"^[0-9a-f]{32}$")
