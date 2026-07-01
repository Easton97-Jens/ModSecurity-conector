#include "msconnector/decision_action.h"
#include "msconnector/intervention.h"

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
        return "abort_connection";
    default:
        return "unknown";
    }
}

msconnector_decision_action msconnector_decision_action_from_decision(
    const msconnector_decision *decision) {
    if (decision == 0) {
        return MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    }

    if (decision->intervention.redirect_url != 0) {
        return MSCONNECTOR_DECISION_ACTION_REDIRECT;
    }

    if (msconnector_intervention_is_disruptive(&decision->intervention)) {
        return MSCONNECTOR_DECISION_ACTION_DENY;
    }

    if (decision->status == MSCONNECTOR_STATUS_BLOCKED) {
        return MSCONNECTOR_DECISION_ACTION_DENY;
    }

    return MSCONNECTOR_DECISION_ACTION_ALLOW;
}

int msconnector_decision_action_is_disruptive(msconnector_decision_action action) {
    return action == MSCONNECTOR_DECISION_ACTION_DENY ||
        action == MSCONNECTOR_DECISION_ACTION_REDIRECT ||
        action == MSCONNECTOR_DECISION_ACTION_DROP ||
        action == MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
}
