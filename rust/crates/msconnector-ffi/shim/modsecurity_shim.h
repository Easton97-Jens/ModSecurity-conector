#pragma once
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct MsShimEngine MsShimEngine;
typedef struct MsShimRules MsShimRules;
typedef struct MsShimTransaction MsShimTransaction;

MsShimEngine *msc_shim_engine_new(void);
void msc_shim_engine_free(MsShimEngine *engine);
MsShimRules *msc_shim_rules_load(MsShimEngine *engine, const char *path, char *error, size_t error_len);
void msc_shim_rules_free(MsShimRules *rules);
MsShimTransaction *msc_shim_transaction_new(MsShimEngine *engine, MsShimRules *rules);
void msc_shim_transaction_free(MsShimTransaction *transaction);
int msc_shim_process_connection(MsShimTransaction *transaction, const char *client_ip);
int msc_shim_process_request_headers(MsShimTransaction *transaction);
int msc_shim_append_request_body(MsShimTransaction *transaction, const uint8_t *data, size_t len);
int msc_shim_finish_request_body(MsShimTransaction *transaction);
int msc_shim_process_response_headers(MsShimTransaction *transaction, int status);
int msc_shim_append_response_body(MsShimTransaction *transaction, const uint8_t *data, size_t len);
int msc_shim_finish_response_body(MsShimTransaction *transaction);
int msc_shim_process_logging(MsShimTransaction *transaction);
int msc_shim_disruptive_status(MsShimTransaction *transaction);

#ifdef __cplusplus
}
#endif
