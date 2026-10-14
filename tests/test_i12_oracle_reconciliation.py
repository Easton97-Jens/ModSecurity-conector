"""Negative controls for the Parent-only immutable I12 oracle review ledger."""

import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "ci/evidence/reports/generate-pr382-i12-oracle-reconciliation.py"
SPEC = importlib.util.spec_from_file_location("i12_oracle_reconciliation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
LEDGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LEDGER)


class OracleReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.requirements = {"rows": []}
        for index in range(1484):
            case_id = f"I12::profile::NEED-synthetic-{index}"
            oracle = self.expectation()
            if index < 596:
                oracle.update(native_result=None, visible_status=None, phase=None,
                              unresolved_expected_value_reason="Synthetic missing fixture")
            contract = {"run_scoped_case_id": case_id, "case_id": f"NEED-synthetic-{index}",
                        "expected_oracle": oracle, "origin": "missing_host_fixture_or_oracle"}
            self.requirements["rows"].append({"run_scoped_case_id": case_id, "leg_id": "profile",
                                              "required_leg": index < 1406,
                                              "selected_requirement": contract,
                                              "status": "NOT_EXECUTED_UNQUALIFIED", "execution_observed": False})
        contracts = [row["selected_requirement"] for row in self.requirements["rows"]]
        self.selection = {"legs": [{"leg_id": "profile", "required_leg": True,
                                    "required_cases": copy.deepcopy(contracts[:1406])},
                                   {"leg_id": "profile", "required_leg": False,
                                    "required_cases": copy.deepcopy(contracts[1406:])}],
                          "revisions": {"parent": "synthetic-revision"}, "source_hashes": {}}
        ids = [row["run_scoped_case_id"] for row in self.requirements["rows"]]
        patches = (mock.patch.object(LEDGER, "CONTRACT_SHA256", LEDGER.canonical_digest(contracts)),
                   mock.patch.object(LEDGER, "ID_SHA256", hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest()))
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    @staticmethod
    def expectation():
        return {"native_result": "allow", "visible_status": 200, "phase": 1,
                "rule_id": None, "event_fields": [], "physical_evidence_not_projection": True,
                "unresolved_expected_value_reason": None}

    def evidence(self, filename, value, kind="official_host_contract"):
        path = self.root / filename
        path.write_text(json.dumps(value))
        return {**LEDGER.reference(path), "kind": kind, "revision": "synthetic-1"}

    def reviewed(self, index=0):
        row = self.requirements["rows"][index]
        return {"run_scoped_case_id": row["run_scoped_case_id"], "leg_id": row["leg_id"],
                "reviewed_by": "root", "category": "SOURCE_CONFIRMED_EXPECTATION",
                "interpretation": "Synthetic contract independently confirms allow semantics",
                "scope": "Only the exact synthetic fixture/profile",
                "independent_sources": [self.evidence("contract.json", {"independent": "contract"})],
                "resolved_expectation": self.expectation()}

    def run_ledger(self, records=()):
        return LEDGER.reconcile(self.requirements, self.selection, records)

    def test_original_inventory_and_resolution_do_not_qualify_execution(self):
        baseline = self.run_ledger()
        self.assertEqual(len(baseline["original_selected_contracts"]), 1484)
        self.assertEqual(len(baseline["oracle_matrix"]), 596)
        self.assertEqual(baseline["summary"]["unresolved_original_oracles"], 596)
        result = self.run_ledger([self.reviewed()])
        self.assertEqual(result["summary"]["resolved_original_oracles"], 1)
        self.assertEqual(result["summary"]["actually_retested_original_oracles"], 0)
        self.assertFalse(result["oracle_matrix"][0]["full_lifecycle_qualified"])
        self.assertIsNone(result["oracle_matrix"][0]["original_oracle"]["visible_status"])

    def test_missing_duplicate_reordered_and_modified_originals_are_rejected(self):
        for mutation in ("missing", "duplicate", "reordered", "oracle", "membership"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(self.requirements)
                rows = changed["rows"]
                if mutation == "missing":
                    rows.pop()
                elif mutation == "duplicate":
                    rows[1] = copy.deepcopy(rows[0])
                elif mutation == "reordered":
                    rows[0], rows[1] = rows[1], rows[0]
                elif mutation == "oracle":
                    rows[0]["selected_requirement"]["expected_oracle"]["visible_status"] = 200
                else:
                    rows[0]["required_leg"], rows[-1]["required_leg"] = rows[-1]["required_leg"], rows[0]["required_leg"]
                with self.assertRaises(ValueError):
                    LEDGER.reconcile(changed, self.selection, [])

    def test_unsupported_category_and_unknown_or_duplicate_review_are_rejected(self):
        review = self.reviewed()
        for mutation in ("category", "unknown", "duplicate", "sibling"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(review)
                records = [changed]
                if mutation == "category":
                    changed["category"] = "AUTOMATIC_PASS"
                elif mutation == "unknown":
                    changed["run_scoped_case_id"] = "I12::profile::missing"
                elif mutation == "duplicate":
                    records.append(copy.deepcopy(changed))
                else:
                    changed["leg_id"] = "other-profile"
                with self.assertRaises(ValueError):
                    self.run_ledger(records)

    def test_resolution_requires_independent_revision_bound_unchanged_bytes(self):
        review = self.reviewed()
        for mutation in ("missing", "kind", "revision", "hash", "implementation"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(review)
                source = changed["independent_sources"][0]
                if mutation == "missing":
                    changed["independent_sources"] = []
                elif mutation == "kind":
                    source["kind"] = "product_source"
                elif mutation == "revision":
                    source.pop("revision")
                elif mutation == "hash":
                    source["sha256"] = "0" * 64
                else:
                    changed["implementation_sources"] = [copy.deepcopy(source)]
                with self.assertRaises(ValueError):
                    self.run_ledger([changed])

    def test_physical_reference_rejects_symlink_component(self):
        (self.root / "actual").mkdir()
        (self.root / "actual/file.json").write_text("{}")
        (self.root / "alias").symlink_to(self.root / "actual", target_is_directory=True)
        with self.assertRaises(ValueError):
            LEDGER.reference(self.root / "alias/file.json")

    def test_unsupported_capability_requires_exact_independent_applicability(self):
        review = self.reviewed()
        review.pop("resolved_expectation")
        review["category"] = "UNSUPPORTED_CAPABILITY"
        with self.assertRaises(ValueError):
            self.run_ledger([review])
        applicability = {"run_scoped_case_id": review["run_scoped_case_id"], "leg_id": "profile",
                         "parent_sha": "synthetic-source", "effective_config_sha256": "1" * 64,
                         "capability_supported": False, "capability_evidence": review["independent_sources"]}
        review["applicability_receipt"] = self.evidence("applicability.json", applicability)
        result = self.run_ledger([review])
        self.assertEqual(result["summary"]["resolved_original_oracles"], 1)
        self.assertIsNone(result["oracle_matrix"][0]["original_oracle"]["visible_status"])
        self.assertIsNone(result["oracle_matrix"][0]["retest"])
        for mutation in ("sibling", "supported", "no-proof"):
            changed = copy.deepcopy(applicability)
            if mutation == "sibling":
                changed["leg_id"] = "other-profile"
            elif mutation == "supported":
                changed["capability_supported"] = True
            else:
                changed["capability_evidence"] = []
            modified_review = copy.deepcopy(review)
            modified_review["applicability_receipt"] = self.evidence(f"applicability-{mutation}.json", changed)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.run_ledger([modified_review])

    def test_oracle_correction_is_separate_and_cannot_conceal_product_defect(self):
        review = self.reviewed(600)
        review.pop("resolved_expectation")
        corrected = self.expectation()
        corrected["visible_status"] = 204
        review.update(category="ORACLE_DEFECT_CONFIRMED", approved_correction={
            "reviewed_by": "root", "reason": "Independent synthetic contract establishes 204",
            "expected_oracle": corrected, "proof": copy.deepcopy(review["independent_sources"])})
        result = self.run_ledger([review])
        self.assertEqual(result["summary"]["resolved_original_oracles"], 0)
        supplemental = result["supplemental_dispositions"][0]
        self.assertEqual(supplemental["original_oracle"]["visible_status"], 200)
        self.assertEqual(supplemental["effective_oracle"]["visible_status"], 204)
        for mutation in ("product", "no-proof", "no-approval"):
            changed = copy.deepcopy(review)
            if mutation == "product":
                changed["category"] = "PRODUCT_DEFECT_CONFIRMED"
            elif mutation == "no-proof":
                changed["approved_correction"]["proof"] = []
            else:
                changed["approved_correction"]["reviewed_by"] = "automatic"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.run_ledger([changed])

    def test_retest_requires_actual_independent_exact_case_measurements(self):
        review = self.reviewed()
        receipt = {"execution_observed": True, "run_scoped_case_id": review["run_scoped_case_id"],
                   "leg_id": "profile", "run_id": "synthetic-actual-run", "parent_sha": "synthetic-source",
                   "effective_config_sha256": "1" * 64, "rules_sha256": "2" * 64,
                   "oracle_sha256": LEDGER.canonical_digest(self.expectation()),
                   "oracle_evaluated": True, "outcome": "PASS", "actual_observations": {"client_exit": 0},
                   "measurement_evidence": [self.evidence("client.json", {"actual_client_exit": 0}, "independent_host_probe")]}
        review["retest"] = self.evidence("retest.json", receipt, "independent_host_probe")
        result = self.run_ledger([review])
        self.assertEqual(result["summary"]["actually_retested_original_oracles"], 1)
        self.assertFalse(result["oracle_matrix"][0]["retest"]["full_lifecycle_qualified"])
        for mutation in ("not-observed", "sibling", "other-case", "oracle", "no-measurements", "no-config"):
            changed = copy.deepcopy(receipt)
            if mutation == "not-observed":
                changed["execution_observed"] = False
            elif mutation == "sibling":
                changed["leg_id"] = "other-profile"
            elif mutation == "other-case":
                changed["run_scoped_case_id"] = self.requirements["rows"][1]["run_scoped_case_id"]
            elif mutation == "oracle":
                changed["oracle_sha256"] = "0" * 64
            elif mutation == "no-measurements":
                changed["measurement_evidence"] = []
            else:
                changed.pop("effective_config_sha256")
            modified_review = copy.deepcopy(review)
            modified_review["retest"] = self.evidence(f"{mutation}.json", changed, "independent_host_probe")
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.run_ledger([modified_review])


if __name__ == "__main__":
    unittest.main()
