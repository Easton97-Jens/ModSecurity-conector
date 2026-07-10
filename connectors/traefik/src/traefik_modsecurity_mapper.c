#include "traefik_modsecurity_mapper.h"

void traefik_modsecurity_config_init(msconnector_config *config)
{
    msconnector_generic_config_init(config);
}

int traefik_modsecurity_map_request(
    const traefik_modsecurity_request *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len)
{
    return msconnector_generic_map_request(
        source,
        contract,
        request,
        error,
        error_len);
}

int traefik_modsecurity_map_response(
    const traefik_modsecurity_response *source,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *response,
    char *error,
    size_t error_len)
{
    return msconnector_generic_map_response(
        source,
        contract,
        response,
        error,
        error_len);
}
