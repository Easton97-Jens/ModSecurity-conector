#!/usr/bin/env python3
"""Focused tests for the payload-free HAProxy HTX smoke helper."""

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
    def test_generated_config_selects_only_native_htx_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rules = root / "rules.conf"
            config = root / "haproxy.cfg"
            self.assertEqual(HELPER.write_rules(str(rules), "phase4"), 0)
            self.assertEqual(HELPER.write_config(str(config), 18080, 18081, str(rules)), 0)
            content = config.read_text(encoding="utf-8")
            self.assertIn("filter modsecurity-htx rules-file", content)
            for forbidden in ("filter spoe", "send-spoe", "http-buffer-request", "wait-for-body", "res.body"):
                self.assertNotIn(forbidden, content)

    def test_event_contains_only_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            events = Path(temporary) / "events.jsonl"
            self.assertEqual(
                HELPER.write_event(
                    str(events),
                    "phase4",
                    "haproxy-htx-phase4",
                    4,
                    910004,
                    200,
                    "not_attempted",
                ),
                0,
            )
            record = json.loads(events.read_text(encoding="utf-8"))
            self.assertEqual(record["connector"], "haproxy")
            self.assertEqual(record["message_id"], "HAPROXY_HTX_OBSERVED_INTERVENTION")
            self.assertEqual(record["status"], "not_attempted")
            self.assertEqual(record["integration_mode"], "native_htx_filter")
            self.assertEqual(record["evaluation_mode"], "observer_nonpromoted")
            self.assertFalse(record["payload_recorded"])
            self.assertNotIn("body", record)
            self.assertNotIn("headers", record)
            self.assertEqual(stat.S_IMODE(events.stat().st_mode), 0o600)


if __name__ == "__main__":
    unittest.main()
