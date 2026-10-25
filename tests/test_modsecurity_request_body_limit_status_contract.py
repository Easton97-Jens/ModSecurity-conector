"""Exact native limit classification preserves the actual engine status."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class NativeRequestLimitStatusContractTest(unittest.TestCase):
    def test_exact_signature_preserves_403_and_413(self):
        source = (ROOT / "common/src/intervention.c").read_text()
        runtime = (ROOT / "common/runtime/msconnector_runtime.c").read_text()
        for condition in ("phase == MSCONNECTOR_PHASE_REQUEST_BODY", "intervention->disruptive != 0", "intervention->status == 403", "intervention->status == 413", "intervention->redirect_url == 0", "intervention->log_message != 0", "MSCONNECTOR_REQUEST_BODY_LIMIT_REJECTION_LOG"):
            self.assertIn(condition, source)
        self.assertNotIn("strstr(", source)
        self.assertNotIn("native_intervention_status(", runtime)
        self.assertIn("msconnector_decision_set_body_limit(decision, intervention.status, native->reason)", runtime)
        self.assertIn("return transaction->native_body_limit_status;", runtime)
        self.assertIn("visible_http_status != decision->http_status", runtime)
    def test_append_rejection_survives_native_eos_reset(self):
        runtime = (ROOT / "common/runtime/msconnector_runtime.c").read_text()
        self.assertIn("pending_request_decision", runtime)
        self.assertIn("msc_process_request_body(native->transaction)", runtime)

# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__": unittest.main()
