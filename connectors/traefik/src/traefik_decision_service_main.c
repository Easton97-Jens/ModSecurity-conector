#include "metadata.h"
#include "traefik_decision_service.h"

#include "msconnector/status.h"

#include <stdio.h>
#include <string.h>

static int print_decision(const char *uri) {
    const msconnector_request request = {
        "GET",
        uri,
        "HTTP/1.1",
        "example.test",
        {"127.0.0.1", 12345},
        {"127.0.0.1", 8080},
        0,
        0,
        {0, 0}
    };
    const msconnector_traefik_adapter_metadata *metadata = msconnector_traefik_adapter_metadata_get();
    msconnector_traefik_decision_result result = msconnector_traefik_decide_request(&request);

    printf("connector=%s\n", metadata->capabilities.connector_name);
    printf("starter=decision-service-starter\n");
    printf("runtime_status=%s\n", metadata->runtime_status);
    printf("uri=%s\n", uri);
    printf("decision_status=%s\n", msconnector_status_name(result.status));
    printf("disruptive=%d\n", result.intervention.disruptive);
    printf("http_status=%d\n", result.intervention.status);
    printf("reason=%s\n", result.reason);
    return 0;
}

int main(int argc, char **argv) {
    if (argc > 1 && strcmp(argv[1], "--self-test") == 0) {
        int rc = msconnector_traefik_decision_service_self_test();
        printf("traefik_decision_service_self_test=%s\n", rc == 0 ? "pass" : "fail");
        return rc;
    }

    if (argc > 2 && strcmp(argv[1], "--decide-uri") == 0) {
        return print_decision(argv[2]);
    }

    printf("usage: %s --self-test | --decide-uri <uri>\n", argv[0]);
    printf("note: local decision-service starter only; no Traefik runtime or libmodsecurity execution.\n");
    return 2;
}
