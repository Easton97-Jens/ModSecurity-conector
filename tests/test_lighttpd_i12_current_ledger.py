"""Synthetic execution-index controls; these never qualify a real host case."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "current_lighttpd_ledger_test", ROOT / "ci/runtime/lifecycle/i12/lighttpd/current_ledger.py")
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)


class CurrentLedgerCoverageTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="lighttpd-current-ledger-control-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.identity = "I12::lighttpd-stock-sidecar::allow_without_marker"
        self.capture = self.root / "capture.json"
        self.capture.write_text('{"synthetic_capture": true}')
        self.process = self.root / "process.json"
        self.process.write_text('{"synthetic_process": true, "actual_returncode": 0}')
        self.row = {
            "run_scoped_case_id": self.identity,
            "original_row_sha256": C.Q.original_row(self.identity)["original_row_sha256"],
            "status": "PARTIAL_HOST_MEASUREMENTS", "execution_kind": "host_http",
            "execution_observed": True, "remaining_reason": "Synthetic coverage only; Root qualification is missing.",
            "capture_refs": [C.Q.reference(self.capture)],
            "process_producers": [C.Q.reference(self.process, "client_process")],
        }
        self.index = {"schema": "lighttpd-i12-execution-index-v1", "reviewed_by": "root",
                      "independent_review": "Synthetic negative controls, never host proof.", "rows": [self.row]}
        self.path = self.root / "index.json"

    def save(self):
        self.path.write_text(json.dumps(self.index))
        return self.path

    def test_capture_is_executed_but_cannot_become_pass_or_resolve_oracle(self):
        result = C.export([], {"synthetic": True}, self.root / "output", self.save())
        summary = result["lighttpd-stock-sidecar"]
        self.assertEqual(summary["current_executed_original_ids"], 1)
        self.assertEqual(summary["current_unique_http_executions"], 1)
        self.assertEqual(summary["newly_qualified_original_ids"], 0)
        self.assertEqual(summary["newly_resolved_original_oracles"], 0)
        self.assertEqual(summary["current_qualified_verdicts"], {})
        self.assertEqual(summary["current_verdicts"], {"PARTIAL_HOST_MEASUREMENTS": 1})

    def test_worker_pass_unknown_review_and_missing_process_cannot_promote(self):
        original = copy.deepcopy(self.index)
        for mutation in ("PASS", "review", "process", "boolean"):
            self.index = copy.deepcopy(original)
            if mutation == "PASS":
                self.index["rows"][0]["status"] = "PASS"
            elif mutation == "review":
                self.index["reviewed_by"] = "worker"
            elif mutation == "process":
                self.index["rows"][0]["process_producers"] = []
            else:
                self.index["rows"][0]["execution_observed"] = 1
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                C.execution_inventory(self.save())

    def test_wrong_original_duplicate_corruption_and_foreign_role_are_rejected(self):
        self.row["original_row_sha256"] = "changed"
        with self.assertRaisesRegex(ValueError, "original ID"):
            C.execution_inventory(self.save())
        self.row["original_row_sha256"] = C.Q.original_row(self.identity)["original_row_sha256"]
        self.index["rows"].append(copy.deepcopy(self.row))
        with self.assertRaisesRegex(ValueError, "original ID"):
            C.execution_inventory(self.save())
        self.index["rows"].pop()
        self.row["process_producers"][0]["role"] = "native_api"
        with self.assertRaisesRegex(ValueError, "independent process"):
            C.execution_inventory(self.save())
        self.row["process_producers"][0]["role"] = "client_process"
        self.capture.write_text("altered")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            C.execution_inventory(self.save())

    def test_copied_receipt_and_reused_request_do_not_inflate_executions(self):
        other = copy.deepcopy(self.row)
        other["run_scoped_case_id"] = "I12::lighttpd-stock-sidecar::deny_header_marker_403"
        other["original_row_sha256"] = C.Q.original_row(other["run_scoped_case_id"])["original_row_sha256"]
        copied = self.root / "copy.json"
        copied.write_bytes(self.process.read_bytes())
        other["process_producers"] = [C.Q.reference(copied, "client_process")]
        self.index["rows"].append(other)
        result = C.export([], {}, self.root / "output", self.save())["lighttpd-stock-sidecar"]
        self.assertEqual(result["current_executed_original_ids"], 2)
        self.assertEqual(result["current_unique_http_executions"], 1)

    def test_host_start_only_is_not_http_and_blocker_requires_source_evidence(self):
        self.row.update(status="HOST_START_ONLY", execution_observed=False,
                        execution_kind="host_start", process_producers=[])
        result = C.export([], {}, self.root / "output", self.save())["lighttpd-stock-sidecar"]
        self.assertEqual(result["current_executed_original_ids"], 0)
        self.assertEqual(result["current_unique_http_executions"], 0)
        self.row.update(status="ENVIRONMENT_BLOCKED", capture_refs=[])
        with self.assertRaisesRegex(ValueError, "concrete evidence"):
            C.execution_inventory(self.save())

    def test_unsupported_needs_existing_per_id_root_oracle_review(self):
        self.row.update(status="UNSUPPORTED_CAPABILITY", execution_observed=False,
                        execution_kind="host_start", process_producers=[])
        with self.assertRaisesRegex(ValueError, "oracle reconciliation"):
            C.execution_inventory(self.save())
        record = self.root / "oracle.json"
        for owner, identity in (("worker", self.identity), ("root", "another-original")):
            record.write_text(json.dumps({"reviewed_by": owner, "run_scoped_case_id": identity}))
            self.row["oracle_record"] = C.Q.reference(record)
            with self.subTest(owner=owner), self.assertRaisesRegex(ValueError, "exact original ID"):
                C.execution_inventory(self.save())

    def test_diagnostic_http_pass_does_not_claim_required_body_lifecycle(self):
        qualifier = {"full_lifecycle_qualified": True, "execution_observed": True,
                     "unknown_fields": []}
        result = {"qualifier": qualifier, "status": "PASS",
                  "oracle_review": {"resolved": True, "effective_oracle": {}}}
        packet = {"execution_kind": "host_http", "run_id": "synthetic-control",
                  "parent_sha": "synthetic", "effective_config_sha256": "synthetic"}
        row = {"required_leg": False}
        actual = C.qualified_result(result, packet, [], row, {})
        self.assertTrue(actual["full_case_qualified"])
        self.assertTrue(actual["diagnostic_host_qualified"])
        self.assertFalse(actual["full_lifecycle_qualified"])
        row["required_leg"] = True
        required = C.qualified_result(result, packet, [], row, {})
        self.assertTrue(required["full_lifecycle_qualified"])
        self.assertFalse(required["diagnostic_host_qualified"])


if __name__ == "__main__":
    unittest.main()
