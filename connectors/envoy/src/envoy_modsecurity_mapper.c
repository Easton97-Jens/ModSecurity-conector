#include "envoy_modsecurity_mapper.h"

void envoy_modsecurity_config_init(msconnector_config *config)
{
    msconnector_generic_config_init(config);
}

int envoy_modsecurity_map_request(
    const envoy_modsecurity_request *src,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len)
{
    return msconnector_generic_map_request(src, contract, out, error, error_len);
}

int envoy_modsecurity_map_response(
    const envoy_modsecurity_response *src,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len)
{
    return msconnector_generic_map_response(src, contract, out, error, error_len);
}
