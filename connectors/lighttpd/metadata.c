#include "metadata.h"

static const msconnector_lighttpd_adapter_metadata lighttpd_metadata = {
    {
        "lighttpd connector bridge starter",
        "not selected",
        "not selected",
        "not selected",
        "not selected",
        "no upstream source imported"
    },
    "bridge-starter",
    "connectors/lighttpd",
    "bridge-starter",
    "not-verified",
    "decision-service bridge starter; native lighttpd module and FastCGI/SCGI runtime integration deferred"
};

msconnector_origin msconnector_lighttpd_adapter_origin(void) {
    return lighttpd_metadata.origin;
}

const msconnector_lighttpd_adapter_metadata *msconnector_lighttpd_adapter_metadata_get(void) {
    return &lighttpd_metadata;
}
