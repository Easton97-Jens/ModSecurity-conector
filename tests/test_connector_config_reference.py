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
