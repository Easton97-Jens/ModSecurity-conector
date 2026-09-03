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
            MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "traefik",
        "minimal-runtime-smoke",
        "traefik",
        "The forwardAuth request path maps headers and the checked-in middleware "
        "enables bounded buffered P2 forwarding. The required private-UDS "
        "response observer supplies the logical connector's P3/P4; direct "
        "forwardAuth alone does not observe upstream responses."
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
