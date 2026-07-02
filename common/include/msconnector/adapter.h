#ifndef MSCONNECTOR_ADAPTER_H
#define MSCONNECTOR_ADAPTER_H

#include "msconnector/adapter_metadata.h"
#include "msconnector/capabilities.h"
#include "msconnector/config.h"
#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/transaction.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_adapter {
    const msconnector_adapter_metadata *(*metadata)(void *userdata);
    const msconnector_capabilities *(*capabilities)(void *userdata);
    int (*init)(void *userdata, const msconnector_config *config, msconnector_error *error);
    void (*cleanup)(void *userdata);
    int (*process_connection)(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error);
    int (*process_request_headers)(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error);
    int (*process_request_body)(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error);
    int (*process_response_headers)(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error);
    int (*process_response_body)(void *userdata, msconnector_transaction_view *tx, msconnector_decision *decision, msconnector_error *error);
    int (*finish)(void *userdata, msconnector_transaction_view *tx, msconnector_error *error);
    void *userdata;
} msconnector_adapter;

void msconnector_adapter_init(msconnector_adapter *adapter);
int msconnector_adapter_has_metadata(const msconnector_adapter *adapter);
int msconnector_adapter_has_capabilities(const msconnector_adapter *adapter);
int msconnector_adapter_supports_phase(const msconnector_adapter *adapter, enum msconnector_phase phase);

#ifdef __cplusplus
}
#endif

#endif
