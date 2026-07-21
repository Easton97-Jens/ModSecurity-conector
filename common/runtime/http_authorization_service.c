#define _POSIX_C_SOURCE 200809L

#include "http_authorization_service.h"
#include "msconnector_runtime.h"

#include "msconnector/decision_action.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include "msconnector/request_helpers.h"

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <netinet/in.h>
#include <poll.h>
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

typedef struct authorization_cli {
    const char *config_path;
    const char *listen_spec;
    int check_config;
    int serve;
    unsigned long max_requests;
    unsigned long connection_timeout_ms;
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

static volatile sig_atomic_t authorization_stop = 0;

static void stop_service(int signal_number) {
    (void)signal_number;
    authorization_stop = 1;
}

static void print_usage(const char *program) {
    (void)fprintf(stderr,
        "usage: %s --check-config --config PATH\n"
        "       %s --serve --config PATH --listen HOST:PORT [--max-requests N] "
        "[--connection-timeout-ms N]\n",
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

static int parse_cli(int argc, char **argv, authorization_cli *cli) {
    int index;
    memset(cli, 0, sizeof(*cli));
    cli->connection_timeout_ms = AUTH_CONNECTION_TIMEOUT_DEFAULT_MS;
    for (index = 1; index < argc; ++index) {
        if (strcmp(argv[index], "--check-config") == 0) {
            cli->check_config = 1;
        } else if (strcmp(argv[index], "--serve") == 0) {
            cli->serve = 1;
        } else if (strcmp(argv[index], "--config") == 0 && index + 1 < argc) {
            cli->config_path = argv[++index];
        } else if (strcmp(argv[index], "--listen") == 0 && index + 1 < argc) {
            cli->listen_spec = argv[++index];
        } else if (strcmp(argv[index], "--max-requests") == 0 && index + 1 < argc) {
            if (!parse_unsigned_long(argv[++index], &cli->max_requests)) {
                return 0;
            }
        } else if (strcmp(argv[index], "--connection-timeout-ms") == 0 &&
            index + 1 < argc) {
            if (!parse_unsigned_long(argv[++index], &cli->connection_timeout_ms) ||
                cli->connection_timeout_ms == 0UL ||
                cli->connection_timeout_ms > AUTH_CONNECTION_TIMEOUT_MAX_MS) {
                return 0;
            }
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
    for (char *cursor = request->method; *cursor != '\0'; ++cursor) {
        if (!http_token_character((unsigned char)*cursor)) {
            (void)snprintf(error, error_len, "%s", "invalid HTTP method");
            return 0;
        }
    }
    for (char *cursor = request->uri; *cursor != '\0'; ++cursor) {
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
    char *first_line_end,
    char *header_end,
    size_t max_header_count,
    char *error,
    size_t error_len) {
    char *cursor = first_line_end + 2;
    request->headers = calloc(max_header_count, sizeof(*request->headers));
    if (request->headers == NULL) {
        (void)snprintf(error, error_len, "%s", "header allocation failed");
        return 0;
    }
    while (cursor < header_end) {
        char *line_end = strstr(cursor, "\r\n");
        char *colon;
        char *value;
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
    int socket_fd,
    parsed_http_request *request,
    const char *body_start,
    size_t buffered_body_size,
    size_t body_limit,
    const connection_deadline *deadline,
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
            socket_fd, request->body, content_length, &copied, deadline);
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
    int socket_fd,
    msconnector_runtime *runtime,
    parsed_http_request *request,
    const struct sockaddr_in *peer,
    const struct sockaddr_in *local,
    const connection_deadline *deadline,
    char *error,
    size_t error_len) {
    size_t header_limit = msconnector_runtime_total_header_limit(runtime);
    size_t header_capacity;
    size_t used = 0U;
    char *header_end;
    char *first_line_end;
    char *body_start;
    size_t buffered_body_size;
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
            socket_fd, request->header_buffer, header_capacity, &used, deadline);
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
            msconnector_runtime_header_count_limit(runtime), error, error_len)) {
        return 0;
    }
    body_start = header_end + 4;
    buffered_body_size = used - (size_t)(body_start - request->header_buffer);
    if (!read_request_body(socket_fd, request, body_start, buffered_body_size,
            msconnector_runtime_request_body_limit(runtime), deadline,
            error, error_len)) {
        return 0;
    }
    if (inet_ntop(AF_INET, &peer->sin_addr, request->client_address,
            sizeof(request->client_address)) == NULL ||
        inet_ntop(AF_INET, &local->sin_addr, request->server_address,
            sizeof(request->server_address)) == NULL) {
        (void)snprintf(error, error_len, "%s", "endpoint address conversion failed");
        return 0;
    }
    request->client_port = (int)ntohs(peer->sin_port);
    request->server_port = (int)ntohs(local->sin_port);
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

static int handle_authorization_request(
    int client_fd,
    msconnector_runtime *runtime,
    const msconnector_http_authorization_profile *profile,
    const struct sockaddr_in *peer,
    const struct sockaddr_in *local,
    const connection_deadline *read_deadline,
    unsigned long timeout_ms) {
    parsed_http_request parsed;
    msconnector_generic_request_source source;
    msconnector_request_mapper_contract contract;
    msconnector_request request;
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_decision decision;
    msconnector_error common_error;
    char error[AUTH_ERROR_SIZE];
    int status = 500;
    int success = 0;
    const char *transaction_id = NULL;
    const char *decision_name = "error";

    memset(&parsed, 0, sizeof(parsed));
    memset(&source, 0, sizeof(source));
    error[0] = '\0';
    msconnector_error_init(&common_error);
    msconnector_decision_set_allow(&decision);
    if (!read_http_request(client_fd, runtime, &parsed, peer, local,
            read_deadline, error, sizeof(error))) {
        status = error_status_from_message(error);
        (void)send_response(
            client_fd, status, NULL, "invalid_request", timeout_ms);
        parsed_request_destroy(&parsed);
        return 0;
    }
    source.method = parsed.method;
    source.uri = request_uri(&parsed, profile);
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
    msconnector_runtime_request_contract(runtime, &contract);
    if (!profile->map_request(&source, &contract, &request, error, sizeof(error))) {
        status = 400;
        decision_name = "mapping_error";
    } else if (!msconnector_runtime_transaction_begin(runtime, &request, NULL,
            &transaction, &decision, &common_error)) {
        status = common_error.code == MSCONNECTOR_ERROR_NONE
            ? msconnector_runtime_error_http_status(runtime, MSCONNECTOR_ERROR_INTERNAL)
            : msconnector_runtime_error_http_status(runtime, common_error.code);
        decision_name = "runtime_error";
    } else {
        msconnector_decision_action action =
            msconnector_decision_action_from_decision(&decision);
        transaction_id = msconnector_runtime_transaction_id(transaction);
        decision_name = msconnector_decision_action_name(action);
        if (action == MSCONNECTOR_DECISION_ACTION_ALLOW ||
            action == MSCONNECTOR_DECISION_ACTION_LOG_ONLY) {
            status = 200;
        } else {
            status = msconnector_decision_http_status(&decision);
            if (!msconnector_http_status_is_valid(status)) {
                status = action == MSCONNECTOR_DECISION_ACTION_ERROR ? 500 : 403;
            }
        }
        success = 1;
    }
    if (transaction != NULL) {
        if (!msconnector_runtime_transaction_finish(transaction, &common_error)) {
            status = msconnector_runtime_error_http_status(
                runtime,
                common_error.code == MSCONNECTOR_ERROR_NONE
                    ? MSCONNECTOR_ERROR_INTERNAL : common_error.code);
            decision_name = "runtime_error";
            success = 0;
        }
    }
    if (!send_response(
            client_fd, status, transaction_id, decision_name, timeout_ms)) {
        success = 0;
    }
    msconnector_runtime_transaction_destroy(&transaction);
    parsed_request_destroy(&parsed);
    return success;
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

static int serve_authorization(
    const authorization_cli *cli,
    const msconnector_http_authorization_profile *profile) {
    msconnector_runtime *runtime = NULL;
    struct sockaddr_in local = {0};
    int listener = -1;
    char error[AUTH_ERROR_SIZE];
    unsigned long handled = 0UL;
    struct sigaction action;

    error[0] = '\0';
    if (!msconnector_runtime_create(profile->connector_name, cli->config_path,
            &runtime, error, sizeof(error))) {
        (void)fprintf(stderr, "%s config/start failed: %s\n",
            profile->connector_name, error);
        return 1;
    }
    if (!create_listener(cli->listen_spec, &listener, &local, error, sizeof(error))) {
        (void)fprintf(stderr, "%s service start failed: %s\n",
            profile->connector_name, error);
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
    while (!authorization_stop &&
        (cli->max_requests == 0UL || handled < cli->max_requests)) {
        struct sockaddr_in peer = {0};
        socklen_t peer_size = sizeof(peer);
        int client_fd;
        connection_deadline read_deadline;
        do {
            client_fd = accept(listener, (struct sockaddr *)&peer, &peer_size);
        } while (client_fd < 0 && errno == EINTR && !authorization_stop);
        if (client_fd < 0) {
            if (authorization_stop) {
                break;
            }
            (void)fprintf(stderr, "%s accept failed: %s\n",
                profile->connector_name, strerror(errno));
            (void)close(listener);
            msconnector_runtime_destroy(&runtime);
            return 1;
        }
        if (!connection_deadline_init(
                &read_deadline, cli->connection_timeout_ms) ||
            !configure_client_socket(client_fd)) {
            (void)fprintf(stderr, "%s client socket deadline setup failed: %s\n",
                profile->connector_name, strerror(errno));
            (void)close(client_fd);
            ++handled;
            continue;
        }
        (void)handle_authorization_request(
            client_fd, runtime, profile, &peer, &local,
            &read_deadline, cli->connection_timeout_ms);
        (void)close(client_fd);
        ++handled;
    }
    (void)close(listener);
    msconnector_runtime_destroy(&runtime);
    return 0;
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
