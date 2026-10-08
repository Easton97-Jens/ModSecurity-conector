/* Attempt-local input fault: mutate only the own nobody worker's exact
 * transaction/URI at the real exported Common validation boundary. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include "msconnector/request_mapper_contract.h"

typedef void *(*new_transaction_fn)(void *, void *, char *, void *);
typedef int (*validate_fn)(const msconnector_request_mapper_contract *, const msconnector_request *, char *, size_t);
static pid_t owned_master;
static char selected_case[64], selected_uri[128], selected_transaction[33];
static int ledger = -1, active_transaction, triggered;

static int owned_worker(void)
{
    return getuid() == 65534 && owned_master > 0 && getppid() == owned_master;
}

__attribute__((constructor)) static void bind_owned_invocation(void)
{
    const char *mode = getenv("MSCONNECTOR_OWNED_INPUT_FAULT");
    const char *transaction = getenv("MSCONNECTOR_OWNED_INPUT_TXID");
    const char *path = getenv("MSCONNECTOR_OWNED_INPUT_LEDGER");
    struct stat info;
    if (getuid() != 0 || mode == NULL || transaction == NULL || path == NULL) { return; }
    if (strcmp(mode, "body_size_nonzero_with_null_data") != 0 &&
        strcmp(mode, "header_count_nonzero_with_null_headers") != 0) { return; }
    if (strlen(transaction) != 32U || strspn(transaction, "0123456789abcdef") != 32U ||
        strncmp(path, "/var/tmp/codex/ModSecurity-conector/", sizeof("/var/tmp/codex/ModSecurity-conector/") - 1U) != 0) { return; }
    ledger = open(path, O_WRONLY | O_APPEND | O_NOFOLLOW | O_CLOEXEC);
    if (ledger < 0 || fstat(ledger, &info) != 0 || !S_ISREG(info.st_mode) ||
        info.st_uid != 0 || (info.st_mode & 0777) != 0600 || info.st_size != 0) {
        if (ledger >= 0) { close(ledger); }
        ledger = -1;
        return;
    }
    owned_master = getpid();
    (void)snprintf(selected_case, sizeof(selected_case), "%s", mode);
    (void)snprintf(selected_uri, sizeof(selected_uri), "/no-crs/input-fault/%s", mode);
    memcpy(selected_transaction, transaction, sizeof(selected_transaction));
}

void *msc_new_transaction_with_id(void *engine, void *rules, char *id, void *opaque)
{
    new_transaction_fn original;
    *(void **)(&original) = dlsym(RTLD_NEXT, "msc_new_transaction_with_id");
    if (original == NULL) { _exit(126); }
    active_transaction = owned_worker() && ledger >= 0 && id != NULL &&
        strcmp(id, selected_transaction) == 0;
    return original(engine, rules, id, opaque);
}

int msconnector_request_mapper_validate_output(const msconnector_request_mapper_contract *contract,
        const msconnector_request *request, char *error, size_t error_len)
{
    validate_fn original;
    *(void **)(&original) = dlsym(RTLD_NEXT, "msconnector_request_mapper_validate_output");
    if (original == NULL) { _exit(126); }
    if (!triggered && active_transaction && owned_worker() && request != NULL &&
        request->uri != NULL && request->method != NULL && strcmp(request->method, "POST") == 0 &&
        strcmp(request->uri, selected_uri) == 0) {
        msconnector_request injected = *request;
        int body = strcmp(selected_case, "body_size_nonzero_with_null_data") == 0;
        const char *diagnostic = body ? "missing body data" : "missing headers";
        char line[768];
        int result, size;
        triggered = 1;
        if (body) { injected.body.data = NULL; injected.body.size = 1U; }
        else { injected.headers = NULL; injected.header_count = 1U; }
        result = original(contract, &injected, error, error_len);
        size = snprintf(line, sizeof(line),
            "{\"case_id\":\"%s\",\"transaction_id\":\"%s\",\"pid\":%ld,\"ppid\":%ld,\"uid\":%ld,"
            "\"validator_return\":%d,\"diagnostic_match\":%s,\"body_size\":%zu,\"body_data_null\":%s,"
            "\"header_count\":%zu,\"headers_null\":%s}\n",
            selected_case, selected_transaction, (long)getpid(), (long)getppid(), (long)getuid(), result,
            error != NULL && error_len > 0U && strncmp(error, diagnostic, error_len) == 0 ? "true" : "false",
            injected.body.size, injected.body.data == NULL ? "true" : "false",
            injected.header_count, injected.headers == NULL ? "true" : "false");
        if (size <= 0 || (size_t)size >= sizeof(line) || write(ledger, line, (size_t)size) != size) { _exit(125); }
        return result;
    }
    return original(contract, request, error, error_len);
}
