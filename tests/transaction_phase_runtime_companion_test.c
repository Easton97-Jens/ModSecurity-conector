#define _POSIX_C_SOURCE 200809L

#include <assert.h>
#include <pthread.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>

#include "common/runtime/msconnector_runtime.h"
#include "connectors/profile_registry.h"
#include "tests/transaction_phase_test_support.h"

typedef struct companion_worker {
    msconnector_runtime_response_companion_registry *registry;
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
    int result;
} companion_worker;

#define TEST_PATH_SIZE 4096U

static char test_private_root[TEST_PATH_SIZE];

static const char *test_private_directory(void)
{
    struct stat directory_stat;

    if (test_private_root[0] == '\0') {
        const char *tmpdir = ".";
        assert(snprintf(test_private_root, sizeof(test_private_root),
            "%s/msconnector-transaction-companion-XXXXXX", tmpdir) > 0);
        assert(mkdtemp(test_private_root) != NULL);
        assert(stat(test_private_root, &directory_stat) == 0);
        assert(directory_stat.st_uid == geteuid());
        assert((directory_stat.st_mode & 0777U) == 0700U);
    }
    return test_private_root;
}

static void create_runtime_fixture(char config_path[TEST_PATH_SIZE],
    char event_path[TEST_PATH_SIZE], char rules_path[TEST_PATH_SIZE],
    const char *rules_text, const char *request_body_mode,
    const char *phase4_mode) {
    const char *directory = test_private_directory();
    FILE *config;
    FILE *rules;
    int config_fd;
    int event_fd;
    int rules_fd;

    assert(snprintf(config_path, TEST_PATH_SIZE,
        "%s/msconnector-transaction-contract-config-XXXXXX", directory) > 0);
    assert(snprintf(event_path, TEST_PATH_SIZE,
        "%s/msconnector-transaction-contract-events-XXXXXX", directory) > 0);
    assert(snprintf(rules_path, TEST_PATH_SIZE,
        "%s/msconnector-transaction-contract-rules-XXXXXX", directory) > 0);
    config_fd = mkstemp(config_path);
    assert(config_fd >= 0);
    event_fd = mkstemp(event_path);
    assert(event_fd >= 0);
    assert(close(event_fd) == 0);
    rules_fd = mkstemp(rules_path);
    assert(rules_fd >= 0);
    rules = fdopen(rules_fd, "w");
    assert(rules != NULL);
    assert(rules_text != NULL);
    assert(request_body_mode != NULL);
    assert(phase4_mode != NULL);
    assert(fputs(rules_text, rules) != EOF);
    assert(fclose(rules) == 0);
    config = fdopen(config_fd, "w");
    assert(config != NULL);
    assert(fprintf(config,
        "enabled=on\n"
        "rules_file=%s\n"
        "transaction_id_header=x-request-id\n"
        "request_body_mode=%s\n"
        "response_body_mode=none\n"
        "request_body_limit=1024\n"
        "response_body_limit=1024\n"
        "phase4_mode=%s\n"
        "default_block_status=403\n"
        "default_error_status=500\n"
        "max_header_count=32\n"
        "max_header_name_size=128\n"
        "max_header_value_size=512\n"
        "max_total_header_bytes=4096\n"
        "max_event_json_bytes=16384\n"
        "event_path=%s\n", rules_path, request_body_mode, phase4_mode,
        event_path) > 0);
    assert(fclose(config) == 0);
}

static void assert_terminal_events(const char *event_path) {
    char contents[32768];
    FILE *event_file;
    size_t size;

    event_file = fopen(event_path, "r");
    assert(event_file != NULL);
    size = fread(contents, 1U, sizeof(contents) - 1U, event_file);
    assert(ferror(event_file) == 0);
    assert(fclose(event_file) == 0);
    contents[size] = '\0';
    assert(strstr(contents, "\"event\":\"engine_timeout\"") != NULL);
    assert(strstr(contents, "\"event\":\"client_cancel\"") != NULL);
    assert(strstr(contents, "\"event\":\"protocol_error\"") != NULL);
    assert(strstr(contents, "\"body_payload\"") == NULL);
}

static void test_regular_block_emits_one_terminal_event(void) {
    static const char blocking_rules[] =
        "SecRuleEngine On\n"
        "SecRule REQUEST_URI \"@streq /blocked\" \"id:1001,phase:1,deny,status:403,log\"\n";
    msconnector_runtime *runtime = NULL;
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_runtime_transaction_snapshot snapshot;
    msconnector_decision decision;
    msconnector_error error;
    char config_path[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char rules_path[TEST_PATH_SIZE];
    char contents[16384];
    FILE *event_file;
    size_t size;

    create_runtime_fixture(config_path, event_path, rules_path, blocking_rules,
        "none", "safe");
    assert(msconnector_runtime_create("envoy", config_path, &runtime, NULL, 0U));
    assert(msconnector_runtime_set_event_integration_mode(runtime, "ext_authz"));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-authz")));
    assert(msconnector_test_begin_transaction(runtime, "/blocked", "rule-block",
        &transaction, &decision, &error));
    assert(transaction != NULL);
    assert(msconnector_decision_action_from_decision(&decision) ==
        MSCONNECTOR_DECISION_ACTION_DENY);
    assert(msconnector_runtime_transaction_snapshot_get(transaction, &snapshot));
    assert(snapshot.contract.created_at_ms > 0U);
    assert(snapshot.contract.completed_at_ms >= snapshot.contract.created_at_ms);
    assert(msconnector_runtime_transaction_finish(transaction, &error));
    msconnector_runtime_transaction_destroy(&transaction);
    msconnector_runtime_destroy(&runtime);

    event_file = fopen(event_path, "r");
    assert(event_file != NULL);
    size = fread(contents, 1U, sizeof(contents) - 1U, event_file);
    assert(ferror(event_file) == 0);
    assert(fclose(event_file) == 0);
    contents[size] = '\0';
    assert(strstr(contents, "MSCONN_EVENT_REQUEST_BLOCKED") != NULL);
    assert(strstr(contents, "MSCONN_EVENT_CONNECTOR_ERROR") == NULL);
    assert(strstr(contents, "\"transaction_id\":\"rule-block\"") != NULL);
    assert(strchr(contents, '\n') == strrchr(contents, '\n'));
    assert(unlink(config_path) == 0);
    assert(unlink(event_path) == 0);
    assert(unlink(rules_path) == 0);
}

static void test_lossy_event_is_not_written_or_chained(void) {
    static const char blocking_rules[] =
        "SecRuleEngine On\n"
        "SecRule REQUEST_URI \"@streq /blocked\" \"id:1002,phase:1,deny,status:403,log\"\n";
    static const char invalid_client_address[] = {
        '1', '2', '7', '.', '0', '.', '0', '.', (char)0x80, '\0'
    };
    msconnector_runtime *runtime = NULL;
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_request request;
    msconnector_decision decision;
    msconnector_error error;
    char config_path[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char rules_path[TEST_PATH_SIZE];
    char contents[16384];
    FILE *event_file;
    size_t size;

    create_runtime_fixture(config_path, event_path, rules_path, blocking_rules,
        "none", "safe");
    assert(msconnector_runtime_create("envoy", config_path, &runtime, NULL, 0U));
    assert(msconnector_runtime_set_event_integration_mode(runtime, "ext_authz"));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-authz")));

    memset(&request, 0, sizeof(request));
    request.method = "GET";
    request.uri = "/blocked";
    request.http_version = "HTTP/1.1";
    request.client.address = invalid_client_address;
    request.client.port = 12345;
    request.server.address = "127.0.0.1";
    request.server.port = 9191;
    msconnector_error_init(&error);
    msconnector_decision_init(&decision);
    assert(!msconnector_runtime_transaction_begin(runtime, &request, "lossy-event",
        &transaction, &decision, &error));
    assert(transaction == NULL);
    assert(error.code == MSCONNECTOR_ERROR_EVENT_TOO_LARGE);

    event_file = fopen(event_path, "r");
    assert(event_file != NULL);
    size = fread(contents, 1U, sizeof(contents), event_file);
    assert(ferror(event_file) == 0);
    assert(fclose(event_file) == 0);
    assert(size == 0U);

    assert(msconnector_test_begin_transaction(runtime, "/blocked", "post-lossy",
        &transaction, &decision, &error));
    assert(transaction != NULL);
    assert(msconnector_decision_action_from_decision(&decision) ==
        MSCONNECTOR_DECISION_ACTION_DENY);
    assert(msconnector_runtime_transaction_finish(transaction, &error));
    msconnector_runtime_transaction_destroy(&transaction);

    event_file = fopen(event_path, "r");
    assert(event_file != NULL);
    size = fread(contents, 1U, sizeof(contents) - 1U, event_file);
    assert(ferror(event_file) == 0);
    assert(fclose(event_file) == 0);
    contents[size] = '\0';
    assert(strstr(contents, "MSCONN_EVENT_REQUEST_BLOCKED") != NULL);
    assert(strstr(contents, "\"transaction_id\":\"post-lossy\"") != NULL);
    assert(strstr(contents, "\"previous_event_hash\":0") != NULL);
    assert(strchr(contents, '\n') == strrchr(contents, '\n'));

    msconnector_runtime_destroy(&runtime);
    assert(unlink(config_path) == 0);
    assert(unlink(event_path) == 0);
    assert(unlink(rules_path) == 0);
}

static void begin_handed_off(
    msconnector_runtime *runtime,
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE]) {
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_decision decision;
    msconnector_error error;

    assert(msconnector_test_begin_transaction(runtime, "/phase-contract",
        transaction_id, &transaction, &decision, &error));
    assert(transaction != NULL);
    assert(strcmp(msconnector_runtime_transaction_id(transaction), transaction_id) == 0);
    assert(msconnector_runtime_response_companion_handoff_with_handle(registry,
        transaction, UINT64_C(60000), handle, &error));
}

/* ext_authz forwards a bounded request entity to P2 before transferring the
 * live transaction to the response companion.  Keep this path distinct from
 * the metadata-only fixture so a zero-length buffered entity cannot regress
 * into a synthetic P2 or prevent the P1/P2 handoff. */
static void test_buffered_request_body_handoff(void) {
    char config_path[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char rules_path[TEST_PATH_SIZE];
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
    msconnector_runtime *runtime = NULL;
    msconnector_runtime_response_companion_registry registry;
    msconnector_error error;

    create_runtime_fixture(config_path, event_path, rules_path,
        "SecRuleEngine DetectionOnly\n", "buffered", "safe");
    assert(msconnector_runtime_create("envoy", config_path, &runtime, NULL, 0U));
    assert(msconnector_runtime_set_event_integration_mode(runtime, "ext_authz"));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-authz")));
    msconnector_runtime_response_companion_registry_init(&registry);
    begin_handed_off(runtime, &registry, "buffered-handoff", handle);
    msconnector_error_init(&error);
    assert(msconnector_runtime_response_companion_registry_shutdown(&registry, &error));
    msconnector_runtime_destroy(&runtime);
    assert(unlink(config_path) == 0);
    assert(unlink(event_path) == 0);
    assert(unlink(rules_path) == 0);
}

static void test_strict_profile_admission_is_fail_closed(void) {
    char config_path[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char rules_path[TEST_PATH_SIZE];
    msconnector_runtime *runtime = NULL;

    create_runtime_fixture(config_path, event_path, rules_path,
        "SecRuleEngine DetectionOnly\n", "none", "strict");
    assert(msconnector_runtime_create("envoy", config_path, &runtime, NULL, 0U));
    assert(!msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-authz")));
    msconnector_runtime_destroy(&runtime);

    /* ext_proc has no proven post-commit host action either.  Strict mode
     * must reject the profile during admission, before any transaction can
     * reach the host adapter; Safe mode remains covered by the runtime
     * matrix and is intentionally not changed here. */
    assert(msconnector_runtime_create("envoy", config_path, &runtime, NULL, 0U));
    assert(msconnector_runtime_set_event_integration_mode(runtime, "ext_proc"));
    assert(!msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-proc")));
    msconnector_runtime_destroy(&runtime);

    assert(msconnector_runtime_create("lighttpd", config_path, &runtime, NULL, 0U));
    assert(msconnector_runtime_set_event_integration_mode(runtime,
        "stock-lighttpd-sidecar"));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("lighttpd-stock")));
    msconnector_runtime_destroy(&runtime);
    assert(unlink(config_path) == 0);
    assert(unlink(event_path) == 0);
    assert(unlink(rules_path) == 0);
}

static int finish_response(
    msconnector_runtime_response_companion_registry *registry,
    const char *handle) {
    msconnector_runtime_response_companion_session session;
    msconnector_response response;
    msconnector_decision decision;
    msconnector_error error;

    memset(&response, 0, sizeof(response));
    response.status = 200;
    response.http_version = "HTTP/1.1";
    msconnector_error_init(&error);
    msconnector_decision_init(&decision);
    memset(&session, 0, sizeof(session));
    if (!msconnector_runtime_response_companion_claim_handle(registry, handle,
            &session, &error) ||
        !msconnector_runtime_response_companion_session_process_response_headers(
            &session, &response, &decision, &error) ||
        !msconnector_runtime_response_companion_session_set_response_commit_state(
            &session, 1, 0, &error) ||
        !msconnector_runtime_response_companion_session_finish_response_body(
            &session, &decision, &error) ||
        !msconnector_runtime_response_companion_session_release(&session, &error)) {
        return 0;
    }
    return 1;
}

static void *run_parallel_response(void *opaque) {
    companion_worker *worker = opaque;

    worker->result = finish_response(worker->registry, worker->handle);
    return NULL;
}

int main(void) {
    msconnector_runtime *runtime = NULL;
    msconnector_runtime_response_companion_registry registry;
    msconnector_error error;
    msconnector_response missing_eos_response;
    msconnector_decision missing_eos_decision;
    companion_worker first;
    companion_worker second;
    pthread_t first_thread;
    pthread_t second_thread;
    char config_path[TEST_PATH_SIZE];
    char event_path[TEST_PATH_SIZE];
    char rules_path[TEST_PATH_SIZE];

    create_runtime_fixture(config_path, event_path, rules_path,
        "SecRuleEngine DetectionOnly\n", "none", "safe");
    assert(msconnector_runtime_create("envoy", config_path,
        &runtime, NULL, 0U));
    assert(runtime != NULL);
    assert(msconnector_runtime_set_event_integration_mode(runtime, "ext_authz"));
    assert(msconnector_runtime_set_transaction_profile(runtime,
        msconnector_profile_registry_find("envoy-ext-authz")));
    msconnector_runtime_response_companion_registry_init(&registry);

    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
    begin_handed_off(runtime, &registry, "live-happy", handle);
    assert(finish_response(&registry, handle));
    msconnector_error_init(&error);
    assert(!msconnector_runtime_response_companion_claim_handle(&registry, handle,
        &(msconnector_runtime_response_companion_session){0}, &error));
    assert(error.code == MSCONNECTOR_ERROR_CORRELATION_MISSING);

    begin_handed_off(runtime, &registry, "live-expire", handle);
    assert(msconnector_runtime_response_companion_expire(&registry, UINT64_MAX) == 1U);

    begin_handed_off(runtime, &registry, "live-cancel", handle);
    msconnector_runtime_response_companion_session session;
    memset(&session, 0, sizeof(session));
    msconnector_error_init(&error);
    assert(msconnector_runtime_response_companion_claim_handle(&registry, handle,
        &session, &error));
    assert(msconnector_runtime_response_companion_session_cancel(&session, 0, &error));
    assert(!msconnector_runtime_response_companion_claim_handle(&registry, handle,
        &session, &error));
    assert(error.code == MSCONNECTOR_ERROR_CORRELATION_MISSING);

    begin_handed_off(runtime, &registry, "live-missing-eos", handle);
    memset(&missing_eos_response, 0, sizeof(missing_eos_response));
    missing_eos_response.status = 200;
    missing_eos_response.http_version = "HTTP/1.1";
    msconnector_error_init(&error);
    msconnector_decision_init(&missing_eos_decision);
    memset(&session, 0, sizeof(session));
    assert(msconnector_runtime_response_companion_claim_handle(&registry, handle,
        &session, &error));
    assert(msconnector_runtime_response_companion_session_process_response_headers(
        &session, &missing_eos_response, &missing_eos_decision, &error));
    assert(msconnector_runtime_response_companion_session_set_response_commit_state(
        &session, 1, 0, &error));
    assert(!msconnector_runtime_response_companion_session_release(&session, &error));
    assert(error.code == MSCONNECTOR_ERROR_PHASE_SEQUENCE);

    begin_handed_off(runtime, &registry, "parallel-a", first.handle);
    begin_handed_off(runtime, &registry, "parallel-b", second.handle);
    first.registry = &registry;
    first.result = 0;
    second.registry = &registry;
    second.result = 0;
    assert(pthread_create(&first_thread, NULL, run_parallel_response, &first) == 0);
    assert(pthread_create(&second_thread, NULL, run_parallel_response, &second) == 0);
    assert(pthread_join(first_thread, NULL) == 0);
    assert(pthread_join(second_thread, NULL) == 0);
    assert(first.result);
    assert(second.result);

    begin_handed_off(runtime, &registry, "stream-reuse", handle);
    assert(finish_response(&registry, handle));
    begin_handed_off(runtime, &registry, "stream-reuse", handle);
    assert(finish_response(&registry, handle));

    /* A host-request ID is an external correlation hint, not the Common
     * ownership key.  Concurrent requests may legitimately reuse it; their
     * generated canonical IDs and opaque response handles must stay distinct.
     */
    begin_handed_off(runtime, &registry, "same-external-id", first.handle);
    begin_handed_off(runtime, &registry, "same-external-id", second.handle);
    assert(strcmp(first.handle, second.handle) != 0);
    assert(finish_response(&registry, first.handle));
    assert(finish_response(&registry, second.handle));

    /* The registry is fixed-capacity. Exhaustion must reject a new handoff
     * without evicting a live transaction; expiry must then reclaim every
     * unclaimed entry so the next independent transaction can proceed. */
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY; ++index) {
        char transaction_id[64];

        assert(snprintf(transaction_id, sizeof(transaction_id), "capacity-%zu", index) > 0);
        begin_handed_off(runtime, &registry, transaction_id, handle);
    }
    {
        msconnector_runtime_transaction *overflow = NULL;
        msconnector_decision decision;

        assert(msconnector_test_begin_transaction(runtime, "/phase-contract",
            "capacity-overflow", &overflow, &decision, &error));
        assert(overflow != NULL);
        assert(!msconnector_runtime_response_companion_handoff_with_handle(&registry,
            overflow, UINT64_C(60000), handle, &error));
        assert(error.code == MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE);
        assert(msconnector_runtime_transaction_cancel(overflow, 0, &error));
        msconnector_runtime_transaction_destroy(&overflow);
    }
    assert(msconnector_runtime_response_companion_expire(&registry, UINT64_MAX) ==
        MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY);
    begin_handed_off(runtime, &registry, "capacity-reclaimed", handle);
    assert(finish_response(&registry, handle));

    begin_handed_off(runtime, &registry, "shutdown-cleanup", handle);
    msconnector_error_init(&error);
    assert(msconnector_runtime_response_companion_registry_shutdown(&registry, &error));
    msconnector_runtime_destroy(&runtime);
    assert_terminal_events(event_path);
    assert(unlink(config_path) == 0);
    assert(unlink(event_path) == 0);
    assert(unlink(rules_path) == 0);
    test_strict_profile_admission_is_fail_closed();
    test_regular_block_emits_one_terminal_event();
    test_lossy_event_is_not_written_or_chained();
    test_buffered_request_body_handoff();
    assert(rmdir(test_private_root) == 0);
    return 0;
}
