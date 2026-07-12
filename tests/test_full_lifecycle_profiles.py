from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "resolve_full_lifecycle_profile", ROOT / "ci/resolve-full-lifecycle-profile.py"
)
assert SPEC is not None and SPEC.loader is not None
profiles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profiles)


class FullLifecycleProfilesTest(unittest.TestCase):
    def capability_manifest(self, connector: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "connector": connector,
            "host_name": "compatibility-host",
            "integration_mode": "compatibility-mode",
            "host_model_constraints": [],
            "capabilities": {
                name: {"state": "verified", "reason": "compatibility fixture"}
                for name in (
                    "phase1",
                    "phase2",
                    "phase3",
                    "phase4",
                    "deny",
                    "request_headers",
                    "request_body_buffered",
                    "request_body_incremental_ingest",
                    "response_headers",
                    "response_body_buffered",
                    "response_body_incremental_ingest",
                    "no_full_response_buffering",
                    "first_byte_before_response_end",
                    "transaction_id",
                    "event_jsonl",
                    "transport_metadata",
                    "connection_metadata",
                    "phase4_rule_evaluation",
                    "phase4_end_of_stream_evaluation",
                    "redirect",
                    "log_only",
                    "late_intervention",
                    "late_intervention_log_only",
                    "late_intervention_status_metadata",
                )
            },
            "evidence_stages": {},
        }

    def test_every_connector_has_one_explicit_native_profile(self) -> None:
        self.assertEqual(
            {"apache", "nginx", "haproxy", "envoy", "traefik", "lighttpd"},
            set(profiles.PROFILE_BY_CONNECTOR),
        )
        for connector, profile in profiles.PROFILE_BY_CONNECTOR.items():
            payload = self.capability_manifest(connector)
            result = profiles.effective_manifest(payload, profile)
            self.assertEqual(profile, result["full_lifecycle_profile"])
            self.assertNotEqual("compatibility-mode", result["integration_mode"])

    def test_non_native_profiles_are_conservatively_downgraded(self) -> None:
        expected_phase4 = {
            "haproxy": "implemented_not_asserted",
            "envoy": "implemented_not_asserted",
            "traefik": "implemented_not_asserted",
            "lighttpd": "implemented_not_asserted",
        }
        for connector, phase4_state in expected_phase4.items():
            result = profiles.effective_manifest(
                self.capability_manifest(connector), profiles.PROFILE_BY_CONNECTOR[connector]
            )
            self.assertEqual(
                phase4_state,
                result["capabilities"]["phase4"]["state"],
            )
            self.assertNotEqual("verified", result["capabilities"]["phase1"]["state"])

    def test_common_bridge_profiles_select_only_unpromoted_native_capabilities(self) -> None:
        for connector in ("envoy", "traefik"):
            result = profiles.effective_manifest(
                self.capability_manifest(connector), profiles.PROFILE_BY_CONNECTOR[connector]
            )
            for capability in (
                "request_headers", "request_body_incremental_ingest",
                "response_headers", "response_body_incremental_ingest",
                "phase1", "phase2", "phase3", "phase4",
                "late_intervention_log_only", "event_jsonl",
            ):
                self.assertEqual(
                    "implemented_not_asserted",
                    result["capabilities"][capability]["state"],
                    f"{connector}/{capability}",
                )
            self.assertNotEqual(
                "verified", result["capabilities"]["phase4"]["state"]
            )

    def test_patched_lighttpd_keeps_entity_body_lifecycle_selectable(self) -> None:
        result = profiles.effective_manifest(
            self.capability_manifest("lighttpd"), profiles.PROFILE_BY_CONNECTOR["lighttpd"]
        )
        for capability in (
            "deny", "response_body_buffered", "response_body_incremental_ingest",
            "phase4", "phase4_rule_evaluation", "phase4_end_of_stream_evaluation",
            "late_intervention_log_only", "first_byte_before_response_end",
        ):
            with self.subTest(capability=capability):
                self.assertEqual("implemented_not_asserted", result["capabilities"][capability]["state"])

    def test_wrong_connector_profile_is_rejected_and_write_is_atomic(self) -> None:
        payload = self.capability_manifest("envoy")
        with self.assertRaisesRegex(ValueError, "invalid full-lifecycle profile"):
            profiles.effective_manifest(payload, "native-htx-filter")
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "nested" / "effective.json"
            profiles.write_json_atomically(
                output, profiles.effective_manifest(payload, "ext_proc")
            )
            loaded = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("ext_proc", loaded["full_lifecycle_profile"])


if __name__ == "__main__":
    unittest.main()
