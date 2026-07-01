#include "msconnector/error.h"
#include "msconnector/block_statuses.h"
#include "msconnector/http_status.h"
#include <stddef.h>

void msconnector_error_init(msconnector_error *error) { if (error != 0) { error->code = MSCONNECTOR_ERROR_NONE; error->message = 0; error->source = 0; } }
void msconnector_error_set(msconnector_error *error, msconnector_error_code code, const char *message, const char *source) { if (error != 0) { error->code = code; error->message = message; error->source = source; } }
const char *msconnector_error_code_name(msconnector_error_code code) {
    switch (code) {
    case MSCONNECTOR_ERROR_NONE: return "none";
    case MSCONNECTOR_ERROR_INVALID_CONFIG: return "invalid_config";
    case MSCONNECTOR_ERROR_RULE_PARSE_FAILED: return "rule_parse_failed";
    case MSCONNECTOR_ERROR_RULE_LOAD_FAILED: return "rule_load_failed";
    case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE: return "runtime_unavailable";
    case MSCONNECTOR_ERROR_UNSUPPORTED_PHASE: return "unsupported_phase";
    case MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY: return "unsupported_capability";
    case MSCONNECTOR_ERROR_BODY_TOO_LARGE: return "body_too_large";
    case MSCONNECTOR_ERROR_HOST_API_FAILURE: return "host_api_failure";
    case MSCONNECTOR_ERROR_MODSECURITY_FAILURE: return "modsecurity_failure";
    case MSCONNECTOR_ERROR_TIMEOUT: return "timeout";
    case MSCONNECTOR_ERROR_IO: return "io";
    case MSCONNECTOR_ERROR_INTERNAL: return "internal";
    default: return "internal";
    }
}
const char *msconnector_error_default_message(msconnector_error_code code) {
    switch (code) {
    case MSCONNECTOR_ERROR_NONE: return "No error";
    case MSCONNECTOR_ERROR_INVALID_CONFIG: return "Invalid connector configuration";
    case MSCONNECTOR_ERROR_RULE_PARSE_FAILED: return "ModSecurity rule parsing failed";
    case MSCONNECTOR_ERROR_RULE_LOAD_FAILED: return "ModSecurity rule loading failed";
    case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE: return "Runtime is unavailable";
    case MSCONNECTOR_ERROR_UNSUPPORTED_PHASE: return "Unsupported transaction phase";
    case MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY: return "Requested capability is not implemented";
    case MSCONNECTOR_ERROR_BODY_TOO_LARGE: return "Body is too large";
    case MSCONNECTOR_ERROR_HOST_API_FAILURE: return "Host API failure";
    case MSCONNECTOR_ERROR_MODSECURITY_FAILURE: return "ModSecurity failure";
    case MSCONNECTOR_ERROR_TIMEOUT: return "Operation timed out";
    case MSCONNECTOR_ERROR_IO: return "I/O error";
    case MSCONNECTOR_ERROR_INTERNAL: return "Internal connector error";
    default: return "Internal connector error";
    }
}
enum msconnector_status msconnector_error_status(msconnector_error_code code) {
    if (code == MSCONNECTOR_ERROR_NONE) { return MSCONNECTOR_STATUS_OK; }
    if (code == MSCONNECTOR_ERROR_UNSUPPORTED_PHASE || code == MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY) { return MSCONNECTOR_STATUS_UNSUPPORTED; }
    return MSCONNECTOR_STATUS_ERROR;
}
int msconnector_error_http_status(msconnector_error_code code) {
    switch (code) {
    case MSCONNECTOR_ERROR_NONE: return 0;
    case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE: return 503;
    case MSCONNECTOR_ERROR_UNSUPPORTED_PHASE:
    case MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY: return MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS;
    case MSCONNECTOR_ERROR_BODY_TOO_LARGE: return 413;
    case MSCONNECTOR_ERROR_TIMEOUT: return 504;
    default: return MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }
}
int msconnector_error_is_fatal(msconnector_error_code code) { return code == MSCONNECTOR_ERROR_INVALID_CONFIG || code == MSCONNECTOR_ERROR_RULE_PARSE_FAILED || code == MSCONNECTOR_ERROR_RULE_LOAD_FAILED || code == MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE || code == MSCONNECTOR_ERROR_HOST_API_FAILURE || code == MSCONNECTOR_ERROR_MODSECURITY_FAILURE || code == MSCONNECTOR_ERROR_TIMEOUT || code == MSCONNECTOR_ERROR_IO || code == MSCONNECTOR_ERROR_INTERNAL; }
int msconnector_error_to_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id) {
    msconnector_error_code code;
    int http_status;
    if (event == 0) { return 0; }
    code = error == 0 ? MSCONNECTOR_ERROR_INTERNAL : error->code;
    http_status = msconnector_error_http_status(code);
    msconnector_event_init(event);
    event->meta.connector = connector; event->meta.transaction_id = transaction_id;
    event->meta.message_id = code == MSCONNECTOR_ERROR_RULE_PARSE_FAILED ? MSCONN_EVENT_RULE_PARSE_ERROR : (code == MSCONNECTOR_ERROR_INVALID_CONFIG ? MSCONN_EVENT_CONFIG_ERROR : (msconnector_error_status(code) == MSCONNECTOR_STATUS_UNSUPPORTED ? MSCONN_EVENT_UNSUPPORTED_CAPABILITY : MSCONN_EVENT_INTERNAL_ERROR));
    event->meta.message = error != 0 && error->message != 0 ? error->message : msconnector_error_default_message(code);
    event->meta.level = msconnector_event_default_level(event->meta.message_id);
    event->decision.status = msconnector_error_status(code); event->decision.action = "error"; event->decision.reason = event->meta.message;
    event->http.http_status = http_status; event->http.http_reason_phrase = msconnector_http_status_reason_phrase(http_status); event->http.http_default_message = msconnector_http_status_default_message(http_status);
    return 1;
}
