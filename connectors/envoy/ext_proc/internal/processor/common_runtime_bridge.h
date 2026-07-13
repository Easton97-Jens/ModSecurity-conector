#ifndef MSCONNECTOR_ENVOY_EXT_PROC_COMMON_RUNTIME_BRIDGE_H
#define MSCONNECTOR_ENVOY_EXT_PROC_COMMON_RUNTIME_BRIDGE_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msc_envoy_ext_proc_runtime msc_envoy_ext_proc_runtime;
typedef struct msc_envoy_ext_proc_transaction msc_envoy_ext_proc_transaction;

typedef struct msc_envoy_ext_proc_header {
    const char *name;
    size_t name_size;
    const char *value;
    size_t value_size;
} msc_envoy_ext_proc_header;

typedef struct msc_envoy_ext_proc_request {
    const char *method;
    const char *uri;
    const char *protocol;
    const char *hostname;
    const char *client_address;
    int client_port;
    const char *server_address;
    int server_port;
    const char *transaction_id;
    const msc_envoy_ext_proc_header *headers;
    size_t header_count;
} msc_envoy_ext_proc_request;

typedef struct msc_envoy_ext_proc_response {
    int status;
    const char *protocol;
    const msc_envoy_ext_proc_header *headers;
    size_t header_count;
} msc_envoy_ext_proc_response;

enum msc_envoy_ext_proc_action {
    MSC_ENVOY_EXT_PROC_ALLOW = 0,
    MSC_ENVOY_EXT_PROC_DENY = 1,
    MSC_ENVOY_EXT_PROC_REDIRECT = 2,
    MSC_ENVOY_EXT_PROC_LOG_ONLY = 3
};

/*
 * This intentionally contains only decision metadata. It never carries a
 * request/response body or a rule message, so adapter diagnostics cannot turn
 * into a payload-bearing parallel event stream.
 */
typedef struct msc_envoy_ext_proc_decision {
    int action;
    int status;
    int phase;
    int disruptive;
    char transaction_id[129];
    char rule_id[129];
    char redirect_url[2049];
} msc_envoy_ext_proc_decision;

int msc_envoy_ext_proc_runtime_create(
    const char *config_path,
    msc_envoy_ext_proc_runtime **out,
    char *error,
    size_t error_len);

void msc_envoy_ext_proc_runtime_destroy(msc_envoy_ext_proc_runtime **runtime);

int msc_envoy_ext_proc_transaction_begin(
    msc_envoy_ext_proc_runtime *runtime,
    const msc_envoy_ext_proc_request *request,
    int end_of_stream,
    msc_envoy_ext_proc_transaction **out,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len);

int msc_envoy_ext_proc_transaction_process_response_headers(
    msc_envoy_ext_proc_transaction *transaction,
    const msc_envoy_ext_proc_response *response,
    int end_of_stream,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len);

int msc_envoy_ext_proc_transaction_process_body(
    msc_envoy_ext_proc_transaction *transaction,
    int response_direction,
    const unsigned char *body,
    size_t body_size,
    int end_of_stream,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len);

void msc_envoy_ext_proc_transaction_mark_response_committed(
    msc_envoy_ext_proc_transaction *transaction,
    int body_started);

int msc_envoy_ext_proc_transaction_record_host_action(
    msc_envoy_ext_proc_transaction *transaction,
    int action,
    int visible_status,
    const char *transport_result,
    char *error,
    size_t error_len);

const char *msc_envoy_ext_proc_transaction_id(
    const msc_envoy_ext_proc_transaction *transaction);

void msc_envoy_ext_proc_transaction_close(
    msc_envoy_ext_proc_transaction *transaction);

#ifdef __cplusplus
}
#endif

#endif
