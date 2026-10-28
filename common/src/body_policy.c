#include "msconnector/body_policy.h"

#include <ctype.h>
#include <stdint.h>
#include <string.h>

void msconnector_body_policy_init(msconnector_body_policy *policy) {
    if (policy == NULL) {
        return;
    }
    policy->request_body_mode = MSCONNECTOR_BODY_MODE_NONE;
    policy->response_body_mode = MSCONNECTOR_BODY_MODE_NONE;
}

const char *msconnector_body_mode_name(msconnector_body_mode mode) {
    switch (mode) {
    case MSCONNECTOR_BODY_MODE_NONE:
        return "none";
    case MSCONNECTOR_BODY_MODE_BUFFERED:
        return "buffered";
    case MSCONNECTOR_BODY_MODE_STREAMING:
        return "streaming";
    default:
        return "unknown";
    }
}

int msconnector_body_mode_is_supported(msconnector_body_mode mode) {
    return mode == MSCONNECTOR_BODY_MODE_NONE ||
        mode == MSCONNECTOR_BODY_MODE_BUFFERED ||
        mode == MSCONNECTOR_BODY_MODE_STREAMING;
}

const char *msconnector_body_limit_outcome_name(
    msconnector_body_limit_outcome outcome) {
    switch (outcome) {
    case MSCONNECTOR_BODY_LIMIT_OUTCOME_NONE:
        return "";
    case MSCONNECTOR_BODY_LIMIT_OUTCOME_AT_LIMIT:
        return "at_limit";
    case MSCONNECTOR_BODY_LIMIT_OUTCOME_OVER_LIMIT:
        return "over_limit";
    case MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL:
        return "process_partial";
    case MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT:
        return "reject";
    default:
        return "unknown";
    }
}
