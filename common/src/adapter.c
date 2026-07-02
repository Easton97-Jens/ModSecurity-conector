#include "msconnector/adapter.h"

void msconnector_adapter_init(msconnector_adapter *adapter) {
    if (adapter == 0) { return; }
    adapter->metadata = 0; adapter->capabilities = 0; adapter->init = 0; adapter->cleanup = 0;
    adapter->process_connection = 0; adapter->process_request_headers = 0; adapter->process_request_body = 0;
    adapter->process_response_headers = 0; adapter->process_response_body = 0; adapter->finish = 0; adapter->userdata = 0;
}

int msconnector_adapter_has_metadata(const msconnector_adapter *adapter) { return adapter != 0 && adapter->metadata != 0; }
int msconnector_adapter_has_capabilities(const msconnector_adapter *adapter) { return adapter != 0 && adapter->capabilities != 0; }

int msconnector_adapter_supports_phase(const msconnector_adapter *adapter, enum msconnector_phase phase) {
    if (adapter == 0) { return 0; }
    switch (phase) {
    case MSCONNECTOR_PHASE_CONNECTION: return adapter->process_connection != 0;
    case MSCONNECTOR_PHASE_REQUEST_HEADERS: return adapter->process_request_headers != 0;
    case MSCONNECTOR_PHASE_REQUEST_BODY: return adapter->process_request_body != 0;
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS: return adapter->process_response_headers != 0;
    case MSCONNECTOR_PHASE_RESPONSE_BODY: return adapter->process_response_body != 0;
    case MSCONNECTOR_PHASE_LOGGING: return adapter->finish != 0;
    case MSCONNECTOR_PHASE_URI: return 0;
    default: return 0;
    }
}
