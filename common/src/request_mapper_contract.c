#include "msconnector/request_mapper_contract.h"

#include <stdio.h>

static void set_error(char *error, size_t error_len, const char *message) { if (error != 0 && error_len > 0U) { (void)snprintf(error, error_len, "%s", message); } }
static int valid_req(msconnector_mapper_requirement value) { return value >= MSCONNECTOR_MAPPER_REQUIRED && value <= MSCONNECTOR_MAPPER_UNSUPPORTED; }
static int missing_string(const char *value) { return value == 0 || value[0] == '\0'; }

void msconnector_request_mapper_contract_init(msconnector_request_mapper_contract *contract) {
    if (contract == 0) { return; }
    contract->method = MSCONNECTOR_MAPPER_REQUIRED;
    contract->uri = MSCONNECTOR_MAPPER_REQUIRED;
    contract->http_version = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->hostname = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->client_endpoint = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->server_endpoint = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->headers = MSCONNECTOR_MAPPER_REQUIRED;
    contract->request_body = MSCONNECTOR_MAPPER_OPTIONAL;
    contract->max_header_count = 1024U;
    contract->max_body_bytes = 0U;
}

int msconnector_request_mapper_contract_validate(const msconnector_request_mapper_contract *contract, char *error, size_t error_len) {
    if (contract == 0) { set_error(error, error_len, "missing contract"); return 0; }
    if (!valid_req(contract->method) || !valid_req(contract->uri) || !valid_req(contract->http_version) || !valid_req(contract->hostname) || !valid_req(contract->client_endpoint) || !valid_req(contract->server_endpoint) || !valid_req(contract->headers) || !valid_req(contract->request_body)) { set_error(error, error_len, "invalid requirement"); return 0; }
    if (contract->method != MSCONNECTOR_MAPPER_REQUIRED) { set_error(error, error_len, "method must be required"); return 0; }
    if (contract->uri != MSCONNECTOR_MAPPER_REQUIRED) { set_error(error, error_len, "uri must be required"); return 0; }
    if (contract->headers != MSCONNECTOR_MAPPER_REQUIRED) { set_error(error, error_len, "headers must be required"); return 0; }
    return 1;
}

int msconnector_request_mapper_validate_output(const msconnector_request_mapper_contract *contract, const msconnector_request *request, char *error, size_t error_len) {
    if (!msconnector_request_mapper_contract_validate(contract, error, error_len)) { return 0; }
    if (request == 0) { set_error(error, error_len, "missing request"); return 0; }
    if (contract->method == MSCONNECTOR_MAPPER_REQUIRED && missing_string(request->method)) { set_error(error, error_len, "missing method"); return 0; }
    if (contract->uri == MSCONNECTOR_MAPPER_REQUIRED && missing_string(request->uri)) { set_error(error, error_len, "missing uri"); return 0; }
    if (contract->http_version == MSCONNECTOR_MAPPER_REQUIRED && missing_string(request->http_version)) { set_error(error, error_len, "missing http_version"); return 0; }
    if (contract->hostname == MSCONNECTOR_MAPPER_REQUIRED && missing_string(request->hostname)) { set_error(error, error_len, "missing hostname"); return 0; }
    if (contract->headers == MSCONNECTOR_MAPPER_REQUIRED && request->header_count > 0U && request->headers == 0) { set_error(error, error_len, "missing headers"); return 0; }
    if (contract->max_header_count > 0U && request->header_count > contract->max_header_count) { set_error(error, error_len, "too many headers"); return 0; }
    if (contract->request_body == MSCONNECTOR_MAPPER_UNSUPPORTED && request->body.size > 0U) { set_error(error, error_len, "body unsupported"); return 0; }
    if (contract->max_body_bytes > 0U && request->body.size > contract->max_body_bytes) { set_error(error, error_len, "body too large"); return 0; }
    return 1;
}
