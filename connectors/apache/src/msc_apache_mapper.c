#include "msc_apache_mapper.h"

#include "msconnector/headers.h"
#include "msconnector/request_helpers.h"
#include "msconnector/resource_limits.h"
#include "msconnector/response_helpers.h"

#include <string.h>

static int copy_apr_headers(apr_pool_t *pool, const apr_table_t *table,
    msconnector_header **headers, size_t *header_count)
{
    const apr_array_header_t *arr;
    const apr_table_entry_t *te;
    int i;

    *headers = NULL;
    *header_count = 0;
    if (table == NULL)
    {
        return 1;
    }

    arr = apr_table_elts(table);
    te = (const apr_table_entry_t *)arr->elts;
    *headers = apr_pcalloc(pool, sizeof(msconnector_header) * (size_t)arr->nelts);
    if (*headers == NULL && arr->nelts > 0)
    {
        return 0;
    }

    for (i = 0; i < arr->nelts; i++)
    {
        (*headers)[i].name = te[i].key;
        (*headers)[i].name_size = te[i].key != NULL ? strlen(te[i].key) : 0U;
        (*headers)[i].value = te[i].val;
        (*headers)[i].value_size = te[i].val != NULL ? strlen(te[i].val) : 0U;
    }
    *header_count = (size_t)arr->nelts;
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
    out->client.port = r->useragent_addr != NULL ? r->useragent_addr->port : (r->connection->client_addr != NULL ? r->connection->client_addr->port : 0);
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

    if (!copy_apr_headers(r->pool, r->headers_out, &headers, &header_count))
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
