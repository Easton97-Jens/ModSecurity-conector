#ifndef MSCONNECTOR_BODY_POLICY_H
#define MSCONNECTOR_BODY_POLICY_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Connector-neutral body support model; it does not imply any connector supports a mode. */
typedef enum msconnector_body_mode { MSCONNECTOR_BODY_MODE_NONE = 0, MSCONNECTOR_BODY_MODE_BUFFERED = 1, MSCONNECTOR_BODY_MODE_STREAMING = 2 } msconnector_body_mode;
typedef struct msconnector_body_policy { msconnector_body_mode request_body_mode; msconnector_body_mode response_body_mode; size_t request_body_limit; size_t response_body_limit; } msconnector_body_policy;
void msconnector_body_policy_init(msconnector_body_policy *policy);
const char *msconnector_body_mode_name(msconnector_body_mode mode);
int msconnector_body_mode_is_supported(msconnector_body_mode mode);
#ifdef __cplusplus
}
#endif
#endif
