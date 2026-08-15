#define _POSIX_C_SOURCE 200809L

#include "http_authorization_service.h"
#include "msconnector_runtime.h"

#include "msconnector/decision_action.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include "msconnector/limits.h"
#include "msconnector/request_helpers.h"

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <netinet/in.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define AUTH_LISTEN_HOST_SIZE 64U
#define AUTH_URI_SIZE 8192U
#define AUTH_HOSTNAME_SIZE 1024U
#define AUTH_HTTP_VERSION_SIZE 32U
#define AUTH_RESPONSE_SIZE 2048U
#define AUTH_ERROR_SIZE 512U
#define AUTH_REQUEST_LINE_OVERHEAD 16384U
#define AUTH_CONNECTION_TIMEOUT_DEFAULT_MS 5000UL
#define AUTH_CONNECTION_TIMEOUT_MAX_MS 600000UL
#define AUTH_MAX_CONNECTIONS_DEFAULT 8UL
#define AUTH_MAX_CONNECTIONS_MAX 64UL
#define AUTH_LISTENER_POLL_TIMEOUT_MS 100

typedef struct authorization_cli {
    const char *config_path;
    const char *listen_spec;
    int check_config;
    int serve;
    unsigned long max_requests;
    unsigned long connection_timeout_ms;
    unsigned long max_connections;
} authorization_cli;

typedef struct parsed_http_request {
    char *header_buffer;
    size_t header_buffer_size;
    msconnector_header *headers;
    size_t header_count;
    uint8_t *body;
    size_t body_size;
    char *method;
    char *uri;
    char *http_version;
    char uri_override[AUTH_URI_SIZE];
    char hostname[AUTH_HOSTNAME_SIZE];
    char client_address[INET_ADDRSTRLEN];
    char server_address[INET_ADDRSTRLEN];
    int client_port;
    int server_port;
} parsed_http_request;

typedef struct connection_deadline {
    struct timespec expires_at;
} connection_deadline;

typedef struct authorization_connection {
    int socket_fd;
    const struct sockaddr_in *peer;
    const struct sockaddr_in *local;
    const connection_deadline *read_deadline;
} authorization_connection;

typedef struct authorization_request_limits {
    size_t body_limit;
    size_t total_header_limit;
    size_t header_count_limit;
    msconnector_request_mapper_contract mapper_contract;
} authorization_request_limits;

struct authorization_worker;

typedef struct authorization_service {
    msconnector_runtime *runtime;
    const msconnector_http_authorization_profile *profile;
    authorization_request_limits request_limits;
    unsigned long connection_timeout_ms;
    unsigned long max_connections;
    unsigned long active_workers;
    struct authorization_worker *workers;
    pthread_mutex_t runtime_lock;
    pthread_mutex_t worker_lock;
    pthread_cond_t workers_idle;
} authorization_service;

typedef struct authorization_worker {
    authorization_service *service;
    int socket_fd;
    struct sockaddr_in peer;
    struct sockaddr_in local;
    connection_deadline read_deadline;
    struct authorization_worker *next;
} authorization_worker;

typedef struct authorization_response_state {
    int status;
    int success;
    const char *decision_name;
    const char *transaction_id;
    char copied_transaction_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
} authorization_response_state;

typedef enum authorization_listener_iteration {
    AUTHORIZATION_LISTENER_READY,
    AUTHORIZATION_LISTENER_RETRY,
    AUTHORIZATION_LISTENER_HANDLED,
    AUTHORIZATION_LISTENER_STOP,
    AUTHORIZATION_LISTENER_ERROR,
} authorization_listener_iteration;

static volatile sig_atomic_t authorization_stop = 0;

static void stop_service(int signal_number) {
    (void)signal_number;
    authorization_stop = 1;
}

static void print_usage(const char *program) {
    (void)fprintf(stderr,
        "usage: %s --check-config --config PATH\n"
        "       %s --serve --config PATH --listen HOST:PORT [--max-requests N] "
        "[--connection-timeout-ms N] [--max-connections N]\n",
        program, program);
}

static int parse_unsigned_long(const char *value, unsigned long *out) {
    char *end = NULL;
    unsigned long parsed;
    if (value == NULL || value[0] == '\0' || out == NULL || value[0] == '-') {
        return 0;
    }
    errno = 0;
    parsed = strtoul(value, &end, 10);
    if (errno != 0 || end == value || *end != '\0') {
        return 0;
    }
    *out = parsed;
    return 1;
}

static int parse_cli_value_option(
    const char *argument,
    const char *value,
    authorization_cli *cli) {
    if (strcmp(argument, "--config") == 0) {
        cli->config_path = value;
        return 1;
    }
    if (strcmp(argument, "--listen") == 0) {
        cli->listen_spec = value;
        return 1;
    }
    if (strcmp(argument, "--max-requests") == 0) {
        return parse_unsigned_long(value, &cli->max_requests);
    }
    if (strcmp(argument, "--connection-timeout-ms") == 0) {
        return parse_unsigned_long(value, &cli->connection_timeout_ms) &&
            cli->connection_timeout_ms != 0UL &&
            cli->connection_timeout_ms <= AUTH_CONNECTION_TIMEOUT_MAX_MS;
    }
    if (strcmp(argument, "--max-connections") == 0) {
        return parse_unsigned_long(value, &cli->max_connections) &&
            cli->max_connections != 0UL &&
            cli->max_connections <= AUTH_MAX_CONNECTIONS_MAX;
    }
    return 0;
}

static int parse_cli(int argc, char **argv, authorization_cli *cli) {
    int skip_option_value = 0;
    memset(cli, 0, sizeof(*cli));
    cli->connection_timeout_ms = AUTH_CONNECTION_TIMEOUT_DEFAULT_MS;
    cli->max_connections = AUTH_MAX_CONNECTIONS_DEFAULT;
    for (int index = 1; index < argc; ++index) {
        if (skip_option_value) {
            skip_option_value = 0;
            continue;
        }
        if (strcmp(argv[index], "--check-config") == 0) {
            cli->check_config = 1;
        } else if (strcmp(argv[index], "--serve") == 0) {
            cli->serve = 1;
        } else if (index + 1 < argc &&
            parse_cli_value_option(argv[index], argv[index + 1], cli)) {
            skip_option_value = 1;
        } else {
            return 0;
        }
    }
    if ((cli->check_config != 0) == (cli->serve != 0) || cli->config_path == NULL) {
        return 0;
    }
    if (cli->serve && cli->listen_spec == NULL) {
        return 0;
    }
    return 1;
}

static int validate_profile(const msconnector_http_authorization_profile *profile) {
    if (profile == NULL || profile->connector_name == NULL ||
        profile->connector_name[0] == '\0' || profile->integration_mode == NULL ||
        profile->integration_mode[0] == '\0' || profile->map_request == NULL) {
        return 0;
    }
    if (profile->original_uri_header_count > 0U && profile->original_uri_headers == NULL) {
        return 0;
    }
    for (size_t index = 0U; index < profile->original_uri_header_count; ++index) {
        if (profile->original_uri_headers[index] == NULL ||
            profile->original_uri_headers[index][0] == '\0') {
            return 0;
        }
    }
    return 1;
}

static int parse_listen_spec(
    const char *spec,
    char *host,
    size_t host_size,
    int *port) {
    const char *separator;
    size_t host_length;
    unsigned long parsed_port;
    if (spec == NULL || host == NULL || host_size == 0U || port == NULL) {
        return 0;
    }
    separator = strrchr(spec, ':');
    if (separator == NULL || separator == spec || separator[1] == '\0') {
        return 0;
    }
    host_length = (size_t)(separator - spec);
    if (host_length >= host_size ||
        !parse_unsigned_long(separator + 1, &parsed_port) ||
        parsed_port == 0UL || parsed_port > 65535UL) {
        return 0;
    }
    memcpy(host, spec, host_length);
    host[host_length] = '\0';
    if (strcmp(host, "localhost") == 0) {
        (void)snprintf(host, host_size, "%s", "127.0.0.1");
    }
    if (strcmp(host, "127.0.0.1") != 0 && strcmp(host, "0.0.0.0") != 0) {
        return 0;
    }
    *port = (int)parsed_port;
    return 1;
}

static void parsed_request_destroy(parsed_http_request *request) {
    if (request == NULL) {
        return;
    }
    free(request->body);
    free(request->headers);
    free(request->header_buffer);
    memset(request, 0, sizeof(*request));
}

static char *find_header_end(char *buffer, size_t size) {
    if (buffer == NULL || size < 4U) {
        return NULL;
    }
    for (size_t index = 0U; index + 3U < size; ++index) {
        if (buffer[index] == '\r' && buffer[index + 1U] == '\n' &&
            buffer[index + 2U] == '\r' && buffer[index + 3U] == '\n') {
            return buffer + index;
        }
    }
    return NULL;
}

/* Use an absolute monotonic deadline rather than an idle socket timeout so a
 * peer that drips bytes cannot retain the synchronous accept loop forever. */
static int connection_deadline_init(
    connection_deadline *deadline,
    unsigned long timeout_ms) {
    if (deadline == NULL || timeout_ms == 0UL ||
        timeout_ms > AUTH_CONNECTION_TIMEOUT_MAX_MS ||
        clock_gettime(CLOCK_MONOTONIC, &deadline->expires_at) != 0) {
        return 0;
    }
    deadline->expires_at.tv_sec += (time_t)(timeout_ms / 1000UL);
    deadline->expires_at.tv_nsec +=
        (long)((timeout_ms % 1000UL) * 1000000UL);
    if (deadline->expires_at.tv_nsec >= 1000000000L) {
        ++deadline->expires_at.tv_sec;
        deadline->expires_at.tv_nsec -= 1000000000L;
    }
    return 1;
}

static int connection_deadline_remaining_ms(const connection_deadline *deadline) {
    struct timespec now;
    time_t seconds;
    long nanoseconds;
    if (deadline == NULL || clock_gettime(CLOCK_MONOTONIC, &now) != 0) {
        return -1;
    }
    seconds = deadline->expires_at.tv_sec - now.tv_sec;
    nanoseconds = deadline->expires_at.tv_nsec - now.tv_nsec;
    if (nanoseconds < 0L) {
        --seconds;
        nanoseconds += 1000000000L;
    }
    if (seconds < 0 || (seconds == 0 && nanoseconds <= 0L)) {
        return 0;
    }
    if (seconds > (time_t)(INT_MAX / 1000)) {
        return INT_MAX;
    }
    return (int)(seconds * 1000 + (nanoseconds + 999999L) / 1000000L);
}

static int wait_for_socket(
    int socket_fd,
    short events,
    const connection_deadline *deadline) {
    struct pollfd descriptor;
    int timeout_ms;
    int result;
    if (socket_fd < 0) {
        return 0;
    }
    for (;;) {
        timeout_ms = connection_deadline_remaining_ms(deadline);
        if (timeout_ms <= 0) {
            return -1;
        }
        memset(&descriptor, 0, sizeof(descriptor));
        descriptor.fd = socket_fd;
        descriptor.events = events;
        result = poll(&descriptor, 1U, timeout_ms);
        if (result < 0 && errno == EINTR && !authorization_stop) {
            continue;
        }
        if (result == 0) {
            return -1;
        }
        if (result < 0) {
            return 0;
        }
        if ((descriptor.revents & events) != 0) {
            return 1;
        }
        if ((descriptor.revents & (POLLERR | POLLHUP | POLLNVAL)) != 0) {
            return 0;
        }
    }
}

static int recv_more(
    int socket_fd,
    void *buffer,
    size_t capacity,
    size_t *used,
    const connection_deadline *deadline) {
    ssize_t received;
    if (buffer == NULL || used == NULL || *used >= capacity) {
        return 0;
    }
    for (;;) {
        const int ready = wait_for_socket(socket_fd, POLLIN, deadline);
        if (ready != 1) {
            return ready;
        }
        do {
            received = recv(socket_fd, (char *)buffer + *used, capacity - *used, 0);
        } while (received < 0 && errno == EINTR && !authorization_stop);
        if (received < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
            continue;
        }
        if (received <= 0) {
            return 0;
        }
        *used += (size_t)received;
        return 1;
    }
}

static int http_token_character(unsigned char value);

static int parse_request_line(
    parsed_http_request *request,
    char *line,
    char *error,
    size_t error_len) {
    char *first_space;
    char *second_space;
    first_space = strchr(line, ' ');
    if (first_space == NULL) {
        (void)snprintf(error, error_len, "%s", "invalid HTTP request line");
        return 0;
    }
    *first_space = '\0';
    second_space = strchr(first_space + 1, ' ');
    if (second_space == NULL) {
        (void)snprintf(error, error_len, "%s", "invalid HTTP request line");
        return 0;
    }
    *second_space = '\0';
    request->method = line;
    request->uri = first_space + 1;
    request->http_version = second_space + 1;
    for (const char *cursor = request->method; *cursor != '\0'; ++cursor) {
        if (!http_token_character((unsigned char)*cursor)) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP method");
            return 0;
        }
    }
    for (const char *cursor = request->uri; *cursor != '\0'; ++cursor) {
        unsigned char current = (unsigned char)*cursor;
        if (current <= 0x20U || current == 0x7fU) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP request target");
            return 0;
        }
    }
    if (request->method[0] == '\0' || request->uri[0] != '/' ||
        strncmp(request->http_version, "HTTP/", 5U) != 0 ||
        strchr(request->http_version, ' ') != NULL ||
        strchr(request->http_version, '\t') != NULL) {
        (void)snprintf(error, error_len, "%s", "unsupported HTTP request line");
        return 0;
    }
    return 1;
}

static int http_token_character(unsigned char value) {
    if ((value >= (unsigned char)'a' && value <= (unsigned char)'z') ||
        (value >= (unsigned char)'A' && value <= (unsigned char)'Z') ||
        (value >= (unsigned char)'0' && value <= (unsigned char)'9')) {
        return 1;
    }
    return value == (unsigned char)'!' || value == (unsigned char)'#' ||
        value == (unsigned char)'$' || value == (unsigned char)'%' ||
        value == (unsigned char)'&' || value == (unsigned char)'\'' ||
        value == (unsigned char)'*' || value == (unsigned char)'+' ||
        value == (unsigned char)'-' || value == (unsigned char)'.' ||
        value == (unsigned char)'^' || value == (unsigned char)'_' ||
        value == (unsigned char)'`' || value == (unsigned char)'|' ||
        value == (unsigned char)'~';
}

static int valid_header_name(const char *name) {
    if (name == NULL || name[0] == '\0') {
        return 0;
    }
    for (size_t index = 0U; name[index] != '\0'; ++index) {
        if (!http_token_character((unsigned char)name[index])) {
            return 0;
        }
    }
    return 1;
}

static int valid_header_value(const char *value) {
    if (value == NULL) {
        return 0;
    }
    for (size_t index = 0U; value[index] != '\0'; ++index) {
        unsigned char current = (unsigned char)value[index];
        if ((current < 0x20U && current != (unsigned char)'\t') ||
            current == 0x7fU) {
            return 0;
        }
    }
    return 1;
}

static int parse_header_lines(
    parsed_http_request *request,
    const char *first_line_end,
    const char *header_end,
    size_t max_header_count,
    char *error,
    size_t error_len) {
    const char *cursor = request->header_buffer +
        (first_line_end - request->header_buffer) + 2;
    request->headers = calloc(max_header_count, sizeof(*request->headers));
    if (request->headers == NULL) {
        (void)snprintf(error, error_len, "%s", "header allocation failed");
        return 0;
    }
    while (cursor < header_end) {
        char *line_end = strstr(cursor, "\r\n");
        char *colon;
        const char *value;
        char *value_end;
        if (line_end == NULL || line_end > header_end) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP header line");
            return 0;
        }
        if (line_end == cursor) {
            break;
        }
        if (request->header_count >= max_header_count) {
            (void)snprintf(error, error_len, "%s", "too many HTTP headers");
            return 0;
        }
        *line_end = '\0';
        colon = strchr(cursor, ':');
        if (colon == NULL || colon == cursor) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP header");
            return 0;
        }
        *colon = '\0';
        value = colon + 1;
        while (*value == ' ' || *value == '\t') {
            ++value;
        }
        value_end = line_end;
        while (value_end > value &&
            (value_end[-1] == ' ' || value_end[-1] == '\t')) {
            *--value_end = '\0';
        }
        if (!valid_header_name(cursor) || !valid_header_value(value)) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP header syntax");
            return 0;
        }
        request->headers[request->header_count].name = cursor;
        request->headers[request->header_count].name_size = strlen(cursor);
        request->headers[request->header_count].value = value;
        request->headers[request->header_count].value_size = strlen(value);
        ++request->header_count;
        cursor = line_end + 2;
    }
    return 1;
}

static int header_value_equals(
    const msconnector_header *header,
    const char *expected) {
    size_t expected_size = strlen(expected);
    return header != NULL && header->value != NULL &&
        header->value_size == expected_size &&
        strncasecmp(header->value, expected, expected_size) == 0;
}

static int transfer_encoding_supported(const parsed_http_request *request) {
    size_t count = msconnector_headers_count_name(
        request->headers, request->header_count, "transfer-encoding");
    const msconnector_header *header = msconnector_headers_find_first(
        request->headers, request->header_count, "transfer-encoding");
    return count == 0U || (count == 1U && header_value_equals(header, "identity"));
}

static int read_request_body(
    const authorization_connection *connection,
    parsed_http_request *request,
    const char *body_start,
    size_t buffered_body_size,
    size_t body_limit,
    char *error,
    size_t error_len) {
    size_t content_length = 0U;
    size_t copied;
    int content_length_result;
    const msconnector_header *content_length_header;
    if (!transfer_encoding_supported(request)) {
        (void)snprintf(error, error_len, "%s", "chunked request bodies are unsupported");
        return 0;
    }
    content_length_header = msconnector_headers_find_first(
        request->headers, request->header_count, "content-length");
    if (content_length_header != NULL) {
        content_length_result = msconnector_headers_parse_content_length(
            request->headers, request->header_count, &content_length);
        if (content_length_result != 1) {
            (void)snprintf(error, error_len, "%s", "invalid content-length header");
            return 0;
        }
    }
    if (content_length > body_limit) {
        (void)snprintf(error, error_len, "%s", "request body exceeds configured limit");
        return 0;
    }
    if (content_length == 0U) {
        return 1;
    }
    request->body = malloc(content_length);
    if (request->body == NULL) {
        (void)snprintf(error, error_len, "%s", "request body allocation failed");
        return 0;
    }
    copied = buffered_body_size < content_length ? buffered_body_size : content_length;
    if (copied > 0U) {
        memcpy(request->body, body_start, copied);
    }
    while (copied < content_length) {
        const int received = recv_more(
            connection->socket_fd, request->body, content_length, &copied,
            connection->read_deadline);
        if (received != 1) {
            (void)snprintf(error, error_len, "%s",
                received < 0 ? "request body read timed out" : "incomplete request body");
            return 0;
        }
    }
    request->body_size = content_length;
    return 1;
}

static int read_http_request(
    const authorization_connection *connection,
    const authorization_request_limits *limits,
    parsed_http_request *request,
    char *error,
    size_t error_len) {
    size_t header_limit;
    size_t header_capacity;
    size_t used = 0U;
    const char *header_end;
    char *first_line_end;
    const char *body_start;
    size_t buffered_body_size;
    if (limits == NULL) {
        (void)snprintf(error, error_len, "%s", "request limits are unavailable");
        return 0;
    }
    header_limit = limits->total_header_limit;
    if (header_limit > SIZE_MAX - AUTH_REQUEST_LINE_OVERHEAD - 1U) {
        (void)snprintf(error, error_len, "%s", "configured header limit is too large");
        return 0;
    }
    header_capacity = header_limit + AUTH_REQUEST_LINE_OVERHEAD;
    request->header_buffer = malloc(header_capacity + 1U);
    if (request->header_buffer == NULL) {
        (void)snprintf(error, error_len, "%s", "request allocation failed");
        return 0;
    }
    header_end = NULL;
    while (header_end == NULL) {
        const int received = recv_more(
            connection->socket_fd, request->header_buffer, header_capacity, &used,
            connection->read_deadline);
        if (received != 1) {
            (void)snprintf(error, error_len, "%s",
                received < 0 ? "HTTP request headers timed out" :
                "incomplete HTTP request headers");
            return 0;
        }
        header_end = find_header_end(request->header_buffer, used);
        if (header_end == NULL && used == header_capacity) {
            (void)snprintf(error, error_len, "%s", "HTTP headers exceed configured limit");
            return 0;
        }
    }
    request->header_buffer[used] = '\0';
    request->header_buffer_size = used;
    first_line_end = strstr(request->header_buffer, "\r\n");
    if (first_line_end == NULL || first_line_end >= header_end) {
        (void)snprintf(error, error_len, "%s", "missing HTTP request line");
        return 0;
    }
    *first_line_end = '\0';
    if (!parse_request_line(request, request->header_buffer, error, error_len) ||
        !parse_header_lines(request, first_line_end, header_end,
            limits->header_count_limit, error, error_len)) {
        return 0;
    }
    body_start = header_end + 4;
    buffered_body_size = used - (size_t)(body_start - request->header_buffer);
    if (!read_request_body(connection, request, body_start, buffered_body_size,
            limits->body_limit,
            error, error_len)) {
        return 0;
    }
    if (inet_ntop(AF_INET, &connection->peer->sin_addr, request->client_address,
            sizeof(request->client_address)) == NULL ||
        inet_ntop(AF_INET, &connection->local->sin_addr, request->server_address,
            sizeof(request->server_address)) == NULL) {
        (void)snprintf(error, error_len, "%s", "endpoint address conversion failed");
        return 0;
    }
    request->client_port = (int)ntohs(connection->peer->sin_port);
    request->server_port = (int)ntohs(connection->local->sin_port);
    return 1;
}

static int copy_slice(
    const char *value,
    size_t value_size,
    char *destination,
    size_t destination_size) {
    if (value == NULL || destination == NULL || destination_size == 0U ||
        value_size >= destination_size) {
        return 0;
    }
    memcpy(destination, value, value_size);
    destination[value_size] = '\0';
    return 1;
}

static const char *request_uri(
    parsed_http_request *request,
    const msconnector_http_authorization_profile *profile) {
    for (size_t index = 0U; index < profile->original_uri_header_count; ++index) {
        const msconnector_header *header = msconnector_headers_find_first(
            request->headers, request->header_count,
            profile->original_uri_headers[index]);
        if (header != NULL && header->value_size > 0U &&
            copy_slice(header->value, header->value_size,
                request->uri_override, sizeof(request->uri_override)) &&
            request->uri_override[0] == '/') {
            return request->uri_override;
        }
    }
    return request->uri;
}

static const char *request_hostname(parsed_http_request *request) {
    const msconnector_header *host = msconnector_headers_find_first(
        request->headers, request->header_count, "host");
    if (host != NULL && host->value_size > 0U &&
        copy_slice(host->value, host->value_size,
            request->hostname, sizeof(request->hostname))) {
        return request->hostname;
    }
    return request->server_address;
}

static int send_all(
    int socket_fd,
    const char *data,
    size_t size,
    const connection_deadline *deadline) {
    size_t sent = 0U;
    while (sent < size) {
        ssize_t result;
        const int ready = wait_for_socket(socket_fd, POLLOUT, deadline);
        if (ready != 1) {
            return 0;
        }
        do {
            result = send(socket_fd, data + sent, size - sent, 0);
        } while (result < 0 && errno == EINTR && !authorization_stop);
        if (result < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
            continue;
        }
        if (result <= 0) {
            return 0;
        }
        sent += (size_t)result;
    }
    return 1;
}

static int send_response(
    int socket_fd,
    int status,
    const char *transaction_id,
    const char *decision_name,
    unsigned long timeout_ms) {
    char response[AUTH_RESPONSE_SIZE];
    connection_deadline deadline;
    const char *reason = msconnector_http_status_reason_phrase(status);
    const char *body = status >= 400 ? "request denied\n" : "request allowed\n";
    int written;
    if (!msconnector_http_status_is_valid(status)) {
        status = 500;
        reason = msconnector_http_status_reason_phrase(status);
        body = "authorization service error\n";
    }
    written = snprintf(response, sizeof(response),
        "HTTP/1.1 %d %s\r\n"
        "content-type: text/plain\r\n"
        "content-length: %zu\r\n"
        "connection: close\r\n"
        "x-msconnector-decision: %s\r\n"
        "x-msconnector-transaction-id: %s\r\n"
        "\r\n%s",
        status,
        reason,
        strlen(body),
        decision_name == NULL ? "error" : decision_name,
        transaction_id == NULL ? "unavailable" : transaction_id,
        body);
    if (written < 0 || (size_t)written >= sizeof(response)) {
        return 0;
    }
    return connection_deadline_init(&deadline, timeout_ms) &&
        send_all(socket_fd, response, (size_t)written, &deadline);
}

static int error_status_from_message(const char *message) {
    if (message != NULL && strstr(message, "timed out") != NULL) {
        return 408;
    }
    if (message != NULL && strstr(message, "body") != NULL &&
        strstr(message, "limit") != NULL) {
        return 413;
    }
    if (message != NULL &&
        (strstr(message, "header") != NULL || strstr(message, "Header") != NULL) &&
        (strstr(message, "limit") != NULL ||
         strstr(message, "exceed") != NULL ||
         strstr(message, "too many") != NULL)) {
        return 431;
    }
    if (message != NULL && strstr(message, "chunked") != NULL) {
        return 501;
    }
    return 400;
}

static void authorization_response_set_runtime_error(
    const authorization_service *service,
    const msconnector_error *common_error,
    authorization_response_state *response) {
    response->status = msconnector_runtime_error_http_status(
        service->runtime,
        common_error->code == MSCONNECTOR_ERROR_NONE
            ? MSCONNECTOR_ERROR_INTERNAL : common_error->code);
    response->decision_name = "runtime_error";
    response->success = 0;
}

static void authorization_response_set_decision(
    const msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    authorization_response_state *response) {
    const msconnector_decision_action action =
        msconnector_decision_action_from_decision(decision);
    const char *runtime_transaction_id =
        msconnector_runtime_transaction_id(transaction);
    response->decision_name = msconnector_decision_action_name(action);
    response->transaction_id = NULL;
    if (runtime_transaction_id != NULL) {
        const int copied = snprintf(response->copied_transaction_id,
            sizeof(response->copied_transaction_id), "%s", runtime_transaction_id);
        if (copied >= 0 && (size_t)copied < sizeof(response->copied_transaction_id)) {
            response->transaction_id = response->copied_transaction_id;
        }
    }
    if (action == MSCONNECTOR_DECISION_ACTION_ALLOW ||
        action == MSCONNECTOR_DECISION_ACTION_LOG_ONLY) {
        response->status = 200;
    } else {
        response->status = msconnector_decision_http_status(decision);
        if (!msconnector_http_status_is_valid(response->status)) {
            response->status = action == MSCONNECTOR_DECISION_ACTION_ERROR ? 500 : 403;
        }
    }
    response->success = 1;
}

static void authorization_process_runtime_request(
    authorization_service *service,
    const msconnector_generic_request_source *source,
    char *error,
    size_t error_len,
    authorization_response_state *response) {
    msconnector_request request;
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_decision decision;
    msconnector_error common_error;
    memset(&request, 0, sizeof(request));
    msconnector_error_init(&common_error);
    msconnector_decision_set_allow(&decision);
    response->transaction_id = NULL;
    if (!service->profile->map_request(source, &service->request_limits.mapper_contract,
            &request, error, error_len)) {
        response->status = 400;
        response->decision_name = "mapping_error";
        response->success = 0;
    } else if (!msconnector_runtime_transaction_begin(service->runtime, &request, NULL,
            &transaction, &decision, &common_error)) {
        authorization_response_set_runtime_error(service, &common_error, response);
    } else {
        authorization_response_set_decision(transaction, &decision, response);
    }
    if (transaction != NULL &&
        !msconnector_runtime_transaction_finish(transaction, &common_error)) {
        authorization_response_set_runtime_error(service, &common_error, response);
    }
    msconnector_runtime_transaction_destroy(&transaction);
}

static int handle_authorization_request(
    const authorization_connection *connection,
    authorization_service *service) {
    parsed_http_request parsed;
    msconnector_generic_request_source source;
    authorization_response_state response;
    char error[AUTH_ERROR_SIZE];

    if (connection == NULL || service == NULL || service->runtime == NULL ||
        service->profile == NULL) {
        return 0;
    }
    memset(&parsed, 0, sizeof(parsed));
    memset(&source, 0, sizeof(source));
    error[0] = '\0';
    if (!read_http_request(connection, &service->request_limits,
            &parsed, error, sizeof(error))) {
        const int status = error_status_from_message(error);
        (void)send_response(
            connection->socket_fd, status, NULL, "invalid_request",
            service->connection_timeout_ms);
        parsed_request_destroy(&parsed);
        return 0;
    }
    source.method = parsed.method;
    source.uri = request_uri(&parsed, service->profile);
    source.http_version = parsed.http_version;
    source.hostname = request_hostname(&parsed);
    source.client.address = parsed.client_address;
    source.client.port = parsed.client_port;
    source.server.address = parsed.server_address;
    source.server.port = parsed.server_port;
    source.headers = parsed.headers;
    source.header_count = parsed.header_count;
    source.body.data = parsed.body;
    source.body.size = parsed.body_size;
    if (pthread_mutex_lock(&service->runtime_lock) != 0) {
        (void)send_response(connection->socket_fd, 500, NULL, "runtime_error",
            service->connection_timeout_ms);
        parsed_request_destroy(&parsed);
        return 0;
    }
    authorization_process_runtime_request(service, &source, error, sizeof(error), &response);
    if (pthread_mutex_unlock(&service->runtime_lock) != 0) {
        parsed_request_destroy(&parsed);
        return 0;
    }
    if (!send_response(
            connection->socket_fd, response.status, response.transaction_id,
            response.decision_name,
            service->connection_timeout_ms)) {
        response.success = 0;
    }
    parsed_request_destroy(&parsed);
    return response.success;
}

static int create_listener(
    const char *listen_spec,
    int *listener,
    struct sockaddr_in *local,
    char *error,
    size_t error_len) {
    char host[AUTH_LISTEN_HOST_SIZE];
    int port;
    int enabled = 1;
    int socket_fd;
    if (!parse_listen_spec(listen_spec, host, sizeof(host), &port)) {
        (void)snprintf(error, error_len, "%s", "invalid --listen value");
        return 0;
    }
    memset(local, 0, sizeof(*local));
    local->sin_family = AF_INET;
    local->sin_port = htons((uint16_t)port);
    if (inet_pton(AF_INET, host, &local->sin_addr) != 1) {
        (void)snprintf(error, error_len, "%s", "invalid listen address");
        return 0;
    }
    socket_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        (void)snprintf(error, error_len, "socket failed: %s", strerror(errno));
        return 0;
    }
    if (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &enabled, sizeof(enabled)) != 0 ||
        bind(socket_fd, (const struct sockaddr *)local, sizeof(*local)) != 0 ||
        listen(socket_fd, 128) != 0) {
        (void)snprintf(error, error_len, "listen setup failed: %s", strerror(errno));
        (void)close(socket_fd);
        return 0;
    }
    *listener = socket_fd;
    return 1;
}

static int configure_client_socket(int socket_fd) {
    int flags;
    if (socket_fd < 0) {
        return 0;
    }
    flags = fcntl(socket_fd, F_GETFL, 0);
    return flags >= 0 && fcntl(socket_fd, F_SETFL, flags | O_NONBLOCK) == 0;
}

static int authorization_service_init(
    authorization_service *service,
    msconnector_runtime *runtime,
    const msconnector_http_authorization_profile *profile,
    const authorization_cli *cli) {
    if (service == NULL || runtime == NULL || profile == NULL || cli == NULL ||
        cli->max_connections == 0UL ||
        cli->max_connections > AUTH_MAX_CONNECTIONS_MAX) {
        return 0;
    }
    memset(service, 0, sizeof(*service));
    service->runtime = runtime;
    service->profile = profile;
    service->connection_timeout_ms = cli->connection_timeout_ms;
    service->max_connections = cli->max_connections;
    msconnector_runtime_request_contract(runtime, &service->request_limits.mapper_contract);
    service->request_limits.body_limit =
        msconnector_runtime_request_body_limit(runtime);
    service->request_limits.total_header_limit =
        msconnector_runtime_total_header_limit(runtime);
    service->request_limits.header_count_limit =
        msconnector_runtime_header_count_limit(runtime);
    if (pthread_mutex_init(&service->runtime_lock, NULL) != 0) {
        return 0;
    }
    if (pthread_mutex_init(&service->worker_lock, NULL) != 0) {
        (void)pthread_mutex_destroy(&service->runtime_lock);
        return 0;
    }
    if (pthread_cond_init(&service->workers_idle, NULL) != 0) {
        (void)pthread_mutex_destroy(&service->worker_lock);
        (void)pthread_mutex_destroy(&service->runtime_lock);
        return 0;
    }
    return 1;
}

static void authorization_service_destroy(authorization_service *service) {
    if (service == NULL) {
        return;
    }
    (void)pthread_cond_destroy(&service->workers_idle);
    (void)pthread_mutex_destroy(&service->worker_lock);
    (void)pthread_mutex_destroy(&service->runtime_lock);
    memset(service, 0, sizeof(*service));
}

static void authorization_worker_release(authorization_worker *worker) {
    authorization_service *service;
    if (worker == NULL) {
        return;
    }
    service = worker->service;
    if (service != NULL && pthread_mutex_lock(&service->worker_lock) == 0) {
        authorization_worker **current = &service->workers;
        while (*current != NULL && *current != worker) {
            current = &(*current)->next;
        }
        if (*current == worker) {
            *current = worker->next;
            if (service->active_workers > 0UL) {
                --service->active_workers;
            }
            (void)pthread_cond_broadcast(&service->workers_idle);
        }
        (void)pthread_mutex_unlock(&service->worker_lock);
    }
    if (worker->socket_fd >= 0) {
        (void)close(worker->socket_fd);
    }
    free(worker);
}

static void *authorization_worker_main(void *argument) {
    authorization_worker *worker = argument;
    authorization_connection connection;
    if (worker == NULL) {
        return NULL;
    }
    connection.socket_fd = worker->socket_fd;
    connection.peer = &worker->peer;
    connection.local = &worker->local;
    connection.read_deadline = &worker->read_deadline;
    (void)handle_authorization_request(&connection, worker->service);
    authorization_worker_release(worker);
    return NULL;
}

static int authorization_start_worker(
    authorization_service *service,
    int socket_fd,
    const struct sockaddr_in *peer,
    const struct sockaddr_in *local,
    const connection_deadline *read_deadline) {
    authorization_worker *worker;
    pthread_attr_t attributes;
    pthread_t thread;
    int result;
    if (service == NULL || socket_fd < 0 || peer == NULL || local == NULL ||
        read_deadline == NULL) {
        if (socket_fd >= 0) {
            (void)close(socket_fd);
        }
        return -1;
    }
    worker = calloc(1U, sizeof(*worker));
    if (worker == NULL) {
        (void)close(socket_fd);
        return -1;
    }
    worker->service = service;
    worker->socket_fd = socket_fd;
    worker->peer = *peer;
    worker->local = *local;
    worker->read_deadline = *read_deadline;
    if (pthread_mutex_lock(&service->worker_lock) != 0) {
        (void)close(socket_fd);
        free(worker);
        return -1;
    }
    if (service->active_workers >= service->max_connections) {
        (void)pthread_mutex_unlock(&service->worker_lock);
        (void)close(socket_fd);
        free(worker);
        return 0;
    }
    worker->next = service->workers;
    service->workers = worker;
    ++service->active_workers;
    (void)pthread_mutex_unlock(&service->worker_lock);
    if (pthread_attr_init(&attributes) != 0) {
        authorization_worker_release(worker);
        return -1;
    }
    result = pthread_attr_setdetachstate(&attributes, PTHREAD_CREATE_DETACHED);
    if (result == 0) {
        result = pthread_create(&thread, &attributes, authorization_worker_main, worker);
    }
    (void)pthread_attr_destroy(&attributes);
    if (result != 0) {
        authorization_worker_release(worker);
        return -1;
    }
    return 1;
}

static void authorization_shutdown_workers(authorization_service *service) {
    if (service == NULL || pthread_mutex_lock(&service->worker_lock) != 0) {
        return;
    }
    for (authorization_worker *worker = service->workers;
        worker != NULL; worker = worker->next) {
        (void)shutdown(worker->socket_fd, SHUT_RDWR);
    }
    (void)pthread_mutex_unlock(&service->worker_lock);
}

static int authorization_wait_for_workers(authorization_service *service) {
    int result;
    if (service == NULL || pthread_mutex_lock(&service->worker_lock) != 0) {
        return 0;
    }
    result = 0;
    while (service->active_workers > 0UL && result == 0) {
        result = pthread_cond_wait(&service->workers_idle, &service->worker_lock);
    }
    if (pthread_mutex_unlock(&service->worker_lock) != 0) {
        return 0;
    }
    return result == 0;
}

static authorization_listener_iteration authorization_wait_for_listener(
    int listener,
    const char *connector_name) {
    struct pollfd listener_descriptor;
    int listener_ready;
    memset(&listener_descriptor, 0, sizeof(listener_descriptor));
    listener_descriptor.fd = listener;
    listener_descriptor.events = POLLIN;
    do {
        listener_ready = poll(&listener_descriptor, 1U,
            AUTH_LISTENER_POLL_TIMEOUT_MS);
    } while (listener_ready < 0 && errno == EINTR && !authorization_stop);
    if (listener_ready == 0) {
        return AUTHORIZATION_LISTENER_RETRY;
    }
    if (authorization_stop) {
        return AUTHORIZATION_LISTENER_STOP;
    }
    if (listener_ready < 0 || (listener_descriptor.revents & POLLIN) == 0) {
        (void)fprintf(stderr, "%s listener poll failed: %s\n",
            connector_name,
            listener_ready < 0 ? strerror(errno) : "unexpected listener state");
        return AUTHORIZATION_LISTENER_ERROR;
    }
    return AUTHORIZATION_LISTENER_READY;
}

static authorization_listener_iteration authorization_serve_next_connection(
    authorization_service *service,
    int listener,
    const struct sockaddr_in *local) {
    struct sockaddr_in peer = {0};
    socklen_t peer_size = sizeof(peer);
    connection_deadline read_deadline;
    authorization_listener_iteration listener_state =
        authorization_wait_for_listener(listener, service->profile->connector_name);
    int client_fd;
    if (listener_state != AUTHORIZATION_LISTENER_READY) {
        return listener_state;
    }
    do {
        client_fd = accept(listener, (struct sockaddr *)&peer, &peer_size);
    } while (client_fd < 0 && errno == EINTR && !authorization_stop);
    if (client_fd < 0) {
        if (authorization_stop) {
            return AUTHORIZATION_LISTENER_STOP;
        }
        (void)fprintf(stderr, "%s accept failed: %s\n",
            service->profile->connector_name, strerror(errno));
        return AUTHORIZATION_LISTENER_ERROR;
    }
    if (!connection_deadline_init(
            &read_deadline, service->connection_timeout_ms) ||
        !configure_client_socket(client_fd)) {
        (void)fprintf(stderr, "%s client socket deadline setup failed: %s\n",
            service->profile->connector_name, strerror(errno));
        (void)close(client_fd);
        return AUTHORIZATION_LISTENER_HANDLED;
    }
    if (authorization_start_worker(
            service, client_fd, &peer, local, &read_deadline) < 0) {
        (void)fprintf(stderr, "%s worker start failed\n",
            service->profile->connector_name);
    }
    return AUTHORIZATION_LISTENER_HANDLED;
}

static int authorization_serve_requests(
    authorization_service *service,
    int listener,
    const struct sockaddr_in *local,
    unsigned long max_requests) {
    unsigned long handled = 0UL;
    while (!authorization_stop && (max_requests == 0UL || handled < max_requests)) {
        const authorization_listener_iteration listener_state =
            authorization_serve_next_connection(service, listener, local);
        if (listener_state == AUTHORIZATION_LISTENER_ERROR) {
            return 1;
        }
        if (listener_state == AUTHORIZATION_LISTENER_STOP) {
            return 0;
        }
        if (listener_state == AUTHORIZATION_LISTENER_HANDLED) {
            ++handled;
        }
    }
    return 0;
}

static int serve_authorization(
    const authorization_cli *cli,
    const msconnector_http_authorization_profile *profile) {
    msconnector_runtime *runtime = NULL;
    authorization_service service;
    struct sockaddr_in local = {0};
    int listener = -1;
    int service_status = 0;
    char error[AUTH_ERROR_SIZE];
    struct sigaction action;

    error[0] = '\0';
    if (!msconnector_runtime_create(profile->connector_name, cli->config_path,
            &runtime, error, sizeof(error))) {
        (void)fprintf(stderr, "%s config/start failed: %s\n",
            profile->connector_name, error);
        return 1;
    }
    if (!authorization_service_init(&service, runtime, profile, cli)) {
        (void)fprintf(stderr, "%s service synchronization setup failed\n",
            profile->connector_name);
        msconnector_runtime_destroy(&runtime);
        return 1;
    }
    if (!create_listener(cli->listen_spec, &listener, &local, error, sizeof(error))) {
        (void)fprintf(stderr, "%s service start failed: %s\n",
            profile->connector_name, error);
        authorization_service_destroy(&service);
        msconnector_runtime_destroy(&runtime);
        return 1;
    }
    memset(&action, 0, sizeof(action));
    action.sa_handler = stop_service;
    (void)sigemptyset(&action.sa_mask);
    (void)sigaction(SIGTERM, &action, NULL);
    (void)sigaction(SIGINT, &action, NULL);
    (void)signal(SIGPIPE, SIG_IGN);
    (void)printf("connector=%s integration_mode=%s listen=%s status=ready\n",
        profile->connector_name, profile->integration_mode, cli->listen_spec);
    (void)fflush(stdout);
    service_status = authorization_serve_requests(
        &service, listener, &local, cli->max_requests);
    if (listener >= 0) {
        (void)close(listener);
    }
    if (authorization_stop || service_status != 0) {
        authorization_shutdown_workers(&service);
    }
    if (!authorization_wait_for_workers(&service)) {
        (void)fprintf(stderr, "%s worker shutdown failed\n",
            profile->connector_name);
        authorization_shutdown_workers(&service);
        abort();
    }
    authorization_service_destroy(&service);
    msconnector_runtime_destroy(&runtime);
    return service_status;
}

int msconnector_http_authorization_service_main(
    int argc,
    char **argv,
    const msconnector_http_authorization_profile *profile) {
    authorization_cli cli;
    char error[AUTH_ERROR_SIZE];
    if (!validate_profile(profile) || !parse_cli(argc, argv, &cli)) {
        print_usage(argc > 0 && argv != NULL ? argv[0] : "authorization-service");
        return 2;
    }
    if (cli.check_config) {
        error[0] = '\0';
        if (!msconnector_runtime_config_check(profile->connector_name,
                cli.config_path, error, sizeof(error))) {
            (void)fprintf(stderr, "%s config invalid: %s\n",
                profile->connector_name, error);
            return 1;
        }
        (void)printf("connector=%s integration_mode=%s config_status=valid\n",
            profile->connector_name, profile->integration_mode);
        return 0;
    }
    return serve_authorization(&cli, profile);
}
