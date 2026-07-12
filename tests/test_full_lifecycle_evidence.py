from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SANITIZER_SPEC = importlib.util.spec_from_file_location(
    "sanitize_full_lifecycle_log", ROOT / "ci/sanitize-full-lifecycle-log.py"
)
assert SANITIZER_SPEC is not None and SANITIZER_SPEC.loader is not None
sanitizer = importlib.util.module_from_spec(SANITIZER_SPEC)
SANITIZER_SPEC.loader.exec_module(sanitizer)

CHECKER_SPEC = importlib.util.spec_from_file_location(
    "check_full_lifecycle_evidence", ROOT / "ci/check-full-lifecycle-evidence.py"
)
assert CHECKER_SPEC is not None and CHECKER_SPEC.loader is not None
checker = importlib.util.module_from_spec(CHECKER_SPEC)
CHECKER_SPEC.loader.exec_module(checker)


class FullLifecycleEvidenceTest(unittest.TestCase):
    def test_log_sanitizer_drops_fixture_bodies_and_credentials(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-log-") as temporary:
            root = Path(temporary)
            source = root / "raw.log"
            destination = root / "canonical.log"
            source.write_text(
                "Authorization: Bearer private-token\n"
                "response=no-crs-response-body-marker\n"
                "normal diagnostic\n",
                encoding="utf-8",
            )
            self.assertEqual(0, sanitizer.main([
                "--input", str(source), "--output", str(destination), "--label", "unit",
            ]))
            text = destination.read_text(encoding="utf-8")
            self.assertNotIn("private-token", text)
            self.assertNotIn("no-crs-response-body-marker", text)
            self.assertIn("[body payload line omitted]", text)
            self.assertIn("normal diagnostic", text)

    def test_first_byte_promotion_requires_causal_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-evidence-") as temporary:
            root = Path(temporary)
            run = root / "run"
            run.mkdir()
            (run / "events.jsonl").write_text(
                '{"rule_id":1100301,"phase":4,"first_byte_before_response_end":true,'
                '"upstream_response_finished_at_first_byte":false}\n',
                encoding="utf-8",
            )
            (run / "results.jsonl").write_text(
                '{"case_id":"phase4_first_byte_before_response_end","status":"PASS",'
                '"expected_rule_id":1100301}\n'
                '{"case_id":"phase4_no_full_response_buffering","status":"PASS",'
                '"expected_rule_id":1100301}\n',
                encoding="utf-8",
            )
            manifest = {"capabilities": {"first_byte_before_response_end": {"state": "verified"}}}
            result = {"artifact_profile": "full_lifecycle", "capabilities_verified": ["first_byte_before_response_end"]}
            errors = checker.first_byte_errors(run, manifest, result)
            self.assertEqual(
                [
                    "phase4_first_byte_before_response_end: missing synchronized first-byte event metadata",
                    "phase4_no_full_response_buffering: missing synchronized first-byte event metadata",
                ],
                errors,
            )

    def test_profile_contract_rejects_generic_compatibility_evidence(self) -> None:
        compatibility_result = {
            "artifact_profile": "generic",
            "host_profile": "ext_authz",
            "integration_mode": "ext_authz",
            "executed_targets": ["no-crs-baseline-envoy"],
        }
        errors = checker.profile_errors(compatibility_result, "envoy")
        self.assertIn(
            "canonical full-lifecycle evidence requires artifact_profile=full_lifecycle",
            errors,
        )
        self.assertIn(
            "canonical full-lifecycle evidence requires host_profile='ext_proc'",
            errors,
        )
        self.assertIn(
            "canonical full-lifecycle evidence requires integration_mode='ext_proc'",
            errors,
        )
        self.assertIn(
            "canonical full-lifecycle evidence requires executed_targets=['full-lifecycle-envoy-ext-proc']",
            errors,
        )

    def test_profile_contract_accepts_only_each_connector_native_identity(self) -> None:
        for connector, identity in checker.FULL_LIFECYCLE_IDENTITIES.items():
            result = {
                "artifact_profile": "full_lifecycle",
                "host_profile": identity["host_profile"],
                "integration_mode": identity["integration_mode"],
                "executed_targets": [identity["target"]],
            }
            with self.subTest(connector=connector):
                self.assertEqual([], checker.profile_errors(result, connector))

    def test_profile_checker_fails_before_capability_claims_for_generic_evidence(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-profile-") as temporary:
            evidence_root = Path(temporary) / "evidence"
            run_dir = evidence_root / "envoy" / "compatibility-run"
            run_dir.mkdir(parents=True)
            (run_dir / "result.json").write_text(
                '{"artifact_profile":"generic","capabilities_verified":[]}',
                encoding="utf-8",
            )
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(
                    1,
                    checker.main([
                        "--connector-root", str(ROOT),
                        "--evidence-root", str(evidence_root),
                        "--run-id", "compatibility-run",
                        "--check", "profile",
                        "--connectors", "envoy",
                    ]),
                )

    def test_lifecycle_inventory_rejects_unbalanced_or_unattributed_counters(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-lifecycle-") as temporary:
            run = Path(temporary)
            (run / "events.jsonl").write_text(
                '{"transaction_id":"tx-one","actual_action":"abort_connection",'
                '"late_intervention_mode":"strict","transport_result":"connection_aborted"}\n',
                encoding="utf-8",
            )
            (run / "lifecycle-counters.json").write_text(
                '{"connector":"apache","transactions_started":2,"transactions_finished":1,'
                '"transactions_destroyed":1,"request_body_finishes":0,'
                '"response_body_finishes":0,"intentional_aborts":2,'
                '"client_disconnects":0,"upstream_disconnects":0,"stream_resets":0,'
                '"timeouts":0,"short_writes":0,"write_would_block":0,'
                '"cleanup_normal":0,"cleanup_cancel":0,"cleanup_abort":0,'
                '"unexpected_engine_errors":0,"transport_counters_bound":true}',
                encoding="utf-8",
            )
            inventory = run / "inventory"
            inventory.mkdir()
            (inventory / "connection-lifecycle.json").write_text(
                '{"records":[]}', encoding="utf-8"
            )
            errors = checker.lifecycle_errors(run, "apache")
            self.assertTrue(any("unbalanced" in error for error in errors))
            self.assertTrue(any("intentional_aborts" in error for error in errors))

    def test_transport_inventory_rejects_unproven_host_survival(self) -> None:
        with tempfile.TemporaryDirectory(prefix="full-lifecycle-transport-") as temporary:
            run = Path(temporary)
            logs = run / "logs"
            inventory = run / "inventory"
            logs.mkdir()
            inventory.mkdir()
            for name in ("client.log", "upstream.log", "transport.log", "cleanup.log"):
                (logs / name).write_text("payload-free\n", encoding="utf-8")
            (inventory / "transport-observations.json").write_text(
                '{"connector":"apache","run_id":"run-one","observations":['
                '{"protocol":"http1","case_id":"strict-http1","transport_case_id":"case-one",'
                '"transaction_id":"tx-one","rule_id":1100301,"phase":4,"event":"phase4",'
                '"message_id":"MSCONN_EVENT","requested_action":"deny","actual_action":"abort_connection",'
                '"response_committed":true,"first_byte_received":true,"eos_received":false,'
                '"client_result":"not_observable","transport_result":"connection_aborted",'
                '"host_survived":true,"followup_request_result":"not_observed"}]}',
                encoding="utf-8",
            )
            (inventory / "connection-lifecycle.json").write_text(
                '{"connector":"apache","run_id":"run-one","records":[]}',
                encoding="utf-8",
            )
            (inventory / "barrier-events.jsonl").write_text("", encoding="utf-8")
            effective = run / "effective-config"
            effective.mkdir()
            (effective / "manifest.json").write_text(
                '{"connector":"apache","run_id":"run-one","files":[]}',
                encoding="utf-8",
            )
            errors = checker.transport_artifact_errors(run, "apache")
            self.assertIn("host_survived=true requires an independent follow-up observation", errors)


if __name__ == "__main__":
    unittest.main()
