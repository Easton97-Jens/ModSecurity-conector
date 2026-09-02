#!/usr/bin/env python3
"""Run the Apache/Common adoption suite plus review-hardened scoped guards."""
import sys

import apache_common_adoption_base as base


DOWNSTREAM_PASS = "rc = ap_pass_brigade(f->next, brigade);"
NORMALIZE_ASSIGNMENT = (
    "*eos_bucket = apache_phase4_normalize_response_brigade(*brigade);"
)
RC_NOT_SUCCESS = "if (rc != APR_SUCCESS)"
RETURN_APR_SUCCESS = "return APR_SUCCESS;"
RETURN_APR_EGENERAL = "return APR_EGENERAL;"
RETURN_VOID = "return;"
INTERVENTION_SENTINEL = "N_INTERVENTION_STATUS"
TERMINAL_EMITTING = "MSC_PHASE4_TERMINAL_OUTPUT_EMITTING"
TERMINAL_SEALED = "MSC_PHASE4_TERMINAL_OUTPUT_SEALED"
RESET_HTTP_STATUS = "r->status = HTTP_OK;"
RESET_STATUS_LINE = "r->status_line = NULL;"
AP_DIE_STATUS = "ap_die(status, r);"
FILTER_ATTACH_FAILURE = "r->connection) == NULL"
CONNECTION_ABORT = "r->connection->aborted = 1;"
CONNECTION_CLOSE = "r->connection->keepalive = AP_CONN_CLOSE;"
PHASE4_GATE_FAILED = "msr->response_phase4_gate_failed = 1;"
RECORD_INTERVENTION = "!msc_apache_contract_record_intervention_decision(msr)"
REQUEST_BODY_PHASE = "MSCONNECTOR_PHASE_REQUEST_BODY"
RESPONSE_HEADERS_PHASE = "MSCONNECTOR_PHASE_RESPONSE_HEADERS"
RESPONSE_BODY_PHASE = "MSCONNECTOR_PHASE_RESPONSE_BODY"
P2_PROCESS = "if (msc_process_request_body(msr->t) < 0)"
P3_PROCESS = 'if (msc_process_response_headers(msr->t, original_status, "HTTP 1.1") != 1)'
P4_PROCESS = "if (msc_process_response_body(msr->t) != 1)"
BUCKET_NEXT_LOOP = "bucket = APR_BUCKET_NEXT(bucket))"

request_body_finalizer = base.source_section(
    base.filters_c,
    "int msc_finalize_request_body(msc_t *msr, request_rec *r)",
    "static apr_status_t apache_input_filter_terminal_error",
)
phase4_normalize_helper = base.source_section(
    base.filters_c,
    "static apr_bucket *apache_phase4_normalize_response_brigade",
    "static int apache_phase4_error_bucket_status",
)
error_bucket_classifier = base.source_section(
    base.filters_c,
    "static int apache_phase4_error_bucket_status",
    "static int apache_phase3_snapshot_table_value",
)
response_start_classifier = base.source_section(
    base.filters_c,
    "static int apache_phase4_brigade_starts_response",
    "static apr_status_t apache_phase4_release_response_brigade",
)
phase4_terminal_guard = base.source_section(
    base.filters_c,
    "apr_status_t phase4_terminal_guard_filter",
    "static int apache_phase4_response_committed",
)
precommit_terminal_helper = base.source_section(
    base.filters_c,
    "static apr_status_t apache_send_precommit_terminal_error",
    "static apr_status_t apache_phase4_fail_closed",
)
phase4_fail_closed_helper = base.source_section(
    base.filters_c,
    "static apr_status_t apache_phase4_fail_closed(msc_t *msr, ap_filter_t *f,\n"
    "    apr_bucket_brigade *bb_in, const char *reason)\n{",
    "static apr_status_t apache_finish_unread_request_body",
)
input_eos_handler = base.source_section(
    base.filters_c,
    "static apr_status_t apache_input_filter_handle_eos",
    "apr_status_t input_filter",
)
prepare_response_brigade = base.source_section(
    base.filters_c,
    "static apr_status_t apache_output_filter_prepare_response_brigade",
    "static apr_status_t apache_phase4_finish_response_body",
)
phase4_finish_helper = base.source_section(
    base.filters_c,
    "static apr_status_t apache_phase4_finish_response_body",
    "static apr_status_t apache_phase4_handle_intervention",
)
phase3_headers_handler = base.source_section(
    base.filters_c,
    "static apr_status_t apache_output_filter_process_headers",
    "static apr_status_t apache_output_filter_prepare_response_brigade",
)
phase4_intervention_handler = base.source_section(
    base.filters_c,
    "static apr_status_t apache_phase4_handle_intervention",
    "static apr_status_t apache_output_filter_finish_response",
)
finish_response_handler = base.source_section(
    base.filters_c,
    "static apr_status_t apache_output_filter_finish_response",
    "apr_status_t output_filter",
)
redirect_terminal_emission = base.source_section(
    base.module_c,
    "static int apache_phase4_redirect_is_terminal_error_emission",
    "static void apache_phase4_fail_normal_redirect",
)
hook_insert_filter = base.source_section(
    base.module_c,
    "static void hook_insert_filter(request_rec *r)\n{",
    "static int apache_emit_phase1_intervention_event",
)
register_hooks = base.source_section(
    base.module_c,
    "static void msc_register_hooks",
    "module AP_MODULE_DECLARE_DATA security3_module",
)
release_after_pass = base.phase4_release_helper.partition(DOWNSTREAM_PASS)[2]
terminal_success_seal = (
    "if (terminal)\n"
    "    {\n"
    "        msr->response_phase4_terminal_output =\n"
    f"            {TERMINAL_SEALED};\n"
    "        apr_brigade_cleanup(brigade);\n"
    "    }"
)

review_guards: list[tuple[bool, str]] = [
    (
        base.tokens_in_order(
            request_body_finalizer,
            "if (msr->request_body_processed)",
            f"return {INTERVENTION_SENTINEL};",
            P2_PROCESS,
            f"msc_apache_contract_complete(msr,\n            {REQUEST_BODY_PHASE})",
            "msr->request_body_processed = 1;",
            "intervention = process_intervention(msr->t, r);",
            "return intervention;",
        ),
        "Apache Phase2 one-shot gate precedes processing, completion, intervention collection, and the collected result return",
    ),
    (
        base.tokens_in_order(
            phase4_normalize_helper,
            "for (bucket = APR_BRIGADE_FIRST(bb_in);",
            "bucket != APR_BRIGADE_SENTINEL(bb_in); bucket = next)",
            "next = APR_BUCKET_NEXT(bucket);",
            "if (eos != NULL)",
            "APR_BUCKET_REMOVE(bucket);",
            "apr_bucket_destroy(bucket);",
            "continue;",
            "if (APR_BUCKET_IS_EOS(bucket))",
            "eos = bucket;",
            "return eos;",
        )
        and base.tokens_in_order(
            prepare_response_brigade,
            NORMALIZE_ASSIGNMENT,
            "for (bucket = APR_BRIGADE_FIRST(*brigade);",
        ),
        "Apache Phase4 advances through normalization, destroys every suffix bucket after the first EOS, returns that EOS, and binds the prepare call site",
    ),
    (
        base.tokens_in_order(
            error_bucket_classifier,
            "first = APR_BRIGADE_FIRST(bb_in);",
            "for (bucket = first; bucket != APR_BRIGADE_SENTINEL(bb_in);",
            BUCKET_NEXT_LOOP,
            "if (!AP_BUCKET_IS_ERROR(bucket))",
            "if (bucket != first)",
            "return -1;",
            "error = (ap_bucket_error *)bucket->data;",
            "if (error == NULL || !ap_is_HTTP_ERROR(error->status))",
            "return -1;",
            "return error->status;",
        ),
        "Apache Phase4 error-bucket classifier scans the complete brigade, validates type, placement, and HTTP status, and returns the validated status",
    ),
    (
        base.tokens_in_order(
            response_start_classifier,
            "for (bucket = APR_BRIGADE_FIRST(brigade);",
            "bucket != APR_BRIGADE_SENTINEL(brigade);",
            BUCKET_NEXT_LOOP,
            "if (APR_BUCKET_IS_FLUSH(bucket) ||",
            "(!APR_BUCKET_IS_METADATA(bucket) && !APR_BUCKET_IS_EOS(bucket)))",
            "return 1;",
            "return 0;",
        ),
        "Apache response-start classifier detects every FLUSH or non-metadata body bucket before release",
    ),
    (
        base.tokens_in_order(
            prepare_response_brigade,
            "error_status = apache_phase4_error_bucket_status(*brigade);",
            "if (error_status < 0)",
            '"malformed response error bucket before Phase 4 decision"',
            "if (error_status > 0)",
            "ap_remove_output_filter(filter);",
            "return apache_send_precommit_terminal_error(msr, filter, *brigade,",
            "error_status);",
            NORMALIZE_ASSIGNMENT,
        ),
        "Apache Phase4 validates malformed and terminal error buckets before normalization",
    ),
    (
        base.tokens_in_order(
            prepare_response_brigade,
            NORMALIZE_ASSIGNMENT,
            "for (bucket = APR_BRIGADE_FIRST(*brigade);",
            "bucket != APR_BRIGADE_SENTINEL(*brigade);",
            BUCKET_NEXT_LOOP,
            "rc = apache_phase4_append_bucket(msr, conf, bucket);",
            RC_NOT_SUCCESS,
            "return apache_phase4_fail_closed(msr, filter, *brigade,",
            '"failed to append response body to libmodsecurity"',
        ),
        "Apache Phase4 walks every normalized bucket and fails closed on append errors",
    ),
    (
        base.tokens_in_order(
            phase4_finish_helper,
            P4_PROCESS,
            "return apache_phase4_fail_closed(msr, f, bb_in,",
            '"failed to finish response body in libmodsecurity"',
            f"msc_apache_contract_complete(msr, {RESPONSE_BODY_PHASE})",
            "msr->response_body_processed = 1;",
            "*intervention = process_intervention(msr->t, f->r);",
            f"if (*intervention != {INTERVENTION_SENTINEL} &&",
            RECORD_INTERVENTION,
            "MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE",
            '"could not record canonical P4 intervention decision"',
        ),
        "Apache Phase4 fails closed on engine finalization errors and completes before collecting intervention",
    ),
    (
        base.tokens_in_order(
            finish_response_handler,
            "if (!msr->response_body_processed)",
            "rc = apache_phase4_finish_response_body(msr, f, bb_in,",
            "&intervention);",
            RC_NOT_SUCCESS,
            f"if (intervention != {INTERVENTION_SENTINEL})",
            "rc = apache_phase4_handle_intervention(msr, conf, f, bb_in,",
            "intervention);",
            RC_NOT_SUCCESS,
            "return apache_phase4_release_response_brigade(msr, f, terminal_brigade,",
        ),
        "Apache Phase4 first-EOS gate finalizes before intervention dispatch and terminal release",
    ),
    (
        base.tokens_in_order(
            input_eos_handler,
            "intervention = msc_finalize_request_body(msr, r);",
            f"if (intervention != {INTERVENTION_SENTINEL})",
            "msr->request_body_intervention_sent = 1;",
            "ap_remove_input_filter(filter);",
            "return apache_input_filter_terminal_error(msr, r, intervention);",
            "msr->request_body_eos_released = 1;",
        ),
        "Apache Phase2 routes every EOS intervention to the terminal error path before successful EOS release",
    ),
    (
        base.tokens_in_order(
            phase3_headers_handler,
            "apache_add_response_headers(msr, r->err_headers_out);",
            "apache_add_response_headers(msr, r->headers_out);",
            P3_PROCESS,
            "ap_remove_output_filter(filter);",
            "return apache_send_precommit_terminal_error(msr, filter, brigade,",
            "HTTP_INTERNAL_SERVER_ERROR);",
            f"msc_apache_contract_complete(msr,\n            {RESPONSE_HEADERS_PHASE})",
            "msr->response_headers_processed = 1;",
            "intervention = process_intervention(msr->t, r);",
            f"if (intervention == {INTERVENTION_SENTINEL})",
            RETURN_APR_SUCCESS,
            f"if ({RECORD_INTERVENTION})",
            "wanted = msc_apache_contract_intervention_action(msr);",
            "apache_phase3_log_event(msr, r, wanted, wanted, original_status);",
            "return apache_send_precommit_terminal_error(msr, filter, brigade,",
            "intervention);",
        ),
        "Apache Phase3 populates both response-header tables, fails closed on engine error, completes, and then collects and enforces intervention",
    ),
    (
        base.tokens_in_order(
            phase4_intervention_handler,
            "msr->response.committed = apache_phase4_response_committed(msr, r);",
            "wanted = msc_apache_contract_intervention_action(msr);",
            "msconnector_late_intervention_policy_init(&policy);",
            "action = msconnector_late_intervention_resolve(&policy,",
            "msr->response.committed, msr->response.committed,",
            "conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);",
            "actual = apache_phase4_actual_action(action, wanted);",
            "if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)",
            RETURN_APR_SUCCESS,
            "if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)",
            "return apache_phase4_abort_response_connection(f);",
            '"response_not_committed"',
            "return apache_send_precommit_terminal_error(msr, f, NULL, intervention);",
        ),
        "Apache Phase4 derives commitment before policy resolution, bypasses only log-only, aborts strict committed responses, and denies before commit",
    ),
    (
        base.tokens_in_order(
            phase4_fail_closed_helper,
            "if (apache_phase4_response_committed(msr, r))",
            "return apache_phase4_abort_response_connection(f);",
            '"ModSecurity: Phase 4 response gate failed before response commit: %s"',
            "ap_remove_output_filter(f);",
            "return apache_send_precommit_terminal_error(msr, f, NULL,",
            "HTTP_INTERNAL_SERVER_ERROR);",
        ),
        "Apache Phase4 fail-closed helper removes the resource filter and emits a terminal error before commit",
    ),
    (
        base.tokens_in_order(
            base.phase4_release_helper,
            "starts_response = apache_phase4_brigade_starts_response(brigade);",
            "if ((starts_response || terminal) && !msr->response.committed &&",
            "msc_apache_contract_mark_response_committed(msr)",
            "msr->response.committed = 1;",
            DOWNSTREAM_PASS,
        )
        and base.tokens_in_order(
            release_after_pass,
            RC_NOT_SUCCESS,
            terminal_success_seal,
            "return rc;",
        ),
        "Apache progressive release derives response-start state, commits before output, and seals the successful terminal path afterward",
    ),
    (
        base.tokens_in_order(
            phase4_terminal_guard,
            "msc_t *msr = f != NULL ? (msc_t *)f->ctx : NULL;",
            "msr->response_phase4_terminal_output ==",
            TERMINAL_SEALED,
            "apr_brigade_cleanup(bb_in);",
            RETURN_APR_EGENERAL,
        ),
        "Apache protocol terminal guard reads its transaction context and rejects every brigade after output is sealed",
    ),
    (
        base.tokens_in_order(
            redirect_terminal_emission,
            "if (!apache_phase4_redirect_has_local_error_document_proof(msr, r))",
            "return 0;",
            "msr->response_phase4_terminal_error_redirect_seen = 1;",
            'apr_table_setn(r->notes, apache_phase4_terminal_error_redirect_note,',
            "return 1;",
        ),
        "Apache terminal-error redirect exception requires the local ErrorDocument proof before permitting the bounded redirect",
    ),
    (
        base.tokens_in_order(
            hook_insert_filter,
            "if (r->main != NULL)",
            RETURN_VOID,
            "if (r->prev != NULL)",
            "if (!apache_phase4_redirect_is_terminal_error_emission(msr, r))",
            "apache_phase4_fail_normal_redirect(msr, r,",
            '"request transaction cannot be safely rebound to the target URI");',
            RETURN_VOID,
            'ap_add_input_filter("MODSECURITY_IN", msr, r, r->connection);',
        ),
        "Apache excludes subrequests and rejects normal internal redirects before attaching request or response filters",
    ),
    (
        base.tokens_in_order(
            hook_insert_filter,
            'ap_add_output_filter("MODSECURITY_PHASE4_GUARD", msr, r,',
            FILTER_ATTACH_FAILURE,
            '"ModSecurity: unable to install the mandatory Phase 4 terminal guard; aborting request"',
            CONNECTION_ABORT,
            RETURN_VOID,
            'ap_add_output_filter("MODSECURITY_OUT", msr, r,',
            FILTER_ATTACH_FAILURE,
            PHASE4_GATE_FAILED,
            TERMINAL_SEALED,
            '"ModSecurity: unable to install the mandatory Phase 4 content filter; aborting request"',
            CONNECTION_CLOSE,
            CONNECTION_ABORT,
            RETURN_VOID,
        ),
        "Apache fails closed when either mandatory output filter cannot be attached",
    ),
    (
        base.tokens_in_order(
            register_hooks,
            'ap_register_output_filter("MODSECURITY_PHASE4_GUARD",',
            "phase4_terminal_guard_filter, NULL, AP_FTYPE_PROTOCOL);",
        ),
        "Apache registers the terminal guard as a protocol output filter",
    ),
    (
        base.tokens_in_order(
            base.process_intervention_helper,
            "z = msc_intervention(t, &intervention);",
            "if (z == 0)",
            f"return {INTERVENTION_SENTINEL};",
            "msconnector_intervention_has_redirect_url(intervention.url)",
            "intervention.status >= HTTP_MULTIPLE_CHOICES",
            "intervention.status < HTTP_BAD_REQUEST",
            'apr_table_setn(r->headers_out, "Location", location);',
            "result = intervention.status;",
            "goto cleanup;",
            f"if (intervention.status != {INTERVENTION_SENTINEL})",
            "result = intervention.status;",
            "cleanup:",
            "msc_release_intervention_buffers(&intervention);",
            "return result;",
        ),
        "Apache validates the native intervention result and preserves both redirect and non-redirect enforcement sinks",
    ),
    (
        base.tokens_in_order(
            base.input_filter_terminal_error,
            TERMINAL_EMITTING,
            RESET_HTTP_STATUS,
            RESET_STATUS_LINE,
            AP_DIE_STATUS,
            TERMINAL_SEALED,
            "return AP_FILTER_ERROR;",
        ),
        "Apache input terminal errors neutralize status, emit, and seal the protocol output guard in order",
    ),
    (
        base.tokens_in_order(
            precommit_terminal_helper,
            TERMINAL_EMITTING,
            RESET_HTTP_STATUS,
            RESET_STATUS_LINE,
            AP_DIE_STATUS,
            TERMINAL_SEALED,
            RETURN_APR_EGENERAL,
        ),
        "Apache pre-commit terminal errors neutralize status, emit, and seal the protocol output guard in order",
    ),
]

ok = True
for passed, message in review_guards:
    if passed:
        print(f"PASS: {message}")
    else:
        print(f"FAIL: {message}")
        ok = False

if not ok:
    sys.exit(1)
print("apache-common-adoption: scoped review guards passed")
