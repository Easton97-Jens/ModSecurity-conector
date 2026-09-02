#!/usr/bin/env python3
"""Run the Apache/Common adoption suite plus review-hardened scoped guards."""
import sys

import apache_common_adoption_base as base


phase4_normalize_helper = base.source_section(
    base.filters_c,
    "static apr_bucket *apache_phase4_normalize_response_brigade",
    "static int apache_phase4_error_bucket_status",
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
        ),
        "Apache Phase4 normalization destroys every suffix bucket after the first EOS",
    ),
    (
        base.tokens_in_order(
            base.phase4_release_helper,
            "msc_apache_contract_mark_response_committed(msr)",
            "msr->response.committed = 1;",
            "rc = ap_pass_brigade(f->next, brigade);",
        ),
        "Apache progressive release sets canonical and local committed state before downstream output",
    ),
    (
        base.tokens_in_order(
            base.input_filter_terminal_error,
            "MSC_PHASE4_TERMINAL_OUTPUT_EMITTING",
            "ap_die(status, r);",
            "MSC_PHASE4_TERMINAL_OUTPUT_SEALED",
            "return AP_FILTER_ERROR;",
        ),
        "Apache input terminal errors open, emit, and seal the protocol output guard in order",
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
