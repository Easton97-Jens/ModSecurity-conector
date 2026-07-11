#include "first.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "array.h"
#include "base.h"
#include "buffer.h"
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
} plugin_data;

typedef struct {
    msconnector_runtime_transaction *transaction;
    lighttpd_modsecurity_map_storage request_storage;
    lighttpd_modsecurity_map_storage response_storage;
    msconnector_request request;
    msconnector_response response;
    char host_request_id[96];
    int response_processed;
    int response_body_finished;
} handler_ctx;

INIT_FUNC(mod_msconnector_init);
FREE_FUNC(mod_msconnector_free);
SETDEFAULTS_FUNC(mod_msconnector_set_defaults);
REQUEST_FUNC(mod_msconnector_handle_uri_clean);
REQUEST_FUNC(mod_msconnector_handle_response_start);
REQUEST_FUNC(mod_msconnector_handle_request_reset);

static const plugin mod_msconnector_plugin = {
  .name                         = "msconnector",
  .version                      = LIGHTTPD_VERSION_ID,
  .init                         = mod_msconnector_init,
  .cleanup                      = mod_msconnector_free,
  .set_defaults                 = mod_msconnector_set_defaults,
  .handle_uri_clean             = mod_msconnector_handle_uri_clean,
  .handle_response_start        = mod_msconnector_handle_response_start,
  .handle_request_reset         = mod_msconnector_handle_request_reset
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
    msconnector_request_mapper_contract request_contract;
    msconnector_response_mapper_contract response_contract;
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

    msconnector_runtime_request_contract(p->runtime, &request_contract);
    msconnector_runtime_response_contract(p->runtime, &response_contract);
    if (request_contract.request_body != MSCONNECTOR_MAPPER_UNSUPPORTED ||
        response_contract.response_body != MSCONNECTOR_MAPPER_UNSUPPORTED) {
        log_error(
            srv->errh,
            __FILE__,
            __LINE__,
            "native lighttpd module requires request_body_mode=none and response_body_mode=none");
        msconnector_runtime_destroy(&p->runtime);
        return HANDLER_ERROR;
    }

    p->request_body_limit =
        msconnector_runtime_request_body_limit(p->runtime);
    p->response_body_limit =
        msconnector_runtime_response_body_limit(p->runtime);
    p->total_header_limit =
        msconnector_runtime_total_header_limit(p->runtime);
    p->header_count_limit =
        msconnector_runtime_header_count_limit(p->runtime);

    /*
     * Body limits are retained for the later body-hook implementation. This
     * Phase-1 module deliberately advertises request and response bodies as
     * unsupported and never exposes a body payload to the runtime.
     */
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
    ctx_slot = (handler_ctx **)&r->plugin_ctx[p->id];
    if (*ctx_slot != NULL) {
        return HANDLER_GO_ON;
    }
    ctx = handler_ctx_create(r);
    if (ctx == NULL) {
        return mod_msconnector_error_response(
            r, p->runtime, MSCONNECTOR_ERROR_INTERNAL);
    }
    *ctx_slot = ctx;

    msconnector_runtime_request_contract(p->runtime, &contract);
    contract.request_body = MSCONNECTOR_MAPPER_UNSUPPORTED;
    contract.max_body_bytes = 0U;
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
    return mod_msconnector_apply_decision(r, &decision);
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
    contract.response_body = MSCONNECTOR_MAPPER_UNSUPPORTED;
    contract.max_body_bytes = 0U;
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
        if (ctx->response_processed && !ctx->response_body_finished) {
            msconnector_decision decision;
            msconnector_decision_init(&decision);
            if (!msconnector_runtime_transaction_finish_response_body(
                    ctx->transaction, &decision, &runtime_error)) {
                log_error(
                    r->conf.errh,
                    __FILE__,
                    __LINE__,
                    "msconnector response-body finalization failed: %s",
                    msconnector_error_code_name(runtime_error.code));
            }
            ctx->response_body_finished = 1;
            msconnector_error_init(&runtime_error);
        }
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
