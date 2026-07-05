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

typedef struct haproxy_modsecurity_mapped_request {
    msconnector_request request;
    msconnector_header *owned_headers;
} haproxy_modsecurity_mapped_request;

typedef struct haproxy_modsecurity_mapped_response {
    msconnector_response response;
    msconnector_header *owned_headers;
} haproxy_modsecurity_mapped_response;

void haproxy_modsecurity_mapped_request_init(
    haproxy_modsecurity_mapped_request *mapped);
void haproxy_modsecurity_mapped_request_cleanup(
    haproxy_modsecurity_mapped_request *mapped);
void haproxy_modsecurity_mapped_response_init(
    haproxy_modsecurity_mapped_response *mapped);
void haproxy_modsecurity_mapped_response_cleanup(
    haproxy_modsecurity_mapped_response *mapped);

int haproxy_modsecurity_map_owned_request(
    const haproxy_modsecurity_request *src,
    const msconnector_request_mapper_contract *contract,
    haproxy_modsecurity_mapped_request *out,
    char *error,
    size_t error_len);

int haproxy_modsecurity_map_owned_response(
    const haproxy_modsecurity_response *src,
    const msconnector_response_mapper_contract *contract,
    haproxy_modsecurity_mapped_response *out,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
