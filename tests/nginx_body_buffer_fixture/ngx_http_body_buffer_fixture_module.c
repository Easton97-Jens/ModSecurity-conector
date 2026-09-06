/*
 * Native-only regression fixture for the NGINX P4 response-buffer boundary.
 *
 * This module is never linked into the connector.  The test runner builds it
 * as a separate dynamic HTTP module next to the exact-head connector and
 * drives its handler over loopback.  Its sole purpose is to create real
 * ngx_buf_t representations that ordinary HTTP upstream responses cannot
 * select deterministically.
 */

#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

#include <errno.h>
#include <signal.h>

#define FIXTURE_BODY "P4-FIXTURE-BODY!"
#define FIXTURE_BODY_LENGTH (sizeof(FIXTURE_BODY) - 1U)
#define FIXTURE_OVER_LIMIT_LENGTH (FIXTURE_BODY_LENGTH + 1U)

typedef struct {
    ngx_str_t mode;
    ngx_str_t file;
    ngx_str_t short_file;
    ngx_str_t mixed_file;
} ngx_http_body_buffer_fixture_loc_conf_t;

static ngx_int_t ngx_http_body_buffer_fixture_handler(ngx_http_request_t *r);
static void *ngx_http_body_buffer_fixture_create_loc_conf(ngx_conf_t *cf);
static char *ngx_http_body_buffer_fixture_merge_loc_conf(ngx_conf_t *cf,
    void *parent, void *child);
static char *ngx_http_body_buffer_fixture_set_mode(ngx_conf_t *cf,
    ngx_command_t *cmd, void *conf);
static ngx_int_t ngx_http_body_buffer_fixture_mode_is(
    const ngx_str_t *mode, const char *literal);
static ngx_int_t ngx_http_body_buffer_fixture_needs_file(
    const ngx_str_t *mode);
static ngx_int_t ngx_http_body_buffer_fixture_open_file(ngx_http_request_t *r,
    const ngx_str_t *path, ngx_file_t **file);
static ngx_int_t ngx_http_body_buffer_fixture_add_header(ngx_http_request_t *r,
    const ngx_str_t *mode);

/* This symbol is linked only into the runner's separately built NGINX test
 * binary with --wrap=malloc.  The production connector and its dynamic module
 * neither compile nor link it. */
extern void *__real_malloc(size_t size);

/* The test-only content handler and this link-time wrapper run in the same
 * NGINX worker.  A process-local flag avoids relying on a mutable environment
 * from the worker while keeping allocation injection out of the connector. */
static volatile sig_atomic_t ngx_http_body_buffer_fixture_fail_allocation;

void *
__wrap_malloc(size_t size)
{
    if (ngx_http_body_buffer_fixture_fail_allocation != 0 && size == 32768U) {
        errno = ENOMEM;
        return NULL;
    }
    return __real_malloc(size);
}

static ngx_command_t ngx_http_body_buffer_fixture_commands[] = {
    {
        ngx_string("body_buffer_fixture"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_http_body_buffer_fixture_set_mode,
        NGX_HTTP_LOC_CONF_OFFSET,
        0,
        NULL
    },
    {
        ngx_string("body_buffer_fixture_file"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_conf_set_str_slot,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_body_buffer_fixture_loc_conf_t, file),
        NULL
    },
    {
        ngx_string("body_buffer_fixture_short_file"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_conf_set_str_slot,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_body_buffer_fixture_loc_conf_t, short_file),
        NULL
    },
    {
        ngx_string("body_buffer_fixture_mixed_file"),
        NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
        ngx_conf_set_str_slot,
        NGX_HTTP_LOC_CONF_OFFSET,
        offsetof(ngx_http_body_buffer_fixture_loc_conf_t, mixed_file),
        NULL
    },
    ngx_null_command
};

static ngx_http_module_t ngx_http_body_buffer_fixture_module_ctx = {
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    ngx_http_body_buffer_fixture_create_loc_conf,
    ngx_http_body_buffer_fixture_merge_loc_conf
};

ngx_module_t ngx_http_body_buffer_fixture_module = {
    NGX_MODULE_V1,
    &ngx_http_body_buffer_fixture_module_ctx,
    ngx_http_body_buffer_fixture_commands,
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

static ngx_int_t
ngx_http_body_buffer_fixture_mode_is(const ngx_str_t *mode, const char *literal)
{
    size_t length;

    length = ngx_strlen(literal);
    return mode != NULL && mode->data != NULL && mode->len == length &&
        ngx_strncmp(mode->data, (const u_char *) literal, length) == 0;
}

static ngx_int_t
ngx_http_body_buffer_fixture_needs_file(const ngx_str_t *mode)
{
    return ngx_http_body_buffer_fixture_mode_is(mode, "file-within") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "file-over-limit") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "mixed-within") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "mixed-over-limit") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "read-error") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "short-read") ||
        ngx_http_body_buffer_fixture_mode_is(mode, "allocation-failure");
}

static ngx_int_t
ngx_http_body_buffer_fixture_open_file(ngx_http_request_t *r,
    const ngx_str_t *path, ngx_file_t **file)
{
    ngx_file_t *opened;
    ngx_pool_cleanup_t *cleanup;
    ngx_pool_cleanup_file_t *cleanup_file;

    if (file == NULL || path == NULL || path->len == 0U ||
        path->data == NULL) {
        return NGX_ERROR;
    }

    opened = ngx_pcalloc(r->pool, sizeof(*opened));
    if (opened == NULL) {
        return NGX_ERROR;
    }
    opened->name = *path;
    opened->log = r->connection->log;
    opened->fd = ngx_open_file(opened->name.data, NGX_FILE_RDONLY,
        NGX_FILE_OPEN, 0);
    if (opened->fd == NGX_INVALID_FILE) {
        return NGX_ERROR;
    }

    cleanup = ngx_pool_cleanup_add(r->pool, sizeof(*cleanup_file));
    if (cleanup == NULL) {
        (void) ngx_close_file(opened->fd);
        return NGX_ERROR;
    }
    cleanup->handler = ngx_pool_cleanup_file;
    cleanup_file = cleanup->data;
    cleanup_file->fd = opened->fd;
    cleanup_file->name = opened->name.data;
    cleanup_file->log = r->connection->log;
    *file = opened;

    return NGX_OK;
}

static ngx_int_t
ngx_http_body_buffer_fixture_add_header(ngx_http_request_t *r,
    const ngx_str_t *mode)
{
    ngx_table_elt_t *header;

    header = ngx_list_push(&r->headers_out.headers);
    if (header == NULL) {
        return NGX_ERROR;
    }
    header->hash = 1;
    ngx_str_set(&header->key, "X-Nginx-Body-Buffer-Fixture");
    header->value = *mode;
    return NGX_OK;
}

static ngx_int_t
ngx_http_body_buffer_fixture_handler(ngx_http_request_t *r)
{
    ngx_http_body_buffer_fixture_loc_conf_t *conf;
    ngx_buf_t *buffer;
    ngx_chain_t output;
    ngx_file_t *file = NULL;
    const ngx_str_t *file_path;
    u_char *memory;
    size_t memory_length = 0U;
    off_t file_length = 0;
    ngx_int_t result;
    ngx_uint_t allocation_failure;

    if (r->method != NGX_HTTP_GET && r->method != NGX_HTTP_HEAD) {
        return NGX_HTTP_NOT_ALLOWED;
    }
    conf = ngx_http_get_module_loc_conf(r, ngx_http_body_buffer_fixture_module);
    if (conf == NULL || conf->mode.len == 0U || conf->mode.data == NULL) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    allocation_failure = ngx_http_body_buffer_fixture_mode_is(&conf->mode,
        "allocation-failure");
    ngx_http_body_buffer_fixture_fail_allocation = 0;

    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "memory-within") ||
        ngx_http_body_buffer_fixture_mode_is(&conf->mode, "mixed-within")) {
        memory_length = FIXTURE_BODY_LENGTH;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "memory-over-limit") ||
               ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "mixed-over-limit")) {
        memory_length = FIXTURE_OVER_LIMIT_LENGTH;
    }

    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "file-within") ||
        ngx_http_body_buffer_fixture_mode_is(&conf->mode, "mixed-within")) {
        file_length = (off_t) FIXTURE_BODY_LENGTH;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "file-over-limit") ||
               ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "mixed-over-limit")) {
        file_length = (off_t) FIXTURE_OVER_LIMIT_LENGTH;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "allocation-failure") ||
               ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "read-error")) {
        /* Keep this file range within the configured limit so the real
         * connector reaches its request-pool scratch allocation. */
        file_length = (off_t) FIXTURE_BODY_LENGTH;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "short-read")) {
        /* The physical short fixture file has one fewer byte.  Keep the
         * declared range within the existing limit so ngx_read_file runs. */
        file_length = (off_t) FIXTURE_BODY_LENGTH;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "invalid-metadata") ||
               ngx_http_body_buffer_fixture_mode_is(&conf->mode,
                   "missing-source")) {
        /* Metadata and missing-source cases must reach their own connector
         * checks, rather than being rejected first by the body-limit plan. */
        file_length = (off_t) FIXTURE_BODY_LENGTH;
    } else if (memory_length == 0U) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }

    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "mixed-within") ||
        ngx_http_body_buffer_fixture_mode_is(&conf->mode, "mixed-over-limit")) {
        file_path = &conf->mixed_file;
    } else if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "short-read")) {
        file_path = &conf->short_file;
    } else {
        file_path = &conf->file;
    }
    if (ngx_http_body_buffer_fixture_needs_file(&conf->mode) &&
        !ngx_http_body_buffer_fixture_mode_is(&conf->mode, "read-error")) {
        if (ngx_http_body_buffer_fixture_open_file(r, file_path, &file) != NGX_OK) {
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
    }
    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "read-error")) {
        file = ngx_pcalloc(r->pool, sizeof(*file));
        if (file == NULL) {
            return NGX_HTTP_INTERNAL_SERVER_ERROR;
        }
        file->fd = NGX_INVALID_FILE;
        file->name = conf->file;
        file->log = r->connection->log;
    }

    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = memory_length != 0U
        ? (off_t) memory_length : file_length;
    ngx_str_set(&r->headers_out.content_type, "text/plain");
    if (ngx_http_body_buffer_fixture_add_header(r, &conf->mode) != NGX_OK) {
        return NGX_HTTP_INTERNAL_SERVER_ERROR;
    }
    result = ngx_http_send_header(r);
    if (result == NGX_ERROR || result > NGX_OK || r->header_only) {
        return result;
    }

    buffer = ngx_pcalloc(r->pool, sizeof(*buffer));
    if (buffer == NULL) {
        return NGX_ERROR;
    }
    if (memory_length != 0U) {
        memory = ngx_pnalloc(r->pool, memory_length);
        if (memory == NULL) {
            return NGX_ERROR;
        }
        ngx_memcpy(memory, FIXTURE_BODY, FIXTURE_BODY_LENGTH);
        if (memory_length > FIXTURE_BODY_LENGTH) {
            memory[FIXTURE_BODY_LENGTH] = 'X';
        }
        buffer->pos = memory;
        buffer->last = memory + memory_length;
        buffer->memory = 1;
    }
    if (file_length != 0) {
        buffer->in_file = 1;
        buffer->file_pos = 0;
        buffer->file_last = file_length;
        buffer->file = file;
    }
    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "invalid-metadata")) {
        buffer->file_pos = 1;
        buffer->file_last = 0;
    }
    if (ngx_http_body_buffer_fixture_mode_is(&conf->mode, "missing-source")) {
        buffer->file = NULL;
    }
    buffer->last_buf = 1;
    buffer->last_in_chain = 1;
    output.buf = buffer;
    output.next = NULL;

    ngx_log_error(NGX_LOG_NOTICE, r->connection->log, 0,
        "body-buffer-fixture mode=%V memory=%ui in_file=%ui file_pos=%O file_last=%O memory_length=%uz",
        &conf->mode, (ngx_uint_t) ngx_buf_in_memory(buffer),
        (ngx_uint_t) buffer->in_file, buffer->file_pos, buffer->file_last,
        memory_length);
    if (allocation_failure != 0U) {
        ngx_http_body_buffer_fixture_fail_allocation = 1;
    }
    result = ngx_http_output_filter(r, &output);
    ngx_http_body_buffer_fixture_fail_allocation = 0;
    return result;
}

static void *
ngx_http_body_buffer_fixture_create_loc_conf(ngx_conf_t *cf)
{
    return ngx_pcalloc(cf->pool, sizeof(ngx_http_body_buffer_fixture_loc_conf_t));
}

static char *
ngx_http_body_buffer_fixture_merge_loc_conf(ngx_conf_t *cf, void *parent,
    void *child)
{
    (void) cf;
    (void) parent;
    (void) child;
    return NGX_CONF_OK;
}

static char *
ngx_http_body_buffer_fixture_set_mode(ngx_conf_t *cf, ngx_command_t *cmd,
    void *conf)
{
    ngx_http_body_buffer_fixture_loc_conf_t *fixture = conf;
    ngx_http_core_loc_conf_t *core;
    ngx_str_t *value;
    const char *allowed[] = {
        "memory-within", "memory-over-limit", "file-within",
        "file-over-limit", "mixed-within", "mixed-over-limit",
        "invalid-metadata", "missing-source", "read-error", "short-read",
        "allocation-failure", NULL
    };
    ngx_uint_t index;

    (void) cmd;
    if (fixture->mode.data != NULL) {
        return "is duplicate";
    }
    value = cf->args->elts;
    for (index = 0U; allowed[index] != NULL; index++) {
        if (ngx_http_body_buffer_fixture_mode_is(&value[1], allowed[index])) {
            fixture->mode = value[1];
            core = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
            core->handler = ngx_http_body_buffer_fixture_handler;
            return NGX_CONF_OK;
        }
    }
    return "has an unsupported body-buffer fixture mode";
}
