#ifndef MSCONNECTOR_MODSECURITY_ENGINE_H
#define MSCONNECTOR_MODSECURITY_ENGINE_H

#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/request.h"
#include "msconnector/response.h"
#include "msconnector/transaction_state.h"

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_modsecurity_engine_ops {
    void *userdata;
    int (*init)(void *userdata, msconnector_error *error);
    void (*cleanup)(void *userdata);
    void *(*create_rules_set)(void *userdata, msconnector_error *error);
    void (*destroy_rules_set)(void *userdata, void *rules_set);
    void *(*new_transaction)(void *userdata, void *rules_set, const char *transaction_id, msconnector_error *error);
    void (*free_transaction)(void *userdata, void *transaction);
    int (*process_connection)(void *userdata, void *transaction, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
    int (*process_request_headers)(void *userdata, void *transaction, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
    int (*process_request_body)(void *userdata, void *transaction, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
    /*
     * Streaming body operations borrow ``data`` only for the duration of the
     * callback.  ``finish_*_body`` is the explicit end-of-stream boundary at
     * which libmodsecurity may perform phase-2/phase-4 evaluation.
     *
     * The older process_*_body callbacks are retained for buffered adapters.
     * A streaming adapter must provide the append/finish pair instead of
     * retaining a host-owned body buffer.
     */
    int (*append_request_body)(void *userdata, void *transaction, const unsigned char *data, size_t size, msconnector_error *error);
    int (*finish_request_body)(void *userdata, void *transaction, msconnector_decision *decision, msconnector_error *error);
    int (*process_response_headers)(void *userdata, void *transaction, const msconnector_response *response, msconnector_decision *decision, msconnector_error *error);
    int (*process_response_body)(void *userdata, void *transaction, const msconnector_response *response, msconnector_decision *decision, msconnector_error *error);
    int (*append_response_body)(void *userdata, void *transaction, const unsigned char *data, size_t size, msconnector_error *error);
    int (*finish_response_body)(void *userdata, void *transaction, msconnector_decision *decision, msconnector_error *error);
    int (*process_logging)(void *userdata, void *transaction, msconnector_error *error);
} msconnector_modsecurity_engine_ops;

typedef struct msconnector_modsecurity_engine { msconnector_modsecurity_engine_ops ops; void *rules_set; int initialized; } msconnector_modsecurity_engine;
typedef struct msconnector_modsecurity_transaction { msconnector_modsecurity_engine *engine; void *native_transaction; msconnector_transaction_state state; } msconnector_modsecurity_transaction;

void msconnector_modsecurity_engine_init(msconnector_modsecurity_engine *engine, const msconnector_modsecurity_engine_ops *ops);
int msconnector_modsecurity_engine_start(msconnector_modsecurity_engine *engine, msconnector_error *error);
void msconnector_modsecurity_engine_cleanup(msconnector_modsecurity_engine *engine);
int msconnector_modsecurity_engine_create_rules(msconnector_modsecurity_engine *engine, msconnector_error *error);
void msconnector_modsecurity_engine_destroy_rules(msconnector_modsecurity_engine *engine);
int msconnector_modsecurity_transaction_init(msconnector_modsecurity_transaction *tx, msconnector_modsecurity_engine *engine, const char *transaction_id, msconnector_error *error);
void msconnector_modsecurity_transaction_cleanup(msconnector_modsecurity_transaction *tx);
int msconnector_modsecurity_process_connection(msconnector_modsecurity_transaction *tx, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_process_request_headers(msconnector_modsecurity_transaction *tx, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_process_request_body(msconnector_modsecurity_transaction *tx, const msconnector_request *request, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_append_request_body(msconnector_modsecurity_transaction *tx, const unsigned char *data, size_t size, msconnector_error *error);
int msconnector_modsecurity_finish_request_body(msconnector_modsecurity_transaction *tx, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_process_response_headers(msconnector_modsecurity_transaction *tx, const msconnector_response *response, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_process_response_body(msconnector_modsecurity_transaction *tx, const msconnector_response *response, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_append_response_body(msconnector_modsecurity_transaction *tx, const unsigned char *data, size_t size, msconnector_error *error);
int msconnector_modsecurity_finish_response_body(msconnector_modsecurity_transaction *tx, msconnector_decision *decision, msconnector_error *error);
int msconnector_modsecurity_process_logging(msconnector_modsecurity_transaction *tx, msconnector_error *error);

#ifdef __cplusplus
}
#endif

#endif
