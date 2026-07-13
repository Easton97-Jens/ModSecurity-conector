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
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/limits.h"
#include "msconnector/rule_id.h"


void
ngx_http_modsecurity_log_rule_match_event(ngx_http_request_t *r,
    enum msconnector_phase phase, const char *rule_id)
{
    msconnector_event event;
    char line[4096];
    char *method = "";
    char *uri = "";
    char *content_type = "";
    int json_truncated = 0;
    size_t line_length;
    ssize_t written;
    ngx_http_modsecurity_ctx_t *ctx;
    ngx_http_modsecurity_conf_t *mcf;

    if (r == NULL || !msconnector_rule_id_validate(rule_id)) {
        return;
    }
    ctx = ngx_http_modsecurity_get_module_ctx(r);
    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (ctx == NULL || mcf == NULL || mcf->phase4_log_file == NULL ||
        mcf->phase4_log_file->fd == NGX_INVALID_FILE) {
        return;
    }

    if (r->method_name.len > 0U) {
        char *value = ngx_str_to_char(r->method_name, r->pool);
        if (value != (char *)-1 && value != NULL) {
            method = value;
        }
    }
    if (r->unparsed_uri.len > 0U) {
        char *value = ngx_str_to_char(r->unparsed_uri, r->pool);
        if (value != (char *)-1 && value != NULL) {
            uri = value;
        }
    }
    if (r->headers_in.content_type != NULL &&
        r->headers_in.content_type->value.len > 0U) {
        char *value = ngx_str_to_char(r->headers_in.content_type->value,
            r->pool);
        if (value != (char *)-1 && value != NULL) {
            content_type = value;
        }
    }

    /* This callback runs synchronously while the native module is executing
     * request processing.  It records only the rule identifier and host
     * metadata; the `pass` action deliberately reflects a non-disruptive
     * match and is not re-labelled as a deny or log-only intervention. */
    msconnector_event_init(&event);
    event.meta.level = "info";
    event.meta.message_id = "MSCONN_EVENT_RULE_MATCHED";
    event.meta.message = "Non-disruptive ModSecurity rule match observed in native NGINX module.";
    event.meta.event = "request_rule_match";
    event.meta.connector = "nginx";
    event.meta.integration_mode = "native-nginx-http-module";
    event.meta.transaction_id = ctx->event_transaction_id.len > 0U
        ? (const char *)ctx->event_transaction_id.data : "";
    event.decision.phase = phase;
    event.decision.status = MSCONNECTOR_STATUS_OK;
    event.decision.action = "pass";
    event.decision.requested_action = "pass";
    event.decision.actual_action = "pass";
    event.decision.rule_id = rule_id;
    event.decision.reason = "non_disruptive_rule_match";
    event.http.transport_result = "not_observable";
    event.request.method = method;
    event.request.uri = uri;
    event.body.content_type = content_type;

    if (!msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated)) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity native rule-match event serialization failed%s",
            json_truncated ? " (truncated)" : "");
        return;
    }

    line_length = ngx_strlen(line);
    written = ngx_write_fd(mcf->phase4_log_file->fd, (u_char *)line,
        line_length);
    if (written < 0 || (size_t)written != line_length) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log,
            written < 0 ? ngx_errno : 0,
            "modsecurity native rule-match log write failed");
    }
}


void
ngx_http_modsecurity_log(void *log, const void* data)
{
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    const char *msg;
    ngx_http_request_t *r;
    ngx_http_modsecurity_ctx_t *ctx;

    if (log == NULL || data == NULL) {
        return;
    }
    msg = (const char *) data;
    r = (ngx_http_request_t *)log;
    ctx = ngx_http_modsecurity_get_module_ctx(r);
    rule_id[0] = '\0';
    if (ctx != NULL && ctx->native_event_phase_active &&
        (ctx->native_event_phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
         ctx->native_event_phase == MSCONNECTOR_PHASE_REQUEST_BODY) &&
        msconnector_rule_id_extract_from_message(msg, rule_id,
            sizeof(rule_id)) > 0) {
        ngx_http_modsecurity_log_rule_match_event(r,
            ctx->native_event_phase, rule_id);
    }

    ngx_log_error(NGX_LOG_INFO, r->connection->log, 0, "%s", msg);
}


ngx_int_t
ngx_http_modsecurity_log_handler(ngx_http_request_t *r)
{
    ngx_pool_t                   *old_pool;
    ngx_http_modsecurity_ctx_t   *ctx;

    dd("catching a new _log_ phase handler");

    /*
    if (r->method != NGX_HTTP_GET &&
        r->method != NGX_HTTP_POST && r->method != NGX_HTTP_HEAD) {
        dd("ModSecurity is not ready to deal with anything different from " \
            "POST, GET or HEAD");
        return NGX_OK;
    }
    */
    ctx = ngx_http_modsecurity_get_module_ctx(r);

    dd("recovering ctx: %p", ctx);

    if (ctx == NULL) {
        dd("ModSecurity not enabled or error occurred");
        return NGX_OK;
    }

    if (ctx->logged) {
        dd("already logged earlier");
        return NGX_OK;
    }

    dd("calling msc_process_logging for %p", ctx);
    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    msc_process_logging(ctx->modsec_transaction);
    ngx_http_modsecurity_pcre_malloc_done(old_pool);

    return NGX_OK;
}
