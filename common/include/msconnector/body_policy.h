#ifndef MSCONNECTOR_BODY_POLICY_H
#define MSCONNECTOR_BODY_POLICY_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Connector-neutral body support model; it does not imply that a particular
 * connector supports every mode. */
typedef enum msconnector_body_mode {
    MSCONNECTOR_BODY_MODE_NONE = 0,
    MSCONNECTOR_BODY_MODE_BUFFERED = 1,
    MSCONNECTOR_BODY_MODE_STREAMING = 2
} msconnector_body_mode;

/* Canonical, payload-free limit observation names. `none` is represented by
 * an empty name so serializers can omit an inapplicable optional field. */
typedef enum msconnector_body_limit_outcome {
    MSCONNECTOR_BODY_LIMIT_OUTCOME_NONE = 0,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_AT_LIMIT,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_OVER_LIMIT,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT
} msconnector_body_limit_outcome;

typedef struct msconnector_body_policy {
    msconnector_body_mode request_body_mode;
    msconnector_body_mode response_body_mode;
} msconnector_body_policy;

void msconnector_body_policy_init(msconnector_body_policy *policy);
const char *msconnector_body_mode_name(msconnector_body_mode mode);
int msconnector_body_mode_is_supported(msconnector_body_mode mode);

const char *msconnector_body_limit_outcome_name(
    msconnector_body_limit_outcome outcome);

#ifdef __cplusplus
}
#endif

#endif
