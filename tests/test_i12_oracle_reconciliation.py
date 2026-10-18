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


# Exact original selected contract and primary YAML from Framework99a7985c.
# Kept inline so Parent validator tests do not depend on a materialized submodule.
CANONICAL_OVER_LIMIT = {'case_id': 'phase2_over_limit',
 'run_scoped_case_id': 'I12::haproxy-spop-request::phase2_over_limit',
 'status': 'PLANNED',
 'origin': 'canonical_selector',
 'canonical_source_case_id': 'phase2_over_limit',
 'requirement_mapping': ['phase2_over_limit',
                         'I12::haproxy-spop-request::obligation::request-reject'],
 'runner_case': None,
 'native_invocation': None,
 'config_invocation': None,
 'derived_invocation': None,
 'execution_kind': 'host_case_or_missing_fixture',
 'harness_path': 'connectors/haproxy/harness/combined_spop_htx/run_combined_spop_htx.sh',
 'missing_harness_reason': None,
 'expected_oracle': {'native_result': 'request_body_over_limit',
                     'visible_status': None,
                     'rule_id': None,
                     'phase': 2,
                     'event_fields': ['body_limit_outcome',
                                      'body_bytes_seen',
                                      'body_bytes_inspected',
                                      'truncated'],
                     'physical_evidence_not_projection': True,
                     'unresolved_expected_value_reason': None},
 'mandatory_missing_observations': ['client-exit-signal-headers-bytes-sha256',
                                    'independent-backend-request-count',
                                    'original-physical-native-events-first-cause',
                                    'commit-eos-order',
                                    'transport-framing-reset-scope',
                                    'once-finish-and-resource-release',
                                    'uid-isolation-and-exact-source-host-config-run-binding'],
 'historical_alias_ids': [],
 'source_fixture_paths': ['tests/cases/no-crs-baseline/full-lifecycle/phase2_body_limits.yaml']}
CANONICAL_LIMIT_YAML = """name: phase2_body_limits_fixture
title: Declarative phase-2 request body limit boundaries
category: no-crs-full-lifecycle
portable: true
status: future
no_crs_baseline: true
phase: 2
capabilities:
  request_body: true
  phase2: true
rules: |
  SecRuleEngine On
request:
  method: POST
  path: /no-crs/full-lifecycle/request-limit
  headers:
    Content-Type: text/plain
  body: 0123456789abcdef
expect:
  status: 200
  intervention: none
full_lifecycle:
  limit_bytes: 16
  variants:
    at_limit: 16
    over_limit: 17
    process_partial: 17
  requires_payload_free_limit_event: true
  evidence_status: not_executed_until_real_host
known_limitations:
  - Limit policy and host-visible status are connector configuration dependent; the canonical event must carry only bounded count and truncation metadata.
"""


class IntentionalNullContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="i12-intentional-null-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.row = {"run_scoped_case_id": CANONICAL_OVER_LIMIT["run_scoped_case_id"],
                    "leg_id": "haproxy-spop-request", "selected_requirement": copy.deepcopy(CANONICAL_OVER_LIMIT)}
        self.assertEqual(LEDGER.canonical_digest(CANONICAL_OVER_LIMIT),
                         "98f5423f9cf2a019997a8c751429c43956d3211488452b1e323b6099d10f847d")
        path = self.root / "phase2_body_limits.yaml"
        path.write_text(CANONICAL_LIMIT_YAML)
        self.proof = {**LEDGER.reference(path), "kind": "protocol_contract",
                      "revision": "99a7985c1be92a2297b1b59208f64df6768f2cbf"}
        self.assertEqual(self.proof["sha256"], "83e1bc8c6292e90f01acc84617f05113d2dbe625c88d7c4278f5327a6c121cfd")
        self.record = {"run_scoped_case_id": self.row["run_scoped_case_id"], "leg_id": self.row["leg_id"],
                       "reviewed_by": "root", "category": "SOURCE_CONFIRMED_EXPECTATION",
                       "scope": "Exact original canonical body-limit contract; no host execution.",
                       "interpretation": "Canonical visible status is host/config dependent, not unresolved.",
                       "independent_sources": [copy.deepcopy(self.proof)],
                       "intentional_null_fields": {"visible_status": {
                           "reviewed_by": "root", "interpretation": "Preserve the original intentionally unspecified status.",
                           "proof": [copy.deepcopy(self.proof)]}}}

    def review(self):
        return LEDGER.review_record(self.record, self.row)

    def test_real_canonical_original_null_is_preserved_without_execution_credit(self):
        original = copy.deepcopy(self.row)
        result = self.review()
        self.assertEqual(self.row, original)
        self.assertEqual(result["effective_oracle"], CANONICAL_OVER_LIMIT["expected_oracle"])
        self.assertIsNone(result["effective_oracle"]["visible_status"])
        self.assertTrue(result["resolved"])
        self.assertFalse(result["full_lifecycle_qualified"])
        self.assertIsNone(result["retest"])
        self.assertEqual(result["intentional_null_fields"]["visible_status"]["proof"][0]["sha256"], self.proof["sha256"])

    def test_canonical_null_still_fails_without_explicit_root_proof(self):
        self.record.pop("intentional_null_fields")
        with self.assertRaisesRegex(ValueError, "visible_status"):
            self.review()

    def test_missing_changed_or_unresolved_original_values_cannot_be_hidden(self):
        for field, mutation in (("visible_status", "missing"), ("visible_status", "changed"),
                                ("native_result", "missing"), ("native_result", "null"),
                                ("phase", "missing"), ("phase", "null"),
                                ("unresolved_expected_value_reason", "unresolved")):
            with self.subTest(field=field, mutation=mutation):
                original = copy.deepcopy(self.row)
                oracle = self.row["selected_requirement"]["expected_oracle"]
                if mutation == "missing":
                    del oracle[field]
                else:
                    oracle[field] = {"changed": 503, "null": None, "unresolved": "Missing fixture"}[mutation]
                with self.assertRaises(ValueError):
                    self.review()
                self.row = original

    def test_null_proof_never_combines_with_resolution_or_correction(self):
        for field in ("resolved_expectation", "approved_correction"):
            with self.subTest(field=field):
                original = copy.deepcopy(self.record)
                self.record[field] = copy.deepcopy(CANONICAL_OVER_LIMIT["expected_oracle"])
                with self.assertRaises(ValueError):
                    self.review()
                self.record = original

    def test_only_visible_status_and_source_confirmation_categories_permitted(self):
        for field, value in (("intentional_null_fields", {"native_result": {}}),
                             ("intentional_null_fields", {}), ("category", "UNRESOLVED_ORACLE"),
                             ("category", "PRODUCT_DEFECT_CONFIRMED")):
            with self.subTest(field=field, value=value):
                original = copy.deepcopy(self.record)
                self.record[field] = value
                with self.assertRaises(ValueError):
                    self.review()
                self.record = original

    def test_separate_root_interpretation_and_primary_proof_required(self):
        for mutation in ("root", "interpretation", "no-proof", "revision", "kind", "hash"):
            with self.subTest(mutation=mutation):
                original = copy.deepcopy(self.record)
                field = self.record["intentional_null_fields"]["visible_status"]
                if mutation == "root": field["reviewed_by"] = "worker"
                elif mutation == "interpretation": field["interpretation"] = ""
                elif mutation == "no-proof": field["proof"] = []
                elif mutation == "revision": field["proof"][0]["revision"] = "other-revision"
                elif mutation == "kind": field["proof"][0]["kind"] = "independent_host_probe"
                else: field["proof"][0]["sha256"] = "0" * 64
                with self.assertRaises(ValueError):
                    self.review()
                self.record = original

    def test_implementation_bytes_and_unbound_primary_sources_rejected(self):
        self.record["implementation_sources"] = [copy.deepcopy(self.proof)]
        with self.assertRaises(ValueError):
            self.review()
        self.record.pop("implementation_sources")
        path = self.root / "other-independent.txt"
        path.write_text("Another primary contract, not the declared independent source.")
        self.record["intentional_null_fields"]["visible_status"]["proof"][0].update(LEDGER.reference(path))
        with self.assertRaises(ValueError):
            self.review()

    def test_intentional_null_requires_the_complete_unchanged_effective_oracle(self):
        original = self.row["selected_requirement"]["expected_oracle"]
        changed = {**original, "fixture_status": 503}
        with self.assertRaises(ValueError):
            LEDGER.intentional_null_fields(self.record, original, changed, [self.proof], [])


if __name__ == "__main__":
    unittest.main()
