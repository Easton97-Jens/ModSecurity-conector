#include "metadata.h"

static const msconnector_envoy_adapter_metadata envoy_metadata = {
    {
        "ModSecurity Envoy ext_authz connector",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "not selected"
    },
    {
        MSCONNECTOR_CAPABILITY_REQUEST_HEADERS |
            MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "envoy",
        "ext-authz-service",
        "Envoy",
        "The request-header path is implemented; buffered request-body forwarding is configured but not exercised. Original downstream connection metadata and upstream response phases are not available through the current service path."
    },
    "envoy",
    "Envoy",
    "repository-local-ext-authz-service",
    "connectors/envoy",
    "Envoy HTTP ext_authz service over connector-neutral common/runtime; pre-upstream request phases only",
    "compile_verified",
    "minimal_runtime_smoke",
    "connector-gap"
};

msconnector_origin msconnector_envoy_adapter_origin(void) {
    return envoy_metadata.origin;
}

const msconnector_envoy_adapter_metadata *msconnector_envoy_adapter_metadata_get(void) {
    return &envoy_metadata;
}
