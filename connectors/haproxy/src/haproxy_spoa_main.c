#include "haproxy_spoa_agent_starter.h"

#include <stdio.h>
#include <string.h>

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe|--self-test\n", program);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("%s\n", haproxy_spoa_agent_starter_description());
        printf("limitations: %s\n", haproxy_spoa_agent_starter_limitations());
        return 0;
    }

    if (argc == 2 && strcmp(argv[1], "--self-test") == 0) {
        int rc = haproxy_spoa_agent_starter_self_test();
        if (rc == 0) {
            printf("haproxy_spoa_agent_starter_self_test: PASS\n");
            printf("scope: local decision logic only; no HAProxy runtime, no SPOP protocol, no libmodsecurity\n");
            return 0;
        }
        printf("haproxy_spoa_agent_starter_self_test: FAIL\n");
        return 1;
    }

    print_usage(argv[0]);
    return 2;
}
