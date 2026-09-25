"""Regression guards for the off/safe/strict Phase-4 migration.

These are source/configuration contracts, not native-host runtime evidence.
The expected modes and MIME ownership come from the migration requirements.
"""

from pathlib import Path
import re
import unittest

from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = (
    "lint.yml",
    "test-nginx.yml",
    "test-apache.yml",
    "test-common.yml",
    "quick-framework-check.yml",
)


class Phase4MigrationContractTests(unittest.TestCase):
    def test_common_default_and_parser_have_only_the_supported_modes(self) -> None:
        options = (ROOT / "common/include/msconnector/options.h").read_text()
        parser = function_definition(
            (ROOT / "common/src/config_parser.c").read_text(),
            "msconnector_parse_phase4_mode",
        )
        self.assertRegex(
            options,
            r"#define\s+MSCONNECTOR_DEFAULT_PHASE4_MODE\s+"
            r"MSCONNECTOR_PHASE4_MODE_OFF\b",
        )
        self.assertNotIn("MSCONNECTOR_PHASE4_MODE_MINIMAL", options)
        self.assertEqual(
            set(re.findall(r'token_equals\(value, "([^"]+)"\)', parser)),
            {"off", "safe", "strict"},
        )
        self.assertIn("else { return 0; }", parser)

    def test_active_configuration_examples_have_no_removed_mode_or_mime_setting(self) -> None:
        old_setting = re.compile(
            r"^\s*(?:(?:modsecurity_)?phase4[_-]mode\s*(?:=|\s)\s*minimal\b|"
            r'(?:modsecurity_)?phase4_content_types_file\b|'
            r'"late_action_policy"\s*:\s*"minimal")',
            re.MULTILINE,
        )
        candidates = list((ROOT / "examples").rglob("*"))
        candidates.extend((ROOT / "connectors/traefik/config").rglob("*"))
        for path in candidates:
            if path.is_file() and path.suffix in {".conf", ".cfg", ".json", ".in", ".yaml"}:
                with self.subTest(path=path.relative_to(ROOT).as_posix()):
                    self.assertIsNone(old_setting.search(path.read_text()))

    def test_native_mime_configuration_is_not_registered_twice(self) -> None:
        for relative in (
            "common/include/msconnector/directives.h",
            "common/include/msconnector/options.h",
            "connectors/apache/src/msc_config.c",
            "connectors/nginx/src/ngx_http_modsecurity_module.c",
        ):
            with self.subTest(path=relative):
                self.assertNotIn("phase4_content_types", (ROOT / relative).read_text().lower())

    def test_prs_do_not_skip_the_post_merge_lint_and_syntax_steps(self) -> None:
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                text = (ROOT / ".github/workflows" / name).read_text()
                self.assertRegex(text, r"(?m)^  pull_request:")
                self.assertNotRegex(
                    text, r"if:.*github\.event_name\s*!=\s*['\"]pull_request['\"]"
                )
                self.assertNotIn("continue-on-error: true", text)
                self.assertRegex(text, r"(?m)^permissions: \\{\\}$")\n                self.assertRegex(text, r"(?m)^    permissions:\\n      contents: read$")
                self.assertRegex(text, r"make (?:lint|quick-check)")

    def test_migration_regressions_and_generated_files_are_checked_in_prs(self) -> None:
        text = (ROOT / ".github/workflows/lint.yml").read_text()
        for marker in (
            "tests.test_phase4_migration_contract",
            "tests.test_nginx_native_security_contract",
            "tests.test_nginx_upstream_security_contract",
            "tests.test_nginx_common_adoption",
            "tests.test_connector_config_reference",
            "tests.test_logical_connector_all_examples",
            "generate-connector-config-reference.py --check",
            "ci/checks/documentation/check-connector-config-reference.py",
        ):
            with self.subTest(check=marker):
                self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
