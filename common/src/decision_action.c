#include "msconnector/decision_action.h"

const char *msconnector_decision_action_name(msconnector_decision_action action) {
    switch (action) {
    case MSCONNECTOR_DECISION_ACTION_ALLOW:
        return "allow";
    case MSCONNECTOR_DECISION_ACTION_DENY:
        return "deny";
    case MSCONNECTOR_DECISION_ACTION_REDIRECT:
        return "redirect";
    case MSCONNECTOR_DECISION_ACTION_DROP:
        return "drop";
    case MSCONNECTOR_DECISION_ACTION_LOG_ONLY:
        return "log_only";
    case MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION:
        return "connection_abort";
    case MSCONNECTOR_DECISION_ACTION_ERROR:
        return "error";
    case MSCONNECTOR_DECISION_ACTION_UNSUPPORTED:
        return "unsupported";
    default:
        return "unknown";
    }
}

msconnector_decision_action msconnector_decision_action_from_decision(
    const msconnector_decision *decision) {
    if (decision == 0) {
        return MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    }
    switch (decision->kind) {
    case MSCONNECTOR_DECISION_KIND_ALLOW:
        return MSCONNECTOR_DECISION_ACTION_ALLOW;
    case MSCONNECTOR_DECISION_KIND_LOG_ONLY:
        return MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    case MSCONNECTOR_DECISION_KIND_DENY:
        return MSCONNECTOR_DECISION_ACTION_DENY;
    case MSCONNECTOR_DECISION_KIND_REDIRECT:
        return MSCONNECTOR_DECISION_ACTION_REDIRECT;
    case MSCONNECTOR_DECISION_KIND_DROP:
        return MSCONNECTOR_DECISION_ACTION_DROP;
    case MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT:
        return MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
    case MSCONNECTOR_DECISION_KIND_ERROR:
        return MSCONNECTOR_DECISION_ACTION_ERROR;
    case MSCONNECTOR_DECISION_KIND_UNSUPPORTED:
        return MSCONNECTOR_DECISION_ACTION_UNSUPPORTED;
    default:
        return MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    }
}

int msconnector_decision_action_is_disruptive(msconnector_decision_action action) {
    return action == MSCONNECTOR_DECISION_ACTION_DENY ||
        action == MSCONNECTOR_DECISION_ACTION_REDIRECT ||
        action == MSCONNECTOR_DECISION_ACTION_DROP ||
        action == MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION ||
        action == MSCONNECTOR_DECISION_ACTION_ERROR;
}
