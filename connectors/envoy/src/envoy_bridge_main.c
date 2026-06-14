#include "envoy_bridge.h"
#include "connectors/envoy/metadata.h"

#include <stdio.h>
#include <string.h>

static int print_self_test_result(void) {
    int rc = msconnector_envoy_bridge_self_test();
    const msconnector_envoy_adapter_metadata *metadata =
        msconnector_envoy_adapter_metadata_get();

    if (rc == 0) {
        printf("envoy_bridge_self_test: pass connector=%s mode=bridge-starter runtime=not-verified\n",
            metadata->capabilities.connector_name);
        return 0;
    }
    printf("envoy_bridge_self_test: fail connector=%s mode=bridge-starter runtime=not-verified\n",
        metadata->capabilities.connector_name);
    return 1;
}

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --self-test\n", program);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--self-test") == 0) {
        return print_self_test_result();
    }
    print_usage(argc > 0 ? argv[0] : "envoy_bridge");
    return 2;
}
