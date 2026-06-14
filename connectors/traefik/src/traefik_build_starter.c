#include "metadata.h"

#include <stdio.h>

int msconnector_traefik_build_starter_is_runtime_adapter(void) {
    return 0;
}

#ifdef MSCONNECTOR_TRAEFIK_BUILD_STARTER_MAIN
int main(void) {
    const msconnector_traefik_adapter_metadata *metadata = msconnector_traefik_adapter_metadata_get();
    const msconnector_capabilities *capabilities = msconnector_traefik_adapter_capabilities();

    printf("connector=%s\n", capabilities->connector_name);
    printf("connector_version=%s\n", capabilities->connector_version);
    printf("build_status=%s\n", metadata->build_status);
    printf("runtime_status=%s\n", metadata->runtime_status);
    printf("source_kind=%s\n", metadata->source_kind);
    printf("imported_path=%s\n", metadata->imported_path);
    printf("capability_flags=%llu\n", (unsigned long long)capabilities->flags);
    printf("runtime_adapter=%d\n", msconnector_traefik_build_starter_is_runtime_adapter());
    printf("notes=%s\n", capabilities->notes);

    return 0;
}
#endif
