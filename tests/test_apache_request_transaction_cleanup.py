"""Regression contract for Apache request-owned ModSecurity transactions."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"
HEADER = ROOT / "connectors" / "apache" / "src" / "mod_security3.h"
UTILS = ROOT / "connectors" / "apache" / "src" / "msc_utils.c"
FILTERS = ROOT / "connectors" / "apache" / "src" / "msc_filters.c"
C17_CHECK = (
    ROOT / "ci" / "checks" / "connectors" / "apache" / "check-apache-c-standards.sh"
)


def c_function(source: str, signature: str) -> str:
    """Return one complete C function body without matching nearby tokens."""
    start = source.index(signature)
    while True:
        body_start = start + len(signature)
        while body_start < len(source) and source[body_start].isspace():
            body_start += 1
        if body_start < len(source) and source[body_start] == "{":
            break
        start = source.index(signature, body_start)
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


class ApacheRequestTransactionCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = MODULE.read_text(encoding="utf-8")
        self.header = HEADER.read_text(encoding="utf-8")
        self.utils = UTILS.read_text(encoding="utf-8")
        self.filters = FILTERS.read_text(encoding="utf-8")
        self.create_context = c_function(
            self.module, "static msc_t *create_tx_context(request_rec *r)"
        )
        self.request_headers = c_function(
            self.module,
            "static int process_request_headers(request_rec *r, msc_t *msr)",
        )
        phase1_start = self.module.index(
            "static int apache_emit_phase1_intervention_event"
        )
        phase1_end = self.module.index(
            "static int process_request_headers", phase1_start
        )
        self.phase1_intervention = self.module[phase1_start:phase1_end]
        self.cleanup = c_function(
            self.utils, "apr_status_t msc_cleanup_request_transaction(void *data)"
        )
        self.output_filter = c_function(
            self.filters,
            "apr_status_t output_filter(ap_filter_t *f, apr_bucket_brigade *bb_in)",
        )

    def test_failed_native_transaction_is_never_published(self) -> None:
        failure_check = self.create_context.index("if (msr->t == NULL)")
        publish = self.create_context.index("store_tx_context(msr, r);")

        self.assertLess(failure_check, publish)
        self.assertIn("return NULL;", self.create_context[failure_check:publish])

    def test_successful_context_is_registered_once_on_owner_request_pool(self) -> None:
        publish = self.create_context.index("store_tx_context(msr, r);")
        registration = self.create_context.index("apr_pool_cleanup_register(r->pool, msr,")

        self.assertLess(publish, registration)
        self.assertEqual(self.create_context.count("apr_pool_cleanup_register("), 1)
        self.assertIn(
            "msc_cleanup_request_transaction, apr_pool_cleanup_null);",
            self.create_context[registration:],
        )

    def test_cleanup_invalidates_native_and_owner_context_before_destroy(self) -> None:
        self.assertIn("request_rec *owner_request;", self.header)
        self.assertIn("owner_request = msr->owner_request;", self.cleanup)
        self.assertIn("msr->owner_request = NULL;", self.cleanup)
        self.assertIn("transaction = msr->t;", self.cleanup)
        self.assertIn("msr->t = NULL;", self.cleanup)
        self.assertIn("apr_table_unset(owner_request->notes, NOTE_MSR);", self.cleanup)
        self.assertIn("if (transaction != NULL)", self.cleanup)
        self.assertIn("msc_transaction_cleanup(transaction);", self.cleanup)
        self.assertNotIn("msr->r", self.cleanup)

        pointer_clear = self.cleanup.index("msr->t = NULL;")
        owner_clear = self.cleanup.index("apr_table_unset(owner_request->notes, NOTE_MSR);")
        native_destroy = self.cleanup.index("msc_transaction_cleanup(transaction);")
        self.assertLess(pointer_clear, native_destroy)
        self.assertLess(owner_clear, native_destroy)

    def test_primary_request_ownership_preserves_existing_redirect_and_subrequest_rules(self) -> None:
        late_hook = c_function(self.module, "static int hook_request_late(request_rec *r)")
        retrieve = c_function(self.module, "static msc_t *retrieve_tx_context(request_rec *r)")

        self.assertIn("if ((r->main != NULL) || (r->prev != NULL))", late_hook)
        self.assertIn("r->main->notes", retrieve)
        self.assertIn("rx = r->prev;", retrieve)
        self.assertIn("msr->r = r;", retrieve)

    def test_c17_check_compiles_the_cleanup_helper(self) -> None:
        source_list = C17_CHECK.read_text(encoding="utf-8")
        self.assertIn("connectors/apache/src/msc_utils.c", source_list)

    def test_unread_request_body_failure_returns_before_response_headers(self) -> None:
        drain = self.output_filter.index(
            "apr_status_t request_body_rc = apache_finish_unread_request_body(f);"
        )
        failure_check = self.output_filter.index(
            "if (request_body_rc != APR_SUCCESS)", drain
        )
        failure_return = self.output_filter.index("return request_body_rc;", failure_check)
        response_headers = self.output_filter.index(
            "rc = apache_output_filter_process_headers(msr, r, f, bb_in);"
        )

        self.assertNotIn(
            "apr_status_t rc = apache_finish_unread_request_body(f);",
            self.output_filter,
        )
        self.assertLess(drain, failure_check)
        self.assertLess(failure_check, failure_return)
        self.assertLess(failure_return, response_headers)

    def test_phase1_intervention_logging_shares_one_bounded_event_writer(self) -> None:
        self.assertEqual(
            self.phase1_intervention.count("apache_emit_intervention_event("), 1
        )
        self.assertIn(
            'event_input.event_name = "phase1_intervention";',
            self.phase1_intervention,
        )
        self.assertIn(
            "event_input.phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;",
            self.phase1_intervention,
        )
        self.assertIn(
            '"request_uri_before_request_headers"', self.request_headers
        )
        self.assertIn('"request_headers_before_handler"', self.request_headers)
        self.assertEqual(
            self.request_headers.count(
                "apache_emit_phase1_intervention_event(msr, r, it,"
            ),
            2,
        )

    def test_native_rule_match_uses_canonical_allow_action(self) -> None:
        rule_match = c_function(
            self.filters,
            "void apache_log_rule_match_event(msc_t *msr, request_rec *r,\n"
            "    enum msconnector_phase phase, const char *rule_id)",
        )

        self.assertIn("event.meta.event = \"request_rule_match\";", rule_match)
        self.assertEqual(rule_match.count('event.decision.action = "allow";'), 1)
        self.assertEqual(
            rule_match.count('event.decision.requested_action = "allow";'), 1
        )
        self.assertEqual(
            rule_match.count('event.decision.actual_action = "allow";'), 1
        )
        self.assertNotIn('event.decision.action = "pass";', rule_match)
        self.assertNotIn('event.decision.requested_action = "pass";', rule_match)
        self.assertNotIn('event.decision.actual_action = "pass";', rule_match)


if __name__ == "__main__":
    unittest.main()
