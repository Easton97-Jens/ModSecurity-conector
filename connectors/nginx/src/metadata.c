#include "metadata.h"

static const msconnector_nginx_adapter_metadata nginx_metadata = {
    {
        "ModSecurity-nginx",
        "https://github.com/owasp-modsecurity/ModSecurity-nginx",
        "master",
        "9eb44fd9ab0988756e1ab8ce5aa5548ddbe57846",
        "v1.0.4-14-g9eb44fd",
        "Apache-2.0"
    },
    "adapter-owned",
    "connectors/nginx/src"
};

msconnector_origin msconnector_nginx_adapter_origin(void) {
    return nginx_metadata.origin;
}

const msconnector_nginx_adapter_metadata *msconnector_nginx_adapter_metadata_get(void) {
    return &nginx_metadata;
}
