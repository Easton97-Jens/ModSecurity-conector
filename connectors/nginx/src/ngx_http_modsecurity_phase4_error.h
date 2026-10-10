/* Internal NGINX Phase-4 failure-state helpers. No host policy is added to
 * Common: NGINX retains ownership of filter re-entry and error generation. */
#ifndef NGX_HTTP_MODSECURITY_PHASE4_ERROR_H
#define NGX_HTTP_MODSECURITY_PHASE4_ERROR_H

/* NGX_DECLINED permits only the synchronous core error response. A later
 * callback, including a NULL-input flush, cannot release the failed chain. */
static ngx_inline ngx_int_t
ngx_http_modsecurity_phase4_error_gate(ngx_http_request_t *r,
    const ngx_http_modsecurity_ctx_t *ctx)
{
    if (ctx->phase4_strict_abort) {
        return NGX_ERROR;
    }
    if (ctx->phase4_processed &&
        ctx->contract.error_class != MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        return ctx->phase4_terminal_error_emitting && r->filter_finalize
            ? NGX_DECLINED : NGX_ERROR;
    }
    return NGX_OK;
}

/* Claim the one emission before calling core: core may synchronously invoke
 * these same filters. Revocation after the call is independent of its result.
 * This records an attempt, not successful client-visible delivery. */
static ngx_inline ngx_int_t
ngx_http_modsecurity_phase4_send_terminal_error(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_int_t status)
{
    ngx_int_t result;

    if (r->header_sent) {
        r->connection->error = 1;
        return NGX_ERROR;
    }
    if (ctx->phase4_terminal_error_started) {
        return NGX_ERROR;
    }
    ctx->phase4_terminal_error_started = 1;
    ctx->phase4_terminal_error_emitting = 1;
    result = ngx_http_filter_finalize_request(r, &ngx_http_modsecurity_module,
        status);
    ctx->phase4_terminal_error_emitting = 0;
    return result;
}

/* A failed enforcement-relevant log write must not turn the next callback
 * into a successful Safe-mode bypass. Never overwrite an earlier cause or
 * recursively try to describe the failed sink through that same sink. */
static ngx_inline ngx_int_t
ngx_http_modsecurity_phase4_event_write_result(ngx_http_request_t *r,
    ngx_http_modsecurity_ctx_t *ctx, ngx_int_t result)
{
    if (result == NGX_OK) {
        return NGX_OK;
    }
    if (ctx != NULL) {
        if (ctx->contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE) {
            (void)msconnector_transaction_contract_fail(&ctx->contract,
                MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, 0U);
        }
        ctx->phase4_processed = 1;
        ctx->intervention_triggered = 1;
    }
    if (r->header_sent) {
        r->connection->error = 1;
    }
    return NGX_ERROR;
}

#endif
