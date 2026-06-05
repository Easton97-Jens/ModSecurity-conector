#include "haproxy_modsecurity_binding.h"

#include <stdio.h>
#include <string.h>

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe|--self-test\n", program);
}

int main(int argc, char **argv) {
    haproxy_modsecurity_decision decision;
    int rc;

    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("%s\n", haproxy_modsecurity_binding_scope());
        printf("limitations: no HAProxy runtime enforcement, no CRS, no RESPONSE_BODY verification\n");
        return 0;
    }
    if (argc != 2 || strcmp(argv[1], "--self-test") != 0) {
        print_usage(argv[0]);
        return 2;
    }

    rc = haproxy_modsecurity_phase1_header_self_test(&decision);
    if (rc == 0) {
        printf("haproxy_modsecurity_binding_self_test: PASS\n");
        printf("modsecurity_binding_status: self-test-verified\n");
        printf("runtime_verified: false\n");
        printf("runtime_status: blocked\n");
        printf("response_body_verified: false\n");
        printf("crs_verified: false\n");
        printf("decision_status: %d\n", decision.status);
        printf("decision_disruptive: %d\n", decision.disruptive);
        return 0;
    }

    printf("haproxy_modsecurity_binding_self_test: BLOCKED\n");
    printf("modsecurity_binding_status: blocked\n");
    printf("runtime_verified: false\n");
    printf("runtime_status: blocked\n");
    printf("response_body_verified: false\n");
    printf("crs_verified: false\n");
    if (decision.log_message[0] != '\0') {
        printf("reason: %s\n", decision.log_message);
    } else {
        printf("reason: modsecurity binding missing or not buildable\n");
    }
    return 77;
}
