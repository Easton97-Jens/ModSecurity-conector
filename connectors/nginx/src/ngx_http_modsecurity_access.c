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
#include <stdint.h>

#ifndef MODSECURITY_DDEBUG
#define MODSECURITY_DDEBUG 0
#endif
#include "ddebug.h"

#include "ngx_http_modsecurity_common.h"
#include "ngx_http_modsecurity_mapper.h"
#include "msconnector/event.h"

static void ngx_http_modsecurity_request_intervention_log_event(
    ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf,
    enum msconnector_phase phase, const char *reason);

void
ngx_http_modsecurity_request_read(ngx_http_request_t *r)
{
    ngx_http_modsecurity_ctx_t *ctx;

    ctx = ngx_http_modsecurity_get_module_ctx(r);

#if defined(nginx_version) && nginx_version >= 8011
    r->main->count--;
#endif

    if (ctx->waiting_more_body)
    {
        ctx->waiting_more_body = 0;
        r->write_event_handler = ngx_http_core_run_phases;
        ngx_http_core_run_phases(r);
    }
}


/* Request-phase interventions happen before NGINX has committed a response.
 * Keep the source event in this actual access/body path so its integration
 * mode comes from the selected native module rather than a report collector. */
static void
ngx_http_modsecurity_request_intervention_log_event(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *mcf, enum msconnector_phase phase,
    const char *reason)
{
    msconnector_event event;
    ngx_http_modsecurity_ctx_t *ctx;
    const char *wanted;
    int body_limit;
    ngx_http_modsecurity_event_request_metadata_t request_metadata;

    if (r == NULL || mcf == NULL || mcf->phase4_log_file == NULL ||
        mcf->phase4_log_file->fd == NGX_INVALID_FILE) {
        return;
    }

    ctx = ngx_http_modsecurity_get_module_ctx(r);
    body_limit = phase == MSCONNECTOR_PHASE_REQUEST_BODY && ctx != NULL &&
        ctx->native_request_body_limit_rejection;
    wanted = !body_limit && ctx != NULL && ctx->last_intervention_status >= 300 &&
        ctx->last_intervention_status < 400 ? "redirect" : "deny";
    request_metadata = ngx_http_modsecurity_event_request_metadata(r);

    msconnector_event_init(&event);
    event.meta.message_id = body_limit ? MSCONN_EVENT_BODY_LIMIT :
        MSCONN_EVENT_REQUEST_BLOCKED;
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = body_limit ? "body_limit" :
        phase == MSCONNECTOR_PHASE_REQUEST_BODY
            ? "phase2_intervention" : "phase1_intervention";
    event.meta.connector = "nginx";
    event.meta.integration_mode = "native-nginx-http-module";
    event.meta.transaction_id = ctx != NULL && ctx->event_transaction_id.len > 0U
        ? (const char *)ctx->event_transaction_id.data : "";
    event.decision.phase = phase;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = wanted;
    event.decision.requested_action = wanted;
    event.decision.actual_action = wanted;
    event.decision.rule_id = body_limit ? "" :
        ctx != NULL ? ctx->last_intervention_rule_id : "";
    event.decision.reason = body_limit ? "request_body_limit_exceeded" : reason;
    event.http.http_status = ctx != NULL && ctx->last_intervention_status > 0
        ? (int)ctx->last_intervention_status : NGX_HTTP_FORBIDDEN;
    event.http.visible_http_status = event.http.http_status;
    event.http.transport_result = "http_status";
    event.request.method = request_metadata.method;
    event.request.uri = request_metadata.uri;
    event.body.content_type = request_metadata.content_type;
    event.body.limit_outcome = body_limit ? "reject" : NULL;

    if (!ngx_http_modsecurity_write_event_jsonl(
            r, mcf, &event,
            "modsecurity request intervention event serialization failed",
            "modsecurity request intervention log write failed")) {
        return;
    }
}


static ngx_int_t
ngx_http_modsecurity_validate_common_request_mapper(ngx_http_request_t *r)
{
    msconnector_request_mapper_contract contract;
    msconnector_request mapped_request;
    char mapper_error[128];

    msconnector_request_mapper_contract_init(&contract);
    if (!ngx_http_modsecurity_map_request(r, &contract, &mapped_request,
            mapper_error, sizeof(mapper_error))) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity common request mapper validation skipped: %s",
            mapper_error);
    }

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_set_request_hostname(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
#if defined(MODSECURITY_CHECK_VERSION) && MODSECURITY_VERSION_NUM >= 30130100
    const char *host_name;
    ngx_http_core_srv_conf_t *cscf;
    ngx_str_t hostname;

    hostname.len = 0U;
    if (r->headers_in.server.len > 0U) {
        hostname = r->headers_in.server;
    } else {
        cscf = ngx_http_get_module_srv_conf(r, ngx_http_core_module);
        if (cscf->server_name.len > 0U) {
            hostname = cscf->server_name;
        }
    }

    if (hostname.len > 0U) {
        host_name = ngx_str_to_char(hostname, r->pool);
        if (host_name == (char *)-1 || host_name == NULL) {
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
        msc_set_request_hostname(ctx->modsec_transaction,
            (const unsigned char *)host_name);
    }
#else
    (void)r;
    (void)ctx;
#endif

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_process_connection(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    const char *client_addr;
    const char *server_addr;
    ngx_connection_t *connection;
    ngx_pool_t *old_pool;
    ngx_str_t addr_text;
    ngx_str_t server_address;
    u_char address[NGX_SOCKADDR_STRLEN];
    int client_port;
    int ret;
    int server_port;

    connection = r->connection;
    addr_text = connection->addr_text;
    client_port = ngx_inet_get_port(connection->sockaddr);
    server_port = ngx_inet_get_port(connection->local_sockaddr);
    client_addr = ngx_str_to_char(addr_text, r->pool);
    if (client_addr == (char *)-1 || client_addr == NULL) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: client address conversion failed");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    server_address.len = NGX_SOCKADDR_STRLEN;
    server_address.data = address;
    if (ngx_connection_local_sockaddr(connection, &server_address, 0) != NGX_OK) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    server_addr = ngx_str_to_char(server_address, r->pool);
    if (server_addr == (char *)-1 || server_addr == NULL) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: server address conversion failed");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    ret = msc_process_connection(ctx->modsec_transaction, client_addr,
        client_port, server_addr, server_port);
    ngx_http_modsecurity_pcre_malloc_done(old_pool);
    if (ret != 1) {
        dd("Was not able to extract connection information.");
    }

    dd("Processing intervention with the connection information filled in");
    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction,
        r, 1);
    if (ret > 0) {
        ctx->intervention_triggered = 1;
        return ret;
    }
    if (ret < 0) {
        ctx->intervention_triggered = 1;
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    return NGX_OK;
}

static const char *
ngx_http_modsecurity_request_http_version(ngx_http_request_t *r)
{
    const char *http_version;

    switch (r->http_version) {
    case NGX_HTTP_VERSION_9:
        return "0.9";
    case NGX_HTTP_VERSION_10:
        return "1.0";
    case NGX_HTTP_VERSION_11:
        return "1.1";
#if defined(nginx_version) && nginx_version >= 1009005
    case NGX_HTTP_VERSION_20:
        return "2.0";
#endif
    default:
        http_version = ngx_str_to_char(r->http_protocol, r->pool);
        if (http_version == (char *)-1) {
            return (const char *)-1;
        }
        if (http_version != NULL && strlen(http_version) > 5U &&
            strncmp("HTTP/", http_version, 5U) == 0) {
            return http_version + 5;
        }
        return "1.0";
    }
}

static ngx_int_t
ngx_http_modsecurity_process_request_uri(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    const char *http_version;
    const char *method;
    const char *uri;
    ngx_pool_t *old_pool;
    int ret;

    http_version = ngx_http_modsecurity_request_http_version(r);
    uri = ngx_str_to_char(r->unparsed_uri, r->pool);
    method = ngx_str_to_char(r->method_name, r->pool);
    if (http_version == (const char *)-1 || uri == (const char *)-1 ||
        method == (const char *)-1 || uri == NULL) {
        dd("request URI or protocol conversion failed");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    ctx->native_event_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
    ctx->native_event_phase_active = 1;
    msc_process_uri(ctx->modsec_transaction, uri, method, http_version);
    ctx->native_event_phase_active = 0;
    ngx_http_modsecurity_pcre_malloc_done(old_pool);

    dd("Processing intervention with the transaction information filled in (uri, method and version)");
    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction,
        r, 1);
    if (ret > 0) {
        ctx->intervention_triggered = 1;
        return ret;
    }
    if (ret < 0) {
        ctx->intervention_triggered = 1;
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    return NGX_OK;
}

static void
ngx_http_modsecurity_add_request_headers(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    ngx_list_part_t *part;
    ngx_table_elt_t *data;
    ngx_table_elt_t *header;
    ngx_uint_t index;

    part = &r->headers_in.headers.part;
    data = part->elts;
    index = 0U;
    while ((header = ngx_http_modsecurity_next_header(&part, &data,
            &index)) != NULL) {

        dd("Adding request header: %.*s with value %.*s",
            (int)header->key.len, header->key.data,
            (int)header->value.len, header->value.data);
        if (msc_add_n_request_header(ctx->modsec_transaction,
                (const unsigned char *)header->key.data,
                header->key.len,
                (const unsigned char *)header->value.data,
                header->value.len) != 1) {
            ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
                "ModSecurity: failed to add request header for inspection");
        }
    }
}

static ngx_int_t
ngx_http_modsecurity_request_header_metrics(ngx_http_request_t *r,
    size_t *count, size_t *bytes)
{
    return ngx_http_modsecurity_header_metrics(r == NULL ? NULL
        : &r->headers_in.headers, count, bytes);
}

static ngx_int_t
ngx_http_modsecurity_process_request_headers(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf)
{
    ngx_pool_t *old_pool;
    char *method;
    char *uri;
    size_t header_count;
    size_t header_bytes;
    int ret;
    msconnector_nginx_intervention_disposition disposition;

    method = ngx_str_to_char(r->method_name, r->pool);
    uri = ngx_str_to_char(r->unparsed_uri.len > 0U ? r->unparsed_uri : r->uri,
        r->pool);
    if (method == (char *)-1 || method == NULL || uri == (char *)-1 || uri == NULL ||
        ngx_http_modsecurity_request_header_metrics(r, &header_count,
            &header_bytes) != NGX_OK ||
        msconnector_transaction_contract_record_request_metadata(&ctx->contract,
            method, uri, NULL, header_count, header_bytes,
            mcf->common_config.request_body_limit > 0U
                ? mcf->common_config.request_body_limit : MSCONNECTOR_MAX_BODY_BUFFER_SIZE) !=
            MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: failed to record canonical request metadata");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    ngx_http_modsecurity_add_request_headers(r, ctx);
    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    if (ngx_http_modsecurity_contract_begin(ctx,
            MSCONNECTOR_PHASE_REQUEST_HEADERS) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P1 transition");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    ctx->native_event_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
    ctx->native_event_phase_active = 1;
    msc_process_request_headers(ctx->modsec_transaction);
    ctx->native_event_phase_active = 0;
    if (ngx_http_modsecurity_contract_complete(ctx,
            MSCONNECTOR_PHASE_REQUEST_HEADERS) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P1 completion");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    ngx_http_modsecurity_pcre_malloc_done(old_pool);

    dd("Processing intervention with the request headers information filled in");
    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction,
        r, 1);
    disposition = ngx_http_modsecurity_intervention_disposition(ret,
        r->error_page);
    if (disposition == MSCONNECTOR_NGINX_INTERVENTION_FAILURE) {
        ctx->intervention_triggered = 1;
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    if (disposition == MSCONNECTOR_NGINX_INTERVENTION_BYPASS) {
        return NGX_DECLINED;
    }
    if (disposition == MSCONNECTOR_NGINX_INTERVENTION_ACTIVE) {
        ngx_http_modsecurity_request_intervention_log_event(r, mcf,
            MSCONNECTOR_PHASE_REQUEST_HEADERS,
            "request_headers_before_handler");
        ctx->intervention_triggered = 1;
        return ret;
    }

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_initialize_request(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *mcf)
{
    ngx_http_modsecurity_ctx_t *ctx;
    ngx_int_t rc;

    ctx = ngx_http_modsecurity_create_ctx(r);
    dd("ctx was NULL, creating new context: %p", ctx);
    if (ctx == NULL) {
        dd("ctx still null; Nothing we can do, returning an error.");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    (void)ngx_http_modsecurity_validate_common_request_mapper(r);
    rc = ngx_http_modsecurity_set_request_hostname(r, ctx);
    if (rc != NGX_OK) {
        return rc;
    }

    rc = ngx_http_modsecurity_process_connection(r, ctx);
    if (rc != NGX_OK) {
        if (rc > 0) {
            ctx->intervention_triggered = 1;
        }
        return rc;
    }

    rc = ngx_http_modsecurity_process_request_uri(r, ctx);
    if (rc != NGX_OK) {
        if (rc > 0) {
            ngx_http_modsecurity_request_intervention_log_event(r, mcf,
                MSCONNECTOR_PHASE_REQUEST_HEADERS,
                "request_uri_before_request_headers");
            ctx->intervention_triggered = 1;
        }
        return rc;
    }

    return ngx_http_modsecurity_process_request_headers(r, ctx, mcf);
}

static ngx_int_t
ngx_http_modsecurity_request_body_start(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    ngx_int_t rc;

    ctx->body_requested = 1;
    dd("asking for the request body, if any. Count: %d", r->main->count);
    r->request_body_in_single_buf = 1;
    r->request_body_in_persistent_file = 1;
    if (!r->request_body_in_file_only) {
        r->request_body_in_clean_file = 1;
    }

    rc = ngx_http_read_client_request_body(r,
        ngx_http_modsecurity_request_read);
    if (rc == NGX_ERROR || rc >= NGX_HTTP_SPECIAL_RESPONSE) {
#if (nginx_version < 1002006) ||                                             \
    (nginx_version >= 1003000 && nginx_version < 1003009)
        r->main->count--;
#endif
        return rc;
    }
    if (rc == NGX_AGAIN) {
        dd("nginx is asking us to wait for more data.");
        ctx->waiting_more_body = 1;
        return NGX_DONE;
    }

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_request_body(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf)
{
    ngx_chain_t *chain;
    int ret;

    chain = r->request_body->bufs;
    while (chain != NULL) {
        u_char *data = chain->buf->pos;
        size_t length = (size_t)(chain->buf->last - data);

        if (ctx->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&
            ngx_http_modsecurity_contract_begin(ctx,
                MSCONNECTOR_PHASE_REQUEST_BODY) != NGX_OK) {
            ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
                "ModSecurity: invalid canonical P2 transition");
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
        if (msconnector_transaction_contract_record_body(&ctx->contract, 0,
                length) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
            ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
                "ModSecurity: canonical request body limit reached");
            return NGX_HTTP_REQUEST_ENTITY_TOO_LARGE;
        }

        ctx->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
        ctx->native_event_phase_active = 1;
        msc_append_request_body(ctx->modsec_transaction, data,
            length);
        ctx->native_event_phase_active = 0;

        if (chain->buf->last_buf) {
            break;
        }
        chain = chain->next;

        ret = ngx_http_modsecurity_process_intervention(
            ctx->modsec_transaction, r, 0);
        if (ret > 0) {
            ngx_http_modsecurity_request_intervention_log_event(r, mcf,
                MSCONNECTOR_PHASE_REQUEST_BODY,
                "request_body_stream_before_handler");
            ctx->intervention_triggered = 1;
            return ret;
        }
        if (ret < 0) {
            ctx->intervention_triggered = 1;
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
    }

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_inspect_request_body(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf)
{
    ngx_pool_t *old_pool;
    ngx_int_t rc;
    int ret;

    dd("request body is ready to be processed");
    r->write_event_handler = ngx_http_core_run_phases;
    if (ctx->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&
        ngx_http_modsecurity_contract_begin(ctx,
            MSCONNECTOR_PHASE_REQUEST_BODY) != NGX_OK) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P2 transition");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    if (r->request_body->temp_file != NULL) {
        const char *file_name = ngx_str_to_char(
            r->request_body->temp_file->file.name, r->pool);
        off_t file_size = r->request_body->temp_file->offset;

        if (file_name == (char *)-1 || file_name == NULL || file_size < 0 ||
            (uintmax_t)file_size > (uintmax_t)SIZE_MAX ||
            (file_size > 0 && msconnector_transaction_contract_record_body(
                &ctx->contract, 0, (size_t)file_size) !=
                MSCONNECTOR_TRANSACTION_TRANSITION_OK)) {
            ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
                "ModSecurity: request body file metadata violates canonical limits");
            return file_size > 0 ? NGX_HTTP_REQUEST_ENTITY_TOO_LARGE :
                NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
        dd("request body inspection: file -- %s", file_name);
        ctx->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
        ctx->native_event_phase_active = 1;
        msc_request_body_from_file(ctx->modsec_transaction, file_name);
        ctx->native_event_phase_active = 0;
    } else {
        dd("inspection request body in memory.");
        rc = ngx_http_modsecurity_append_request_body(r, ctx, mcf);
        if (rc != NGX_OK) {
            return rc;
        }
    }

    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    ctx->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
    ctx->native_event_phase_active = 1;
    ret = msc_process_request_body(ctx->modsec_transaction);
    ctx->native_event_phase_active = 0;
    ngx_http_modsecurity_pcre_malloc_done(old_pool);
    ctx->request_body_processed = 1;

    if (ngx_http_modsecurity_contract_complete(ctx,
            MSCONNECTOR_PHASE_REQUEST_BODY) != NGX_OK) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P2 completion");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    if (ret != 1) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: request body phase processing failed");
        ctx->intervention_triggered = 1;
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction,
        r, 0);
    if (ret < 0) {
        ctx->intervention_triggered = 1;
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    if (r->error_page) {
        return NGX_DECLINED;
    }
    if (ret > 0) {
        ngx_http_modsecurity_request_intervention_log_event(r, mcf,
            MSCONNECTOR_PHASE_REQUEST_BODY, "request_body_before_handler");
        ctx->intervention_triggered = 1;
        return ret;
    }

    return NGX_DECLINED;
}

static ngx_int_t
ngx_http_modsecurity_process_request_body(ngx_http_request_t *r,
    ngx_http_modsecurity_conf_t *mcf)
{
    ngx_http_modsecurity_ctx_t *ctx;
    ngx_int_t rc;

    ctx = ngx_http_modsecurity_get_module_ctx(r);
    dd("recovering ctx: %p", ctx);
    if (ctx == NULL) {
        dd("ctx is null; Nothing we can do, returning an error.");
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    if (ctx->request_body_processed || ctx->intervention_triggered) {
        return NGX_DECLINED;
    }
    if (ctx->waiting_more_body == 1) {
        dd("waiting for more data before proceed. / count: %d", r->main->count);
        return NGX_DONE;
    }
    if (ctx->body_requested == 0) {
        rc = ngx_http_modsecurity_request_body_start(r, ctx);
        if (rc != NGX_OK) {
            return rc;
        }
    }
    if (ctx->waiting_more_body == 0) {
        return ngx_http_modsecurity_inspect_request_body(r, ctx, mcf);
    }

    dd("Nothing to add on the body inspection, reclaiming a NGX_DECLINED");
    return NGX_DECLINED;
}

ngx_int_t
ngx_http_modsecurity_access_handler(ngx_http_request_t *r)
{
    ngx_http_modsecurity_conf_t *mcf;
    ngx_http_modsecurity_ctx_t *ctx;
    ngx_int_t rc;

    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (mcf == NULL || mcf->enable != 1) {
        dd("ModSecurity not enabled... returning");
        return NGX_DECLINED;
    }

    dd("catching a new _access_ phase handler");
    ctx = ngx_http_modsecurity_get_module_ctx(r);
    dd("recovering ctx: %p", ctx);
    if (ctx == NULL) {
        rc = ngx_http_modsecurity_initialize_request(r, mcf);
        if (rc != NGX_OK) {
            return rc;
        }
    }

    return ngx_http_modsecurity_process_request_body(r, mcf);
}
