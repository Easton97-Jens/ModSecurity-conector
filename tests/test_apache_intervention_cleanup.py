"""Source-contract regression for Apache intervention-owned values."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"
C17_CHECK = (
    ROOT / "ci" / "checks" / "connectors" / "apache" / "check-apache-c-standards.sh"
)


def c_function(source: str, signature: str) -> str:
    """Return one complete C function body for the exact signature."""
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


class ApacheInterventionCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.source = c_function(
            MODULE.read_text(encoding="utf-8"),
            "int process_intervention (Transaction *t, request_rec *r)",
        )

    def test_successful_interventions_funnel_through_one_cleanup(self) -> None:
        self.assertEqual(self.source.count("msc_intervention_cleanup(&intervention);"), 1)
        cleanup = self.source.index("msc_intervention_cleanup(&intervention);")
        self.assertIn("cleanup:", self.source[:cleanup])
        self.assertNotIn("intervention.url", self.source[cleanup:])
        self.assertNotIn("intervention.log", self.source[cleanup:])
        self.assertLess(cleanup, self.source.index("return result;"))

        returns = re.findall(r"\breturn(?:\s+[^;\s][^;]*|\s{2,});", self.source)
        self.assertEqual(returns, ["return N_INTERVENTION_STATUS;", "return result;"])

    def test_log_fallback_does_not_overwrite_the_cleanup_owned_field(self) -> None:
        self.assertIn("log = intervention.log;", self.source)
        self.assertIn('log = "(no log message was specified)";', self.source)
        self.assertIn("apr_pstrdup(r->pool, log);", self.source)
        self.assertNotIn('intervention.log = "(no log message was specified)";', self.source)

    def test_no_intervention_preserves_the_existing_allow_result(self) -> None:
        no_intervention = self.source.index("if (z == 0)")
        cleanup = self.source.index("cleanup:")
        self.assertLess(no_intervention, cleanup)
        self.assertIn(
            "return N_INTERVENTION_STATUS;",
            self.source[no_intervention:cleanup],
        )

    def test_redirect_url_is_request_owned_before_native_cleanup(self) -> None:
        copy = "location = apr_pstrdup(r->pool, intervention.url);"
        assign = 'apr_table_setn(r->headers_out, "Location", location);'
        cleanup = "msc_intervention_cleanup(&intervention);"

        self.assertIn(copy, self.source)
        self.assertIn(assign, self.source)
        self.assertNotIn(
            'apr_table_setn(r->headers_out, "Location", intervention.url);',
            self.source,
        )
        self.assertLess(self.source.index(copy), self.source.index(assign))
        self.assertLess(self.source.index(assign), self.source.index(cleanup))
        self.assertIn("result = HTTP_MOVED_TEMPORARILY;", self.source)
        self.assertIn("result = intervention.status;", self.source)

    def test_changed_translation_unit_and_regression_are_in_required_wiring(self) -> None:
        source_list = C17_CHECK.read_text(encoding="utf-8")
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        lint_match = re.search(
            r"^lint:[^\n]*\n(?P<body>(?:\t.*\n)+)", makefile, re.MULTILINE
        )

        self.assertIn("connectors/apache/src/mod_security3.c", source_list)
        self.assertIn("check-apache-intervention-cleanup:", makefile)
        self.assertIsNotNone(lint_match)
        self.assertIn(
            "$(MAKE) check-apache-intervention-cleanup", lint_match.group("body")
        )


if __name__ == "__main__":
    unittest.main()
