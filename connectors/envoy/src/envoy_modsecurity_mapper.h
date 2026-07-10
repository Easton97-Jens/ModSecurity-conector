#ifndef ENVOY_MODSECURITY_MAPPER_H
#define ENVOY_MODSECURITY_MAPPER_H

#include <stddef.h>

#include "msconnector/config.h"
#include "msconnector/generic_mapper.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_generic_request_source envoy_modsecurity_request;
typedef msconnector_generic_response_source envoy_modsecurity_response;

void envoy_modsecurity_config_init(msconnector_config *config);

int envoy_modsecurity_map_request(
    const envoy_modsecurity_request *src,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len);

int envoy_modsecurity_map_response(
    const envoy_modsecurity_response *src,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
