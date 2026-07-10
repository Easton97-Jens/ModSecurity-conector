#include "connectors/lighttpd/metadata.h"
#include "msconnector/status.h"

#include <stdio.h>
#include <string.h>

const char *msconnector_lighttpd_build_starter_status(void) {
    return "native module build is available through build-lighttpd-connector";
}

enum msconnector_status msconnector_lighttpd_runtime_status(void) {
    return MSCONNECTOR_STATUS_OK;
}

#ifdef MSCONNECTOR_LIGHTTPD_BUILD_STARTER_MAIN
int main(void) {
    const msconnector_lighttpd_adapter_metadata *metadata;

    metadata = msconnector_lighttpd_adapter_metadata_get();
    if (metadata == 0) {
        return 1;
    }
    if (strcmp(metadata->source_kind, "repository-local-native-module") != 0) {
        return 1;
    }
    if (strcmp(metadata->runtime_status, "minimal_runtime_smoke") != 0) {
        return 1;
    }

    printf("connector=%s\n", metadata->origin.component);
    printf("build_status=%s\n", metadata->build_status);
    printf("runtime_status=%s\n", metadata->runtime_status);
    printf("integration_path=%s\n", metadata->integration_path);
    printf("starter_status=%s\n", msconnector_lighttpd_build_starter_status());
    printf("runtime_status_code=%s\n", msconnector_status_name(msconnector_lighttpd_runtime_status()));
    return 0;
}
#endif
