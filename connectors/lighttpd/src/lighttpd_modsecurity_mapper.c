#include "lighttpd_modsecurity_mapper.h"

#include <string.h>

#include "msconnector/generic_mapper.h"

void lighttpd_modsecurity_config_init(msconnector_config *config) {
    msconnector_config_init(config);
    msconnector_config_apply_defaults(config);
}

int lighttpd_modsecurity_map_request(
        const lighttpd_modsecurity_request *src,
        const msconnector_request_mapper_contract *contract,
        msconnector_request *out,
        char *error,
        size_t error_len) {
    msconnector_generic_request_source generic;

    if (src == 0) {
        return msconnector_generic_map_request(0, contract, out, error, error_len);
    }

    memset(&generic, 0, sizeof(generic));
    generic.method = src->method;
    generic.uri = src->uri;
    generic.http_version = src->http_version;
    generic.hostname = src->hostname;
    generic.client.address = src->client_address;
    generic.client.port = src->client_port;
    generic.server.address = src->server_address;
    generic.server.port = src->server_port;
    generic.headers = src->headers;
    generic.header_count = src->header_count;
    generic.body.data = src->body;
    generic.body.size = src->body_size;

    return msconnector_generic_map_request(&generic, contract, out, error, error_len);
}

int lighttpd_modsecurity_map_response(
        const lighttpd_modsecurity_response *src,
        const msconnector_response_mapper_contract *contract,
        msconnector_response *out,
        char *error,
        size_t error_len) {
    msconnector_generic_response_source generic;

    if (src == 0) {
        return msconnector_generic_map_response(0, contract, out, error, error_len);
    }

    memset(&generic, 0, sizeof(generic));
    generic.status = src->status;
    generic.http_version = src->http_version;
    generic.headers = src->headers;
    generic.header_count = src->header_count;
    generic.body.data = src->body;
    generic.body.size = src->body_size;

    return msconnector_generic_map_response(&generic, contract, out, error, error_len);
}
