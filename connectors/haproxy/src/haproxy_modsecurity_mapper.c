#include "haproxy_modsecurity_mapper.h"

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "msconnector/headers.h"
#include "msconnector/limits.h"
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

static unsigned char haproxy_ascii_lower(unsigned char value) {
    return value >= (unsigned char)'A' && value <= (unsigned char)'Z' ?
        (unsigned char)(value - (unsigned char)'A' + (unsigned char)'a') : value;
}

static int haproxy_header_token_char(unsigned char ch) {
    return (ch >= (unsigned char)'A' && ch <= (unsigned char)'Z') ||
        (ch >= (unsigned char)'a' && ch <= (unsigned char)'z') ||
        (ch >= (unsigned char)'0' && ch <= (unsigned char)'9') ||
        ch == (unsigned char)'!' || ch == (unsigned char)'#' ||
        ch == (unsigned char)'$' || ch == (unsigned char)'%' ||
        ch == (unsigned char)'&' || ch == (unsigned char) '\'' ||
        ch == (unsigned char)'*' || ch == (unsigned char)'+' ||
        ch == (unsigned char)'-' || ch == (unsigned char)'.' ||
        ch == (unsigned char)'^' || ch == (unsigned char)'_' ||
        ch == (unsigned char)'`' || ch == (unsigned char)'|' ||
        ch == (unsigned char)'~';
}

static int haproxy_header_name_is(const char *name, const char *expected) {
    size_t index;

    if (name == 0 || expected == 0 || strlen(name) != strlen(expected)) {
        return 0;
    }
    for (index = 0U; expected[index] != '\0'; ++index) {
        if (haproxy_ascii_lower((unsigned char)name[index]) !=
                haproxy_ascii_lower((unsigned char)expected[index])) {
            return 0;
        }
    }
    return 1;
}

static int haproxy_header_name_valid(const char *name) {
    size_t index;

    if (name == 0 || name[0] == '\0') {
        return 0;
    }
    for (index = 0U; name[index] != '\0'; ++index) {
        if (!haproxy_header_token_char((unsigned char)name[index])) {
            return 0;
        }
    }
    return 1;
}

static int haproxy_header_value_valid(const char *value) {
    size_t index;

    if (value == 0) {
        return 0;
    }
    for (index = 0U; value[index] != '\0'; ++index) {
        unsigned char ch = (unsigned char)value[index];
        if ((ch < 32U && ch != 9U) || ch == 127U) {
            return 0;
        }
    }
    return 1;
}

static int haproxy_header_decimal_valid(const char *value) {
    size_t index = 0U;
    size_t result = 0U;
    size_t length;

    if (value == 0) {
        return 0;
    }
    length = strlen(value);
    while (index < length && (value[index] == ' ' || value[index] == '\t')) {
        ++index;
    }
    if (index == length) {
        return 0;
    }
    for (; index < length && value[index] >= '0' && value[index] <= '9'; ++index) {
        size_t digit = (size_t)(value[index] - '0');
        if (result > (SIZE_MAX - digit) / 10U) {
            return 0;
        }
        result = result * 10U + digit;
    }
    while (index < length && (value[index] == ' ' || value[index] == '\t')) {
        ++index;
    }
    return index == length;
}

static int haproxy_validate_source_headers(
        const haproxy_modsecurity_header *headers,
        unsigned int header_count,
        int require_host,
        char *error,
        size_t error_len) {
    unsigned int host_count = 0U;
    unsigned int content_length_count = 0U;
    unsigned int transfer_encoding_count = 0U;
    unsigned int index;
    size_t total_bytes = 0U;

    if (header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
            (header_count > 0U && headers == 0)) {
        haproxy_mapper_error(error, error_len, "invalid or excessive header count");
        return 0;
    }
    for (index = 0U; index < header_count; ++index) {
        const char *name = headers[index].name;
        const char *value = headers[index].value;
        size_t name_size = haproxy_cstr_size(name);
        size_t value_size = haproxy_cstr_size(value);
        if (name_size == 0U || name_size > MSCONNECTOR_MAX_HEADER_NAME_LENGTH ||
                value_size > MSCONNECTOR_MAX_HEADER_VALUE_LENGTH ||
                name_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - total_bytes) {
            haproxy_mapper_error(error, error_len, "header size limit exceeded");
            return 0;
        }
        total_bytes += name_size;
        if (value_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - total_bytes) {
            haproxy_mapper_error(error, error_len, "total header size limit exceeded");
            return 0;
        }
        total_bytes += value_size;
        if (!haproxy_header_name_valid(name) || !haproxy_header_value_valid(value)) {
            haproxy_mapper_error(error, error_len, "invalid header syntax");
            return 0;
        }
        if (haproxy_header_name_is(name, "host")) {
            ++host_count;
        } else if (haproxy_header_name_is(name, "content-length")) {
            ++content_length_count;
            if (!haproxy_header_decimal_valid(value)) {
                haproxy_mapper_error(error, error_len, "invalid Content-Length");
                return 0;
            }
        } else if (haproxy_header_name_is(name, "transfer-encoding")) {
            ++transfer_encoding_count;
        }
    }
    if (require_host && host_count != 1U) {
        haproxy_mapper_error(error, error_len, "missing or duplicate Host header");
        return 0;
    }
    if (content_length_count > 1U) {
        haproxy_mapper_error(error, error_len, "duplicate Content-Length");
        return 0;
    }
    if (transfer_encoding_count > 1U) {
        haproxy_mapper_error(error, error_len, "multiple Transfer-Encoding headers");
        return 0;
    }
    if (content_length_count != 0U && transfer_encoding_count != 0U) {
        haproxy_mapper_error(error, error_len, "ambiguous Content-Length and Transfer-Encoding");
        return 0;
    }
    return 1;
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
    if (haproxy_validate_source_headers(src->headers, src->header_count, 1,
            error, error_len) != 1) {
        return 0;
    }
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
    if (host_header == 0 || host_header->value == 0 ||
            host_header->value_size == 0U) {
        haproxy_mapper_error(error, error_len, "missing or invalid Host header");
        haproxy_modsecurity_mapped_request_cleanup(out);
        return 0;
    }
    out->request.hostname = host_header->value;
    if (src->body != 0 && src->body_len > 0U) {
        out->request.body.data = src->body;
        out->request.body.size = (size_t)src->body_len;
    }
    rc = msconnector_request_mapper_validate_output(contract, &out->request, error, error_len);
    if (rc != 1) {
        haproxy_modsecurity_mapped_request_cleanup(out);
        return 0;
    }
    if (msconnector_request_validate(&out->request) != 1) {
        haproxy_mapper_error(error, error_len, "invalid mapped request headers");
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
    if (haproxy_validate_source_headers(src->headers, src->header_count, 0,
            error, error_len) != 1) {
        return 0;
    }
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
    if (msconnector_response_validate(&out->response) != 1) {
        haproxy_mapper_error(error, error_len, "invalid mapped response headers");
        haproxy_modsecurity_mapped_response_cleanup(out);
        return 0;
    }
    return 1;
}
