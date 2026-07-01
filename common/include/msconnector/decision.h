#ifndef MSCONNECTOR_DECISION_H
#define MSCONNECTOR_DECISION_H

#include "msconnector/block_statuses.h"
#include "msconnector/intervention.h"
#include "msconnector/status.h"
#ifndef MSCONNECTOR_TRANSACTION_H
#include "msconnector/transaction.h"
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_event msconnector_event;

typedef enum msconnector_decision_kind {
    MSCONNECTOR_DECISION_KIND_ALLOW = 0,
    MSCONNECTOR_DECISION_KIND_LOG_ONLY = 1,
    MSCONNECTOR_DECISION_KIND_DENY = 2,
    MSCONNECTOR_DECISION_KIND_REDIRECT = 3,
    MSCONNECTOR_DECISION_KIND_DROP = 4,
    MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT = 5,
    MSCONNECTOR_DECISION_KIND_ERROR = 6,
    MSCONNECTOR_DECISION_KIND_UNSUPPORTED = 7
} msconnector_decision_kind;

/* Connector-neutral decision model. Pointer fields are borrowed. */
typedef struct msconnector_decision {
    msconnector_decision_kind kind;
    enum msconnector_status status;
    enum msconnector_phase phase;
    int http_status;
    const char *redirect_url;
    const char *rule_id;
    const char *reason;
    const char *log_message;
    int disruptive;
    int late_intervention;
    msconnector_intervention intervention;
} msconnector_decision;

void msconnector_decision_init(msconnector_decision *decision);
const char *msconnector_decision_kind_name(msconnector_decision_kind kind);
int msconnector_decision_is_disruptive(const msconnector_decision *decision);
int msconnector_decision_is_deny(const msconnector_decision *decision);
int msconnector_decision_is_redirect(const msconnector_decision *decision);
int msconnector_decision_is_drop(const msconnector_decision *decision);
int msconnector_decision_is_connection_abort(const msconnector_decision *decision);
int msconnector_decision_is_allow(const msconnector_decision *decision);
int msconnector_decision_http_status(const msconnector_decision *decision);
void msconnector_decision_set_allow(msconnector_decision *decision);
void msconnector_decision_set_log_only(msconnector_decision *decision, const char *reason);
void msconnector_decision_set_deny(msconnector_decision *decision, int http_status, const char *rule_id, const char *reason);
void msconnector_decision_set_redirect(msconnector_decision *decision, int http_status, const char *url, const char *rule_id, const char *reason);
void msconnector_decision_set_drop(msconnector_decision *decision, const char *rule_id, const char *reason);
void msconnector_decision_set_connection_abort(msconnector_decision *decision, const char *rule_id, const char *reason);
void msconnector_decision_set_error(msconnector_decision *decision, int http_status, const char *reason);
void msconnector_decision_set_unsupported(msconnector_decision *decision, const char *reason);
int msconnector_decision_from_intervention(msconnector_decision *out, const msconnector_intervention *intervention, enum msconnector_phase phase, const char *rule_id, const char *reason);
int msconnector_decision_to_event(const msconnector_decision *decision, msconnector_event *event, const char *connector, const char *transaction_id);

/* Compatibility constructors retained for existing common helpers. */
msconnector_decision msconnector_decision_make(enum msconnector_status status, msconnector_intervention intervention, const char *rule_id, const char *reason);
msconnector_decision msconnector_decision_allow(const char *rule_id, const char *reason);
msconnector_decision msconnector_decision_block(int http_status, const char *rule_id, const char *reason);

#ifdef __cplusplus
}
#endif

#endif
