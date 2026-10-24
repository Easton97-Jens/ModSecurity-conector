"""Regression for Apache P4 rate-limit action fidelity."""

from __future__ import annotations

import unittest

from tests.test_apache_intervention_cleanup import FILTERS, MODULE, c_function


class ApachePhase4RateLimitTests(unittest.TestCase):
    def test_precommit_rate_limit_preserves_http_action_and_outcome(self) -> None:
        module_source = MODULE.read_text(encoding="utf-8")
        filters_source = FILTERS.read_text(encoding="utf-8")
        decision_kind = c_function(
            module_source,
            "static msconnector_transaction_decision_kind apache_intervention_decision_kind(",
        )
        action_mapper = c_function(
            module_source,
            "const char *msc_apache_contract_intervention_action(const msc_t *msr)",
        )
        phase4_actual = c_function(
            filters_source,
            "static const char *apache_phase4_actual_action(",
        )
        intervention_http = c_function(
            filters_source,
            "static void apache_intervention_set_http(",
        )
        enforced_http = intervention_http.split(
            'else if (strcmp(input->actual, "abort_connection") == 0)', 1
        )[0]

        self.assertIn("if (status == HTTP_TOO_MANY_REQUESTS)", decision_kind)
        self.assertIn(
            "return MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT;", decision_kind
        )
        self.assertIn('return "rate_limit";', action_mapper)
        self.assertIn('strcmp(requested_action, "redirect") == 0', phase4_actual)
        self.assertIn('strcmp(requested_action, "rate_limit") == 0', phase4_actual)
        self.assertIn('return "deny";', phase4_actual)
        self.assertIn('strcmp(input->actual, "rate_limit") == 0', enforced_http)
        self.assertIn(
            "event->http.visible_http_status = msr->last_intervention_status;",
            enforced_http,
        )
        self.assertIn(
            'event->http.transport_result = "http_status";', enforced_http
        )
        self.assertIn(
            'event->http.transport_result = "log_only";', intervention_http
        )


if __name__ == "__main__":
    unittest.main()
