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
#include <ctype.h>
#include <string.h>

#ifndef MODSECURITY_DDEBUG
#define MODSECURITY_DDEBUG 0
#endif
#include "ddebug.h"

#include "ngx_http_modsecurity_common.h"
#include "ngx_http_modsecurity_mapper.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"
#include "msconnector/rule_id.h"

static ngx_http_output_body_filter_pt ngx_http_next_body_filter;
static ngx_int_t ngx_http_modsecurity_phase4_in_scope(ngx_http_request_t *r);
static ngx_int_t ngx_http_modsecurity_phase4_log_event(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf, const char *wanted, const char *actual, const char *reason);
static ngx_int_t ngx_http_modsecurity_phase4_handle_intervention(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf);
static ngx_int_t ngx_http_modsecurity_validate_response_mapper_once(ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx);
static ngx_int_t ngx_http_modsecurity_append_limited_response_body(ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf, u_char *data, size_t len, ngx_int_t in_scope);
static void ngx_http_modsecurity_common_rule(ngx_pool_t *pool, ngx_str_t *intervention, ngx_str_t *rule_id);
static const char *ngx_http_modsecurity_phase4_actual_action(msconnector_late_intervention_action action, const char *requested_action);

/* XXX: check behaviour on few body filters installed */
ngx_int_t
ngx_http_modsecurity_body_filter_init(void)
{
    ngx_http_next_body_filter = ngx_http_top_body_filter;
    ngx_http_top_body_filter = ngx_http_modsecurity_body_filter;

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_validate_response_mapper_once(ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx)
{
    msconnector_response_mapper_contract contract;
    msconnector_response mapped_response;
    char mapper_error[128];

    if (ctx->common_response_validated) {
        return NGX_OK;
    }

    msconnector_response_mapper_contract_init(&contract);
    if (!ngx_http_modsecurity_map_response_from_ctx(ctx, r, &contract,
            &mapped_response, mapper_error, sizeof(mapper_error))) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity common response-body mapper validation skipped: %s", mapper_error);
    }
    ctx->common_response_validated = 1;

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_limited_response_body(ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, u_char *data, size_t len, ngx_int_t in_scope)
{
    size_t limit;
    size_t allowed;
    size_t remaining;

    if (len == 0U) {
        return NGX_OK;
    }

    limit = mcf ? mcf->common_config.phase4_body_limit : 0U;
    allowed = len;

    ctx->response_body_seen = 1;
    ctx->response_body_bytes_seen += len;

    if (in_scope == 0) {
        return NGX_OK;
    }

    if (limit > 0U && ctx->response_body_bytes_inspected >= limit) {
        ctx->response_body_truncated = 1;
        return NGX_OK;
    }

    if (limit > 0U) {
        remaining = limit - ctx->response_body_bytes_inspected;
        if (allowed > remaining) {
            allowed = remaining;
        }
    }

    if (allowed > 0U) {
        if (msc_append_response_body(ctx->modsec_transaction, data, allowed) < 0) {
            return NGX_ERROR;
        }
        ctx->response_body_bytes_inspected += allowed;
    }
    if (allowed < len) {
        ctx->response_body_truncated = 1;
    }
    return NGX_OK;
}

ngx_int_t
ngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in)
{
    ngx_chain_t *chain = in;
    ngx_http_modsecurity_ctx_t *ctx = NULL;
    ngx_http_modsecurity_conf_t *mcf;
#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_list_part_t *part = &r->headers_out.headers.part;
    ngx_table_elt_t *data = part->elts;
    ngx_uint_t i = 0;
#endif

    if (in == NULL) {
        return ngx_http_next_body_filter(r, in);
    }

    ctx = ngx_http_modsecurity_get_module_ctx(r);

    dd("body filter, recovering ctx: %p", ctx);

    if (ctx == NULL) {
        return ngx_http_next_body_filter(r, in);
    }

    if (ctx->intervention_triggered) {
        return ngx_http_next_body_filter(r, in);
    }

    if (ngx_http_modsecurity_validate_response_mapper_once(r, ctx) != NGX_OK) {
        return NGX_ERROR;
    }

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (mcf != NULL && mcf->sanity_checks_enabled != NGX_CONF_UNSET)
    {
#if 0
        dd("dumping stored ctx headers");
        for (i = 0; i < ctx->sanity_headers_out->nelts; i++)
        {
            ngx_http_modsecurity_header_t *vals = ctx->sanity_headers_out->elts;
            ngx_str_t *s2 = &vals[i].name, *s3 = &vals[i].value;
            dd(" dump[%d]: name = '%.*s', value = '%.*s'", (int)i,
                (int)s2->len, (char*)s2->data,
                (int)s3->len, (char*)s3->data);
        }
#endif
        /*
         * Identify if there is a header that was not inspected by ModSecurity.
         */
        int worth_to_fail = 0;

        for (i = 0; ; i++)
        {
            int found = 0;
            ngx_uint_t j = 0;
            ngx_table_elt_t *s1;
            ngx_http_modsecurity_header_t *vals;

            if (i >= part->nelts)
            {
                if (part->next == NULL) {
                    break;
                }

                part = part->next;
                data = part->elts;
                i = 0;
            }

            vals = ctx->sanity_headers_out->elts;
            s1 = &data[i];

            /*
             * Headers that were inspected by ModSecurity.
             */
            while (j < ctx->sanity_headers_out->nelts)
            {
                ngx_str_t *s2 = &vals[j].name;
                ngx_str_t *s3 = &vals[j].value;

                if (s1->key.len == s2->len && ngx_strncmp(s1->key.data, s2->data, s1->key.len) == 0)
                {
                    if (s1->value.len == s3->len && ngx_strncmp(s1->value.data, s3->data, s1->value.len) == 0)
                    {
                        found = 1;
                        break;
                    }
                }
                j++;
            }
            if (!found) {
                dd("header: `%.*s' with value: `%.*s' was not inspected by ModSecurity",
                    (int) s1->key.len,
                    (const char *) s1->key.data,
                    (int) s1->value.len,
                    (const char *) s1->value.data);
                worth_to_fail++;
            }
        }

        if (worth_to_fail)
        {
            dd("%d header(s) were not inspected by ModSecurity, so exiting", worth_to_fail);
            return ngx_http_filter_finalize_request(r,
                &ngx_http_modsecurity_module, NGX_HTTP_INTERNAL_SERVER_ERROR);
        }
    }
#endif

    int is_request_processed = 0;
    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    for (; chain != NULL; chain = chain->next)
    {
        u_char *data = chain->buf->pos;
        size_t len = chain->buf->last >= chain->buf->pos
            ? (size_t) (chain->buf->last - chain->buf->pos)
            : 0;
        int ret;

        if (ngx_http_modsecurity_append_limited_response_body(ctx, mcf, data,
                len, ngx_http_modsecurity_phase4_in_scope(r)) != NGX_OK) {
            return NGX_ERROR;
        }

        is_request_processed = chain->buf->last_buf ||
            chain->buf->last_in_chain;

        if (!is_request_processed) {
            continue;
        }

        if (ctx->phase4_processed) {
            continue;
        }
        ctx->phase4_processed = 1;
        ctx->response_committed = r->header_sent ? 1 : 0;

        {
            ngx_pool_t *old_pool;

            old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
            if (msc_process_response_body(ctx->modsec_transaction) < 0) {
                ngx_http_modsecurity_pcre_malloc_done(old_pool);
                return NGX_ERROR;
            }
            ngx_http_modsecurity_pcre_malloc_done(old_pool);

/* XXX: I don't get how body from modsec being transferred to nginx's buffer.  If so - after adjusting of nginx's
   XXX: body we can proceed to adjust body size (content-length).  see xslt_body_filter() for example */
            ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction, r, 0);
            if (ret != 0) {
                ctx->phase4_intervention = 1;
                ctx->response_committed = r->header_sent ? 1 : 0;
                ret = ngx_http_modsecurity_phase4_handle_intervention(r, mcf);
                if (ret != NGX_OK) {
                    return ret;
                }
                return ngx_http_next_body_filter(r, in);
            }
        }
    }
    if (!is_request_processed)
    {
        dd("buffer was not fully loaded! ctx: %p", ctx);
    }

/* XXX: xflt_filter() -- return NGX_OK here */
    return ngx_http_next_body_filter(r, in);
}

static ngx_int_t
ngx_http_modsecurity_phase4_handle_intervention(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf)
{
    ngx_http_modsecurity_ctx_t *ctx = ngx_http_modsecurity_get_module_ctx(r);
    ngx_int_t in_scope = ngx_http_modsecurity_phase4_in_scope(r);
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action action;
    const char *actual;
    const char *wanted = "deny";
    if (ctx && ctx->last_intervention_status >= 300 && ctx->last_intervention_status < 400) {
        wanted = "redirect";
    }
    if (ctx && ctx->phase4_headers_checked) return NGX_OK;
    if (ctx) ctx->phase4_headers_checked = 1;
    if (ctx) {
        ctx->phase4_intervention = 1;
        ctx->response_committed = r->header_sent ? 1 : 0;
    }

    if (in_scope == 0) {
        ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, "log_only", r->headers_out.content_type.len ? "content_type_not_in_scope" : "content_type_missing");
        return NGX_OK;
    }

    msconnector_late_intervention_policy_init(&policy);
    action = msconnector_late_intervention_resolve(&policy,
        r->header_sent ? 1 : 0,
        r->header_sent ? 1 : 0,
        mcf->phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
    actual = ngx_http_modsecurity_phase4_actual_action(action, wanted);

    if (action == MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE) {
        ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
            "response_not_committed");
        return ctx != NULL && ctx->last_intervention_status > 0
            ? ctx->last_intervention_status : NGX_HTTP_FORBIDDEN;
    }
    if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION) {
        if (ctx) {
            ctx->phase4_strict_abort = 1;
        }
        ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
            "response_committed_strict");
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "modsecurity phase4 intervention after response commit, action=abort_connection, uri=\"%V\"", &r->uri);
        r->connection->error = 1;
        return NGX_ERROR;
    }
    ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
        "response_committed_safe");
    return NGX_OK;
}

static const char *
ngx_http_modsecurity_phase4_actual_action(msconnector_late_intervention_action action,
    const char *requested_action)
{
    const char *name = msconnector_late_intervention_action_name(action);

    if (ngx_strcmp(name, "deny_if_possible") == 0) {
        return requested_action != NULL &&
            ngx_strcmp(requested_action, "redirect") == 0
            ? "redirect" : "deny";
    }
    return name;
}

static ngx_int_t
ngx_http_modsecurity_phase4_in_scope(ngx_http_request_t *r)
{
    ngx_http_modsecurity_conf_t *mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    ngx_uint_t i;
    ngx_str_t ct;
    u_char *semi;
    if (r->headers_out.content_type.len == 0 || mcf->phase4_content_types == NULL) return 0;
    ct = r->headers_out.content_type;
    semi = (u_char *)ngx_strlchr(ct.data, ct.data + ct.len, ';');
    if (semi != NULL) ct.len = semi - ct.data;
    while (ct.len > 0 && isspace((unsigned char)ct.data[ct.len - 1])) ct.len--;
    for (i = 0; i < mcf->phase4_content_types->nelts; i++) {
        ngx_str_t *arr = mcf->phase4_content_types->elts;
        if (arr[i].len == ct.len && ngx_strncasecmp(arr[i].data, ct.data, ct.len) == 0) return 1;
    }
    return 0;
}

static ngx_int_t
ngx_http_modsecurity_phase4_log_event(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf, const char *wanted, const char *actual, const char *reason)
{
    msconnector_event event;
    char line[4096];
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    char content_type[256];
    ngx_str_t raw_log;
    ngx_str_t extracted_rule;
    int original_status;
    int json_truncated = 0;
    size_t content_type_length = 0U;
    size_t line_length;
    ssize_t written;
    ngx_http_modsecurity_ctx_t *ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (mcf->phase4_log_file == NULL ||
        mcf->phase4_log_file->fd == NGX_INVALID_FILE) {
        return NGX_OK;
    }

    original_status = r->err_status != 0 ? (int)r->err_status :
        (r->headers_out.status != 0 ? (int)r->headers_out.status : (int)NGX_HTTP_OK);
    content_type[0] = '\0';
    if (r->headers_out.content_type.data != NULL &&
        r->headers_out.content_type.len > 0U &&
        r->headers_out.content_type.len < sizeof(content_type)) {
        content_type_length = r->headers_out.content_type.len;
        ngx_memcpy(content_type, r->headers_out.content_type.data,
            content_type_length);
        content_type[content_type_length] = '\0';
    }
    rule_id[0] = '\0';
    if (ctx) {
        raw_log = ctx->last_intervention_log;
        ngx_http_modsecurity_common_rule(r->pool, &raw_log, &extracted_rule);
        if (extracted_rule.data != NULL && extracted_rule.len > 0U) {
            size_t length = extracted_rule.len < sizeof(rule_id) - 1U
                ? extracted_rule.len : sizeof(rule_id) - 1U;
            ngx_memcpy(rule_id, extracted_rule.data, length);
            rule_id[length] = '\0';
        }
    } else {
        raw_log.len = 0;
        raw_log.data = (u_char *)"";
    }

    msconnector_event_init(&event);
    event.meta.message_id = strcmp(actual, "abort_connection") == 0
        ? MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200
        : (strcmp(actual, "log_only") == 0
            ? MSCONN_EVENT_PHASE4_LATE_INTERVENTION
            : MSCONN_EVENT_RESPONSE_BLOCKED);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = "phase4_intervention";
    event.meta.connector = "nginx";
    event.meta.transaction_id = ctx != NULL && ctx->event_transaction_id.len > 0U
        ? (const char *) ctx->event_transaction_id.data : "";
    event.decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual;
    event.decision.requested_action = wanted;
    event.decision.actual_action = actual;
    event.decision.rule_id = rule_id;
    event.decision.reason = reason;
    event.http.http_status = ctx != NULL && ctx->last_intervention_status > 0
        ? (int)ctx->last_intervention_status : NGX_HTTP_FORBIDDEN;
    event.http.original_http_status = original_status;
    event.http.visible_http_status = (strcmp(actual, "deny") == 0 ||
        strcmp(actual, "redirect") == 0)
        ? event.http.http_status : original_status;
    event.http.transport_result = strcmp(actual, "abort_connection") == 0
        ? "connection_aborted" : (strcmp(actual, "log_only") == 0
            ? "log_only" : "http_status");
    event.flags.late_intervention = ctx != NULL && ctx->response_committed;
    event.body.content_type = content_type;
    event.body.bytes_seen = ctx != NULL ? ctx->response_body_bytes_seen : 0U;
    event.body.bytes_inspected = ctx != NULL
        ? ctx->response_body_bytes_inspected : 0U;
    event.flags.response_started = r->header_sent ? 1 :
        (ctx != NULL && ctx->response_body_seen);
    event.flags.response_committed = ctx != NULL && ctx->response_committed;
    event.flags.headers_sent = r->header_sent ? 1 : 0;
    event.flags.body_started = ctx != NULL && ctx->response_body_seen;
    event.flags.body_truncated = ctx != NULL && ctx->response_body_truncated;
    event.flags.connection_aborted = ctx != NULL && ctx->phase4_strict_abort;

    if (!msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated)) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity phase4 common event serialization failed%s",
            json_truncated ? " (truncated)" : "");
        return NGX_ERROR;
    }

    line_length = ngx_strlen(line);
    written = ngx_write_fd(mcf->phase4_log_file->fd, (u_char *)line,
        line_length);
    if (written < 0 || (size_t)written != line_length) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, ngx_errno,
            "modsecurity phase4 log write failed");
        return NGX_ERROR;
    }
    return NGX_OK;
}

static void
ngx_http_modsecurity_common_rule(ngx_pool_t *pool, ngx_str_t *intervention, ngx_str_t *rule_id)
{
    char extracted[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    int rule_id_result;

    extracted[0] = '\0';
    rule_id->data = (u_char *)"";
    rule_id->len = 0;
    if (intervention == NULL || intervention->data == NULL) {
        return;
    }
    char *message = ngx_pnalloc(pool, intervention->len + 1U);
    if (message == NULL) {
        return;
    }
    ngx_memcpy(message, intervention->data, intervention->len);
    message[intervention->len] = '\0';
    rule_id_result = msconnector_rule_id_extract_from_message(message, extracted, sizeof(extracted));
    if (rule_id_result > 0) {
        rule_id->len = ngx_strlen(extracted);
        rule_id->data = ngx_pnalloc(pool, rule_id->len + 1U);
        if (rule_id->data == NULL) {
            rule_id->len = 0;
            rule_id->data = (u_char *)"";
            return;
        }
        ngx_memcpy(rule_id->data, extracted, rule_id->len);
        rule_id->data[rule_id->len] = '\0';
    }
}
