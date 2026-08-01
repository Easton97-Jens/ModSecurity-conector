"""Framework-independent contracts for no-CRS collector helper boundaries."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
CI_LIB = ROOT / "ci" / "lib"
if str(CI_LIB) not in sys.path:
    sys.path.insert(0, str(CI_LIB))


def load_collector() -> object:
    specification = importlib.util.spec_from_file_location(
        "collect_no_crs_source_helpers",
        ROOT / "ci/runtime/lifecycle/collect-no-crs-source.py",
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


COLLECTOR = load_collector()


class CollectNoCrsSourceHelpersTest(unittest.TestCase):
    def test_metadata_dispatch_retains_allow_lists_and_scalar_rejection(self) -> None:
        self.assertEqual(
            COLLECTOR.safe_metadata_value("actual_action", "connection_abort"),
            "abort_connection",
        )
        self.assertEqual(
            COLLECTOR.safe_metadata_value("requested_protocol", "http2"), "h2"
        )
        self.assertEqual(
            COLLECTOR.safe_metadata_value("transport_case_id", "case-1"), "case-1"
        )
        self.assertIsNone(COLLECTOR.safe_metadata_value("actual_action", True))
        self.assertIsNone(
            COLLECTOR.safe_metadata_value("late_intervention_mode", "late-403")
        )
        self.assertIsNone(
            COLLECTOR.safe_metadata_value("transport_case_id", "../outside")
        )

    def test_first_byte_record_requires_real_host_contract_and_normalizes_counters(self) -> None:
        record = {
            "evidence_type": "synchronized_first_byte",
            "evidence_origin": "real_host",
            "promotion_eligible": True,
            "outcome": "PASS",
            "body_payload_persisted": False,
            "client_first_byte_received": True,
            "first_byte_before_response_end": True,
            "first_chunk_size": "7",
            "upstream_paused": True,
            "upstream_eos_sent_at_first_byte": False,
            "upstream_response_finished_at_first_byte": False,
            "response_committed": True,
            "body_bytes_seen": "11",
            "body_bytes_inspected": 7,
            "no_full_response_buffering": True,
            "connector_owned_full_response_buffer": False,
        }

        self.assertTrue(COLLECTOR.first_byte_evidence_identity_is_valid(record))
        self.assertTrue(COLLECTOR.first_byte_evidence_contract_is_valid(record))
        self.assertTrue(COLLECTOR.normalize_first_byte_counters(record))
        self.assertEqual(record["first_chunk_size"], 7)
        self.assertEqual(record["body_bytes_seen"], 11)

        record["body_bytes_inspected"] = 12
        self.assertFalse(COLLECTOR.normalize_first_byte_counters(record))

    def test_event_evidence_rejects_hidden_payload_and_preserves_valid_metadata(self) -> None:
        valid = {
            "connector": "apache",
            "transaction_id": "tx-1",
            "rule_id": 1100001,
            "phase": 1,
            "status": "blocked",
        }
        hidden_payload = {**valid, "nested": {"body": "secret-payload"}}

        clean_result = COLLECTOR.event_evidence([], "1100001", [valid])
        result = COLLECTOR.event_evidence([], "1100001", [valid, hidden_payload])

        self.assertTrue(clean_result["event_metadata_verified"])
        self.assertFalse(result["event_metadata_verified"])
        self.assertFalse(result["body_payload_absent_from_events"])
        self.assertEqual(result["event_records"], 1)
        self.assertIn("nested", " ".join(result["forbidden_event_keys"]))

    def test_case_pass_requires_selected_rule_and_phase(self) -> None:
        record = {"phase": 4, "rule_id": 1100301}
        self.assertTrue(
            COLLECTOR.case_passes(
                "PASS", True, 200, 200, "1100301", 4,
                "phase4_deny_after_commit_log_only", {"1100301"}, [record],
            )
        )
        self.assertFalse(
            COLLECTOR.case_passes(
                "PASS", True, 200, 200, "1100301", 4,
                "phase4_deny_after_commit_log_only", {"1100301"}, [],
            )
        )

    def test_case_observations_retain_transaction_binding(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-helper-transaction-") as temporary:
            root = Path(temporary)
            decision_path = root / "decision.jsonl"
            decision_path.write_text(
                "\n".join(
                    json.dumps(event)
                    for event in (
                        {
                            "connector": "apache",
                            "transaction_id": "tx-current",
                            "rule_id": 1100201,
                            "phase": "response_headers",
                            "status": "blocked",
                            "headers_sent": False,
                        },
                        {
                            "connector": "apache",
                            "transaction_id": "tx-other",
                            "rule_id": 1100201,
                            "phase": "response_headers",
                            "status": "blocked",
                            "headers_sent": True,
                        },
                    )
                )
                + "\n",
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase3_deny_before_commit",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 403,
                        "transaction_id": "tx-current",
                        "decision_log_path": str(decision_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            cases, events = COLLECTOR.case_observations(
                [results_path],
                "apache",
                "1100001",
                {"phase3_deny_before_commit": (403, "1100201", 3)},
                allowed_source_root=root,
            )

        self.assertEqual(cases[0]["status"], "PASS")
        self.assertEqual(cases[0]["transaction_ids"], ["tx-current"])
        self.assertFalse(cases[0]["headers_sent"])
        self.assertEqual(len(events), 1)

    def test_phase4_audit_fallback_remains_forbidden(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-helper-phase4-") as temporary:
            root = Path(temporary)
            audit_path = root / "audit.log"
            audit_path.write_text(
                '[id "1100301"] (phase 4) [unique_id "tx-audit"]\n',
                encoding="utf-8",
            )
            results_path = root / "results.jsonl"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "phase4_rule_observed",
                        "status": "PASS",
                        "live_executed": True,
                        "actual_status": 200,
                        "audit_log_path": str(audit_path),
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            cases, events = COLLECTOR.case_observations(
                [results_path],
                "apache",
                "1100001",
                {"phase4_rule_observed": (None, "1100301", 4)},
                allowed_source_root=root,
            )

        self.assertEqual(events, [])
        self.assertEqual(cases[0]["status"], "FAIL")
        self.assertFalse(cases[0]["event_metadata_verified"])

    def test_collector_status_preserves_terminal_precedence(self) -> None:
        events = {
            "event_metadata_verified": True,
            "body_payload_absent_from_events": True,
        }
        self.assertEqual(
            COLLECTOR.collector_status(
                77, False, False, [], True, "1100001", ["1100001"], events
            ),
            "BLOCKED",
        )
        self.assertEqual(
            COLLECTOR.collector_status(
                77, True, False, [], True, "1100001", ["1100001"], events
            ),
            "FAIL",
        )
        self.assertEqual(
            COLLECTOR.collector_status(
                0,
                False,
                True,
                [],
                True,
                "1100001",
                ["1100001"],
                events,
            ),
            "NOT_EXECUTED",
        )
        self.assertEqual(
            COLLECTOR.collector_status(
                0,
                True,
                False,
                [],
                True,
                "1100001",
                ["1100001"],
                events,
            ),
            "PASS",
        )

    def test_core_response_statuses_keep_case_evidence_precedence(self) -> None:
        allowed, blocked = COLLECTOR.core_response_statuses(
            [
                {
                    "allowed_request_status": 201,
                    "baseline_status": 200,
                    "blocked_request_status": 401,
                    "block_status": 403,
                }
            ],
            [
                {"case_id": "allow_without_marker", "actual_status": 200},
                {"case_id": "deny_header_marker_403", "actual_status": 403},
            ],
        )

        self.assertEqual((allowed, blocked), (200, 403))

    def test_scrub_uses_no_follow_artifact_removal_and_log_writer(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-helper-scrub-") as temporary:
            root = Path(temporary)
            event = root / "decision.jsonl"
            event.write_text('{"transaction_id":"tx-one"}\n', encoding="utf-8")
            log = root / "logs" / "scrub.log"
            removed = COLLECTOR.scrub_source_event_paths([event], root, log)

            self.assertEqual(removed, [event])
            self.assertFalse(event.exists())
            self.assertEqual(
                log.read_text(encoding="utf-8"),
                f"removed_after_allowlist_normalization={event}\n",
            )

    def test_scrub_rejects_final_symlink_without_touching_target(self) -> None:
        with tempfile.TemporaryDirectory(prefix="no-crs-helper-scrub-") as temporary:
            root = Path(temporary)
            target = root / "target.jsonl"
            target.write_text("unchanged\n", encoding="utf-8")
            event = root / "decision.jsonl"
            event.symlink_to(target)

            with self.assertRaisesRegex(ValueError, "contains a symlink"):
                COLLECTOR.scrub_source_event_paths([event], root)
            self.assertEqual(target.read_text(encoding="utf-8"), "unchanged\n")


if __name__ == "__main__":
    unittest.main()
