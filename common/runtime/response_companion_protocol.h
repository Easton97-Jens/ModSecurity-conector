#ifndef MSCONNECTOR_RESPONSE_COMPANION_PROTOCOL_H
#define MSCONNECTOR_RESPONSE_COMPANION_PROTOCOL_H

#include "msconnector/decision_action.h"

/* RELEASE eligibility after acknowledged P3 OUTCOME. This does not change
 * OUTCOME acceptance: it prevents an incompatible host observation from
 * being used as authority for normal precommit policy cleanup. */
static inline int msconnector_response_companion_precommit_outcome_matches(
    msconnector_decision_kind kind, int native_status,
    msconnector_decision_action action, int visible_status, int connection_aborted)
{
    if (action == MSCONNECTOR_DECISION_ACTION_DENY) {
        if (kind == MSCONNECTOR_DECISION_KIND_DENY) {
            return visible_status == native_status;
        }
        /* HTX translates unsupported disruptive P3 replies to its
         * deterministic fail-closed 503 response. */
        return kind >= MSCONNECTOR_DECISION_KIND_REDIRECT &&
            kind <= MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT && visible_status == 503;
    }
    if (action == MSCONNECTOR_DECISION_ACTION_REDIRECT) {
        return kind == MSCONNECTOR_DECISION_KIND_REDIRECT && visible_status == native_status;
    }
    if (action == MSCONNECTOR_DECISION_ACTION_DROP) {
        return kind == MSCONNECTOR_DECISION_KIND_DROP && connection_aborted && visible_status == 0;
    }
    if (action == MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION) {
        return kind == MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT && connection_aborted && visible_status == 0;
    }
    return 0;
}

#endif
