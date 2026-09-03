/*
 * Regression for bounded shutdown when a detached authorization worker is
 * held inside an uninterruptible runtime operation.  Build this source with
 * common/runtime/http_authorization_service.c and the Common C sources, then
 * run it under ASan/UBSan.  The service entry point must return after its two
 * configured grace periods without invalidating worker-owned state; the final
 * worker performs the deferred release after the test unblocks the runtime.
 */
#define _POSIX_C_SOURCE 200809L

#include "common/runtime/http_authorization_service.h"
#include "common/runtime/msconnector_runtime.h"

#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"

#include <arpa/inet.h>
#include <errno.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <time.h>
#include <unistd.h>

#define TEST_TIMEOUT_MS 25UL
#define TEST_WAIT_SECONDS 3L

struct msconnector_runtime {
    int placeholder;
};

struct msconnector_runtime_transaction {
    int finished;
};

static msconnector_runtime fake_runtime = {0};
static pthread_mutex_t test_lock = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t test_changed = PTHREAD_COND_INITIALIZER;
static int runtime_entered = 0;
static int runtime_release = 0;
static int runtime_destroyed = 0;
static int server_done = 0;

static int wait_for_flag(int *flag) {
    struct timespec deadline;
    int result = 0;
    if (clock_gettime(CLOCK_REALTIME, &deadline) != 0 ||
        pthread_mutex_lock(&test_lock) != 0) {
        return 0;
    }
    deadline.tv_sec += TEST_WAIT_SECONDS;
    while (*flag == 0 && result == 0) {
        result = pthread_cond_timedwait(&test_changed, &test_lock, &deadline);
    }
    result = *flag != 0;
    (void)pthread_mutex_unlock(&test_lock);
    return result;
}
static void unblock_runtime(void) {
    if (pthread_mutex_lock(&test_lock) == 0) {
        runtime_release = 1;
        (void)pthread_cond_broadcast(&test_changed);
        (void)pthread_mutex_unlock(&test_lock);
    }
}

static int runtime_destroyed_once(void) {
    int destroyed_once = 0;

    if (pthread_mutex_lock(&test_lock) == 0) {
        destroyed_once = runtime_destroyed == 1;
        (void)pthread_mutex_unlock(&test_lock);
    }
    return destroyed_once;
}

int msconnector_runtime_config_check(
    const char *connector_name,
    const char *config_path,
    char *error,
    size_t error_len) {
    (void)connector_name;
    (void)config_path;
    if (error != NULL && error_len > 0U) {
        error[0] = '\0';
    }
    return 1;
}

int msconnector_runtime_set_event_integration_mode(
    msconnector_runtime *runtime,
    const char *integration_mode) {
    return runtime != NULL && integration_mode != NULL && integration_mode[0] != '\0';
}

int msconnector_runtime_set_transaction_profile(
    msconnector_runtime *runtime,
    const msconnector_transaction_profile *profile) {
    return runtime != NULL && profile != NULL && profile->profile_name != NULL;
}

int msconnector_runtime_error_log_enabled(const msconnector_runtime *runtime) {
    (void)runtime;
    return 0;
}

int msconnector_runtime_create(
    const char *connector_name,
    const char *config_path,
    msconnector_runtime **out,
    char *error,
    size_t error_len) {
    (void)connector_name;
    (void)config_path;
    if (out == NULL) {
        return 0;
    }
    if (error != NULL && error_len > 0U) {
        error[0] = '\0';
    }
    *out = &fake_runtime;
    return 1;
}

void msconnector_runtime_destroy(msconnector_runtime **runtime) {
    if (pthread_mutex_lock(&test_lock) == 0) {
        ++runtime_destroyed;
        (void)pthread_cond_broadcast(&test_changed);
        (void)pthread_mutex_unlock(&test_lock);
    }
    if (runtime != NULL) {
        *runtime = NULL;
    }
}

void msconnector_runtime_request_contract(
    const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract) {
    (void)runtime;
    msconnector_request_mapper_contract_init(contract);
    contract->max_header_count = 16U;
    contract->max_body_bytes = 1024U;
}

size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 1024U;
}

size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 4096U;
}

size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 16U;
}

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;
    (void)runtime;
    (void)host_request_id;
    if (request == NULL || out == NULL || decision == NULL ||
        request->method == NULL || request->uri == NULL ||
        strcmp(request->method, "GET") != 0 || strcmp(request->uri, "/ok") != 0 ||
        pthread_mutex_lock(&test_lock) != 0) {
        return 0;
    }
    runtime_entered = 1;
    (void)pthread_cond_broadcast(&test_changed);
    while (runtime_release == 0) {
        if (pthread_cond_wait(&test_changed, &test_lock) != 0) {
            (void)pthread_mutex_unlock(&test_lock);
            return 0;
        }
    }
    (void)pthread_mutex_unlock(&test_lock);
    transaction = calloc(1U, sizeof(*transaction));
    if (transaction == NULL) {
        return 0;
    }
    *out = transaction;
    msconnector_decision_set_allow(decision);
    if (error != NULL) {
        msconnector_error_init(error);
    }
    return 1;
}

int msconnector_runtime_transaction_finish(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    if (transaction == NULL) {
        return 0;
    }
    transaction->finished = 1;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    return 1;
}

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction) {
    return transaction == NULL ? NULL : "detached-worker-smoke";
}

void msconnector_runtime_transaction_destroy(
    msconnector_runtime_transaction **transaction) {
    if (transaction != NULL) {
        free(*transaction);
        *transaction = NULL;
    }
}

int msconnector_runtime_error_http_status(
    const msconnector_runtime *runtime,
    msconnector_error_code code) {
    (void)runtime;
    (void)code;
    return 500;
}

static int map_request(
    const msconnector_generic_request_source *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len) {
    (void)contract;
    if (source == NULL || request == NULL || source->method == NULL ||
        source->uri == NULL) {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "%s", "invalid smoke request");
        }
        return 0;
    }
    memset(request, 0, sizeof(*request));
    request->method = source->method;
    request->uri = source->uri;
    request->http_version = source->http_version;
    request->hostname = source->hostname;
    request->client = source->client;
    request->server = source->server;
    request->headers = source->headers;
    request->header_count = source->header_count;
    request->body = source->body;
    return 1;
}

static const msconnector_transaction_profile smoke_transaction_profile = {
    .profile_id = 1U,
    .profile_name = "detached-worker-smoke",
    .connector_id = "detached-worker-smoke",
    .host_adapter_id = "detached-worker-smoke",
    .direct_phase_mask = MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL,
    .companion_phase_mask = 0U,
    .strict_post_commit_action = 0,
    .private_default_binding = 1,
};

static const msconnector_http_authorization_profile profile = {
    .connector_name = "detached-worker-smoke",
    .integration_mode = "detached-worker-smoke",
    .transaction_profile = &smoke_transaction_profile,
    .original_uri_headers = NULL,
    .original_uri_header_count = 0U,
    .map_request = map_request,
    .map_response = NULL,
};

typedef struct server_thread_args {
    char listen_spec[64];
    int result;
} server_thread_args;

static void *run_service(void *argument) {
    server_thread_args *args = argument;
    char *argv[] = {
        "detached-worker-smoke",
        "--serve",
        "--config",
        "ignored.conf",
        "--listen",
        args->listen_spec,
        "--max-requests",
        "1",
        "--connection-timeout-ms",
        "25",
        NULL,
    };
    args->result = msconnector_http_authorization_service_main(10, argv, &profile);
    if (pthread_mutex_lock(&test_lock) == 0) {
        server_done = 1;
        (void)pthread_cond_broadcast(&test_changed);
        (void)pthread_mutex_unlock(&test_lock);
    }
    return NULL;
}

static int reserve_loopback_port(unsigned short *port) {
    struct sockaddr_in address = {0};
    socklen_t address_size = sizeof(address);
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        return 0;
    }
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = 0;
    if (bind(socket_fd, (const struct sockaddr *)&address, sizeof(address)) != 0 ||
        getsockname(socket_fd, (struct sockaddr *)&address, &address_size) != 0) {
        (void)close(socket_fd);
        return 0;
    }
    *port = ntohs(address.sin_port);
    return close(socket_fd) == 0;
}

static int connect_loopback(unsigned short port) {
    struct sockaddr_in address = {0};
    int socket_fd;
    address.sin_family = AF_INET;
    address.sin_port = htons(port);
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    for (int attempt = 0; attempt < 100; ++attempt) {
        socket_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (socket_fd >= 0 &&
            connect(socket_fd, (const struct sockaddr *)&address, sizeof(address)) == 0) {
            return socket_fd;
        }
        if (socket_fd >= 0) {
            (void)close(socket_fd);
        }
        {
            const struct timespec delay = {.tv_sec = 0, .tv_nsec = 10000000L};
            (void)nanosleep(&delay, NULL);
        }
    }
    return -1;
}

int main(void) {
    static const char request[] = "GET /ok HTTP/1.1\r\nHost: smoke.test\r\n"
        "Connection: close\r\n\r\n";
    server_thread_args args = {{0}, -1};
    unsigned short port = 0U;
    pthread_t server;
    int client_fd = -1;
    int server_started = 0;
    int server_joined = 0;
    int result = 1;

    if (!reserve_loopback_port(&port) ||
        snprintf(args.listen_spec, sizeof(args.listen_spec), "127.0.0.1:%u",
            (unsigned int)port) < 0 ||
        pthread_create(&server, NULL, run_service, &args) != 0) {
        (void)fprintf(stderr, "could not start detached-worker service\n");
        return 1;
    }
    server_started = 1;
    client_fd = connect_loopback(port);
    if (client_fd < 0 ||
        send(client_fd, request, sizeof(request) - 1U,
#ifdef MSG_NOSIGNAL
            MSG_NOSIGNAL) !=
#else
            0) !=
#endif
            (ssize_t)(sizeof(request) - 1U) ||
        !wait_for_flag(&runtime_entered) || !wait_for_flag(&server_done) ||
        pthread_join(server, NULL) != 0 ||
        args.result != 1) {
        (void)fprintf(stderr, "service did not reach bounded deferred shutdown\n");
        goto done;
    }
    server_joined = 1;
    unblock_runtime();
    if (!wait_for_flag(&runtime_destroyed) || !runtime_destroyed_once()) {
        (void)fprintf(stderr, "deferred worker cleanup did not finish\n");
        goto done;
    }
    result = 0;

done:
    unblock_runtime();
    if (server_started && !server_joined && wait_for_flag(&server_done)) {
        (void)pthread_join(server, NULL);
    }
    if (client_fd >= 0) {
        (void)close(client_fd);
    }
    if (result == 0) {
        (void)puts("http authorization detached-worker smoke: passed");
    }
    return result;
}
