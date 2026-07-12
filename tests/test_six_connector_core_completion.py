from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "six_connector_core_completion",
    ROOT / "ci" / "check-six-connector-core-completion.py",
)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class SixConnectorCoreCompletionTest(unittest.TestCase):
    def test_safe_event_requires_real_post_commit_log_only_semantics(self) -> None:
        event = {
            "requested_action": "deny",
            "actual_action": "log_only",
            "late_intervention": True,
            "late_intervention_mode": "safe",
            "headers_sent": True,
            "body_started": True,
            "response_committed": True,
            "connection_aborted": False,
            "http_status": 403,
            "original_http_status": 200,
            "visible_http_status": 200,
            "transport_result": "log_only",
        }
        self.assertTrue(checker.safe_event(event))
        event["visible_http_status"] = 403
        self.assertFalse(checker.safe_event(event))

    def test_barrier_event_requires_upstream_pause_and_no_buffer_when_requested(self) -> None:
        event = {
            "client_first_byte_received": True,
            "first_byte_before_response_end": True,
            "upstream_paused": True,
            "upstream_eos_sent_at_first_byte": False,
            "upstream_response_finished_at_first_byte": False,
            "response_committed": True,
            "first_chunk_size": 1,
            "no_full_response_buffering": True,
        }
        self.assertTrue(checker.barrier_event(event, require_no_buffer=True))
        event["no_full_response_buffering"] = False
        self.assertFalse(checker.barrier_event(event, require_no_buffer=True))
        self.assertTrue(checker.barrier_event(event, require_no_buffer=False))


if __name__ == "__main__":
    unittest.main()
