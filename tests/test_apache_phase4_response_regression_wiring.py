#!/usr/bin/env python3
"""Guard the Parent-owned Apache Phase-4 response regression seam."""

from pathlib import Path
import unittest


ROOT = next(parent for parent in Path(__file__).resolve().parents if (parent / "Makefile").is_file())
HARNESS = ROOT / "connectors/apache/harness/run_apache_smoke.sh"
RUNNER = ROOT / "ci/runtime/lifecycle/run-apache-phase4-response-regression.sh"
CASE_ROOT = ROOT / "ci/runtime/lifecycle/cases/apache-phase4-response"
FILTERS = ROOT / "connectors/apache/src/msc_filters.c"
UTILS = ROOT / "connectors/apache/src/msc_utils.c"
ROGUE_HANDLER = ROOT / "connectors/apache/harness/mod_phase4_terminal_rogue.c"


class ApachePhase4ResponseRegressionWiringTest(unittest.TestCase):
    def test_harness_has_explicit_secure_and_vulnerable_barrier_expectations(self) -> None:
        source = HARNESS.read_text(encoding="utf-8")
        self.assertIn("MSCONNECTOR_PHASE4_SYNC_EXPECTATION", source)
        self.assertIn("bypass|precommit_deny|custom_mime_deny|allow|log_only|client_abort|engine_append_failure", source)
        self.assertIn("pre-commit deny released original response bytes before EOS", source)
        self.assertIn("custom-MIME pre-commit deny released original response bytes before EOS", source)
        self.assertIn("engine ProcessPartial failure", source)
        self.assertIn("bypass reproduction did not take the Safe log_only fallback", source)
        self.assertIn("APACHE_PHASE4_BODY_LIMIT", source)
        self.assertIn("assert_single_h1_status", source)
        self.assertIn("assert_text_response_headers", source)
        self.assertIn("--http1.1", source)

    def test_parent_runner_keeps_framework_catalog_unchanged(self) -> None:
        source = RUNNER.read_text(encoding="utf-8")
        self.assertIn("EXTRA_CASE_ROOTS", source)
        self.assertIn("MODSECURITY_RULE_PREAMBLE_FILE=", source)
        self.assertIn("FORCE_ALL_CASES=1", source)
        for mode in (
            "bypass|deny|allow|log-only|client-abort|empty|empty-deny|limit|custom-mime-deny|engine-limit",
            "redirect-bypass-h1|redirect-abort-h1|redirect-bypass-h2|redirect-abort-h2",
            "redirect-target-config-bypass-h1|redirect-target-config-abort-h1",
            "redirect-uri-bypass-h1|redirect-uri-abort-h1",
            "downstream-error-document-h1|downstream-error-document-h2|upstream-error-document-h1|upstream-error-document-h2",
            "nested-error-document-redirect-h1|preoutput-error-document-h1|preoutput-error-document-h2",
            "rogue-h1|rogue-allow-h1|rogue-p3-h1|rogue-p3-header-freeze-h1|rogue-p3-header-freeze-h2|rogue-error-document-h1|rogue-h2|rogue-error-document-h2",
        ):
            self.assertIn(mode, source)
        self.assertIn("apache_phase4_content_type_synchronized_upstream.py", source)
        self.assertIn("APACHE_PHASE4_ROGUE_TEST", source)
        self.assertNotIn("modules/ModSecurity-test-Framework/tests/cases", source)

    def test_regression_cases_cover_deny_allow_log_only_empty_and_limit(self) -> None:
        expected = {
            "precommit-deny.yaml": ("2190401", "deny,status:403", "SecAuditLog"),
            "allow.yaml": ("SecResponseBodyAccess On",),
            "log-only.yaml": ("2190402", "pass,log", "SecAuditLog"),
            "empty-allow.yaml": ('body: ""',),
            "empty-deny.yaml": ("2190403", "@rx ^$", "text/html", "deny,status:403", 'body: ""'),
            "limit-reject.yaml": ("body-exceeds-eight-byte-phase4-limit",),
            "custom-mime-deny.yaml": ("2190404", "application/vnd.apache-phase4+json", "deny,status:403"),
            "engine-limit-process-partial.yaml": ("2190405", "SecResponseBodyLimit 8", "SecResponseBodyLimitAction ProcessPartial"),
            "precommit-phase3-deny.yaml": ("2190406", "RESPONSE_HEADERS:Content-Type", "phase:3", "deny,status:403"),
            "precommit-phase3-header-freeze.yaml": ("2190407", "2190408", "RESPONSE_HEADERS:ETag", "phase:3", "deny,status:403"),
            "redirect-uri-policy.yaml": ("2190411", "REQUEST_URI", "RESPONSE_BODY", "deny,status:403"),
        }
        for name, markers in expected.items():
            with self.subTest(case=name):
                source = (CASE_ROOT / name).read_text(encoding="utf-8")
                for marker in markers:
                    self.assertIn(marker, source)

    def test_all_mime_phase4_gate_uses_setaside_and_terminal_cleanup(self) -> None:
        filters = FILTERS.read_text(encoding="utf-8")
        utils = UTILS.read_text(encoding="utf-8")
        self.assertIn("ap_save_brigade(f, &msr->response_brigade, &bb_in, r->pool)", filters)
        self.assertIn("apache_phase4_release_response_brigade", filters)
        self.assertIn("apache_phase4_normalize_response_brigade", filters)
        self.assertIn("APR_BUCKET_IS_FLUSH(bucket)", filters)
        self.assertIn("bucket->length == 0", filters)
        self.assertIn("MSCONNECTOR_BODY_LIMIT_ACTION_REJECT", filters)
        self.assertNotIn("apache_phase4_in_scope", filters)
        self.assertNotIn("response_body_scope_decided", filters)
        self.assertIn("SecResponseBodyMimeType selection", filters)
        self.assertIn("msc_append_response_body(msr->t,", filters)
        self.assertIn("plan.append_size) != 1", filters)
        self.assertIn("msc_process_response_body(msr->t) != 1", filters)
        self.assertIn("r->bytes_sent > 0", filters)
        self.assertIn("response_phase4_eos_released", filters)
        self.assertNotIn("|| r->eos_sent", filters)
        self.assertIn("missing saved response brigade", filters)
        self.assertIn("response_phase4_gate_failed", filters)
        self.assertIn("if (msr->response_phase4_eos_released)", filters)
        self.assertIn("r->connection->aborted = 1", filters)
        self.assertIn("phase4_terminal_guard_filter", filters)
        self.assertIn("MSC_PHASE4_TERMINAL_OUTPUT_EMITTING", filters)
        self.assertIn("MSC_PHASE4_TERMINAL_OUTPUT_SEALED", filters)
        self.assertIn("ap_register_output_filter(\"MODSECURITY_PHASE4_GUARD\"", (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8"))
        self.assertIn("ap_add_output_filter(\"MODSECURITY_PHASE4_GUARD\"", (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8"))
        self.assertIn("mandatory Phase 4 content filter; aborting request", (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8"))
        self.assertNotIn("ap_bucket_eoc_create", filters)
        self.assertNotIn("ap_flush_conn(r->connection)", filters)
        self.assertIn("msc_discard_response_brigade(msr);", utils)

    def test_rogue_handler_exercises_late_output_after_a_phase4_eos(self) -> None:
        harness = HARNESS.read_text(encoding="utf-8")
        handler = ROGUE_HANDLER.read_text(encoding="utf-8")
        self.assertIn("apr_bucket_immortal_create", handler)
        self.assertIn("phase4-rogue-prefix-", handler)
        self.assertIn("no-crs-response-body-marker", handler)
        self.assertIn("phase4-rogue-late-after-deny", handler)
        self.assertIn("phase4-rogue-suffix-after-eos", handler)
        self.assertIn("phase4_rogue_pass(r, \"phase4-rogue-late-after-deny\", 1, 1,", handler)
        self.assertIn("late_rc=0", harness)
        self.assertIn("--http2 --trace-ids", harness)
        self.assertIn("did not reuse the connection after denial", harness)
        self.assertIn("sole terminal Phase-4 response", harness)
        self.assertIn("APACHE_PHASE4_ROGUE_EXPECT", harness)
        self.assertIn("APACHE_PHASE4_ROGUE_PHASE", harness)
        self.assertIn("response_headers_before_commit", harness)
        self.assertIn("APACHE_PHASE4_ROGUE_HEADER_MUTATION", harness)
        self.assertIn("X-Phase3-Late", harness)
        self.assertIn("Phase-3 header-freeze H2", harness)
        self.assertIn("header_mutation=%d", handler)
        self.assertIn('"no-etag", "1"', handler)
        self.assertIn("phase3_etag[1] = 'X'", handler)
        self.assertIn("response_note_no_etag_snapshot", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("response_env_force_no_vary_snapshot", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("apr_table_clone", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("apache_phase3_clone_content_languages", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("response_header_only_snapshot", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("r->header_only = 1", handler)

    def test_internal_redirect_regression_has_explicit_pre_fix_bypass_and_post_fix_abort_modes(self) -> None:
        harness = HARNESS.read_text(encoding="utf-8")
        handler = ROGUE_HANDLER.read_text(encoding="utf-8")
        self.assertIn("APACHE_PHASE4_INTERNAL_REDIRECT_TEST", harness)
        self.assertIn("APACHE_PHASE4_INTERNAL_REDIRECT_EXPECT", harness)
        self.assertIn("send_phase4_internal_redirect_request", harness)
        self.assertIn("response_not_committed", harness)
        self.assertIn("phase4-internal-redirect", harness)
        self.assertIn("redirect-bypass-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-abort-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-bypass-h2", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-abort-h2", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-target-config-bypass-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-target-config-abort-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-uri-bypass-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("redirect-uri-abort-h1", RUNNER.read_text(encoding="utf-8"))
        self.assertIn("ap_internal_redirect", handler)
        self.assertIn("/__phase4_internal_redirect_target.txt", handler)
        connector = (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8")
        self.assertIn("apache_phase4_redirect_is_terminal_error_emission", connector)
        self.assertIn("apache_phase4_fail_normal_redirect", connector)
        self.assertIn("request transaction cannot be safely rebound to the target URI", connector)
        self.assertNotIn("apache_phase4_redirect_can_reattach", connector)
        self.assertNotIn("transaction_conf", connector)
        self.assertIn("apache_phase3_snapshot_response_state", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("apache_phase3_restore_response_state", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("assert_single_h2_status", harness)
        self.assertIn("phase4_terminal_test_uses_h2", harness)
        self.assertIn("APACHE_PHASE4_INTERNAL_REDIRECT_TARGET_CONFIG_TEST", harness)
        self.assertIn("APACHE_PHASE4_INTERNAL_REDIRECT_URI_POLICY_TEST", harness)
        self.assertIn("phase4_redirect_direct_rule_event_count", harness)
        self.assertIn("2190410", harness)
        self.assertIn("2190411", (CASE_ROOT / "redirect-uri-policy.yaml").read_text(encoding="utf-8"))
        self.assertNotIn("effective ModSecurity configuration changed", harness)

    def test_downstream_apache_error_document_is_a_bounded_allow_path(self) -> None:
        harness = HARNESS.read_text(encoding="utf-8")
        handler = ROGUE_HANDLER.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        connector = (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8")
        self.assertIn("APACHE_PHASE4_DOWNSTREAM_ERROR_TEST", harness)
        self.assertIn("APACHE_PHASE4_UPSTREAM_ERROR_TEST", harness)
        self.assertIn("send_phase4_downstream_error_request", harness)
        self.assertIn("send_phase4_upstream_error_request", harness)
        self.assertIn("phase4-downstream-error-document", harness)
        self.assertIn("downstream-error-document-h1", runner)
        self.assertIn("downstream-error-document-h2", runner)
        self.assertIn("upstream-error-document-h1", runner)
        self.assertIn("upstream-error-document-h2", runner)
        self.assertIn("phase4_downstream_error_filter", handler)
        self.assertIn("ap_bucket_error_create(HTTP_INTERNAL_SERVER_ERROR", handler)
        self.assertIn("PHASE4_DOWNSTREAM_ERROR", handler)
        self.assertIn("AP_FTYPE_CONTENT_SET - 2", handler)
        self.assertIn("no-crs-response-body-marker", handler)
        self.assertIn("phase4_upstream_error_pass", handler)
        self.assertIn("phase4-upstream-error", handler)
        self.assertIn("AP_BUCKET_IS_ERROR", FILTERS.read_text(encoding="utf-8"))
        self.assertIn("apache_phase4_error_bucket_status", FILTERS.read_text(encoding="utf-8"))
        filters = FILTERS.read_text(encoding="utf-8")
        self.assertIn("ap_die(status, r)", filters)
        self.assertIn("r->status = HTTP_OK", filters)
        self.assertIn("r->status_line = NULL", filters)
        self.assertNotIn("ap_send_error_response(r, 0)", filters)
        self.assertIn("REDIRECT_STATUS", connector)
        self.assertIn("ap_is_HTTP_ERROR(r->prev->status)", connector)
        self.assertIn("no_local_copy", connector)
        self.assertIn("response_phase4_terminal_error_redirect_seen", connector)
        self.assertIn("assert_phase4_error_document_headers", harness)
        self.assertIn("X-Phase4-Original-Response", handler)

    def test_error_document_redirect_boundary_is_single_hop_and_preoutput_fail_closed(self) -> None:
        harness = HARNESS.read_text(encoding="utf-8")
        handler = ROGUE_HANDLER.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        connector = (ROOT / "connectors/apache/src/mod_security3.c").read_text(encoding="utf-8")
        self.assertIn("APACHE_PHASE4_NESTED_ERROR_REDIRECT_TEST", harness)
        self.assertIn("APACHE_PHASE4_PREOUTPUT_ERROR_DOCUMENT_TEST", harness)
        self.assertIn("send_phase4_nested_error_document_redirect_request", harness)
        self.assertIn("send_phase4_preoutput_error_document_request", harness)
        self.assertIn("nested-error-document-redirect-h1", runner)
        self.assertIn("preoutput-error-document-h1", runner)
        self.assertIn("preoutput-error-document-h2", runner)
        self.assertIn("phase4_nested_error_document_redirect_handler", handler)
        self.assertIn("phase4_preoutput_error_document_handler", handler)
        self.assertIn("HTTP_NOT_FOUND before any response brigade", handler)
        self.assertIn("no_local_copy", connector)
        self.assertIn("response_phase4_terminal_error_redirect_seen", connector)
        self.assertIn("request transaction cannot be safely rebound to the target URI", harness)


if __name__ == "__main__":
    unittest.main()
