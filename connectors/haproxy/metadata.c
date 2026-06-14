#include "metadata.h"

static const msconnector_haproxy_adapter_metadata haproxy_metadata = {
    {
        "HAProxy connector build-starter",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "not selected"
    },
    "repo-authored metadata/build-starter only",
    "connectors/haproxy",
    "spoa-agent-starter",
    "local-self-test-only",
    "not-verified"
};

msconnector_origin msconnector_haproxy_adapter_origin(void) {
    return haproxy_metadata.origin;
}

const msconnector_haproxy_adapter_metadata *msconnector_haproxy_adapter_metadata_get(void) {
    return &haproxy_metadata;
}
