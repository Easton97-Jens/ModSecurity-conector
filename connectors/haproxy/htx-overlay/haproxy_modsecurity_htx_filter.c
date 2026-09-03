/*
 * HAProxy HTX ModSecurity streaming filter selected by version-contract.json.
 *
 * This file is deliberately kept outside the upstream HAProxy tree.  The
 * companion build-overlay.sh copies it into a version-pinned worktree
 * and links it with the repository-owned ModSecurity binding.
 *
 * The filter is forward-first and does not own a request or response buffer:
 *
 *   - http_payload walks only the current HTX DATA slices and passes borrowed
 *     pointers directly to the matching request or response binding call;
 *   - no bytes, chains, or HTX blocks are retained in this module;
 *   - request Phase 2 and response Phase 4 are finalized exactly once at the
 *     respective HTX http_end callbacks;
 *   - body chunks always return their original length, so this filter never
 *     waits for a complete body before HAProxy can continue forwarding it.
 *
 * A Phase-4 intervention discovered after response commitment is resolved
 * through the Common late-intervention policy.  This overlay currently records
 * the requested and policy-resolved actions only: a reliable HAProxy HTX
 * post-commit stream-abort integration still needs host-runtime verification.
 */

#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <haproxy/api.h>
#include <haproxy/channel-t.h>
#include <haproxy/errors.h>
#include <haproxy/filters.h>
#include <haproxy/http_ana.h>
#include <haproxy/http_ana-t.h>
#include <haproxy/http_htx.h>
#include <haproxy/htx.h>
#include <haproxy/init.h>
#include <haproxy/sc_strm.h>
#include <haproxy/stream.h>
#include <haproxy/sample.h>
#include <haproxy/vars.h>
#include <haproxy/tools.h>

#include "haproxy_modsecurity_binding.h"
#include "response_companion_client.h"
#include "msconnector/block_statuses.h"
#include "msconnector/config.h"
#include "msconnector/config_parser.h"
#include "msconnector/decision_action.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"

#define HAPROXY_MODSECURITY_HTX_MAX_HEADERS MSCONNECTOR_MAX_HEADER_COUNT
#define HAPROXY_MODSECURITY_HTX_MAX_HEADER_NAME_BYTES \
    MSCONNECTOR_MAX_HEADER_NAME_LENGTH
#define HAPROXY_MODSECURITY_HTX_MAX_HEADER_VALUE_BYTES \
    MSCONNECTOR_MAX_HEADER_VALUE_LENGTH
#define HAPROXY_MODSECURITY_HTX_MAX_TOTAL_HEADER_BYTES \
    MSCONNECTOR_MAX_TOTAL_HEADER_BYTES
#define HAPROXY_MODSECURITY_HTX_MAX_METHOD_BYTES 32U
#define HAPROXY_MODSECURITY_HTX_MAX_URI_BYTES 8192U
#define HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES 32U
#define HAPROXY_MODSECURITY_HTX_RESPONSE_HANDLE_LENGTH 64U

const char *haproxy_modsecurity_htx_filter_id = "modsecurity-htx streaming filter";

struct haproxy_modsecurity_htx_filter_config {
    char *rules_file;
    char *response_companion_socket;
    uint64_t response_companion_timeout_ms;
    uid_t response_companion_uid;
    gid_t response_companion_gid;
    int response_companion_uid_set;
    int response_companion_gid_set;
    haproxy_modsecurity_engine *engine;
    msconnector_config common_config;
};

struct haproxy_modsecurity_htx_owned_headers {
    haproxy_modsecurity_header *items;
    char **names;
    char **values;
    unsigned int count;
};

struct haproxy_modsecurity_htx_filter_context {
    haproxy_modsecurity_transaction *transaction;
    struct {
        char transaction_id[128];
        int disabled;
        int fail_closed;
    } lifecycle;
    struct {
        struct haproxy_modsecurity_htx_owned_headers headers;
        char *method;
        char *uri;
        int headers_seen;
        int finished;
        size_t payload_bytes_seen;
        size_t body_limit;
    } request;
    struct {
        int headers_seen;
        int headers_committed;
        int body_started;
        int finished;
        size_t payload_bytes_seen;
        size_t body_limit;
        char handle[HAPROXY_MODSECURITY_HTX_RESPONSE_HANDLE_LENGTH + 1U];
        int handle_present;
    } response;
    struct {
        msconnector_response_companion_client client;
        int mode;
        int terminal;
    } companion;
};

typedef int (*haproxy_modsecurity_htx_append_body_chunk)(
    haproxy_modsecurity_transaction *transaction,
    const unsigned char *body,
    unsigned int body_len,
    haproxy_modsecurity_decision *decision);

static size_t haproxy_modsecurity_htx_bounded_text_size(
    const char *value, size_t maximum)
{
    size_t size = 0U;

    if (value == NULL) {
        return 0U;
    }
    while (size <= maximum && value[size] != '\0') {
        ++size;
    }
    return size;
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
    if (!headers) {
        return;
    }
    for (unsigned int i = 0; i < headers->count; ++i) {
        free(headers->names[i]);
        free(headers->values[i]);
    }
    free(headers->items);
    free(headers->names);
    free(headers->values);
    headers->items = NULL;
    headers->names = NULL;
    headers->values = NULL;
    headers->count = 0U;
}

static void haproxy_modsecurity_htx_request_snapshot_free(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (!ctx) {
        return;
    }
    haproxy_modsecurity_htx_owned_headers_free(&ctx->request.headers);
    free(ctx->request.method);
    free(ctx->request.uri);
    ctx->request.method = NULL;
    ctx->request.uri = NULL;
}

static int haproxy_modsecurity_htx_companion_enabled(
    const struct haproxy_modsecurity_htx_filter_config *config)
{
    return config != NULL && config->response_companion_socket != NULL;
}

static void haproxy_modsecurity_htx_companion_result_reset(
    msconnector_response_companion_result *result)
{
    if (result != NULL) {
        msconnector_response_companion_result_destroy(result);
    }
}

/* Preserve the concrete MRC1/client failure class when the companion API
 * supplied one.  A missing or unrelated error is deliberately reduced to the
 * connector class: HAProxy lifecycle teardown has no evidence for a more
 * specific engine or protocol cause. */
static msconnector_response_companion_cancel_cause
haproxy_modsecurity_htx_companion_cancel_cause_from_error(
    const msconnector_error *error)
{
    if (error == NULL) {
        return MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR;
    }
    switch (error->code) {
    case MSCONNECTOR_ERROR_TIMEOUT:
        return MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_TIMEOUT;
    case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE:
        return MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_UNAVAILABLE;
    case MSCONNECTOR_ERROR_PROTOCOL:
    case MSCONNECTOR_ERROR_PHASE_SEQUENCE:
    case MSCONNECTOR_ERROR_CORRELATION_MISSING:
    case MSCONNECTOR_ERROR_CORRELATION_EXPIRED:
    case MSCONNECTOR_ERROR_CORRELATION_MISMATCH:
        return MSCONNECTOR_RESPONSE_COMPANION_CANCEL_PROTOCOL_ERROR;
    default:
        return MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR;
    }
}

/* Every abnormal HTX lifecycle path closes the private stream after an
 * explicit CANCEL where one is still valid.  `close` remains a final guard for
 * an I/O failure during CANCEL and never retains a transaction handle. */
static void haproxy_modsecurity_htx_companion_cancel_and_close(
    struct haproxy_modsecurity_htx_filter_context *ctx,
    const msconnector_error *error)
{
    msconnector_response_companion_result result;
    msconnector_error cancel_error;

    if (ctx == NULL || !ctx->companion.client.opened) {
        return;
    }
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&cancel_error);
    if (ctx->companion.client.claimed &&
        !ctx->companion.client.response_eos) {
        (void)msconnector_response_companion_client_cancel_with_cause(
            &ctx->companion.client,
            haproxy_modsecurity_htx_companion_cancel_cause_from_error(error),
            &result, &cancel_error);
    }
    haproxy_modsecurity_htx_companion_result_reset(&result);
    msconnector_error_init(&cancel_error);
    (void)msconnector_response_companion_client_close(
        &ctx->companion.client, &cancel_error);
    ctx->companion.terminal = 1;
}

static int haproxy_modsecurity_htx_copy_common_headers(
    const struct haproxy_modsecurity_htx_owned_headers *headers,
    msconnector_header **out)
{
    msconnector_header *items;

    if (headers == NULL || out == NULL) {
        return -1;
    }
    *out = NULL;
    if (headers->count == 0U) {
        return 0;
    }
    items = calloc(headers->count, sizeof(*items));
    if (items == NULL) {
        return -1;
    }
    for (unsigned int index = 0U; index < headers->count; ++index) {
        const char *name = headers->items[index].name;
        const char *value = headers->items[index].value;
        size_t name_size;
        size_t value_size;

        if (name == NULL || value == NULL) {
            free(items);
            return -1;
        }
        name_size = haproxy_modsecurity_htx_bounded_text_size(name,
            HAPROXY_MODSECURITY_HTX_MAX_HEADER_NAME_BYTES);
        value_size = haproxy_modsecurity_htx_bounded_text_size(value,
            HAPROXY_MODSECURITY_HTX_MAX_HEADER_VALUE_BYTES);
        if (name_size == 0U || name_size > HAPROXY_MODSECURITY_HTX_MAX_HEADER_NAME_BYTES ||
            value_size > HAPROXY_MODSECURITY_HTX_MAX_HEADER_VALUE_BYTES) {
            free(items);
            return -1;
        }
        items[index].name = name;
        items[index].name_size = name_size;
        items[index].value = value;
        items[index].value_size = value_size;
    }
    *out = items;
    return 0;
}

/*
 * The SPOP owner publishes only a bounded opaque MRC1 handle.  The HTX side
 * must copy it while the sample is valid and must never treat arbitrary HAProxy
 * variable text as a socket/session identifier.  A missing handle is allowed
 * for the existing native binding path; a malformed published handle is a
 * protocol error and therefore fails the response transaction closed.
 */
static int haproxy_modsecurity_htx_copy_response_handle(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx)
{
    struct sample sample = { 0 };
    const char *value;
    size_t length;

    if (!s || !ctx) {
        return -1;
    }
    ctx->response.handle[0] = '\0';
    ctx->response.handle_present = 0;
    sample.sess = s->sess;
    sample.strm = s;
    sample.opt = SMP_OPT_DIR_REQ | SMP_OPT_FINAL;
    if (!vars_get_by_name("txn.modsec.response_handle",
            sizeof("txn.modsec.response_handle") - 1U, &sample, NULL)) {
        return 0;
    }
    if (sample.data.type != SMP_T_STR || !sample.data.u.str.data ||
        !sample.data.u.str.area) {
        return -1;
    }
    length = sample.data.u.str.data;
    if (length != HAPROXY_MODSECURITY_HTX_RESPONSE_HANDLE_LENGTH) {
        return -1;
    }
    value = sample.data.u.str.area;
    for (size_t index = 0U; index < length; ++index) {
        unsigned char character = (unsigned char)value[index];

        if (!((character >= '0' && character <= '9') ||
              (character >= 'a' && character <= 'f'))) {
            return -1;
        }
    }
    memcpy(ctx->response.handle, value, length);
    ctx->response.handle[length] = '\0';
    ctx->response.handle_present = 1;
    return 0;
}

static int haproxy_modsecurity_htx_set_transaction_id(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (s == NULL || ctx == NULL) {
        return -1;
    }
    /* `uniq_id` is generated by the current HAProxy host stream.  Never
     * replace the canonical transaction identity with an attacker-controlled
     * request header: user-provided correlation data is neither unique nor a
     * valid ownership capability. */
    snprintf(ctx->lifecycle.transaction_id, sizeof(ctx->lifecycle.transaction_id),
        "haproxy-htx-%u", s->uniq_id);
    return 0;
}

static int haproxy_modsecurity_htx_copy_headers(
    const struct htx *htx,
    struct haproxy_modsecurity_htx_owned_headers *headers)
{
    struct htx_blk *blk;
    unsigned int count = 0U;
    size_t total_header_bytes = 0U;

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
            if (count >= HAPROXY_MODSECURITY_HTX_MAX_HEADERS) {
                return -1;
            }
            ++count;
        }
    }
    if (count == 0U) {
        return 0;
    }
    headers->items = calloc(count, sizeof(*headers->items));
    headers->names = calloc(count, sizeof(*headers->names));
    headers->values = calloc(count, sizeof(*headers->values));
    if (!headers->items || !headers->names || !headers->values) {
        haproxy_modsecurity_htx_owned_headers_free(headers);
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
        if (name.len == 0U ||
            name.ptr == NULL || (value.len > 0U && value.ptr == NULL) ||
            name.len > HAPROXY_MODSECURITY_HTX_MAX_HEADER_NAME_BYTES ||
            value.len > HAPROXY_MODSECURITY_HTX_MAX_HEADER_VALUE_BYTES ||
            memchr(name.ptr, '\0', name.len) != NULL ||
            memchr(value.ptr, '\0', value.len) != NULL ||
            name.len > HAPROXY_MODSECURITY_HTX_MAX_TOTAL_HEADER_BYTES -
                total_header_bytes ||
            value.len > HAPROXY_MODSECURITY_HTX_MAX_TOTAL_HEADER_BYTES -
                total_header_bytes - name.len) {
            haproxy_modsecurity_htx_owned_headers_free(headers);
            return -1;
        }
        headers->names[headers->count] =
            haproxy_modsecurity_htx_dup_ist(name,
                HAPROXY_MODSECURITY_HTX_MAX_HEADER_NAME_BYTES);
        headers->values[headers->count] =
            haproxy_modsecurity_htx_dup_ist(value,
                HAPROXY_MODSECURITY_HTX_MAX_HEADER_VALUE_BYTES);
        if (!headers->names[headers->count] || !headers->values[headers->count]) {
            haproxy_modsecurity_htx_owned_headers_free(headers);
            return -1;
        }
        headers->items[headers->count].name = headers->names[headers->count];
        headers->items[headers->count].value = headers->values[headers->count];
        total_header_bytes += name.len + value.len;
        ++headers->count;
    }
    return 0;
}

static void haproxy_modsecurity_htx_report_decision(
    const char *stage, const struct haproxy_modsecurity_htx_filter_context *ctx,
    const haproxy_modsecurity_decision *decision)
{
    if (!decision || !decision->disruptive) {
        return;
    }
    /* Do not include decision->log_message, URI, headers, or body bytes. */
    ha_warning("modsecurity-htx: %s intervention observed; transaction_id=%s phase=%d status=%d rule_id=%d action=%s\n",
        stage, ctx && ctx->lifecycle.transaction_id[0] ? ctx->lifecycle.transaction_id : "unavailable",
        decision->phase, decision->status, decision->rule_id,
        decision->action[0] ? decision->action : "deny");
}

static void haproxy_modsecurity_htx_report_late_decision(
    const struct haproxy_modsecurity_htx_filter_config *config,
    const struct haproxy_modsecurity_htx_filter_context *ctx,
    const haproxy_modsecurity_decision *decision)
{
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action action;
    const char *requested_action;
    const char *resolved_action;
    const char *host_action;
    int strict_mode;

    if (!decision || !decision->disruptive) {
        return;
    }
    strict_mode = config != NULL &&
        config->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT;
    msconnector_late_intervention_policy_init(&policy);
    action = msconnector_late_intervention_resolve(&policy,
        ctx != NULL && ctx->response.headers_committed,
        ctx != NULL && ctx->response.body_started, strict_mode);
    requested_action = decision->action[0] ? decision->action : "deny";
    resolved_action = msconnector_late_intervention_action_name(action);
    /* Safe/minimal deliberately forwards the original response after recording
     * a real log-only downgrade.  Strict requests HAProxy's stream-kill path
     * immediately after this record; wire-level behavior remains separately
     * subject to native host-runtime verification. */
    host_action = action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY
        ? "log_only" : "abort_connection";
    ha_warning("modsecurity-htx: response-body late intervention observed; transaction_id=%s phase=%d status=%d rule_id=%d requested_action=%s resolved_policy_action=%s host_action=%s\n",
        ctx && ctx->lifecycle.transaction_id[0] ? ctx->lifecycle.transaction_id : "unavailable",
        decision->phase, decision->status, decision->rule_id, requested_action,
        resolved_action, host_action);
}

static void haproxy_modsecurity_htx_abort_context(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    if (!ctx) {
        return;
    }
    /* Context teardown is normally an internal/connector failure.  An
     * upstream disconnect is only valid when an explicit host callback has
     * established that observation; this generic abort path has no such
     * evidence and must not manufacture one on the MRC1 wire. */
    haproxy_modsecurity_htx_companion_cancel_and_close(ctx, NULL);
    if (ctx->transaction) {
        haproxy_modsecurity_transaction_abort(ctx->transaction);
        ctx->transaction = NULL;
    }
    haproxy_modsecurity_htx_request_snapshot_free(ctx);
    ctx->lifecycle.disabled = 1;
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

/*
 * A request Phase-1 or response-header Phase-3 deny is still precommit: the
 * current HTX headers have not been forwarded by this filter callback.  Use
 * HAProxy's normal error-reply path so the client receives an actual HTTP
 * reply, rather than returning an error to the generic filter handler after
 * setting txn->status (that path supplies a NULL reply and only truncates the
 * stream).
 *
 * A disruptive decision that cannot be represented by the proven local-reply
 * path must not be reclassified as observer-only.  Latch the filter into its
 * fail-closed error state instead; this preserves the enforcement boundary
 * without claiming an unverified redirect or status mapping.
 * HAProxy's selected API has no supported dynamic redirect/rate-limit reply
 * builder.  Callers therefore use this helper for a validated deny and map
 * every other disruptive precommit decision to the deterministic 503 path;
 * none of them may become an observer-only fail-open.
 */
static int haproxy_modsecurity_htx_apply_precommit_deny(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx,
    const haproxy_modsecurity_decision *decision)
{
    int status;

    if (!s || !s->txn || !ctx || !decision || !decision->disruptive ||
        strcmp(decision->action, "deny") != 0) {
        return 0;
    }
    if (decision->status != 0 &&
        !msconnector_block_status_is_allowed(decision->status)) {
        ha_warning("modsecurity-htx: precommit deny host action not attempted; transaction_id=%s phase=%d status=%d reason=unsupported-block-status\n",
            ctx->lifecycle.transaction_id[0] ? ctx->lifecycle.transaction_id : "unavailable",
            decision->phase, decision->status);
        return 0;
    }
    status = msconnector_block_status_normalize(decision->status);
    if (!msconnector_block_status_is_allowed(status)) {
        return 0;
    }

    /* Disable before the generated local response can revisit this filter. */
    haproxy_modsecurity_htx_finish_context(ctx);
    ctx->lifecycle.disabled = 1;
    s->txn->status = (short)status;
    http_set_term_flags(s);
    http_reply_and_close(s, (short)status, http_error_message(s));
    return 1;
}

/* A Common/body/engine failure is not a Safe/log-only decision.  Before
 * response commitment HAProxy can still deliver a deterministic 503. */
static int haproxy_modsecurity_htx_fail_closed_precommit(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx,
    const char *stage)
{
    haproxy_modsecurity_htx_abort_context(ctx);
    if (!s || !s->txn) {
        return -1;
    }
    ha_warning("modsecurity-htx: fail-closed %s; transaction_id=%s status=503\n",
        stage != NULL ? stage : "phase", ctx != NULL && ctx->lifecycle.transaction_id[0] ?
        ctx->lifecycle.transaction_id : "unavailable");
    s->txn->status = 503;
    http_set_term_flags(s);
    http_reply_and_close(s, 503, http_error_message(s));
    return -1;
}

static void haproxy_modsecurity_htx_apply_precommit_decision_or_fail_closed(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx,
    const haproxy_modsecurity_decision *decision, const char *stage)
{
    if (!haproxy_modsecurity_htx_apply_precommit_deny(s, ctx, decision)) {
        (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx, stage);
    }
}

/* After response commitment a local HTTP error reply is invalid.  Requesting
 * HAProxy's supported stream-kill primitive is the only fail-closed action
 * available to this filter; exact wire-level abort behavior remains a native
 * host-runtime validation item. */
static void haproxy_modsecurity_htx_fail_closed_postcommit(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx,
    const char *stage)
{
    ha_warning("modsecurity-htx: fail-closed postcommit %s; transaction_id=%s\n",
        stage != NULL ? stage : "phase", ctx != NULL && ctx->lifecycle.transaction_id[0] ?
        ctx->lifecycle.transaction_id : "unavailable");
    haproxy_modsecurity_htx_abort_context(ctx);
    if (s != NULL) {
        stream_shutdown(s, SF_ERR_KILLED);
    }
}

/* Request callbacks can be delivered late by a host stream.  Once response
 * headers are committed, generating a new local reply would itself violate
 * the HTTP lifecycle, so the same request-phase failure must terminate the
 * already committed stream instead. */
static void haproxy_modsecurity_htx_fail_closed_request_phase(
    struct stream *s, struct haproxy_modsecurity_htx_filter_context *ctx,
    const char *stage)
{
    if (ctx != NULL && ctx->response.headers_committed) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx, stage);
    } else {
        (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx, stage);
    }
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
    if (haproxy_modsecurity_htx_copy_headers(htx, &ctx->request.headers) != 0) {
        return -1;
    }
    method = htx_sl_req_meth(sl);
    uri = htx_sl_req_uri(sl);
    ctx->request.method = haproxy_modsecurity_htx_dup_ist(method,
        HAPROXY_MODSECURITY_HTX_MAX_METHOD_BYTES);
    ctx->request.uri = haproxy_modsecurity_htx_dup_ist(uri,
        HAPROXY_MODSECURITY_HTX_MAX_URI_BYTES);
    if (!ctx->request.method || !ctx->request.uri) {
        haproxy_modsecurity_htx_request_snapshot_free(ctx);
        return -1;
    }
    return 0;
}

/* Use the active frontend stream's actual socket metadata.  This must not
 * synthesize a loopback address or a nominal port when HAProxy cannot supply
 * a real peer/local endpoint: the Common mapper treats both endpoints as
 * required transaction metadata. */
static int haproxy_modsecurity_htx_capture_request_endpoints(
    struct stream *s, haproxy_modsecurity_request *request,
    char client_address[INET6_ADDRSTRLEN],
    char server_address[INET6_ADDRSTRLEN])
{
    const struct sockaddr_storage *client_endpoint;
    const struct sockaddr_storage *server_endpoint;
    int client_family;
    int server_family;

    if (!s || !s->scf || !request || !client_address || !server_address) {
        return -1;
    }
    client_endpoint = sc_src(s->scf);
    server_endpoint = sc_dst(s->scf);
    if (!client_endpoint || !server_endpoint) {
        return -1;
    }
    client_family = addr_to_str(client_endpoint, client_address,
        INET6_ADDRSTRLEN);
    server_family = addr_to_str(server_endpoint, server_address,
        INET6_ADDRSTRLEN);
    /* addr_to_str preserves HAProxy's supported Internet and UNIX endpoint
     * families.  Reject only conversion failure/unknown families; replacing a
     * valid UNIX endpoint with an invented IP would violate the same
     * invariant. */
    if (client_family <= 0 || server_family <= 0) {
        return -1;
    }

    request->client_ip = client_address;
    request->client_port = get_host_port(client_endpoint);
    request->server_ip = server_address;
    request->server_port = get_host_port(server_endpoint);
    return 0;
}

static int haproxy_modsecurity_htx_begin_request(
    struct stream *s, struct filter *filter)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct haproxy_modsecurity_htx_filter_config *config = FLT_CONF(filter);
    haproxy_modsecurity_request request;
    haproxy_modsecurity_decision decision;
    char client_address[INET6_ADDRSTRLEN];
    char server_address[INET6_ADDRSTRLEN];
    int rc;

    if (!ctx || !config || !config->engine || !ctx->request.method ||
        !ctx->request.uri ||
        haproxy_modsecurity_htx_set_transaction_id(s, ctx) != 0) {
        return -1;
    }
    memset(&request, 0, sizeof(request));
    request.request_id = ctx->lifecycle.transaction_id;
    request.method = ctx->request.method;
    request.uri = ctx->request.uri;
    request.headers = ctx->request.headers.items;
    request.header_count = ctx->request.headers.count;
    if (haproxy_modsecurity_htx_capture_request_endpoints(s, &request,
            client_address, server_address) != 0) {
        return -1;
    }
    rc = haproxy_modsecurity_transaction_begin_request_with_profile(
        config->engine, &request, "haproxy-htx", &decision,
        &ctx->transaction);
    haproxy_modsecurity_htx_request_snapshot_free(ctx);
    if (rc != 0) {
        return -1;
    }
    haproxy_modsecurity_htx_report_decision("request", ctx, &decision);
    if (decision.disruptive) {
        /* P1 is still before the request is committed.  Translate a valid
         * deny through HAProxy's native reply path; every other disruptive
         * common decision has no safe dynamic reply representation here and
         * therefore fails closed rather than being silently downgraded. */
        if (!haproxy_modsecurity_htx_apply_precommit_deny(s, ctx, &decision)) {
            (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                "request disruptive decision");
        }
    }
    return 0;
}

static int haproxy_modsecurity_htx_append_payload(
    struct filter *filter, struct http_msg *msg, unsigned int offset, unsigned int len,
    haproxy_modsecurity_htx_append_body_chunk append_body_chunk,
    size_t *body_bytes_seen, size_t body_limit)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct htx *htx;
    struct htx_blk *blk;
    struct htx_ret found;
    unsigned int remaining = len;

    if (!ctx || !ctx->transaction || !msg || !msg->chn || !append_body_chunk ||
            !body_bytes_seen || body_limit == 0U) {
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
                value.len > body_limit || *body_bytes_seen > body_limit - value.len ||
                append_body_chunk(
                    ctx->transaction, (const unsigned char *)value.ptr,
                    (unsigned int)value.len, &decision) != 0) {
                return -1;
            }
            *body_bytes_seen += value.len;
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

static int haproxy_modsecurity_htx_append_request_payload(
    struct filter *filter, struct http_msg *msg, unsigned int offset, unsigned int len)
{
    return haproxy_modsecurity_htx_append_payload(
        filter, msg, offset, len,
        haproxy_modsecurity_transaction_append_request_body_chunk,
        &((struct haproxy_modsecurity_htx_filter_context *)filter->ctx)->request.payload_bytes_seen,
        ((struct haproxy_modsecurity_htx_filter_context *)filter->ctx)->request.body_limit);
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
    ctx->response.headers_seen = 1;
    haproxy_modsecurity_htx_report_decision("response-header", ctx, &decision);
    if (decision.disruptive) {
        /* P3 remains pre-commit.  Only a validated deny has a native
         * HAProxy response translation; all other disruptive decisions use
         * the deterministic fail-closed reply. */
        if (!haproxy_modsecurity_htx_apply_precommit_deny(s, ctx, &decision)) {
            (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                "response-header disruptive decision");
        }
    }
    return 0;
}

static int haproxy_modsecurity_htx_companion_result_is_forwardable(
    const msconnector_response_companion_result *result)
{
    return result != NULL && result->success &&
        (result->decision == MSCONNECTOR_DECISION_KIND_ALLOW ||
         result->decision == MSCONNECTOR_DECISION_KIND_LOG_ONLY);
}

static int haproxy_modsecurity_htx_companion_record_precommit_outcome(
    struct haproxy_modsecurity_htx_filter_context *ctx,
    msconnector_decision_action action, int visible_status)
{
    msconnector_response_companion_result result;
    msconnector_error error;
    int ok;

    if (ctx == NULL || !ctx->companion.client.claimed) {
        return 0;
    }
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&error);
    ok = msconnector_response_companion_client_outcome(
        &ctx->companion.client, action, visible_status, 0, &result,
        &error);
    haproxy_modsecurity_htx_companion_result_reset(&result);
    haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);
    return ok;
}

static int haproxy_modsecurity_htx_companion_record_terminal_outcome(
    struct haproxy_modsecurity_htx_filter_context *ctx,
    msconnector_decision_action action, int visible_status,
    int connection_aborted, int record_host_action)
{
    msconnector_response_companion_result result;
    msconnector_error error;
    int ok;

    if (ctx == NULL || !ctx->companion.client.claimed ||
        !ctx->companion.client.response_eos) {
        return 0;
    }
    /* OUTCOME records an actual host translation of a disruptive decision.
     * Allow and ordinary log-only results have no host action; emitting an
     * OUTCOME for them is rejected by the Runtime, so their normal terminal
     * sequence is EOS -> RELEASE. */
    ok = 1;
    if (record_host_action) {
        memset(&result, 0, sizeof(result));
        msconnector_error_init(&error);
        ok = msconnector_response_companion_client_outcome(
            &ctx->companion.client, action, visible_status,
            connection_aborted, &result, &error);
        haproxy_modsecurity_htx_companion_result_reset(&result);
    }
    if (ok) {
        memset(&result, 0, sizeof(result));
        msconnector_error_init(&error);
        ok = msconnector_response_companion_client_release(
            &ctx->companion.client, &result, &error);
        haproxy_modsecurity_htx_companion_result_reset(&result);
    }
    if (!ok) {
        haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);
        return 0;
    }
    msconnector_error_init(&error);
    (void)msconnector_response_companion_client_close(
        &ctx->companion.client, &error);
    ctx->companion.terminal = 1;
    return 1;
}

static int haproxy_modsecurity_htx_companion_open_and_claim(
    struct stream *s, const struct haproxy_modsecurity_htx_filter_config *config,
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    msconnector_response_companion_result result;
    msconnector_error error;
    int ok;

    if (s == NULL || config == NULL || ctx == NULL ||
        !haproxy_modsecurity_htx_companion_enabled(config) ||
        haproxy_modsecurity_htx_copy_response_handle(s, ctx) != 0 ||
        !ctx->response.handle_present) {
        return 0;
    }
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&error);
    ok = msconnector_response_companion_client_open(&ctx->companion.client,
        config->response_companion_socket,
        config->response_companion_timeout_ms, config->response_companion_uid,
        config->response_companion_gid, &error);
    if (ok) {
        ok = msconnector_response_companion_client_claim(
            &ctx->companion.client, ctx->response.handle, &result,
            &error);
    }
    haproxy_modsecurity_htx_companion_result_reset(&result);
    if (!ok) {
        haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);
    }
    return ok;
}

static int haproxy_modsecurity_htx_companion_commit(
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    msconnector_response_companion_result result;
    msconnector_error error;
    int ok;

    if (ctx == NULL || !ctx->companion.client.claimed) {
        return 0;
    }
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&error);
    ok = msconnector_response_companion_client_commit(
        &ctx->companion.client, 1, 0, &result, &error) &&
        haproxy_modsecurity_htx_companion_result_is_forwardable(&result);
    haproxy_modsecurity_htx_companion_result_reset(&result);
    if (!ok) {
        haproxy_modsecurity_htx_companion_cancel_and_close(ctx, &error);
    }
    return ok;
}

static int haproxy_modsecurity_htx_process_companion_response_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    const struct haproxy_modsecurity_htx_filter_config *config = FLT_CONF(filter);
    struct haproxy_modsecurity_htx_owned_headers headers;
    msconnector_header *common_headers = NULL;
    struct htx *htx;
    struct htx_sl *sl;
    struct ist protocol;
    char *protocol_copy = NULL;
    msconnector_response response;
    msconnector_response_companion_result result;
    msconnector_error error;
    haproxy_modsecurity_decision host_decision;
    int status;
    int ok;

    if (ctx == NULL || config == NULL || msg == NULL || msg->chn == NULL ||
        !ctx->companion.mode || !ctx->request.finished ||
        !haproxy_modsecurity_htx_companion_open_and_claim(s, config, ctx)) {
        return haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
            "response-companion claim");
    }
    htx = htxbuf(&msg->chn->buf);
    sl = http_get_stline(htx);
    memset(&headers, 0, sizeof(headers));
    if (sl == NULL || haproxy_modsecurity_htx_copy_headers(htx, &headers) != 0 ||
        haproxy_modsecurity_htx_copy_common_headers(&headers, &common_headers) != 0) {
        haproxy_modsecurity_htx_owned_headers_free(&headers);
        free(common_headers);
        return haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
            "response-companion response headers");
    }
    protocol = htx_sl_res_vsn(sl);
    protocol_copy = haproxy_modsecurity_htx_dup_ist(protocol,
        HAPROXY_MODSECURITY_HTX_MAX_PROTOCOL_BYTES);
    if (protocol_copy == NULL) {
        haproxy_modsecurity_htx_owned_headers_free(&headers);
        free(common_headers);
        return haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
            "response-companion response version");
    }
    memset(&response, 0, sizeof(response));
    response.status = s != NULL && s->txn != NULL && s->txn->status > 0 ?
        s->txn->status : 200;
    response.http_version = protocol_copy;
    response.headers = common_headers;
    response.header_count = headers.count;
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&error);
    ok = msconnector_response_companion_client_response_headers(
        &ctx->companion.client, &response, &result, &error);
    free(protocol_copy);
    haproxy_modsecurity_htx_owned_headers_free(&headers);
    free(common_headers);
    if (!ok) {
        haproxy_modsecurity_htx_companion_result_reset(&result);
        return haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
            "response-companion phase-3");
    }
    ctx->response.headers_seen = 1;
    if (haproxy_modsecurity_htx_companion_result_is_forwardable(&result)) {
        haproxy_modsecurity_htx_companion_result_reset(&result);
        return 0;
    }

    /* HAProxy's selected HTX API has a concrete deny reply, but no supported
     * dynamic redirect reply builder.  Preserve a deny status where valid and
     * otherwise fail closed with 503 rather than forwarding a disruptive P3. */
    status = result.decision == MSCONNECTOR_DECISION_KIND_DENY &&
        msconnector_block_status_is_allowed((int)result.status) ?
        (int)result.status : 503;
    (void)haproxy_modsecurity_htx_companion_record_precommit_outcome(ctx,
        MSCONNECTOR_DECISION_ACTION_DENY, status);
    haproxy_modsecurity_htx_companion_result_reset(&result);
    memset(&host_decision, 0, sizeof(host_decision));
    host_decision.disruptive = 1;
    host_decision.phase = 3;
    host_decision.status = status;
    snprintf(host_decision.action, sizeof(host_decision.action), "%s", "deny");
    if (haproxy_modsecurity_htx_apply_precommit_deny(s, ctx, &host_decision)) {
        return 1;
    }
    return haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
        "response-companion disruptive phase-3");
}

static int haproxy_modsecurity_htx_send_companion_response_chunk(
    struct haproxy_modsecurity_htx_filter_context *ctx,
    const char *data, size_t data_size)
{
    while (data_size != 0U) {
        msconnector_response_companion_result result;
        msconnector_error error;
        size_t chunk_size = data_size;

        if (chunk_size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK) {
            chunk_size = MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK;
        }
        memset(&result, 0, sizeof(result));
        msconnector_error_init(&error);
        if (!msconnector_response_companion_client_body_chunk(
                &ctx->companion.client,
                (const unsigned char *)data, chunk_size, &result, &error) ||
            !haproxy_modsecurity_htx_companion_result_is_forwardable(&result)) {
            haproxy_modsecurity_htx_companion_result_reset(&result);
            return -1;
        }
        haproxy_modsecurity_htx_companion_result_reset(&result);
        data += chunk_size;
        data_size -= chunk_size;
    }
    return 0;
}

static int haproxy_modsecurity_htx_append_companion_response_block(
    struct haproxy_modsecurity_htx_filter_context *ctx,
    struct htx *htx, struct htx_blk *blk, unsigned int *offset,
    unsigned int *remaining)
{
    enum htx_blk_type type = htx_get_blk_type(blk);
    uint32_t block_size = htx_get_blksz(blk);

    if (type == HTX_BLK_UNUSED) {
        return 0;
    }
    if (type == HTX_BLK_DATA) {
        struct ist value = htx_get_blk_value(htx, blk);
        size_t data_size;

        if (*offset > value.len) {
            return -1;
        }
        value = istadv(value, *offset);
        if (value.len > *remaining) {
            value = isttrim(value, *remaining);
        }
        data_size = value.len;
        if (haproxy_modsecurity_htx_send_companion_response_chunk(ctx,
                value.ptr, value.len) != 0) {
            return -1;
        }
        *remaining -= (unsigned int)data_size;
    } else {
        if (*offset != 0U || block_size > *remaining) {
            return -1;
        }
        *remaining -= block_size;
    }
    *offset = 0U;
    return 0;
}

static int haproxy_modsecurity_htx_append_companion_response_payload(
    struct filter *filter, struct http_msg *msg, unsigned int offset,
    unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;
    struct htx *htx;
    struct htx_blk *blk;
    struct htx_ret found;
    unsigned int remaining = len;

    if (ctx == NULL || !ctx->companion.client.claimed || msg == NULL ||
        msg->chn == NULL) {
        return -1;
    }
    htx = htxbuf(&msg->chn->buf);
    found = htx_find_offset(htx, offset);
    blk = found.blk;
    offset = found.ret;
    while (blk != NULL && remaining != 0U) {
        if (haproxy_modsecurity_htx_append_companion_response_block(ctx, htx,
                blk, &offset, &remaining) != 0) {
            return -1;
        }
        blk = htx_get_next_blk(htx, blk);
    }
    return remaining == 0U ? 0 : -1;
}

static int haproxy_modsecurity_htx_append_response_payload(
    struct filter *filter, struct http_msg *msg, unsigned int offset, unsigned int len)
{
    return haproxy_modsecurity_htx_append_payload(
        filter, msg, offset, len,
        haproxy_modsecurity_transaction_append_response_body_chunk,
        &((struct haproxy_modsecurity_htx_filter_context *)filter->ctx)->response.payload_bytes_seen,
        ((struct haproxy_modsecurity_htx_filter_context *)filter->ctx)->response.body_limit);
}

static int haproxy_modsecurity_htx_finish_companion_response(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    const struct haproxy_modsecurity_htx_filter_config *config = FLT_CONF(filter);
    msconnector_response_companion_result result;
    msconnector_error error;
    msconnector_decision_action actual_action;
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action late_action;
    int visible_status;
    int connection_aborted = 0;
    int record_host_action = 0;
    int strict_mode;

    if (ctx->lifecycle.disabled) {
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    if (ctx->response.finished) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "duplicate response-companion body eos");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    if (!ctx->response.headers_seen ||
        !ctx->companion.client.claimed) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "response-companion body eos without response phase");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    ctx->response.finished = 1;
    memset(&result, 0, sizeof(result));
    msconnector_error_init(&error);
    if (!msconnector_response_companion_client_body_eos(
            &ctx->companion.client, &result, &error)) {
        haproxy_modsecurity_htx_companion_result_reset(&result);
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "response-companion phase-4 eos");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    visible_status = s != NULL && s->txn != NULL && s->txn->status > 0 ?
        s->txn->status : 200;
    if (haproxy_modsecurity_htx_companion_result_is_forwardable(&result)) {
        actual_action = result.decision == MSCONNECTOR_DECISION_KIND_LOG_ONLY ?
            MSCONNECTOR_DECISION_ACTION_LOG_ONLY :
            MSCONNECTOR_DECISION_ACTION_ALLOW;
    } else if (result.decision == MSCONNECTOR_DECISION_KIND_ERROR ||
        result.decision == MSCONNECTOR_DECISION_KIND_UNSUPPORTED) {
        actual_action = MSCONNECTOR_DECISION_ACTION_ERROR;
        connection_aborted = 1;
        record_host_action = 1;
    } else {
        strict_mode = config != NULL && config->common_config.phase4_mode ==
            MSCONNECTOR_PHASE4_MODE_STRICT;
        msconnector_late_intervention_policy_init(&policy);
        late_action = msconnector_late_intervention_resolve(&policy, 1, 1,
            strict_mode);
        actual_action = late_action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY ?
            MSCONNECTOR_DECISION_ACTION_LOG_ONLY :
            MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
        connection_aborted = actual_action ==
            MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
        record_host_action = 1;
        ha_warning("modsecurity-htx: response-companion phase-4 intervention; transaction_id=%s rule_id=%s requested=%s host_action=%s\n",
            ctx->lifecycle.transaction_id[0] ? ctx->lifecycle.transaction_id : "unavailable",
            result.rule_id != NULL ? result.rule_id : "unavailable",
            msconnector_decision_kind_name(result.decision),
            msconnector_decision_action_name(actual_action));
    }
    haproxy_modsecurity_htx_companion_result_reset(&result);
    if (!haproxy_modsecurity_htx_companion_record_terminal_outcome(ctx,
            actual_action, visible_status, connection_aborted,
            record_host_action)) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "response-companion terminal cleanup");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    if (connection_aborted) {
        /* The stream-kill request is intentionally the only strict postcommit
         * host action.  Its exact client-visible behavior needs native
         * HAProxy runtime evidence before it can be promoted as enforcement. */
        ctx->lifecycle.disabled = 1;
        stream_shutdown(s, SF_ERR_KILLED);
    }
    unregister_data_filter(s, msg->chn, filter);
    return 1;
}

static int haproxy_modsecurity_htx_filter_init(struct proxy *px, struct flt_conf *fconf)
{
    struct haproxy_modsecurity_htx_filter_config *config = fconf->conf;
    haproxy_modsecurity_engine_config engine_config;
    haproxy_modsecurity_decision decision;

    (void)px;
    if (!config) {
        ha_alert("modsecurity-htx: filter configuration is required\n");
        return -1;
    }
    if (haproxy_modsecurity_htx_companion_enabled(config)) {
        fconf->flags |= FLT_CFG_FL_HTX;
        return 0;
    }
    if (!config->rules_file || config->rules_file[0] == '\0') {
        ha_alert("modsecurity-htx: rules-file is required without response-companion-socket\n");
        return -1;
    }
    memset(&engine_config, 0, sizeof(engine_config));
    engine_config.connector_info = "HAProxy native HTX streaming overlay";
    engine_config.common_config = config->common_config;
    engine_config.rules_file = config->rules_file;
    if (haproxy_modsecurity_engine_create(&engine_config, &config->engine, &decision) != 0) {
        ha_alert("modsecurity-htx: failed to initialize the ModSecurity engine\n");
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
    if (config->engine != NULL) {
        haproxy_modsecurity_engine_destroy(config->engine);
    }
    free(config->rules_file);
    free(config->response_companion_socket);
    free(config);
    fconf->conf = NULL;
}

static int haproxy_modsecurity_htx_filter_attach(struct stream *s, struct filter *filter)
{
    struct haproxy_modsecurity_htx_filter_context *ctx;
    struct haproxy_modsecurity_htx_filter_config *config;

    (void)s;
    config = FLT_CONF(filter);
    ctx = calloc(1U, sizeof(*ctx));
    if (!ctx || !config) {
        free(ctx);
        return -1;
    }
    ctx->request.body_limit = config->common_config.request_body_limit;
    ctx->response.body_limit = config->common_config.response_body_limit;
    ctx->companion.mode =
        haproxy_modsecurity_htx_companion_enabled(config);
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

static int haproxy_modsecurity_htx_handle_response_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

        if (ctx->companion.mode) {
            if (ctx->lifecycle.disabled || !ctx->request.finished ||
                haproxy_modsecurity_htx_process_companion_response_headers(
                    s, filter, msg) != 0) {
                /* The companion helper has either generated the only valid
                 * precommit host reply or has already made cleanup terminal. */
                return 1;
            }
            if (!haproxy_modsecurity_htx_companion_commit(ctx)) {
                (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                    "response-companion commit");
                return 1;
            }
            ctx->response.headers_committed = 1;
            register_data_filter(s, msg->chn, filter);
            return 1;
        }
        if (ctx->lifecycle.disabled) {
            haproxy_modsecurity_htx_abort_context(ctx);
        } else if (!ctx->transaction) {
            /* P3 without a live P1/P2 transaction is never a valid direct
             * HTX transition.  A previously terminal local reply is handled
             * above; every other case receives the deterministic 503 path. */
            (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                "response headers without request transaction");
        } else if (haproxy_modsecurity_htx_process_response_headers(s, filter, msg) != 0) {
            /* P3 before request EOS is an invalid canonical transition.  The
             * binding performs the Common phase validation and reports the
             * protocol/phase error; abort the transaction so the response is
             * never silently passed or detached from P1/P2. */
            (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                "response headers");
        } else if (!ctx->lifecycle.disabled) {
            /* The following return lets HAProxy forward the headers.  By the
             * later body EOS they are necessarily committed. */
            ctx->response.headers_committed = 1;
            register_data_filter(s, msg->chn, filter);
        }
    return 1;
}

static int haproxy_modsecurity_htx_handle_request_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (ctx->request.headers_seen) {
        /* P1 is a single logical phase even when HAProxy reuses the stream or
         * retries a message.  Do not overwrite a live header snapshot or
         * create a second direct transaction for the same filter context. */
        haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
            "duplicate request headers");
        return 1;
    }
    ctx->request.headers_seen = 1;
    if (ctx->companion.mode) {
        /* SPOP owns P1/P2 in companion mode.  Creating a local binding here
         * would split one logical transaction across two engines. */
        if (haproxy_modsecurity_htx_set_transaction_id(s, ctx) != 0) {
            haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
                "request transaction identity");
        } else if (!ctx->lifecycle.disabled) {
            /* Companion mode still needs the native HTX data-filter hooks to
             * observe the request payload boundary and exactly one local
             * request EOS.  It does not invoke a second engine; it only
             * establishes the P2 ordering precondition for the MRC1 P3/P4
             * claim. */
            register_data_filter(s, msg->chn, filter);
        }
        return 1;
    }
    if (haproxy_modsecurity_htx_capture_request_headers(filter, msg) != 0 ||
        haproxy_modsecurity_htx_begin_request(s, filter) != 0) {
        haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
            "request headers");
    } else if (!ctx->lifecycle.disabled) {
        register_data_filter(s, msg->chn, filter);
    }
    return 1;
}

static int haproxy_modsecurity_htx_filter_http_headers(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (ctx->lifecycle.fail_closed) {
        haproxy_modsecurity_htx_abort_context(ctx);
        return -1;
    }
    if (msg->chn->flags & CF_ISRESP) {
        return haproxy_modsecurity_htx_handle_response_headers(s, filter, msg);
    }
    return haproxy_modsecurity_htx_handle_request_headers(s, filter, msg);
}

static int haproxy_modsecurity_htx_filter_request_payload(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    unsigned int offset, unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (ctx->companion.mode) {
        if (!ctx->lifecycle.disabled &&
            (!ctx->request.headers_seen || ctx->request.finished)) {
            ctx->lifecycle.fail_closed = 1;
            haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
                "response-companion request payload outside active request phase");
            return -1;
        }
        return (int)len;
    }
    if (ctx->lifecycle.disabled) {
        return (int)len;
    }
    if (!ctx->transaction ||
        haproxy_modsecurity_htx_append_request_payload(filter, msg, offset, len) != 0) {
        ctx->lifecycle.fail_closed = 1;
        haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx, "request body");
        /* The borrowed HTX slice that failed validation must not be forwarded
         * as if it had been inspected successfully. */
        return -1;
    }
    return (int)len;
}

static int haproxy_modsecurity_htx_filter_response_payload(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    unsigned int offset, unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (ctx->companion.mode) {
        if (ctx->lifecycle.disabled) {
            return -1;
        }
        if (!ctx->response.headers_seen ||
            haproxy_modsecurity_htx_append_companion_response_payload(
                filter, msg, offset, len) != 0) {
            haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
                "response-companion body");
            return -1;
        }
    } else {
        if (ctx->lifecycle.disabled) {
            return -1;
        }
        if (!ctx->transaction || !ctx->response.headers_seen ||
            haproxy_modsecurity_htx_append_response_payload(filter, msg, offset, len) != 0) {
            haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx, "response body");
            return -1;
        }
    }
    ctx->response.headers_committed = 1;
    ctx->response.body_started = 1;
    return (int)len;
}

static int haproxy_modsecurity_htx_filter_http_payload(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    unsigned int offset, unsigned int len)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (!(msg->chn->flags & CF_ISRESP)) {
        return haproxy_modsecurity_htx_filter_request_payload(
            s, filter, msg, offset, len);
    }
    return haproxy_modsecurity_htx_filter_response_payload(
        s, filter, msg, offset, len);
}

static int haproxy_modsecurity_htx_finish_request(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    haproxy_modsecurity_decision decision;

    unregister_data_filter(s, msg->chn, filter);
    if (ctx->request.finished) {
        if (!ctx->lifecycle.disabled) {
            haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
                "duplicate request body eos");
        }
        return 1;
    }
    ctx->request.finished = 1;
    if (ctx->companion.mode) {
        /* The SPOP owner has already evaluated and handed off P1/P2.  This
         * local EOS only establishes the HTX-side ordering precondition for
         * CLAIM/P3; it must not synthesize a second engine phase. */
        if (!ctx->request.headers_seen) {
            haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
                "response-companion request body eos without request phase");
        }
        return 1;
    }
    if (ctx->lifecycle.disabled) {
        return 1;
    }
    if (!ctx->request.headers_seen || !ctx->transaction) {
        haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
            "request body eos without request phase");
        return 1;
    }
    if (haproxy_modsecurity_transaction_finish_request_body(
            ctx->transaction, &decision) != 0) {
        haproxy_modsecurity_htx_fail_closed_request_phase(s, ctx,
            "request body eos");
        return 1;
    }
    haproxy_modsecurity_htx_report_decision("request-body", ctx, &decision);
    if (decision.disruptive) {
        /* P2 can be reached after HAProxy has borrowed a current DATA slice,
         * but before P3 it still has a valid local reply path.  Scheduler
         * timing yields zero-or-one dispatch observations; it is not
         * incremental-request-forwarding evidence.  Once P3 has started, a
         * body decision cannot be converted into a fabricated HTTP reply and
         * must instead terminate the stream. */
        if (!ctx->response.headers_seen) {
            if (!haproxy_modsecurity_htx_apply_precommit_deny(s, ctx,
                    &decision)) {
                (void)haproxy_modsecurity_htx_fail_closed_precommit(s, ctx,
                    "request-body disruptive decision");
            }
        } else {
            haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
                "request-body disruptive decision after response phase");
        }
        return 1;
    }
    return 1;
}

static int haproxy_modsecurity_htx_finish_response(
    struct stream *s, struct filter *filter, struct http_msg *msg,
    struct haproxy_modsecurity_htx_filter_context *ctx)
{
    haproxy_modsecurity_decision decision;
    const struct haproxy_modsecurity_htx_filter_config *config = FLT_CONF(filter);
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action late_action;

    if (ctx->companion.mode) {
        return haproxy_modsecurity_htx_finish_companion_response(s, filter,
            msg, ctx);
    }
    if (ctx->lifecycle.disabled) {
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    if (ctx->response.finished) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "duplicate response body eos");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    if (!ctx->transaction || !ctx->response.headers_seen) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "response body eos without response phase");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    /* HTX http_end is the only Phase-4 evaluation point and is idempotently
     * guarded so the binding's finish primitive is called exactly once. */
    ctx->response.finished = 1;
    if (haproxy_modsecurity_transaction_finish_response_body(ctx->transaction,
            &decision) != 0) {
        haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
            "response body eos");
        unregister_data_filter(s, msg->chn, filter);
        return 1;
    }
    haproxy_modsecurity_htx_report_late_decision(config, ctx, &decision);
    if (decision.disruptive) {
        msconnector_late_intervention_policy_init(&policy);
        late_action = msconnector_late_intervention_resolve(&policy, 1, 1,
            config != NULL && config->common_config.phase4_mode ==
                MSCONNECTOR_PHASE4_MODE_STRICT);
        if (late_action != MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY) {
            /* Strict P4 is enforcement, not a log-only request.  This uses
             * HAProxy's supported postcommit stream-kill primitive; the exact
             * client-visible wire result is an explicit native-runtime test
             * obligation rather than a reason to forward the response. */
            haproxy_modsecurity_htx_fail_closed_postcommit(s, ctx,
                "response body strict intervention");
            unregister_data_filter(s, msg->chn, filter);
            return 1;
        }
    }
    /* Safe P4 resolves only to log-only; after that normal terminal cleanup
     * is allowed to complete without a disruptive host action. */
    haproxy_modsecurity_htx_finish_context(ctx);
    unregister_data_filter(s, msg->chn, filter);
    return 1;
}

static int haproxy_modsecurity_htx_filter_http_end(
    struct stream *s, struct filter *filter, struct http_msg *msg)
{
    struct haproxy_modsecurity_htx_filter_context *ctx = filter->ctx;

    if (!ctx || !msg || !msg->chn) {
        return -1;
    }
    if (!(msg->chn->flags & CF_ISRESP)) {
        return haproxy_modsecurity_htx_finish_request(s, filter, msg, ctx);
    }
    return haproxy_modsecurity_htx_finish_response(s, filter, msg, ctx);
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

static int haproxy_modsecurity_htx_parse_u64(
    const char *value, uint64_t minimum, uint64_t maximum, uint64_t *out)
{
    char *end = NULL;
    unsigned long long parsed;

    if (value == NULL || value[0] == '\0' || out == NULL) {
        return 0;
    }
    errno = 0;
    parsed = strtoull(value, &end, 10);
    if (errno != 0 || end == value || *end != '\0' ||
        parsed < minimum || parsed > maximum) {
        return 0;
    }
    *out = (uint64_t)parsed;
    return 1;
}

static int haproxy_modsecurity_htx_private_socket_path_character_is_safe(
    const char *value, size_t index, size_t length)
{
    unsigned char character = (unsigned char)value[index];

    if (character < 32U || character == 127U) {
        return 0;
    }
    return character != '/' || index + 2U >= length ||
        value[index + 1U] != '.' || value[index + 2U] != '.' ||
        (index + 3U != length && value[index + 3U] != '/');
}

static int haproxy_modsecurity_htx_private_socket_path_is_valid(
    const char *value)
{
    size_t length;

    if (value == NULL || value[0] != '/') {
        return 0;
    }
    length = haproxy_modsecurity_htx_bounded_text_size(value,
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE - 1U);
    if (length == 0U || length >=
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE) {
        return 0;
    }
    for (size_t index = 0U; index < length; ++index) {
        if (!haproxy_modsecurity_htx_private_socket_path_character_is_safe(
                value, index, length)) {
            return 0;
        }
    }
    return 1;
}

static void haproxy_modsecurity_htx_filter_config_destroy(
    struct haproxy_modsecurity_htx_filter_config *config)
{
    if (config == NULL) {
        return;
    }
    free(config->rules_file);
    free(config->response_companion_socket);
    free(config);
}

enum haproxy_modsecurity_htx_parse_result {
    HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED = 0,
    HAPROXY_MODSECURITY_HTX_PARSE_HANDLED,
    HAPROXY_MODSECURITY_HTX_PARSE_ERROR
};

static int parse_owned_path_option(
    struct haproxy_modsecurity_htx_filter_config *config,
    char **args, int pos, char **err, int cur_arg, int socket_option)
{
    char **target;
    const char *name = socket_option ? "response-companion-socket" : "rules-file";

    if (strcmp(args[pos], name) != 0) {
        return HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED;
    }
    target = socket_option ? &config->response_companion_socket : &config->rules_file;
    if (args[pos + 1] == NULL || args[pos + 1][0] == '\0' || *target != NULL ||
            (socket_option && config->rules_file != NULL) ||
            (!socket_option && config->response_companion_socket != NULL) ||
            (socket_option && !haproxy_modsecurity_htx_private_socket_path_is_valid(args[pos + 1]))) {
        memprintf(err, "'%s' has an invalid or duplicate value", args[cur_arg]);
        return HAPROXY_MODSECURITY_HTX_PARSE_ERROR;
    }
    *target = strdup(args[pos + 1]);
    if (*target == NULL) {
        memprintf(err, "%s: out of memory", args[cur_arg]);
        return HAPROXY_MODSECURITY_HTX_PARSE_ERROR;
    }
    return HAPROXY_MODSECURITY_HTX_PARSE_HANDLED;
}

static int parse_timeout_option(
    struct haproxy_modsecurity_htx_filter_config *config,
    char **args, int pos, char **err, int cur_arg, int *timeout_set)
{
    if (strcmp(args[pos], "response-companion-timeout-ms") != 0) {
        return HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED;
    }
    if (args[pos + 1] == NULL || *timeout_set ||
            !haproxy_modsecurity_htx_parse_u64(args[pos + 1], 1U, UINT64_MAX,
                &config->response_companion_timeout_ms)) {
        memprintf(err, "'%s' requires a valid response-companion-timeout-ms", args[cur_arg]);
        return HAPROXY_MODSECURITY_HTX_PARSE_ERROR;
    }
    *timeout_set = 1;
    return HAPROXY_MODSECURITY_HTX_PARSE_HANDLED;
}

static uint64_t haproxy_modsecurity_htx_uid_maximum(void)
{
    return (uint64_t)(uid_t)-1;
}

static uint64_t haproxy_modsecurity_htx_gid_maximum(void)
{
    return (uint64_t)(gid_t)-1;
}

static uint64_t haproxy_modsecurity_htx_identity_maximum(int uid_option)
{
    if (uid_option) {
        return haproxy_modsecurity_htx_uid_maximum();
    }
    return haproxy_modsecurity_htx_gid_maximum();
}

static int parse_identity_option(
    struct haproxy_modsecurity_htx_filter_config *config,
    char **args, int pos, char **err, int cur_arg, int uid_option)
{
    const char *name = uid_option ? "response-companion-uid" : "response-companion-gid";
    int *seen = uid_option ? &config->response_companion_uid_set : &config->response_companion_gid_set;
    uint64_t parsed;
    uint64_t maximum;

    /* Keep the platform-specific limits explicit while selecting them
     * without duplicating the option-processing control flow. */
    maximum = haproxy_modsecurity_htx_identity_maximum(uid_option);

    if (strcmp(args[pos], name) != 0) {
        return HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED;
    }
    if (args[pos + 1] == NULL || *seen ||
            !haproxy_modsecurity_htx_parse_u64(args[pos + 1], 0U, maximum, &parsed)) {
        memprintf(err, "'%s' requires a valid %s", args[cur_arg], name);
        return HAPROXY_MODSECURITY_HTX_PARSE_ERROR;
    }
    if (uid_option) {
        config->response_companion_uid = (uid_t)parsed;
    } else {
        config->response_companion_gid = (gid_t)parsed;
    }
    *seen = 1;
    return HAPROXY_MODSECURITY_HTX_PARSE_HANDLED;
}

static int parse_phase4_option(
    struct haproxy_modsecurity_htx_filter_config *config,
    char **args, int pos)
{
    if (strcmp(args[pos], "phase4-mode") != 0 || args[pos + 1] == NULL ||
            !msconnector_parse_phase4_mode(args[pos + 1],
                &config->common_config.phase4_mode)) {
        return HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED;
    }
    return HAPROXY_MODSECURITY_HTX_PARSE_HANDLED;
}

static int haproxy_modsecurity_htx_filter_parse(
    char **args, int *cur_arg, struct proxy *px, struct flt_conf *fconf,
    char **err, void *private)
{
    struct haproxy_modsecurity_htx_filter_config *config;
    int pos;
    int timeout_set = 0;

    (void)px;
    (void)private;
    config = calloc(1U, sizeof(*config));
    if (!config) {
        memprintf(err, "%s: out of memory", args[*cur_arg]);
        return -1;
    }
    msconnector_config_init(&config->common_config);
    msconnector_config_apply_defaults(&config->common_config);
    pos = *cur_arg + 1;
    while (args[pos] != NULL && args[pos][0] != '\0') {
        int handled = parse_owned_path_option(config, args, pos, err, *cur_arg, 0);
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            handled = parse_owned_path_option(config, args, pos, err, *cur_arg, 1);
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            handled = parse_timeout_option(config, args, pos, err, *cur_arg, &timeout_set);
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            handled = parse_identity_option(config, args, pos, err, *cur_arg, 1);
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            handled = parse_identity_option(config, args, pos, err, *cur_arg, 0);
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            handled = parse_phase4_option(config, args, pos);
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_ERROR) {
            haproxy_modsecurity_htx_filter_config_destroy(config);
            return -1;
        }
        if (handled == HAPROXY_MODSECURITY_HTX_PARSE_UNHANDLED) {
            memprintf(err, "'%s' requires either 'rules-file <path>' or private 'response-companion-socket <absolute-path> response-companion-timeout-ms <ms> response-companion-uid <uid> response-companion-gid <gid>'", args[*cur_arg]);
            haproxy_modsecurity_htx_filter_config_destroy(config);
            return -1;
        }
        pos += 2;
    }
    if (config->response_companion_socket != NULL &&
        (!timeout_set || !config->response_companion_uid_set ||
         !config->response_companion_gid_set)) {
        memprintf(err, "'%s' response companion requires timeout, uid, and gid", args[*cur_arg]);
        haproxy_modsecurity_htx_filter_config_destroy(config);
        return -1;
    }
    if (config->rules_file == NULL && config->response_companion_socket == NULL) {
        memprintf(err, "'%s' requires rules-file or response-companion-socket", args[*cur_arg]);
        haproxy_modsecurity_htx_filter_config_destroy(config);
        return -1;
    }
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
