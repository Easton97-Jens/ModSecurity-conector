"""The duplication guard must not treat missing or rounded evidence as zero."""
from decimal import Decimal
from pathlib import Path
import runpy
import unittest

MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / "ci/checks/common/check-sonar-duplication.py"))


class SonarDuplicationGateTests(unittest.TestCase):
    def test_summary_requires_explicit_single_density(self):
        parse = MODULE["summary_density"]
        self.assertEqual(parse("[0.0% Duplication on New Code](example)"), Decimal("0"))
        self.assertEqual(parse("[0.1% Duplication on New Code](example)"), Decimal("0.1"))
        for value in ("", "0% Coverage on New Code", "0.0% Duplication on New Code 1% Duplication on New Code"):
            with self.subTest(value=value), self.assertRaises(MODULE["GateError"]):
                parse(value)

    def test_all_three_exact_measures_are_required(self):
        entries = [{"metric": key, "period": {"value": "0"}} for key in MODULE["METRICS"]]
        self.assertEqual(set(MODULE["metric_values"]({"measures": entries})), set(MODULE["METRICS"]))
        for measures in (entries[:-1], entries + entries[:1], []):
            with self.subTest(measures=measures), self.assertRaises(MODULE["GateError"]):
                MODULE["metric_values"]({"measures": measures})

    def test_nonfinite_negative_and_nonstring_metrics_are_rejected(self):
        for invalid in ("NaN", "Infinity", "-1", 0, None):
            measures = [{"metric": key, "period": {"value": "0"}} for key in MODULE["METRICS"]]
            measures[0]["period"]["value"] = invalid
            with self.subTest(invalid=invalid), self.assertRaises(MODULE["GateError"]):
                MODULE["metric_values"]({"measures": measures})

    def test_positive_line_count_survives_rounded_zero_density(self):
        measures = [{"metric": key, "period": {"value": "0"}} for key in MODULE["METRICS"]]
        measures[0]["period"]["value"] = "1"
        result = MODULE["metric_values"]({"measures": measures})
        self.assertNotEqual(result["new_duplicated_lines"], 0)
        self.assertEqual(result["new_duplicated_lines_density"], 0)

    def test_invalid_endpoint_is_rejected_before_network(self):
        with self.assertRaises(MODULE["GateError"]):
            MODULE["sonar_get"]("https://untrusted.invalid", {})


if __name__ == "__main__":
    unittest.main()
