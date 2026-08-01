"""Framework-independent contracts for no-CRS collector helper boundaries."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
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


if __name__ == "__main__":
    unittest.main()
