#include "msconnector/dos_guard.h"

static void set_error(msconnector_error *error, msconnector_error_code code, const char *message) { msconnector_error_set(error, code, message, "common/dos_guard"); }
static int bounded_string_ok(const char *value, size_t max) {
    size_t i;
    if (value == 0) { return 1; }
    for (i = 0U; i <= max; ++i) { if (value[i] == '\0') { return 1; } }
    return 0;
}

int msconnector_dos_guard_check_request(const msconnector_request *request, const msconnector_resource_limits *limits, msconnector_error *error) {
    if (error != 0) { msconnector_error_init(error); }
    if (request == 0 || !msconnector_resource_limits_validate(limits)) { set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid request or resource limits"); return 0; }
    if (!bounded_string_ok(request->hostname, limits->max_log_message_length)) { set_error(error, MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE, "request metadata exceeds limit"); return 0; }
    if (!msconnector_resource_limits_headers_ok(request->headers, request->header_count, limits)) { set_error(error, MSCONNECTOR_ERROR_HEADER_TOO_LARGE, "request headers exceed resource limits"); return 0; }
    if (!msconnector_resource_limits_body_ok(request->body.size, limits->max_request_body_bytes)) { set_error(error, MSCONNECTOR_ERROR_BODY_TOO_LARGE, "request body exceeds resource limit"); return 0; }
    return 1;
}

int msconnector_dos_guard_check_response(const msconnector_response *response, const msconnector_resource_limits *limits, msconnector_error *error) {
    if (error != 0) { msconnector_error_init(error); }
    if (response == 0 || !msconnector_resource_limits_validate(limits)) { set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid response or resource limits"); return 0; }
    if (!msconnector_resource_limits_headers_ok(response->headers, response->header_count, limits)) { set_error(error, MSCONNECTOR_ERROR_HEADER_TOO_LARGE, "response headers exceed resource limits"); return 0; }
    if (!msconnector_resource_limits_body_ok(response->body.size, limits->max_response_body_bytes)) { set_error(error, MSCONNECTOR_ERROR_BODY_TOO_LARGE, "response body exceeds resource limit"); return 0; }
    return 1;
}

int msconnector_dos_guard_check_event_json_size(size_t size, const msconnector_resource_limits *limits, msconnector_error *error) {
    if (error != 0) { msconnector_error_init(error); }
    if (!msconnector_resource_limits_validate(limits)) { set_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid resource limits"); return 0; }
    if (size > limits->max_event_json_bytes) { set_error(error, MSCONNECTOR_ERROR_EVENT_TOO_LARGE, "event JSON exceeds resource limit"); return 0; }
    return 1;
}
