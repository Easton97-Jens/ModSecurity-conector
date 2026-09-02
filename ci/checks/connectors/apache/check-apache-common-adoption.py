#!/usr/bin/env python3
"""Run the Apache/Common adoption suite plus review-hardened scoped guards."""
import sys

import apache_common_adoption_base as base


DOWNSTREAM_PASS = "rc = ap_pass_brigade(f->next, brigade);"
NORMALIZE_ASSIGNMENT = (
    "*eos_bucket = apache_phase4_normalize_response_brigade(*brigade);"
)
phase4_normalize_helper = base.source_section(
    base.filters_c,
    "static apr_bucket *apache_phase4_normalize_response_brigade",
    "static int apache_phase4_error_bucket_status",
)
phase4_terminal_guard = base.source_section(
    base.filters_c,
    "apr_status_t phase4_terminal_guard_filter",
    "static int apache_phase4_response_committed",
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
    "            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;\n"
    "        apr_brigade_cleanup(brigade);\n"
    "    }"
)

review_guards: list[tuple[bool, str]] = [
    (
        base.tokens_in_order(
            phase4_normalize_helper,
            "for (bucket = APR_BRIGADE_FIRST(bb_in);",
            "if (eos != NULL)",
            "APR_BUCKET_REMOVE(bucket);",
            "apr_bucket_destroy(bucket);",
            "continue;",
            "if (APR_BUCKET_IS_EOS(bucket))",
            "eos = bucket;",
        )
        and base.tokens_in_order(
            prepare_response_brigade,
            NORMALIZE_ASSIGNMENT,
            "for (bucket = APR_BRIGADE_FIRST(*brigade);",
        ),
        "Apache Phase4 normalizes at the prepare call site and destroys every suffix bucket after the first EOS",
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
            "rc = apache_phase4_append_bucket(msr, conf, bucket);",
            "if (rc != APR_SUCCESS)",
            "return apache_phase4_fail_closed(msr, filter, *brigade,",
            '"failed to append response body to libmodsecurity"',
        ),
        "Apache Phase4 appends every normalized bucket and fails closed on append errors",
    ),
    (
        base.tokens_in_order(
            base.phase4_release_helper,
            "msc_apache_contract_mark_response_committed(msr)",
            "msr->response.committed = 1;",
            DOWNSTREAM_PASS,
        )
        and base.tokens_in_order(
            release_after_pass,
            "if (rc != APR_SUCCESS)",
            terminal_success_seal,
            "return rc;",
        ),
        "Apache progressive release commits before output and seals the successful terminal path after downstream output",
    ),
    (
        base.tokens_in_order(
            phase4_terminal_guard,
            "msr->response_phase4_terminal_output ==",
            "MSC_PHASE4_TERMINAL_OUTPUT_SEALED",
            "apr_brigade_cleanup(bb_in);",
            "return APR_EGENERAL;",
        ),
        "Apache protocol terminal guard rejects every brigade after output is sealed",
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
            base.input_filter_terminal_error,
            "MSC_PHASE4_TERMINAL_OUTPUT_EMITTING",
            "r->status = HTTP_OK;",
            "r->status_line = NULL;",
            "ap_die(status, r);",
            "MSC_PHASE4_TERMINAL_OUTPUT_SEALED",
            "return AP_FILTER_ERROR;",
        ),
        "Apache input terminal errors neutralize status, emit, and seal the protocol output guard in order",
    ),
    (
        base.tokens_in_order(
            phase3_headers_handler,
            "msc_apache_contract_record_intervention_decision(msr)",
            "wanted = msc_apache_contract_intervention_action(msr);",
            "apache_phase3_log_event(msr, r, wanted, wanted, original_status);",
        )
        and base.tokens_in_order(
            phase4_intervention_handler,
            "wanted = msc_apache_contract_intervention_action(msr);",
            "msconnector_late_intervention_policy_init(&policy);",
            "actual = apache_phase4_actual_action(action, wanted);",
        ),
        "Apache P3 and P4 independently preserve the canonical redirect action",
    ),
    (
        base.tokens_in_order(
            phase4_finish_helper,
            "*intervention = process_intervention(msr->t, f->r);",
            "if (*intervention != N_INTERVENTION_STATUS &&",
            "!msc_apache_contract_record_intervention_decision(msr))",
            "MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE",
            '"could not record canonical P4 intervention decision"',
        ),
        "Apache Phase4 records disruptive decisions and fails closed on invalid engine correlation",
    ),
    (
        base.tokens_in_order(
            phase4_intervention_handler,
            "msconnector_late_intervention_policy_init(&policy);",
            "action = msconnector_late_intervention_resolve(&policy,",
            "msr->response.committed, msr->response.committed,",
            "conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);",
            "actual = apache_phase4_actual_action(action, wanted);",
        ),
        "Apache Phase4 resolves late intervention with the canonical strict-mode predicate",
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
