#include "metadata.h"

static const msconnector_envoy_adapter_metadata envoy_metadata = {
    {
        "ModSecurity-envoy build starter",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "not selected"
    },
    {
        MSCONNECTOR_CAPABILITY_NONE,
        "envoy",
        "bridge-starter",
        "Envoy",
        "local sidecar/HTTP bridge decision self-test; no Envoy SDK, no libmodsecurity adapter, no runtime ModSecurity capabilities claimed"
    },
    "bridge-starter",
    "connectors/envoy",
    "sidecar/HTTP bridge starter; native Envoy SDK/API dependency not present in this repository",
    "bridge-starter",
    "not_verified",
    "connector-gap"
};

msconnector_origin msconnector_envoy_adapter_origin(void) {
    return envoy_metadata.origin;
}

const msconnector_envoy_adapter_metadata *msconnector_envoy_adapter_metadata_get(void) {
    return &envoy_metadata;
}
