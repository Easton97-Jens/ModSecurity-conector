"""Ownership contract for Apache configuration RulesSet objects."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "connectors/apache/src/msc_config.c"


def c_function(source: str, signature: str) -> str:
    start = source.index(signature)
    opening = source.index("{", start)
    depth = 0
    for index in range(opening, len(source)):
        depth += source[index] == "{"
        depth -= source[index] == "}"
        if depth == 0:
            return source[start:index + 1]
    raise AssertionError(f"incomplete C function: {signature}")


class ApacheRulesetCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.source = SOURCE.read_text(encoding="utf-8")
        cls.cleanup = c_function(
            cls.source, "static apr_status_t msc_rules_set_pool_cleanup(void *data)"
        )
        cls.create = c_function(
            cls.source, "void *msc_hook_create_config_directory(apr_pool_t *mp, char *path)"
        )
        cls.merge = c_function(
            cls.source, "void *msc_hook_merge_config_directory(apr_pool_t *mp, void *parent,"
        )

    def test_adapter_is_null_safe_and_has_apr_cleanup_contract(self) -> None:
        self.assertIn("if (data != NULL)", self.cleanup)
        self.assertEqual(1, self.cleanup.count("msc_rules_cleanup((RulesSet *)data);"))
        self.assertIn("return APR_SUCCESS;", self.cleanup)

    def test_every_creation_is_registered_once_after_null_check(self) -> None:
        self.assertEqual(1, len(re.findall(r"msc_create_rules_set\s*\(", self.source)))
        self.assertEqual(1, self.create.count("apr_pool_cleanup_register("))
        null_check = self.create.index("if (cnf->rules_set == NULL)")
        registration = self.create.index("apr_pool_cleanup_register(mp, cnf->rules_set,")
        self.assertLess(null_check, registration)
        self.assertIn(
            "msc_rules_set_pool_cleanup, apr_pool_cleanup_null);",
            self.create[registration:],
        )

    def test_merge_owns_a_fresh_ruleset_via_the_merge_pool(self) -> None:
        self.assertIn("msc_hook_create_config_directory(mp,", self.merge)
        self.assertNotIn("apr_pool_cleanup_register", self.merge)
        self.assertNotIn("msc_rules_cleanup", self.merge)

    def test_no_manual_destroy_can_race_the_pool_owner(self) -> None:
        self.assertEqual(1, self.source.count("msc_rules_cleanup("))
        self.assertNotIn("apr_pool_cleanup_kill", self.source)

    def test_make_and_c17_wiring_include_the_contract(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        c17 = (ROOT / "ci/checks/connectors/apache/check-apache-c-standards.sh").read_text(encoding="utf-8")
        self.assertIn("check-apache-ruleset-cleanup:", makefile)
        self.assertIn("$(MAKE) check-apache-ruleset-cleanup", makefile)
        self.assertIn("connectors/apache/src/msc_config.c", c17)


if __name__ == "__main__":
    unittest.main()
