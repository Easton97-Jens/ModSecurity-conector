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
        MSCONNECTOR_CAPABILITY_CONNECTION_METADATA |
            MSCONNECTOR_CAPABILITY_REQUEST_HEADERS |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "envoy",
        "ext-authz-service",
        "Envoy",
        "minimal ext_authz request-header 200/403 smoke verified; response phases, CRS, security and production remain unverified"
    },
    "envoy",
    "Envoy",
    "repository-local-ext-authz-service",
    "connectors/envoy",
    "Envoy HTTP ext_authz service over connector-neutral common/runtime; request phase only",
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
