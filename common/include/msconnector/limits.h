#ifndef MSCONNECTOR_LIMITS_H
#define MSCONNECTOR_LIMITS_H
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
#define MSCONNECTOR_MAX_HEADER_COUNT 256U
#define MSCONNECTOR_MAX_HEADER_NAME_LENGTH 256U
#define MSCONNECTOR_MAX_HEADER_VALUE_LENGTH 8192U
#define MSCONNECTOR_MAX_BODY_BUFFER_SIZE 1048576U
#define MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE 1048576U
#define MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH 128U
#define MSCONNECTOR_MAX_RULE_ID_LENGTH 128U
#define MSCONNECTOR_MAX_LOG_MESSAGE_LENGTH 1024U
#define MSCONNECTOR_MAX_PATH_LENGTH 4096U
#define MSCONNECTOR_MAX_JSON_FIELD_LENGTH 1024U
size_t msconnector_limit_header_count(void);
size_t msconnector_limit_header_name_length(void);
size_t msconnector_limit_header_value_length(void);
size_t msconnector_limit_body_buffer_size(void);
size_t msconnector_limit_response_body_buffer_size(void);
size_t msconnector_limit_transaction_id_length(void);
size_t msconnector_limit_rule_id_length(void);
size_t msconnector_limit_log_message_length(void);
size_t msconnector_limit_path_length(void);
size_t msconnector_limit_json_field_length(void);
#ifdef __cplusplus
}
#endif
#endif
