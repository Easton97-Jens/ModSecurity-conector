#ifndef MSCONNECTOR_DECISION_ACTION_H
#define MSCONNECTOR_DECISION_ACTION_H
#include "msconnector/decision.h"
#ifdef __cplusplus
extern "C" {
#endif
/* High-level connector-neutral action view derived from decisions/interventions. */
typedef enum msconnector_decision_action { MSCONNECTOR_DECISION_ACTION_ALLOW = 0, MSCONNECTOR_DECISION_ACTION_DENY = 1, MSCONNECTOR_DECISION_ACTION_REDIRECT = 2, MSCONNECTOR_DECISION_ACTION_DROP = 3, MSCONNECTOR_DECISION_ACTION_LOG_ONLY = 4, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION = 5, MSCONNECTOR_DECISION_ACTION_ERROR = 6, MSCONNECTOR_DECISION_ACTION_UNSUPPORTED = 7 } msconnector_decision_action;
const char *msconnector_decision_action_name(msconnector_decision_action action);
msconnector_decision_action msconnector_decision_action_from_decision(const msconnector_decision *decision);
int msconnector_decision_action_is_disruptive(msconnector_decision_action action);
#ifdef __cplusplus
}
#endif
#endif
