#ifndef HAPROXY_MODSECURITY_MAPPER_H
#define HAPROXY_MODSECURITY_MAPPER_H

#include "haproxy_modsecurity_binding.h"

#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

int haproxy_modsecurity_map_request(
    const haproxy_modsecurity_request *src,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len);

int haproxy_modsecurity_map_response(
    const haproxy_modsecurity_response *src,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
