#include "metadata.h"

static const msconnector_traefik_adapter_metadata traefik_metadata = {
    {
        "Traefik forwardAuth connector source",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "not documented"
    },
    {
        MSCONNECTOR_CAPABILITY_REQUEST_HEADERS |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "traefik",
        "minimal-runtime-smoke",
        "traefik",
        "The forwardAuth request-header path is implemented. Traefik supports "
        "buffered body forwarding, but the checked-in path does not enable it; "
        "upstream response phases remain outside this host model."
    },
    "traefik",
    "Traefik",
    "repo-owned forwardAuth-service-source",
    "none",
    "external HTTP forwardAuth authorization service; request phase only",
    "link_verified",
    "minimal_runtime_smoke",
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
