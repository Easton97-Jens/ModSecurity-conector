"""Negative controls for Root-reviewed original I12 host acceptance packets."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest import mock
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

    def test_direct_sdk_mime_accessor_is_native_api_and_transport_cannot_replace_it(self):
        self.packet["observations"]["mime_gate"] = {
            "value": {"native_mime_selection": {"content_type": "text/plain", "selected": True}},
            "evidence": [{**self.raw_ref, "role": "native_api"}]}
        self.assertTrue(self.review()["full_lifecycle_qualified"])
        self.packet["observations"]["mime_gate"]["evidence"][0]["role"] = "client_process"
        with self.assertRaisesRegex(ValueError, "suitable physical producer"):
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

    def parser_control(self):
        """Synthetic validator control; never exported as host evidence."""
        row, packet, self.oracle = configuration_control(self.root)
        return row, packet

    def parser_review(self, row, packet):
        path = self.root / "parser-packet.json"
        path.write_text(json.dumps(packet))
        return LEDGER.reviewed_configuration_packet(LEDGER.ORACLES.reference(path), row, self.oracle)

    def test_parser_scope_never_becomes_a_host_lifecycle_or_covers_an_http_id(self):
        row, packet = self.parser_control()
        result = self.parser_review(row, packet)
        self.assertTrue(result["full_case_qualified"])
        self.assertFalse(result["full_lifecycle_qualified"])
        self.assertEqual(result["qualification_scope"], "configuration_control")
        row["selected_requirement"]["execution_kind"] = "host_case_or_missing_fixture"
        with self.assertRaisesRegex(ValueError, "original actual_configtest"):
            self.parser_review(row, packet)

    def test_parser_scope_requires_actual_process_image_and_independent_oracle(self):
        row, packet = self.parser_control()
        del packet["actual_observations"]["parser_process"]["waited_exit"]
        with self.assertRaisesRegex(ValueError, "actual argv/cwd"):
            self.parser_review(row, packet)
        row, packet = self.parser_control()
        packet["measurement_evidence"] = [item for item in packet["measurement_evidence"]
                                          if item["role"] != "invoked_image"]
        with self.assertRaisesRegex(ValueError, "independent process, image"):
            self.parser_review(row, packet)
        row, packet = self.parser_control()
        packet["actual_observations"]["parser_process"]["waited_exit"] = 1
        with self.assertRaisesRegex(ValueError, "differs from physical process"):
            self.parser_review(row, packet)


def configuration_control(root):
    """A synthetic control for the existing configuration_parser packet API."""
    def write(name, content, role):
        path = root / name
        path.write_bytes(content if isinstance(content, bytes) else json.dumps(content).encode())
        return {**LEDGER.ORACLES.reference(path), "role": role}

    oracle = {"native_result": "config_accepted", "visible_status": 0, "phase": 0,
              "rule_id": 1100001, "physical_evidence_not_projection": True}
    case_id = "I12::haproxy-spop-request::valid_rules_file"
    row = {"run_scoped_case_id": case_id, "leg_id": "haproxy-spop-request", "required_leg": True,
           "status": "NOT_EXECUTED_UNQUALIFIED", "execution_observed": None,
           "selected_requirement": {"execution_kind": "actual_configtest", "expected_oracle": oracle,
                                    "mandatory_missing_observations": list(LEDGER.CONFIGURATION_FIELDS)}}
    refs = {role: write(role, content, role) for role, content in (
        ("invoked_image", b"synthetic host"), ("native_module", b"synthetic module"),
        ("effective_configuration", b"synthetic config"), ("rules_file", b"synthetic rules"),
        ("parser_stdout", b""), ("parser_stderr", b""),
        ("source_manifest", {"parent_sha": "control-parent"}),
        ("cleanup_observer", {"processes_remaining": 0}), ("isolation_receipt", {"synthetic_isolation": True}),
        ("expectation_source", {"official_contract": "independent synthetic expectation"}))}
    refs["expectation_source"].update(kind="official_host_contract", revision="synthetic-1")
    packet = {"run_scoped_case_id": case_id, "leg_id": row["leg_id"], "reviewed_by": "root",
              "execution_kind": "configuration_parser", "execution_observed": True,
              "run_id": "synthetic-parser-run", "parent_sha": "control-parent",
              "effective_config_sha256": refs["effective_configuration"]["sha256"],
              "rules_sha256": refs["rules_file"]["sha256"], "oracle_evaluated": True,
              "oracle_sha256": LEDGER.ORACLES.canonical_digest(oracle), "outcome": "PASS"}
    process = {"argv": ["/synthetic/parser", "-c", "-f", "/synthetic/config"], "cwd": str(root),
               "waited_exit": 0, "waited_signal": None, "stdout": "", "stderr": "",
               "executable_sha256": refs["invoked_image"]["sha256"]}
    packet["actual_observations"] = {
        "parser_process": process,
        "invocation_identity": {"host_binary_sha256": refs["invoked_image"]["sha256"],
                                "module_sha256": refs["native_module"]["sha256"]},
        "source_config_binding": {name: packet[name] for name in ("parent_sha", "effective_config_sha256", "rules_sha256")},
        "cleanup": {"processes_remaining": 0}}
    actual = {name: packet[name] for name in ("run_scoped_case_id", "leg_id", "run_id", "parent_sha",
             "effective_config_sha256", "rules_sha256", "execution_kind", "execution_observed")}
    refs["parser_process"] = write("process.json", {**actual, **process}, "parser_process")
    packet["measurement_evidence"] = list(refs.values())
    return row, packet, oracle


class ConfigurationLedgerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="i12-configuration-ledger-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.row, self.packet, self.oracle = configuration_control(self.root)

    def review(self):
        path = self.root / "packet.json"
        path.write_text(json.dumps(self.packet))
        return LEDGER.reviewed_configuration_packet(LEDGER.ORACLES.reference(path), self.row, self.oracle)

    def process(self):
        return self.packet["actual_observations"]["parser_process"]

    def rebind_process(self):
        ref = next(item for item in self.packet["measurement_evidence"] if item["role"] == "parser_process")
        path = Path(ref["path"])
        actual = json.loads(path.read_text())
        actual.update(self.process())
        path.write_text(json.dumps(actual))
        ref.update(LEDGER.ORACLES.reference(path))

    def test_exact_three_original_observations_without_lifecycle_fabrication(self):
        result = self.review()
        self.assertEqual(set(result["mandatory_observations"]), set(LEDGER.CONFIGURATION_FIELDS))
        self.assertTrue(result["full_case_qualified"])
        self.assertFalse(result["full_lifecycle_qualified"])
        self.assertEqual(result["qualification_scope"], "configuration_control")

    def test_exact_rejection_exit_and_truthful_failure(self):
        self.oracle.update(native_result="config_rejected", visible_status=1, rule_id=None)
        self.packet["oracle_sha256"] = LEDGER.ORACLES.canonical_digest(self.oracle)
        self.process()["waited_exit"] = 1
        self.rebind_process()
        self.assertEqual(self.review()["outcome"], "PASS")
        self.process()["waited_exit"] = 77
        self.rebind_process()
        with self.assertRaises(ValueError):
            self.review()
        self.packet["outcome"] = "FAIL"
        self.assertEqual(self.review()["outcome"], "FAIL")

    def test_exact_source_reviewed_rejection_exit_255_is_not_normalized(self):
        self.oracle.update(native_result="config_rejected", visible_status=255, rule_id=None)
        self.packet["oracle_sha256"] = LEDGER.ORACLES.canonical_digest(self.oracle)
        self.process()["waited_exit"] = 255
        self.rebind_process()
        self.assertEqual(self.review()["outcome"], "PASS")
        self.process()["waited_exit"] = 1
        self.rebind_process()
        with self.assertRaisesRegex(ValueError, "contradicts actual exit"):
            self.review()
        self.packet["outcome"] = "FAIL"
        self.assertEqual(self.review()["outcome"], "FAIL")

    def test_parser_expected_exit_must_be_an_exact_posix_code(self):
        for result, code in (("config_rejected", 0), ("config_rejected", -1),
                             ("config_rejected", 256), ("config_rejected", True),
                             ("config_rejected", 1.0), ("config_accepted", 255)):
            with self.subTest(result=result, code=code):
                self.oracle.update(native_result=result, visible_status=code)
                self.packet["oracle_sha256"] = LEDGER.ORACLES.canonical_digest(self.oracle)
                with self.assertRaisesRegex(ValueError, "explicit acceptance or rejection oracle"):
                    self.review()

    def test_missing_rules_file_binds_absence_without_inventing_file_hash(self):
        identity = "I12::haproxy-spop-request::missing_rules_file"
        self.row["run_scoped_case_id"] = identity
        self.packet["run_scoped_case_id"] = identity
        self.oracle.update(native_result="config_rejected", visible_status=1, rule_id=None)
        self.packet["oracle_sha256"] = LEDGER.ORACLES.canonical_digest(self.oracle)
        self.packet["rules_sha256"] = None
        absence = {name: self.packet[name] for name in ("run_scoped_case_id", "leg_id", "run_id", "parent_sha")}
        absence.update(type="physical_path_absence", rules_path="/synthetic/missing.conf", exists=False,
                       measurement="lstat", errno=2, symlink_components=[])
        path = self.root / "absence.json"
        path.write_text(json.dumps(absence))
        ref = {**LEDGER.ORACLES.reference(path), "role": "rules_absence"}
        self.packet["rules_absence_sha256"] = ref["sha256"]
        self.packet["measurement_evidence"] = [item for item in self.packet["measurement_evidence"] if item["role"] != "rules_file"] + [ref]
        binding = self.packet["actual_observations"]["source_config_binding"]
        binding.update(rules_sha256=None, rules_absence_sha256=ref["sha256"])
        process_ref = next(item for item in self.packet["measurement_evidence"] if item["role"] == "parser_process")
        actual_path = Path(process_ref["path"])
        actual = json.loads(actual_path.read_text())
        actual.update(run_scoped_case_id=identity, rules_sha256=None, rules_path=absence["rules_path"], rules_exists=False,
                      rules_lstat_errno=2, rules_absence_sha256=ref["sha256"])
        self.process()["waited_exit"] = 1
        actual.update(self.process())
        actual_path.write_text(json.dumps(actual))
        process_ref.update(LEDGER.ORACLES.reference(actual_path))
        self.assertEqual(self.review()["outcome"], "PASS")
        self.packet["rules_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.review()
        self.packet["rules_sha256"] = None
        actual["rules_path"] = "/synthetic/other-missing.conf"
        actual_path.write_text(json.dumps(actual))
        process_ref.update(LEDGER.ORACLES.reference(actual_path))
        with self.assertRaises(ValueError):
            self.review()

    def test_wrong_profile_id_review_kind_and_oracle_rejected(self):
        for name, value in (("run_scoped_case_id", "other"), ("leg_id", "haproxy-native-htx"),
                            ("reviewed_by", "worker"), ("execution_kind", "driver_exit"),
                            ("oracle_sha256", "0" * 64), ("execution_observed", False),
                            ("full_lifecycle_qualified", True)):
            with self.subTest(name=name):
                original = copy.deepcopy(self.packet)
                self.packet[name] = value
                with self.assertRaises(ValueError):
                    self.review()
                self.packet = original

    def test_projected_process_fields_rejected(self):
        for name, value in (("argv", ["driver"]), ("cwd", "/wrong"), ("waited_exit", 1),
                            ("waited_signal", 9), ("stderr", "invented"), ("executable_sha256", "0" * 64)):
            with self.subTest(name=name):
                original = copy.deepcopy(self.packet)
                self.process()[name] = value
                with self.assertRaises(ValueError):
                    self.review()
                self.packet = original

    def test_signal_and_false_pass_fail_without_lifecycle_credit(self):
        self.process()["waited_signal"] = 9
        self.rebind_process()
        with self.assertRaises(ValueError):
            self.review()
        self.packet["outcome"] = "FAIL"
        self.assertFalse(self.review()["full_lifecycle_qualified"])

    def test_missing_required_physical_producers_rejected(self):
        for ref in self.packet["measurement_evidence"][:]:
            with self.subTest(role=ref["role"]):
                original = copy.deepcopy(self.packet)
                self.packet["measurement_evidence"].remove(ref)
                with self.assertRaises(ValueError):
                    self.review()
                self.packet = original

    def test_corrupt_and_symlink_evidence_rejected(self):
        ref = self.packet["measurement_evidence"][0]
        original = copy.deepcopy(ref)
        ref["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.review()
        ref.update(original)
        alias = self.root / "alias"
        alias.symlink_to(Path(ref["path"]))
        ref["path"] = str(alias)
        with self.assertRaises(ValueError):
            self.review()

    def test_independent_expectation_cannot_be_implementation_or_unversioned(self):
        ref = next(item for item in self.packet["measurement_evidence"] if item["role"] == "expectation_source")
        del ref["revision"]
        with self.assertRaises(ValueError):
            self.review()
        ref["revision"] = "synthetic-1"
        ref.update({name: self.packet["measurement_evidence"][0][name] for name in ("path", "sha256", "bytes")})
        with self.assertRaises(ValueError):
            self.review()

    def test_configuration_and_source_identity_changes_rejected(self):
        for name in ("parent_sha", "effective_config_sha256", "rules_sha256"):
            with self.subTest(name=name):
                original = self.packet[name]
                self.packet[name] = "0" * 64
                with self.assertRaises(ValueError):
                    self.review()
                self.packet[name] = original

    def test_physical_stdout_stderr_and_executable_cannot_be_substituted(self):
        for name, value in (("stdout", "invented"), ("stderr", "invented"),
                            ("executable_sha256", "0" * 64), ("cwd", "relative")):
            with self.subTest(name=name):
                original = copy.deepcopy(self.packet)
                self.process()[name] = value
                self.rebind_process()
                with self.assertRaises(ValueError):
                    self.review()
                self.packet = original
                self.rebind_process()

    def test_build_ledger_dispatches_parser_and_preserves_historical_contract(self):
        requirements = {"rows": [self.row]}
        reconciliation = {"original_selected_contracts": [self.row["selected_requirement"]],
                          "oracle_matrix": [], "supplemental_dispositions": [], "summary": {}}
        original = copy.deepcopy(requirements)
        path = self.root / "packet.json"
        path.write_text(json.dumps(self.packet))
        with mock.patch.object(LEDGER.ORACLES, "original_contracts", return_value=requirements["rows"]):
            result = LEDGER.build_ledger(requirements, {}, reconciliation, [LEDGER.ORACLES.reference(path)])
        self.assertEqual(requirements, original)
        row = result["rows"][0]
        self.assertEqual(row["historical_status"], "NOT_EXECUTED_UNQUALIFIED")
        self.assertTrue(row["qualified_configuration_pass"])
        self.assertFalse(row["qualified_host_lifecycle_pass"])
        self.assertIsNone(row["current_lifecycle_packet"])
        self.assertEqual(result["summary"]["current_configuration_pass"], 1)
        self.assertEqual(result["summary"]["full_lifecycle_pass"], 0)


if __name__ == "__main__":
    unittest.main()
