/*
 * ModSecurity connector for nginx, http://www.modsecurity.org/
 * Copyright (c) 2015 Trustwave Holdings, Inc. (http://www.trustwave.com/)
 *
 * You may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * If any of the files related to licensing are missing or if you have any
 * other questions related to licensing please contact Trustwave Holdings, Inc.
 * directly using the email address security@modsecurity.org.
 *
 */

#include <ngx_config.h>

#ifndef MODSECURITY_DDEBUG
#define MODSECURITY_DDEBUG 0
#endif
#include "ddebug.h"

#include "ngx_http_modsecurity_common.h"
#include "ngx_http_modsecurity_mapper.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"

static ngx_http_output_header_filter_pt ngx_http_next_header_filter;

static ngx_int_t ngx_http_modsecurity_resolv_header_server(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_date(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_content_length(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_content_type(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_last_modified(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_connection(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_transfer_encoding(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_resolv_header_vary(ngx_http_request_t *r, ngx_str_t name, off_t offset);
static ngx_int_t ngx_http_modsecurity_phase3_log_event(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *mcf, int original_status,
    const char *wanted, const char *actual);

ngx_http_modsecurity_header_out_t ngx_http_modsecurity_headers_out[] = {

    { ngx_string("Server"),
            offsetof(ngx_http_headers_out_t, server),
            ngx_http_modsecurity_resolv_header_server },

    { ngx_string("Date"),
            offsetof(ngx_http_headers_out_t, date),
            ngx_http_modsecurity_resolv_header_date },

    { ngx_string("Content-Length"),
            offsetof(ngx_http_headers_out_t, content_length_n),
            ngx_http_modsecurity_resolv_header_content_length },

    { ngx_string("Content-Type"),
            offsetof(ngx_http_headers_out_t, content_type),
            ngx_http_modsecurity_resolv_header_content_type },

    { ngx_string("Last-Modified"),
            offsetof(ngx_http_headers_out_t, last_modified),
            ngx_http_modsecurity_resolv_header_last_modified },

    { ngx_string("Connection"),
            0,
            ngx_http_modsecurity_resolv_header_connection },

    { ngx_string("Transfer-Encoding"),
            0,
            ngx_http_modsecurity_resolv_header_transfer_encoding },

    { ngx_string("Vary"),
            0,
            ngx_http_modsecurity_resolv_header_vary },

#if 0
    { ngx_string("Content-Encoding"),
            offsetof(ngx_http_headers_out_t, content_encoding),
            NGX_TABLE },

    { ngx_string("Cache-Control"),
            offsetof(ngx_http_headers_out_t, cache_control),
            NGX_ARRAY },

    { ngx_string("Location"),
            offsetof(ngx_http_headers_out_t, location),
            NGX_TABLE },

    { ngx_string("Content-Range"),
            offsetof(ngx_http_headers_out_t, content_range),
            NGX_TABLE },

    { ngx_string("Accept-Ranges"),
            offsetof(ngx_http_headers_out_t, accept_ranges),
            NGX_TABLE },

    returiders_out[i].name 1;
    { ngx_string("WWW-Authenticate"),
            offsetof(ngx_http_headers_out_t, www_authenticate),
            NGX_TABLE },

    { ngx_string("Expires"),
            offsetof(ngx_http_headers_out_t, expires),
            NGX_TABLE },
#endif
    { ngx_null_string, 0, 0 }
};


#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
int
ngx_http_modsecurity_store_ctx_header(ngx_http_request_t *r, ngx_str_t *name, ngx_str_t *value)
{
    ngx_http_modsecurity_ctx_t     *ctx;
    ngx_http_modsecurity_conf_t    *mcf;
    ngx_http_modsecurity_header_t  *hdr;

    ctx = ngx_http_modsecurity_get_module_ctx(r);
    if (ctx == NULL || ctx->sanity_headers_out == NULL) {
        return NGX_ERROR;
    }

    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (mcf == NULL || mcf->sanity_checks_enabled == NGX_CONF_UNSET)
    {
        return NGX_OK;
    }

    hdr = ngx_array_push(ctx->sanity_headers_out);
    if (hdr == NULL) {
        return NGX_ERROR;
    }

    hdr->name.data = ngx_pnalloc(r->pool, name->len);
    hdr->value.data = ngx_pnalloc(r->pool, value->len);
    if (hdr->name.data == NULL || hdr->value.data == NULL) {
        return NGX_ERROR;
    }

    ngx_memcpy(hdr->name.data, name->data, name->len);
    hdr->name.len = name->len;
    ngx_memcpy(hdr->value.data, value->data, value->len);
    hdr->value.len = value->len;

    return NGX_OK;
}
#endif


static ngx_int_t
ngx_http_modsecurity_resolv_header_server(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    static char ngx_http_server_full_string[] = NGINX_VER;
    static char ngx_http_server_string[] = "nginx";

    ngx_http_core_loc_conf_t *clcf = NULL;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_str_t value;

    clcf = ngx_http_get_module_loc_conf(r, ngx_http_core_module);
    ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (r->headers_out.server == NULL) {
        if (clcf->server_tokens) {
            value.data = (u_char *)ngx_http_server_full_string;
            value.len = sizeof(ngx_http_server_full_string) - 1U;
        } else {
            value.data = (u_char *)ngx_http_server_string;
            value.len = sizeof(ngx_http_server_string) - 1U;
        }
    } else {
        ngx_table_elt_t *h = r->headers_out.server;
        value.data = h->value.data;
        value.len =  h->value.len;
    }

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif

    return msc_add_n_response_header(ctx->modsec_transaction,
        (const unsigned char *) name.data,
        name.len,
        (const unsigned char *) value.data,
        value.len);
}


static ngx_int_t
ngx_http_modsecurity_resolv_header_date(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_str_t date;

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (r->headers_out.date == NULL) {
        date.data = ngx_cached_http_time.data;
        date.len = ngx_cached_http_time.len;
    } else {
        ngx_table_elt_t *h = r->headers_out.date;
        date.data = h->value.data;
        date.len = h->value.len;
    }

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_http_modsecurity_store_ctx_header(r, &name, &date);
#endif

    return msc_add_n_response_header(ctx->modsec_transaction,
        (const unsigned char *) name.data,
        name.len,
        (const unsigned char *) date.data,
        date.len);
}


static ngx_int_t
ngx_http_modsecurity_resolv_header_content_length(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_str_t value;
    char buf[NGX_INT64_LEN+2];

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (r->headers_out.content_length_n >= 0)
    {
        ngx_sprintf((u_char *)buf, "%O%Z", r->headers_out.content_length_n);
        value.data = (unsigned char *)buf;
        value.len = strlen(buf);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
        ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif
        return msc_add_n_response_header(ctx->modsec_transaction,
            (const unsigned char *) name.data,
            name.len,
            (const unsigned char *) value.data,
            value.len);
    }

    return 1;
}


static ngx_int_t
ngx_http_modsecurity_resolv_header_content_type(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (r->headers_out.content_type.len > 0)
    {

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
        ngx_http_modsecurity_store_ctx_header(r, &name, &r->headers_out.content_type);
#endif

        return msc_add_n_response_header(ctx->modsec_transaction,
            (const unsigned char *) name.data,
            name.len,
            (const unsigned char *) r->headers_out.content_type.data,
            r->headers_out.content_type.len);
    }

    return 1;
}


static ngx_int_t
ngx_http_modsecurity_resolv_header_last_modified(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    u_char buf[1024];
    u_char *p;
    ngx_str_t value;

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (r->headers_out.last_modified_time == -1) {
        return 1;
    }

    p = ngx_http_time(buf, r->headers_out.last_modified_time);

    value.data = buf;
    value.len = (int)(p-buf);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif

    return msc_add_n_response_header(ctx->modsec_transaction,
        (const unsigned char *) name.data,
        name.len,
        (const unsigned char *) value.data,
        value.len);
}


static ngx_int_t
ngx_http_modsecurity_resolv_header_connection(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_http_core_loc_conf_t *clcf = NULL;
    char *connection = NULL;
    ngx_str_t value;

    clcf = ngx_http_get_module_loc_conf(r, ngx_http_core_module);
    ctx = ngx_http_modsecurity_get_module_ctx(r);

#if (NGX_HTTP_V2)
    /* NGINX does not emit HTTP/1.x hop-by-hop headers on an HTTP/2 stream.
     * Do not make ModSecurity inspect a fictional Connection or Keep-Alive
     * response header. */
    if (r->stream) {
        return 1;
    }
#endif
#if defined(nginx_version) && nginx_version >= 1025000
    /* HTTP/3 has the same hop-by-hop-header prohibition.  Its requests do
     * not use the HTTP/2 stream pointer, so guard the native H3 version
     * separately before constructing either synthetic header. */
    if (r->http_version == NGX_HTTP_VERSION_30) {
        return 1;
    }
#endif

    if (r->headers_out.status == NGX_HTTP_SWITCHING_PROTOCOLS) {
        connection = "upgrade";
    } else if (r->keepalive) {
        connection = "keep-alive";
        if (clcf->keepalive_header)
        {
            u_char buf[1024];
            ngx_sprintf(buf, "timeout=%T%Z", clcf->keepalive_header);
            ngx_str_t name2 = ngx_string("Keep-Alive");

            value.data = buf;
            value.len = strlen((char *)buf);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
            ngx_http_modsecurity_store_ctx_header(r, &name2, &value);
#endif

            if (msc_add_n_response_header(ctx->modsec_transaction,
                    (const unsigned char *) name2.data,
                    name2.len,
                    (const unsigned char *) value.data,
                    value.len) != 1) {
                ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                    "ModSecurity: failed to add synthetic response header for inspection");
            }
        }
    } else {
        connection = "close";
    }

    value.data = (u_char *) connection;
    value.len = strlen(connection);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif

    return msc_add_n_response_header(ctx->modsec_transaction,
        (const unsigned char *) name.data,
        name.len,
        (const unsigned char *) value.data,
        value.len);
}

static ngx_int_t
ngx_http_modsecurity_resolv_header_transfer_encoding(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
    ngx_http_modsecurity_ctx_t *ctx = NULL;

    if (r->chunked) {
        ngx_str_t value = ngx_string("chunked");

        ctx = ngx_http_modsecurity_get_module_ctx(r);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
        ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif

        return msc_add_n_response_header(ctx->modsec_transaction,
            (const unsigned char *) name.data,
            name.len,
            (const unsigned char *) value.data,
            value.len);
    }

    return 1;
}

static ngx_int_t
ngx_http_modsecurity_resolv_header_vary(ngx_http_request_t *r, ngx_str_t name, off_t offset)
{
    (void)offset;
#if (NGX_HTTP_GZIP)
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_http_core_loc_conf_t *clcf = NULL;

    clcf = ngx_http_get_module_loc_conf(r, ngx_http_core_module);
    if (r->gzip_vary && clcf->gzip_vary) {
        ngx_str_t value = ngx_string("Accept-Encoding");

        ctx = ngx_http_modsecurity_get_module_ctx(r);

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
        ngx_http_modsecurity_store_ctx_header(r, &name, &value);
#endif

        return msc_add_n_response_header(ctx->modsec_transaction,
            (const unsigned char *) name.data,
            name.len,
            (const unsigned char *) value.data,
            value.len);
    }
#endif

    return 1;
}

/*
 * Phase 3 is still before NGINX's terminal header filter.  Preserve only
 * bounded metadata about a disruptive response-header decision before the
 * request is finalized; neither response headers nor body bytes are copied
 * into the evidence stream.
 */
static ngx_int_t
ngx_http_modsecurity_phase3_log_event(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *mcf, int original_status,
    const char *wanted, const char *actual)
{
    msconnector_event event;
    ngx_http_modsecurity_ctx_t *ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (mcf == NULL || mcf->phase4_log_file == NULL ||
        mcf->phase4_log_file->fd == NGX_INVALID_FILE) {
        return NGX_OK;
    }

    msconnector_event_init(&event);
    event.meta.message_id = MSCONN_EVENT_RESPONSE_BLOCKED;
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = "phase3_intervention";
    event.meta.connector = "nginx";
    event.meta.integration_mode = "native-nginx-http-module";
    event.meta.transaction_id = ctx != NULL && ctx->event_transaction_id.len > 0U
        ? (const char *)ctx->event_transaction_id.data : "";
    event.decision.phase = MSCONNECTOR_PHASE_RESPONSE_HEADERS;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual;
    event.decision.requested_action = wanted;
    event.decision.actual_action = actual;
    event.decision.rule_id = ctx != NULL ? ctx->last_intervention_rule_id : "";
    event.decision.reason = "response_headers_before_commit";
    event.http.http_status = ctx != NULL && ctx->last_intervention_status > 0
        ? (int)ctx->last_intervention_status : NGX_HTTP_FORBIDDEN;
    event.http.original_http_status = original_status;
    event.http.visible_http_status = event.http.http_status;
    event.http.transport_result = "http_status";
    event.flags.late_intervention = 0;
    event.flags.response_started = 0;
    event.flags.response_committed = 0;
    event.flags.headers_sent = 0;
    event.flags.body_started = 0;
    event.flags.body_truncated = 0;
    event.flags.connection_aborted = 0;

    return ngx_http_modsecurity_write_phase_event_jsonl(r, mcf, &event,
        "phase3");
}

static void
ngx_http_modsecurity_add_response_headers(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    ngx_list_part_t *part = &r->headers_out.headers.part;
    ngx_table_elt_t *data = part->elts;
    ngx_table_elt_t *header;
    ngx_uint_t i;

    for (i = 0; ngx_http_modsecurity_headers_out[i].name.len; i++) {
        dd(" Sending header to ModSecurity - header: `%.*s'.",
            (int) ngx_http_modsecurity_headers_out[i].name.len,
            ngx_http_modsecurity_headers_out[i].name.data);

        if (ngx_http_modsecurity_headers_out[i].resolver(r,
                ngx_http_modsecurity_headers_out[i].name,
                ngx_http_modsecurity_headers_out[i].offset) != 1) {
            ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                "ModSecurity: failed to add synthetic response header for inspection");
        }
    }

    i = 0U;
    while ((header = ngx_http_modsecurity_next_header(&part, &data,
            &i)) != NULL) {

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
        ngx_http_modsecurity_store_ctx_header(r, &header->key, &header->value);
#endif

        /* Doing this ugly cast here, explanation on the request header. */
        if (msc_add_n_response_header(ctx->modsec_transaction,
                (const unsigned char *) header->key.data,
                header->key.len,
                (const unsigned char *) header->value.data,
                header->value.len) != 1) {
            ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                "ModSecurity: failed to add response header for inspection");
        }
    }
}

static ngx_int_t
ngx_http_modsecurity_response_header_metrics(ngx_http_request_t *r,
    size_t *count, size_t *bytes)
{
    ngx_list_part_t *part;
    ngx_table_elt_t *data;
    ngx_uint_t index;

    if (r == NULL || count == NULL || bytes == NULL) {
        return NGX_ERROR;
    }
    *count = 0U;
    *bytes = 0U;
    part = &r->headers_out.headers.part;
    data = part->elts;
    index = 0U;
    for (;;) {
        if (index >= part->nelts) {
            if (part->next == NULL) {
                return NGX_OK;
            }
            part = part->next;
            data = part->elts;
            index = 0U;
            continue;
        }
        if (data[index].key.len == 0U ||
            data[index].key.len > MSCONNECTOR_MAX_HEADER_NAME_LENGTH ||
            data[index].value.len > MSCONNECTOR_MAX_HEADER_VALUE_LENGTH ||
            *count >= MSCONNECTOR_MAX_HEADER_COUNT ||
            data[index].key.len > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes ||
            data[index].value.len > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes -
                data[index].key.len) {
            return NGX_ERROR;
        }
        ++*count;
        *bytes += data[index].key.len + data[index].value.len;
        ++index;
    }
}

static ngx_int_t
ngx_http_modsecurity_handle_response_header_intervention(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_uint_t status, int ret)
{
    ngx_http_modsecurity_conf_t *mcf;
    const char *wanted;

    if (ret < 0) {
        /* A disruptive intervention can no longer be materialized safely
         * after headers have committed.  Do not pass it through as an allow
         * and do not synthesize a second response. */
        ctx->intervention_triggered = 1;
        return NGX_ERROR;
    }
    if (r->error_page) {
        return ngx_http_next_header_filter(r);
    }
    if (ret == 0) {
        return ngx_http_next_header_filter(r);
    }

    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    wanted = ctx->last_intervention_status >= 300 &&
        ctx->last_intervention_status < 400 ? "redirect" : "deny";
    if (ngx_http_modsecurity_phase3_log_event(r, mcf, (int) status,
            wanted, wanted) != NGX_OK) {
        return NGX_ERROR;
    }
    ctx->intervention_triggered = 1;
    if (ctx->intervention_redirect_location_installed &&
        r->headers_out.location != NULL) {
        /* Only the redirect helper's connector-owned Location denotes a
         * response replacement.  A status-only intervention may retain an
         * upstream Location and must use finalization, which cleans that
         * pending response's headers. */
        ctx->response_replaced = 1;
        r->headers_out.status = ret;
        ngx_str_null(&r->headers_out.status_line);
        r->headers_out.content_length_n = 0;
        r->header_only = 1;
        return ngx_http_next_header_filter(r);
    }
    return ngx_http_filter_finalize_request(r, &ngx_http_modsecurity_module,
        ret);
}

ngx_int_t
ngx_http_modsecurity_header_filter_init(void)
{
    ngx_http_next_header_filter = ngx_http_top_header_filter;
    ngx_http_top_header_filter = ngx_http_modsecurity_header_filter;

    return NGX_OK;
}


ngx_int_t
ngx_http_modsecurity_header_filter(ngx_http_request_t *r)
{
    ngx_http_modsecurity_ctx_t *ctx;
    int ret = 0;
    ngx_uint_t status;
    char *http_response_ver;
    ngx_pool_t *old_pool;
    ngx_http_modsecurity_conf_t *mcf;
    size_t response_header_count;
    size_t response_header_bytes;
    char *response_content_type = NULL;


/* XXX: if NOT_MODIFIED, do we need to process it at all?  see xslt_header_filter() */

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    dd("header filter, recovering ctx: %p", ctx);

    if (ctx == NULL)
    {
        dd("something really bad happened or ModSecurity is disabled. going to the next filter.");
        return ngx_http_next_header_filter(r);
    }

    if (ctx->intervention_triggered) {
        return ngx_http_next_header_filter(r);
    }

    ngx_http_modsecurity_validate_response_mapper(ctx, r,
        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_HEADER);
    ctx->common_response_validated = 1;

/* The context may already have been processed by an earlier header-filter
 * invocation; preserve NGINX's next-filter behavior in that case. */

    if (ctx && ctx->processed)
    {
        dd("Already processed... going to the next header...");
        return ngx_http_next_header_filter(r);
    }

    /* Keep the response body in memory for the native response inspection
     * path. This remains enabled independently of SecResponseBody so the
     * filter lifecycle is consistent for every processed request. */
    r->filter_need_in_memory = 1;

    ctx->processed = 1;
    /*
     *
     * Assuming ModSecurity module is running immediately before the
     * ngx_http_header_filter, we will be able to populate ModSecurity with
     * headers from the headers_out structure.
     *
     * As ngx_http_header_filter place a direct call to the
     * ngx_http_write_filter_module, we cannot hook between those two. In order
     * to enumerate all headers, we first look at the headers_out structure,
     * and later we look into the ngx_list_part_t. The ngx_list_part_t must be
     * checked. Other module(s) in the chain may added some content to it.
     *
     */
    ngx_http_modsecurity_add_response_headers(r, ctx);

    /* prepare extra paramters for msc_process_response_headers() */
    if (r->err_status) {
        status = r->err_status;
    } else {
        status = r->headers_out.status;
    }
    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (r->headers_out.content_type.len > 0U) {
        response_content_type = ngx_str_to_char(r->headers_out.content_type,
            r->pool);
    }
    if (mcf == NULL || response_content_type == (char *)-1 ||
        ngx_http_modsecurity_response_header_metrics(r, &response_header_count,
            &response_header_bytes) != NGX_OK ||
        msconnector_transaction_contract_record_response_metadata(
            &ctx->contract, (int)status, response_content_type,
            response_header_count, response_header_bytes,
            mcf->common_config.phase4_body_limit > 0U
                ? mcf->common_config.phase4_body_limit : MSCONNECTOR_MAX_BODY_BUFFER_SIZE) !=
            MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: failed to record canonical response metadata");
        return NGX_ERROR;
    }

    /* The WAF-visible response version must match the negotiated request
     * protocol, including the native HTTP/3 mapping where available. */
    http_response_ver = "HTTP 1.1";
#if (NGX_HTTP_V2)
    if (r->stream) {
        http_response_ver = "HTTP 2.0";
    }
#endif
#if defined(nginx_version) && nginx_version >= 1025000
    if (r->http_version == NGX_HTTP_VERSION_30) {
        http_response_ver = "HTTP 3.0";
    }
#endif

    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    if (ngx_http_modsecurity_contract_begin(ctx,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P3 transition");
        return NGX_ERROR;
    }
    msc_process_response_headers(ctx->modsec_transaction, status, http_response_ver);
    if (ngx_http_modsecurity_contract_complete(ctx,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P3 completion");
        return NGX_ERROR;
    }
    ngx_http_modsecurity_pcre_malloc_done(old_pool);
    ctx->response_headers_seen = 1;
    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction, r, 0);
    return ngx_http_modsecurity_handle_response_header_intervention(r, ctx,
        status, ret);
}
