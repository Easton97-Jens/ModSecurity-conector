#ifndef MSCONNECTOR_TRANSACTION_ID_H
#define MSCONNECTOR_TRANSACTION_ID_H

#include "msconnector/config.h"
#include "msconnector/error.h"
#include "msconnector/request.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum msconnector_transaction_id_source {
    MSCONNECTOR_TRANSACTION_ID_SOURCE_NONE = 0,
    MSCONNECTOR_TRANSACTION_ID_SOURCE_STATIC,
    MSCONNECTOR_TRANSACTION_ID_SOURCE_EXPR,
    MSCONNECTOR_TRANSACTION_ID_SOURCE_HOST,
    MSCONNECTOR_TRANSACTION_ID_SOURCE_HEADER,
    MSCONNECTOR_TRANSACTION_ID_SOURCE_FALLBACK
} msconnector_transaction_id_source;

typedef int (*msconnector_transaction_id_expr_eval)(void *userdata, const msconnector_request *request, char *out, size_t out_len);

typedef struct msconnector_transaction_id_context {
    const msconnector_config *config;
    const msconnector_request *request;
    const char *host_request_id;
    const char *fallback_id;
    const char *header_name;
    msconnector_transaction_id_expr_eval expr_eval;
    void *expr_userdata;
} msconnector_transaction_id_context;

typedef struct msconnector_transaction_id_result { msconnector_transaction_id_source source; char value[128]; } msconnector_transaction_id_result;
int msconnector_transaction_id_validate(const char *value);
int msconnector_transaction_id_copy(const char *value, char *out, size_t out_len);
int msconnector_transaction_id_resolve(const msconnector_transaction_id_context *ctx, msconnector_transaction_id_result *out, msconnector_error *error);
const char *msconnector_transaction_id_source_name(msconnector_transaction_id_source source);

#ifdef __cplusplus
}
#endif

#endif
