"""Driver shape controls do not prove a real native injected operation."""
import importlib.util
import copy
import json
import os
from pathlib import Path
import unittest
import tempfile

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

    def test_source_bound_protocol_selection_retains_cleanup_and_raw(self):
        helper_path = Path(os.environ.get("FRAMEWORK_ROOT", ROOT / "modules/ModSecurity-test-Framework")) / "tests/runners/nginx_common_input_faults.py"
        if not helper_path.is_file():
            self.skipTest("strict pure Framework helper requires explicit FRAMEWORK_ROOT")
        spec = importlib.util.spec_from_file_location("pointer_strict_helper", helper_path)
        helper = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
        transaction = "a" * 32
        path = "/no-crs/input-fault/header_count_nonzero_with_null_headers"
        event = dict(event="protocol_error", message_id="MSCONN_EVENT_PROTOCOL_ERROR", connector="nginx",
                     integration_mode="native-nginx-http-module", transaction_id=transaction,
                     phase="request_headers", method="POST", uri=path, status="error",
                     reason="protocol_error", rule_id="")
        cleanup = dict(event, event="transaction_cleanup", phase="logging", message_id="MSCONN_TRANSACTION_CLEANUP")
        rows = [event, cleanup]
        retained = copy.deepcopy(rows)
        selected = self.driver.select_protocol_events(rows, transaction, path)
        self.assertEqual(selected, [event])
        self.assertEqual(helper.native_event_errors(selected, transaction), [])
        self.assertEqual(rows, retained)
        with tempfile.TemporaryDirectory(prefix="pointer-selection-", dir="/var/tmp/codex/ModSecurity-conector") as temporary:
            output = Path(temporary)
            leaf = output / "phase1-events.jsonl"
            raw = b"".join((json.dumps(row) + "\n").encode() for row in rows)
            leaf.write_bytes(raw)
            before = self.driver.BASE.digest(self.driver.STARTUP.bounded_capture(leaf))
            self.assertEqual(self.driver.select_protocol_events(self.driver.read_rows(output, leaf.name), transaction, path), [event])
            self.assertEqual(leaf.read_bytes(), raw)
            self.assertEqual(self.driver.BASE.digest(self.driver.STARTUP.bounded_capture(leaf)), before)
        for field, wrong in (("transaction_id", "b" * 32), ("phase", "response_body"),
                             ("uri", path + "-wrong"), ("method", "GET"),
                             ("connector", "apache"), ("integration_mode", "synthetic")):
            with self.subTest(field=field):
                selected = self.driver.select_protocol_events([dict(event, **{field: wrong}), cleanup], transaction, path)
                self.assertTrue(helper.native_event_errors(selected, transaction))
        selected = self.driver.select_protocol_events([event, event, cleanup], transaction, path)
        self.assertTrue(helper.native_event_errors(selected, transaction))
