"""Contract guards for actual native observation selection and configuration."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest import mock
from types import SimpleNamespace

PATH = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/run-nginx-phase4-cases.py"
SPEC = importlib.util.spec_from_file_location("phase4_driver", PATH)
driver = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(driver)


class NativePhase4DriverTest(unittest.TestCase):
    def test_closed_phase4_entry_delegates_without_changing_spec_or_input_identity(self):
        args = SimpleNamespace(framework_root="/trusted-framework", case_id="phase4_body_at_limit")
        spec = {"source_record_id": args.case_id, "operation": "native_phase4_request"}
        inputs = SimpleNamespace(operation=mock.Mock(return_value=spec))
        with mock.patch.object(driver.HOST.BASE, "absolute_path", side_effect=Path), \
                mock.patch.object(driver, "load", return_value=inputs) as loader, \
                mock.patch.object(driver, "run_operation", return_value=True) as runtime:
            self.assertTrue(driver.run(args))
        path = Path("/trusted-framework/tests/runners/nginx_phase4_contracts.py")
        loader.assert_called_once_with("phase4_closed_inputs", path)
        inputs.operation.assert_called_once_with(args.case_id)
        runtime.assert_called_once_with(args, spec, input_path=path)

    def test_shared_operation_requires_explicit_spec_source_and_preserves_native_defaults(self):
        import inspect
        signature = inspect.signature(driver.run_operation)
        self.assertIs(signature.parameters["input_path"].default, inspect.Parameter.empty)
        self.assertIs(signature.parameters["upstream_factory"].default, driver.BoundedPhase4Upstream)
        self.assertIs(signature.parameters["configuration_factory"].default, driver.configuration)
        self.assertEqual(signature.parameters["upstream_path"].default,
                         PATH.parent.parent / "common/nginx_phase4_upstream.py")

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
