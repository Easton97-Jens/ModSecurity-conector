#include "first.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "array.h"
#include "base.h"
#include "buffer.h"
#include "fdevent.h"
#include "http_status.h"
#include "log.h"
#include "plugin.h"
#include "request.h"

#include "common/runtime/msconnector_runtime.h"
#include "connectors/lighttpd/src/lighttpd_modsecurity_mapper.h"

typedef struct {
    int enabled;
    const buffer *config_file;
} plugin_config;

typedef struct {
    PLUGIN_DATA;
    plugin_config defaults;
    msconnector_runtime *runtime;
    size_t request_body_limit;
    size_t response_body_limit;
    size_t total_header_limit;
    size_t header_count_limit;
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    int request_body_hooks_enabled;
#endif
} plugin_data;

typedef struct {
    msconnector_runtime_transaction *transaction;
    lighttpd_modsecurity_map_storage request_storage;
    lighttpd_modsecurity_map_storage response_storage;
    msconnector_request request;
    msconnector_response response;
    char host_request_id[96];
    int response_processed;
    int request_body_finished;
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    off_t request_body_next_offset;
#endif
} handler_ctx;

INIT_FUNC(mod_msconnector_init);
FREE_FUNC(mod_msconnector_free);
SETDEFAULTS_FUNC(mod_msconnector_set_defaults);
REQUEST_FUNC(mod_msconnector_handle_uri_clean);
REQUEST_FUNC(mod_msconnector_handle_response_start);
REQUEST_FUNC(mod_msconnector_handle_request_reset);
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
static handler_t mod_msconnector_handle_request_body(
    request_st *r,
    const chunkqueue *queue,
    off_t queue_offset,
    off_t length,
    off_t stream_offset,
    int eos,
    void *p_d);
static plugin_body_hook_result mod_msconnector_handle_response_body(
    request_st *r,
    const chunkqueue *queue,
    off_t queue_offset,
    off_t length,
    off_t stream_offset,
    int eos,
    void *p_d);
#endif

static const plugin mod_msconnector_plugin = {
  .name                         = "msconnector",
  .version                      = LIGHTTPD_VERSION_ID,
  .init                         = mod_msconnector_init,
  .cleanup                      = mod_msconnector_free,
  .set_defaults                 = mod_msconnector_set_defaults,
  .handle_uri_clean             = mod_msconnector_handle_uri_clean,
  .handle_response_start        = mod_msconnector_handle_response_start,
  .handle_request_reset         = mod_msconnector_handle_request_reset,
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
  .handle_request_body          = mod_msconnector_handle_request_body,
  .handle_response_body         = mod_msconnector_handle_response_body,
#endif
};

INIT_FUNC(mod_msconnector_init) {
    plugin_data * const p = ck_calloc(1, sizeof(*p));
    p->self = &mod_msconnector_plugin;
    return p;
}

__attribute_cold__
__declspec_dllexport__
int mod_msconnector_plugin_init(plugin *p);
int mod_msconnector_plugin_init(plugin *p) {
    memcpy(p, &mod_msconnector_plugin, sizeof(*p));
    return 0;
}

FREE_FUNC(mod_msconnector_free) {
    plugin_data * const p = p_d;
    msconnector_runtime_destroy(&p->runtime);
}

static void mod_msconnector_merge_config_cpv(
        plugin_config * const config,
        const config_plugin_value_t * const cpv) {
    switch (cpv->k_id) {
      case 0: /* msconnector.enabled */
        config->enabled = cpv->v.u != 0U;
        break;
      case 1: /* msconnector.config-file */
        config->config_file = cpv->v.b;
        break;
      default:
        break;
    }
}

static void mod_msconnector_merge_config(
        plugin_config * const config,
        const config_plugin_value_t *cpv) {
    do {
        mod_msconnector_merge_config_cpv(config, cpv);
    } while ((++cpv)->k_id != -1);
}

SETDEFAULTS_FUNC(mod_msconnector_set_defaults) {
    static const config_plugin_keys_t keys[] = {
      { CONST_STR_LEN("msconnector.enabled"),
        T_CONFIG_BOOL,
        T_CONFIG_SCOPE_SERVER }
     ,{ CONST_STR_LEN("msconnector.config-file"),
        T_CONFIG_STRING,
        T_CONFIG_SCOPE_SERVER }
     ,{ NULL, 0,
        T_CONFIG_UNSET,
        T_CONFIG_SCOPE_UNSET }
    };
    plugin_data * const p = p_d;
#ifndef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    msconnector_request_mapper_contract request_contract;
    msconnector_response_mapper_contract response_contract;
#else
    msconnector_body_mode request_body_mode;
    msconnector_body_mode response_body_mode;
#endif
    char error[512] = "";

    if (!config_plugin_values_init(srv, p, keys, "mod_msconnector")) {
        return HANDLER_ERROR;
    }
    if (p->nconfig > 0 && p->cvlist->v.u2[1]) {
        const config_plugin_value_t *cpv =
            p->cvlist + p->cvlist->v.u2[0];
        if (cpv->k_id != -1) {
            mod_msconnector_merge_config(&p->defaults, cpv);
        }
    }
    if (!p->defaults.enabled) {
        return HANDLER_GO_ON;
    }
    if (p->defaults.config_file == NULL ||
        buffer_is_blank(p->defaults.config_file)) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "msconnector.config-file is required when msconnector.enabled is true");
        return HANDLER_ERROR;
    }
    if (!msconnector_runtime_config_check(
            "lighttpd",
            p->defaults.config_file->ptr,
            error,
            sizeof(error))) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "msconnector runtime config check failed: %s",
            error[0] == '\0' ? "unknown error" : error);
        return HANDLER_ERROR;
    }
    if (!msconnector_runtime_create(
            "lighttpd",
            p->defaults.config_file->ptr,
            &p->runtime,
            error,
            sizeof(error))) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "msconnector runtime creation failed: %s",
            error[0] == '\0' ? "unknown error" : error);
        return HANDLER_ERROR;
    }

#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    request_body_mode = msconnector_runtime_request_body_mode(p->runtime);
    response_body_mode = msconnector_runtime_response_body_mode(p->runtime);
    if (request_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED ||
        response_body_mode != MSCONNECTOR_BODY_MODE_NONE) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "patched lighttpd module requires request_body_mode=none or streaming and response_body_mode=none (HTTP/1.x output hooks expose wire bytes, not a decoded response entity)");
        msconnector_runtime_destroy(&p->runtime);
        return HANDLER_ERROR;
    }
    p->request_body_hooks_enabled =
        request_body_mode == MSCONNECTOR_BODY_MODE_STREAMING;
#else
    msconnector_runtime_request_contract(p->runtime, &request_contract);
    msconnector_runtime_response_contract(p->runtime, &response_contract);
    if (request_contract.request_body != MSCONNECTOR_MAPPER_UNSUPPORTED ||
        response_contract.response_body != MSCONNECTOR_MAPPER_UNSUPPORTED) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "stock lighttpd module requires request_body_mode=none and response_body_mode=none; rebuild lighttpd with the 1.4.84 streaming-hook patch for request streaming");
        msconnector_runtime_destroy(&p->runtime);
        return HANDLER_ERROR;
    }
#endif

    p->request_body_limit =
        msconnector_runtime_request_body_limit(p->runtime);
    p->response_body_limit =
        msconnector_runtime_response_body_limit(p->runtime);
    p->total_header_limit =
        msconnector_runtime_total_header_limit(p->runtime);
    p->header_count_limit =
        msconnector_runtime_header_count_limit(p->runtime);

    return HANDLER_GO_ON;
}

static handler_ctx *handler_ctx_create(const request_st * const r) {
    handler_ctx * const ctx = calloc(1U, sizeof(*ctx));
    if (ctx == NULL) {
        return NULL;
    }
    lighttpd_modsecurity_map_storage_init(&ctx->request_storage);
    lighttpd_modsecurity_map_storage_init(&ctx->response_storage);
    (void)snprintf(
        ctx->host_request_id,
        sizeof(ctx->host_request_id),
        "lighttpd-%ld-%d-%u-%u",
        (long)getpid(),
        r->con == NULL ? -1 : r->con->fd,
        r->con == NULL ? 0U : r->con->request_count,
        r->x.h2.id);
    return ctx;
}

static void handler_ctx_destroy(handler_ctx **ctx_ptr) {
    handler_ctx *ctx;
    if (ctx_ptr == NULL || *ctx_ptr == NULL) {
        return;
    }
    ctx = *ctx_ptr;
    msconnector_runtime_transaction_destroy(&ctx->transaction);
    lighttpd_modsecurity_map_storage_free(&ctx->request_storage);
    lighttpd_modsecurity_map_storage_free(&ctx->response_storage);
    free(ctx);
    *ctx_ptr = NULL;
}

static handler_t mod_msconnector_error_response(
        request_st * const r,
        const msconnector_runtime * const runtime,
        msconnector_error_code code) {
    int status = msconnector_runtime_error_http_status(runtime, code);
    if (status < 400 || status > 599) {
        status = 500;
    }
    return http_status_set_err(r, status);
}

static handler_t mod_msconnector_apply_decision(
        request_st * const r,
        const msconnector_decision * const decision) {
    int status;
    if (!msconnector_decision_is_disruptive(decision)) {
        return HANDLER_GO_ON;
    }
    status = msconnector_decision_http_status(decision);
    if (status < 400 || status > 599) {
        status = 403;
    }
    return http_status_set_err(r, status);
}

#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION

typedef struct {
    handler_ctx *ctx;
    msconnector_error runtime_error;
} mod_msconnector_body_append_context;

static int mod_msconnector_append_request_body_range(
        void *userdata,
        const unsigned char *data,
        size_t size,
        char *error,
        size_t error_len) {
    mod_msconnector_body_append_context *append = userdata;

    if (!msconnector_runtime_transaction_append_request_body_chunk(
            append->ctx->transaction,
            data,
            size,
            &append->runtime_error)) {
        (void)snprintf(
            error,
            error_len,
            "request body append failed: %s",
            msconnector_error_code_name(append->runtime_error.code));
        return 0;
    }
    return 1;
}

static handler_t mod_msconnector_finish_request_body(
        request_st *r,
        plugin_data *p,
        handler_ctx *ctx) {
    msconnector_decision decision;
    msconnector_error runtime_error;

    if (ctx->request_body_finished) {
        return HANDLER_GO_ON;
    }
    msconnector_decision_init(&decision);
    msconnector_error_init(&runtime_error);
    if (!msconnector_runtime_transaction_finish_request_body(
            ctx->transaction,
            &decision,
            &runtime_error)) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector request-body finalization failed: %s",
            msconnector_error_code_name(runtime_error.code));
        return mod_msconnector_error_response(r, p->runtime, runtime_error.code);
    }
    ctx->request_body_finished = 1;
    return mod_msconnector_apply_decision(r, &decision);
}

static handler_t mod_msconnector_prepare_request_body(
        request_st *r,
        plugin_data *p,
        handler_ctx *ctx) {
    handler_t rc;

    if (!p->request_body_hooks_enabled || ctx->request_body_finished) {
        return HANDLER_GO_ON;
    }
    if (r->http_version > HTTP_VERSION_1_1) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "patched msconnector request streaming is limited to HTTP/1.x");
        return http_status_set_err(r, 501);
    }
    if (r->reqbody_length == 0) {
        return mod_msconnector_finish_request_body(r, p, ctx);
    }

    r->conf.stream_request_body |= FDEVENT_STREAM_REQUEST;
    rc = r->con->reqbody_read(r);
    if (rc != HANDLER_GO_ON) {
        return rc;
    }
    return ctx->request_body_finished ? HANDLER_GO_ON : HANDLER_WAIT_FOR_EVENT;
}

static handler_t mod_msconnector_handle_request_body(
        request_st *r,
        const chunkqueue *queue,
        off_t queue_offset,
        off_t length,
        off_t stream_offset,
        int eos,
        void *p_d) {
    plugin_data *p = p_d;
    handler_ctx *ctx = r->plugin_ctx[p->id];
    mod_msconnector_body_append_context append;
    char mapper_error[256] = "";

    if (!p->request_body_hooks_enabled || ctx == NULL ||
        ctx->transaction == NULL || ctx->request_body_finished) {
        return HANDLER_GO_ON;
    }
    if (stream_offset != ctx->request_body_next_offset) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector request-body hook received a non-contiguous range");
        return mod_msconnector_error_response(
            r, p->runtime, MSCONNECTOR_ERROR_HOST_API_FAILURE);
    }

    append.ctx = ctx;
    msconnector_error_init(&append.runtime_error);
    if (length > 0 && !lighttpd_modsecurity_visit_body_range(
            queue,
            queue_offset,
            length,
            mod_msconnector_append_request_body_range,
            &append,
            mapper_error,
            sizeof(mapper_error))) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector request-body mapping failed: %s",
            mapper_error[0] == '\0' ? "unknown error" : mapper_error);
        return mod_msconnector_error_response(
            r,
            p->runtime,
            append.runtime_error.code == MSCONNECTOR_ERROR_NONE
              ? MSCONNECTOR_ERROR_HOST_API_FAILURE : append.runtime_error.code);
    }
    ctx->request_body_next_offset += length;
    return eos ? mod_msconnector_finish_request_body(r, p, ctx) : HANDLER_GO_ON;
}

static plugin_body_hook_result mod_msconnector_handle_response_body(
        request_st *r,
        const chunkqueue *queue,
        off_t queue_offset,
        off_t length,
        off_t stream_offset,
        int eos,
        void *p_d) {
    /*
     * The local core patch invokes this at the HTTP/1.x socket-write stage.
     * That queue can contain transfer framing, so it is intentionally not a
     * Common response-body ingestion path.  Keep the callback registered to
     * exercise the patched ABI, but never turn wire ranges or EOS into Phase
     * 4 processing.  The supported `none` mode does not call the runtime
     * response-body finish API at reset either: no decoded entity was ever
     * supplied to that lifecycle.
     */
    (void)r;
    (void)queue;
    (void)queue_offset;
    (void)length;
    (void)stream_offset;
    (void)eos;
    (void)p_d;
    return PLUGIN_BODY_HOOK_CONTINUE;
}

#endif

REQUEST_FUNC(mod_msconnector_handle_uri_clean) {
    plugin_data * const p = p_d;
    handler_ctx **ctx_slot;
    handler_ctx *ctx;
    msconnector_request_mapper_contract contract;
    msconnector_decision decision;
    msconnector_error runtime_error;
    char mapper_error[256] = "";

    if (!p->defaults.enabled || p->runtime == NULL) {
        return HANDLER_GO_ON;
    }
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    if (r->http_version > HTTP_VERSION_1_1) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "patched msconnector full lifecycle is limited to HTTP/1.x; HTTP/2 uses a multiplexed output queue");
        return http_status_set_err(r, 501);
    }
#endif
    ctx_slot = (handler_ctx **)&r->plugin_ctx[p->id];
    if (*ctx_slot != NULL) {
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
        return mod_msconnector_prepare_request_body(r, p, *ctx_slot);
#else
        return HANDLER_GO_ON;
#endif
    }
    ctx = handler_ctx_create(r);
    if (ctx == NULL) {
        return mod_msconnector_error_response(
            r, p->runtime, MSCONNECTOR_ERROR_INTERNAL);
    }
    *ctx_slot = ctx;

    msconnector_runtime_request_contract(p->runtime, &contract);
#ifndef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    contract.request_body = MSCONNECTOR_MAPPER_UNSUPPORTED;
    contract.max_body_bytes = 0U;
#endif
    if (p->header_count_limit > 0U &&
        (contract.max_header_count == 0U ||
         p->header_count_limit < contract.max_header_count)) {
        contract.max_header_count = p->header_count_limit;
    }
    if (!lighttpd_modsecurity_map_request(
            r,
            &contract,
            p->total_header_limit,
            &ctx->request_storage,
            &ctx->request,
            mapper_error,
            sizeof(mapper_error))) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector request mapping failed: %s",
            mapper_error[0] == '\0' ? "unknown error" : mapper_error);
        handler_ctx_destroy(ctx_slot);
        return mod_msconnector_error_response(
            r,
            p->runtime,
            MSCONNECTOR_ERROR_HOST_API_FAILURE);
    }

    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&decision);
    if (!msconnector_runtime_transaction_begin(
            p->runtime,
            &ctx->request,
            ctx->host_request_id,
            &ctx->transaction,
            &decision,
            &runtime_error)) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector transaction begin failed: %s",
            msconnector_error_code_name(runtime_error.code));
        handler_ctx_destroy(ctx_slot);
        return mod_msconnector_error_response(
            r, p->runtime, runtime_error.code);
    }
    {
        const handler_t rc = mod_msconnector_apply_decision(r, &decision);
        if (rc != HANDLER_GO_ON) {
            return rc;
        }
    }
#ifdef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    return mod_msconnector_prepare_request_body(r, p, ctx);
#else
    return HANDLER_GO_ON;
#endif
}

REQUEST_FUNC(mod_msconnector_handle_response_start) {
    plugin_data * const p = p_d;
    handler_ctx *ctx;
    msconnector_response_mapper_contract contract;
    msconnector_decision decision;
    msconnector_error runtime_error;
    char mapper_error[256] = "";

    if (!p->defaults.enabled || p->runtime == NULL) {
        return HANDLER_GO_ON;
    }
    ctx = r->plugin_ctx[p->id];
    if (ctx == NULL || ctx->transaction == NULL || ctx->response_processed) {
        return HANDLER_GO_ON;
    }

    msconnector_runtime_response_contract(p->runtime, &contract);
#ifndef LIGHTTPD_MSCONNECTOR_STREAM_HOOK_ABI_VERSION
    contract.response_body = MSCONNECTOR_MAPPER_UNSUPPORTED;
    contract.max_body_bytes = 0U;
#endif
    if (p->header_count_limit > 0U &&
        (contract.max_header_count == 0U ||
         p->header_count_limit < contract.max_header_count)) {
        contract.max_header_count = p->header_count_limit;
    }
    if (!lighttpd_modsecurity_map_response(
            r,
            &contract,
            p->total_header_limit,
            &ctx->response_storage,
            &ctx->response,
            mapper_error,
            sizeof(mapper_error))) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector response mapping failed: %s",
            mapper_error[0] == '\0' ? "unknown error" : mapper_error);
        return mod_msconnector_error_response(
            r,
            p->runtime,
            MSCONNECTOR_ERROR_HOST_API_FAILURE);
    }

    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&decision);
    if (!msconnector_runtime_transaction_process_response_headers(
            ctx->transaction,
            &ctx->response,
            &decision,
            &runtime_error)) {
        log_error(
            r->conf.errh,
            __FILE__,
            __LINE__,
            "msconnector response processing failed: %s",
            msconnector_error_code_name(runtime_error.code));
        return mod_msconnector_error_response(
            r, p->runtime, runtime_error.code);
    }
    ctx->response_processed = 1;
    return mod_msconnector_apply_decision(r, &decision);
}

REQUEST_FUNC(mod_msconnector_handle_request_reset) {
    plugin_data * const p = p_d;
    handler_ctx **ctx_slot = (handler_ctx **)&r->plugin_ctx[p->id];
    handler_ctx *ctx = *ctx_slot;
    msconnector_error runtime_error;

    if (ctx == NULL) {
        return HANDLER_GO_ON;
    }
    if (ctx->transaction != NULL) {
        msconnector_error_init(&runtime_error);
        if (!msconnector_runtime_transaction_finish(
                ctx->transaction,
                &runtime_error)) {
            log_error(
                r->conf.errh,
                __FILE__,
                __LINE__,
                "msconnector transaction finish failed: %s",
                msconnector_error_code_name(runtime_error.code));
        }
    }
    handler_ctx_destroy(ctx_slot);
    return HANDLER_GO_ON;
}
