#ifndef TRAEFIK_MODSECURITY_MAPPER_H
#define TRAEFIK_MODSECURITY_MAPPER_H

#include <stddef.h>

#include "msconnector/config.h"
#include "msconnector/generic_mapper.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_generic_request_source traefik_modsecurity_request;
typedef msconnector_generic_response_source traefik_modsecurity_response;

void traefik_modsecurity_config_init(msconnector_config *config);

int traefik_modsecurity_map_request(
    const traefik_modsecurity_request *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len);

int traefik_modsecurity_map_response(
    const traefik_modsecurity_response *source,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *response,
    char *error,
    size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
