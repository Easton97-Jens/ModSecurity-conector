#include "msconnector/response_mapper_contract.h"

#include <stdio.h>

static void set_error(char *error, size_t error_len, const char *message) { if (error != 0 && error_len > 0U) { (void)snprintf(error, error_len, "%s", message); } }
static int valid_req(msconnector_mapper_requirement value) { return value >= MSCONNECTOR_MAPPER_REQUIRED && value <= MSCONNECTOR_MAPPER_UNSUPPORTED; }
static int missing_string(const char *value) { return value == 0 || value[0] == '\0'; }
static int valid_status(int status) { return status >= 100 && status <= 599; }

void msconnector_response_mapper_contract_init(msconnector_response_mapper_contract *contract) {
    if (contract == 0) { return; }
    contract->status = MSCONNECTOR_MAPPER_REQUIRED;
    contract->http_version = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->headers = MSCONNECTOR_MAPPER_REQUIRED;
    contract->response_body = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->max_header_count = 1024U;
    contract->max_body_bytes = 0U;
}

int msconnector_response_mapper_contract_validate(const msconnector_response_mapper_contract *contract, char *error, size_t error_len) {
    if (contract == 0) { set_error(error, error_len, "missing contract"); return 0; }
    if (!valid_req(contract->status) || !valid_req(contract->http_version) || !valid_req(contract->headers) || !valid_req(contract->response_body)) { set_error(error, error_len, "invalid requirement"); return 0; }
    if (contract->status != MSCONNECTOR_MAPPER_REQUIRED) { set_error(error, error_len, "status must be required"); return 0; }
    if (contract->headers != MSCONNECTOR_MAPPER_REQUIRED) { set_error(error, error_len, "headers must be required"); return 0; }
    return 1;
}

int msconnector_response_mapper_validate_output(const msconnector_response_mapper_contract *contract, const msconnector_response *response, char *error, size_t error_len) {
    if (!msconnector_response_mapper_contract_validate(contract, error, error_len)) { return 0; }
    if (response == 0) { set_error(error, error_len, "missing response"); return 0; }
    if (contract->status == MSCONNECTOR_MAPPER_REQUIRED && !valid_status(response->status)) { set_error(error, error_len, "invalid status"); return 0; }
    if (contract->http_version == MSCONNECTOR_MAPPER_REQUIRED && missing_string(response->http_version)) { set_error(error, error_len, "missing http_version"); return 0; }
    if (contract->headers == MSCONNECTOR_MAPPER_REQUIRED && response->header_count > 0U && response->headers == 0) { set_error(error, error_len, "missing headers"); return 0; }
    if (contract->max_header_count > 0U && response->header_count > contract->max_header_count) { set_error(error, error_len, "too many headers"); return 0; }
    if (contract->response_body == MSCONNECTOR_MAPPER_UNSUPPORTED && response->body.size > 0U) { set_error(error, error_len, "body unsupported"); return 0; }
    if (contract->max_body_bytes > 0U && response->body.size > contract->max_body_bytes) { set_error(error, error_len, "body too large"); return 0; }
    return 1;
}
