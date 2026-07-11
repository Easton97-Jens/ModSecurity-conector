from __future__ import annotations

from pathlib import Path
import os
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONSUMER = ROOT / "ci" / "consume-no-crs-selected-cases.sh"


class NoCrsSelectedRunnerWiringTest(unittest.TestCase):
    def consume(self, connector: str, selected_cases: str) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["NO_CRS_SELECTED_CASES"] = selected_cases
        return subprocess.run(
            [str(CONSUMER), connector],
            cwd=ROOT,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def test_consumer_requires_the_capability_selected_core_cases(self) -> None:
        result = self.consume("envoy", "allow_without_marker.yaml")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("deny_header_marker_403.yaml", result.stderr)

    def test_consumer_receipt_does_not_claim_unrun_selected_cases_passed(self) -> None:
        result = self.consume(
            "traefik",
            " ".join(
                (
                    "allow_without_marker.yaml",
                    "deny_header_marker_403.yaml",
                    "deny_with_alternative_status.yaml",
                    "transaction_id_present.yaml",
                    "log_only.yaml",
                )
            ),
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("selected=", result.stdout)
        self.assertIn("unrun_selected_runner_cases=deny_with_alternative_status.yaml", result.stdout)
        self.assertNotIn("PASS", result.stdout)

    def test_remaining_connectors_use_distinct_plan_consuming_targets(self) -> None:
        stage = (ROOT / "ci" / "run-connector-stage.sh").read_text(encoding="utf-8")
        self.assertIn(
            "envoy:no_crs_baseline|traefik:no_crs_baseline|lighttpd:no_crs_baseline)",
            stage,
        )
        self.assertIn('run_remaining_connector "no-crs-baseline-$connector"', stage)
        self.assertIn("capability-selected No-CRS runner cases are missing", stage)

        target_runner = (ROOT / "ci" / "run-remaining-connector-target.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("no-crs-baseline-*", target_runner)

    def test_each_connector_baseline_target_enables_the_selection_consumer(self) -> None:
        contracts = {
            "envoy": (
                ROOT / "connectors/envoy/Makefile",
                ROOT / "connectors/envoy/harness/run_envoy_connector_runtime.sh",
                "no-crs-baseline-envoy",
            ),
            "traefik": (
                ROOT / "connectors/traefik/Makefile",
                ROOT / "connectors/traefik/scripts/runtime_smoke.py",
                "no-crs-baseline-traefik",
            ),
            "lighttpd": (
                ROOT / "connectors/lighttpd/Makefile",
                ROOT / "connectors/lighttpd/harness/runtime_lighttpd_smoke.sh",
                "no-crs-baseline-lighttpd",
            ),
        }
        for connector, (makefile, harness, target) in contracts.items():
            with self.subTest(connector=connector):
                make_text = makefile.read_text(encoding="utf-8")
                harness_text = harness.read_text(encoding="utf-8")
                self.assertIn(f"{target}: export MSCONNECTOR_NO_CRS_BASELINE := 1", make_text)
                self.assertIn("consume-no-crs-selected-cases.sh", harness_text)


if __name__ == "__main__":
    unittest.main()
