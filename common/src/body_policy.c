#include "msconnector/body_policy.h"

#include <ctype.h>
#include <stdint.h>
#include <string.h>

static int token_equals(const char *value, const char *expected) {
    size_t index = 0U;
    if (value == NULL || expected == NULL || value[0] == '\0') {
        return 0;
    }
    while (value[index] != '\0' && expected[index] != '\0') {
        if (tolower((unsigned char)value[index]) !=
            tolower((unsigned char)expected[index])) {
            return 0;
        }
        ++index;
    }
    return value[index] == '\0' && expected[index] == '\0';
}

void msconnector_body_policy_init(msconnector_body_policy *policy) {
    if (policy == NULL) {
        return;
    }
    policy->request_body_mode = MSCONNECTOR_BODY_MODE_NONE;
    policy->response_body_mode = MSCONNECTOR_BODY_MODE_NONE;
    policy->request_body_limit = 0U;
    policy->response_body_limit = 0U;
    policy->body_limit_action = MSCONNECTOR_BODY_LIMIT_ACTION_REJECT;
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

const char *msconnector_body_limit_action_name(
    msconnector_body_limit_action action) {
    switch (action) {
    case MSCONNECTOR_BODY_LIMIT_ACTION_REJECT:
        return "reject";
    case MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL:
        return "process_partial";
    case MSCONNECTOR_BODY_LIMIT_ACTION_UNSET:
        return "unset";
    default:
        return "unknown";
    }
}

int msconnector_body_limit_action_is_supported(
    msconnector_body_limit_action action) {
    return action == MSCONNECTOR_BODY_LIMIT_ACTION_REJECT ||
        action == MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL;
}

int msconnector_body_limit_action_parse(
    const char *value,
    msconnector_body_limit_action *out) {
    msconnector_body_limit_action parsed;
    if (value == NULL) {
        return 0;
    }
    if (token_equals(value, "reject")) {
        parsed = MSCONNECTOR_BODY_LIMIT_ACTION_REJECT;
    } else if (token_equals(value, "process_partial") ||
        token_equals(value, "process-partial") ||
        token_equals(value, "processpartial")) {
        parsed = MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL;
    } else {
        return 0;
    }
    if (out != NULL) {
        *out = parsed;
    }
    return 1;
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

int msconnector_body_limit_plan_chunk(
    size_t bytes_seen,
    size_t bytes_inspected,
    size_t limit,
    msconnector_body_limit_action action,
    size_t chunk_size,
    msconnector_body_limit_plan *plan) {
    size_t next_seen;

    if (plan == NULL) {
        return 0;
    }
    memset(plan, 0, sizeof(*plan));
    plan->bytes_seen = bytes_seen;
    if (limit == 0U || bytes_inspected > bytes_seen ||
        bytes_inspected > limit ||
        !msconnector_body_limit_action_is_supported(action)) {
        return 0;
    }

    if (chunk_size > SIZE_MAX - bytes_seen) {
        plan->bytes_seen = SIZE_MAX;
        if (action == MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL) {
            plan->append_size = limit - bytes_inspected;
            plan->truncated = 1;
            plan->outcome = MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL;
            return 1;
        }
        plan->outcome = MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT;
        return 0;
    }

    next_seen = bytes_seen + chunk_size;
    plan->bytes_seen = next_seen;
    if (next_seen < limit) {
        plan->append_size = chunk_size;
        return 1;
    }
    if (next_seen == limit) {
        plan->append_size = chunk_size;
        plan->outcome = MSCONNECTOR_BODY_LIMIT_OUTCOME_AT_LIMIT;
        return 1;
    }

    if (action == MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL) {
        plan->append_size = limit - bytes_inspected;
        plan->truncated = 1;
        plan->outcome = MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL;
        return 1;
    }

    plan->outcome = MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT;
    return 0;
}
