from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_repository_organization_inventory.py"
SPEC = importlib.util.spec_from_file_location("repository_organization_inventory_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
INVENTORY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = INVENTORY
SPEC.loader.exec_module(INVENTORY)

OPEN_BRACE = "$" + "{"


class RepositoryOrganizationInventoryTest(unittest.TestCase):
    def test_variable_regex_preserves_supported_and_rejected_forms(self) -> None:
        cases = {
            "$FOO": ["$FOO"],
            OPEN_BRACE + "FOO}": [OPEN_BRACE + "FOO}"],
            "$(FOO)": ["$(FOO)"],
            "VAR=": ["VAR="],
            "ABC =": ["ABC ="],
            "BUILD_MODE:=": ["BUILD_MODE:="],
            "FEATURE+=": ["FEATURE+="],
            "$FOO}": ["$FOO}"],
            f"{OPEN_BRACE}FOO": [f"{OPEN_BRACE}FOO"],
            f"{OPEN_BRACE}FOO)": [f"{OPEN_BRACE}FOO"],
            "$FOO=": ["$FOO"],
            "$foo": [],
            "$(FOO": [],
            "AB=": [],
            "lower=": [],
            "ABC-=": [],
            "$": [],
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(INVENTORY.variable_matches(text), expected)

    def test_reference_regex_preserves_known_reference_boundaries(self) -> None:
        cases = {
            "ci/checks/foo.py": ["ci/checks/foo.py"],
            "docs/a-b.md": ["docs/a-b.md"],
            "reports/a.b/c": ["reports/a.b/c"],
            "examples/demo.yml": ["examples/demo.yml"],
            "make check-docs": ["make check-docs"],
            "make\tquick-check": ["make\tquick-check"],
            "cix/foo": [],
            "myci/foo": [],
            "CI/foo": [],
            "ci/": [],
            "documentation/a": [],
            "make": [],
            "make /": [],
        }

        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertEqual(INVENTORY.REFERENCE_RE.findall(text), expected)

    def test_framework_check_prefixes_keep_catalog_routing(self) -> None:
        framework_prefix = "modules/ModSecurity-test-Framework/ci/"

        self.assertEqual(
            INVENTORY.proposed_destination(f"{framework_prefix}check-smoke.py", True),
            f"{framework_prefix}checks/catalog/check-smoke.py",
        )
        self.assertEqual(
            INVENTORY.proposed_destination(f"{framework_prefix}check_smoke.py", True),
            f"{framework_prefix}checks/catalog/check_smoke.py",
        )
