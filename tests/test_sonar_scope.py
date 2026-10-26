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
            ".github/workflows/lint.yml", "examples/envoy/service.yaml", "config/runtime.json",
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

    def test_rejects_real_workflow_exclusion_even_with_github_readme(self) -> None:
        self.files.append(".github/README.md")
        self.config["sonar.exclusions"] += ",.github/workflows/**"
        with self.assertRaisesRegex(ValueError, r"maintained source excluded: \.github/workflows/lint.yml"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_rejects_maintained_json_config_exclusion_even_with_config_readme(self) -> None:
        self.files.append("config/README.md")
        self.config["sonar.exclusions"] += ",config/**/*.json"
        with self.assertRaisesRegex(ValueError, "maintained source excluded: config/runtime.json"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_rejects_maintained_yaml_example_exclusion_even_with_examples_readme(self) -> None:
        self.files.append("examples/README.md")
        self.config["sonar.exclusions"] += ",examples/**/*.yaml"
        with self.assertRaisesRegex(ValueError, "maintained source excluded: examples/envoy/service.yaml"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_keeps_negative_workflow_fixtures_separate_from_real_workflows(self) -> None:
        fixtures = [
            "ci/fixtures/workflow-permission-contract/unsafe.yml",
            "ci/fixtures/zizmor/insecure.yml",
            "tests/fixtures/python-version-contract/missing-setup.yml",
            "tests/fixtures/python-version-contract/valid-control.yaml",
        ]
        self.files.extend(fixtures)
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertEqual(result["excluded_tracked_files"], fixtures)
        self.assertIn(".github/workflows/lint.yml", result["source_paths"])

    def test_fixture_directory_does_not_exempt_python(self) -> None:
        self.files.append("ci/fixtures/zizmor/verify.py")
        self.config["sonar.exclusions"] += ",ci/fixtures/zizmor/**"
        with self.assertRaisesRegex(ValueError, "maintained source excluded: ci/fixtures/zizmor/verify.py"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_fixture_directory_does_not_exempt_nested_yaml(self) -> None:
        self.files.append("ci/fixtures/zizmor/tooling/config.yaml")
        self.config["sonar.exclusions"] += ",ci/fixtures/zizmor/**"
        with self.assertRaisesRegex(ValueError, "maintained source excluded: ci/fixtures/zizmor/tooling/config.yaml"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_preserves_explicit_generated_json_boundary(self) -> None:
        self.files.append("reports/testing/generated/canonical/full-runtime-matrix.generated.json")
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertEqual(result["excluded_tracked_files"], [self.files[-1]])

    def test_config_cannot_be_hidden_in_test_scope(self) -> None:
        self.config["sonar.test.inclusions"] += ",config/**/*.json"
        with self.assertRaisesRegex(ValueError, "incorrect test classification: config/runtime.json"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_readme_alone_does_not_count_as_analyzed_component(self) -> None:
        self.files.remove("examples/envoy/service.yaml")
        self.files.append("examples/README.md")
        with self.assertRaisesRegex(ValueError, "component missing analyzable code/config: examples"):
            SCOPE.validate(self.config, "3.15.1", self.files)

    def test_preserves_distributed_python_go_test_classification(self) -> None:
        paths = [
            "connectors/haproxy/harness/test_response.py",
            "connectors/lighttpd/harness/response_test.py",
            "connectors/traefik/native_middleware/middleware_test.go",
        ]
        self.files.extend(paths)
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertTrue(set(paths).issubset(result["test_paths"]))
        self.assertFalse(set(paths).intersection(result["source_paths"]))

    def test_ci_prefixed_python_unittest_is_classified_as_test(self) -> None:
        suite = "ci/runtime/lifecycle/i12/envoy/test_qualify_originals.py"
        self.files.extend([suite, "common/include/core.h"])
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertIn(suite, result["test_paths"])
        self.assertNotIn(suite, result["source_paths"])
        self.assertIn("common/include/core.h", result["source_paths"])
        self.assertIn("ci/check.py", result["source_paths"])
        self.assertIn("tests/regression.c", result["source_paths"])

    def test_ci_suffixed_python_unittest_is_classified_as_test(self) -> None:
        suite = "ci/runtime/lifecycle/i12/envoy/qualification_test.py"
        self.files.append(suite)
        result = SCOPE.validate(self.config, "3.15.1", self.files)
        self.assertIn(suite, result["test_paths"])
        self.assertNotIn(suite, result["source_paths"])
        self.assertIn("common/src/core.c", result["source_paths"])

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


# Parent discovery remains inventory-bound; only an explicit selected Master
# assessment may opt into the complete module without importing helpers eagerly.
if __import__("os").environ.get("ON_DEMAND_TESTS") != "1":
    def load_tests(loader, standard_tests, pattern):
        from ci.lib.active_test_inventory import module_load_tests
        return module_load_tests(loader, standard_tests, pattern)


if __name__ == "__main__":
    unittest.main()
