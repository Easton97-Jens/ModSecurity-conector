#define _POSIX_C_SOURCE 200809L
/* Real Common runtime + libModSecurity response policy test. Arguments are
 * required; this executable never supplies engine policy defaults. */
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "common/runtime/msconnector_runtime.h"
#include "tests/transaction_phase_test_support.h"
#include "connectors/profile_registry.h"

#define CHECK(x) do { if (!(x)) { fprintf(stderr, "line %d: %s (%s)\n", __LINE__, #x, error.message); goto cleanup; } } while (0)
/* Configuration loading only: no response inspection and no fixture defaults. */
static int config_omission_test(const char *directory) {
    char rules[4096];
    char config[4096];
    char diagnostic[1024];
    FILE *file;
    msconnector_runtime *runtime = NULL;
    if (snprintf(rules, sizeof(rules), "%s/omitted-rules", directory) < 0 ||
        snprintf(config, sizeof(config), "%s/omitted-config", directory) < 0) return 1;
    file = fopen(rules, "w");
    if (file == NULL) return 1;
    int written = fputs("SecRuleEngine On\n", file) != EOF;
    int closed = fclose(file) == 0;
    if (!written || !closed) return 1;
    file = fopen(config, "w");
    if (file == NULL) return 1;
    written = fprintf(file, "enabled=on\nrules_file=%s\nrequest_body_mode=none\n"
            "response_body_mode=none\nphase4_mode=safe\n", rules) >= 0;
    closed = fclose(file) == 0;
    if (!written || !closed) return 1;
    if (!msconnector_runtime_create("lighttpd", config, &runtime,
            diagnostic, sizeof(diagnostic))) {
        fprintf(stderr, "config-only omission failed: %s\n", diagnostic);
        return 1;
    }
    msconnector_runtime_destroy(&runtime);
    puts("config-only omission PASS; no response inspection executed");
    return 0;
}

static int close_test_file(FILE **file) {
    FILE *owned = *file;
    *file = NULL;
    return fclose(owned) == 0;
}

static int append_test_body(msconnector_runtime_transaction *tx, size_t length,
    size_t chunk_size, size_t marker_offset, size_t *offset,
    msconnector_error *error) {
    unsigned char chunk[65536];
    while (*offset < length) {
        size_t count = length - *offset < chunk_size ? length - *offset : chunk_size;
        memset(chunk, 'x', count);
        for (size_t i = 0; i < count; ++i) {
            size_t position = *offset + i;
            if (position >= marker_offset && position - marker_offset < 6U)
                chunk[i] = (unsigned char)"MARKER"[position - marker_offset];
        }
        if (!msconnector_runtime_transaction_append_response_body_chunk(tx, chunk, count, error)) { return 0; }
        *offset += count;
    }
    return 1;
}

static int check_reject_evidence(const char *events) {
    char evidence[16384];
    FILE *file = fopen(events, "r");
    if (file == NULL) return 0;
    size_t count = fread(evidence, 1U, sizeof(evidence) - 1U, file);
    int readable = !ferror(file);
    int closed = fclose(file) == 0;
    if (!readable || !closed) return 0;
    evidence[count] = '\0';
    return strstr(evidence, "MSCONN_EVENT_BODY_LIMIT") != NULL &&
        strstr(evidence, "\"body_limit_outcome\":\"reject\"") != NULL &&
        strstr(evidence, "MSCONN_EVENT_INVALID_ENGINE_RESPONSE") == NULL;
}

int main(int argc, char **argv) {
    msconnector_error error;
    msconnector_runtime *runtime = NULL;
    msconnector_runtime_transaction *tx = NULL;
    msconnector_decision decision;
    msconnector_runtime_transaction_snapshot snapshot;
    msconnector_response response = {0};
    msconnector_header headers[] = {{"Content-Type", 12U, "text/plain", 10U}};
    char config[4096];
    char rules[4096];
    char events[4096];
    char message[1024];
    size_t limit;
    size_t length;
    size_t chunk_size;
    size_t offset = 0;
    int partial;
    int expect_marker;
    int appended;
    int finished;
    int result = 1;
    FILE *file = NULL;
    msconnector_error_init(&error);
    if (argc == 3 && strcmp(argv[1], "--config-only") == 0) {
        return config_omission_test(argv[2]);
    }
    if (argc != 8) {
        fprintf(stderr, "required: directory limit Reject|ProcessPartial off|safe|strict length chunk_size marker_offset\n");
        return 2;
    }
    limit = (size_t)strtoull(argv[2], NULL, 10);
    length = (size_t)strtoull(argv[5], NULL, 10);
    chunk_size = (size_t)strtoull(argv[6], NULL, 10);
    const size_t marker_offset = (size_t)strtoull(argv[7], NULL, 10);
    partial = strcmp(argv[3], "ProcessPartial") == 0;
    CHECK(limit > 0U && chunk_size > 0U && chunk_size <= 65536U);
    CHECK(partial || strcmp(argv[3], "Reject") == 0);
    CHECK(marker_offset <= length && length - marker_offset >= 6U);
    CHECK(snprintf(config, sizeof(config), "%s/config", argv[1]) > 0);
    CHECK(snprintf(rules, sizeof(rules), "%s/rules", argv[1]) > 0);
    CHECK(snprintf(events, sizeof(events), "%s/events", argv[1]) > 0);
    file = fopen(rules, "w"); CHECK(file != NULL);
    CHECK(fprintf(file,
        "SecRuleEngine On\nSecRequestBodyAccess Off\nSecResponseBodyAccess On\n"
        "SecResponseBodyMimeType text/plain\nSecResponseBodyLimit %zu\n"
        "SecResponseBodyLimitAction %s\n"
        /* Matching P4 pass can clear an earlier native Reject at EOS. */
        "SecAction \"id:710002,phase:4,pass,nolog\"\n"
        "SecRule RESPONSE_BODY \"@contains MARKER\" \"id:710001,phase:4,deny,status:451,log\"\n",
        limit, argv[3]) > 0);
    CHECK(close_test_file(&file));
    file = fopen(config, "w"); CHECK(file != NULL);
    CHECK(fprintf(file, "enabled=on\nrules_file=%s\nrequest_body_mode=none\n"
        "response_body_mode=streaming\nphase4_mode=%s\nevent_path=%s\n", rules, argv[4], events) > 0);
    CHECK(close_test_file(&file));
    CHECK(msconnector_runtime_create("lighttpd", config, &runtime, message, sizeof(message)) ||
          (fprintf(stderr, "%s\n", message), 0));
    CHECK(msconnector_runtime_set_event_integration_mode(runtime, "stock-lighttpd-sidecar"));
    CHECK(msconnector_runtime_set_transaction_profile(runtime, msconnector_profile_registry_find("lighttpd-stock")));
    CHECK(msconnector_test_begin_transaction(runtime, "/engine-response-limit", "real-limit-test", &tx, &decision, &error));
    response.status = 200; response.http_version = "HTTP/1.1";
    response.headers = headers; response.header_count = 1U;
    CHECK(msconnector_runtime_transaction_process_response_headers(tx, &response, &decision, &error));
    appended = append_test_body(tx, length, chunk_size, marker_offset, &offset, &error);
    expect_marker = marker_offset + 6U <= (length < limit ? length : limit);
    if (length <= limit || partial) {
        CHECK(appended && offset == length);
        finished = msconnector_runtime_transaction_finish_response_body(tx, &decision, &error);
        CHECK(finished);
        CHECK(expect_marker ? decision.intervention.status == 451 : !decision.disruptive);
        CHECK(msconnector_runtime_transaction_snapshot_get(tx, &snapshot));
        CHECK(snapshot.response_body.bytes_seen == length);
        CHECK(snapshot.response_body.bytes_inspected == length);
        CHECK(!snapshot.response_body.truncated);
        CHECK(snapshot.contract.last_completed_phase == MSCONNECTOR_PHASE_RESPONSE_BODY);
    } else {
        if (appended) {
            CHECK(msconnector_runtime_transaction_finish_response_body(tx, &decision, &error));
            CHECK(decision.disruptive && decision.intervention.status == 403);
        } else {
            /* A native negative append result remains a technical failure. */
            CHECK(error.code == MSCONNECTOR_ERROR_MODSECURITY_FAILURE);
        }
    }
    printf("engine-limit PASS limit=%zu action=%s mode=%s length=%zu chunk=%zu marker=%zu appended=%d native_status=%d\n",
        limit, argv[3], argv[4], length, chunk_size, marker_offset, appended, decision.intervention.status);
    msconnector_runtime_transaction_destroy(&tx);
    msconnector_runtime_destroy(&runtime);
    if (length > limit && !partial && appended) {
        CHECK(check_reject_evidence(events));
    }
    file = fopen(config, "a"); CHECK(file != NULL);
    CHECK(fputs("response_body_limit=128\n", file) != EOF); CHECK(close_test_file(&file));
    CHECK(!msconnector_runtime_config_check("lighttpd", config, message, sizeof(message)));
    CHECK(strstr(message, "unknown") != NULL);
    result = 0;
cleanup:
    if (file != NULL && fclose(file) != 0) result = 1;
    msconnector_runtime_transaction_destroy(&tx);
    msconnector_runtime_destroy(&runtime);
    return result;
}
