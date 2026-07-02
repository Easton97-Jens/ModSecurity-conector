#ifndef MSCONNECTOR_BLOCK_STATUSES_H
#define MSCONNECTOR_BLOCK_STATUSES_H

#include "msconnector/http_status.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MSCONNECTOR_DEFAULT_BLOCK_STATUS 403
#define MSCONNECTOR_DEFAULT_ERROR_STATUS 500
#define MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS 501

typedef struct msconnector_block_status_support {
    int status;
    int request_phase_supported;
    int response_phase_supported;
    int late_intervention_supported;
} msconnector_block_status_support;

int msconnector_block_status_is_allowed(int status);
int msconnector_block_status_normalize(int requested_status);
const char *msconnector_http_status_name(int status);

#ifdef __cplusplus
}
#endif

#endif
