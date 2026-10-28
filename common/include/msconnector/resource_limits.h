#ifndef MSCONNECTOR_RESOURCE_LIMITS_H
#define MSCONNECTOR_RESOURCE_LIMITS_H

#include "msconnector/request.h"
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_resource_limits {
    size_t max_header_count;
    size_t max_header_name_size;
    size_t max_header_value_size;
    size_t max_total_header_bytes;
    size_t max_event_json_bytes;
    size_t max_transaction_id_length;
    size_t max_rule_id_length;
    size_t max_log_message_length;
} msconnector_resource_limits;

void msconnector_resource_limits_init(msconnector_resource_limits *limits);
int msconnector_resource_limits_validate(const msconnector_resource_limits *limits);
int msconnector_resource_limits_headers_ok(const msconnector_header *headers, size_t header_count, const msconnector_resource_limits *limits);

#ifdef __cplusplus
}
#endif

#endif
