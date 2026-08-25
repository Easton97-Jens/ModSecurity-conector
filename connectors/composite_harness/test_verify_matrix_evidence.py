import json
import os
import tempfile
import unittest
from pathlib import Path

from connectors.composite_harness.verify_matrix_evidence import (
    MAX_EVENT_LINE_BYTES,
    EvidenceError,
    verify_manifest,
)
from connectors.traefik.harness.traefik_composite_upstream import response_header_delay_seconds


DECISION = "a" * 64
EVENT_TIME = "2026-08-24T17:00:00Z"
PIPELINES = {
    "envoy": {
        "request_path": "envoy.ext_authz",
        "response_path": "envoy.ext_proc",
        "transport": "envoy_ext_authz_ext_proc_grpc",
    },
    "traefik": {
        "request_path": "traefik.forwardAuth",
        "response_path": "traefik.native_uds",
        "transport": "traefik_forwardauth_private_uds",
    },
}
CASE_RULE_IDS = {
    ("p1_deny", "P1"): "1101001",
    ("p2_deny", "P2"): "1102001",
    ("p3_deny", "P3"): "1103001",
    ("p4_safe", "P4"): "1104002",
}


class CompositeEvidenceVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    @staticmethod
    def pipeline_fields(connector):
        return dict(PIPELINES[connector])

    def write_case(self, *, case="p4_safe", connector="envoy", mutate=None, strict_observation=False):
        directory = Path(self.tempdir.name)
        directory.chmod(0o700)
        phases = {
            "p1_allow": ["P1", "P2", "P3", "P4"],
            "p1_deny": ["P1"],
            "p2_allow": ["P1", "P2", "P3", "P4"],
            "p2_deny": ["P1", "P2"],
            "p2_oversize": ["P1", "P2"],
            "p3_deny": ["P1", "P2", "P3"],
            "p3_redirect": ["P1", "P2", "P3"],
            "p4_safe": ["P1", "P2", "P3", "P4"],
            "p4_strict": ["P1", "P2", "P3", "P4"],
            "metadata_omitted": [],
            "p2_to_p3_timeout": ["P1", "P2"],
        }[case]
        events = []
        for phase in phases:
            if case == "p1_deny" or (case == "p2_deny" and phase == "P2"):
                action = "deny"
            else:
                action = "allow" if phase in {"P1", "P2"} else "deny"
            status = 200 if action == "allow" else 403
            if case == "p2_oversize" and phase == "P2":
                action, status = "deny", 413
            if case == "p3_redirect" and phase == "P3":
                action, status = "redirect", 302
            events.append({
                "decision_id": DECISION,
                "connector": connector,
                "phase": phase,
                "outcome": "observed",
                "requested_action": action,
                "visible_status": status,
                "event_time": EVENT_TIME,
                **self.pipeline_fields(connector),
            })
            rule_id = CASE_RULE_IDS.get((case, phase))
            if rule_id is not None:
                events[-1]["rule_id"] = rule_id
        if case != "metadata_omitted":
            events.insert(len(events), {
                "decision_id": DECISION,
                "connector": connector,
                "phase": "lease",
                "outcome": "issued",
                "event_time": EVENT_TIME,
                **self.pipeline_fields(connector),
            })
        else:
            events.insert(0, {
                "decision_id": DECISION,
                "connector": connector,
                "phase": "reservation",
                "outcome": "reserved",
                "event_time": EVENT_TIME,
                **self.pipeline_fields(connector),
            })
        host_action = None
        host_status = None
        if case == "p4_safe":
            host_action, host_status = "log_only", 200
        elif case in {"p1_deny", "p2_deny", "p3_deny"}:
            host_action, host_status = "deny", 403
        elif case == "p3_redirect":
            host_action, host_status = "redirect", 302
        elif case == "p2_oversize":
            host_action, host_status = "deny", 413
        if host_action is not None:
            events.insert(len(events), {
                "decision_id": DECISION,
                "connector": connector,
                "phase": "host_action" if case == "p4_safe" else "request_host_action",
                "outcome": "recorded",
                "actual_host_action": host_action,
                "visible_status": host_status,
                "event_time": EVENT_TIME,
                **self.pipeline_fields(connector),
            })
        terminal_event = {
            "decision_id": DECISION,
            "connector": connector,
            "phase": "terminal",
            "outcome": "closed",
            "cleanup_outcome": "closed",
            "event_time": EVENT_TIME,
            **self.pipeline_fields(connector),
        }
        if case == "p2_to_p3_timeout":
            terminal_event["reason"] = "timeout"
        if case == "metadata_omitted":
            terminal_event["reason"] = "disconnect"
        events.insert(len(events), terminal_event)
        if mutate:
            mutate(events)
        event_log = directory / "case-001.events.jsonl"
        event_log.write_text("".join(json.dumps(event) + "\n" for event in events), encoding="utf-8")
        event_log.chmod(0o600)
        client_outcome = "none"
        client_status = 503 if case in {"metadata_omitted", "p2_to_p3_timeout"} else 200
        committed = case not in {"metadata_omitted", "p2_to_p3_timeout"}
        if case == "p4_strict" and strict_observation:
            client_outcome, client_status, committed = "abort", None, False
        client_observation = directory / "client.observation.json"
        client_observation.write_text(json.dumps({
            "lease_observed": False,
            "visible_status": 503 if case in {"metadata_omitted", "p2_to_p3_timeout"} else (413 if case == "p2_oversize" else (302 if case == "p3_redirect" else (403 if case in {"p1_deny", "p2_deny", "p3_deny"} else 200))),
            "p4_outcome": client_outcome,
            "p4_visible_status": client_status,
            "p4_response_committed": committed,
        }), encoding="utf-8")
        client_observation.chmod(0o600)
        upstream_observation = directory / "upstream.observation.json"
        upstream_observation.write_text(json.dumps({
            "lease_observed": False,
            "request_terminal": case in {"p1_deny", "p2_deny", "p2_oversize"},
            "response_observed": case in {
                "p1_allow", "p2_allow", "p3_deny", "p3_redirect", "p4_safe",
                "p4_strict", "p2_to_p3_timeout",
            },
        }), encoding="utf-8")
        upstream_observation.chmod(0o600)
        manifest = {
            "schema": "msc-composite-evidence/v1",
            "connector": connector,
            "case": case,
            "case_artifact": {"id": "case-001", "event_log": event_log.name},
            "expected_phases": phases,
            "client_observation": client_observation.name,
            "upstream_observation": upstream_observation.name,
            "cleanup": {"count": 1, "status": "completed"},
        }
        manifest_path = directory / "case-001.manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        manifest_path.chmod(0o600)
        return manifest_path

    def test_real_observer_schema_passes_with_lifecycle_records(self):
        result = verify_manifest(self.write_case())
        self.assertTrue(result.passed)
        self.assertEqual(result.status, "LIFECYCLE_ONLY")
        self.assertTrue(result.lifecycle_verified)
        self.assertFalse(result.catalog_acceptance)
        self.assertEqual(result.phases, ("P1", "P2", "P3", "P4"))

    def test_explicit_private_runtime_root_is_bound_to_direct_children(self):
        manifest = self.write_case()
        self.assertTrue(verify_manifest(manifest, runtime_root=manifest.parent).passed)
        with self.assertRaisesRegex(EvidenceError, "direct child"):
            verify_manifest(manifest, runtime_root=manifest.parent.parent)

    def test_private_runtime_root_rejects_unsafe_modes(self):
        manifest = self.write_case()
        manifest.parent.chmod(0o755)
        with self.assertRaisesRegex(EvidenceError, "0700"):
            verify_manifest(manifest)

        manifest = self.write_case()
        manifest.chmod(0o644)
        with self.assertRaisesRegex(EvidenceError, "0600"):
            verify_manifest(manifest)

    def test_private_runtime_root_rejects_hardlinks(self):
        manifest = self.write_case()
        duplicate = manifest.parent / "manifest-hardlink.json"
        try:
            os.link(manifest, duplicate)
        except OSError:
            self.skipTest("hard links unavailable")
        with self.assertRaisesRegex(EvidenceError, "hard links"):
            verify_manifest(manifest)

    def test_private_runtime_root_rejects_symlink_and_traversal_leaves(self):
        manifest = self.write_case()
        outside = Path(self.tempdir.name).parent / "outside-event-log.jsonl"
        outside.write_text((manifest.parent / "case-001.events.jsonl").read_text(), encoding="utf-8")
        outside.chmod(0o600)
        event_log = manifest.parent / "case-001.events.jsonl"
        event_log.unlink()
        try:
            os.symlink(outside, event_log)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(EvidenceError, "regular file|symlink"):
            verify_manifest(manifest)

        manifest = self.write_case()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["client_observation"] = "../outside-event-log.jsonl"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "relative basename"):
            verify_manifest(manifest)

    def test_event_line_limit_includes_crlf_terminator(self):
        manifest = self.write_case()
        event_log = manifest.parent / "case-001.events.jsonl"
        event_log.write_bytes(b"{}" + b" " * (MAX_EVENT_LINE_BYTES - 3) + b"\r\n")
        event_log.chmod(0o600)
        with self.assertRaisesRegex(EvidenceError, "exceeds metadata bounds"):
            verify_manifest(manifest)

    def test_strict_requires_actual_client_abort_or_reset_observation(self):
        result = verify_manifest(self.write_case(case="p4_strict"))
        self.assertEqual(result.status, "NON_PASS")
        result = verify_manifest(self.write_case(case="p4_strict", strict_observation=True))
        self.assertEqual(result.status, "NON_PASS")

    def test_metadata_omitted_requires_pre_admission_reservation_and_cleanup(self):
        result = verify_manifest(self.write_case(case="metadata_omitted"))
        self.assertEqual(result.status, "LIFECYCLE_ONLY")
        self.assertEqual(result.phases, ())

        def remove_reservation(events):
            events.pop(0)

        with self.assertRaisesRegex(EvidenceError, "pre-admission reservation"):
            verify_manifest(self.write_case(case="metadata_omitted", mutate=remove_reservation))

    def test_p2_to_p3_timeout_requires_upstream_observation_and_timeout_cleanup(self):
        result = verify_manifest(self.write_case(case="p2_to_p3_timeout"))
        self.assertEqual(result.status, "LIFECYCLE_ONLY")
        self.assertEqual(result.phases, ("P1", "P2"))

        def fabricate_p3(events):
            events.insert(2, {
                "decision_id": DECISION, "connector": "envoy", "phase": "P3",
                "outcome": "observed", "event_time": EVENT_TIME,
                **self.pipeline_fields("envoy"),
            })

        with self.assertRaisesRegex(EvidenceError, "out of order"):
            verify_manifest(self.write_case(case="p2_to_p3_timeout", mutate=fabricate_p3))

        manifest = self.write_case(case="p2_to_p3_timeout")
        upstream = manifest.parent / "upstream.observation.json"
        data = json.loads(upstream.read_text(encoding="utf-8"))
        data["response_observed"] = False
        upstream.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "upstream request observation"):
            verify_manifest(manifest)

        manifest = self.write_case(case="p2_to_p3_timeout")
        event_log = manifest.parent / "case-001.events.jsonl"
        events = [json.loads(line) for line in event_log.read_text(encoding="utf-8").splitlines()]
        events[-1]["reason"] = "other"
        event_log.write_text(
            "".join(json.dumps(event) + "\n" for event in events), encoding="utf-8"
        )
        with self.assertRaisesRegex(EvidenceError, "timeout cleanup"):
            verify_manifest(manifest)

    def test_timeout_header_delay_is_selected_only_by_exact_runtime_root(self):
        self.assertEqual(response_header_delay_seconds(Path("/tmp/p2_to_p3_timeout")), 6.0)
        self.assertEqual(response_header_delay_seconds(Path("/tmp/run-p2_to_p3_timeout")), 6.0)
        self.assertEqual(response_header_delay_seconds(Path("/tmp/p2_to_p3_timeout-extra")), 0.0)
        self.assertEqual(response_header_delay_seconds(Path("/tmp/run-p2_to_p3_timeout-extra")), 0.0)

    def test_rejects_unknown_body_and_lease_fields_in_raw_observer_log(self):
        def add_body(events):
            events[0]["request_body"] = "forbidden"

        with self.assertRaisesRegex(EvidenceError, "forbidden payload field"):
            verify_manifest(self.write_case(mutate=add_body))

        def add_lease(events):
            events[0]["lease"] = "forbidden"

        with self.assertRaisesRegex(EvidenceError, "forbidden payload field"):
            verify_manifest(self.write_case(mutate=add_lease))

    def test_rejects_lease_exposure_in_separate_client_observation(self):
        manifest = self.write_case()
        observation = manifest.parent / "client.observation.json"
        data = json.loads(observation.read_text(encoding="utf-8"))
        data["lease_observed"] = True
        observation.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "lease observed"):
            verify_manifest(manifest)

    def test_rejects_inline_observation_assertions_and_unsafe_paths(self):
        manifest = self.write_case()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["observations"] = {"client": {"lease_observed": False}}
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "unknown field|forbidden"):
            verify_manifest(manifest)

        manifest = self.write_case()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["client_observation"] = "../client.observation.json"
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "relative basename"):
            verify_manifest(manifest)

    def test_rejects_symlinked_observation_file(self):
        manifest = self.write_case()
        observation = manifest.parent / "client.observation.json"
        target = manifest.parent / "client.observation.target.json"
        target.write_text(observation.read_text(encoding="utf-8"), encoding="utf-8")
        observation.unlink()
        try:
            os.symlink(target, observation)
        except OSError:
            self.skipTest("symlinks unavailable")
        with self.assertRaisesRegex(EvidenceError, "non-symlink"):
            verify_manifest(manifest)

    def test_allow_cases_require_raw_allow_upstream_response_and_no_termination(self):
        for case in ("p1_allow", "p2_allow"):
            with self.subTest(case=case):
                self.assertTrue(verify_manifest(self.write_case(case=case)).passed)

                def deny(events):
                    events[0]["requested_action"] = "deny"

                with self.assertRaisesRegex(EvidenceError, "allow"):
                    verify_manifest(self.write_case(case=case, mutate=deny))

                def request_action(events):
                    events.insert(1, {
                        "decision_id": DECISION, "connector": "envoy", "phase": "request_host_action",
                        "outcome": "recorded", "actual_host_action": "deny", "visible_status": 403,
                        "event_time": EVENT_TIME, **self.pipeline_fields("envoy"),
                    })

                with self.assertRaisesRegex(EvidenceError, "request_host_action"):
                    verify_manifest(self.write_case(case=case, mutate=request_action))

    def test_allow_controls_require_response_lifecycle_on_the_same_receipt(self):
        manifest = self.write_case(case="p1_allow")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["expected_phases"] = ["P1", "P2"]
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "exactly match"):
            verify_manifest(manifest)

    def test_expected_event_log_option_requires_exact_absolute_regular_path(self):
        manifest = self.write_case()
        event_log = manifest.parent / "case-001.events.jsonl"
        self.assertTrue(verify_manifest(manifest, event_log).passed)

        other = manifest.parent / "other.events.jsonl"
        other.write_text(event_log.read_text(encoding="utf-8"), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "does not match"):
            verify_manifest(manifest, other)

        with self.assertRaisesRegex(EvidenceError, "absolute"):
            verify_manifest(manifest, "case-001.events.jsonl")

    def test_rejects_cross_connector_decision_or_phase_mismatch(self):
        def cross_connector(events):
            events[2]["connector"] = "traefik"

        with self.assertRaisesRegex(EvidenceError, "connector"):
            verify_manifest(self.write_case(mutate=cross_connector))

        def cross_decision(events):
            events[-1]["decision_id"] = "b" * 64

        with self.assertRaisesRegex(EvidenceError, "exactly one"):
            verify_manifest(self.write_case(mutate=cross_decision))

        def reorder(events):
            events[0]["phase"], events[1]["phase"] = events[1]["phase"], events[0]["phase"]

        with self.assertRaisesRegex(EvidenceError, "order"):
            verify_manifest(self.write_case(case="p2_allow", mutate=reorder))

    def test_requires_exactly_one_terminal_cleanup(self):
        def add_terminal(events):
            events.append(dict(events[-1]))

        with self.assertRaisesRegex(EvidenceError, "terminal cleanup"):
            verify_manifest(self.write_case(mutate=add_terminal))

        def append_after_terminal(events):
            events.append({
                "decision_id": DECISION, "connector": "envoy", "phase": "neutral_outcome",
                "outcome": "allow", "event_time": EVENT_TIME, **self.pipeline_fields("envoy"),
            })

        with self.assertRaisesRegex(EvidenceError, "final observer event"):
            verify_manifest(self.write_case(mutate=append_after_terminal))

    def test_p4_safe_requires_raw_log_only_action(self):
        def remove_log_only(events):
            events[:] = [event for event in events if event.get("actual_host_action") != "log_only"]

        with self.assertRaisesRegex(EvidenceError, "log_only"):
            verify_manifest(self.write_case(mutate=remove_log_only))

    def test_requires_connector_pipeline_metadata_and_selected_rule_id(self):
        def missing_pipeline(events):
            del events[0]["transport"]

        with self.assertRaisesRegex(EvidenceError, "missing required"):
            verify_manifest(self.write_case(mutate=missing_pipeline))

        def wrong_rule(events):
            for event in events:
                if event.get("phase") == "P4":
                    event["rule_id"] = "9999999"

        with self.assertRaisesRegex(EvidenceError, "p4_safe.*rule_id=1104002"):
            verify_manifest(self.write_case(mutate=wrong_rule))

    def test_p3_deny_rejects_incorrect_raw_outcome(self):
        def replace_deny(events):
            for event in events:
                if event.get("phase") == "request_host_action":
                    event["actual_host_action"] = "allow"

        with self.assertRaisesRegex(EvidenceError, "p3_deny"):
            verify_manifest(self.write_case(case="p3_deny", mutate=replace_deny))

    def test_p1_deny_requires_matching_request_side_deny(self):
        self.assertTrue(verify_manifest(self.write_case(case="p1_deny")).passed)

        def replace_deny(events):
            for event in events:
                if event.get("phase") == "request_host_action":
                    event["actual_host_action"] = "allow"

        with self.assertRaisesRegex(EvidenceError, "p1_deny"):
            verify_manifest(self.write_case(case="p1_deny", mutate=replace_deny))

    def test_p2_deny_requires_matching_request_side_deny(self):
        self.assertTrue(verify_manifest(self.write_case(case="p2_deny")).passed)

        def replace_deny(events):
            for event in events:
                if event.get("phase") == "request_host_action":
                    event["actual_host_action"] = "allow"

        with self.assertRaisesRegex(EvidenceError, "p2_deny"):
            verify_manifest(self.write_case(case="p2_deny", mutate=replace_deny))

    def test_phase_actions_and_response_observation_cannot_be_relabeled(self):
        def incorrect_p1(events):
            events[0]["requested_action"] = "allow"

        with self.assertRaisesRegex(EvidenceError, "p1_deny.*P1"):
            verify_manifest(self.write_case(case="p1_deny", mutate=incorrect_p1))

        def incorrect_p3(events):
            for event in events:
                if event.get("phase") == "P3":
                    event["requested_action"] = "allow"

        with self.assertRaisesRegex(EvidenceError, "p3_deny.*P3"):
            verify_manifest(self.write_case(case="p3_deny", mutate=incorrect_p3))

        manifest = self.write_case(case="p3_redirect")
        upstream = manifest.parent / "upstream.observation.json"
        data = json.loads(upstream.read_text(encoding="utf-8"))
        data["response_observed"] = False
        upstream.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(EvidenceError, "upstream response observation"):
            verify_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
