"""Regression contract for native P2 body-limit host translations."""

from __future__ import annotations

from pathlib import Path
import unittest

from tests.c_source_contract import function_definition


ROOT = Path(__file__).resolve().parents[1]
APACHE = ROOT / "connectors" / "apache" / "src" / "mod_security3.c"
APACHE_FILTERS = ROOT / "connectors" / "apache" / "src" / "msc_filters.c"
NGINX = ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_module.c"
NGINX_ACCESS = ROOT / "connectors" / "nginx" / "src" / "ngx_http_modsecurity_access.c"
HAPROXY = ROOT / "connectors" / "haproxy" / "src" / "haproxy_modsecurity_binding.c"
HAPROXY_SPOP = (
    ROOT / "connectors" / "haproxy" / "src" / "haproxy_spop_diagnostic_runtime.c"
)


class NativeRequestBodyLimitAdapterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.apache = APACHE.read_text(encoding="utf-8")
        cls.apache_filters = APACHE_FILTERS.read_text(encoding="utf-8")
        cls.nginx = NGINX.read_text(encoding="utf-8")
        cls.nginx_access = NGINX_ACCESS.read_text(encoding="utf-8")
        cls.haproxy = HAPROXY.read_text(encoding="utf-8")
        cls.haproxy_spop = HAPROXY_SPOP.read_text(encoding="utf-8")

    def test_apache_classifies_before_rule_id_correlation(self) -> None:
        intervention = function_definition(self.apache, "process_intervention")
        mapper = function_definition(
            self.apache, "msc_apache_contract_record_intervention_decision"
        )
        phase2 = function_definition(self.apache_filters, "msc_finalize_request_body")

        classifier = intervention.index(
            "msconnector_intervention_is_request_body_limit_rejection"
        )
        normalize = intervention.index("msconnector_intervention_normalize_status")
        retained = intervention.index("msr->last_intervention_body_limit", classifier)
        self.assertLess(classifier, normalize)
        self.assertLess(retained, normalize)
        self.assertIn("HTTP_REQUEST_ENTITY_TOO_LARGE", intervention)
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT", mapper)
        self.assertLess(
            mapper.index("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT"),
            mapper.index("msconnector_rule_id_extract_from_message"),
        )
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT", phase2)
        self.assertIn("HTTP_REQUEST_ENTITY_TOO_LARGE", phase2)

    def test_nginx_classifies_before_rule_id_correlation_and_emits_body_limit(self) -> None:
        intervention = function_definition(
            self.nginx, "ngx_http_modsecurity_process_intervention"
        )
        mapper = function_definition(
            self.nginx, "ngx_http_modsecurity_contract_record_intervention"
        )
        event = function_definition(
            self.nginx_access, "ngx_http_modsecurity_request_intervention_log_event"
        )

        classifier = intervention.index(
            "msconnector_intervention_is_request_body_limit_rejection"
        )
        normalize = intervention.index("msconnector_intervention_normalize_status")
        retained = intervention.index(
            "ctx->native_request_body_limit_rejection =", classifier
        )
        self.assertLess(classifier, normalize)
        self.assertLess(retained, normalize)
        self.assertIn("NGX_HTTP_REQUEST_ENTITY_TOO_LARGE", intervention)
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT", mapper)
        self.assertLess(
            mapper.index("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT"),
            mapper.index("ctx->last_intervention_rule_id"),
        )
        self.assertIn("MSCONN_EVENT_BODY_LIMIT", event)
        self.assertIn('"body_limit"', event)
        self.assertIn('event.body.limit_outcome = body_limit ? "reject" : NULL;', event)

    def test_haproxy_preserves_the_exact_marker_through_legacy_spop(self) -> None:
        capture = function_definition(self.haproxy, "capture_intervention")
        mapper = function_definition(self.haproxy, "record_contract_decision")
        native_self_test = function_definition(
            self.haproxy, "haproxy_modsecurity_request_body_limit_self_test"
        )
        request_body_self_test = function_definition(
            self.haproxy, "haproxy_modsecurity_request_body_self_test"
        )
        legacy_ack = function_definition(self.haproxy_spop, "send_legacy_decision_ack")

        self.assertIn("msconnector_intervention_is_request_body_limit_rejection", capture)
        self.assertIn("decision->body_limit", capture)
        self.assertIn("decision->status = body_limit ? 413", capture)
        self.assertIn("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT", mapper)
        self.assertLess(
            mapper.index("MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT"),
            mapper.index("msconnector_decision_init(&common)"),
        )
        self.assertIn("SecRequestBodyLimit 8", native_self_test)
        self.assertIn("SecRequestBodyLimitAction Reject", native_self_test)
        self.assertIn("decision->body_limit != 0", native_self_test)
        self.assertIn("decision->status == 413", native_self_test)
        self.assertIn("decision->rule_id == 0", native_self_test)
        self.assertIn(
            "return haproxy_modsecurity_request_body_limit_self_test(decision);",
            request_body_self_test,
        )
        self.assertIn("decision->body_limit == 0", legacy_ack)
        self.assertIn("build_set_var_blocked_payload", legacy_ack)


if __name__ == "__main__":
    unittest.main()
