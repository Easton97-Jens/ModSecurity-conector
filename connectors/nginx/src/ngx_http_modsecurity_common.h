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


#ifndef _NGX_HTTP_MODSECURITY_COMMON_H_INCLUDED_
#define _NGX_HTTP_MODSECURITY_COMMON_H_INCLUDED_

#include <nginx.h>
#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>

#include <modsecurity/modsecurity.h>
#include <modsecurity/transaction.h>

#include "msconnector/config.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/limits.h"
#include "msconnector/phase.h"
#include "msconnector/rule_load_stats.h"


/* #define MSC_USE_RULES_SET 1 */

#if defined(MODSECURITY_CHECK_VERSION)
#if MODSECURITY_VERSION_NUM >= 304010
#define MSC_USE_RULES_SET 1
#endif
#endif

#if defined(MSC_USE_RULES_SET)
#include <modsecurity/rules_set.h>
#else
#include <modsecurity/rules.h>
#endif


/**
 * TAG_NUM:
 *
 * Alpha  - 001
 * Beta   - 002
 * Dev    - 010
 * Rc1    - 051
 * Rc2    - 052
 * ...    - ...
 * Release- 100
 *
 */

#define MODSECURITY_NGINX_MAJOR "1"
#define MODSECURITY_NGINX_MINOR "0"
#define MODSECURITY_NGINX_PATCHLEVEL "4"
#define MODSECURITY_NGINX_TAG ""
#define MODSECURITY_NGINX_TAG_NUM "100"

#define MODSECURITY_NGINX_VERSION MODSECURITY_NGINX_MAJOR "." \
    MODSECURITY_NGINX_MINOR "." MODSECURITY_NGINX_PATCHLEVEL \
    MODSECURITY_NGINX_TAG

#define MODSECURITY_NGINX_VERSION_NUM MODSECURITY_NGINX_MAJOR \
    MODSECURITY_NGINX_MINOR MODSECURITY_NGINX_PATCHLEVEL \
    MODSECURITY_NGINX_TAG_NUM

#define MODSECURITY_NGINX_WHOAMI "ModSecurity-nginx v" \
    MODSECURITY_NGINX_VERSION

typedef struct {
    ngx_str_t name;
    ngx_str_t value;
} ngx_http_modsecurity_header_t;


typedef struct {
    ngx_http_request_t *r;
    Transaction *modsec_transaction;
    ModSecurityIntervention *delayed_intervention;

#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    /*
     * Should be filled with the headers that were sent to ModSecurity.
     *
     * The idea is to compare this set of headers with the headers that were
     * sent to the client. This check was placed because we don't have control
     * over other modules, thus, we may partially inspect the headers.
     *
     */
    ngx_array_t *sanity_headers_out;
#endif

    unsigned waiting_more_body:1;
    unsigned body_requested:1;
    unsigned processed:1;
    unsigned logged:1;
    unsigned intervention_triggered:1;
    /* Set only after the redirect helper installs a connector-owned Location.
     * A pre-existing upstream Location must not be mistaken for a ModSecurity
     * response replacement when a status-only intervention is finalized. */
    unsigned intervention_redirect_location_installed:1;
    /* A pre-commit Phase-3 redirect replaced the prepared upstream response.
     * The body filter must drain, rather than forward or inspect, its old
     * response chain.  This is deliberately separate from Phase-4 state. */
    unsigned response_replaced:1;
    unsigned request_body_processed:1;
    unsigned phase4_headers_checked:1;
    unsigned response_headers_seen:1;
    unsigned response_body_seen:1;
    unsigned response_body_truncated:1;
    unsigned response_committed:1;
    unsigned phase4_processed:1;
    unsigned phase4_intervention:1;
    unsigned phase4_strict_abort:1;
    unsigned common_response_validated:1;
    /* Set only around synchronous libmodsecurity request processing calls so
     * its native log callback can emit bounded non-disruptive rule metadata
     * with the actual host phase. */
    unsigned native_event_phase_active:1;
    size_t request_body_bytes_seen;
    size_t response_body_bytes_seen;
    size_t response_body_bytes_inspected;
    size_t request_header_count;
    size_t request_header_bytes;
    size_t response_header_count;
    size_t response_header_bytes;
    ngx_str_t event_transaction_id;
    enum msconnector_phase native_event_phase;
    /* Keep only the bounded rule identifier needed for a metadata-only
     * Phase-4 event.  Do not retain the full libmodsecurity intervention
     * message in the request pool. */
    char last_intervention_rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    ngx_int_t last_intervention_status;
} ngx_http_modsecurity_ctx_t;

/* Keep the native NGINX-to-libmodsecurity header boundary bounded by the
 * same Common limits even when NGINX's list contains attacker-controlled or
 * module-generated entries. */
static ngx_inline ngx_int_t
ngx_http_modsecurity_validate_header(ngx_http_modsecurity_ctx_t *ctx,
    const u_char *name, size_t name_len, const u_char *value, size_t value_len,
    ngx_flag_t response)
{
    size_t current_bytes;

    if (ctx == NULL || ctx->modsec_transaction == NULL ||
        name == NULL || value == NULL ||
        name_len > MSCONNECTOR_MAX_HEADER_NAME_LENGTH ||
        value_len > MSCONNECTOR_MAX_HEADER_VALUE_LENGTH ||
        name_len > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - value_len) {
        return NGX_ERROR;
    }

    current_bytes = name_len + value_len;
    if ((response ? ctx->response_header_count : ctx->request_header_count) >=
            MSCONNECTOR_MAX_HEADER_COUNT ||
        (response ? ctx->response_header_bytes : ctx->request_header_bytes) >
            MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - current_bytes) {
        return NGX_ERROR;
    }

    if (response) {
        ctx->response_header_count++;
        ctx->response_header_bytes += current_bytes;
    } else {
        ctx->request_header_count++;
        ctx->request_header_bytes += current_bytes;
    }

    return NGX_OK;
}

static ngx_inline ngx_int_t
ngx_http_modsecurity_add_n_request_header(ngx_http_modsecurity_ctx_t *ctx,
    const u_char *name, size_t name_len, const u_char *value, size_t value_len)
{
    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,
            value_len, 0) != NGX_OK) {
        return NGX_ERROR;
    }

    return msc_add_n_request_header(ctx->modsec_transaction, name, name_len,
        value, value_len) == 1 ? 1 : NGX_ERROR;
}

static ngx_inline ngx_int_t
ngx_http_modsecurity_add_n_response_header(ngx_http_modsecurity_ctx_t *ctx,
    const u_char *name, size_t name_len, const u_char *value, size_t value_len)
{
    if (ngx_http_modsecurity_validate_header(ctx, name, name_len, value,
            value_len, 1) != NGX_OK) {
        return NGX_ERROR;
    }

    return msc_add_n_response_header(ctx->modsec_transaction, name, name_len,
        value, value_len) == 1 ? 1 : NGX_ERROR;
}


typedef struct {
    void                      *pool;
    ModSecurity               *modsec;
    ngx_uint_t                 rules_inline;
    ngx_uint_t                 rules_file;
    ngx_uint_t                 rules_remote;
} ngx_http_modsecurity_main_conf_t;


static ngx_inline msconnector_rule_load_stats
ngx_http_modsecurity_rule_load_stats(const ngx_http_modsecurity_main_conf_t *mmcf)
{
    msconnector_rule_load_stats stats;

    msconnector_rule_load_stats_init(&stats);
    msconnector_rule_load_stats_add_inline(&stats,
                                           (unsigned) mmcf->rules_inline);
    msconnector_rule_load_stats_add_file(&stats,
                                         (unsigned) mmcf->rules_file);
    msconnector_rule_load_stats_add_remote(&stats,
                                           (unsigned) mmcf->rules_remote);

    return stats;
}


typedef struct {
    void                      *pool;
    /* RulesSet or Rules */
    void                      *rules_set;

    ngx_flag_t                 enable;
    ngx_flag_t                 use_error_log;
#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
    ngx_flag_t                 sanity_checks_enabled;
#endif

    msconnector_config        common_config;

    /* NGINX-owned transitional fields: retained for ngx_conf merge/runtime glue and
     * synchronized into common_config for connector-neutral semantics. */
    ngx_http_complex_value_t  *transaction_id;
    ngx_uint_t                 phase4_mode;
    ngx_array_t               *phase4_content_types;
    ngx_str_t                  phase4_content_types_file;
    ngx_open_file_t           *phase4_log_file;
    ngx_str_t                  phase4_log_path;
} ngx_http_modsecurity_conf_t;


typedef ngx_int_t (*ngx_http_modsecurity_resolv_header_pt)(ngx_http_request_t *r, ngx_str_t name, off_t offset);

typedef struct {
    ngx_str_t name;
    ngx_uint_t offset;
    ngx_http_modsecurity_resolv_header_pt resolver;
} ngx_http_modsecurity_header_out_t;


extern ngx_module_t ngx_http_modsecurity_module;

/* ngx_http_modsecurity_module.c */
int ngx_http_modsecurity_process_intervention (Transaction *transaction, ngx_http_request_t *r, ngx_int_t early_log);
ngx_http_modsecurity_ctx_t *ngx_http_modsecurity_create_ctx(ngx_http_request_t *r);
ngx_http_modsecurity_ctx_t *ngx_http_modsecurity_get_module_ctx(ngx_http_request_t *r);
char *ngx_str_to_char(ngx_str_t a, ngx_pool_t *p);

typedef struct {
    const char *method;
    const char *uri;
    const char *content_type;
} ngx_http_modsecurity_event_request_metadata_t;

/* Event records retain bounded request metadata only.  Keep the established
 * empty-string fallback for absent, empty, NULL, or allocation-failure NGINX
 * values. */
static ngx_inline ngx_http_modsecurity_event_request_metadata_t
ngx_http_modsecurity_event_request_metadata(ngx_http_request_t *r)
{
    ngx_http_modsecurity_event_request_metadata_t metadata = {
        "", "", ""
    };
    char *value;

    if (r == NULL) {
        return metadata;
    }

    if (r->method_name.len > 0U) {
        value = ngx_str_to_char(r->method_name, r->pool);
        if (value != (char *)-1 && value != NULL) {
            metadata.method = value;
        }
    }
    if (r->unparsed_uri.len > 0U) {
        value = ngx_str_to_char(r->unparsed_uri, r->pool);
        if (value != (char *)-1 && value != NULL) {
            metadata.uri = value;
        }
    }
    if (r->headers_in.content_type != NULL &&
        r->headers_in.content_type->value.len > 0U) {
        value = ngx_str_to_char(r->headers_in.content_type->value, r->pool);
        if (value != (char *)-1 && value != NULL) {
            metadata.content_type = value;
        }
    }

    return metadata;
}

/* Callers retain their source-specific guards and event construction.  This
 * helper only owns the common bounded JSONL serialization and warning-only
 * write tail used by request metadata events. */
static ngx_inline int
ngx_http_modsecurity_write_event_jsonl(
    ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf,
    const msconnector_event *event,
    const char *serialization_failure_message,
    const char *write_failure_message)
{
    char line[4096];
    int json_truncated = 0;
    size_t line_length;
    ssize_t written;

    if (!msconnector_event_write_jsonl_line(event, line, sizeof(line),
        &json_truncated)) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "%s%s", serialization_failure_message,
            json_truncated ? " (truncated)" : "");
        return 0;
    }

    line_length = ngx_strlen(line);
    written = ngx_write_fd(mcf->phase4_log_file->fd, (u_char *)line,
        line_length);
    if (written < 0 || (size_t)written != line_length) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log,
            written < 0 ? ngx_errno : 0, "%s", write_failure_message);
    }

    return 1;
}

/* Phase 3/4 evidence writes are enforcement-relevant: unlike request-event
 * logging, serialization, write, and short-write failures must propagate. */
static ngx_inline ngx_int_t
ngx_http_modsecurity_write_phase_event_jsonl(
    ngx_http_request_t *r, ngx_http_modsecurity_conf_t *mcf,
    const msconnector_event *event, const char *phase)
{
    char line[4096];
    int json_truncated = 0;
    size_t line_length;
    ssize_t written;

    if (!msconnector_event_write_jsonl_line(event, line, sizeof(line),
        &json_truncated)) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity %s common event serialization failed%s", phase,
            json_truncated ? " (truncated)" : "");
        return NGX_ERROR;
    }

    line_length = ngx_strlen(line);
    written = ngx_write_fd(mcf->phase4_log_file->fd, (u_char *)line,
        line_length);
    if (written < 0) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, ngx_errno,
            "modsecurity %s log write failed", phase);
        return NGX_ERROR;
    }
    if ((size_t)written != line_length) {
        ngx_log_error(NGX_LOG_WARN, r->connection->log, 0,
            "modsecurity %s log short write: %z of %uz bytes", phase,
            written, line_length);
        return NGX_ERROR;
    }

    return NGX_OK;
}

#if !(NGX_PCRE) || (NGX_PCRE2)
#define ngx_http_modsecurity_pcre_malloc_init(x) NULL
#define ngx_http_modsecurity_pcre_malloc_done(x) (void)x
#else
ngx_pool_t *ngx_http_modsecurity_pcre_malloc_init(ngx_pool_t *pool);
void ngx_http_modsecurity_pcre_malloc_done(ngx_pool_t *old_pool);
#endif

/* ngx_http_modsecurity_body_filter.c */
ngx_int_t ngx_http_modsecurity_body_filter_init(void);
ngx_int_t ngx_http_modsecurity_body_filter(ngx_http_request_t *r, ngx_chain_t *in);

/* ngx_http_modsecurity_header_filter.c */
ngx_int_t ngx_http_modsecurity_header_filter_init(void);
ngx_int_t ngx_http_modsecurity_header_filter(ngx_http_request_t *r);
#if defined(MODSECURITY_SANITY_CHECKS) && (MODSECURITY_SANITY_CHECKS)
int ngx_http_modsecurity_store_ctx_header(ngx_http_request_t *r, ngx_str_t *name, ngx_str_t *value);
#endif

/* ngx_http_modsecurity_log.c */
void ngx_http_modsecurity_log(void *log, const void* data);
void ngx_http_modsecurity_log_rule_match_event(ngx_http_request_t *r,
    enum msconnector_phase phase, const char *rule_id);
ngx_int_t ngx_http_modsecurity_log_handler(ngx_http_request_t *r);

/* ngx_http_modsecurity_access.c */
ngx_int_t ngx_http_modsecurity_access_handler(ngx_http_request_t *r);

#endif /* _NGX_HTTP_MODSECURITY_COMMON_H_INCLUDED_ */
