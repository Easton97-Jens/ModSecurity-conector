#ifndef MSCONNECTOR_LATE_INTERVENTION_H
#define MSCONNECTOR_LATE_INTERVENTION_H
#ifdef __cplusplus
extern "C" {
#endif
/* Common late-intervention decision model; connectors must explicitly implement any resulting behavior. */
typedef enum msconnector_late_intervention_action { MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY = 0, MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE = 1, MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION = 2 } msconnector_late_intervention_action;
typedef struct msconnector_late_intervention_policy { msconnector_late_intervention_action default_action; msconnector_late_intervention_action strict_action; } msconnector_late_intervention_policy;
void msconnector_late_intervention_policy_init(msconnector_late_intervention_policy *policy);
const char *msconnector_late_intervention_action_name(msconnector_late_intervention_action action);
msconnector_late_intervention_action msconnector_late_intervention_resolve(const msconnector_late_intervention_policy *policy, int response_headers_committed, int response_body_started, int strict_mode);
#ifdef __cplusplus
}
#endif
#endif
