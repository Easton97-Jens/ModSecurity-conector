#include "connectors/lighttpd/src/lighttpd_modsecurity_mapper.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#ifdef MSCONNECTOR_LIGHTTPD_HOST_API

#include "array.h"
#include "base.h"
#include "buffer.h"
#include "http_kv.h"
#include "request.h"

static void mapper_error(char *error, size_t error_len, const char *message) {
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", message);
    }
}

void lighttpd_modsecurity_map_storage_init(
        lighttpd_modsecurity_map_storage *storage) {
    if (storage == NULL) {
        return;
    }
    storage->headers = NULL;
    storage->header_count = 0U;
}

void lighttpd_modsecurity_map_storage_free(
        lighttpd_modsecurity_map_storage *storage) {
    if (storage == NULL) {
        return;
    }
    free(storage->headers);
    storage->headers = NULL;
    storage->header_count = 0U;
}

static int map_headers(
        const array *source,
        size_t max_header_count,
        size_t total_header_limit,
        lighttpd_modsecurity_map_storage *storage,
        char *error,
        size_t error_len) {
    size_t total_size = 0U;
    size_t count;

    lighttpd_modsecurity_map_storage_free(storage);
    count = source == NULL ? 0U : (size_t)source->used;
    if (max_header_count > 0U && count > max_header_count) {
        mapper_error(error, error_len, "lighttpd header count exceeds runtime limit");
        return 0;
    }
    if (count == 0U) {
        return 1;
    }

    storage->headers = calloc(count, sizeof(*storage->headers));
    if (storage->headers == NULL) {
        mapper_error(error, error_len, "could not allocate lighttpd header mapping");
        return 0;
    }

    for (size_t i = 0U; i < count; ++i) {
        const data_unset *entry = source->data[i];
        const data_string *header;
        size_t name_size;
        size_t value_size;

        if (entry == NULL || entry->type != TYPE_STRING) {
            mapper_error(error, error_len, "lighttpd header entry is not a string");
            lighttpd_modsecurity_map_storage_free(storage);
            return 0;
        }
        header = (const data_string *)entry;
        name_size = (size_t)buffer_clen(&header->key);
        value_size = (size_t)buffer_clen(&header->value);
        if (name_size > SIZE_MAX - value_size ||
            total_size > SIZE_MAX - name_size - value_size) {
            mapper_error(error, error_len, "lighttpd header size overflow");
            lighttpd_modsecurity_map_storage_free(storage);
            return 0;
        }
        total_size += name_size + value_size;
        if (total_header_limit > 0U && total_size > total_header_limit) {
            mapper_error(error, error_len, "lighttpd headers exceed runtime byte limit");
            lighttpd_modsecurity_map_storage_free(storage);
            return 0;
        }

        storage->headers[i].name = header->key.ptr;
        storage->headers[i].name_size = name_size;
        storage->headers[i].value = header->value.ptr;
        storage->headers[i].value_size = value_size;
    }
    storage->header_count = count;
    return 1;
}

int lighttpd_modsecurity_map_request(
        const request_st *request,
        const msconnector_request_mapper_contract *contract,
        size_t total_header_limit,
        lighttpd_modsecurity_map_storage *storage,
        msconnector_request *out,
        char *error,
        size_t error_len) {
    msconnector_generic_request_source source;
    const buffer *method;
    const buffer *version;

    if (request == NULL || contract == NULL || storage == NULL || out == NULL) {
        mapper_error(error, error_len, "missing lighttpd request mapper input");
        return 0;
    }
    if (!map_headers(
            &request->rqst_headers,
            contract->max_header_count,
            total_header_limit,
            storage,
            error,
            error_len)) {
        return 0;
    }

    method = http_method_buf(request->http_method);
    version = http_version_buf(request->http_version);
    source.method = method->ptr;
    source.uri = request->target.ptr;
    source.http_version = version->ptr;
    source.hostname = request->http_host == NULL ? NULL : request->http_host->ptr;
    source.client.address = request->dst_addr_buf == NULL ? NULL : request->dst_addr_buf->ptr;
    source.client.port = request->dst_addr == NULL
        ? 0
        : (int)sock_addr_get_port(request->dst_addr);
    source.server.address = request->server_name == NULL ? NULL : request->server_name->ptr;
    source.server.port = request->con == NULL || request->con->srv_socket == NULL
        ? 0
        : (int)sock_addr_get_port(&request->con->srv_socket->addr);
    source.headers = storage->headers;
    source.header_count = storage->header_count;
    source.body.data = NULL;
    source.body.size = 0U;

    if (!msconnector_generic_map_request(&source, contract, out, error, error_len)) {
        lighttpd_modsecurity_map_storage_free(storage);
        return 0;
    }
    return 1;
}

int lighttpd_modsecurity_map_response(
        const request_st *request,
        const msconnector_response_mapper_contract *contract,
        size_t total_header_limit,
        lighttpd_modsecurity_map_storage *storage,
        msconnector_response *out,
        char *error,
        size_t error_len) {
    msconnector_generic_response_source source;
    const buffer *version;

    if (request == NULL || contract == NULL || storage == NULL || out == NULL) {
        mapper_error(error, error_len, "missing lighttpd response mapper input");
        return 0;
    }
    if (!map_headers(
            &request->resp_headers,
            contract->max_header_count,
            total_header_limit,
            storage,
            error,
            error_len)) {
        return 0;
    }

    version = http_version_buf(request->http_version);
    source.status = request->http_status;
    source.http_version = version->ptr;
    source.headers = storage->headers;
    source.header_count = storage->header_count;
    source.body.data = NULL;
    source.body.size = 0U;

    if (!msconnector_generic_map_response(&source, contract, out, error, error_len)) {
        lighttpd_modsecurity_map_storage_free(storage);
        return 0;
    }
    return 1;
}

#else

/*
 * Generic repository C-standard checks do not provision lighttpd headers.
 * The real implementations above are compiled by build/build_module.sh with
 * MSCONNECTOR_LIGHTTPD_HOST_API and the pinned lighttpd source directory.
 */
void lighttpd_modsecurity_map_storage_init(
        lighttpd_modsecurity_map_storage *storage) {
    if (storage != NULL) {
        storage->headers = NULL;
        storage->header_count = 0U;
    }
}

void lighttpd_modsecurity_map_storage_free(
        lighttpd_modsecurity_map_storage *storage) {
    if (storage != NULL) {
        free(storage->headers);
        storage->headers = NULL;
        storage->header_count = 0U;
    }
}

int lighttpd_modsecurity_map_request(
        const request_st *request,
        const msconnector_request_mapper_contract *contract,
        size_t total_header_limit,
        lighttpd_modsecurity_map_storage *storage,
        msconnector_request *out,
        char *error,
        size_t error_len) {
    (void)request;
    (void)contract;
    (void)total_header_limit;
    (void)storage;
    (void)out;
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", "lighttpd host headers were not enabled");
    }
    return 0;
}

int lighttpd_modsecurity_map_response(
        const request_st *request,
        const msconnector_response_mapper_contract *contract,
        size_t total_header_limit,
        lighttpd_modsecurity_map_storage *storage,
        msconnector_response *out,
        char *error,
        size_t error_len) {
    (void)request;
    (void)contract;
    (void)total_header_limit;
    (void)storage;
    (void)out;
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", "lighttpd host headers were not enabled");
    }
    return 0;
}

#endif
