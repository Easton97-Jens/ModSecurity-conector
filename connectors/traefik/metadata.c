#include "metadata.h"

static const msconnector_traefik_adapter_metadata traefik_metadata = {
    {
        "Traefik decision-service starter",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "not documented"
    },
    {
        MSCONNECTOR_CAPABILITY_NONE,
        "traefik",
        "decision-service-starter",
        "traefik",
        "Local decision-service starter only; no Traefik API, libmodsecurity runtime, "
        "Traefik traffic handling, CRS execution, or runtime capability is verified."
    },
    "repo-owned decision-service-starter",
    "none",
    "decision-service-starter",
    "not_verified",
    "connector-gap"
};

msconnector_origin msconnector_traefik_adapter_origin(void) {
    return traefik_metadata.origin;
}

const msconnector_capabilities *msconnector_traefik_adapter_capabilities(void) {
    return &traefik_metadata.capabilities;
}

const msconnector_traefik_adapter_metadata *msconnector_traefik_adapter_metadata_get(void) {
    return &traefik_metadata;
}
