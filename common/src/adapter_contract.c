#include "msconnector/adapter_contract.h"

static void set_result(msconnector_adapter_contract_result *result, int ok, const char *message) {
    if (result != 0) { result->ok = ok; result->message = message; }
}

static int has_flag(const msconnector_capabilities *capabilities, enum msconnector_capability_flag flag) {
    return capabilities != 0 && (capabilities->flags & (msconnector_capability_flags)flag) != 0;
}

static int validate_phase_callbacks(const msconnector_adapter *adapter, const msconnector_capabilities *capabilities, msconnector_adapter_contract_result *result) {
    if (has_flag(capabilities, MSCONNECTOR_CAPABILITY_CONNECTION_METADATA) && adapter->process_connection == 0) {
        set_result(result, 0, "connection capability requires process_connection");
        return 0;
    }
    if (has_flag(capabilities, MSCONNECTOR_CAPABILITY_REQUEST_HEADERS) && adapter->process_request_headers == 0) {
        set_result(result, 0, "request headers capability requires process_request_headers");
        return 0;
    }
    if ((has_flag(capabilities, MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED) || has_flag(capabilities, MSCONNECTOR_CAPABILITY_REQUEST_BODY_STREAMING)) && adapter->process_request_body == 0) {
        set_result(result, 0, "request body capability requires process_request_body");
        return 0;
    }
    if (has_flag(capabilities, MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS) && adapter->process_response_headers == 0) {
        set_result(result, 0, "response headers capability requires process_response_headers");
        return 0;
    }
    if ((has_flag(capabilities, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED) || has_flag(capabilities, MSCONNECTOR_CAPABILITY_RESPONSE_BODY_STREAMING)) && adapter->process_response_body == 0) {
        set_result(result, 0, "response body capability requires process_response_body");
        return 0;
    }
    return 1;
}

void msconnector_adapter_contract_result_init(msconnector_adapter_contract_result *result) { set_result(result, 0, "not checked"); }

int msconnector_adapter_contract_validate(const msconnector_adapter *adapter, msconnector_adapter_contract_result *result) {
    const msconnector_adapter_metadata *metadata;
    const msconnector_capabilities *capabilities;
    if (adapter == 0) { set_result(result, 0, "adapter is required"); return 0; }
    if (adapter->metadata == 0) { set_result(result, 0, "metadata callback is required"); return 0; }
    if (adapter->capabilities == 0) { set_result(result, 0, "capabilities callback is required"); return 0; }
    metadata = adapter->metadata(adapter->userdata);
    capabilities = adapter->capabilities(adapter->userdata);
    if (!msconnector_adapter_metadata_is_complete(metadata)) { set_result(result, 0, "metadata is incomplete"); return 0; }
    if (capabilities == 0 || capabilities->connector_name == 0 || capabilities->connector_name[0] == '\0') { set_result(result, 0, "capabilities are incomplete"); return 0; }
    if (!validate_phase_callbacks(adapter, capabilities, result)) { return 0; }
    set_result(result, 1, "adapter contract ok"); return 1;
}
