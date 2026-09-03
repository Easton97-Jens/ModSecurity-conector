from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTATION_CHECKS = ROOT / "ci" / "checks" / "documentation"
if str(DOCUMENTATION_CHECKS) not in sys.path:
    sys.path.insert(0, str(DOCUMENTATION_CHECKS))

import connector_config_reference as REFERENCE


class ConnectorConfigReferenceTests(unittest.TestCase):
    def test_common_runtime_limits_are_extracted_from_enforced_header_caps(self) -> None:
        limits = REFERENCE.common_runtime_limits(ROOT)
        self.assertEqual(
            limits,
            {
                "request_body_limit": 10485760,
                "response_body_limit": 10485760,
                "max_header_count": 256,
                "max_header_name_size": 256,
                "max_header_value_size": 8192,
                "max_total_header_bytes": 65536,
                "max_event_json_bytes": 16384,
            },
        )
        options = {
            option["name"]: option
            for option in REFERENCE.extract_common_runtime(ROOT)
        }
        self.assertEqual(options["max_header_count"]["allowed_values"], "1 through 256")
        self.assertIn("values above 256", options["max_header_count"]["validation"])

    def test_lighttpd_native_directive_inventory_is_closed_and_documents_opt_in_evidence(self) -> None:
        directives = {
            option["name"]: option
            for option in REFERENCE.extract_lighttpd(ROOT)
            if option["configuration_layer"] == "host_connector_directive"
        }

        self.assertSetEqual(
            set(directives),
            {
                "msconnector.enabled",
                "msconnector.config-file",
                "msconnector.expose-host-transaction-id",
                "msconnector.request-body-gate",
            },
        )
        evidence = directives["msconnector.expose-host-transaction-id"]
        self.assertEqual(evidence["default"], "off")
        self.assertEqual(
            evidence["syntax"],
            'msconnector.expose-host-transaction-id = "enable" | "disable"',
        )
        self.assertIn("server-generated", evidence["security_relevance"])
        self.assertIn("never reflects a request header", evidence["security_relevance"])
        request_gate = directives["msconnector.request-body-gate"]
        self.assertEqual(
            request_gate["syntax"],
            'msconnector.request-body-gate = "pre-upstream"',
        )
        self.assertIn("P2", request_gate["phase_relevance"])
        self.assertIn("pre-upstream", request_gate["security_relevance"])

    def test_apache_example_file_mapping_is_complete_and_stable(self) -> None:
        example_by_directive = {
            item["name"]: item["example_file"]
            for item in REFERENCE.extract_apache(ROOT)
        }
        source_directive = "modsecurity_phase4_content_types_file"
        source_example = "connectors/apache/src/msc_config.c"
        minimal_example = "examples/apache/minimal/httpd.conf"
        safe_example = "examples/apache/safe/httpd.conf"
        minimal_directives = {
            "modsecurity",
            "modsecurity_rules_file",
            "modsecurity_use_error_log",
        }

        self.assertEqual(example_by_directive[source_directive], source_example)
        self.assertSetEqual(
            {
                directive
                for directive, example_file in example_by_directive.items()
                if example_file == minimal_example
            },
            minimal_directives,
        )
        safe_directives = set(example_by_directive) - minimal_directives - {source_directive}
        self.assertTrue(safe_directives)
        self.assertTrue(
            all(example_by_directive[directive] == safe_example for directive in safe_directives)
        )

    def test_haproxy_spop_limits_match_runtime_contract(self) -> None:
        options = {
            option["name"].split(":", 1)[1]: option
            for option in REFERENCE.extract_haproxy(ROOT)
            if option["name"].startswith("spoe-agent:")
        }
        self.assertEqual(options["worker-count"]["default"], "8")
        self.assertEqual(
            options["worker-count"]["allowed_values"],
            "decimal integer, 2..64; worker-count * max-transactions <= 65536",
        )
        self.assertEqual(
            options["max-transactions"]["allowed_values"],
            "decimal integer, 1..4096; worker-count * max-transactions <= 65536",
        )
        self.assertEqual(options["spoe-timeout"]["allowed_values"], "positive decimal milliseconds, 1..60000")
        self.assertIn(
            "must be 0 with response-companion=none",
            options["response-body-timeout"]["validation"],
        )
        self.assertIn("unknown keys and malformed values", options["max-transactions"]["validation"])

        german = REFERENCE._german_option(options["worker-count"])
        self.assertIn("dezimale Ganzzahl", german["allowed_values"])
        self.assertIn("worker-count akzeptiert 2..64", REFERENCE._german_option(options["worker-count"])["validation"])
