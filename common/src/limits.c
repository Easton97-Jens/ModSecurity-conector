#include "msconnector/limits.h"
size_t msconnector_limit_header_count(void) { return MSCONNECTOR_MAX_HEADER_COUNT; }
size_t msconnector_limit_header_name_length(void) { return MSCONNECTOR_MAX_HEADER_NAME_LENGTH; }
size_t msconnector_limit_header_value_length(void) { return MSCONNECTOR_MAX_HEADER_VALUE_LENGTH; }
size_t msconnector_limit_body_buffer_size(void) { return MSCONNECTOR_MAX_BODY_BUFFER_SIZE; }
size_t msconnector_limit_response_body_buffer_size(void) { return MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE; }
size_t msconnector_limit_transaction_id_length(void) { return MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH; }
size_t msconnector_limit_rule_id_length(void) { return MSCONNECTOR_MAX_RULE_ID_LENGTH; }
size_t msconnector_limit_log_message_length(void) { return MSCONNECTOR_MAX_LOG_MESSAGE_LENGTH; }
size_t msconnector_limit_path_length(void) { return MSCONNECTOR_MAX_PATH_LENGTH; }
size_t msconnector_limit_json_field_length(void) { return MSCONNECTOR_MAX_JSON_FIELD_LENGTH; }
