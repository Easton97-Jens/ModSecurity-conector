#ifndef MSCONNECTOR_RESPONSE_MAPPER_CONTRACT_H
#define MSCONNECTOR_RESPONSE_MAPPER_CONTRACT_H

#include <stddef.h>

#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_response_mapper_contract {
    msconnector_mapper_requirement status;
    msconnector_mapper_requirement http_version;
    msconnector_mapper_requirement headers;
    msconnector_mapper_requirement response_body;
    size_t max_header_count;
    size_t max_body_bytes;
} msconnector_response_mapper_contract;

void msconnector_response_mapper_contract_init(msconnector_response_mapper_contract *contract);
int msconnector_response_mapper_contract_validate(const msconnector_response_mapper_contract *contract, char *error, size_t error_len);
int msconnector_response_mapper_validate_output(const msconnector_response_mapper_contract *contract, const msconnector_response *response, char *error, size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
