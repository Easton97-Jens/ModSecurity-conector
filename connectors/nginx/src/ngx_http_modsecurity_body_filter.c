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
#include <stdint.h>
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

static ngx_http_output_body_filter_pt ngx_http_next_body_filter;

/* File-only nginx buffers need bounded materialization before the native
 * libModSecurity append API can inspect them. This is deliberately much
 * smaller than the configurable transaction limit and is reused per request. */
#define NGX_HTTP_MODSECURITY_PHASE4_FILE_READ_CHUNK 32768U

static ngx_int_t
ngx_http_modsecurity_contract_record_response_commit(
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_request_t *r)
{
    if (ctx == NULL || r == NULL || !ctx->contract_initialized || !r->header_sent) {
        return NGX_OK;
    }
    return msconnector_transaction_contract_set_response_committed(&ctx->contract, 1) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK ? NGX_OK : NGX_ERROR;
}
static ngx_int_t ngx_http_modsecurity_phase4_in_scope(ngx_http_request_t *r);
static ngx_int_t ngx_http_modsecurity_phase4_log_event(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf, const char *wanted, const char *actual, const char *reason);
static ngx_int_t ngx_http_modsecurity_phase4_handle_intervention(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf);
static ngx_int_t ngx_http_modsecurity_validate_response_mapper_once(ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx);
static ngx_int_t ngx_http_modsecurity_plan_limited_response_body(
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,
    size_t len, size_t *allowed);
static ngx_int_t ngx_http_modsecurity_append_response_body_chunk(
    ngx_http_modsecurity_ctx_t *ctx, u_char *data, size_t bytes);
static ngx_int_t ngx_http_modsecurity_append_limited_response_body(ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf, u_char *data, size_t len);
static ngx_int_t ngx_http_modsecurity_append_file_response_body(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_buf_t *buffer);
static ngx_int_t ngx_http_modsecurity_append_response_body_buffer(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_buf_t *buffer);
static ngx_int_t ngx_http_modsecurity_prepare_response_body_filter(
    ngx_http_request_t *r, ngx_chain_t *in,
    ngx_http_modsecurity_ctx_t **context);
static ngx_int_t ngx_http_modsecurity_append_response_chain_buffer(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_int_t phase4_in_scope,
    ngx_chain_t *chain);
static ngx_int_t ngx_http_modsecurity_forward_response_body_prefix(
    ngx_http_request_t *r, ngx_chain_t *segment_start,
    ngx_chain_t *segment_previous, ngx_chain_t *chain,
    ngx_chain_t **terminal_input);
static ngx_int_t ngx_http_modsecurity_finalize_terminal_response_body(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_chain_t *in,
    ngx_uint_t *forwarded, ngx_uint_t *processed);
static ngx_int_t ngx_http_modsecurity_process_response_body_chain(
    ngx_http_request_t *r, ngx_chain_t *in,
    ngx_http_modsecurity_ctx_t *ctx);
static void ngx_http_modsecurity_discard_replaced_response_body(ngx_chain_t *in);
static ngx_int_t ngx_http_modsecurity_process_final_response_body(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_chain_t *in,
    ngx_uint_t *forwarded);
static const char *ngx_http_modsecurity_phase4_actual_action(msconnector_late_intervention_action action, const char *requested_action);
static int ngx_http_modsecurity_phase4_original_status(ngx_http_request_t *r);
static const char *ngx_http_modsecurity_phase4_message_id(const char *actual);
static int ngx_http_modsecurity_phase4_visible_status(const char *actual,
    int intervention_status, int original_status);
static const char *ngx_http_modsecurity_phase4_transport_result(const char *actual);
static int ngx_http_modsecurity_phase4_response_started(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx);
static void ngx_http_modsecurity_phase4_copy_content_type(ngx_http_request_t *r,
    char *content_type, size_t content_type_size);
static void ngx_http_modsecurity_phase4_copy_intervention_identifier(
    ngx_http_modsecurity_ctx_t *ctx, char *rule_id, size_t rule_id_size);
#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
static ngx_int_t ngx_http_modsecurity_run_response_header_sanity_checks(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx);
static ngx_int_t ngx_http_modsecurity_response_sanity_next_header(
    ngx_list_part_t **part, ngx_table_elt_t **data, ngx_uint_t *index,
    ngx_table_elt_t **header);
static ngx_int_t ngx_http_modsecurity_response_sanity_header_is_inspected(
    ngx_http_modsecurity_ctx_t *ctx, const ngx_table_elt_t *header);
#endif

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
    if (ctx->common_response_validated) {
        return NGX_OK;
    }

    ngx_http_modsecurity_validate_response_mapper(ctx, r,
        NGX_HTTP_MODSECURITY_RESPONSE_MAPPER_DIAGNOSTIC_BODY);
    ctx->common_response_validated = 1;

    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_plan_limited_response_body(
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,
    size_t len, size_t *allowed)
{
    msconnector_body_limit_plan plan;
    size_t limit;

    if (allowed == NULL) {
        return NGX_ERROR;
    }
    *allowed = 0U;
    if (len == 0U) {
        return NGX_OK;
    }

    limit = mcf ? mcf->common_config.phase4_body_limit : 0U;
    ctx->response_body_seen = 1;
    /* A P4 limit applies before the current native buffer reaches the next
     * filter. Passing an inspected prefix and forwarding an uninspected tail
     * would violate the shared body-limit contract, so NGINX uses the Common
     * reject plan just like the Apache output filter. */
    if (!msconnector_body_limit_plan_chunk(ctx->response_body_bytes_seen,
            ctx->response_body_bytes_inspected, limit,
            MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, len, &plan)) {
        ctx->response_body_bytes_seen = plan.bytes_seen;
        ctx->response_body_truncated = 1;
        (void)msconnector_transaction_contract_fail(&ctx->contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, 0U);
        return NGX_ERROR;
    }
    ctx->response_body_bytes_seen = plan.bytes_seen;
    if (plan.truncated) {
        ctx->response_body_truncated = 1;
    }
    *allowed = plan.append_size;
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_response_body_chunk(
    ngx_http_modsecurity_ctx_t *ctx, u_char *data, size_t bytes)
{
    size_t allowed = bytes;

    if (bytes == 0U) {
        return NGX_OK;
    }
    if (data == NULL || ctx->response_body_bytes_inspected > SIZE_MAX - bytes) {
        (void)msconnector_transaction_contract_fail(&ctx->contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, 0U);
        return NGX_ERROR;
    }
    if (ctx->contract.active_phase != MSCONNECTOR_PHASE_RESPONSE_BODY &&
        ngx_http_modsecurity_contract_begin(ctx,
            MSCONNECTOR_PHASE_RESPONSE_BODY) != NGX_OK) {
        return NGX_ERROR;
    }
    if (msconnector_transaction_contract_record_body(&ctx->contract, 1,
            bytes) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return NGX_ERROR;
    }
    if (msc_append_response_body(ctx->modsec_transaction, data, allowed) != 1) {
        return NGX_ERROR;
    }
    ctx->response_body_bytes_inspected += bytes;
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_limited_response_body(ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, u_char *data, size_t len)
{
    size_t allowed;

    if (ngx_http_modsecurity_plan_limited_response_body(ctx, mcf, len,
            &allowed) != NGX_OK) {
        return NGX_ERROR;
    }
    return ngx_http_modsecurity_append_response_body_chunk(ctx, data, allowed);
}

static ngx_int_t
ngx_http_modsecurity_append_file_response_body(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_buf_t *buffer)
{
    uintmax_t file_length;
    size_t allowed;
    size_t remaining;
    size_t chunk;
    off_t file_offset;
    ssize_t read_count;

    if (buffer == NULL || buffer->file_pos < 0 ||
        buffer->file_last < buffer->file_pos) {
        (void)msconnector_transaction_contract_fail(&ctx->contract,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, 0U);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid file-backed response body metadata");
        return NGX_ERROR;
    }
    file_length = (uintmax_t)buffer->file_last -
        (uintmax_t)buffer->file_pos;
    if (file_length > (uintmax_t)SIZE_MAX) {
        (void)msconnector_transaction_contract_fail(&ctx->contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, 0U);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: file-backed response body exceeds local limits");
        return NGX_ERROR;
    }
    if (ngx_http_modsecurity_plan_limited_response_body(ctx, mcf,
            (size_t)file_length, &allowed) != NGX_OK) {
        return NGX_ERROR;
    }
    if (allowed == 0U) {
        return NGX_OK;
    }
    if (buffer->file == NULL) {
        (void)msconnector_transaction_contract_fail(&ctx->contract,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, 0U);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: missing file-backed response body source");
        return NGX_ERROR;
    }
    if (ctx->phase4_file_scratch == NULL) {
        ctx->phase4_file_scratch = ngx_pnalloc(r->pool,
            NGX_HTTP_MODSECURITY_PHASE4_FILE_READ_CHUNK);
        if (ctx->phase4_file_scratch == NULL) {
            (void)msconnector_transaction_contract_fail(&ctx->contract,
                MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, 0U);
            ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
                "ModSecurity: cannot allocate file-backed response body scratch");
            return NGX_ERROR;
        }
    }

    file_offset = buffer->file_pos;
    remaining = allowed;
    while (remaining > 0U) {
        chunk = remaining > NGX_HTTP_MODSECURITY_PHASE4_FILE_READ_CHUNK
            ? NGX_HTTP_MODSECURITY_PHASE4_FILE_READ_CHUNK : remaining;
        read_count = ngx_read_file(buffer->file, ctx->phase4_file_scratch,
            chunk, file_offset);
        if (read_count < 0 || (size_t)read_count != chunk) {
            (void)msconnector_transaction_contract_fail(&ctx->contract,
                MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, 0U);
            ngx_log_error(NGX_LOG_ERR, r->connection->log,
                read_count < 0 ? ngx_errno : 0,
                "ModSecurity: file-backed response body read is short or failed");
            return NGX_ERROR;
        }
        if (ngx_http_modsecurity_append_response_body_chunk(ctx,
                ctx->phase4_file_scratch, chunk) != NGX_OK) {
            return NGX_ERROR;
        }
        file_offset += (off_t)chunk;
        remaining -= chunk;
    }
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_response_body_buffer(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx,
    ngx_http_modsecurity_conf_t *mcf, ngx_buf_t *buffer)
{
    if (ngx_buf_in_memory(buffer)) {
        u_char *data = buffer->pos;
        size_t len = buffer->last >= buffer->pos
            ? (size_t) (buffer->last - buffer->pos)
            : 0;

        return ngx_http_modsecurity_append_limited_response_body(ctx, mcf,
            data, len);
    }
    if (buffer->in_file) {
        return ngx_http_modsecurity_append_file_response_body(r, ctx, mcf,
            buffer);
    }
    return NGX_OK;
}

static void
ngx_http_modsecurity_discard_replaced_response_body(ngx_chain_t *in)
{
    ngx_chain_t *chain;

    for (chain = in; chain != NULL; chain = chain->next) {
        chain->buf->pos = chain->buf->last;
        chain->buf->in_file = 0;
        chain->buf->file_last = chain->buf->file_pos;
    }
}

static ngx_int_t
ngx_http_modsecurity_process_final_response_body(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,
    ngx_chain_t *in, ngx_uint_t *forwarded)
{
    ngx_pool_t *old_pool;
    int ret;

    *forwarded = 0;
    old_pool = ngx_http_modsecurity_pcre_malloc_init(r->pool);
    if (ctx->contract.active_phase != MSCONNECTOR_PHASE_RESPONSE_BODY &&
        ngx_http_modsecurity_contract_begin(ctx,
            MSCONNECTOR_PHASE_RESPONSE_BODY) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P4 transition");
        return NGX_ERROR;
    }
    ret = msc_process_response_body(ctx->modsec_transaction);
    if (ret != 1) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: response body phase processing failed");
        ctx->intervention_triggered = 1;
        if (r->header_sent) {
            r->connection->error = 1;
            return NGX_ERROR;
        }
        return ngx_http_filter_finalize_request(r,
            &ngx_http_modsecurity_module,
            NGX_HTTP_INTERNAL_SERVER_ERROR);
    }
    if (ngx_http_modsecurity_contract_complete(ctx,
            MSCONNECTOR_PHASE_RESPONSE_BODY) != NGX_OK) {
        ngx_http_modsecurity_pcre_malloc_done(old_pool);
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid canonical P4 completion");
        ctx->intervention_triggered = 1;
        return NGX_ERROR;
    }
    ngx_http_modsecurity_pcre_malloc_done(old_pool);

    ret = ngx_http_modsecurity_process_intervention(ctx->modsec_transaction, r,
        0);
    if (ret == 0) {
        return NGX_OK;
    }

    /* A late intervention cannot safely rewrite committed headers.  Both a
     * negative control failure and a positive intervention use the existing
     * Safe/Strict policy rather than a second generic error response. */
    ctx->phase4_intervention = 1;
    ctx->response_committed = r->header_sent ? 1 : 0;
    ret = ngx_http_modsecurity_phase4_handle_intervention(r, mcf);
    if (ret != NGX_OK) {
        return ret;
    }

    *forwarded = 1;
    return ngx_http_next_body_filter(r, in);
}

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
static ngx_int_t
ngx_http_modsecurity_response_sanity_next_header(ngx_list_part_t **part,
    ngx_table_elt_t **data, ngx_uint_t *index, ngx_table_elt_t **header)
{
    while (*index >= (*part)->nelts) {
        if ((*part)->next == NULL) {
            return NGX_DECLINED;
        }
        *part = (*part)->next;
        *data = (*part)->elts;
        *index = 0;
    }
    *header = &(*data)[*index];
    (*index)++;
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_response_sanity_header_is_inspected(
    ngx_http_modsecurity_ctx_t *ctx, const ngx_table_elt_t *header)
{
    ngx_http_modsecurity_header_t *headers;
    ngx_uint_t index;

    headers = ctx->sanity_headers_out->elts;
    for (index = 0; index < ctx->sanity_headers_out->nelts; index++) {
        ngx_str_t *name = &headers[index].name;
        ngx_str_t *value = &headers[index].value;

        if (header->key.len == name->len &&
            ngx_strncmp(header->key.data, name->data, header->key.len) == 0 &&
            header->value.len == value->len &&
            ngx_strncmp(header->value.data, value->data,
                header->value.len) == 0) {
            return NGX_OK;
        }
    }
    return NGX_DECLINED;
}

static ngx_int_t
ngx_http_modsecurity_run_response_header_sanity_checks(
    ngx_http_request_t *r, ngx_http_modsecurity_ctx_t *ctx)
{
    ngx_http_modsecurity_conf_t *mcf;
    ngx_list_part_t *part = &r->headers_out.headers.part;
    ngx_table_elt_t *data = part->elts;
    ngx_table_elt_t *header;
    ngx_uint_t i = 0;
    int worth_to_fail = 0;

    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    if (mcf == NULL || mcf->sanity_checks_enabled == NGX_CONF_UNSET) {
        return NGX_OK;
    }
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
    while (ngx_http_modsecurity_response_sanity_next_header(&part, &data,
            &i, &header) == NGX_OK) {
        if (ngx_http_modsecurity_response_sanity_header_is_inspected(ctx,
                header) != NGX_OK) {
            dd("header: `%.*s' with value: `%.*s' was not inspected by ModSecurity",
                (int) header->key.len,
                (const char *) header->key.data,
                (int) header->value.len,
                (const char *) header->value.data);
            worth_to_fail++;
        }
    }
    if (worth_to_fail == 0) {
        return NGX_OK;
    }
    dd("%d header(s) were not inspected by ModSecurity, so exiting", worth_to_fail);
    return ngx_http_filter_finalize_request(r,
        &ngx_http_modsecurity_module, NGX_HTTP_INTERNAL_SERVER_ERROR);
}
#endif

static ngx_int_t
ngx_http_modsecurity_prepare_response_body_filter(ngx_http_request_t *r,
    ngx_chain_t *in, ngx_http_modsecurity_ctx_t **context)
{
    ngx_http_modsecurity_ctx_t *ctx;

    if (context == NULL) {
        return NGX_ERROR;
    }
    *context = NULL;
    if (in == NULL) {
        return NGX_DECLINED;
    }
    ctx = ngx_http_modsecurity_get_module_ctx(r);
    dd("body filter, recovering ctx: %p", ctx);
    if (ctx == NULL) {
        return NGX_DECLINED;
    }
    if (ctx->response_replaced) {
        /* The Phase-3 header filter installed a body-less redirect before
         * commit. Drain the original body, including file-backed buffers,
         * while preserving completion flags for later filters. */
        ngx_http_modsecurity_discard_replaced_response_body(in);
        return NGX_DECLINED;
    }
    if (ctx->intervention_triggered || ctx->phase4_processed) {
        return NGX_DECLINED;
    }
    if (ngx_http_modsecurity_validate_response_mapper_once(r, ctx) != NGX_OK) {
        return NGX_ERROR;
    }
#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    if (ngx_http_modsecurity_run_response_header_sanity_checks(r, ctx) != NGX_OK) {
        return NGX_ERROR;
    }
#endif
    *context = ctx;
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_append_response_chain_buffer(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,
    ngx_int_t phase4_in_scope, ngx_chain_t *chain)
{
    if (phase4_in_scope == 0) {
        return NGX_OK;
    }
    return ngx_http_modsecurity_append_response_body_buffer(r, ctx, mcf,
        chain->buf);
}

static ngx_int_t
ngx_http_modsecurity_forward_response_body_prefix(ngx_http_request_t *r,
    ngx_chain_t *segment_start, ngx_chain_t *segment_previous,
    ngx_chain_t *chain, ngx_chain_t **terminal_input)
{
    ngx_int_t prefix_ret;

    if (segment_start == chain) {
        return NGX_OK;
    }
    if (segment_previous == NULL) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: invalid response chain prefix state");
        return NGX_ERROR;
    }
    segment_previous->next = NULL;
    prefix_ret = ngx_http_next_body_filter(r, segment_start);
    segment_previous->next = chain;
    if (prefix_ret != NGX_OK) {
        return prefix_ret;
    }
    *terminal_input = chain;
    return NGX_OK;
}

static ngx_int_t
ngx_http_modsecurity_finalize_terminal_response_body(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_http_modsecurity_conf_t *mcf,
    ngx_chain_t *in, ngx_uint_t *forwarded, ngx_uint_t *processed)
{
    *forwarded = 0;
    *processed = 0;
    if (ctx->phase4_processed) {
        return NGX_OK;
    }
    ctx->phase4_processed = 1;
    ctx->response_committed = r->header_sent ? 1 : 0;
    if (ngx_http_modsecurity_contract_record_response_commit(ctx, r) != NGX_OK) {
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "ModSecurity: canonical response commitment is invalid");
        return NGX_ERROR;
    }
    *processed = 1;
    return ngx_http_modsecurity_process_final_response_body(r, ctx, mcf, in,
        forwarded);
}

static ngx_int_t
ngx_http_modsecurity_process_response_body_chain(ngx_http_request_t *r,
    ngx_chain_t *in, ngx_http_modsecurity_ctx_t *ctx)
{
    ngx_chain_t *chain;
    ngx_chain_t *segment_start = in;
    ngx_chain_t *segment_previous = NULL;
    ngx_http_modsecurity_conf_t *mcf;
    ngx_int_t phase4_in_scope;
    int is_request_processed = 0;

    mcf = ngx_http_get_module_loc_conf(r, ngx_http_modsecurity_module);
    phase4_in_scope = ngx_http_modsecurity_phase4_in_scope(r);
    for (chain = in; chain != NULL; chain = chain->next)
    {
        ngx_int_t ret;
        ngx_uint_t final_body_forwarded;
        ngx_uint_t terminal_processed;

        ret = ngx_http_modsecurity_append_response_chain_buffer(r, ctx, mcf,
            phase4_in_scope, chain);
        if (ret != NGX_OK) {
            return ret;
        }
        is_request_processed = chain->buf->last_buf ||
            chain->buf->last_in_chain;
        if (!is_request_processed) {
            segment_previous = chain;
            continue;
        }
        ret = ngx_http_modsecurity_forward_response_body_prefix(r,
            segment_start, segment_previous, chain, &in);
        if (ret != NGX_OK) {
            return ret;
        }
        ret = ngx_http_modsecurity_finalize_terminal_response_body(r, ctx, mcf,
            in, &final_body_forwarded, &terminal_processed);
        if (ret != NGX_OK || final_body_forwarded) {
            return ret;
        }
        if (!terminal_processed) {
            continue;
        }
        /* msc_process_response_body() finalizes the transaction. A later
         * link in this same chain may carry a flush or transformed buffer;
         * preserve it for NGINX, but never append it again. */
        break;
    }
    if (!is_request_processed)
    {
        dd("buffer was not fully loaded! ctx: %p", ctx);
    }
    return ngx_http_next_body_filter(r, in);
}

ngx_int_t
ngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in)
{
    ngx_http_modsecurity_ctx_t *ctx;
    ngx_int_t status;

    status = ngx_http_modsecurity_prepare_response_body_filter(r, in, &ctx);
    if (status == NGX_DECLINED) {
        return ngx_http_next_body_filter(r, in);
    }
    if (status != NGX_OK) {
        return status;
    }
    return ngx_http_modsecurity_process_response_body_chain(r, in, ctx);
}

static ngx_int_t
ngx_http_modsecurity_phase4_handle_intervention(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf)
{
    ngx_http_modsecurity_ctx_t *ctx = ngx_http_modsecurity_get_module_ctx(r);
    ngx_int_t in_scope = ngx_http_modsecurity_phase4_in_scope(r);
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action action;
    ngx_int_t log_result;
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
        return ngx_http_modsecurity_phase4_log_event(r, mcf, wanted,
            "log_only", r->headers_out.content_type.len
                ? "content_type_not_in_scope" : "content_type_missing");
    }

    msconnector_late_intervention_policy_init(&policy);
    action = msconnector_late_intervention_resolve(&policy,
        r->header_sent ? 1 : 0,
        ngx_http_modsecurity_phase4_response_started(r, ctx),
        mcf->phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
    actual = ngx_http_modsecurity_phase4_actual_action(action, wanted);

    if (action == MSCONNECTOR_LATE_INTERVENTION_DENY_IF_POSSIBLE) {
        log_result = ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
            "response_not_committed");
        if (log_result != NGX_OK) {
            return log_result;
        }
        return ctx != NULL && ctx->last_intervention_status > 0
            ? ctx->last_intervention_status : NGX_HTTP_FORBIDDEN;
    }
    if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION) {
        if (ctx) {
            ctx->phase4_strict_abort = 1;
        }
        r->connection->error = 1;
        ngx_log_error(NGX_LOG_ERR, r->connection->log, 0,
            "modsecurity phase4 intervention after response commit, action=abort_connection, uri=\"%V\"", &r->uri);
        log_result = ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
            "response_committed_strict");
        if (log_result != NGX_OK) {
            return log_result;
        }
        return NGX_ERROR;
    }
    return ngx_http_modsecurity_phase4_log_event(r, mcf, wanted, actual,
        "response_committed_safe");
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

static const char *
ngx_http_modsecurity_phase4_mode_name(ngx_uint_t mode)
{
    switch (mode) {
    case MSCONNECTOR_PHASE4_MODE_MINIMAL:
        return "minimal";
    case MSCONNECTOR_PHASE4_MODE_SAFE:
        return "safe";
    case MSCONNECTOR_PHASE4_MODE_STRICT:
        return "strict";
    default:
        return NULL;
    }
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

static int
ngx_http_modsecurity_phase4_original_status(ngx_http_request_t *r)
{
    if (r->err_status != 0) {
        return (int)r->err_status;
    }

    if (r->headers_out.status != 0) {
        return (int)r->headers_out.status;
    }

    return (int)NGX_HTTP_OK;
}

static const char *
ngx_http_modsecurity_phase4_message_id(const char *actual)
{
    if (strcmp(actual, "abort_connection") == 0) {
        return MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200;
    }

    if (strcmp(actual, "log_only") == 0) {
        return MSCONN_EVENT_PHASE4_LATE_INTERVENTION;
    }

    return MSCONN_EVENT_RESPONSE_BLOCKED;
}

static int
ngx_http_modsecurity_phase4_visible_status(const char *actual,
    int intervention_status, int original_status)
{
    if (strcmp(actual, "deny") == 0 || strcmp(actual, "redirect") == 0) {
        return intervention_status;
    }

    return original_status;
}

static const char *
ngx_http_modsecurity_phase4_transport_result(const char *actual)
{
    if (strcmp(actual, "abort_connection") == 0) {
        return "connection_aborted";
    }

    if (strcmp(actual, "log_only") == 0) {
        return "log_only";
    }

    return "http_status";
}

static int
ngx_http_modsecurity_phase4_response_started(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx)
{
    if (r->header_sent) {
        return 1;
    }

    return ctx != NULL && ctx->response_body_seen;
}

static void
ngx_http_modsecurity_phase4_copy_content_type(ngx_http_request_t *r,
    char *content_type, size_t content_type_size)
{
    size_t content_type_length;

    content_type[0] = '\0';
    if (r->headers_out.content_type.data == NULL ||
        r->headers_out.content_type.len == 0U ||
        r->headers_out.content_type.len >= content_type_size) {
        return;
    }

    content_type_length = r->headers_out.content_type.len;
    ngx_memcpy(content_type, r->headers_out.content_type.data,
        content_type_length);
    content_type[content_type_length] = '\0';
}

static void
ngx_http_modsecurity_phase4_copy_intervention_identifier(
    ngx_http_modsecurity_ctx_t *ctx,
    char *rule_id, size_t rule_id_size)
{
    size_t length;

    rule_id[0] = '\0';
    if (ctx == NULL || ctx->last_intervention_rule_id[0] == '\0') {
        return;
    }

    length = ngx_strlen(ctx->last_intervention_rule_id);
    if (length >= rule_id_size) {
        length = rule_id_size - 1U;
    }
    ngx_memcpy(rule_id, ctx->last_intervention_rule_id, length);
    rule_id[length] = '\0';
}

static ngx_int_t
ngx_http_modsecurity_phase4_log_event(ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf, const char *wanted, const char *actual, const char *reason)
{
    msconnector_event event;
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    char content_type[256];
    int original_status;
    ngx_http_modsecurity_ctx_t *ctx = ngx_http_modsecurity_get_module_ctx(r);

    if (mcf->phase4_log_file == NULL ||
        mcf->phase4_log_file->fd == NGX_INVALID_FILE) {
        return NGX_OK;
    }

    original_status = ngx_http_modsecurity_phase4_original_status(r);
    ngx_http_modsecurity_phase4_copy_content_type(r, content_type,
        sizeof(content_type));
    ngx_http_modsecurity_phase4_copy_intervention_identifier(ctx, rule_id,
        sizeof(rule_id));

    msconnector_event_init(&event);
    event.meta.message_id = ngx_http_modsecurity_phase4_message_id(actual);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = "phase4_intervention";
    event.meta.connector = "nginx";
    event.meta.integration_mode = "native-nginx-http-module";
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
    event.http.visible_http_status = ngx_http_modsecurity_phase4_visible_status(
        actual, event.http.http_status, original_status);
    event.http.transport_result =
        ngx_http_modsecurity_phase4_transport_result(actual);
    event.flags.late_intervention = ctx != NULL && ctx->response_committed;
    if (event.flags.late_intervention) {
        event.flags.late_intervention_mode =
            ngx_http_modsecurity_phase4_mode_name(mcf->phase4_mode);
    }
    event.body.content_type = content_type;
    event.body.bytes_seen = ctx != NULL ? ctx->response_body_bytes_seen : 0U;
    event.body.bytes_inspected = ctx != NULL
        ? ctx->response_body_bytes_inspected : 0U;
    event.flags.response_started =
        ngx_http_modsecurity_phase4_response_started(r, ctx);
    event.flags.response_committed = ctx != NULL && ctx->response_committed;
    event.flags.headers_sent = r->header_sent ? 1 : 0;
    event.flags.body_started = ctx != NULL && ctx->response_body_seen;
    /* The Phase-4 event is emitted from the last_buf/last_in_chain finish
     * path, so this marks engine EOS delivery only. */
    event.flags.eos_seen = 1;
    event.flags.body_truncated = ctx != NULL && ctx->response_body_truncated;
    event.flags.connection_aborted = ctx != NULL && ctx->phase4_strict_abort;

    return ngx_http_modsecurity_write_phase_event_jsonl(r, mcf, &event,
        "phase4");
}
