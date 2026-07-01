#include "msconnector/transaction_id.h"
#include "msconnector/headers.h"
#include <ctype.h>
#include <string.h>

static int fail_error(msconnector_error *error, msconnector_error_code code, const char *message) { msconnector_error_set(error, code, message, "transaction_id"); return 0; }
int msconnector_transaction_id_validate(const char *value) {
    size_t len;
    if (value == 0) { return 0; }
    len = strlen(value);
    if (len == 0 || len >= sizeof(((msconnector_transaction_id_result *)0)->value)) { return 0; }
    if (isspace((unsigned char)value[0]) || isspace((unsigned char)value[len - 1U])) { return 0; }
    for (size_t index = 0; index < len; ++index) { unsigned char ch = (unsigned char)value[index]; if (ch < 32U || ch == 127U) { return 0; } }
    return 1;
}
int msconnector_transaction_id_copy(const char *value, char *out, size_t out_len) {
    size_t len;
    if (!msconnector_transaction_id_validate(value) || out == 0 || out_len == 0) { return 0; }
    len = strlen(value); if (len >= out_len) { out[0] = '\0'; return 0; }
    memcpy(out, value, len + 1U); return 1;
}
static int use_value(msconnector_transaction_id_result *out, msconnector_transaction_id_source source, const char *value, msconnector_error *error) {
    if (!msconnector_transaction_id_copy(value, out->value, sizeof(out->value))) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid transaction id"); }
    out->source = source; return 1;
}
int msconnector_transaction_id_resolve(const msconnector_transaction_id_context *ctx, msconnector_transaction_id_result *out, msconnector_error *error) {
    if (out == 0 || ctx == 0) { return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "transaction id context is required"); }
    out->source = MSCONNECTOR_TRANSACTION_ID_SOURCE_NONE; out->value[0] = '\0';
    if (ctx->config != 0 && ctx->config->transaction_id != 0) { return use_value(out, MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC, ctx->config->transaction_id, error); }
    if (ctx->config != 0 && ctx->config->transaction_id_expr != 0) {
        if (ctx->expr_eval == 0) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "transaction id expression callback is required"); }
        if (!ctx->expr_eval(ctx->expr_userdata, ctx->request, out->value, sizeof(out->value))) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "transaction id expression failed"); }
        if (!msconnector_transaction_id_validate(out->value)) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "invalid transaction id expression result"); }
        out->source = MSCONNECTOR_TRANSACTION_ID_SOURCE_EXPR; return 1;
    }
    if (ctx->host_request_id != 0) { return use_value(out, MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST, ctx->host_request_id, error); }
    if (ctx->header_name != 0 && ctx->request != 0) { const char *value = msconnector_headers_find_value(ctx->request->headers, ctx->request->header_count, ctx->header_name); if (value != 0) { return use_value(out, MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER, value, error); } }
    if (ctx->fallback_id != 0) { return use_value(out, MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK, ctx->fallback_id, error); }
    return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "no transaction id source available");
}
const char *msconnector_transaction_id_source_name(msconnector_transaction_id_source source) {
    switch (source) {
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_NONE: return "none";
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC: return "static";
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_EXPR: return "expr";
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST: return "host";
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER: return "header";
    case MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK: return "fallback";
    default: return "none";
    }
}
