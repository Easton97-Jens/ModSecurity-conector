#include "msconnector/body_policy.h"
void msconnector_body_policy_init(msconnector_body_policy *policy) { if (policy) { policy->request_body_mode = MSCONNECTOR_BODY_MODE_NONE; policy->response_body_mode = MSCONNECTOR_BODY_MODE_NONE; policy->request_body_limit = 0; policy->response_body_limit = 0; } }
const char *msconnector_body_mode_name(msconnector_body_mode mode) { switch (mode) { case MSCONNECTOR_BODY_MODE_NONE: return "none"; case MSCONNECTOR_BODY_MODE_BUFFERED: return "buffered"; case MSCONNECTOR_BODY_MODE_STREAMING: return "streaming"; } return "unknown"; }
int msconnector_body_mode_is_supported(msconnector_body_mode mode) { return mode == MSCONNECTOR_BODY_MODE_NONE || mode == MSCONNECTOR_BODY_MODE_BUFFERED || mode == MSCONNECTOR_BODY_MODE_STREAMING; }
