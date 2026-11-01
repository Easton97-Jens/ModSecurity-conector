#include "haproxy_spoa_agent_starter.h"

#include <stdio.h>
#include <string.h>

static void print_usage(const char *program) {
    fprintf(stderr, "usage: %s --describe\n", program);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--describe") == 0) {
        printf("%s\n", haproxy_spoa_agent_starter_description());
        printf("limitations: %s\n", haproxy_spoa_agent_starter_limitations());
        return 0;
    }

    print_usage(argv[0]);
    return 2;
}
