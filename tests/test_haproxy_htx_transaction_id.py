"""Parent-owned regression coverage for HAProxy HTX transaction-ID bounds."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


HELPER_PATH = (
    Path(__file__).resolve().parents[1]
    / "connectors/haproxy/harness/haproxy_htx_smoke_helper.py"
)
SPEC = importlib.util.spec_from_file_location("haproxy_htx_smoke_helper", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class HAProxyHTXTransactionIdTest(unittest.TestCase):
    def test_native_128_byte_buffer_limit_applies_to_allow_and_evidence_writers(self) -> None:
        accepted = "a" * HELPER.HTX_TRANSACTION_ID_MAX_LENGTH
        rejected = "b" * (HELPER.HTX_TRANSACTION_ID_MAX_LENGTH + 1)
        self.assertEqual(HELPER.safe_htx_transaction_id(accepted), accepted)
        with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
            HELPER.safe_htx_transaction_id(rejected)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            events = root / "events.jsonl"
            probe = root / "client-probe.json"
            upstream = root / "upstream-requests.jsonl"
            host_evidence = root / "host-runtime-evidence.jsonl"
            decision_log = root / "haproxy.stderr.log"
            probe.write_text(
                json.dumps({"status": 200, "response_bytes": 24, "content_type": "text/plain"}),
                encoding="utf-8",
            )
            upstream.write_text(
                json.dumps({"profile": "ordinary", "request_id": accepted}) + "\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_allow_event(str(events), str(probe), str(upstream), accepted),
                0,
            )
            self.assertEqual(
                json.loads(events.read_text(encoding="utf-8"))["transaction_id"],
                accepted,
            )
            with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
                HELPER.write_allow_event(str(events), str(probe), str(upstream), rejected)

            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                f"transaction_id={accepted} phase=1 status=403 rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_host_evidence(
                    str(host_evidence), "phase1_403", 1, 1100001, str(probe), 0,
                    "enforced_reply", str(decision_log),
                ),
                0,
            )
            self.assertEqual(
                json.loads(host_evidence.read_text(encoding="utf-8"))["transaction_id"],
                accepted,
            )
            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                f"transaction_id={rejected} phase=1 status=403 rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "invalid HTX transaction id"):
                HELPER.write_host_evidence(
                    str(host_evidence), "phase1_403", 1, 1100001, str(probe), 0,
                    "enforced_reply", str(decision_log),
                )


if __name__ == "__main__":
    unittest.main()
