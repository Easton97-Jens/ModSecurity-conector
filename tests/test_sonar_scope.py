"""Reject scope changes that silently lose Parent analysis coverage."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sonar_scope", ROOT / "ci/checks/analysis/check-sonar-scope.py")
assert SPEC is not None
assert SPEC.loader is not None
SCOPE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCOPE)


class SonarScopeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = SCOPE.properties(ROOT / "sonar-project.properties")
        self.files = [
            "common/src/core.c", "connectors/apache/build/build.sh", "ci/check.py",
            "scripts/tool.py", "tests/helper.py", "tests/regression.c",
            ".github/workflows/lint.yml", "examples/host.conf", "config/runtime.json",
            "fuzz/http.c", "connectors/envoy/test_peer.py",
            "connectors/envoy/ext_proc/main_test.go",
            "connectors/envoy/ext_proc/go.mod",
            "connectors/traefik/native_middleware/go.mod",
            "connectors/traefik/composite_middleware/go.mod",
            "connectors/traefik/response_observer/go.mod",
            "modules/ModSecurity-test-Framework",
        ]

    def test_preserves_cfamily_tests_and_connector_build_scripts(self) -> None:
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertEqual(result["test_files"], 3)
        self.assertEqual(result["cfamily_translation_units"], 3)
        self.assertEqual(result["excluded_tracked_files"], [])

    def test_rejects_python_minor_drift(self) -> None:
        with self.assertRaisesRegex(ValueError, "major.minor"):
            SCOPE.validate(self.config, "3.16.1", self.files)

    def test_rejects_language_blind_test_scope(self) -> None:
        self.config["sonar.test.inclusions"] += ",tests/**"
        with self.assertRaisesRegex(ValueError, "CFamily|classification"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_rejects_nested_build_script_exclusion(self) -> None:
        self.config["sonar.exclusions"] += ",**/build/**"
        with self.assertRaisesRegex(ValueError, "maintained source excluded"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_rejects_ambiguous_property_files(self) -> None:
        cases = (
            ("sonar.sources\n", "unsupported property syntax"),
            ("sonar.sources=.\nsonar.sources=ci\n", "duplicate property"),
            ("sonar.sources=.\\\n", "unsupported property syntax"),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sonar-project.properties"
            for contents, message in cases:
                with self.subTest(contents=contents):
                    path.write_text(contents, encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, message):
                        SCOPE.properties(path)

    def test_scope_patterns_reject_foreign_glob_syntax(self) -> None:
        for pattern in ("", "tests/[ab].py", "tests\\*.py"):
            with self.subTest(pattern=pattern):
                with self.assertRaisesRegex(ValueError, "unsupported scope pattern"):
                    SCOPE.matches("tests/a.py", pattern)
        self.assertTrue(SCOPE.matches("tests/a.py", "tests/?.py"))
        self.assertFalse(SCOPE.matches("tests/ab.py", "tests/?.py"))

    def test_requires_independent_submodule_boundary(self) -> None:
        self.config["sonar.exclusions"] = ",".join(
            pattern for pattern in self.config["sonar.exclusions"].split(",")
            if "modules" not in pattern
        )
        with self.assertRaisesRegex(ValueError, "independent submodule"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_requires_review_when_go_module_inventory_changes(self) -> None:
        self.files.append("connectors/new_connector/go.mod")
        with self.assertRaisesRegex(ValueError, "review Go module inventory"):
            SCOPE.validate(self.config, "3.15.1", self.files)


if __name__ == "__main__":
    unittest.main()
