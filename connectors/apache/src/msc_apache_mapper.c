#include "msc_apache_mapper.h"

#include "msconnector/headers.h"
#include "msconnector/request_helpers.h"
#include "msconnector/resource_limits.h"
#include "msconnector/response_helpers.h"

#include <string.h>

static size_t apr_header_count(const apr_table_t *table)
{
    const apr_array_header_t *arr;

    if (table == NULL)
    {
        return 0U;
    }

    arr = apr_table_elts(table);
    return arr != NULL && arr->nelts > 0 ? (size_t)arr->nelts : 0U;
}

static void copy_apr_header_table(const apr_table_t *table,
    msconnector_header *headers, size_t *offset)
{
    const apr_array_header_t *arr;
    const apr_table_entry_t *te;
    int i;

    if (table == NULL)
    {
        return;
    }

    arr = apr_table_elts(table);
    te = (const apr_table_entry_t *)arr->elts;
    for (i = 0; i < arr->nelts; i++)
    {
        headers[*offset].name = te[i].key;
        headers[*offset].name_size = te[i].key != NULL ? strlen(te[i].key) : 0U;
        headers[*offset].value = te[i].val;
        headers[*offset].value_size = te[i].val != NULL ? strlen(te[i].val) : 0U;
        (*offset)++;
    }
}

static int copy_apr_headers(apr_pool_t *pool, const apr_table_t *table,
    msconnector_header **headers, size_t *header_count)
{
    size_t offset = 0U;

    *headers = NULL;
    *header_count = apr_header_count(table);
    if (*header_count == 0U)
    {
        return 1;
    }

    *headers = apr_pcalloc(pool, sizeof(msconnector_header) * *header_count);
    if (*headers == NULL)
    {
        return 0;
    }

    copy_apr_header_table(table, *headers, &offset);
    return offset == *header_count;
}

static int copy_apr_response_headers(apr_pool_t *pool, const request_rec *r,
    msconnector_header **headers, size_t *header_count)
{
    size_t offset = 0U;
    size_t capacity;

    *headers = NULL;
    *header_count = 0U;
    if (r == NULL)
    {
        return 0;
    }

    capacity = apr_header_count(r->headers_out)
        + apr_header_count(r->err_headers_out) + 1U;
    if (capacity == 0U)
    {
        return 1;
    }

    *headers = apr_pcalloc(pool, sizeof(msconnector_header) * capacity);
    if (*headers == NULL)
    {
        return 0;
    }

    copy_apr_header_table(r->err_headers_out, *headers, &offset);
    copy_apr_header_table(r->headers_out, *headers, &offset);
    *header_count = offset;

    if (r->content_type != NULL && r->content_type[0] != '\0'
        && msconnector_headers_find(*headers, *header_count,
            "Content-Type") == NULL)
    {
        (*headers)[offset].name = "Content-Type";
        (*headers)[offset].name_size = strlen("Content-Type");
        (*headers)[offset].value = r->content_type;
        (*headers)[offset].value_size = strlen(r->content_type);
        offset++;
        *header_count = offset;
    }

    return 1;
}

int msc_apache_map_request(request_rec *r,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *out,
    char *error,
    size_t error_len)
{
    msconnector_header *headers = NULL;
    size_t header_count = 0;
    msconnector_resource_limits limits;

    msconnector_request_init(out);
    if (r == NULL || out == NULL)
    {
        return 0;
    }

    if (!copy_apr_headers(r->pool, r->headers_in, &headers, &header_count))
    {
        return 0;
    }

    out->method = r->method;
    out->uri = r->unparsed_uri;
    out->http_version = r->protocol;
    out->hostname = msconnector_headers_host(headers, header_count);
    if (out->hostname == NULL)
    {
        out->hostname = r->hostname;
    }
    out->headers = headers;
    out->header_count = header_count;
    out->body.size = 0U;
    msconnector_resource_limits_init(&limits);
    if (!msconnector_resource_limits_headers_ok(headers, header_count, &limits))
    {
        return 0;
    }
#if AP_SERVER_MAJORVERSION_NUMBER > 1 && AP_SERVER_MINORVERSION_NUMBER < 3
    out->client.address = r->connection->remote_ip;
    out->client.port = r->connection->remote_addr != NULL ? r->connection->remote_addr->port : 0;
#else
    out->client.address = r->useragent_ip != NULL ? r->useragent_ip : r->connection->client_ip;
    out->client.port = 0;
    if (r->useragent_addr != NULL)
    {
        out->client.port = r->useragent_addr->port;
    }
    else if (r->connection->client_addr != NULL)
    {
        out->client.port = r->connection->client_addr->port;
    }
#endif
    out->server.address = r->server != NULL ? r->server->server_hostname : NULL;
    out->server.port = r->server != NULL ? (int)r->server->port : 0;

    return msconnector_request_mapper_validate_output(contract, out, error,
        error_len);
}

int msc_apache_map_response(request_rec *r,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *out,
    char *error,
    size_t error_len)
{
    msconnector_header *headers = NULL;
    size_t header_count = 0;
    msconnector_resource_limits limits;

    msconnector_response_init(out);
    if (r == NULL || out == NULL)
    {
        return 0;
    }

    if (!copy_apr_response_headers(r->pool, r, &headers, &header_count))
    {
        return 0;
    }

    out->status = r->status;
    out->http_version = r->protocol;
    out->headers = headers;
    out->header_count = header_count;
    out->body.size = 0U;
    msconnector_resource_limits_init(&limits);
    if (!msconnector_resource_limits_headers_ok(headers, header_count, &limits))
    {
        return 0;
    }

    return msconnector_response_mapper_validate_output(contract, out, error,
        error_len);
}
