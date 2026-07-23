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
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

#define TEST_CONNECTION_TIMEOUT_MS 250UL
#define TEST_START_TIMEOUT_MS 2000L
#define TEST_RESPONSE_TIMEOUT_MS 1500L
#define TEST_CHILD_TIMEOUT_MS 3000L

struct msconnector_runtime {
    unsigned int active_transactions;
};

struct msconnector_runtime_transaction {
    msconnector_runtime *runtime;
    int finished;
};

static msconnector_runtime fake_runtime = {0U};

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
    if (runtime != NULL) {
        *runtime = NULL;
    }
}

void msconnector_runtime_request_contract(
    const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract) {
    (void)runtime;
    msconnector_request_mapper_contract_init(contract);
    contract->max_header_count = 64U;
    contract->max_body_bytes = 1024U;
}

size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 1024U;
}

size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 8192U;
}

size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime) {
    (void)runtime;
    return 64U;
}

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;
    (void)host_request_id;
    if (runtime == NULL || request == NULL || out == NULL || decision == NULL ||
        request->method == NULL || request->uri == NULL ||
        strcmp(request->method, "GET") != 0 || strcmp(request->uri, "/ok") != 0) {
        return 0;
    }
    transaction = calloc(1U, sizeof(*transaction));
    if (transaction == NULL) {
        return 0;
    }
    transaction->runtime = runtime;
    transaction->finished = 0;
    ++runtime->active_transactions;
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
    if (transaction == NULL || transaction->runtime == NULL) {
        return 0;
    }
    if (transaction->finished != 0) {
        return 1;
    }
    if (transaction->runtime->active_transactions == 0U) {
        return 0;
    }
    --transaction->runtime->active_transactions;
    transaction->finished = 1;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    return 1;
}

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction) {
    return transaction == NULL ? NULL : "timeout-smoke";
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

static int smoke_map_request(
    const msconnector_generic_request_source *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len) {
    (void)contract;
    if (source == NULL || request == NULL || source->method == NULL ||
        source->uri == NULL || strcmp(source->method, "GET") != 0 ||
        strcmp(source->uri, "/ok") != 0) {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "%s", "unexpected smoke request");
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

static const msconnector_http_authorization_profile smoke_profile = {
    .connector_name = "timeout-smoke",
    .integration_mode = "timeout-smoke",
    .original_uri_headers = NULL,
    .original_uri_header_count = 0U,
    .map_request = smoke_map_request,
    .map_response = NULL,
};

static int sleep_milliseconds(long milliseconds) {
    struct timespec duration;
    if (milliseconds < 0L) {
        return 0;
    }
    duration.tv_sec = milliseconds / 1000L;
    duration.tv_nsec = (milliseconds % 1000L) * 1000000L;
    return nanosleep(&duration, NULL) == 0;
}

static long monotonic_milliseconds(void) {
    struct timespec current;
    if (clock_gettime(CLOCK_MONOTONIC, &current) != 0) {
        return -1L;
    }
    return current.tv_sec * 1000L + current.tv_nsec / 1000000L;
}

static int reserve_loopback_port(unsigned short *port) {
    struct sockaddr_in address;
    socklen_t address_size = sizeof(address);
    int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        return 0;
    }
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = htons(0U);
    if (bind(socket_fd, (const struct sockaddr *)&address, sizeof(address)) != 0 ||
        getsockname(socket_fd, (struct sockaddr *)&address, &address_size) != 0) {
        (void)close(socket_fd);
        return 0;
    }
    *port = ntohs(address.sin_port);
    (void)close(socket_fd);
    return *port != 0U;
}

static int connect_loopback(unsigned short port, long timeout_ms) {
    const long deadline = monotonic_milliseconds() + timeout_ms;
    struct sockaddr_in address;
    if (deadline < 0L) {
        return -1;
    }
    memset(&address, 0, sizeof(address));
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    address.sin_port = htons(port);
    while (monotonic_milliseconds() <= deadline) {
        const int socket_fd = socket(AF_INET, SOCK_STREAM, 0);
        if (socket_fd < 0) {
            return -1;
        }
        if (connect(socket_fd, (const struct sockaddr *)&address, sizeof(address)) == 0) {
            return socket_fd;
        }
        (void)close(socket_fd);
        if (!sleep_milliseconds(10L)) {
            return -1;
        }
    }
    return -1;
}

static int send_all(int socket_fd, const char *data) {
    size_t sent = 0U;
    const size_t size = strlen(data);
    while (sent < size) {
        const ssize_t result = send(socket_fd, data + sent, size - sent, 0);
        if (result < 0 && errno == EINTR) {
            continue;
        }
        if (result <= 0) {
            return 0;
        }
        sent += (size_t)result;
    }
    return 1;
}

static int read_response(int socket_fd, char *response, size_t response_size) {
    struct timeval timeout;
    size_t used = 0U;
    if (response_size == 0U) {
        return 0;
    }
    timeout.tv_sec = TEST_RESPONSE_TIMEOUT_MS / 1000L;
    timeout.tv_usec = (suseconds_t)((TEST_RESPONSE_TIMEOUT_MS % 1000L) * 1000L);
    if (setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO,
            &timeout, sizeof(timeout)) != 0) {
        return 0;
    }
    while (used + 1U < response_size) {
        const ssize_t received = recv(socket_fd, response + used,
            response_size - used - 1U, 0);
        if (received < 0 && errno == EINTR) {
            continue;
        }
        if (received < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
            return 0;
        }
        if (received < 0) {
            return 0;
        }
        if (received == 0) {
            break;
        }
        used += (size_t)received;
    }
    response[used] = '\0';
    return used > 0U;
}

static pid_t start_service(unsigned short port) {
    char listen[64];
    char timeout[32];
    char *argv[] = {
        "timeout-smoke-service",
        "--serve",
        "--config",
        "timeout-smoke.conf",
        "--listen",
        listen,
        "--max-requests",
        "2",
        "--connection-timeout-ms",
        timeout,
        NULL,
    };
    const pid_t child = fork();
    if (child != 0) {
        return child;
    }
    (void)snprintf(listen, sizeof(listen), "127.0.0.1:%u", (unsigned int)port);
    (void)snprintf(timeout, sizeof(timeout), "%lu", TEST_CONNECTION_TIMEOUT_MS);
    _exit(msconnector_http_authorization_service_main(10, argv, &smoke_profile));
}

static int wait_for_service(pid_t child) {
    const long deadline = monotonic_milliseconds() + TEST_CHILD_TIMEOUT_MS;
    int status = 0;
    if (deadline < 0L) {
        return 0;
    }
    while (monotonic_milliseconds() <= deadline) {
        const pid_t result = waitpid(child, &status, WNOHANG);
        if (result == child) {
            return WIFEXITED(status) && WEXITSTATUS(status) == 0;
        }
        if (result < 0) {
            return 0;
        }
        if (!sleep_milliseconds(10L)) {
            return 0;
        }
    }
    (void)kill(child, SIGTERM);
    (void)waitpid(child, &status, 0);
    return 0;
}

static int response_has_status(const char *response, const char *status) {
    return response != NULL && strncmp(response, status, strlen(status)) == 0;
}

static int run_stalled_request_case(const char *case_name, const char *stall_request) {
    const char valid_request[] = "GET /ok HTTP/1.1\r\nHost: valid.example\r\n\r\n";
    char stalled_response[1024];
    char valid_response[1024];
    unsigned short port;
    int stalled_fd = -1;
    int valid_fd = -1;
    int result = 0;
    long valid_started;
    long valid_finished;
    pid_t service;

    if (!reserve_loopback_port(&port)) {
        (void)fprintf(stderr, "%s: could not reserve loopback port\n", case_name);
        return 0;
    }
    service = start_service(port);
    if (service < 0) {
        (void)fprintf(stderr, "%s: could not fork service\n", case_name);
        return 0;
    }
    stalled_fd = connect_loopback(port, TEST_START_TIMEOUT_MS);
    if (stalled_fd < 0 || !send_all(stalled_fd, stall_request)) {
        (void)fprintf(stderr, "%s: could not establish stalled peer\n", case_name);
        goto done;
    }
    if (!sleep_milliseconds((long)TEST_CONNECTION_TIMEOUT_MS + 100L)) {
        (void)fprintf(stderr, "%s: sleep failed\n", case_name);
        goto done;
    }
    valid_started = monotonic_milliseconds();
    valid_fd = connect_loopback(port, TEST_RESPONSE_TIMEOUT_MS);
    if (valid_fd < 0 || !send_all(valid_fd, valid_request) ||
        !read_response(valid_fd, valid_response, sizeof(valid_response))) {
        (void)fprintf(stderr, "%s: valid following request was not served\n", case_name);
        goto done;
    }
    valid_finished = monotonic_milliseconds();
    if (!response_has_status(valid_response, "HTTP/1.1 200") ||
        valid_started < 0L || valid_finished < valid_started ||
        valid_finished - valid_started > TEST_RESPONSE_TIMEOUT_MS) {
        (void)fprintf(stderr, "%s: valid following request did not receive a timely 200\n",
            case_name);
        goto done;
    }
    if (!read_response(stalled_fd, stalled_response, sizeof(stalled_response)) ||
        !response_has_status(stalled_response, "HTTP/1.1 408")) {
        (void)fprintf(stderr, "%s: stalled peer did not receive a bounded 408 response\n",
            case_name);
        goto done;
    }
    if (!wait_for_service(service)) {
        (void)fprintf(stderr, "%s: service did not exit cleanly after the valid mapping\n",
            case_name);
        service = -1;
        goto done;
    }
    service = -1;
    result = 1;

done:
    if (stalled_fd >= 0) {
        (void)close(stalled_fd);
    }
    if (valid_fd >= 0) {
        (void)close(valid_fd);
    }
    if (service > 0) {
        int status = 0;
        (void)kill(service, SIGTERM);
        (void)waitpid(service, &status, 0);
    }
    return result;
}

static pid_t start_dripping_peer(int socket_fd) {
    const pid_t child = fork();
    if (child != 0) {
        return child;
    }
    for (unsigned int index = 0U; index < 200U; ++index) {
        if (!sleep_milliseconds(20L) || !send_all(socket_fd, "x")) {
            _exit(0);
        }
    }
    _exit(0);
}

static int run_dripping_header_case(void) {
    const char initial_request[] = "GET /stall HTTP/1.1\r\nHost: slow.example";
    const char valid_request[] = "GET /ok HTTP/1.1\r\nHost: valid.example\r\n\r\n";
    char stalled_response[1024];
    char valid_response[1024];
    unsigned short port;
    int stalled_fd = -1;
    int valid_fd = -1;
    int result = 0;
    long valid_started;
    long valid_finished;
    pid_t service = -1;
    pid_t dripper = -1;

    if (!reserve_loopback_port(&port)) {
        (void)fprintf(stderr, "dripping_headers: could not reserve loopback port\n");
        return 0;
    }
    service = start_service(port);
    if (service < 0) {
        (void)fprintf(stderr, "dripping_headers: could not fork service\n");
        return 0;
    }
    stalled_fd = connect_loopback(port, TEST_START_TIMEOUT_MS);
    if (stalled_fd < 0 || !send_all(stalled_fd, initial_request)) {
        (void)fprintf(stderr, "dripping_headers: could not establish stalled peer\n");
        goto done;
    }
    dripper = start_dripping_peer(stalled_fd);
    if (dripper < 0 || !sleep_milliseconds((long)TEST_CONNECTION_TIMEOUT_MS + 100L)) {
        (void)fprintf(stderr, "dripping_headers: could not maintain a slow drip\n");
        goto done;
    }
    valid_started = monotonic_milliseconds();
    valid_fd = connect_loopback(port, TEST_RESPONSE_TIMEOUT_MS);
    if (valid_fd < 0 || !send_all(valid_fd, valid_request) ||
        !read_response(valid_fd, valid_response, sizeof(valid_response))) {
        (void)fprintf(stderr, "dripping_headers: valid following request was not served\n");
        goto done;
    }
    valid_finished = monotonic_milliseconds();
    if (!response_has_status(valid_response, "HTTP/1.1 200") ||
        valid_started < 0L || valid_finished < valid_started ||
        valid_finished - valid_started > TEST_RESPONSE_TIMEOUT_MS) {
        (void)fprintf(stderr, "dripping_headers: valid following request did not receive a timely 200\n");
        goto done;
    }
    if (!read_response(stalled_fd, stalled_response, sizeof(stalled_response)) ||
        !response_has_status(stalled_response, "HTTP/1.1 408")) {
        (void)fprintf(stderr, "dripping_headers: dripped peer did not receive a bounded 408 response\n");
        goto done;
    }
    if (!wait_for_service(service) || !wait_for_service(dripper)) {
        (void)fprintf(stderr, "dripping_headers: service or dripper did not exit cleanly\n");
        service = -1;
        dripper = -1;
        goto done;
    }
    service = -1;
    dripper = -1;
    result = 1;

done:
    if (stalled_fd >= 0) {
        (void)close(stalled_fd);
    }
    if (valid_fd >= 0) {
        (void)close(valid_fd);
    }
    if (dripper > 0) {
        int status = 0;
        (void)kill(dripper, SIGTERM);
        (void)waitpid(dripper, &status, 0);
    }
    if (service > 0) {
        int status = 0;
        (void)kill(service, SIGTERM);
        (void)waitpid(service, &status, 0);
    }
    return result;
}

static int rejects_unbounded_timeout_override(void) {
    char *argv[] = {
        "timeout-smoke-service",
        "--serve",
        "--config",
        "timeout-smoke.conf",
        "--listen",
        "127.0.0.1:18000",
        "--connection-timeout-ms",
        "0",
        NULL,
    };
    return msconnector_http_authorization_service_main(9, argv, &smoke_profile) == 2;
}

int main(void) {
    const char incomplete_headers[] =
        "GET /stall HTTP/1.1\r\nHost: slow.example\r\n";
    const char incomplete_body[] =
        "POST /stall HTTP/1.1\r\nHost: slow.example\r\nContent-Length: 4\r\n\r\nx";

    (void)signal(SIGPIPE, SIG_IGN);
    if (!rejects_unbounded_timeout_override()) {
        (void)fprintf(stderr, "timeout override of zero was unexpectedly accepted\n");
        return 1;
    }
    if (!run_stalled_request_case("incomplete_headers", incomplete_headers) ||
        !run_stalled_request_case("incomplete_body", incomplete_body) ||
        !run_dripping_header_case()) {
        return 1;
    }
    (void)printf("http_authorization_service_timeout_smoke: pass\n");
    return 0;
}
