#ifndef MSCONNECTOR_LATE_INTERVENTION_H
#define MSCONNECTOR_LATE_INTERVENTION_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif
/*
 * Common late-intervention decision model.  It models only host-observed
 * protocol/lifecycle facts; connectors retain ownership of transport calls.
 * In particular, a stream reset is never inferred from a protocol label alone.
 */
typedef enum msconnector_protocol_kind {
    MSCONNECTOR_PROTOCOL_UNKNOWN = 0,
    MSCONNECTOR_PROTOCOL_HTTP_1_1 = 1,
    MSCONNECTOR_PROTOCOL_HTTP_2 = 2,
    MSCONNECTOR_PROTOCOL_HTTP_3 = 3
} msconnector_protocol_kind;

typedef enum msconnector_late_intervention_action {
    MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY = 0,
    MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE = 1,
    MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION = 2,
    MSCONNECTOR_LATE_INTERVENTION_STREAM_RESET = 3
} msconnector_late_intervention_action;

typedef struct msconnector_late_intervention_policy {
    msconnector_late_intervention_action default_action;
    msconnector_late_intervention_action strict_action;
} msconnector_late_intervention_policy;

typedef struct msconnector_late_intervention_context {
    msconnector_protocol_kind protocol;
    uint64_t stream_id;
    int has_stream_id;
    int input_ended;
    int output_ended;
    int response_headers_committed;
    int response_body_started;
    int stream_reset_supported;
} msconnector_late_intervention_context;

const char *msconnector_protocol_kind_name(msconnector_protocol_kind protocol);
msconnector_protocol_kind msconnector_protocol_kind_parse(const char *value);
int msconnector_protocol_is_multiplexed(msconnector_protocol_kind protocol);
void msconnector_late_intervention_policy_init(msconnector_late_intervention_policy *policy);
void msconnector_late_intervention_context_init(
    msconnector_late_intervention_context *context);
const char *msconnector_late_intervention_action_name(msconnector_late_intervention_action action);
msconnector_late_intervention_action msconnector_late_intervention_resolve(const msconnector_late_intervention_policy *policy, int response_headers_committed, int response_body_started, int strict_mode);
msconnector_late_intervention_action msconnector_late_intervention_resolve_for_context(
    const msconnector_late_intervention_policy *policy,
    const msconnector_late_intervention_context *context,
    int strict_mode);
#ifdef __cplusplus
}
#endif
#endif
