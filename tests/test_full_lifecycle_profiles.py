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
                    "request_headers",
                    "request_body_incremental_ingest",
                    "response_headers",
                    "response_body_incremental_ingest",
                    "no_full_response_buffering",
                    "transaction_id",
                    "event_jsonl",
                    "transport_metadata",
                    "connection_metadata",
                    "phase4_rule_evaluation",
                    "phase4_end_of_stream_evaluation",
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
        for connector in ("haproxy", "envoy", "traefik", "lighttpd"):
            result = profiles.effective_manifest(
                self.capability_manifest(connector), profiles.PROFILE_BY_CONNECTOR[connector]
            )
            self.assertEqual(
                "implemented_not_asserted" if connector == "haproxy" else "not_implemented",
                result["capabilities"]["phase4"]["state"],
            )
            self.assertNotEqual("verified", result["capabilities"]["phase1"]["state"])

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
