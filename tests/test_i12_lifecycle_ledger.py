"""Negative controls for Root-reviewed original I12 host acceptance packets."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "i12_lifecycle_ledger", ROOT / "ci/evidence/reports/generate-pr382-i12-lifecycle-ledger.py")
LEDGER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LEDGER)


class LifecycleLedgerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="i12-lifecycle-ledger-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.raw = self.root / "physical-observation.json"
        self.raw.write_text('{"actual_measurement":1}\n')
        self.raw_ref = {"path": str(self.raw), "sha256": hashlib.sha256(self.raw.read_bytes()).hexdigest()}
        self.case = "I12::traefik-native-uds::NEED-request-eos-once"
        self.row = {"run_scoped_case_id": self.case, "leg_id": "traefik-native-uds"}
        self.oracle = {"native_result": "allow", "visible_status": 200, "phase": 2,
                       "physical_evidence_not_projection": True}
        self.packet = {"run_scoped_case_id": self.case, "leg_id": "traefik-native-uds",
                       "reviewed_by": "root", "execution_observed": True, "execution_kind": "host_http",
                       "run_id": "synthetic-validator-control", "parent_sha": "control-parent",
                       "framework_sha": "control-framework", "mrts_sha": "control-mrts",
                       "effective_config_sha256": "control-config", "oracle_evaluated": True,
                       "oracle_sha256": LEDGER.ORACLES.canonical_digest(self.oracle), "outcome": "PASS",
                       "observations": {field: {"value": 1, "evidence": [{**self.raw_ref, "role": role} for role in sorted(roles)]}
                                        for field, roles in LEDGER.ROLES.items()}}

    def review(self, packet=None, oracle=None):
        path = self.root / "reviewed-packet.json"
        path.write_text(json.dumps(self.packet if packet is None else packet))
        ref = LEDGER.ORACLES.reference(path)
        return LEDGER.reviewed_packet(ref, self.row, self.oracle if oracle is None else oracle)

    def test_complete_validator_control_and_measured_failure_are_distinct(self):
        self.assertTrue(self.review()["full_lifecycle_qualified"])
        self.packet["outcome"] = "FAIL"
        self.assertEqual(self.review()["outcome"], "FAIL")

    def test_missing_native_eos_never_uses_client_eof_as_replacement(self):
        self.packet["observations"]["native_eos"] = {"value": None, "reason": "Native EOS was not measured."}
        result = self.review()
        self.assertFalse(result["full_lifecycle_qualified"])
        self.assertIsNone(result["outcome"])
        self.assertEqual(result["unknown_fields"], ["native_eos"])
        self.packet["full_lifecycle_qualified"] = True
        with self.assertRaisesRegex(ValueError, "prevents full qualification"):
            self.review()

    def test_transport_receipt_cannot_prove_native_free(self):
        self.packet["observations"]["native_free_calls"]["evidence"][0]["role"] = "client_process"
        with self.assertRaisesRegex(ValueError, "suitable physical producer"):
            self.review()

    def test_native_call_without_independent_host_eos_producer_is_partial(self):
        self.packet["observations"]["native_eos"]["evidence"] = [{**self.raw_ref, "role": "native_api"}]
        with self.assertRaisesRegex(ValueError, "Independent producers are missing"):
            self.review()

    def test_unknown_without_reason_is_rejected(self):
        self.packet["observations"]["mime_gate"] = {"value": None}
        with self.assertRaisesRegex(ValueError, "exact missing reason"):
            self.review()

    def test_sibling_case_or_route_cannot_inherit_packet(self):
        for field, replacement in (("leg_id", "traefik-forwardauth-request"),
                                   ("run_scoped_case_id", "I12::traefik-native-uds::allow_without_marker")):
            packet = copy.deepcopy(self.packet)
            packet[field] = replacement
            with self.assertRaisesRegex(ValueError, "sibling route or case"):
                self.review(packet)

    def test_parser_pass_and_driver_exit_are_not_host_verdicts(self):
        self.packet["execution_kind"] = "configuration_parser"
        with self.assertRaisesRegex(ValueError, "actual host HTTP"):
            self.review()
        self.packet["execution_kind"] = "host_http"
        self.packet["outcome"] = "EXIT_0"
        with self.assertRaisesRegex(ValueError, "not a lifecycle verdict"):
            self.review()

    def test_unresolved_oracle_and_missing_root_review_rejected(self):
        self.packet["oracle_sha256"] = "unresolved-oracle"
        with self.assertRaisesRegex(ValueError, "independently reviewed"):
            self.review()
        self.packet["oracle_sha256"] = LEDGER.ORACLES.canonical_digest(self.oracle)
        self.packet["reviewed_by"] = "worker"
        with self.assertRaisesRegex(ValueError, "Root review"):
            self.review()

    def test_nonapplicability_needs_capability_and_never_hides_backend_count(self):
        self.packet["observations"]["mime_gate"] = {
            "value": None, "applicable": False, "reason": "Request-only control, no response engine path.",
            "capability_proof": [{**self.raw_ref, "role": "source_contract"}]}
        self.assertTrue(self.review()["full_lifecycle_qualified"])
        self.packet["observations"]["backend_request_count"] = copy.deepcopy(self.packet["observations"]["mime_gate"])
        with self.assertRaisesRegex(ValueError, "Invalid nonapplicability"):
            self.review()

    def test_altered_physical_evidence_or_symlink_rejected(self):
        self.raw.write_text('{"actual_measurement":2}\n')
        with self.assertRaisesRegex(ValueError, "SHA256"):
            self.review()
        self.raw.write_text('{"actual_measurement":1}\n')
        alias = self.root / "alias.json"
        alias.symlink_to(self.raw)
        self.packet["observations"]["native_free_calls"]["evidence"][0]["path"] = str(alias)
        with self.assertRaisesRegex(ValueError, "physical absolute regular file"):
            self.review()


if __name__ == "__main__":
    unittest.main()
