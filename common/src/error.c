#include "msconnector/error.h"
#include "msconnector/block_statuses.h"
#include "msconnector/http_status.h"
#include <stddef.h>

typedef struct msconnector_error_description {
    msconnector_error_code code;
    const char *name;
    const char *default_message;
} msconnector_error_description;

static const msconnector_error_description msconnector_error_descriptions[] = {
    {MSCONNECTOR_ERROR_NONE, "none", "No error"},
    {MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid_config", "Invalid connector configuration"},
    {MSCONNECTOR_ERROR_RULE_PARSE_FAILED, "rule_parse_failed", "ModSecurity rule parsing failed"},
    {MSCONNECTOR_ERROR_RULE_LOAD_FAILED, "rule_load_failed", "ModSecurity rule loading failed"},
    {MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, "runtime_unavailable", "Runtime is unavailable"},
    {MSCONNECTOR_ERROR_UNSUPPORTED_PHASE, "unsupported_phase", "Unsupported transaction phase"},
    {MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "unsupported_capability", "Requested capability is not implemented"},
    {MSCONNECTOR_ERROR_BODY_TOO_LARGE, "body_too_large", "Body is too large"},
    {MSCONNECTOR_ERROR_HEADER_TOO_LARGE, "header_too_large", "Header data is too large"},
    {MSCONNECTOR_ERROR_EVENT_TOO_LARGE, "event_too_large", "Event JSON is too large"},
    {MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE, "log_message_too_large", "Log message is too large"},
    {MSCONNECTOR_ERROR_HOST_API_FAILURE, "host_api_failure", "Host API failure"},
    {MSCONNECTOR_ERROR_MODSECURITY_FAILURE, "modsecurity_failure", "ModSecurity failure"},
    {MSCONNECTOR_ERROR_TIMEOUT, "timeout", "Operation timed out"},
    {MSCONNECTOR_ERROR_IO, "io", "I/O error"},
    {MSCONNECTOR_ERROR_INTERNAL, "internal", "Internal connector error"}
};

static const msconnector_error_description *msconnector_error_description_for_code(
    msconnector_error_code code) {
    size_t index;

    for (index = 0U;
         index < sizeof(msconnector_error_descriptions) / sizeof(msconnector_error_descriptions[0]);
         ++index) {
        if (msconnector_error_descriptions[index].code == code) {
            return &msconnector_error_descriptions[index];
        }
    }
    return NULL;
}

void msconnector_error_init(msconnector_error *error) { if (error != 0) { error->code = MSCONNECTOR_ERROR_NONE; error->message = 0; error->source = 0; } }
void msconnector_error_set(msconnector_error *error, msconnector_error_code code, const char *message, const char *source) { if (error != 0) { error->code = code; error->message = message; error->source = source; } }
const char *msconnector_error_code_name(msconnector_error_code code) {
    const msconnector_error_description *description = msconnector_error_description_for_code(code);

    if (description != NULL) {
        return description->name;
    }
    return "internal";
}
const char *msconnector_error_default_message(msconnector_error_code code) {
    const msconnector_error_description *description = msconnector_error_description_for_code(code);

    if (description != NULL) {
        return description->default_message;
    }
    return "Internal connector error";
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
    case MSCONNECTOR_ERROR_BODY_TOO_LARGE:
    case MSCONNECTOR_ERROR_HEADER_TOO_LARGE:
    case MSCONNECTOR_ERROR_EVENT_TOO_LARGE:
    case MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE: return 413;
    case MSCONNECTOR_ERROR_TIMEOUT: return 504;
    default: return MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }
}
int msconnector_error_is_fatal(msconnector_error_code code) { return code == MSCONNECTOR_ERROR_INVALID_CONFIG || code == MSCONNECTOR_ERROR_RULE_PARSE_FAILED || code == MSCONNECTOR_ERROR_RULE_LOAD_FAILED || code == MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE || code == MSCONNECTOR_ERROR_HOST_API_FAILURE || code == MSCONNECTOR_ERROR_MODSECURITY_FAILURE || code == MSCONNECTOR_ERROR_TIMEOUT || code == MSCONNECTOR_ERROR_IO || code == MSCONNECTOR_ERROR_INTERNAL; }
int msconnector_error_to_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id) {
    msconnector_error_code code;
    int http_status;
    if (event == 0 || error == 0 || error->code == MSCONNECTOR_ERROR_NONE) { return 0; }
    code = error->code;
    http_status = msconnector_error_http_status(code);
    msconnector_event_init(event);
    event->meta.connector = connector; event->meta.transaction_id = transaction_id;
    if (code == MSCONNECTOR_ERROR_RULE_PARSE_FAILED) {
        event->meta.message_id = MSCONN_EVENT_RULE_PARSE_ERROR;
    } else if (code == MSCONNECTOR_ERROR_INVALID_CONFIG) {
        event->meta.message_id = MSCONN_EVENT_CONFIG_ERROR;
    } else if (msconnector_error_status(code) == MSCONNECTOR_STATUS_UNSUPPORTED) {
        event->meta.message_id = MSCONN_EVENT_UNSUPPORTED_CAPABILITY;
    } else {
        event->meta.message_id = MSCONN_EVENT_INTERNAL_ERROR;
    }
    event->meta.message = error != 0 && error->message != 0 ? error->message : msconnector_error_default_message(code);
    event->meta.level = msconnector_event_default_level(event->meta.message_id);
    event->decision.status = msconnector_error_status(code); event->decision.action = "error"; event->decision.reason = event->meta.message;
    event->http.http_status = http_status; event->http.http_reason_phrase = msconnector_http_status_reason_phrase(http_status); event->http.http_default_message = msconnector_http_status_default_message(http_status);
    return 1;
}
