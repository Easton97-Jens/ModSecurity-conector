#include "connectors/lighttpd/metadata.h"
#include "connectors/lighttpd/src/lighttpd_bridge.h"

#include <stdio.h>
#include <string.h>

static void print_status(void) {
    const msconnector_lighttpd_adapter_metadata *metadata;
    msconnector_capabilities capabilities;
    msconnector_request request;
    msconnector_lighttpd_bridge_decision decision;

    metadata = msconnector_lighttpd_adapter_metadata_get();
    capabilities = msconnector_lighttpd_bridge_starter_capabilities();
    request = msconnector_lighttpd_bridge_make_probe_request("GET", "/");
    decision = msconnector_lighttpd_bridge_evaluate_probe(&request);

    printf("connector=%s\n", metadata->origin.component);
    printf("source_kind=%s\n", metadata->source_kind);
    printf("build_status=%s\n", metadata->build_status);
    printf("runtime_status=%s\n", metadata->runtime_status);
    printf("integration_path=%s\n", metadata->integration_path);
    printf("bridge_kind=%s\n", msconnector_lighttpd_bridge_starter_kind());
    printf("capability_flags=%llu\n", (unsigned long long)capabilities.flags);
    printf("probe_decision_status=%s\n", msconnector_status_name(decision.status));
    printf("probe_decision_reason=%s\n", decision.reason);
}

int main(int argc, char **argv) {
    enum msconnector_status self_test_status;

    if (argc == 2 && strcmp(argv[1], "--self-test") == 0) {
        self_test_status = msconnector_lighttpd_bridge_self_test();
        print_status();
        printf("self_test_status=%s\n", msconnector_status_name(self_test_status));
        return self_test_status == MSCONNECTOR_STATUS_OK ? 0 : 1;
    }

    if (argc == 1 || (argc == 2 && strcmp(argv[1], "--status") == 0)) {
        print_status();
        return 0;
    }

    fprintf(stderr, "usage: %s [--status|--self-test]\n", argv[0]);
    return 2;
}
