/* Regression for detached-worker shutdown, profile ownership and Host checks. */
#define _POSIX_C_SOURCE 200809L
#include "common/runtime/http_authorization_service.h"
#include "common/runtime/msconnector_runtime.h"
#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#define TEST_WAIT_SECONDS 3L
struct msconnector_runtime { int placeholder; };
struct msconnector_runtime_transaction { int finished; };
static msconnector_runtime fake_runtime;
static pthread_mutex_t test_lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t test_changed = PTHREAD_COND_INITIALIZER;
static int mapper_entered, runtime_entered, runtime_release, runtime_destroyed;
static int server_done;
static const msconnector_transaction_profile test_transaction_profile = {
    1U, "detached-worker-smoke", "detached-worker-smoke", "test-adapter",
    0U, 0U, 0, 1,
};

static void clear_error(char *error, size_t length) {
    if (error != NULL && length > 0U) error[0] = '\0';
}
static int wait_for_flag(const int *flag) {
    struct timespec deadline;
    int result = 0;
    if (clock_gettime(CLOCK_REALTIME, &deadline) != 0 ||
        pthread_mutex_lock(&test_lock) != 0) return 0;
    deadline.tv_sec += TEST_WAIT_SECONDS;
    while (*flag == 0 && result == 0)
        result = pthread_cond_timedwait(&test_changed, &test_lock, &deadline);
    result = *flag != 0;
    (void)pthread_mutex_unlock(&test_lock);
    return result;
}
static void unblock_runtime(void) {
    if (pthread_mutex_lock(&test_lock) == 0) {
        runtime_release = 1; (void)pthread_cond_broadcast(&test_changed);
        (void)pthread_mutex_unlock(&test_lock);
    }
}
static int flag_is_zero(const int *flag) {
    int result = 0;
    if (pthread_mutex_lock(&test_lock) == 0) {
        result = *flag == 0; (void)pthread_mutex_unlock(&test_lock);
    }
    return result;
}
static int runtime_destroyed_once(void) {
    int result = 0;
    if (pthread_mutex_lock(&test_lock) == 0) {
        result = runtime_destroyed == 1; (void)pthread_mutex_unlock(&test_lock);
    }
    return result;
}

int msconnector_runtime_config_check(const char *name, const char *path,
    char *error, size_t length) {
    (void)name; (void)path; clear_error(error, length); return 1;
}
int msconnector_runtime_create(const char *name, const char *path,
    msconnector_runtime **out, char *error, size_t length) {
    (void)name; (void)path; if (out == NULL) return 0;
    clear_error(error, length); *out = &fake_runtime; return 1;
}
void msconnector_runtime_destroy(msconnector_runtime **runtime) {
    if (pthread_mutex_lock(&test_lock) == 0) {
        ++runtime_destroyed; (void)pthread_cond_broadcast(&test_changed);
        (void)pthread_mutex_unlock(&test_lock);
    }
    if (runtime != NULL) *runtime = NULL;
}
int msconnector_runtime_set_event_integration_mode(msconnector_runtime *runtime,
    const char *mode) { if (runtime != NULL) runtime->placeholder = mode != NULL;
    return runtime != NULL && mode != NULL; }
int msconnector_runtime_set_transaction_profile(msconnector_runtime *runtime,
    const msconnector_transaction_profile *profile) {
    if (runtime != NULL) runtime->placeholder = profile != NULL;
    return runtime != NULL && profile != NULL;
}
int msconnector_runtime_error_log_enabled(const msconnector_runtime *runtime) {
    (void)runtime; return 0;
}
void msconnector_runtime_request_contract(const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract) {
    (void)runtime; msconnector_request_mapper_contract_init(contract);
    contract->max_header_count = 16U; contract->max_body_bytes = 1024U;
}
size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime)
    { (void)runtime; return 1024U; }
size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime)
    { (void)runtime; return 4096U; }
size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime)
    { (void)runtime; return 16U; }
int msconnector_runtime_transaction_begin(msconnector_runtime *runtime,
    const msconnector_request *request, const char *request_id,
    msconnector_runtime_transaction **out, msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;
    (void)request_id;
    if (runtime == NULL || request == NULL || out == NULL || decision == NULL ||
        request->method == NULL || request->uri == NULL ||
        strcmp(request->method, "GET") != 0 || strcmp(request->uri, "/ok") != 0 ||
        pthread_mutex_lock(&test_lock) != 0) return 0;
    runtime->placeholder = 1; runtime_entered = 1;
    (void)pthread_cond_broadcast(&test_changed);
    while (runtime_release == 0) {
        if (pthread_cond_wait(&test_changed, &test_lock) != 0) {
            (void)pthread_mutex_unlock(&test_lock); return 0;
        }
    }
    (void)pthread_mutex_unlock(&test_lock);
    transaction = calloc(1U, sizeof(*transaction)); if (transaction == NULL) return 0;
    *out = transaction; msconnector_decision_set_allow(decision);
    if (error != NULL) msconnector_error_init(error);
    return 1;
}
int msconnector_runtime_transaction_finish(msconnector_runtime_transaction *tx,
    msconnector_error *error) { if (tx == NULL) return 0; tx->finished = 1;
    if (error != NULL) msconnector_error_init(error);
    return 1;
}
const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *tx)
    { return tx == NULL ? NULL : "detached-worker-smoke"; }
void msconnector_runtime_transaction_destroy(msconnector_runtime_transaction **tx)
    { if (tx != NULL) { free(*tx); *tx = NULL; } }
int msconnector_runtime_error_http_status(const msconnector_runtime *runtime,
    msconnector_error_code code) { (void)runtime; (void)code; return 500; }

static int map_request(const msconnector_generic_request_source *source,
    const msconnector_request_mapper_contract *contract, msconnector_request *request,
    char *error, size_t length) {
    (void)contract;
    if (source == NULL || request == NULL || source->method == NULL || source->uri == NULL) {
        if (error != NULL && length > 0U) (void)snprintf(error, length, "%s", "invalid smoke request");
        return 0;
    }
    if (pthread_mutex_lock(&test_lock) != 0) return 0;
    ++mapper_entered; (void)pthread_cond_broadcast(&test_changed);
    (void)pthread_mutex_unlock(&test_lock); memset(request, 0, sizeof(*request));
    request->method = source->method; request->uri = source->uri;
    request->http_version = source->http_version; request->hostname = source->hostname;
    request->client = source->client; request->server = source->server;
    request->headers = source->headers; request->header_count = source->header_count;
    request->body = source->body; return 1;
}
typedef struct server_thread_args { char listen_spec[64]; int result;
    const msconnector_http_authorization_profile *profile; } server_thread_args;
static void *run_service(void *argument) {
    server_thread_args *args = argument;
    char *argv[] = {"detached-worker-smoke", "--serve", "--config", "ignored.conf",
        "--listen", args->listen_spec, "--max-requests", "3",
        "--connection-timeout-ms", "25", NULL};
    args->result = msconnector_http_authorization_service_main(10, argv, args->profile);
    if (pthread_mutex_lock(&test_lock) == 0) { server_done = 1;
        (void)pthread_cond_broadcast(&test_changed); (void)pthread_mutex_unlock(&test_lock); }
    return NULL;
}
static int reserve_loopback_port(unsigned short *port) {
    struct sockaddr_in address = {0}; socklen_t size = sizeof(address);
    int fd = socket(AF_INET, SOCK_STREAM, 0); if (fd < 0) return 0;
    address.sin_family = AF_INET; address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    if (bind(fd, (const struct sockaddr *)&address, sizeof(address)) != 0 ||
        getsockname(fd, (struct sockaddr *)&address, &size) != 0) { close(fd); return 0; }
    *port = ntohs(address.sin_port); return close(fd) == 0;
}
static int connect_loopback(unsigned short port) {
    struct sockaddr_in address = {0}; address.sin_family = AF_INET;
    address.sin_port = htons(port); address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    for (int attempt = 0; attempt < 100; ++attempt) {
        int fd = socket(AF_INET, SOCK_STREAM, 0);
        if (fd >= 0 && connect(fd, (const struct sockaddr *)&address, sizeof(address)) == 0) return fd;
        if (fd >= 0) close(fd);
        struct timespec delay = {0, 10000000L};
        nanosleep(&delay, NULL);
    } return -1;
}
static int response_starts_with(int fd, const char *expected) {
    struct timeval timeout = {TEST_WAIT_SECONDS, 0}; char response[64]; size_t used = 0;
    size_t length = expected == NULL ? 0U : strlen(expected);
    if (length == 0U || length > sizeof(response) ||
        setsockopt(fd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) != 0) return 0;
    while (used < length) { ssize_t received = recv(fd, response + used, length - used, 0);
        if (received <= 0) return 0;
        used += (size_t)received;
    }
    return memcmp(response, expected, length) == 0;
}

int main(void) {
    static const char request[] = "GET /ok HTTP/1.1\r\nHost: smoke.test\r\nConnection: close\r\n\r\n";
    static const char missing_host[] = "GET /ok HTTP/1.1\r\nConnection: close\r\n\r\n";
    static const char host_prefix[] = "GET /ok HTTP/1.1\r\nHost: ";
    static const char host_suffix[] = "\r\nConnection: close\r\n\r\n";
    char oversized[sizeof(host_prefix) - 1U + 1024U + sizeof(host_suffix) - 1U];
    char *name = strdup("detached-worker-smoke"), *mode = strdup("detached-worker-smoke");
    char *header = strdup("X-Original-Uri");
    const char **headers = calloc(1U, sizeof(*headers));
    msconnector_http_authorization_profile profile = {0};
    server_thread_args args = {{0}, -1, NULL}; unsigned short port = 0; pthread_t server;
    int fd = -1, started = 0, joined = 0, result = 1;
    if (name == NULL || mode == NULL || header == NULL || headers == NULL) goto done;
    headers[0] = header; profile.connector_name = name; profile.integration_mode = mode;
    profile.transaction_profile = &test_transaction_profile; profile.original_uri_headers = headers;
    profile.original_uri_header_count = 1U; profile.map_request = map_request; args.profile = &profile;
    memcpy(oversized, host_prefix, sizeof(host_prefix) - 1U);
    memset(oversized + sizeof(host_prefix) - 1U, 'a', 1024U);
    memcpy(oversized + sizeof(host_prefix) - 1U + 1024U, host_suffix, sizeof(host_suffix) - 1U);
    if (!reserve_loopback_port(&port) || snprintf(args.listen_spec, sizeof(args.listen_spec),
        "127.0.0.1:%u", (unsigned int)port) < 0 || pthread_create(&server, NULL, run_service, &args) != 0) goto done;
    started = 1; fd = connect_loopback(port);
    if (fd < 0 || send(fd, missing_host, sizeof(missing_host) - 1U, 0) != (ssize_t)(sizeof(missing_host) - 1U) ||
        !response_starts_with(fd, "HTTP/1.1 400") || !flag_is_zero(&mapper_entered) || !flag_is_zero(&runtime_entered)) goto done;
    close(fd); fd = connect_loopback(port);
    if (fd < 0 || send(fd, oversized, sizeof(oversized), 0) != (ssize_t)sizeof(oversized) ||
        !response_starts_with(fd, "HTTP/1.1 400") || !flag_is_zero(&mapper_entered) || !flag_is_zero(&runtime_entered)) goto done;
    close(fd); fd = connect_loopback(port);
    if (fd < 0 || send(fd, request, sizeof(request) - 1U, 0) != (ssize_t)(sizeof(request) - 1U) ||
        !wait_for_flag(&runtime_entered) || pthread_join(server, NULL) != 0 || args.result != 1) goto done;
    joined = 1; free(name); name = NULL; free(mode); mode = NULL; free(header); header = NULL; free(headers); headers = NULL;
    unblock_runtime(); if (!wait_for_flag(&runtime_destroyed) || !runtime_destroyed_once()) goto done;
    result = 0;
done:
    unblock_runtime(); if (started && !joined && wait_for_flag(&server_done)) pthread_join(server, NULL);
    free(name); free(mode); free(header); free(headers); if (fd >= 0) close(fd);
    if (result == 0) puts("http authorization detached-worker smoke: passed");
    return result;
}
