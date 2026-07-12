#!/usr/bin/env python3
"""Focused tests for the payload-free HAProxy HTX host-runtime helper."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import stat
import tempfile
import unittest


HELPER_PATH = Path(__file__).with_name("haproxy_htx_smoke_helper.py")
SPEC = importlib.util.spec_from_file_location("haproxy_htx_smoke_helper", HELPER_PATH)
assert SPEC is not None and SPEC.loader is not None
HELPER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HELPER)


class HAProxyHTXSmokeHelperTest(unittest.TestCase):
    def test_phase2_upstream_profile_is_isolated_from_ordinary_requests(self) -> None:
        self.assertEqual(
            ("phase2", None, HELPER.UPSTREAM_OK_BODY),
            HELPER.upstream_profile("/no-crs/request-body?trace=ignored"),
        )

    def test_generated_config_selects_only_native_htx_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rules = root / "rules.conf"
            config = root / "haproxy.cfg"
            self.assertEqual(HELPER.write_rules(str(rules)), 0)
            self.assertEqual(HELPER.write_config(str(config), 18080, 18081, str(rules)), 0)
            content = config.read_text(encoding="utf-8")
            self.assertIn("filter modsecurity-htx rules-file", content)
            for forbidden in ("filter spoe", "send-spoe", "http-buffer-request", "wait-for-body", "res.body"):
                self.assertNotIn(forbidden, content)
            generated_rules = rules.read_text(encoding="utf-8")
            self.assertEqual(generated_rules, HELPER.canonical_rules_content())
            for rule_id in (1100001, 1100002, 1100101, 1100201, 1100301):
                self.assertIn(f"id:{rule_id}", generated_rules)
            self.assertNotIn("91000", generated_rules)

    def test_event_contains_only_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            events = Path(temporary) / "events.jsonl"
            decision_log = Path(temporary) / "haproxy.stderr.log"
            decision_log.write_text(
                "modsecurity-htx: request intervention observed; "
                "transaction_id=haproxy-htx-phase1 phase=1 status=403 "
                "rule_id=1100001 action=deny\n",
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_event(
                    str(events),
                    "phase1_403",
                    str(decision_log),
                    1,
                    1100001,
                    403,
                    "enforced_reply",
                ),
                0,
            )
            record = json.loads(events.read_text(encoding="utf-8"))
            self.assertEqual(record["connector"], "haproxy")
            self.assertEqual(record["message_id"], "HAPROXY_HTX_NATIVE_PRECOMMIT_DENY")
            self.assertEqual(record["status"], "blocked")
            self.assertEqual(record["integration_mode"], "native-htx-filter")
            self.assertEqual(record["evaluation_mode"], "native_host_runtime_nonpromoted")
            self.assertEqual(record["actual_action"], "deny")
            self.assertEqual(record["visible_http_status"], 403)
            self.assertFalse(record["headers_sent"])
            self.assertNotIn("body", record)
            self.assertNotIn("headers", record)
            self.assertEqual(stat.S_IMODE(events.stat().st_mode), 0o600)

            probe = Path(temporary) / "client-probe.json"
            host_evidence = Path(temporary) / "host-runtime-evidence.jsonl"
            probe.write_text(
                json.dumps({"status": 403, "response_bytes": 93, "content_type": "text/html"}),
                encoding="utf-8",
            )
            self.assertEqual(
                HELPER.write_host_evidence(
                    str(host_evidence),
                    "phase1_403",
                    1,
                    1100001,
                    str(probe),
                    0,
                    "enforced_reply",
                    str(decision_log),
                ),
                0,
            )
            raw_record = json.loads(host_evidence.read_text(encoding="utf-8"))
            self.assertEqual(raw_record["upstream_requests"], 0)
            self.assertEqual(raw_record["client_response_bytes"], 93)
            self.assertNotIn("no-crs-request-body-marker", host_evidence.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
