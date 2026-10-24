"""Regression checks for the common remote-rule deny policy.

This test is deliberately source-level: it proves that configuration rejection
and the host-specific directive handlers occur before any libmodsecurity remote
API call.  It does not make a network request.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY_ERROR = "remote rule loading is disabled by security policy"


class RemoteRulesDisabledTest(unittest.TestCase):
    def test_common_config_and_loader_reject_both_remote_pair_shapes(self) -> None:
        config = (ROOT / "common/src/config.c").read_text(encoding="utf-8")
        loader = (ROOT / "common/src/rule_loader.c").read_text(encoding="utf-8")
        merge = (ROOT / "common/src/rule_merge.c").read_text(encoding="utf-8")

        self.assertIn('if (remote_pair_requested(config))', config)
        self.assertIn(POLICY_ERROR, config)
        self.assertIn('if (remote_pair_requested(config))', loader)
        self.assertIn(POLICY_ERROR, loader)
        self.assertIn('return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY', loader)
        self.assertNotIn('backend.add_remote(loader->backend.userdata', loader)
        self.assertIn('remote_pair_requested(config->rules_remote_key, config->rules_remote_url)', merge)
        self.assertIn('remote_pair_requested(parent->rules_remote_key, parent->rules_remote_url)', merge)
        self.assertNotIn('remote_pair_complete(', merge)

    def test_common_runtime_has_no_remote_libmodsecurity_sink(self) -> None:
        runtime = (ROOT / "common/runtime/msconnector_runtime.c").read_text(
            encoding="utf-8"
        )

        self.assertIn(POLICY_ERROR, runtime)
        self.assertNotIn("msc_rules_add_remote", runtime)
        self.assertNotIn("rule_backend.add_remote", runtime)

    def test_apache_and_nginx_directives_fail_before_native_conversion(self) -> None:
        apache = (ROOT / "connectors/apache/src/msc_config.c").read_text(
            encoding="utf-8"
        )
        nginx = (
            ROOT / "connectors/nginx/src/ngx_http_modsecurity_module.c"
        ).read_text(encoding="utf-8")

        self.assertIn(POLICY_ERROR, apache)
        self.assertIn(POLICY_ERROR, nginx)
        self.assertNotIn("msc_rules_add_remote", apache)
        self.assertNotIn("msc_rules_add_remote", nginx)
        remote_handler = re.search(
            r"ngx_conf_set_rules_remote\([^}]+\}", nginx, re.DOTALL
        )
        self.assertIsNotNone(remote_handler)
        remote_handler = remote_handler.group(0)
        self.assertNotIn("ngx_str_to_char(value[1]", remote_handler)

    def test_all_connector_capabilities_report_remote_rules_disabled(self) -> None:
        for connector in (
            "apache",
            "envoy",
            "haproxy",
            "lighttpd",
            "nginx",
            "traefik",
        ):
            capabilities = json.loads(
                (ROOT / "connectors" / connector / "capabilities.json").read_text(
                    encoding="utf-8"
                )
            )
            remote = capabilities["capabilities"]["config_remote_rules"]
            self.assertEqual(remote["state"], "not_implemented", connector)
            self.assertIn("disabled by the common security policy", remote["reason"])


if __name__ == "__main__":
    unittest.main()
