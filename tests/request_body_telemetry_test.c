#define _POSIX_C_SOURCE 200809L
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <errno.h>
#include <modsecurity/transaction.h>
#include "common/runtime/msconnector_runtime.h"
#include "connectors/profile_registry.h"

static int fault;
size_t __real_msc_get_request_body_length(Transaction *transaction);
size_t __wrap_msc_get_request_body_length(Transaction *transaction) {
    return fault == 1 ? SIZE_MAX : __real_msc_get_request_body_length(transaction);
}
int __real_msc_process_request_body(Transaction *transaction);
int __wrap_msc_process_request_body(Transaction *transaction) {
    return fault == 2 ? -1 : __real_msc_process_request_body(transaction);
}
int __real_fflush(FILE *stream);
int __wrap_fflush(FILE *stream) {
    if (fault == 3) { errno = EIO; return EOF; }
    return __real_fflush(stream);
}

int main(int argc, char **argv) {
    assert(argc == 3);
    const char *scenario = argv[2];
    const int reject = strcmp(scenario, "reject") == 0;
    const int sink_error = strcmp(scenario, "sink-error") == 0;
    const int partial = strcmp(scenario, "partial") == 0 || sink_error;
    const int disabled = strcmp(scenario, "disabled") == 0;
    char rules[4096], config[4096], events[4096], diagnostic[1024];
    assert(snprintf(rules, sizeof(rules), "%s/rules", argv[1]) > 0);
    assert(snprintf(config, sizeof(config), "%s/config", argv[1]) > 0);
    assert(snprintf(events, sizeof(events), "%s/events", argv[1]) > 0);
    FILE *file = fopen(rules, "w"); assert(file);
    assert(fprintf(file, "SecRuleEngine On\nSecRequestBodyAccess %s\n"
        "SecRequestBodyLimit %d\nSecRequestBodyNoFilesLimit %d\n"
        "SecRequestBodyLimitAction %s\n"
        "SecAction \"id:77301,phase:2,pass,nolog\"\n",
        disabled ? "Off" : "On", reject || partial ? 16 : 64,
        reject || partial ? 16 : 64, reject ? "Reject" : "ProcessPartial") > 0);
    assert(fclose(file) == 0);
    file = fopen(config, "w"); assert(file);
    assert(fprintf(file, "enabled=on\nrules_file=%s\nrequest_body_mode=streaming\n"
        "response_body_mode=none\nevent_path=%s\n", rules, events) > 0);
    assert(fclose(file) == 0);
    msconnector_runtime *runtime = NULL;
    assert(msconnector_runtime_create("traefik", config, &runtime, diagnostic, sizeof(diagnostic)));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("traefik-forwardauth")));
    msconnector_request request = {0};
    request.method = "POST"; request.uri = "/telemetry"; request.http_version = "HTTP/1.1";
    request.client.address = "127.0.0.1"; request.server.address = "127.0.0.1";
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_decision decision;
    msconnector_error error;
    msconnector_runtime_body_progress progress;
    assert(msconnector_runtime_transaction_begin_request_stream(runtime, &request,
        "telemetry", &transaction, &decision, &error));
    if (strcmp(scenario, "accessor-error") == 0) fault = 1;
    int appended = msconnector_runtime_transaction_append_request_body_chunk(transaction,
        (const unsigned char *)"abcdefgh", 8U, &error);
    if (fault == 1) {
        assert(!appended && error.code == MSCONNECTOR_ERROR_MODSECURITY_FAILURE);
        msconnector_runtime_transaction_request_body_progress(transaction, &progress);
        assert(progress.bytes_inspected == 0U && progress.bytes_retained == 0U);
    } else {
        assert(appended);
        assert(msconnector_runtime_transaction_append_request_body_chunk(transaction,
            (const unsigned char *)"ijklmnopq", 9U, &error));
        msconnector_runtime_transaction_request_body_progress(transaction, &progress);
        assert(progress.bytes_seen == 17U && progress.bytes_inspected == 0U);
        if (strcmp(scenario, "phase-error") == 0) fault = 2;
        if (sink_error) fault = 3;
        int finished = msconnector_runtime_transaction_finish_request_body(transaction, &decision, &error);
        msconnector_runtime_transaction_request_body_progress(transaction, &progress);
        if (fault == 3) {
            assert(!finished && error.code == MSCONNECTOR_ERROR_IO);
            assert(progress.finished && progress.bytes_inspected == 0U);
        } else if (fault == 2) {
            assert(!finished && error.code == MSCONNECTOR_ERROR_MODSECURITY_FAILURE);
            assert(!progress.finished && progress.bytes_inspected == 0U);
        } else {
            assert(finished && progress.finished);
            assert(progress.bytes_retained == (reject ? 8U : partial ? 16U : 17U));
            assert(progress.bytes_inspected == 0U);
            assert(progress.limit_outcome == (reject ? MSCONNECTOR_BODY_LIMIT_OUTCOME_REJECT :
                partial ? MSCONNECTOR_BODY_LIMIT_OUTCOME_PROCESS_PARTIAL : MSCONNECTOR_BODY_LIMIT_OUTCOME_NONE));
            assert((decision.disruptive != 0) == reject);
        }
    }
    fault = 0;
    msconnector_runtime_transaction_destroy(&transaction);
    msconnector_runtime_destroy(&runtime);
    file = fopen(events, "r"); assert(file);
    char evidence[16384]; size_t count = fread(evidence, 1U, sizeof(evidence)-1U, file);
    assert(!ferror(file) && fclose(file) == 0); evidence[count] = '\0';
    if (reject || partial) {
        const char *limit_event = strstr(evidence, "MSCONN_EVENT_BODY_LIMIT");
        assert(limit_event);
        assert(!strstr(limit_event + strlen("MSCONN_EVENT_BODY_LIMIT"), "MSCONN_EVENT_BODY_LIMIT"));
        assert(strstr(evidence, "\"body_bytes_inspected\":0"));
        assert(strstr(evidence, "\"body_bytes_seen\":17"));
        assert(strstr(evidence, "\"body_truncated\":true"));
        assert(strstr(evidence, reject ? "\"body_limit_outcome\":\"reject\"" :
            "\"body_limit_outcome\":\"process_partial\""));
    } else assert(!strstr(evidence, "MSCONN_EVENT_BODY_LIMIT"));
    puts("native request telemetry PASS");
    return 0;
}
