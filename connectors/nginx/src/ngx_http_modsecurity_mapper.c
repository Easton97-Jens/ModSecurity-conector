#include "ngx_http_modsecurity_mapper.h"

#include "msconnector/headers.h"
#include "msconnector/request_helpers.h"
#include "msconnector/response_helpers.h"

#include <stdio.h>
#include <string.h>

static void ngx_http_modsecurity_mapper_error(char *error, size_t error_len, const char *message)
{
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", message);
    }
}

static char *ngx_http_modsecurity_pool_strndup(ngx_pool_t *pool, const u_char *data, size_t len)
{
    char *dst;

    if (data == NULL) {
        return NULL;
    }

    dst = ngx_pnalloc(pool, len + 1U);
    if (dst == NULL) {
        return NULL;
    }
    ngx_memcpy(dst, data, len);
    dst[len] = '\0';
    return dst;
}

static char *ngx_http_modsecurity_pool_cstrdup(ngx_pool_t *pool, const char *value)
{
    if (value == NULL) {
        return NULL;
    }
    return ngx_http_modsecurity_pool_strndup(pool, (const u_char *)value, ngx_strlen(value));
}

static char *ngx_http_modsecurity_http_version(ngx_pool_t *pool, ngx_http_request_t *r)
{
    const char *version;

    switch (r->http_version) {
    case NGX_HTTP_VERSION_9: version = "0.9"; break;
    case NGX_HTTP_VERSION_10: version = "1.0"; break;
    case NGX_HTTP_VERSION_11: version = "1.1"; break;
#if defined(nginx_version) && nginx_version >= 1009005
    case NGX_HTTP_VERSION_20: version = "2.0"; break;
#endif
    default:
        if (r->http_protocol.len > 5U && ngx_strncmp(r->http_protocol.data, "HTTP/", 5) == 0) {
            return ngx_http_modsecurity_pool_strndup(pool, r->http_protocol.data + 5, r->http_protocol.len - 5U);
        }
        version = "1.0";
        break;
    }
    return ngx_http_modsecurity_pool_cstrdup(pool, version);
}

static size_t ngx_http_modsecurity_count_list_headers(ngx_list_t *headers)
{
    ngx_list_part_t *part = &headers->part;
    size_t count = 0U;

    for (;;) {
        count += part->nelts;
        if (part->next == NULL) {
            break;
        }
        part = part->next;
    }
    return count;
}

static int ngx_http_modsecurity_copy_headers(ngx_pool_t *pool, ngx_list_t *list,
    size_t extra_capacity, msconnector_header **out_headers, size_t *out_count)
{
    ngx_list_part_t *part = &list->part;
    ngx_table_elt_t *data = part->elts;
    size_t count = ngx_http_modsecurity_count_list_headers(list);
    size_t written = 0U;
    ngx_uint_t i;
    msconnector_header *headers;

    *out_headers = NULL;
    *out_count = 0U;
    if (count == 0U && extra_capacity == 0U) {
        return 1;
    }

    headers = ngx_pcalloc(pool, (count + extra_capacity) * sizeof(*headers));
    if (headers == NULL) {
        return 0;
    }

    for (i = 0; ; i++) {
        if (i >= part->nelts) {
            if (part->next == NULL) {
                break;
            }
            part = part->next;
            data = part->elts;
            i = 0;
        }
        headers[written].name = (const char *)data[i].key.data;
        headers[written].name_size = data[i].key.len;
        headers[written].value = (const char *)data[i].value.data;
        headers[written].value_size = data[i].value.len;
        written++;
    }

    *out_headers = headers;
    *out_count = written;
    return 1;
}

static int ngx_http_modsecurity_append_header(ngx_pool_t *pool, msconnector_header *headers,
    size_t *header_count, const char *name, const char *value)
{
    char *copied_name;
    char *copied_value;

    copied_name = ngx_http_modsecurity_pool_cstrdup(pool, name);
    copied_value = ngx_http_modsecurity_pool_cstrdup(pool, value);
    if (copied_name == NULL || copied_value == NULL) {
        return 0;
    }
    headers[*header_count].name = copied_name;
    headers[*header_count].name_size = ngx_strlen(copied_name);
    headers[*header_count].value = copied_value;
    headers[*header_count].value_size = ngx_strlen(copied_value);
    (*header_count)++;
    return 1;
}

static char *ngx_http_modsecurity_request_hostname(ngx_pool_t *pool, ngx_http_request_t *r,
    msconnector_header *headers, size_t header_count)
{
    const msconnector_header *host;

    host = msconnector_headers_find_first(headers, header_count, "host");
    if (host != NULL && host->value != NULL) {
        return ngx_http_modsecurity_pool_strndup(pool, (const u_char *)host->value, host->value_size);
    }
    if (r->headers_in.server.len > 0U) {
        return ngx_http_modsecurity_pool_strndup(pool, r->headers_in.server.data, r->headers_in.server.len);
    }
    return NULL;
}

int ngx_http_modsecurity_map_request(ngx_http_request_t *r,
    const msconnector_request_mapper_contract *contract, msconnector_request *out,
    char *error, size_t error_len)
{
    msconnector_header *headers = NULL;
    size_t header_count = 0U;
    ngx_str_t local;

    if (r == NULL || out == NULL || contract == NULL) {
        ngx_http_modsecurity_mapper_error(error, error_len, "request mapper arguments are required");
        return 0;
    }

    msconnector_request_init(out);
    if (!ngx_http_modsecurity_copy_headers(r->pool, &r->headers_in.headers, 0U, &headers, &header_count)) {
        ngx_http_modsecurity_mapper_error(error, error_len, "request header allocation failed");
        return 0;
    }

    out->method = ngx_http_modsecurity_pool_strndup(r->pool, r->method_name.data, r->method_name.len);
    out->uri = ngx_http_modsecurity_pool_strndup(r->pool, r->unparsed_uri.data, r->unparsed_uri.len);
    out->http_version = ngx_http_modsecurity_http_version(r->pool, r);
    out->hostname = ngx_http_modsecurity_request_hostname(r->pool, r, headers, header_count);
    out->client.address = ngx_http_modsecurity_pool_strndup(r->pool, r->connection->addr_text.data, r->connection->addr_text.len);
    if (out->method == NULL || out->uri == NULL || out->http_version == NULL || out->client.address == NULL) {
        ngx_http_modsecurity_mapper_error(error, error_len, "request string allocation failed");
        return 0;
    }
    out->headers = headers;
    out->header_count = header_count;
    out->client.port = ngx_inet_get_port(r->connection->sockaddr);
    local.len = NGX_SOCKADDR_STRLEN;
    local.data = ngx_pnalloc(r->pool, local.len);
    if (local.data != NULL && ngx_connection_local_sockaddr(r->connection, &local, 0) == NGX_OK) {
        out->server.address = ngx_http_modsecurity_pool_strndup(r->pool, local.data, local.len);
        out->server.port = ngx_inet_get_port(r->connection->local_sockaddr);
        if (out->server.address == NULL) {
            ngx_http_modsecurity_mapper_error(error, error_len, "server address allocation failed");
            return 0;
        }
    }
    out->body.data = NULL;
    out->body.size = 0U;

    if (!msconnector_request_mapper_validate_output(contract, out, error, error_len)) {
        return 0;
    }
    return 1;
}

static int ngx_http_modsecurity_add_synthetic_response_headers(ngx_http_request_t *r,
    msconnector_header *headers, size_t *header_count)
{
    char content_length[NGX_OFF_T_LEN + 1];
    u_char *last;
    char *content_type;

    if (r->headers_out.content_type.len > 0U &&
        msconnector_headers_find_first(headers, *header_count, "content-type") == NULL) {
        content_type = ngx_http_modsecurity_pool_strndup(r->pool,
            r->headers_out.content_type.data, r->headers_out.content_type.len);
        if (content_type == NULL ||
            !ngx_http_modsecurity_append_header(r->pool, headers, header_count, "Content-Type", content_type)) {
            return 0;
        }
    }

    if (r->headers_out.content_length_n >= 0 &&
        msconnector_headers_find_first(headers, *header_count, "content-length") == NULL) {
        last = ngx_snprintf((u_char *)content_length, sizeof(content_length), "%O", r->headers_out.content_length_n);
        if (last >= (u_char *)content_length + sizeof(content_length)) {
            return 0;
        }
        *last = '\0';
        if (!ngx_http_modsecurity_append_header(r->pool, headers, header_count, "Content-Length", content_length)) {
            return 0;
        }
    }
    return 1;
}

int ngx_http_modsecurity_map_response_from_ctx(const ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_request_t *r, const msconnector_response_mapper_contract *contract,
    msconnector_response *out, char *error, size_t error_len)
{
    msconnector_header *headers = NULL;
    size_t header_count = 0U;

    (void)ctx;
    if (r == NULL || out == NULL || contract == NULL) {
        ngx_http_modsecurity_mapper_error(error, error_len, "response mapper arguments are required");
        return 0;
    }

    msconnector_response_init(out);
    if (!ngx_http_modsecurity_copy_headers(r->pool, &r->headers_out.headers, 2U, &headers, &header_count)) {
        ngx_http_modsecurity_mapper_error(error, error_len, "response header allocation failed");
        return 0;
    }
    if (!ngx_http_modsecurity_add_synthetic_response_headers(r, headers, &header_count)) {
        ngx_http_modsecurity_mapper_error(error, error_len, "synthetic response header allocation failed");
        return 0;
    }

    if (r->headers_out.status != 0) {
        out->status = (int) r->headers_out.status;
    } else if (r->err_status != 0) {
        out->status = (int) r->err_status;
    } else {
        out->status = NGX_HTTP_OK;
    }
    out->http_version = ngx_http_modsecurity_http_version(r->pool, r);
    if (out->http_version == NULL) {
        ngx_http_modsecurity_mapper_error(error, error_len, "response http version allocation failed");
        return 0;
    }
    out->headers = headers;
    out->header_count = header_count;
    out->body.data = NULL;
    out->body.size = 0U;

    if (!msconnector_response_mapper_validate_output(contract, out, error, error_len)) {
        return 0;
    }
    return 1;
}

int ngx_http_modsecurity_map_response(ngx_http_request_t *r,
    const msconnector_response_mapper_contract *contract, msconnector_response *out,
    char *error, size_t error_len)
{
    return ngx_http_modsecurity_map_response_from_ctx(NULL, r, contract, out, error, error_len);
}
