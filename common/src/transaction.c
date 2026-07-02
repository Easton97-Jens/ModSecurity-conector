#include "msconnector/transaction.h"

static msconnector_decision_kind kind_from_status(enum msconnector_status status)
{
    switch (status) {
    case MSCONNECTOR_STATUS_BLOCKED:
        return MSCONNECTOR_DECISION_KIND_DENY;
    case MSCONNECTOR_STATUS_ERROR:
        return MSCONNECTOR_DECISION_KIND_ERROR;
    case MSCONNECTOR_STATUS_UNSUPPORTED:
        return MSCONNECTOR_DECISION_KIND_UNSUPPORTED;
    case MSCONNECTOR_STATUS_OK:
    default:
        return MSCONNECTOR_DECISION_KIND_ALLOW;
    }
}

static void decision_constructor_init(msconnector_decision *decision)
{
    if (decision == 0) {
        return;
    }
    decision->kind = MSCONNECTOR_DECISION_KIND_ALLOW;
    decision->status = MSCONNECTOR_STATUS_OK;
    decision->phase = MSCONNECTOR_PHASE_CONNECTION;
    decision->http_status = 0;
    decision->redirect_url = 0;
    decision->rule_id = 0;
    decision->reason = 0;
    decision->log_message = 0;
    decision->disruptive = 0;
    decision->late_intervention = 0;
    decision->intervention = msconnector_intervention_none();
}

msconnector_decision msconnector_decision_make(
    enum msconnector_status status,
    msconnector_intervention intervention,
    const char *rule_id,
    const char *reason)
{
    msconnector_decision decision;

    decision_constructor_init(&decision);
    decision.status = status;
    decision.kind = kind_from_status(status);
    decision.phase = MSCONNECTOR_PHASE_CONNECTION;
    decision.rule_id = rule_id;
    decision.reason = reason;
    decision.log_message = intervention.log_message;
    decision.intervention = intervention;
    if (msconnector_intervention_is_disruptive(&intervention)) {
        decision.kind = intervention.redirect_url != 0 ?
            MSCONNECTOR_DECISION_KIND_REDIRECT : MSCONNECTOR_DECISION_KIND_DENY;
        decision.disruptive = 1;
        decision.http_status = intervention.status;
        decision.redirect_url = intervention.redirect_url;
    } else if (status == MSCONNECTOR_STATUS_BLOCKED || status == MSCONNECTOR_STATUS_ERROR) {
        decision.disruptive = 1;
    }
    return decision;
}

msconnector_decision msconnector_decision_allow(const char *rule_id, const char *reason)
{
    msconnector_decision decision;

    decision_constructor_init(&decision);
    decision.rule_id = rule_id;
    decision.reason = reason;
    return decision;
}

msconnector_decision msconnector_decision_block(int http_status, const char *rule_id, const char *reason)
{
    msconnector_decision decision;

    decision_constructor_init(&decision);
    decision.kind = MSCONNECTOR_DECISION_KIND_DENY;
    decision.status = MSCONNECTOR_STATUS_BLOCKED;
    decision.http_status = http_status == 0 ? MSCONNECTOR_DEFAULT_BLOCK_STATUS : http_status;
    decision.rule_id = rule_id;
    decision.reason = reason;
    decision.disruptive = 1;
    decision.intervention = msconnector_intervention_make(1, decision.http_status, 0, reason);
    return decision;
}
