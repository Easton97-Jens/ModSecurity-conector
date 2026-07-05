#ifndef NGX_HTTP_MODSECURITY_MAPPER_H
#define NGX_HTTP_MODSECURITY_MAPPER_H

#include "ngx_http_modsecurity_common.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response_mapper_contract.h"

int ngx_http_modsecurity_map_request(
    ngx_http_request_t *r,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len);

int ngx_http_modsecurity_map_response_from_ctx(
    const ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_request_t *r,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

int ngx_http_modsecurity_map_response(
    ngx_http_request_t *r,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

#endif
