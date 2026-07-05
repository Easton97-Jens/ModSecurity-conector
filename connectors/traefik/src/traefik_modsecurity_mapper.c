#include "traefik_modsecurity_mapper.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "msconnector/config.h"
#include "msconnector/headers.h"
#include "msconnector/request_helpers.h"
#include "msconnector/response_helpers.h"

static void mapper_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0U) { snprintf(error, error_len, "%s", message); }
}

static size_t cstr_size(const char *value) { return value != 0 ? strlen(value) : 0U; }

static int headers_to_common(const traefik_modsecurity_header *src, size_t count, msconnector_header **out, size_t *out_count, char *error, size_t error_len) {
    msconnector_header *headers;
    if (out == 0 || out_count == 0) { mapper_error(error, error_len, "missing header output"); return 0; }
    *out = 0; *out_count = 0U;
    if (count == 0U) { return 1; }
    if (src == 0) { mapper_error(error, error_len, "header count provided without headers"); return 0; }
    headers = (msconnector_header *)calloc(count, sizeof(*headers));
    if (headers == 0) { mapper_error(error, error_len, "failed to allocate headers"); return 0; }
    for (size_t i = 0U; i < count; ++i) {
        headers[i].name = src[i].name; headers[i].name_size = cstr_size(src[i].name);
        headers[i].value = src[i].value != 0 ? src[i].value : ""; headers[i].value_size = cstr_size(headers[i].value);
    }
    *out = headers; *out_count = count; return 1;
}

void traefik_modsecurity_config_init(msconnector_config *config) { msconnector_config_init(config); msconnector_config_apply_defaults(config); }

static void mapped_request_init(traefik_modsecurity_mapped_request *mapped) { if (mapped) { msconnector_request_init(&mapped->request); mapped->owned_headers = 0; } }
static void mapped_response_init(traefik_modsecurity_mapped_response *mapped) { if (mapped) { msconnector_response_init(&mapped->response); mapped->owned_headers = 0; } }
void traefik_modsecurity_mapped_request_cleanup(traefik_modsecurity_mapped_request *mapped) { if (mapped) { free(mapped->owned_headers); mapped->owned_headers = 0; mapped->request.headers = 0; mapped->request.header_count = 0U; } }
void traefik_modsecurity_mapped_response_cleanup(traefik_modsecurity_mapped_response *mapped) { if (mapped) { free(mapped->owned_headers); mapped->owned_headers = 0; mapped->response.headers = 0; mapped->response.header_count = 0U; } }

int traefik_modsecurity_map_owned_request(const traefik_modsecurity_request *src, const msconnector_request_mapper_contract *contract, traefik_modsecurity_mapped_request *out, char *error, size_t error_len) {
    const msconnector_header *host; size_t count = 0U; int rc;
    if (src == 0 || out == 0) { mapper_error(error, error_len, "missing request mapper input"); return 0; }
    mapped_request_init(out);
    if (!headers_to_common(src->headers, src->header_count, &out->owned_headers, &count, error, error_len)) { return 0; }
    out->request.method = src->method; out->request.uri = src->uri; out->request.http_version = src->http_version;
    out->request.client.address = src->client_address; out->request.client.port = src->client_port;
    out->request.server.address = src->server_address; out->request.server.port = src->server_port;
    out->request.headers = out->owned_headers; out->request.header_count = count;
    host = msconnector_headers_find_first(out->request.headers, out->request.header_count, "host");
    out->request.hostname = (host != 0 && host->value != 0 && host->value_size > 0U) ? host->value : src->server_address;
    if (src->body != 0 && src->body_size > 0U) { out->request.body.data = src->body; out->request.body.size = src->body_size; }
    rc = msconnector_request_mapper_validate_output(contract, &out->request, error, error_len);
    if (rc != 1) { traefik_modsecurity_mapped_request_cleanup(out); return 0; }
    return 1;
}

int traefik_modsecurity_map_request(const traefik_modsecurity_request *src, const msconnector_request_mapper_contract *contract, msconnector_request *out, char *error, size_t error_len) {
    traefik_modsecurity_mapped_request mapped;
    if (out == 0) { mapper_error(error, error_len, "missing request output"); return 0; }
    if (!traefik_modsecurity_map_owned_request(src, contract, &mapped, error, error_len)) { return 0; }
    *out = mapped.request; return 1;
}

int traefik_modsecurity_map_owned_response(const traefik_modsecurity_response *src, const msconnector_response_mapper_contract *contract, traefik_modsecurity_mapped_response *out, char *error, size_t error_len) {
    size_t count = 0U; int rc;
    if (src == 0 || out == 0) { mapper_error(error, error_len, "missing response mapper input"); return 0; }
    mapped_response_init(out);
    if (!headers_to_common(src->headers, src->header_count, &out->owned_headers, &count, error, error_len)) { return 0; }
    out->response.status = src->status; out->response.http_version = src->http_version;
    out->response.headers = out->owned_headers; out->response.header_count = count;
    if (src->body != 0 && src->body_size > 0U) { out->response.body.data = src->body; out->response.body.size = src->body_size; }
    rc = msconnector_response_mapper_validate_output(contract, &out->response, error, error_len);
    if (rc != 1) { traefik_modsecurity_mapped_response_cleanup(out); return 0; }
    return 1;
}

int traefik_modsecurity_map_response(const traefik_modsecurity_response *src, const msconnector_response_mapper_contract *contract, msconnector_response *out, char *error, size_t error_len) {
    traefik_modsecurity_mapped_response mapped;
    if (out == 0) { mapper_error(error, error_len, "missing response output"); return 0; }
    if (!traefik_modsecurity_map_owned_response(src, contract, &mapped, error, error_len)) { return 0; }
    *out = mapped.response; return 1;
}
