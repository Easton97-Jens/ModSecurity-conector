"""Packaging must preserve original/null contracts and reject invented PASS."""

import copy
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest


PATH = Path(__file__).resolve().parents[1] / "ci/runtime/lifecycle/apache-i12/package.py"
SPEC = importlib.util.spec_from_file_location("apache_i12_package", PATH)
PACKAGE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PACKAGE)


class PackagingTest(unittest.TestCase):
    def setUp(self):
        root = Path(os.environ.get("CODEX_TEST_TMP_ROOT", "/var/tmp/codex/ModSecurity-conector/runs/i12-apache-410-20261015/package-tests"))
        root.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=root)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        unknown = {role: {"value": None, "reason": "No fresh physical packet."} for role in PACKAGE.ROLES}
        rows = []
        for number in range(155):
            identity = "I12::apache-native::fixture-" + str(number)
            oracle = {"visible_status": None, "unresolved_expected_value_reason": "No independently reviewed expectation."}
            rows.append({"run_scoped_case_id": identity, "leg_id": "apache-native", "required_leg": True,
                "selected_requirement": {"run_scoped_case_id": identity, "expected_oracle": copy.deepcopy(oracle)},
                "original_oracle": copy.deepcopy(oracle),
                "historical_result": {"status": "PASS" if number == 0 else "NOT_EXECUTED_UNQUALIFIED",
                    "execution_observed": number == 0,
                    "qualification_scope": "historical_configuration_only" if number == 0 else None},
                "oracle_reconciliation": None, "fresh_packet": None, "fresh_observations": copy.deepcopy(unknown),
                "fresh_execution_observed": False, "fresh_full_lifecycle_qualified": False,
                "fresh_outcome": None, "fresh_qualified_pass": False})
        self.source = {"scope": "apache-native", "rows": rows,
            "original_ordered_id_sha256": PACKAGE.ORACLES.ID_SHA256,
            "original_selected_contract_sha256": PACKAGE.ORACLES.CONTRACT_SHA256,
            "summary": {"original_open_oracle_subset": 155, "resolved_original_oracles": 0, "unresolved_original_oracles": 155}}
        self.source_path = self.root / "ledger.json"
        self.write("candidate-index.json", [])
        self.write("sink-readback.json", {"cases": []})

    def write(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value))
        return path

    def package(self):
        self.source_path.write_text(json.dumps(self.source))
        return PACKAGE.package(self.source_path, self.root)

    def test_original_oracle_and_null_roles_survive_without_config_promotion(self):
        result = self.package()
        self.assertEqual(len(result["rows"]), 155)
        self.assertEqual(result["summary"]["fresh_full_lifecycle_pass"], 0)
        row = result["rows"][0]
        self.assertTrue(row["historical"]["configuration_pass"])
        self.assertEqual(row["fresh"]["qualification"], "NOT_EXECUTED")
        self.assertEqual(row["selected_requirement"], self.source["rows"][0]["selected_requirement"])
        self.assertEqual(row["original_oracle"], self.source["rows"][0]["original_oracle"])
        self.assertEqual(row["fresh"]["observations"], self.source["rows"][0]["fresh_observations"])
        self.assertEqual(result["source_full_ledger"], PACKAGE.ref(self.source_path))

    def test_no_accepted_packet_cannot_claim_full_pass(self):
        self.source["rows"][0]["fresh_qualified_pass"] = True
        with self.assertRaisesRegex(ValueError, "no fresh qualification"):
            self.package()

    def test_unsigned_candidate_stays_partial_even_when_it_claims_pass(self):
        row = self.source["rows"][0]
        candidate = self.write("candidate.json", {"run_scoped_case_id": row["run_scoped_case_id"],
            "execution_observed": True, "reviewed_by": None, "full_lifecycle_qualified": True,
            "outcome": "PASS", "observations": row["fresh_observations"]})
        self.write("candidate-index.json", [{"case_id": row["run_scoped_case_id"], "candidate": PACKAGE.ref(candidate)}])
        result = self.package()
        fresh = result["rows"][0]["fresh"]
        self.assertTrue(fresh["execution_observed"])
        self.assertEqual(fresh["qualification"], "PARTIAL_HOST_MEASUREMENTS")
        self.assertIsNone(fresh["outcome"])
        self.assertFalse(fresh["qualified_pass"])
        self.assertIsNone(fresh["accepted_packet"])

    def test_packet_lookup_uses_supplied_reference_without_overwriting_acceptance(self):
        first = self.write("first.json", {"run_scoped_case_id": "first"})
        second = self.write("second.json", {"run_scoped_case_id": "second"})
        work = PACKAGE.ApachePackage(None, None, None, None)
        work.packets = {}
        work.supplied = PACKAGE.ref(first)
        work.receipt = None
        work.packet = None
        supplied = PACKAGE.ref(second)
        receipt, packet = work.packet_reference(supplied)
        self.assertEqual(receipt, supplied)
        self.assertEqual(packet["run_scoped_case_id"], "second")
        self.assertIsNone(work.receipt)
        self.assertIsNone(work.packet)

    def test_known_values_reference_exact_packet_without_replacing_nulls(self):
        observations = copy.deepcopy(self.source["rows"][0]["fresh_observations"])
        observations["client_exit"] = {"value": 0, "evidence": []}
        receipt = {"path": "/physical/packet.json", "sha256": "fixture-digest"}
        result = PACKAGE.compact_observations(observations, receipt)
        self.assertEqual(result["client_exit"]["observed_value_reference"],
                         {"packet_sha256": "fixture-digest", "json_pointer": "/observations/client_exit"})
        self.assertIsNone(result["backend_request_count"]["value"])

    def test_mutated_reference_and_foreign_id_rejected(self):
        candidate = self.write("candidate.json", {})
        receipt = PACKAGE.ref(candidate)
        candidate.write_text("changed")
        self.write("candidate-index.json", [{"case_id": self.source["rows"][0]["run_scoped_case_id"], "candidate": receipt}])
        with self.assertRaisesRegex(ValueError, "SHA256"):
            self.package()
        self.write("candidate-index.json", [{"case_id": "I12::nginx-native::foreign", "candidate": None}])
        with self.assertRaisesRegex(ValueError, "foreign"):
            self.package()


if __name__ == "__main__":
    unittest.main()
