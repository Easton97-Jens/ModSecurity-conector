#include "msconnector/decision.h"
#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include <string.h>

static int redirect_status(int status) { return status >= 300 && status < 400; }
static const char *kind_action(msconnector_decision_kind kind) {
    switch (kind) {
    case MSCONNECTOR_DECISION_KIND_ALLOW: return "allow";
    case MSCONNECTOR_DECISION_KIND_LOG_ONLY: return "log_only";
    case MSCONNECTOR_DECISION_KIND_DENY: return "deny";
    case MSCONNECTOR_DECISION_KIND_REDIRECT: return "redirect";
    case MSCONNECTOR_DECISION_KIND_DROP: return "drop";
    case MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT: return "connection_abort";
    case MSCONNECTOR_DECISION_KIND_ERROR: return "error";
    case MSCONNECTOR_DECISION_KIND_UNSUPPORTED: return "unsupported";
    default: return "unknown";
    }
}

void msconnector_decision_init(msconnector_decision *decision) {
    if (decision == 0) { return; }
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

const char *msconnector_decision_kind_name(msconnector_decision_kind kind) { return kind_action(kind); }
int msconnector_decision_is_disruptive(const msconnector_decision *decision) { return decision != 0 && decision->disruptive != 0; }
int msconnector_decision_is_deny(const msconnector_decision *decision) { return decision != 0 && decision->kind == MSCONNECTOR_DECISION_KIND_DENY; }
int msconnector_decision_is_redirect(const msconnector_decision *decision) { return decision != 0 && decision->kind == MSCONNECTOR_DECISION_KIND_REDIRECT; }
int msconnector_decision_is_drop(const msconnector_decision *decision) { return decision != 0 && decision->kind == MSCONNECTOR_DECISION_KIND_DROP; }
int msconnector_decision_is_connection_abort(const msconnector_decision *decision) { return decision != 0 && decision->kind == MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT; }
int msconnector_decision_is_allow(const msconnector_decision *decision) { return decision != 0 && decision->kind == MSCONNECTOR_DECISION_KIND_ALLOW; }
int msconnector_decision_http_status(const msconnector_decision *decision) { return decision == 0 ? 0 : decision->http_status; }

void msconnector_decision_set_allow(msconnector_decision *decision) { msconnector_decision_init(decision); }
void msconnector_decision_set_log_only(msconnector_decision *decision, const char *reason) {
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_LOG_ONLY; decision->reason = reason; decision->log_message = reason;
}
void msconnector_decision_set_deny(msconnector_decision *decision, int http_status, const char *rule_id, const char *reason) {
    int normalized = msconnector_block_status_normalize(http_status);
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_DENY; decision->status = MSCONNECTOR_STATUS_BLOCKED;
    decision->http_status = normalized; decision->rule_id = rule_id; decision->reason = reason;
    decision->disruptive = 1; decision->intervention = msconnector_intervention_make(1, normalized, 0, reason);
}
void msconnector_decision_set_redirect(msconnector_decision *decision, int http_status, const char *url, const char *rule_id, const char *reason) {
    int status = redirect_status(http_status) ? http_status : 302;
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_REDIRECT; decision->status = MSCONNECTOR_STATUS_BLOCKED;
    decision->http_status = status; decision->redirect_url = url; decision->rule_id = rule_id; decision->reason = reason;
    decision->disruptive = 1; decision->intervention = msconnector_intervention_make(1, status, url, reason);
}
void msconnector_decision_set_drop(msconnector_decision *decision, const char *rule_id, const char *reason) {
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_DROP; decision->status = MSCONNECTOR_STATUS_BLOCKED;
    decision->rule_id = rule_id; decision->reason = reason; decision->disruptive = 1; decision->intervention = msconnector_intervention_make(1, 0, 0, reason);
}
void msconnector_decision_set_connection_abort(msconnector_decision *decision, const char *rule_id, const char *reason) {
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT; decision->status = MSCONNECTOR_STATUS_BLOCKED;
    decision->rule_id = rule_id; decision->reason = reason; decision->disruptive = 1; decision->intervention = msconnector_intervention_make(1, 0, 0, reason);
}
void msconnector_decision_set_error(msconnector_decision *decision, int http_status, const char *reason) {
    int status = http_status == 0 ? MSCONNECTOR_DEFAULT_ERROR_STATUS : http_status;
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_ERROR; decision->status = MSCONNECTOR_STATUS_ERROR;
    decision->http_status = status; decision->reason = reason; decision->disruptive = msconnector_http_status_is_error(status);
}
void msconnector_decision_set_unsupported(msconnector_decision *decision, const char *reason) {
    msconnector_decision_init(decision); if (decision == 0) { return; }
    decision->kind = MSCONNECTOR_DECISION_KIND_UNSUPPORTED; decision->status = MSCONNECTOR_STATUS_UNSUPPORTED;
    decision->http_status = MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS; decision->reason = reason;
}
int msconnector_decision_from_intervention(msconnector_decision *out, const msconnector_intervention *intervention, enum msconnector_phase phase, const char *rule_id, const char *reason) {
    if (out == 0) { return 0; }
    if (!msconnector_intervention_is_disruptive(intervention)) { msconnector_decision_set_allow(out); out->phase = phase; out->rule_id = rule_id; out->reason = reason; return 1; }
    if (intervention->redirect_url != 0) { msconnector_decision_set_redirect(out, intervention->status, intervention->redirect_url, rule_id, reason); }
    else { msconnector_decision_set_deny(out, intervention->status, rule_id, reason); }
    out->phase = phase; out->log_message = intervention->log_message; return 1;
}
int msconnector_decision_to_event(const msconnector_decision *decision, msconnector_event *event, const char *connector, const char *transaction_id) {
    if (decision == 0 || event == 0) { return 0; }
    msconnector_event_init(event);
    event->meta.connector = connector; event->meta.transaction_id = transaction_id;
    event->decision.phase = decision->phase; event->decision.status = decision->status;
    event->decision.action = kind_action(decision->kind); event->decision.requested_action = kind_action(decision->kind); event->decision.actual_action = kind_action(decision->kind);
    event->decision.rule_id = decision->rule_id; event->decision.reason = decision->reason;
    event->http.http_status = decision->http_status;
    event->http.http_reason_phrase = msconnector_http_status_reason_phrase(decision->http_status);
    event->http.http_default_message = msconnector_http_status_default_message(decision->http_status);
    if (decision->kind == MSCONNECTOR_DECISION_KIND_DENY) { event->meta.message_id = MSCONN_EVENT_REQUEST_BLOCKED; }
    else if (decision->kind == MSCONNECTOR_DECISION_KIND_UNSUPPORTED) { event->meta.message_id = MSCONN_EVENT_UNSUPPORTED_CAPABILITY; }
    else if (decision->kind == MSCONNECTOR_DECISION_KIND_ERROR) { event->meta.message_id = MSCONN_EVENT_INTERNAL_ERROR; }
    else { event->meta.message_id = decision->disruptive ? MSCONN_EVENT_RESPONSE_BLOCKED : MSCONN_EVENT_REQUEST_BLOCKED; }
    event->meta.message = msconnector_event_default_message(event->meta.message_id);
    event->meta.level = msconnector_event_default_level(event->meta.message_id);
    event->flags.late_intervention = decision->late_intervention;
    return 1;
}
msconnector_decision msconnector_decision_make(enum msconnector_status status, msconnector_intervention intervention, const char *rule_id, const char *reason) {
    msconnector_decision decision; msconnector_decision_from_intervention(&decision, &intervention, MSCONNECTOR_PHASE_CONNECTION, rule_id, reason); decision.status = status; return decision;
}
msconnector_decision msconnector_decision_allow(const char *rule_id, const char *reason) { msconnector_decision decision; msconnector_decision_set_allow(&decision); decision.rule_id = rule_id; decision.reason = reason; return decision; }
msconnector_decision msconnector_decision_block(int http_status, const char *rule_id, const char *reason) { msconnector_decision decision; msconnector_decision_set_deny(&decision, http_status, rule_id, reason); return decision; }
