#include "metadata.h"

static const msconnector_apache_adapter_metadata apache_metadata = {
    {
        "ModSecurity-apache",
        "https://github.com/owasp-modsecurity/ModSecurity-apache",
        "master",
        "0488c77f69669584324b70460614a382224b4883",
        "v0.0.9-beta1-26-g0488c77",
        "Apache-2.0"
    },
    "adapter-owned",
    "connectors/apache"
};

msconnector_origin msconnector_apache_adapter_origin(void) {
    return apache_metadata.origin;
}

const msconnector_apache_adapter_metadata *msconnector_apache_adapter_metadata_get(void) {
    return &apache_metadata;
}
