"""Closed sequence configuration and native-fixture authority tests."""
import argparse
import importlib.util
from pathlib import Path
import sys
import unittest
from unittest import mock

DIRECTORY = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle"
sys.path.insert(0, str(DIRECTORY))
SPEC = importlib.util.spec_from_file_location("nginx_sequence_driver", DIRECTORY / "run-nginx-lifecycle-sequences.py")
DRIVER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DRIVER)


class DriverTests(unittest.TestCase):
    def test_finish_fault_identity_does_not_capture_listener_probes(self):
        identity = "a" * 32
        config = DRIVER.sequence_config(Path("/var/tmp/codex/sequence"), 19000,
                                        Path("/var/tmp/codex/projection/child"),
                                        "finish_failure_propagation", fault_transaction=identity)
        self.assertIn(b"default $request_id;", config)
        self.assertIn(b'/no-crs/sequence/' + b'a' * 24 + b'/0', config)
        self.assertIn(b"modsecurity_transaction_id \"$sequence_transaction_id\";", config)

    def test_fault_controls_cannot_change_an_unrelated_sequence(self):
        args = argparse.Namespace(case_id="keepalive_allow_allow", fault_negative_control=True)
        with mock.patch.object(DRIVER.BASE, "validate_inputs", return_value=(Path("/binary"), Path("/module"), Path("/output"))):
            with self.assertRaisesRegex(ValueError, "exact native fixture case"):
                DRIVER.run(args)

    def test_late_modes_and_fault_identity_are_closed_configuration(self):
        output = Path("/var/tmp/codex/ModSecurity-conector/sequence")
        safe = DRIVER.sequence_config(output, 19000, Path("/var/tmp/codex/projection/child"),
                                      "keepalive_safe_followup", upstream_port=19001)
        strict = DRIVER.sequence_config(output, 19000, Path("/var/tmp/codex/projection/child"),
                                        "phase4_strict_http1_client_abort", upstream_port=19001)
        self.assertIn(b"modsecurity_phase4_mode safe;", safe)
        self.assertIn(b"modsecurity_phase4_mode strict;", strict)
        self.assertIn(b"proxy_buffering off;", strict)
        self.assertIn(b"connection_requests", strict)
        self.assertIn(b"$request_id", strict)


if __name__ == "__main__":
    unittest.main()
