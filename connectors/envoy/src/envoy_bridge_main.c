#include "connectors/envoy/metadata.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        const msconnector_envoy_adapter_metadata *metadata =
            msconnector_envoy_adapter_metadata_get();
        printf("connector=%s mode=bridge-starter runtime=%s\n",
            metadata->capabilities.connector_name, metadata->runtime_status);
        return 0;
    }
    fprintf(stderr, "usage: %s --describe\n", argc > 0 ? argv[0] : "envoy_bridge");
    return 2;
}
