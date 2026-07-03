#ifndef MSCONNECTOR_REQUEST_MAPPER_CONTRACT_H
#define MSCONNECTOR_REQUEST_MAPPER_CONTRACT_H

#include <stddef.h>

#include "msconnector/request.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum msconnector_mapper_requirement {
    MSCONNECTOR_MAPPER_REQUIRED = 0,
    MSCONNECTOR_MAPPER_OPTIONAL,
    MSCONNECTOR_MAPPER_UNSUPPORTED
} msconnector_mapper_requirement;

typedef struct msconnector_request_mapper_contract {
    msconnector_mapper_requirement method;
    msconnector_mapper_requirement uri;
    msconnector_mapper_requirement http_version;
    msconnector_mapper_requirement hostname;
    msconnector_mapper_requirement client_endpoint;
    msconnector_mapper_requirement server_endpoint;
    msconnector_mapper_requirement headers;
    msconnector_mapper_requirement request_body;
    size_t max_header_count;
    size_t max_body_bytes;
} msconnector_request_mapper_contract;

void msconnector_request_mapper_contract_init(msconnector_request_mapper_contract *contract);
int msconnector_request_mapper_contract_validate(const msconnector_request_mapper_contract *contract, char *error, size_t error_len);
int msconnector_request_mapper_validate_output(const msconnector_request_mapper_contract *contract, const msconnector_request *request, char *error, size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
