#include "msconnector/blocking.h"

const char *msconnector_block_action_name(enum msconnector_block_action action) {
    switch (action) {
    case MSCONNECTOR_BLOCK_ACTION_DENY:
        return "deny";
    case MSCONNECTOR_BLOCK_ACTION_REDIRECT:
        return "redirect";
    case MSCONNECTOR_BLOCK_ACTION_DROP:
        return "drop";
    case MSCONNECTOR_BLOCK_ACTION_LOG_ONLY:
        return "log_only";
    case MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION:
        return "abort_connection";
    default:
        return "deny";
    }
}

int msconnector_block_action_is_disruptive(enum msconnector_block_action action) {
    return action == MSCONNECTOR_BLOCK_ACTION_DENY ||
        action == MSCONNECTOR_BLOCK_ACTION_REDIRECT ||
        action == MSCONNECTOR_BLOCK_ACTION_DROP ||
        action == MSCONNECTOR_BLOCK_ACTION_ABORT_CONNECTION;
}

msconnector_blocking_policy msconnector_blocking_policy_make(
    enum msconnector_block_action action,
    int requested_status) {
    msconnector_blocking_policy policy;
    policy.action = action;
    policy.status = msconnector_block_status_normalize(requested_status);
    if (!msconnector_block_action_is_disruptive(action)) {
        policy.status = 0;
    }
    return policy;
}
