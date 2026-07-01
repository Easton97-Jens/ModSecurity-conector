#include "msconnector/late_intervention.h"

void msconnector_late_intervention_policy_init(
    msconnector_late_intervention_policy *policy) {
    if (policy == 0) {
        return;
    }

    policy->default_action = MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY;
    policy->strict_action = MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION;
}

const char *msconnector_late_intervention_action_name(
    msconnector_late_intervention_action action) {
    switch (action) {
    case MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY:
        return "log_only";
    case MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE:
        return "deny_if_possible";
    case MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION:
        return "abort_connection";
    default:
        return "unknown";
    }
}

msconnector_late_intervention_action msconnector_late_intervention_resolve(
    const msconnector_late_intervention_policy *policy,
    int response_headers_committed,
    int response_body_started,
    int strict_mode) {
    msconnector_late_intervention_policy fallback_policy;

    if (policy == 0) {
        msconnector_late_intervention_policy_init(&fallback_policy);
        policy = &fallback_policy;
    }

    if (strict_mode) {
        return policy->strict_action;
    }

    if (response_headers_committed || response_body_started) {
        return policy->default_action;
    }

    return MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE;
}
