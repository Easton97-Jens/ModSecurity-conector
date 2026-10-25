"""The duplication guard must not treat missing or rounded evidence as zero."""
from decimal import Decimal
from contextlib import redirect_stdout
import io
from pathlib import Path
import runpy
import unittest
from tests.test_sonar_zero_gate import Evidence, HEAD, REPOSITORY, PR

MODULE = runpy.run_path(str(Path(__file__).resolve().parents[1] / "ci/checks/common/check-sonar-duplication.py"))


class SonarDuplicationGateTests(unittest.TestCase):
    def test_absent_summary_density_requires_all_structured_metrics(self):
        evidence = Evidence()
        with redirect_stdout(io.StringIO()):
            result = MODULE['verify_duplication'](REPOSITORY, HEAD, PR, evidence.fetch, evidence.sonar)
        for metric in MODULE['METRICS']:
            self.assertEqual(result[metric], '0')

    def test_each_nonzero_duplication_metric_fails_despite_rounded_summary(self):
        for metric in MODULE['METRICS']:
            with self.subTest(metric=metric):
                evidence = Evidence()
                evidence.set_measure(metric, '1')
                evidence.checks[0]['output']['summary'] = '0.0% Duplication on New Code'
                with redirect_stdout(io.StringIO()), self.assertRaises(MODULE['GateError']):
                    MODULE['verify_duplication'](REPOSITORY, HEAD, PR, evidence.fetch, evidence.sonar)

    def test_all_three_exact_measures_are_required(self):
        entries = [{"metric": key, "period": {"value": "0"}} for key in MODULE["METRICS"]]
        self.assertEqual(set(MODULE["metric_values"]({"measures": entries})), set(MODULE["METRICS"]))
        for measures in (entries[:-1], entries + entries[:1], []):
            with self.subTest(measures=measures), self.assertRaises(MODULE["GateError"]):
                MODULE["metric_values"]({"measures": measures})

    def test_nonfinite_negative_and_nonstring_metrics_are_rejected(self):
        for invalid in ("NaN", "Infinity", "-1", 0, None, "١"):
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

    def test_single_legacy_period_preserves_exact_count(self):
        measures = [{"metric": key, "periods": [{"index": 1, "value": "0"}]} for key in MODULE["METRICS"]]
        measures[0]["periods"][0]["value"] = "7"
        self.assertEqual(MODULE["metric_values"]({"measures": measures})["new_duplicated_lines"], Decimal(7))

    def test_ambiguous_period_shapes_and_missing_values_fail(self):
        values = ({"periods": []}, {"periods": [{"value": "0"}, {"value": "1"}]},
                  {"period": {"value": "0"}, "value": "0"}, {"periods": [{}]})
        for measure in values:
            with self.subTest(measure=measure), self.assertRaises(MODULE["GateError"]):
                MODULE["measure_value"](measure)



# Parent default discovery uses the one admitted active-case inventory.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)

if __name__ == "__main__":
    unittest.main()
