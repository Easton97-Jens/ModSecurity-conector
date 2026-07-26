"""Regression contract for Apache directory-config RulesSet ownership."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "connectors" / "apache" / "src" / "msc_config.c"
C17_CHECK = (
    ROOT / "ci" / "checks" / "connectors" / "apache" / "check-apache-c-standards.sh"
)
NATIVE_HARNESS = (
    ROOT / "ci" / "checks" / "connectors" / "apache" / "apache_rules_set_cleanup.c"
)
NATIVE_CHECK = ROOT / "ci" / "checks" / "connectors" / "apache" / (
    "check-apache-rules-set-cleanup.sh"
)


def c_function(source: str, signature: str) -> str:
    """Return the complete C function that begins with ``signature``."""
    start = source.index(signature)
    opening_brace = source.index("{", start)
    depth = 0
    for index in range(opening_brace, len(source)):
        if source[index] == "{":
            depth += 1
        elif source[index] == "}":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise AssertionError(f"incomplete C function: {signature}")


class ApacheRulesSetCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = CONFIG.read_text(encoding="utf-8")
        self.cleanup = c_function(
            self.source, "static apr_status_t msc_rules_set_cleanup(void *data)"
        )
        self.create = c_function(
            self.source,
            "void *msc_hook_create_config_directory(apr_pool_t *mp, char *path)",
        )
        self.merge = c_function(
            self.source,
            "void *msc_hook_merge_config_directory(apr_pool_t *mp, void *parent,",
        )

    def test_cleanup_adapter_accepts_only_non_null_rules_sets(self) -> None:
        self.assertIn("if (data != NULL)", self.cleanup)
        self.assertEqual(self.cleanup.count("msc_rules_cleanup(data);"), 1)
        self.assertIn("return APR_SUCCESS;", self.cleanup)
        self.assertEqual(self.source.count("msc_rules_cleanup("), 1)

    def test_successful_config_creation_registers_one_pool_cleanup(self) -> None:
        create_rules_set = self.create.index("cnf->rules_set = msc_create_rules_set();")
        null_check = self.create.index("if (cnf->rules_set == NULL)")
        registration = self.create.index(
            "apr_pool_cleanup_register(mp, cnf->rules_set,"
        )

        self.assertLess(create_rules_set, null_check)
        self.assertLess(null_check, registration)
        self.assertEqual(self.create.count("apr_pool_cleanup_register("), 1)
        self.assertIn("msc_rules_set_cleanup,", self.create[registration:])
        self.assertIn("apr_pool_cleanup_null);", self.create[registration:])
        self.assertIn("return NULL;", self.create[null_check:registration])

    def test_merge_creates_a_new_owned_rules_set_without_manual_cleanup(self) -> None:
        self.assertEqual(
            self.merge.count("msc_hook_create_config_directory(mp,"), 1
        )
        self.assertEqual(self.merge.count("msc_rules_merge("), 2)
        self.assertNotIn("apr_pool_cleanup_register(", self.merge)
        self.assertNotIn("msc_rules_cleanup(", self.merge)

    def test_c17_and_native_harness_cover_the_changed_translation_unit(self) -> None:
        c17_sources = C17_CHECK.read_text(encoding="utf-8")
        native_harness = NATIVE_HARNESS.read_text(encoding="utf-8")
        native_check = NATIVE_CHECK.read_text(encoding="utf-8")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        check_target = makefile.split(
            "check-apache-ruleset-cleanup:\n", 1
        )[1].split("\n\n", 1)[0]
        lint_target = makefile.split(
            "check-apache-ruleset-cleanup-lint:\n", 1
        )[1].split("\n\n", 1)[0]
        lint_match = re.search(
            r"^lint:[^\n]*\n(?P<body>(?:\t.*\n)+)", makefile, re.MULTILINE
        )

        self.assertIn("connectors/apache/src/msc_config.c", c17_sources)
        self.assertIn("msc_hook_create_config_directory", native_harness)
        self.assertIn("msc_hook_merge_config_directory", native_harness)
        self.assertIn("test_null_rules_set_never_registers_cleanup", native_harness)
        self.assertIn(
            "test_pool_clear_does_not_repeat_rules_set_cleanup", native_harness
        )
        self.assertIn(
            "test_rules_merge_error_keeps_new_rules_set_pool_owned", native_harness
        )
        self.assertIn(
            "test_second_rules_merge_error_keeps_new_rules_set_pool_owned",
            native_harness,
        )
        self.assertIn(
            "test_common_config_error_keeps_new_rules_set_pool_owned", native_harness
        )
        self.assertIn("-std=c17", native_check)
        self.assertIn("-UNDEBUG", native_check)
        self.assertIn("-Wl,--wrap=ap_log_perror_", native_check)
        self.assertIn("msc_config.c", native_check)
        self.assertIn("APACHE_RULES_SET_CLEANUP_OUT", native_check)
        self.assertIn("reject_symlink_components", native_check)
        self.assertIn("exit 77", native_check)
        self.assertNotIn("eval ", native_check)
        self.assertIn("tests.test_apache_rules_set_cleanup", check_target)
        self.assertIn("check-apache-rules-set-cleanup.sh", check_target)
        self.assertIn("ci/tools/run-check-status.py", lint_target)
        self.assertIn("--check apache_rules_set_cleanup", lint_target)
        self.assertIn("--blocked-if-missing-apache-development", lint_target)
        self.assertIn("check-apache-rules-set-cleanup.sh", lint_target)
        self.assertIsNotNone(lint_match)
        self.assertIn(
            "$(MAKE) check-apache-ruleset-cleanup-lint", lint_match.group("body")
        )
        self.assertIn("check-apache-ruleset-cleanup:", makefile)
        self.assertIn("check-apache-ruleset-cleanup-lint:", makefile)
        self.assertIn("$(MAKE) check-apache-ruleset-cleanup-lint", makefile)
        self.assertIn("void __wrap_ap_log_perror_(void)", native_harness)
        self.assertNotIn("void ap_log_perror_(", native_harness)


if __name__ == "__main__":
    unittest.main()
