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

static const char *ngx_http_modsecurity_http_version(ngx_http_request_t *r)
{
    switch (r->http_version) {
    case NGX_HTTP_VERSION_9: return "0.9";
    case NGX_HTTP_VERSION_10: return "1.0";
    case NGX_HTTP_VERSION_11: return "1.1";
#if defined(nginx_version) && nginx_version >= 1009005
    case NGX_HTTP_VERSION_20: return "2.0";
#endif
    default: return "1.0";
    }
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
    msconnector_header **out_headers, size_t *out_count)
{
    ngx_list_part_t *part = &list->part;
    ngx_table_elt_t *data = part->elts;
    size_t count = ngx_http_modsecurity_count_list_headers(list);
    size_t written = 0U;
    ngx_uint_t i;
    msconnector_header *headers;

    *out_headers = NULL;
    *out_count = 0U;
    if (count == 0U) {
        return 1;
    }

    headers = ngx_pcalloc(pool, count * sizeof(*headers));
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

static const char *ngx_http_modsecurity_host_fallback(ngx_http_request_t *r, msconnector_header *headers, size_t header_count)
{
    const char *host = msconnector_headers_host(headers, header_count);
    if (host != NULL) {
        return host;
    }
    if (r->headers_in.server.len > 0U) {
        return (const char *)r->headers_in.server.data;
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
    if (!ngx_http_modsecurity_copy_headers(r->pool, &r->headers_in.headers, &headers, &header_count)) {
        ngx_http_modsecurity_mapper_error(error, error_len, "request header allocation failed");
        return 0;
    }

    out->method = (const char *)r->method_name.data;
    out->uri = (const char *)r->unparsed_uri.data;
    out->http_version = ngx_http_modsecurity_http_version(r);
    out->headers = headers;
    out->header_count = header_count;
    out->hostname = ngx_http_modsecurity_host_fallback(r, headers, header_count);
    out->client.address = (const char *)r->connection->addr_text.data;
    out->client.port = ngx_inet_get_port(r->connection->sockaddr);
    local.len = NGX_SOCKADDR_STRLEN;
    local.data = ngx_pnalloc(r->pool, local.len);
    if (local.data != NULL && ngx_connection_local_sockaddr(r->connection, &local, 0) == NGX_OK) {
        out->server.address = (const char *)local.data;
        out->server.port = ngx_inet_get_port(r->connection->local_sockaddr);
    }
    out->body.data = NULL;
    out->body.size = 0U;

    if (!msconnector_request_mapper_validate_output(contract, out, error, error_len)) {
        return 0;
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
    if (!ngx_http_modsecurity_copy_headers(r->pool, &r->headers_out.headers, &headers, &header_count)) {
        ngx_http_modsecurity_mapper_error(error, error_len, "response header allocation failed");
        return 0;
    }

    out->status = r->headers_out.status ? (int)r->headers_out.status : NGX_HTTP_OK;
    out->http_version = ngx_http_modsecurity_http_version(r);
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
