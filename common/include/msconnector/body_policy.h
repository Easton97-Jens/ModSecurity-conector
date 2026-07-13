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

/* A body-limit action is applied when observed bytes exceed the configured
 * inspection limit. `process_partial` passes only the remaining bounded bytes
 * to the engine; `reject` passes no bytes from the offending chunk. */
typedef enum msconnector_body_limit_action {
    MSCONNECTOR_BODY_LIMIT_ACTION_UNSET = -1,
    MSCONNECTOR_BODY_LIMIT_ACTION_REJECT = 0,
    MSCONNECTOR_BODY_LIMIT_ACTION_PROCESS_PARTIAL = 1
} msconnector_body_limit_action;

/* Canonical, payload-free limit observation names. `none` is represented by
 * an empty name so serializers can omit an inapplicable optional field. */
typedef enum msconnector_body_limit_outcome {
    MSCONNECTOR_BODY_LIMIT_OUTCOME_NONE = 0,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_AT_LIMIT,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_OVER_LIMIT,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL,
    MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT
} msconnector_body_limit_outcome;

typedef struct msconnector_body_limit_plan {
    size_t bytes_seen;
    size_t append_size;
    int truncated;
    msconnector_body_limit_outcome outcome;
} msconnector_body_limit_plan;

typedef struct msconnector_body_policy {
    msconnector_body_mode request_body_mode;
    msconnector_body_mode response_body_mode;
    size_t request_body_limit;
    size_t response_body_limit;
    msconnector_body_limit_action body_limit_action;
} msconnector_body_policy;

void msconnector_body_policy_init(msconnector_body_policy *policy);
const char *msconnector_body_mode_name(msconnector_body_mode mode);
int msconnector_body_mode_is_supported(msconnector_body_mode mode);

const char *msconnector_body_limit_action_name(
    msconnector_body_limit_action action);
int msconnector_body_limit_action_is_supported(
    msconnector_body_limit_action action);
int msconnector_body_limit_action_parse(
    const char *value,
    msconnector_body_limit_action *out);

const char *msconnector_body_limit_outcome_name(
    msconnector_body_limit_outcome outcome);

/* Plans a single borrowed body chunk without retaining it. bytes_seen is
 * updated even when `reject` rejects the offending chunk. bytes_inspected is
 * the amount already accepted by the engine and must never exceed limit.
 * Returns nonzero only when append_size is safe to pass to the engine. */
int msconnector_body_limit_plan_chunk(
    size_t bytes_seen,
    size_t bytes_inspected,
    size_t limit,
    msconnector_body_limit_action action,
    size_t chunk_size,
    msconnector_body_limit_plan *plan);

#ifdef __cplusplus
}
#endif

#endif
