"""Regression contract for Apache's connection-phase failure gates."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"


def function_region(source: str, marker: str) -> str:
    start = source.index(marker)
    end = source.find("\nstatic ", start + len(marker))
    return source[start:] if end < 0 else source[start:end]


class ApacheConnectionPhaseContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = MODULE.read_text(encoding="utf-8")
        self.early = function_region(
            self.source, "static int hook_request_early(request_rec *r) {"
        )
        self.late = function_region(
            self.source, "static int hook_request_late(request_rec *r)\n{"
        )

    def test_both_connection_branches_require_exact_success(self) -> None:
        self.assertEqual(self.source.count("msc_process_connection(msr->t,"), 2)
        for branch in (self.early, self.late):
            call = branch.index("msc_process_connection(msr->t,")
            gate = branch.index(") != 1)", call)
            intervention = branch.index("it = process_intervention(msr->t, r);")
            self.assertLess(call, gate)
            self.assertLess(gate, intervention)
            self.assertIn("return apache_fail_closed", branch[gate:intervention])

    def test_failure_gate_logs_and_precedes_normal_request_processing(self) -> None:
        fail_closed = function_region(self.source, "static int apache_fail_closed(")
        self.assertIn("libmodsecurity operation failed", fail_closed)
        self.assertIn("HTTP_INTERNAL_SERVER_ERROR", fail_closed)
        for branch in (self.early, self.late):
            gate = branch.index(") != 1)")
            intervention = branch.index("it = process_intervention(msr->t, r);")
            failure_path = branch[gate:intervention]
            self.assertIn("apache_fail_closed", failure_path)
            self.assertIn("return apache_fail_closed", failure_path)


if __name__ == "__main__":
    unittest.main()
