#include "haproxy_modsecurity_mapper.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "msconnector/headers.h"
#include "msconnector/request_helpers.h"
#include "msconnector/response_helpers.h"

static void haproxy_mapper_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0U) {
        snprintf(error, error_len, "%s", message != 0 ? message : "haproxy mapper error");
    }
}

static size_t haproxy_cstr_size(const char *value) {
    return value != 0 ? strlen(value) : 0U;
}

static int haproxy_headers_to_common(
        const haproxy_modsecurity_header *src,
        unsigned int header_count,
        msconnector_header **headers_out,
        size_t *header_count_out,
        char *error,
        size_t error_len) {
    msconnector_header *headers;

    if (headers_out == 0 || header_count_out == 0) {
        haproxy_mapper_error(error, error_len, "missing header mapper output");
        return 0;
    }
    *headers_out = 0;
    *header_count_out = 0U;
    if (header_count == 0U) {
        return 1;
    }
    if (src == 0) {
        haproxy_mapper_error(error, error_len, "header count provided without headers");
        return 0;
    }
    headers = (msconnector_header *)calloc((size_t)header_count, sizeof(*headers));
    if (headers == 0) {
        haproxy_mapper_error(error, error_len, "failed to allocate common headers");
        return 0;
    }
    for (unsigned int i = 0U; i < header_count; ++i) {
        headers[i].name = src[i].name;
        headers[i].name_size = haproxy_cstr_size(src[i].name);
        headers[i].value = src[i].value != 0 ? src[i].value : "";
        headers[i].value_size = haproxy_cstr_size(headers[i].value);
    }
    *headers_out = headers;
    *header_count_out = (size_t)header_count;
    return 1;
}

void haproxy_modsecurity_mapped_request_init(
        haproxy_modsecurity_mapped_request *mapped) {
    if (mapped == 0) {
        return;
    }
    msconnector_request_init(&mapped->request);
    mapped->owned_headers = 0;
}

void haproxy_modsecurity_mapped_request_cleanup(
        haproxy_modsecurity_mapped_request *mapped) {
    if (mapped == 0) {
        return;
    }
    free(mapped->owned_headers);
    mapped->owned_headers = 0;
    mapped->request.headers = 0;
    mapped->request.header_count = 0U;
}

void haproxy_modsecurity_mapped_response_init(
        haproxy_modsecurity_mapped_response *mapped) {
    if (mapped == 0) {
        return;
    }
    msconnector_response_init(&mapped->response);
    mapped->owned_headers = 0;
}

void haproxy_modsecurity_mapped_response_cleanup(
        haproxy_modsecurity_mapped_response *mapped) {
    if (mapped == 0) {
        return;
    }
    free(mapped->owned_headers);
    mapped->owned_headers = 0;
    mapped->response.headers = 0;
    mapped->response.header_count = 0U;
}

int haproxy_modsecurity_map_owned_request(
        const haproxy_modsecurity_request *src,
        const msconnector_request_mapper_contract *contract,
        haproxy_modsecurity_mapped_request *out,
        char *error,
        size_t error_len) {
    size_t header_count = 0U;
    const msconnector_header *host_header;
    int rc;

    if (src == 0 || out == 0) {
        haproxy_mapper_error(error, error_len, "missing request mapper input");
        return 0;
    }
    haproxy_modsecurity_mapped_request_init(out);
    if (haproxy_headers_to_common(src->headers, src->header_count,
            &out->owned_headers, &header_count, error, error_len) != 1) {
        return 0;
    }
    out->request.method = src->method;
    out->request.uri = src->uri;
    out->request.http_version = "1.1";
    out->request.client.address = src->client_ip;
    out->request.client.port = src->client_port;
    out->request.server.address = src->server_ip;
    out->request.server.port = src->server_port;
    out->request.headers = out->owned_headers;
    out->request.header_count = header_count;
    host_header = msconnector_headers_find_first(out->request.headers,
        out->request.header_count, "host");
    if (host_header != 0 && host_header->value != 0 && host_header->value_size > 0U) {
        out->request.hostname = host_header->value;
    } else {
        out->request.hostname = src->server_ip;
    }
    if (src->body != 0 && src->body_len > 0U) {
        out->request.body.data = src->body;
        out->request.body.size = (size_t)src->body_len;
    }
    rc = msconnector_request_mapper_validate_output(contract, &out->request, error, error_len);
    if (rc != 1) {
        haproxy_modsecurity_mapped_request_cleanup(out);
        return 0;
    }
    return 1;
}

int haproxy_modsecurity_map_owned_response(
        const haproxy_modsecurity_response *src,
        const msconnector_response_mapper_contract *contract,
        haproxy_modsecurity_mapped_response *out,
        char *error,
        size_t error_len) {
    size_t header_count = 0U;
    int rc;

    if (src == 0 || out == 0) {
        haproxy_mapper_error(error, error_len, "missing response mapper input");
        return 0;
    }
    haproxy_modsecurity_mapped_response_init(out);
    if (haproxy_headers_to_common(src->headers, src->header_count,
            &out->owned_headers, &header_count, error, error_len) != 1) {
        return 0;
    }
    out->response.status = src->status;
    out->response.http_version = src->protocol;
    out->response.headers = out->owned_headers;
    out->response.header_count = header_count;
    if (src->body != 0 && src->body_len > 0U) {
        out->response.body.data = src->body;
        out->response.body.size = (size_t)src->body_len;
    }
    rc = msconnector_response_mapper_validate_output(contract, &out->response, error, error_len);
    if (rc != 1) {
        haproxy_modsecurity_mapped_response_cleanup(out);
        return 0;
    }
    return 1;
}
