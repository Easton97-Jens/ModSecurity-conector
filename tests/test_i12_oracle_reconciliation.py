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


class ApacheStatusAbsenceTests(unittest.TestCase):
    """Physical synthetic validator controls; none are exported as runtime evidence."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="i12-absence-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.case = "I12::apache-native::NEED-cancel"
        self.row = {"run_scoped_case_id": self.case, "leg_id": "apache-native",
                    "selected_requirement": {
                        "case_id": "NEED-cancel", "run_scoped_case_id": self.case,
                        "requirement_mapping": ["I12::apache-native::obligation::cancel"],
                        "expected_oracle": {"native_result": None, "visible_status": None, "phase": None,
                                            "unresolved_expected_value_reason": "Original unresolved scenario"}}}
        self.oracle = {"native_result": "cancelled", "visible_status": None, "phase": 2,
                       "physical_evidence_not_projection": True,
                       "expected_absence": {"visible_status": {"kind": "no_complete_http_status_line"}}}
        sources = [self.write("host-source", {"host_contract": "synthetic-control"},
                              kind="official_host_contract", revision="control-1"),
                   self.write("protocol-source", {"protocol_contract": "synthetic-control"},
                              kind="protocol_contract", revision="control-1")]
        self.review = {"run_scoped_case_id": self.case, "leg_id": "apache-native", "reviewed_by": "root",
                       "category": "HOST_SEMANTICS_CONFIRMED", "interpretation": "Synthetic absence control",
                       "scope": "Exact original cancellation", "independent_sources": sources,
                       "resolved_expectation": self.oracle,
                       "expected_absence_approval": {
                           "reviewed_by": "root", "scope": "visible_status_absence", "reason": "Source control",
                           "run_scoped_case_id": self.case,
                           "selected_requirement_sha256": LEDGER.canonical_digest(self.row["selected_requirement"]),
                           "requirement_mapping_sha256": LEDGER.canonical_digest(
                               self.row["selected_requirement"]["requirement_mapping"]), "proof": sources}}
        self.identity = {"run_scoped_case_id": self.case, "leg_id": "apache-native", "run_id": "control-run",
                         "parent_sha": "control-parent", "effective_config_sha256": "control-config",
                         "rules_sha256": "control-rules", "request_id": "control-request", "host_pid": 100,
                         "client_pid": 101, "native_transaction_id": "control-native"}
        self.client = {**self.identity, "execution_observed": True, "executed_case_contract": True,
                       "started_ns": 100, "completed_ns": 200,
                       "status": None, "termination_kind": "client_signalled", "actual_waited_exit": -15,
                       "actual_waited_signal": 15, "argv": ["control-client"], "cwd": str(self.root)}
        self.host = {**self.identity, "execution_observed": True, "termination_observed": True,
                     "termination_kind": "client_signalled"}
        spec = importlib.util.spec_from_file_location("absence_control_ledger", SCRIPT.with_name(
            "generate-pr382-i12-lifecycle-ledger.py"))
        lifecycle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lifecycle)
        self.physical = self.write("measurement", {"synthetic_measurement": True})
        self.packet = {**self.identity, "reviewed_by": "root", "execution_observed": True,
                       "execution_kind": "host_http", "framework_sha": "control-framework", "mrts_sha": "control-mrts",
                       "oracle_evaluated": True, "oracle_sha256": LEDGER.canonical_digest(self.oracle), "outcome": "PASS",
                       "observations": {field: {"value": 1, "evidence": [{**self.physical, "role": role}
                                                  for role in sorted(roles)]}
                                        for field, roles in lifecycle.ROLES.items()}}
        self.packet["observations"]["native_transaction_id"]["value"] = {
            "transaction_id": "control-native", "canonical_transaction_id": "control-native",
            "transaction_id_origin": "native"}
        self.packet["observations"]["finish_calls"]["value"] = {"common_finish": 1, "native_logging": 1}
        self.packet["observations"]["native_free_calls"]["value"] = {
            "native_cleanup": 1, "common_cleanup": 1, "host_association_retire": 1}
        self.packet["observations"]["native_events"]["value"] = {
            "native_transaction_id": "control-native", "native_audit_lines": ["actual-control"],
            "physical_common_rows": []}
        self.receipt = {**self.identity, "execution_observed": True, "oracle_evaluated": True,
                        "oracle_sha256": LEDGER.canonical_digest(self.oracle), "outcome": "PASS",
                        "actual_observations": {"synthetic": True}, "measurement_evidence": [self.physical]}
        self.raw = b""

    def write(self, name, content, **metadata):
        path = self.root / name
        path.write_bytes(content if isinstance(content, bytes) else json.dumps(content).encode())
        return {**LEDGER.reference(path), **metadata}

    def bind(self):
        capture = self.write("raw-response", self.raw)
        self.client["response_capture_sha256"] = capture["sha256"]
        client = self.write("client-receipt", self.client)
        host = self.write("host-receipt", self.host)
        for field in ("client_exit", "client_headers", "transport_framing"):
            self.packet["observations"][field]["evidence"] = [
                {**ref, "role": "client_process"} for ref in (client, capture)]
        self.packet["observations"]["transport_reset_scope"] = {
            "value": {"scope": "actual-connection"},
            "evidence": [{**client, "role": "client_process"}, {**host, "role": "host_callback"}]}
        self.receipt["visible_status_absence"] = {
            "client_termination_receipt": client, "response_capture": capture,
            "host_termination_receipt": host, "lifecycle_packet": self.write("packet", self.packet)}
        self.review["retest"] = self.write("retest", self.receipt)

    def result(self):
        return LEDGER.review_record(self.review, self.row)

    def zero_event_observer(self):
        controls = [{"transaction_id": identity, "connector": "apache", "message_id": "MSCONN_EVENT_CONTROL"}
                    for identity in ("before-native", "after-native")]
        chunks = [(json.dumps(record) + "\n").encode() for record in controls]
        sink = self.write("physical-event-sink", b"".join(chunks))
        native = [{"schema": "native-lifecycle-v1", "run": self.identity["run_id"], "profile": "apache-native",
                   "case": "NEED-cancel", "pid": self.identity["host_pid"], "invalid": False,
                   "function": "native_new", "edge": "return", "result": 1,
                   "monotonic_ns": timestamp, "transaction_id": control["transaction_id"]}
                  for timestamp, control in zip((50, 250), controls)]
        native_ref = self.write("native-controls", b"".join((json.dumps(record) + "\n").encode() for record in native))
        self.packet["observations"]["native_api_returns"]["evidence"] = [{**native_ref, "role": "native_api"}]
        events = self.packet["observations"]["native_events"]
        events["value"]["native_audit_lines"] = []
        events["evidence"] = [{**sink, "role": "physical_event_sink"}]
        return {**self.identity, "execution_observed": True, "window_complete": True,
                "positive_control_observed": True, "sink_sha256": [sink["sha256"]], "sink": sink,
                "observed_from_ns": 90, "observed_through_ns": 210,
                "before_offset": len(chunks[0]), "after_offset": len(chunks[0]),
                "before_control": {"start_offset": 0, "end_offset": len(chunks[0])},
                "after_control": {"start_offset": len(chunks[0]), "end_offset": sum(map(len, chunks))}}

    def bind_observer(self, observer):
        self.bind()
        self.receipt["visible_status_absence"]["event_observer_receipt"] = self.write("event-observer", observer)
        self.review["retest"] = self.write("retest", self.receipt)

    def test_typed_correlated_control_requires_full_lifecycle_but_does_not_promote_report(self):
        self.bind()
        result = self.result()
        self.assertTrue(result["resolved"])
        self.assertIsNone(result["effective_oracle"]["visible_status"])
        self.assertTrue(result["retest"]["visible_status_absence"]["lifecycle_packet"]["full_lifecycle_qualified"])
        self.assertFalse(result["full_lifecycle_qualified"])
        self.assertFalse(result["retest"]["full_lifecycle_qualified"])
        self.raw = b"HTTP/1.1 20"  # An incomplete prefix is not a complete status line.
        self.bind()
        self.result()

    def test_absence_shape_and_native_phase_expectations_remain_strict(self):
        for field, value in (("expected_absence", {"visible_status": "no_complete_http_status_line"}),
                             ("expected_absence", {"visible_status": {"kind": "EOF"}}),
                             ("native_result", None), ("phase", None), ("visible_status", 200)):
            original = copy.deepcopy(self.oracle)
            with self.subTest(field=field, value=value):
                self.oracle[field] = value
                self.bind()
                with self.assertRaises(ValueError):
                    self.result()
            self.oracle.clear()
            self.oracle.update(original)
        del self.oracle["visible_status"]
        self.bind()
        with self.assertRaises(ValueError):
            self.result()

    def test_exact_original_id_mapping_and_separate_source_approval_required(self):
        self.bind()
        for mutation in ("id", "mapping", "root", "contract", "mapping-digest", "protocol", "host", "source-alias", "retest", "old-status"):
            review, row = copy.deepcopy(self.review), copy.deepcopy(self.row)
            approval = review["expected_absence_approval"]
            if mutation == "id":
                row["selected_requirement"]["case_id"] = "NEED-other"
            elif mutation == "mapping":
                row["selected_requirement"]["requirement_mapping"] = []
            elif mutation == "root":
                approval["reviewed_by"] = "worker"
            elif mutation == "contract":
                approval["selected_requirement_sha256"] = "0" * 64
            elif mutation == "mapping-digest":
                approval["requirement_mapping_sha256"] = "0" * 64
            elif mutation in ("protocol", "host"):
                kind = "protocol_contract" if mutation == "protocol" else "official_host_contract"
                approval["proof"] = [p for p in approval["proof"] if p["kind"] != kind]
            elif mutation == "source-alias":
                approval["proof"][1] = {**approval["proof"][0], "kind": "protocol_contract"}
            elif mutation == "retest":
                review.pop("retest")
            else:
                row["selected_requirement"]["expected_oracle"]["visible_status"] = 200
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                LEDGER.review_record(review, row)

    def test_eof_stubs_missing_wait_and_uncorrelated_process_or_host_are_rejected(self):
        original_client, original_host = copy.deepcopy(self.client), copy.deepcopy(self.host)
        for mutation in ("eof", "stub", "wait", "signal", "signal-exit", "pid", "request", "host-run", "host-unobserved", "host-termination", "native"):
            self.client, self.host = copy.deepcopy(original_client), copy.deepcopy(original_host)
            if mutation == "eof":
                self.client["termination_kind"] = "eof"
            elif mutation == "stub":
                self.client["executed_case_contract"] = False
            elif mutation == "wait":
                self.client.pop("actual_waited_exit")
            elif mutation == "signal":
                self.client["actual_waited_signal"] = None
            elif mutation == "signal-exit":
                self.client["actual_waited_exit"] = 0
            elif mutation == "pid":
                self.host["client_pid"] += 1
            elif mutation == "request":
                self.host["request_id"] = "another-request"
            elif mutation == "host-run":
                self.host["run_id"] = "another-run"
            elif mutation == "host-unobserved":
                self.host["execution_observed"] = False
            elif mutation == "host-termination":
                self.host["termination_observed"] = False
            else:
                self.host["native_transaction_id"] = "another-native"
            self.bind()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.result()

    def test_complete_status_and_incomplete_native_or_cleanup_cannot_pass(self):
        for raw in (b"HTTP/1.1 200 OK\r\n", b"HTTP/1.0 500 Error\n", b"HTTP/1.1 100 Continue\r\n"):
            self.raw = raw
            self.bind()
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.result()
        self.raw = b""
        for field in ("native_events", "native_api_returns", "native_transaction_id", "finish_calls", "native_free_calls", "cleanup_receipts"):
            old = copy.deepcopy(self.packet["observations"][field])
            self.packet["observations"][field] = {"value": None, "reason": "Not actually measured"}
            self.bind()
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.result()
            self.packet["observations"][field] = old

    def test_zero_events_and_missing_once_only_lifetime_are_not_absence_evidence(self):
        for field, value in (("native_events", []), ("native_events", 0), ("native_api_returns", []),
                             ("finish_calls", 0), ("finish_calls", {"common_finish": 1, "native_logging": 2}),
                             ("finish_calls", {"common_finish": True, "native_logging": 1}),
                             ("native_free_calls", {"native_cleanup": 1, "common_cleanup": 1, "host_association_retire": 0}),
                             ("native_free_calls", True),
                             ("cleanup_receipts", {})):
            old = copy.deepcopy(self.packet["observations"][field])
            self.packet["observations"][field]["value"] = value
            self.bind()
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.result()
            self.packet["observations"][field] = old

    def test_zero_physical_event_dictionary_requires_correlated_actual_observer(self):
        self.packet["observations"]["native_events"]["value"]["native_audit_lines"] = []
        self.bind()
        with self.assertRaises(KeyError):
            self.result()
        observer = {**self.identity, "execution_observed": True, "window_complete": True,
                    "positive_control_observed": True, "sink_sha256": [self.physical["sha256"]]}
        self.bind_observer(observer)
        with self.assertRaises((KeyError, ValueError)):
            self.result()
        observer = self.zero_event_observer()
        self.bind_observer(observer)
        self.result()
        observer["positive_control_observed"] = False
        self.bind_observer(observer)
        with self.assertRaises(ValueError):
            self.result()

    def test_zero_event_window_rejects_untyped_incomplete_and_nonempty_observations(self):
        for mutation in ("bool-offset", "outside-sink", "new-bytes", "late-start", "early-end", "bool-time",
                         "reversed-client", "missing-client-time", "empty-control", "overlap-control", "other-sink"):
            observer = self.zero_event_observer()
            old_client = copy.deepcopy(self.client)
            if mutation == "bool-offset":
                observer["before_offset"] = True
            elif mutation == "outside-sink":
                observer["before_offset"] = observer["after_offset"] = observer["sink"]["bytes"] + 1
            elif mutation == "new-bytes":
                observer["after_offset"] += 1
            elif mutation == "late-start":
                observer["observed_from_ns"] = 101
            elif mutation == "early-end":
                observer["observed_through_ns"] = 199
            elif mutation == "bool-time":
                observer["observed_from_ns"] = False
            elif mutation == "reversed-client":
                self.client["completed_ns"] = 99
            elif mutation == "missing-client-time":
                self.client.pop("started_ns")
            elif mutation == "empty-control":
                observer["before_control"]["end_offset"] = 0
            elif mutation == "overlap-control":
                observer["before_control"]["end_offset"] += 1
            else:
                observer["sink"] = self.physical
            self.bind_observer(observer)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.result()
            self.client = old_client

    def test_zero_event_controls_require_actual_correlated_successful_native_allocations(self):
        for mutation in ("foreign-id", "wrong-host", "wrong-run", "wrong-case", "wrong-schema", "invalid",
                         "false-result", "failed-allocation", "inside-main", "bool-time", "main-id", "not-native-jsonl"):
            observer = self.zero_event_observer()
            proof = self.packet["observations"]["native_api_returns"]["evidence"][0]
            native = [json.loads(line) for line in Path(proof["path"]).read_text().splitlines()]
            record = native[0]
            if mutation == "foreign-id":
                record["transaction_id"] = "foreign"
            elif mutation == "wrong-host":
                record["pid"] += 1
            elif mutation == "wrong-run":
                record["run"] = "other-run"
            elif mutation == "wrong-case":
                record["case"] = "other-case"
            elif mutation == "wrong-schema":
                record["schema"] = "invented"
            elif mutation == "invalid":
                record["invalid"] = True
            elif mutation == "false-result":
                record["result"] = True
            elif mutation == "failed-allocation":
                record["result"] = 0
            elif mutation == "inside-main":
                record["monotonic_ns"] = 150
            elif mutation == "bool-time":
                record["monotonic_ns"] = False
            elif mutation == "main-id":
                record["transaction_id"] = self.identity["native_transaction_id"]
            else:
                native = ["flag-only"]
            changed = self.write("native-controls", b"".join((json.dumps(row) + "\n").encode() for row in native))
            self.packet["observations"]["native_api_returns"]["evidence"] = [{**changed, "role": "native_api"}]
            self.bind_observer(observer)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                self.result()

    def test_zero_event_observer_rejects_sink_bytes_changed_after_sealing(self):
        observer = self.zero_event_observer()
        self.bind_observer(observer)
        Path(observer["sink"]["path"]).write_bytes(b"replaced sink")
        with self.assertRaises(ValueError):
            self.result()

    def test_uncorrelated_empty_capture_and_client_only_reset_cannot_pass(self):
        self.bind()
        witness = self.receipt["visible_status_absence"]
        self.client["response_capture_sha256"] = "0" * 64
        witness["client_termination_receipt"] = self.write("client-receipt", self.client)
        self.review["retest"] = self.write("retest", self.receipt)
        with self.assertRaises(ValueError):
            self.result()
        self.bind()
        reset = self.packet["observations"]["transport_reset_scope"]
        reset["evidence"] = [p for p in reset["evidence"] if p["role"] == "client_process"]
        self.receipt["visible_status_absence"]["lifecycle_packet"] = self.write("packet", self.packet)
        self.review["retest"] = self.write("retest", self.receipt)
        with self.assertRaises(ValueError):
            self.result()


if __name__ == "__main__":
    unittest.main()
