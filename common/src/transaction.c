#include "msconnector/transaction.h"

msconnector_decision msconnector_decision_make(
    enum msconnector_status status,
    msconnector_intervention intervention,
    const char *rule_id,
    const char *reason) {
    msconnector_decision decision;
    decision.status = status;
    decision.intervention = intervention;
    decision.rule_id = rule_id;
    decision.reason = reason;
    return decision;
}

msconnector_decision msconnector_decision_allow(
    const char *rule_id,
    const char *reason) {
    return msconnector_decision_make(
        MSCONNECTOR_STATUS_OK,
        msconnector_intervention_none(),
        rule_id,
        reason);
}

msconnector_decision msconnector_decision_block(
    int http_status,
    const char *rule_id,
    const char *reason) {
    return msconnector_decision_make(
        MSCONNECTOR_STATUS_BLOCKED,
        msconnector_intervention_make(1, http_status, 0, reason),
        rule_id,
        reason);
}
