#ifndef MSCONNECTOR_ERROR_H
#define MSCONNECTOR_ERROR_H

#include "msconnector/event.h"
#include "msconnector/status.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum msconnector_error_code {
    MSCONNECTOR_ERROR_NONE = 0,
    MSCONNECTOR_ERROR_INVALID_CONFIG,
    MSCONNECTOR_ERROR_RULE_PARSE_FAILED,
    MSCONNECTOR_ERROR_RULE_LOAD_FAILED,
    MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
    MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
    MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY,
    MSCONNECTOR_ERROR_BODY_TOO_LARGE,
    MSCONNECTOR_ERROR_HEADER_TOO_LARGE,
    MSCONNECTOR_ERROR_EVENT_TOO_LARGE,
    MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE,
    MSCONNECTOR_ERROR_HOST_API_FAILURE,
    MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
    MSCONNECTOR_ERROR_TIMEOUT,
    MSCONNECTOR_ERROR_IO,
    MSCONNECTOR_ERROR_INTERNAL
} msconnector_error_code;

typedef struct msconnector_error { msconnector_error_code code; const char *message; const char *source; } msconnector_error;

void msconnector_error_init(msconnector_error *error);
void msconnector_error_set(msconnector_error *error, msconnector_error_code code, const char *message, const char *source);
const char *msconnector_error_code_name(msconnector_error_code code);
const char *msconnector_error_default_message(msconnector_error_code code);
enum msconnector_status msconnector_error_status(msconnector_error_code code);
int msconnector_error_http_status(msconnector_error_code code);
int msconnector_error_is_fatal(msconnector_error_code code);
int msconnector_error_to_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id);

#ifdef __cplusplus
}
#endif

#endif
