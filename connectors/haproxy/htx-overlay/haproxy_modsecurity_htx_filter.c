/*
 * HAProxy 3.2.21 HTX ModSecurity observer filter.
 *
 * This file is deliberately kept outside the upstream HAProxy tree.  The
 * companion build-overlay.sh copies it into a version-pinned 3.2.21 worktree
 * and links it with the repository-owned ModSecurity binding.
 *
 * The filter is an observer, not a response-rewrite or a buffering filter:
 *
 *   - http_payload walks only the current HTX DATA slices and passes their
 *     borrowed pointers directly to haproxy_modsecurity_binding;
 *   - no response bytes, chains, or HTX blocks are retained in this module;
 *   - Phase 4 is evaluated once from http_end, after HAProxy has forwarded
 *     all body data; a resulting intervention is therefore reported but is
 *     never translated into a late deny, redirect, or connection action.
 *
 * The currently available binding finalizes request phase 2 in
 * haproxy_modsecurity_transaction_begin().  To avoid pretending that a
 * streaming request body has been processed, this narrow overlay begins a
 * transaction only when the request reached EOS with no body bytes and no
 * advertised body framing.  Body-bearing or response-before-request-EOS
 * exchanges are explicitly bypassed.  A future binding with request append /
 * finish primitives can remove that conservative guard without changing the
 * response HTX lifecycle below.
 */

#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <haproxy/api.h>
#include <haproxy/channel-t.h>
#include <haproxy/errors.h>
#include <haproxy/filters.h>
#include <haproxy/http_ana-t.h>
#include <haproxy/http_htx.h>
#include <haproxy/htx.h>
#include <haproxy/init.h>
#include <haproxy/stream.h>
#include <haproxy/tools.h>

#include "haproxy_modsecurity_binding.h"

#define HAPROXY_MODSECURITY_HTX_MAX_HEADERS 256U
#define HAPROXY_MODSECURITY_HTX_MAX_HEADER_BYTES 16384U
#define HAPROXY_MODSECURITY_HTX_MAX_METHOD_BYTES 32U
#define HAPROXY_MODSECURITY_HTX_MAX_URI_BYTES 8192U
#define HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES 32U

const char *haproxy_modsecurity_htx_filter_id = "modsecurity-htx observer filter";

struct haproxy_modsecurity_htx_filter_config {
    char *rules_file;
    haproxy_modsecurity_engine *engine;
};

struct haproxy_modsecurity_htx_owned_headers {
    haproxy_modsecurity_header *items;
    unsigned int count;
};

struct haproxy_modsecurity_htx_filter_context {
    haproxy_modsecurity_transaction *transaction;
    struct haproxy_modsecurity_htx_owned_headers request_headers;
    char *request_method;
    char *request_uri;
    unsigned long long request_body_bytes;
    int request_headers_seen;
    int request_body_advertised;
    int request_finished;
    int response_headers_seen;
    int response_finished;
    int disabled;
};

static int haproxy_modsecurity_htx_ascii_equal(const struct ist value, const char *literal)
{
    size_t i;
    size_t literal_len;

    if (!literal) {
        return 0;
    }
    literal_len = strlen(literal);
    if (value.len != literal_len) {
        return 0;
    }
    for (i = 0; i < literal_len; ++i) {
        unsigned char left = (unsigned char)value.ptr[i];
        unsigned char right = (unsigned char)literal[i];

        if (left >= 'A' && left <= 'Z') {
            left = (unsigned char)(left - 'A' + 'a');
        }
        if (right >= 'A' && right <= 'Z') {
            right = (unsigned char)(right - 'A' + 'a');
        }
        if (left != right) {
            return 0;
        }
    }
    return 1;
}

static char *haproxy_modsecurity_htx_dup_ist(const struct ist value, size_t limit)
{
    char *copy;

    if (value.len > limit || value.len > SIZE_MAX - 1U) {
        return NULL;
    }
    copy = calloc(value.len + 1U, 1U);
    if (!copy) {
        return NULL;
    }
    if (value.len != 0U) {
        memcpy(copy, value.ptr, value.len);
    }
    return copy;
}

static void haproxy_modsecurity_htx_owned_headers_free(
    struct haproxy_modsecurity_htx_owned_headers *headers)
{
    unsigned int i;

    if (!headers) {
        return;
    }
    for (i = 0; i < headers->count; ++i) {
        free((char *)headers->items[i].name);
        free((char *)headers->items[i].value);
    }
    free(headers->items);
    headers->items = NULL;
    headers->count = 0U;
}

static void haproxy_modsecurity_htx_request_snapshot_free(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (!ctx) {
        return;
    }
    haproxy_modsecurity_htx_owned_headers_free(&ctx->request_headers);
    free(ctx->request_method);
    free(ctx->request_uri);
    ctx->request_method = NULL;
    ctx->request_uri = NULL;
}

static int haproxy_modsecurity_htx_copy_headers(
    const struct htx *htx,
    struct haproxy_modsecurity_htx_owned_headers *headers)
{
    struct htx_blk *blk;
    unsigned int count = 0U;

    if (!htx || !headers) {
        return -1;
    }
    memset(headers, 0, sizeof(*headers));
    for (blk = htx_get_first_blk(htx); blk; blk = htx_get_next_blk(htx, blk)) {
        enum htx_blk_type type = htx_get_blk_type(blk);

        if (type == HTX_BLK_EOH) {
            break;
        }
        if (type == HTX_BLK_HDR) {
            if (count == HAPROXY_MODSECURITY_HTX_MAX_HEADERS) {
                return -1;
            }
            ++count;
        }
    }
    if (count == 0U) {
        return 0;
    }
    headers->items = calloc(count, sizeof(*headers->items));
    if (!headers->items) {
        return -1;
    }
    for (blk = htx_get_first_blk(htx); blk; blk = htx_get_next_blk(htx, blk)) {
        struct ist name;
        struct ist value;
        enum htx_blk_type type = htx_get_blk_type(blk);

        if (type == HTX_BLK_EOH) {
            break;
        }
        if (type != HTX_BLK_HDR) {
            continue;
        }
        name = htx_get_blk_name(htx, blk);
        value = htx_get_blk_value(htx, blk);
        headers->items[headers->count].name =
            haproxy_modsecurity_htx_dup_ist(name, HAPROXY_MODSECURITY_HTX_MAX_HEADER_BYTES);
        headers->items[headers->count].value =
            haproxy_modsecurity_htx_dup_ist(value, HAPROXY_MODSECURITY_HTX_MAX_HEADER_BYTES);
        if (!headers->items[headers->count].name || !headers->items[headers->count].value) {
            haproxy_modsecurity_htx_owned_headers_free(headers);
            return -1;
        }
        ++headers->count;
    }
    return 0;
}

static int haproxy_modsecurity_htx_parse_nonzero_decimal(const struct ist value)
{
    size_t i;
    unsigned long long parsed = 0U;

    if (value.len == 0U) {
        return 1;
    }
    for (i = 0; i < value.len; ++i) {
        unsigned char byte = (unsigned char)value.ptr[i];

        if (byte < '0' || byte > '9') {
            return 1;
        }
        if (parsed > (ULLONG_MAX - (unsigned long long)(byte - '0')) / 10U) {
            return 1;
        }
        parsed = parsed * 10U + (unsigned long long)(byte - '0');
    }
    return parsed != 0U;
}

static int haproxy_modsecurity_htx_request_advertises_body(const struct htx *htx)
{
    struct htx_blk *blk;

    if (!htx) {
        return 1;
    }
    for (blk = htx_get_first_blk(htx); blk; blk = htx_get_next_blk(htx, blk)) {
        struct ist name;
        struct ist value;
        enum htx_blk_type type = htx_get_blk_type(blk);

        if (type == HTX_BLK_EOH) {
            break;
        }
        if (type != HTX_BLK_HDR) {
            continue;
        }
        name = htx_get_blk_name(htx, blk);
        value = htx_get_blk_value(htx, blk);
        if (haproxy_modsecurity_htx_ascii_equal(name, "content-length") &&
            haproxy_modsecurity_htx_parse_nonzero_decimal(value)) {
            return 1;
        }
        if (haproxy_modsecurity_htx_ascii_equal(name, "transfer-encoding")) {
            return 1;
        }
    }
    return 0;
}

static unsigned int haproxy_modsecurity_htx_data_bytes(
    struct http_msg *msg, unsigned int offset, unsigned int len)
{
    struct htx *htx;
    struct htx_blk *blk;
    struct htx_ret found;
    unsigned int remaining = len;
    unsigned int data_bytes = 0U;

    if (!msg || !msg->chn || len == 0U) {
        return 0U;
    }
    htx = htxbuf(&msg->chn->buf);
    found = htx_find_offset(htx, offset);
    blk = found.blk;
    offset = found.ret;
    for (; blk && remaining; blk = htx_get_next_blk(htx, blk)) {
        enum htx_blk_type type = htx_get_blk_type(blk);
        uint32_t block_size = htx_get_blksz(blk);

        if (type == HTX_BLK_UNUSED) {
            continue;
        }
        if (type == HTX_BLK_DATA) {
            struct ist value = htx_get_blk_value(htx, blk);

            if (offset > value.len) {
                return data_bytes;
            }
            value = istadv(value, offset);
            if (value.len > remaining) {
                value = isttrim(value, remaining);
            }
            if (value.len > UINT_MAX - data_bytes) {
                return UINT_MAX;
            }
            data_bytes += (unsigned int)value.len;
            remaining -= (unsigned int)value.len;
        } else {
            if (offset != 0U) {
                return data_bytes;
            }
            if (block_size > remaining) {
                return data_bytes;
            }
            remaining -= block_size;
        }
        offset = 0U;
    }
    return data_bytes;
}

static void haproxy_modsecurity_htx_report_decision(
    const char *stage, const haproxy_modsecurity_decision *decision)
{
    if (!decision || !decision->disruptive) {
        return;
    }
    /* Do not include decision->log_message, URI, headers, or body bytes. */
    ha_warning("modsecurity-htx observer: %s intervention observed; phase=%d status=%d rule_id=%d action=%s; no late HAProxy action is attempted\n",
        stage, decision->phase, decision->status, decision->rule_id,
        decision->action[0] ? decision->action : "deny");
}

static void haproxy_modsecurity_htx_abort_context(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (!ctx) {
        return;
    }
    if (ctx->transaction) {
        haproxy_modsecurity_transaction_abort(ctx->transaction);
        ctx->transaction = NULL;
    }
    haproxy_modsecurity_htx_request_snapshot_free(ctx);
    ctx->disabled = 1;
}

static void haproxy_modsecurity_htx_finish_context(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (!ctx || !ctx->transaction) {
        return;
    }
    haproxy_modsecurity_transaction_finish(ctx->transaction);
    ctx->transaction = NULL;
}

static int haproxy_modsecurity_htx_capture_request_headers(
    struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct htx *htx;
    struct htx_sl *sl;
    struct ist method;
    struct ist uri;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    htx = htxbuf(&msg->chn->buf);
    sl = http_get_stline(htx);
    if (!sl) {
        return -1;
    }
    ctx->request_body_advertised = haproxy_modsecurity_htx_request_advertises_body(htx);
    if (ctx->request_body_advertised) {
        return 0;
    }
    if (haproxy_modsecurity_htx_copy_headers(htx, &ctx->request_headers) != 0) {
        return -1;
    }
    method = htx_sl_req_meth(sl);
    uri = htx_sl_req_uri(sl);
    ctx->request_method = haproxy_modsecurity_htx_dup_ist(method,
        HAPROXY_MODSECURITY_HTX_MAX_METHOD_BYTES);
    ctx->request_uri = haproxy_modsecurity_htx_dup_ist(uri,
        HAPROXY_MODSECURITY_HTX_MAX_URI_BYTES);
    if (!ctx->request_method || !ctx->request_uri) {
        haproxy_modsecurity_htx_request_snapshot_free(ctx);
        return -1;
    }
    return 0;
}

static int haproxy_modsecurity_htx_begin_bodyless_request(
    struct stream *s, struct filter *filter)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct haproxy_modsecurity_htx_filter_config *config = FLT_CONF(filter);
    char request_id[32];
    haproxy_modsecurity_request request;
    haproxy_modsecurity_decision decision;
    int rc;

    if (!ctx || !config || !config->engine || !ctx->request_method ||
        !ctx->request_uri) {
        return -1;
    }
    snprintf(request_id, sizeof(request_id), "%u", s->uniq_id);
    memset(&request, 0, sizeof(request));
    request.request_id = request_id;
    request.method = ctx->request_method;
    request.uri = ctx->request_uri;
    request.headers = ctx->request_headers.items;
    request.header_count = ctx->request_headers.count;
    rc = haproxy_modsecurity_transaction_begin(config->engine, &request,
        &decision, &ctx->transaction);
    haproxy_modsecurity_htx_request_snapshot_free(ctx);
    if (rc != 0) {
        return -1;
    }
    haproxy_modsecurity_htx_report_decision("request", &decision);
    if (decision.disruptive) {
        haproxy_modsecurity_htx_finish_context(ctx);
        ctx->disabled = 1;
    }
    return 0;
}

static int haproxy_modsecurity_htx_process_response_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct haproxy_modsecurity_htx_owned_headers headers;
    struct htx *htx;
    struct htx_sl *sl;
    struct ist protocol;
    char *protocol_copy = NULL;
    haproxy_modsecurity_response response;
    haproxy_modsecurity_decision decision;
    int rc;

    if (!ctx || !ctx->transaction || !msg || !msg->chn) {
        return -1;
    }
    htx = htxbuf(&msg->chn->buf);
    sl = http_get_stline(htx);
    if (!sl || haproxy_modsecurity_htx_copy_headers(htx, &headers) != 0) {
        return -1;
    }
    protocol = htx_sl_res_vsn(sl);
    protocol_copy = haproxy_modsecurity_htx_dup_ist(protocol,
        HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES);
    if (!protocol_copy) {
        haproxy_modsecurity_htx_owned_headers_free(&headers);
        return -1;
    }
    memset(&response, 0, sizeof(response));
    response.status = s && s->txn && s->txn->status > 0 ? s->txn->status : 200;
    response.protocol = protocol_copy;
    response.headers = headers.items;
    response.header_count = headers.count;
    rc = haproxy_modsecurity_transaction_process_response_headers(
        ctx->transaction, &response, &decision);
    free(protocol_copy);
    haproxy_modsecurity_htx_owned_headers_free(&headers);
    if (rc != 0) {
        return -1;
    }
    ctx->response_headers_seen = 1;
    haproxy_modsecurity_htx_report_decision("response-header", &decision);
    if (decision.disruptive) {
        haproxy_modsecurity_htx_finish_context(ctx);
        ctx->disabled = 1;
    }
    return 0;
}

static int haproxy_modsecurity_htx_append_response_payload(
    struct filter *filter, struct http_msg *msg, unsigned int offset, unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct htx *htx;
    struct htx_blk *blk;
    struct htx_ret found;
    unsigned int remaining = len;

    if (!ctx || !ctx->transaction || !msg || !msg->chn) {
        return -1;
    }
    htx = htxbuf(&msg->chn->buf);
    found = htx_find_offset(htx, offset);
    blk = found.blk;
    offset = found.ret;
    for (; blk && remaining; blk = htx_get_next_blk(htx, blk)) {
        enum htx_blk_type type = htx_get_blk_type(blk);
        uint32_t block_size = htx_get_blksz(blk);

        if (type == HTX_BLK_UNUSED) {
            continue;
        }
        if (type == HTX_BLK_DATA) {
            struct ist value = htx_get_blk_value(htx, blk);
            haproxy_modsecurity_decision decision;

            if (offset > value.len) {
                return -1;
            }
            value = istadv(value, offset);
            if (value.len > remaining) {
                value = isttrim(value, remaining);
            }
            /* `value.ptr` is borrowed from HAProxy's current HTX buffer. */
            if (value.len > UINT_MAX ||
                haproxy_modsecurity_transaction_append_response_body_chunk(
                    ctx->transaction, (const unsigned char *)value.ptr,
                    (unsigned int)value.len, &decision) != 0) {
                return -1;
            }
            remaining -= (unsigned int)value.len;
        } else {
            if (offset != 0U || block_size > remaining) {
                return -1;
            }
            remaining -= block_size;
        }
        offset = 0U;
    }
    return remaining == 0U ? 0 : -1;
}

static int haproxy_modsecurity_htx_filter_init(struct proxy *px, struct flt_conf *fconf)
{
    struct haproxy_modsecurity_htx_filter_config *config = fconf->conf;
    haproxy_modsecurity_engine_config engine_config;
    haproxy_modsecurity_decision decision;

    (void)px;
    if (!config || !config->rules_file || config->rules_file[0] == '\0') {
        ha_alert("modsecurity-htx observer: rules-file is required\n");
        return -1;
    }
    memset(&engine_config, 0, sizeof(engine_config));
    engine_config.connector_info = "HAProxy 3.2.21 native HTX observer overlay";
    engine_config.rules_file = config->rules_file;
    if (haproxy_modsecurity_engine_create(&engine_config, &config->engine, &decision) != 0) {
        ha_alert("modsecurity-htx observer: failed to initialize the ModSecurity engine\n");
        return -1;
    }
    fconf->flags |= FLT_CFG_FL_HTX;
    return 0;
}

static void haproxy_modsecurity_htx_filter_deinit(struct proxy *px, struct flt_conf *fconf)
{
    struct haproxy_modsecurity_htx_filter_config *config = fconf ? fconf->conf : NULL;

    (void)px;
    if (!config) {
        return;
    }
    haproxy_modsecurity_engine_destroy(config->engine);
    free(config->rules_file);
    free(config);
    fconf->conf = NULL;
}

static int haproxy_modsecurity_htx_filter_attach(struct stream *s, struct filter *filter)
{
    struct haproxy_modsecurity_htx_filter_context *ctx;

    (void)s;
    ctx = calloc(1U, sizeof(*ctx));
    if (!ctx) {
        return -1;
    }
    filter->ctx = ctx;
    return 1;
}

static void haproxy_modsecurity_htx_filter_detach(struct stream *s, struct filter *filter)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter ? filter->ctx : NULL;

    (void)s;
    if (!ctx) {
        return;
    }
    haproxy_modsecurity_htx_abort_context(ctx);
    free(ctx);
    filter->ctx = NULL;
}

static int haproxy_modsecurity_htx_filter_http_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (msg->chn->flags & CF_ISRESP) {
        if (!ctx->request_finished || !ctx->transaction || ctx->disabled ||
            haproxy_modsecurity_htx_process_response_headers(s, filter, msg) != 0) {
            haproxy_modsecurity_htx_abort_context(ctx);
        } else if (!ctx->disabled) {
            register_data_filter(s, msg->chn, filter);
        }
        return 1;
    }
    ctx->request_headers_seen = 1;
    if (haproxy_modsecurity_htx_capture_request_headers(filter, msg) != 0) {
        haproxy_modsecurity_htx_abort_context(ctx);
    } else if (ctx->request_body_advertised) {
        /* The current binding only has an atomic request-body API.  Refuse to
         * claim that framed request content was inspected incrementally. */
        ctx->disabled = 1;
    } else {
        register_data_filter(s, msg->chn, filter);
    }
    return 1;
}

static int haproxy_modsecurity_htx_filter_http_payload(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    unsigned int offset, unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    (void)s;
    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (!(msg->chn->flags & CF_ISRESP)) {
        unsigned int body_bytes = haproxy_modsecurity_htx_data_bytes(msg, offset, len);

        if (body_bytes > ULLONG_MAX - ctx->request_body_bytes) {
            ctx->request_body_bytes = ULLONG_MAX;
        } else {
            ctx->request_body_bytes += body_bytes;
        }
        return (int)len;
    }
    if (ctx->disabled || !ctx->transaction || !ctx->response_headers_seen ||
        haproxy_modsecurity_htx_append_response_payload(filter, msg, offset, len) != 0) {
        haproxy_modsecurity_htx_abort_context(ctx);
    }
    /* Never hold or delay output: report the exact bytes HAProxy forwarded. */
    return (int)len;
}

static int haproxy_modsecurity_htx_filter_http_end(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    haproxy_modsecurity_decision decision;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (!(msg->chn->flags & CF_ISRESP)) {
        unregister_data_filter(s, msg->chn, filter);
        if (!ctx->request_finished) {
            ctx->request_finished = 1;
            if (!ctx->disabled && ctx->request_headers_seen &&
                !ctx->request_body_advertised && ctx->request_body_bytes == 0U &&
                haproxy_modsecurity_htx_begin_bodyless_request(s, filter) != 0) {
                haproxy_modsecurity_htx_abort_context(ctx);
            }
        }
        return 1;
    }
    if (ctx->disabled || !ctx->transaction || !ctx->response_headers_seen ||
        ctx->response_finished) {
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    /* HTX http_end is the only Phase-4 evaluation point and is idempotently
     * guarded so the binding's finish primitive is called exactly once. */
    ctx->response_finished = 1;
    if (haproxy_modsecurity_transaction_finish_response_body(ctx->transaction,
            &decision) != 0) {
        haproxy_modsecurity_htx_abort_context(ctx);
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    haproxy_modsecurity_htx_report_decision("response-body (late)", &decision);
    /* All response body bytes have already been forwarded at http_end.  A
     * disruptive rule is intentionally telemetry-only here. */
    haproxy_modsecurity_htx_finish_context(ctx);
    unregister_data_filter(s, msg->chn, filter);
    return 1;
}

static void haproxy_modsecurity_htx_filter_http_reset(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    (void)s;
    (void)msg;
    /* A 100 response or L7 retry invalidates the observed transaction.  Do
     * not reuse it for a later message and do not synthesize a second EOS. */
    haproxy_modsecurity_htx_abort_context(ctx);
}

static void haproxy_modsecurity_htx_filter_http_reply(
    struct stream *s, struct filter *filter, short status, const struct buffer *reply)
{
    (void)s;
    (void)status;
    (void)reply;
    haproxy_modsecurity_htx_abort_context(filter ? filter->ctx : NULL);
}

static struct flt_ops haproxy_modsecurity_htx_filter_ops = {
    .init = haproxy_modsecurity_htx_filter_init,
    .deinit = haproxy_modsecurity_htx_filter_deinit,
    .attach = haproxy_modsecurity_htx_filter_attach,
    .detach = haproxy_modsecurity_htx_filter_detach,
    .http_headers = haproxy_modsecurity_htx_filter_http_headers,
    .http_payload = haproxy_modsecurity_htx_filter_http_payload,
    .http_end = haproxy_modsecurity_htx_filter_http_end,
    .http_reset = haproxy_modsecurity_htx_filter_http_reset,
    .http_reply = haproxy_modsecurity_htx_filter_http_reply,
};

static int haproxy_modsecurity_htx_filter_parse(
    char **args, int *cur_arg, struct proxy *px, struct flt_conf *fconf,
    char **err, void *private)
{
    struct haproxy_modsecurity_htx_filter_config *config;
    int pos;

    (void)px;
    (void)private;
    config = calloc(1U, sizeof(*config));
    if (!config) {
        memprintf(err, "%s: out of memory", args[*cur_arg]);
        return -1;
    }
    pos = *cur_arg + 1;
    if (!args[pos] || strcmp(args[pos], "rules-file") != 0 || !args[pos + 1]) {
        memprintf(err, "'%s' requires 'rules-file <path>'", args[*cur_arg]);
        free(config);
        return -1;
    }
    config->rules_file = strdup(args[pos + 1]);
    if (!config->rules_file) {
        memprintf(err, "%s: out of memory", args[*cur_arg]);
        free(config);
        return -1;
    }
    pos += 2;
    *cur_arg = pos;
    fconf->id = haproxy_modsecurity_htx_filter_id;
    fconf->ops = &haproxy_modsecurity_htx_filter_ops;
    fconf->conf = config;
    return 0;
}

static struct flt_kw_list haproxy_modsecurity_htx_filter_keywords = {
    "MODSECURITY_HTX", { }, {
        { "modsecurity-htx", haproxy_modsecurity_htx_filter_parse, NULL },
        { NULL, NULL, NULL },
    }
};

INITCALL1(STG_REGISTER, flt_register_keywords,
    &haproxy_modsecurity_htx_filter_keywords);
