"""Source-contract regression for Apache intervention-owned values."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"
FILTERS = ROOT / "connectors" / "apache" / "src" / "msc_filters.c"
C17_CHECK = (
    ROOT / "ci" / "checks" / "connectors" / "apache" / "check-apache-c-standards.sh"
)


def c_function(source: str, signature: str) -> str:
    """Return one complete C function body for the exact signature."""
    start = source.index(signature)
    while True:
        opening_brace = source.index("{", start)
        semicolon = source.index(";", start)
        if opening_brace < semicolon:
            break
        start = source.index(signature, semicolon)
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
        self.module_source = MODULE.read_text(encoding="utf-8")
        self.filters_source = FILTERS.read_text(encoding="utf-8")
        self.source = c_function(
            self.module_source,
            "int process_intervention (Transaction *t, request_rec *r)",
        )
        self.cleanup_helper = c_function(
            self.module_source,
            "static void msc_release_intervention_buffers(",
        )

    def test_successful_interventions_funnel_through_one_cleanup(self) -> None:
        cleanup_call = "msc_release_intervention_buffers(&intervention);"
        self.assertEqual(self.source.count(cleanup_call), 1)
        cleanup = self.source.index(cleanup_call)
        self.assertIn("cleanup:", self.source[:cleanup])
        self.assertNotIn("intervention.url", self.source[cleanup:])
        self.assertNotIn("intervention.log", self.source[cleanup:])
        self.assertLess(cleanup, self.source.index("return result;"))

        returns = re.findall(r"\breturn(?:\s+[^;\s][^;]*|\s{2,});", self.source)
        self.assertEqual(returns, ["return N_INTERVENTION_STATUS;", "return result;"])

    def test_cleanup_uses_only_the_legacy_public_intervention_contract(self) -> None:
        self.assertNotIn("msc_intervention_cleanup(&", self.module_source)
        self.assertEqual(self.cleanup_helper.count("free(intervention->url);"), 1)
        self.assertEqual(self.cleanup_helper.count("free(intervention->log);"), 1)
        self.assertIn("intervention->url = NULL;", self.cleanup_helper)
        self.assertIn("intervention->log = NULL;", self.cleanup_helper)
        self.assertIn("intervention->status = N_INTERVENTION_STATUS;", self.cleanup_helper)
        self.assertIn("intervention->pause = 0;", self.cleanup_helper)
        self.assertIn("intervention->disruptive = 0;", self.cleanup_helper)
        self.assertIn("intervention.pause = 0;", self.source)

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
        cleanup = "msc_release_intervention_buffers(&intervention);"

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

    def test_p3_intervention_records_a_canonical_terminal_decision_before_sink(self) -> None:
        phase3 = c_function(
            self.filters_source,
            "static apr_status_t apache_output_filter_process_headers(",
        )
        mapper = c_function(
            self.module_source,
            "int msc_apache_contract_record_intervention_decision(msc_t *msr)",
        )
        decision_kind_mapper = c_function(
            self.module_source,
            "static msconnector_transaction_decision_kind apache_intervention_decision_kind(",
        )
        decision_wrapper = c_function(
            self.module_source,
            "int msc_apache_contract_record_decision(",
        )
        failure_wrapper = c_function(
            self.module_source,
            "int msc_apache_contract_fail(",
        )

        complete = phase3.index("msc_apache_contract_complete(msr,")
        record = phase3.index("msc_apache_contract_record_intervention_decision(msr)")
        failure = phase3.index(
            "MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE", record
        )
        event = phase3.index("apache_phase3_log_event(msr, r, wanted, wanted, original_status)")
        sink = phase3.index(
            "apache_send_precommit_terminal_error(msr, filter, brigade,", event
        )
        self.assertLess(complete, record)
        self.assertLess(record, event)
        self.assertLess(event, sink)
        self.assertLess(record, failure)
        self.assertLess(failure, sink)
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE", phase3)
        self.assertIn("char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH]", mapper)
        self.assertIn("msconnector_rule_id_extract_from_message", mapper)
        self.assertIn("MSCONNECTOR_TRANSACTION_DECISION_REDIRECT", decision_kind_mapper)
        self.assertIn("MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT", decision_kind_mapper)
        self.assertIn("MSCONNECTOR_TRANSACTION_DECISION_BLOCK", decision_kind_mapper)
        self.assertIn("HTTP_TOO_MANY_REQUESTS", decision_kind_mapper)
        self.assertNotIn("last_intervention_status >= 300", decision_kind_mapper)
        for redirect_status in ("case 301:", "case 302:", "case 303:", "case 307:"):
            with self.subTest(redirect_status=redirect_status):
                self.assertIn(redirect_status, decision_kind_mapper)
        self.assertIn("apache_intervention_decision_kind", mapper)
        self.assertIn("msc_apache_contract_record_decision(msr, kind, rule_id)", mapper)
        self.assertIn("msconnector_transaction_contract_record_decision", decision_wrapper)
        self.assertIn("apache_contract_now_ms()", decision_wrapper)
        self.assertIn("msconnector_transaction_contract_fail", failure_wrapper)
        self.assertIn("apache_contract_now_ms()", failure_wrapper)

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
