#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <ngx_string.h>

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
extern int msc_rust_disruptive_status(MsShimTransaction *transaction);

typedef struct {
    ngx_str_t rules_path;
    MscRustEngine *engine;
} nginx_rust_main_conf;

typedef struct {
    MsShimTransaction *transaction;
} nginx_rust_loc_conf;

typedef struct {
    ngx_flag_t enabled;
} nginx_rust_location_conf;

static ngx_int_t ngx_http_rust_waf_handler(ngx_http_request_t *request);
static void *ngx_http_rust_create_main_conf(ngx_conf_t *conf);
static char *ngx_http_rust_init_rules(ngx_conf_t *conf, ngx_command_t *command, void *mconfig);
static void *ngx_http_rust_create_loc_conf(ngx_conf_t *conf);
static char *ngx_http_rust_enable(ngx_conf_t *conf, ngx_command_t *command, void *mconfig);

static ngx_command_t ngx_http_rust_commands[] = {
    {
        ngx_string("RustModSecurityRules"),
        NGX_HTTP_MAIN_CONF | NGX_CONF_TAKE1,
        ngx_http_rust_init_rules,
        NGX_HTTP_MAIN_CONF_OFFSET,
        offsetof(nginx_rust_main_conf, rules_path),
        NULL
    },
    {
        ngx_string("RustModSecurityOn"),
        NGX_HTTP_LOC_CONF | NGX_CONF_NOARGS,
        ngx_http_rust_enable,
        NGX_HTTP_LOC_CONF_OFFSET,
        0,
        NULL
    },
    ngx_null_command
};

static ngx_http_module_t ngx_http_rust_module_ctx = {
    NULL,
    NULL,
    ngx_http_rust_create_main_conf,
    NULL,
    NULL,
    NULL,
    ngx_http_rust_create_loc_conf,
    NULL
};

ngx_module_t ngx_http_rust_module = {
    NGX_MODULE_V1,
    &ngx_http_rust_module_ctx,
    ngx_http_rust_commands,
    NGX_HTTP_MODULE,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NGX_MODULE_V1_PADDING
};

static void *ngx_http_rust_create_main_conf(ngx_conf_t *conf) {
    return ngx_pcalloc(conf->pool, sizeof(nginx_rust_main_conf));
}

static void *ngx_http_rust_create_loc_conf(ngx_conf_t *conf) {
    nginx_rust_location_conf *location =
        ngx_pcalloc(conf->pool, sizeof(nginx_rust_location_conf));
    if (location == NULL) {
        return NULL;
    }
    location->enabled = NGX_CONF_UNSET;
    return location;
}

static char *ngx_http_rust_enable(ngx_conf_t *conf, ngx_command_t *command, void *mconfig) {
    nginx_rust_location_conf *location = mconfig;
    location->enabled = 1;
    ngx_http_core_loc_conf_t *core =
        ngx_http_conf_get_module_loc_conf(conf, ngx_http_core_module);
    if (core != NULL) {
        core->handler = ngx_http_rust_waf_handler;
    }
    (void)command;
    return NGX_CONF_OK;
}

static char *ngx_http_rust_init_rules(ngx_conf_t *conf, ngx_command_t *command, void *mconfig) {
    nginx_rust_main_conf *main_conf = ngx_http_conf_get_module_main_conf(conf, ngx_http_rust_module);
    ngx_str_t *value = conf->args->elts;
    main_conf->rules_path = value[1];
    char *path = ngx_pnalloc(conf->pool, main_conf->rules_path.len + 1);
    if (path == NULL) {
        return NGX_CONF_ERROR;
    }
    ngx_memcpy(path, main_conf->rules_path.data, main_conf->rules_path.len);
    path[main_conf->rules_path.len] = '\0';
    main_conf->engine = msc_rust_engine_new(path);
    if (main_conf->engine == NULL) {
        return "failed to load Rust ModSecurity rules";
    }
    (void)mconfig;
    (void)command;
    return NGX_CONF_OK;
}

static ngx_int_t ngx_http_rust_waf_handler(ngx_http_request_t *request) {
    nginx_rust_main_conf *main_conf =
        ngx_http_get_module_main_conf(request, ngx_http_rust_module);
    if (main_conf == NULL || main_conf->engine == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    char id[64];
    ngx_snprintf((u_char *)id, sizeof(id), "nginx-rust-%d", (int)request->connection->number);
    MsShimTransaction *transaction =
        msc_rust_transaction_new(main_conf->engine, id);
    if (transaction == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    char client_ip[INET6_ADDRSTRLEN];
    ngx_str_t client = request->connection->addr_text;
    ngx_snprintf((u_char *)client_ip, sizeof(client_ip), "%*s",
        (int)client.len, client.data);
    if (msc_rust_process_connection(transaction, client_ip) < 0) {
        msc_rust_transaction_free(transaction);
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    char uri[4097];
    ngx_snprintf((u_char *)uri, sizeof(uri), "%*s",
        (int)request->unparsed_uri.len, request->unparsed_uri.data);
    if (msc_rust_process_uri(transaction, uri, "http",
            request->http_protocol.len > 0 ? "HTTP/1.1" : "HTTP/1.1") < 0) {
        msc_rust_transaction_free(transaction);
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    ngx_list_part_t *part = &request->headers_in.headers.part;
    ngx_table_elt_t *header = part->elts;
    for (ngx_uint_t index = 0;; index++) {
        if (index >= part->nelts) {
            if (part->next == NULL) break;
            part = part->next;
            header = part->elts;
            index = 0;
        }
        char name[257], value[8193];
        ngx_snprintf((u_char *)name, sizeof(name), "%*s",
            (int)header[index].key.len, header[index].key.data);
        ngx_snprintf((u_char *)value, sizeof(value), "%*s",
            (int)header[index].value.len, header[index].value.data);
        if (msc_rust_add_request_header(transaction, name, value) < 0) {
            msc_rust_transaction_free(transaction);
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
    }
    if (msc_rust_process_request_headers(transaction) < 0) {
        msc_rust_transaction_free(transaction);
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    int status = msc_rust_disruptive_status(transaction);
    msc_rust_transaction_free(transaction);
    if (status >= 400) {
        return status <= 599 ? status : NGX_HTTP_FORBIDDEN;
    }
    return NGX_DECLINED;
}
