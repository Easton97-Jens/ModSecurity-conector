#include "httpd.h"
#include "http_config.h"
#include "http_request.h"
#include "http_protocol.h"
#include "http_log.h"
#include "apr_tables.h"
#include "apr_strings.h"

#include <stddef.h>

typedef struct MscRustEngine MscRustEngine;
typedef struct MsShimTransaction MsShimTransaction;

extern MscRustEngine *msc_rust_engine_new(const char *rules_path);
extern void msc_rust_engine_free(MscRustEngine *engine);
extern MsShimTransaction *msc_rust_transaction_new(MscRustEngine *engine, const char *id);
extern void msc_rust_transaction_free(MsShimTransaction *transaction);
extern int msc_rust_process_connection(MsShimTransaction *transaction, const char *client_ip);
extern int msc_rust_process_uri(MsShimTransaction *transaction, const char *uri, const char *protocol, const char *http_version);
extern int msc_rust_add_request_header(MsShimTransaction *transaction, const char *name, const char *value);
extern int msc_rust_process_request_headers(MsShimTransaction *transaction);
extern int msc_rust_append_request_body(MsShimTransaction *transaction, const unsigned char *data, size_t len);
extern int msc_rust_finish_request_body(MsShimTransaction *transaction);
extern int msc_rust_disruptive_status(MsShimTransaction *transaction);

typedef struct {
    const char *rules_path;
} rust_security_config;

typedef struct {
    MscRustEngine *engine;
    MsShimTransaction *transaction;
} rust_security_context;

extern module AP_MODULE_DECLARE_DATA rust_security_module;

static rust_security_config *rust_security_server_config(server_rec *server);

static void *rust_security_create_server_config(apr_pool_t *pool, server_rec *server) {
    rust_security_config *config = apr_pcalloc(pool, sizeof(*config));
    (void)server;
    config->rules_path = NULL;
    return config;
}

static const char *rust_security_set_rules(cmd_parms *cmd, void *mconfig, const char *path) {
    rust_security_config *config = rust_security_server_config(cmd->server);
    config->rules_path = apr_pstrdup(cmd->pool, path);
    (void)mconfig;
    return NULL;
}

static rust_security_config *rust_security_server_config(server_rec *server) {
    return ap_get_module_config(server->module_config, &rust_security_module);
}

static rust_security_context *rust_security_context_for(request_rec *request) {
    rust_security_context *context =
        ap_get_module_config(request->request_config, &rust_security_module);
    if (context == NULL) {
        context = apr_pcalloc(request->pool, sizeof(*context));
        ap_set_module_config(request->request_config, &rust_security_module, context);
    }
    return context;
}

static apr_status_t rust_security_cleanup(void *data) {
    rust_security_context *context = data;
    if (context != NULL && context->transaction != NULL) {
        msc_rust_transaction_free(context->transaction);
        context->transaction = NULL;
    }
    if (context != NULL && context->engine != NULL) {
        msc_rust_engine_free(context->engine);
        context->engine = NULL;
    }
    return APR_SUCCESS;
}

static int rust_security_translate(request_rec *request) {
    rust_security_config *config = rust_security_server_config(request->server);
    if (config == NULL || config->rules_path == NULL || *config->rules_path == '\0') {
        return DECLINED;
    }
    rust_security_context *context = rust_security_context_for(request);
    if (context->engine == NULL) {
        context->engine = msc_rust_engine_new(config->rules_path);
        if (context->engine == NULL) {
            ap_log_rerror(APLOG_MARK, APLOG_ERR, 0, request,
                "Rust ModSecurity engine failed to load rules");
            return HTTP_INTERNAL_SERVER_ERROR;
        }
    }
    char transaction_id[64];
    apr_snprintf(transaction_id, sizeof(transaction_id), "apache-rust-%lu",
        (unsigned long)request->connection->id);
    context->transaction = msc_rust_transaction_new(context->engine, transaction_id);
    if (context->transaction == NULL) {
        ap_log_rerror(APLOG_MARK, APLOG_ERR, 0, request,
            "Rust ModSecurity transaction creation failed");
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    apr_pool_cleanup_register(request->pool, context, rust_security_cleanup,
        apr_pool_cleanup_null);
    const char *client_ip = request->connection->client_ip;
    if (msc_rust_process_connection(context->transaction,
            client_ip != NULL ? client_ip : "127.0.0.1") < 0 ||
        msc_rust_process_uri(context->transaction,
            request->unparsed_uri != NULL ? request->unparsed_uri : "/",
            "http",
            request->protocol != NULL ? request->protocol : "HTTP/1.1") < 0) {
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    const apr_array_header_t *headers = apr_table_elts(request->headers_in);
    const apr_table_entry_t *entries = (const apr_table_entry_t *)headers->elts;
    for (int index = 0; index < headers->nelts; ++index) {
        if (entries[index].key != NULL &&
            msc_rust_add_request_header(context->transaction,
                entries[index].key,
                entries[index].val != NULL ? entries[index].val : "") < 0) {
            return HTTP_INTERNAL_SERVER_ERROR;
        }
    }
    if (msc_rust_process_request_headers(context->transaction) < 0) {
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    int status = msc_rust_disruptive_status(context->transaction);
    if (status >= 400) {
        return status <= 599 ? status : HTTP_FORBIDDEN;
    }
    return DECLINED;
}

static const command_rec rust_security_commands[] = {
    AP_INIT_TAKE1("RustModSecurityConfigFile", rust_security_set_rules, NULL,
        RSRC_CONF, "Path to ModSecurity rules"),
    { NULL }
};

static void rust_security_register_hooks(apr_pool_t *pool) {
    (void)pool;
    ap_hook_translate_name(rust_security_translate, NULL, NULL, APR_HOOK_FIRST);
}

module AP_MODULE_DECLARE_DATA rust_security_module = {
    STANDARD20_MODULE_STUFF,
    NULL,
    NULL,
    rust_security_create_server_config,
    NULL,
    rust_security_commands,
    rust_security_register_hooks
};
