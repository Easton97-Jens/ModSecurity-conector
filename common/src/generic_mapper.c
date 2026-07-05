#include "msconnector/generic_mapper.h"

#include <stdio.h>

#include "msconnector/request_helpers.h"
#include "msconnector/response_helpers.h"

void msconnector_generic_config_init(msconnector_config *config) {
    msconnector_config_init(config);
}

static void set_mapper_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0U) {
        snprintf(error, error_len, "%s", message);
    }
}

int msconnector_generic_map_request(
        const msconnector_generic_request_source *src,
        const msconnector_request_mapper_contract *contract,
        msconnector_request *out,
        char *error,
        size_t error_len) {
    if (src == 0 || out == 0) {
        set_mapper_error(error, error_len, "missing request mapper input");
        return 0;
    }

    if (src->body.size > 0U && src->body.data == 0) {
        set_mapper_error(error, error_len, "request body data is required when body size is nonzero");
        return 0;
    }

    msconnector_request_init(out);
    out->method = src->method;
    out->uri = src->uri;
    out->http_version = src->http_version;
    out->hostname = src->hostname;
    out->client = src->client;
    out->server = src->server;
    out->headers = src->headers;
    out->header_count = src->header_count;
    out->body = src->body;

    if (out->hostname == 0) {
        out->hostname = src->server.address;
    }

    return msconnector_request_mapper_validate_output(contract, out, error, error_len);
}

int msconnector_generic_map_response(
        const msconnector_generic_response_source *src,
        const msconnector_response_mapper_contract *contract,
        msconnector_response *out,
        char *error,
        size_t error_len) {
    if (src == 0 || out == 0) {
        set_mapper_error(error, error_len, "missing response mapper input");
        return 0;
    }

    if (src->body.size > 0U && src->body.data == 0) {
        set_mapper_error(error, error_len, "response body data is required when body size is nonzero");
        return 0;
    }

    msconnector_response_init(out);
    out->status = src->status;
    out->http_version = src->http_version;
    out->headers = src->headers;
    out->header_count = src->header_count;
    out->body = src->body;

    return msconnector_response_mapper_validate_output(contract, out, error, error_len);
}
