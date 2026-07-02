#include "msconnector/resource_limits.h"
#include "msconnector/limits.h"

void msconnector_resource_limits_init(msconnector_resource_limits *limits) {
    if (limits == 0) { return; }
    limits->max_header_count = MSCONNECTOR_MAX_HEADER_COUNT;
    limits->max_header_name_size = MSCONNECTOR_MAX_HEADER_NAME_LENGTH;
    limits->max_header_value_size = MSCONNECTOR_MAX_HEADER_VALUE_LENGTH;
    limits->max_total_header_bytes = MSCONNECTOR_MAX_TOTAL_HEADER_BYTES;
    limits->max_request_body_bytes = MSCONNECTOR_MAX_BODY_BUFFER_SIZE;
    limits->max_response_body_bytes = MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE;
    limits->max_event_json_bytes = MSCONNECTOR_MAX_EVENT_JSON_BYTES;
    limits->max_transaction_id_length = MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH;
    limits->max_rule_id_length = MSCONNECTOR_MAX_RULE_ID_LENGTH;
    limits->max_log_message_length = MSCONNECTOR_MAX_LOG_MESSAGE_LENGTH;
}

int msconnector_resource_limits_validate(const msconnector_resource_limits *limits) {
    return limits != 0 && limits->max_header_count > 0U && limits->max_header_name_size > 0U &&
        limits->max_header_value_size > 0U && limits->max_total_header_bytes > 0U &&
        limits->max_request_body_bytes > 0U && limits->max_response_body_bytes > 0U &&
        limits->max_event_json_bytes > 0U && limits->max_transaction_id_length > 0U &&
        limits->max_rule_id_length > 0U && limits->max_log_message_length > 0U;
}

int msconnector_resource_limits_headers_ok(const msconnector_header *headers, size_t header_count, const msconnector_resource_limits *limits) {
    size_t total = 0U;
    if (!msconnector_resource_limits_validate(limits)) { return 0; }
    if (header_count > limits->max_header_count) { return 0; }
    if (header_count > 0U && headers == 0) { return 0; }
    for (size_t i = 0; i < header_count; ++i) {
        if (headers[i].name_size == 0U || headers[i].name_size > limits->max_header_name_size || headers[i].value_size > limits->max_header_value_size) { return 0; }
        if (headers[i].name == 0 || (headers[i].value_size > 0U && headers[i].value == 0)) { return 0; }
        if (headers[i].name_size > limits->max_total_header_bytes - total) { return 0; }
        total += headers[i].name_size;
        if (headers[i].value_size > limits->max_total_header_bytes - total) { return 0; }
        total += headers[i].value_size;
    }
    return 1;
}

int msconnector_resource_limits_body_ok(size_t body_size, size_t max_body_size) { return max_body_size > 0U && body_size <= max_body_size; }
