#define _POSIX_C_SOURCE 200809L
#include "lighttpd-host-observer.h"
#include <errno.h>
#include <stdlib.h>
#include <string.h>
static int unknown;
uint64_t msconnector_lifecycle_runtime_scope_call(const msconnector_runtime_transaction *transaction) {
    (void)transaction;return unknown?0:42;
}
int main(int argc,char **argv) {
    if (argc!=3 || setenv("MSCONNECTOR_LIGHTTPD_HOST_OBSERVER",argv[1],1)!=0) return 2;
    unknown=strcmp(argv[2],"unknown_scope")==0;
    const msconnector_runtime_transaction *key=(const msconnector_runtime_transaction *)(uintptr_t)0x1234;
    errno=EDOM;
    lighttpd_observe_body("stock_request_content_length_eos",key,23,23,0U,1);
    if (errno!=EDOM)return 3;
    if (strcmp(argv[2],"duplicate_eos")==0)lighttpd_observe_body("stock_request_content_length_eos",key,23,23,0U,1);
    lighttpd_observe_body("patched_response_body_hook",key,-1,0,24U,0);
    return errno==EDOM?0:4;
}
