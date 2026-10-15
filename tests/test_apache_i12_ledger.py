"""Mutation negatives for the Apache-only adapter using real physical files."""

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


PATH = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/apache-i12/ledger.py"
SPEC = importlib.util.spec_from_file_location("apache_i12_ledger", PATH)
LEDGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LEDGER)


class ApacheLedgerTest(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ.get("CODEX_TEST_TMP_ROOT") or os.environ.get("RUNNER_TEMP") or
                    "/var/tmp/codex/ModSecurity-conector/runs/i12-apache-410-20261015/ledger-tests")
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        oracle = {"native_result": "allow", "visible_status": 200, "phase": 4,
                  "physical_evidence_not_projection": True, "unresolved_expected_value_reason": None}
        rows = []
        for index in range(1484):
            leg = "apache-native" if index < 155 else "fixture-other-profile"
            identity = f"I12::{leg}::fixture-{index}"
            rows.append({"run_scoped_case_id": identity, "leg_id": leg, "required_leg": True,
                         "selected_requirement": {"run_scoped_case_id": identity, "expected_oracle": oracle},
                         "status": "PASS" if index < 10 else "NOT_EXECUTED_UNQUALIFIED",
                         "execution_observed": index < 25,
                         "qualification_scope": "historical_configuration_only" if index < 9 else
                         "full_host_lifecycle" if index == 9 else None,
                         "oracle_reconciliation": None})
        self.baseline = {"rows": rows}
        ids = [row["run_scoped_case_id"] for row in rows]
        # Only immutable catalog digests are replaced for this synthetic catalog;
        # every physical packet/oracle/measurement validator remains real.
        self.digest_patch = patch.multiple(LEDGER.ORACLES,
            ID_SHA256=hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest(),
            CONTRACT_SHA256=LEDGER.ORACLES.canonical_digest([row["selected_requirement"] for row in rows]))
        self.digest_patch.start()
        self.addCleanup(self.digest_patch.stop)
        self.packet = {
            "reviewed_by": "root", "run_scoped_case_id": ids[0], "leg_id": "apache-native",
            "execution_observed": True, "execution_kind": "host_http", "run_id": "fresh-run",
            "parent_sha": "parent-source", "framework_sha": "framework-source", "mrts_sha": "mrts-source",
            "effective_config_sha256": "config", "oracle_evaluated": True,
            "oracle_sha256": LEDGER.ORACLES.canonical_digest(oracle), "outcome": "PASS",
            "full_lifecycle_qualified": True, "observations": {},
        }
        for name, roles in LEDGER.SHARED.ROLES.items():
            evidence = []
            for role in sorted(roles):
                evidence.append(self.write_reference(f"{name}-{role}.txt", f"physical fixture {name} {role}", role))
            self.packet["observations"][name] = {"value": 1, "evidence": evidence}

    def write_reference(self, name, content, role=None):
        path = self.root / name
        path.write_text(content)
        result = LEDGER.ORACLES.reference(path)
        if role:
            result["role"] = role
        return result

    def build(self, packet=None, **kwargs):
        ref = self.write_reference("packet.json", json.dumps(packet or self.packet))
        return LEDGER.build_ledger(self.baseline, [ref], **kwargs)

    def test_no_fresh_execution_from_configuration_or_history(self):
        result = LEDGER.build_ledger(self.baseline, [])
        self.assertEqual(result["summary"]["historical_executed"], 25)
        self.assertEqual(result["summary"]["historical_configuration_pass"], 9)
        self.assertEqual(result["summary"]["historical_full_lifecycle_pass"], 1)
        self.assertEqual(result["summary"]["fresh_executed"], 0)
        self.assertEqual(result["summary"]["fresh_full_lifecycle_pass"], 0)
        self.assertEqual(len(result["rows"]), 155)
        for row in result["rows"]:
            self.assertEqual(len(row["fresh_observations"]), 35)
            self.assertTrue(all(item["value"] is None for item in row["fresh_observations"].values()))
            self.assertIsNone(row["fresh_outcome"])
        self.assertEqual(result["rows"][0]["historical_result"], self.baseline["rows"][0])

    def test_complete_physical_packet_uses_shared_qualification(self):
        result = self.build(expected_identity={"run_id": "fresh-run", "parent_sha": "parent-source"})
        self.assertEqual(result["summary"]["fresh_full_lifecycle_pass"], 1)
        self.assertEqual(result["summary"]["missing_fresh_full_qualification"], 154)
        self.assertTrue(result["rows"][0]["fresh_qualified_pass"])

    def test_null_measurement_stays_partial(self):
        self.packet["observations"]["client_exit"] = {"value": None, "reason": "No waited exit."}
        self.packet["full_lifecycle_qualified"] = False
        result = self.build()
        self.assertEqual(result["summary"]["fresh_executed"], 1)
        self.assertEqual(result["summary"]["fresh_full_lifecycle_pass"], 0)
        self.assertIsNone(result["rows"][0]["fresh_outcome"])

    def test_incomplete_packet_cannot_claim_full_pass(self):
        self.packet["observations"]["client_exit"] = {"value": None, "reason": "Missing exit."}
        with self.assertRaisesRegex(ValueError, "missing observation"):
            self.build()

    def test_missing_physical_evidence_rejected(self):
        self.packet["observations"]["native_api_returns"]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "physical producer"):
            self.build()

    def test_source_only_native_calls_rejected(self):
        refs = self.packet["observations"]["native_api_returns"]["evidence"]
        refs[0]["role"] = "source_contract"
        with self.assertRaisesRegex(ValueError, "physical producer"):
            self.build()

    def test_mutated_evidence_bytes_rejected(self):
        ref = self.packet["observations"]["client_exit"]["evidence"][0]
        Path(ref["path"]).write_text("changed")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            self.build()

    def test_duplicate_and_foreign_packets_rejected(self):
        ref = self.write_reference("packet.json", json.dumps(self.packet))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            LEDGER.build_ledger(self.baseline, [ref, ref])
        self.packet["run_scoped_case_id"] = self.baseline["rows"][155]["run_scoped_case_id"]
        with self.assertRaisesRegex(ValueError, "foreign"):
            self.build()

    def test_wrong_route_and_run_binding_rejected(self):
        with self.assertRaisesRegex(ValueError, "expected identity"):
            self.build(expected_identity={"run_id": "another-run"})
        self.packet["leg_id"] = "nginx-native"
        with self.assertRaisesRegex(ValueError, "sibling route"):
            self.build()

    def test_oracle_digest_and_missing_identity_rejected(self):
        self.packet["oracle_sha256"] = "wrong"
        with self.assertRaisesRegex(ValueError, "effective oracle"):
            self.build()
        self.packet["parent_sha"] = None
        with self.assertRaisesRegex(ValueError, "identity"):
            self.build()

    def test_catalog_contract_mutation_rejected(self):
        changed = copy.deepcopy(self.baseline)
        changed["rows"][0]["selected_requirement"]["expected_oracle"]["visible_status"] = 201
        with self.assertRaisesRegex(ValueError, "oracles changed"):
            LEDGER.build_ledger(changed, [])

    def test_review_records_cannot_transfer_from_foreign_id(self):
        with self.assertRaisesRegex(ValueError, "foreign"):
            LEDGER.build_ledger(self.baseline, [], [{"run_scoped_case_id": "I12::nginx-native::foreign"}])


if __name__ == "__main__":
    unittest.main()
