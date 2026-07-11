#include "metadata.h"

static const msconnector_haproxy_adapter_metadata haproxy_metadata = {
    {
        "HAProxy repository SPOP agent",
        "repository-owned",
        "not applicable",
        "not applicable",
        "repository source",
        "not selected"
    },
    {
        MSCONNECTOR_CAPABILITY_CONNECTION_METADATA |
            MSCONNECTOR_CAPABILITY_REQUEST_HEADERS |
            MSCONNECTOR_CAPABILITY_REQUEST_BODY_BUFFERED |
            MSCONNECTOR_CAPABILITY_RESPONSE_HEADERS |
            MSCONNECTOR_CAPABILITY_RESPONSE_BODY_BUFFERED |
            MSCONNECTOR_CAPABILITY_AUDIT_LOG_ARTIFACTS |
            MSCONNECTOR_CAPABILITY_ERROR_LOG_ARTIFACTS |
            MSCONNECTOR_CAPABILITY_CUSTOM_TRANSACTION_ID,
        "haproxy",
        "repository-spop-agent",
        "HAProxy",
        "The real HAProxy/SPOP request path is implemented. Buffered request body, response notifications, and bounded experimental response body paths remain unasserted by the canonical no-CRS baseline."
    },
    "haproxy",
    "HAProxy",
    "repository-local-spop-agent",
    "connectors/haproxy",
    "HAProxy SPOE/SPOP notifications to a repository-owned libmodsecurity agent; starter self-tests are non-runtime",
    "implemented_not_asserted",
    "implemented_not_asserted",
    "requires_runtime_evidence"
};

msconnector_origin msconnector_haproxy_adapter_origin(void) {
    return haproxy_metadata.origin;
}

const msconnector_capabilities *msconnector_haproxy_adapter_capabilities(void) {
    return &haproxy_metadata.capabilities;
}

const msconnector_haproxy_adapter_metadata *msconnector_haproxy_adapter_metadata_get(void) {
    return &haproxy_metadata;
}
