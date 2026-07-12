#include "metadata.h"

static const msconnector_lighttpd_adapter_metadata lighttpd_metadata = {
    {
        "lighttpd native ModSecurity connector module",
        "repository-owned",
        "not applicable",
        "not applicable",
        "native module source",
        "not separately declared"
    },
    {
        MSCONNECTOR_CAPABILITY_CONNECTION_METADATA |
            MSCONNECTOR_CAPABILITY_REQUEST_HEADERS |
            MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "lighttpd",
        "minimal-runtime-smoke",
        "lighttpd",
        "The stock native Phase-1 request-header path has a real-host smoke producer. Response-header Phase 3 is implemented but not asserted. A separately patched 1.4.84 core/module pair has non-promoted borrowed request and HTTP/1 identity entity-response source hooks; its Phase-4 runtime evidence remains unverified."
    },
    "lighttpd",
    "lighttpd",
    "repository-local-native-module",
    "connectors/lighttpd",
    "native lighttpd plugin with request/response header mapping and Phase-1 deny; stock body modes disabled, with separately patched non-promoted HTTP/1 identity entity-body hooks",
    "link_verified",
    "minimal_runtime_smoke",
    "partial_runtime_path"
};

msconnector_origin msconnector_lighttpd_adapter_origin(void) {
    return lighttpd_metadata.origin;
}

const msconnector_lighttpd_adapter_metadata *msconnector_lighttpd_adapter_metadata_get(void) {
    return &lighttpd_metadata;
}
