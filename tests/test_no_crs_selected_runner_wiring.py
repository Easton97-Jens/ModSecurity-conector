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

    def test_remaining_connectors_keep_compatibility_and_native_targets_distinct(self) -> None:
        stage = (ROOT / "ci" / "run-connector-stage.sh").read_text(encoding="utf-8")
        for connector, native_target, compatibility_target in (
            ("envoy", "runtime-smoke-envoy-ext-proc", "no-crs-baseline-envoy"),
            ("traefik", "runtime-smoke-traefik-native", "no-crs-baseline-traefik"),
            ("lighttpd", "runtime-smoke-lighttpd-patched", "no-crs-baseline-lighttpd"),
        ):
            with self.subTest(connector=connector):
                self.assertIn(f"{connector}:no_crs_baseline)", stage)
                self.assertIn(f"run_remaining_connector {native_target}", stage)
                self.assertIn(f"run_remaining_connector {compatibility_target}", stage)
        self.assertIn("run_full_lifecycle_haproxy_htx", stage)
        self.assertIn("runtime-smoke-haproxy-htx", stage)
        self.assertNotIn("compatibility SPOE/SPOP runner is forbidden", stage)
        self.assertIn("capability-selected No-CRS runner cases are missing", stage)

        target_runner = (ROOT / "ci" / "run-remaining-connector-target.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("no-crs-baseline-*", target_runner)
        self.assertIn("EXT_PROC_RUNTIME_ROOT", target_runner)
        self.assertIn("TRAEFIK_NATIVE_RUNTIME_ROOT", target_runner)
        self.assertIn("LIGHTTPD_PATCHED_SMOKE_DIR", target_runner)

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

    def test_apache_maps_selected_late_phase4_cases_to_real_host_fixtures(self) -> None:
        harness = (
            ROOT / "connectors/apache/harness/run_apache_smoke.sh"
        ).read_text(encoding="utf-8")
        self.assertIn("append_selected_phase4_fixtures", harness)
        self.assertIn("phase4_deny_after_commit_log_only", harness)
        self.assertIn("apache_phase4_deny_after_commit_log_only", harness)
        self.assertIn("phase4_deny_after_commit_abort", harness)
        self.assertIn("apache_phase4_deny_after_commit_abort", harness)
        for fixture in (
            "apache_phase4_deny_after_commit_log_only.yaml",
            "apache_phase4_deny_after_commit_abort.yaml",
        ):
            with self.subTest(fixture=fixture):
                self.assertTrue(
                    (
                        ROOT
                        / "modules/ModSecurity-test-Framework/tests/cases/connector-specific/apache"
                        / fixture
                    ).is_file()
                )

    def test_lighttpd_runner_uses_the_checkout_root_and_haproxy_preserves_status(self) -> None:
        lighttpd_harness = (
            ROOT / "connectors/lighttpd/harness/runtime_lighttpd_smoke.sh"
        ).read_text(encoding="utf-8")
        self.assertIn('cd "$SCRIPT_DIR/../../.."', lighttpd_harness)

        haproxy_harness = (
            ROOT / "connectors/haproxy/harness/run_haproxy_smoke.sh"
        ).read_text(encoding="utf-8")
        for scope in ("http-request", "http-response"):
            status_429 = haproxy_harness.index(
                f"{scope} deny status 429 if {{ var(txn.modsec.status) -m int 429 }}"
            )
            fallback_403 = haproxy_harness.index(
                f"{scope} deny status 403 if {{ var(txn.modsec.blocked) -m bool }}"
            )
            self.assertLess(status_429, fallback_403)


if __name__ == "__main__":
    unittest.main()
