"""Contract guards for actual native observation selection and configuration."""
import importlib.util
import json
from pathlib import Path
import unittest

PATH = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/run-nginx-phase4-cases.py"
SPEC = importlib.util.spec_from_file_location("phase4_driver", PATH)
driver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(driver)


class NativePhase4DriverTest(unittest.TestCase):
    def test_foreign_case_phase_or_connector_cannot_be_native_observation(self):
        actual = {"connector": "nginx", "integration_mode": "native-nginx-http-module",
                  "phase": "response_body", "method": "GET", "uri": "/exact"}
        values = [actual, dict(actual, uri="/other"), dict(actual, phase="request_headers"),
                  dict(actual, connector="apache"), dict(actual, method="POST"),
                  dict(actual, integration_mode="synthetic_harness")]
        raw = b"\n".join(json.dumps(value).encode() for value in values)
        self.assertEqual(driver.native_observations(raw, "/exact"), [actual])
        self.assertNotIn("status", driver.native_observations(raw, "/exact")[0])

    def test_existing_mode_only_and_buffering_not_enabled(self):
        for mode in ("off", "safe"):
            config = driver.configuration(Path("/owned"), 18081, 18082, Path("/projection"), "/exact", mode, "owned-case-run")
            self.assertIn("modsecurity_phase4_mode " + mode + ";", config)
            self.assertIn("proxy_buffering off;", config)
            self.assertIn("user nobody nogroup;", config)
            self.assertIn('modsecurity_transaction_id "owned-case-run-$connection-$connection_requests";', config)
        for mode in ("minimal", "unknown", "safe; off"):
            with self.assertRaises(ValueError):
                driver.configuration(Path("/owned"), 18081, 18082, Path("/projection"), "/exact", mode, "owned-case-run")


if __name__ == "__main__":
    unittest.main()
