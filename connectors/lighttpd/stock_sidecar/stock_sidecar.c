#define _POSIX_C_SOURCE 200809L

#include "stock_sidecar.h"

#include "msconnector_runtime.h"
#include "msconnector/decision_action.h"
#include "msconnector/generic_mapper.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"
#include "msconnector/transaction_contract.h"
#include "connectors/profile_registry.h"

#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netdb.h>
#include <openssl/sha.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>

#define SIDECAR_NAME "lighttpd-stock-sidecar"
#define SIDECAR_RUNTIME_CONNECTOR "lighttpd"
#define SIDECAR_HEADER_BUFFER (128U * 1024U)
#define SIDECAR_IO_CHUNK (2U * 1024U)
#define SIDECAR_DEFAULT_TIMEOUT_MS 10000U
#define SIDECAR_BACKLOG 64
#define SIDECAR_MAX_PARALLEL 16U
#define SIDECAR_RECEIPT_HEX_SIZE (SHA256_DIGEST_LENGTH * 2U)
#define SIDECAR_RECEIPT_BINDING_SIZE 64U

typedef struct sidecar_options {
    const char *config;
    const char *listen;
    const char *upstream;
    uint64_t timeout_ms;
} sidecar_options;

typedef struct sidecar_runtime_context {
    const sidecar_options *options;
    msconnector_runtime *runtime;
    unsigned int active;
    pthread_mutex_t lock;
} sidecar_runtime_context;

typedef struct sidecar_worker {
    sidecar_runtime_context *context;
    int client;
} sidecar_worker;

typedef enum sidecar_failure_origin {
    SIDECAR_FAILURE_CONNECTOR = 0,
    SIDECAR_FAILURE_CLIENT,
    SIDECAR_FAILURE_UPSTREAM,
    SIDECAR_FAILURE_PROTOCOL
} sidecar_failure_origin;

typedef struct sidecar_headers {
    char *storage;
    size_t storage_size;
    msconnector_header *items;
    char method[32];
    char uri[MSCONNECTOR_TRANSACTION_CONTRACT_URI_SIZE];
    char version[16];
    size_t count;
    size_t content_length;
    int has_content_length;
    int chunked;
    int upgrade;
    size_t host_count;
    int status_code;
    int no_body;
} sidecar_headers;

typedef struct sidecar_deadline {
    uint64_t at_ms;
} sidecar_deadline;

static uint64_t sidecar_now_ms(void) {
    struct timespec value;
    (void)clock_gettime(CLOCK_MONOTONIC, &value);
    return (uint64_t)value.tv_sec * 1000U + (uint64_t)value.tv_nsec / 1000000U;
}

static int sidecar_remaining(const sidecar_deadline *deadline) {
    uint64_t now = sidecar_now_ms();
    uint64_t remaining;
    if (deadline == NULL || deadline->at_ms <= now) {
        return 0;
    }
    remaining = deadline->at_ms - now;
    return remaining > (uint64_t)INT32_MAX ? INT32_MAX : (int)remaining;
}

static int sidecar_wait(int fd, short events, const sidecar_deadline *deadline) {
    struct pollfd descriptor;
    int result;
    memset(&descriptor, 0, sizeof(descriptor));
    descriptor.fd = fd;
    descriptor.events = events;
    do {
        result = poll(&descriptor, 1U, sidecar_remaining(deadline));
    } while (result < 0 && errno == EINTR && sidecar_remaining(deadline) > 0);
    if (result <= 0 || (descriptor.revents & (events | POLLERR | POLLHUP)) == 0) {
        return 0;
    }
    return 1;
}

static int sidecar_send_all_observed(int fd, const unsigned char *data, size_t size,
                                     const sidecar_deadline *deadline,
                                     size_t *bytes_sent) {
    size_t offset = 0U;
    if (bytes_sent != NULL) *bytes_sent = 0U;
    while (offset < size) {
        ssize_t written;
        if (!sidecar_wait(fd, POLLOUT, deadline)) {
            return 0;
        }
        do {
            written = send(fd, data + offset, size - offset,
                           MSG_NOSIGNAL | MSG_DONTWAIT);
        } while (written < 0 && errno == EINTR && sidecar_remaining(deadline) > 0);
        if (written > 0) {
            offset += (size_t)written;
            if (bytes_sent != NULL) *bytes_sent = offset;
            continue;
        }
        if (written < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) {
            continue;
        }
        if (written <= 0) {
            return 0;
        }
    }
    return 1;
}

static int sidecar_send_all(int fd, const unsigned char *data, size_t size,
                            const sidecar_deadline *deadline) {
    return sidecar_send_all_observed(fd, data, size, deadline, NULL);
}

static int sidecar_recv_some_with_flags(int fd, unsigned char *data,
                                        size_t capacity,
                                        const sidecar_deadline *deadline,
                                        size_t *received, int flags) {
    ssize_t result;
    if (received == NULL || capacity == 0U) {
        return 0;
    }
    for (;;) {
        if (!sidecar_wait(fd, POLLIN, deadline)) return 0;
        do {
            result = recv(fd, data, capacity, MSG_DONTWAIT | flags);
        } while (result < 0 && errno == EINTR && sidecar_remaining(deadline) > 0);
        if (result > 0) {
            *received = (size_t)result;
            return 1;
        }
        if (result < 0 && (errno == EAGAIN || errno == EWOULDBLOCK)) continue;
        return 0;
    }
}

static int sidecar_recv_some(int fd, unsigned char *data, size_t capacity,
                             const sidecar_deadline *deadline, size_t *received) {
    return sidecar_recv_some_with_flags(fd, data, capacity, deadline, received, 0);
}

/* Peek before consuming a header block so a bounded read never discards the
 * first bytes of a following informational or final response. */
static int sidecar_peek_some(int fd, unsigned char *data, size_t capacity,
                             const sidecar_deadline *deadline, size_t *received) {
    return sidecar_recv_some_with_flags(fd, data, capacity, deadline, received,
                                        MSG_PEEK);
}

static void sidecar_headers_release(sidecar_headers *headers) {
    if (headers != NULL) {
        free(headers->items);
        memset(headers, 0, sizeof(*headers));
    }
}

static char *sidecar_trim(char *value) {
    char *end;
    while (*value == ' ' || *value == '\t') {
        ++value;
    }
    end = value + strlen(value);
    while (end > value && (end[-1] == ' ' || end[-1] == '\t')) {
        --end;
    }
    *end = '\0';
    return value;
}

static int sidecar_decimal(const char *value, size_t *out) {
    char *end = NULL;
    unsigned long long number;
    errno = 0;
    number = strtoull(value, &end, 10);
    if (errno != 0 || end == value || *end != '\0' || number > SIZE_MAX) {
        return 0;
    }
    *out = (size_t)number;
    return 1;
}

static int sidecar_token(const char *value) {
    const unsigned char *cursor = (const unsigned char *)value;
    if (*cursor == '\0') return 0;
    while (*cursor != '\0') {
        if (!((*cursor >= 'a' && *cursor <= 'z') || (*cursor >= 'A' && *cursor <= 'Z') ||
              (*cursor >= '0' && *cursor <= '9') || strchr("!#$%&'*+-.^_`|~", *cursor) != NULL)) return 0;
        ++cursor;
    }
    return 1;
}

static int sidecar_safe_text(const char *value) {
    const unsigned char *cursor = (const unsigned char *)value;
    while (*cursor != '\0') {
        if (*cursor < 0x20U || *cursor == 0x7fU) return 0;
        ++cursor;
    }
    return 1;
}

static int sidecar_hop_by_hop(const char *name) {
    return strcasecmp(name, "Proxy-Connection") == 0 ||
        strcasecmp(name, "TE") == 0 || strcasecmp(name, "Trailer") == 0 ||
        strcasecmp(name, "Transfer-Encoding") == 0 || strcasecmp(name, "Upgrade") == 0;
}

static int sidecar_connection_value_allowed(const char *value) {
    char copy[128];
    char *cursor;
    if (strlen(value) >= sizeof(copy)) return 0;
    (void)snprintf(copy, sizeof(copy), "%s", value);
    cursor = copy;
    for (;;) {
        char *comma = strchr(cursor, ',');
        if (comma != NULL) *comma = '\0';
        cursor = sidecar_trim(cursor);
        if (cursor[0] == '\0' ||
            (strcasecmp(cursor, "close") != 0 &&
             strcasecmp(cursor, "keep-alive") != 0)) return 0;
        if (comma == NULL) return 1;
        cursor = comma + 1;
    }
}

static int sidecar_private_spec(const char *spec) {
    static const char loopback_prefix[] = "127.0.0.1:";
    size_t port;

    /* This HTTP/1.1 bridge has no TLS or peer-authentication layer.  Keep
     * both endpoints literal IPv4 loopback addresses instead of relying on a
     * resolver-controlled hostname or a wildcard binding. */
    return spec != NULL && strncmp(spec, loopback_prefix,
        sizeof(loopback_prefix) - 1U) == 0 &&
        sidecar_decimal(spec + sizeof(loopback_prefix) - 1U, &port) &&
        port > 0U && port <= 65535U;
}

static int sidecar_parse_request_start(char *line, char **method, char **uri,
                                       char **version) {
    char *first = strchr(line, ' ');
    char *second;
    if (first == NULL || first == line || first[1] == '\0') return 0;
    second = strchr(first + 1, ' ');
    if (second == NULL || second == first + 1 || second[1] == '\0' || strchr(second + 1, ' ') != NULL) return 0;
    *first = '\0';
    *second = '\0';
    *method = line;
    *uri = first + 1;
    *version = second + 1;
    return strcmp(*version, "HTTP/1.1") == 0 && sidecar_token(*method) && sidecar_safe_text(*uri);
}

static int sidecar_parse_response_start(char *line, char **version, int *status) {
    char *space = strchr(line, ' ');
    char *reason;
    const char *mutable_end;
    const char *end;
    size_t value;
    if (space == NULL || space == line || space[1] == '\0') return 0;
    *space = '\0';
    mutable_end = space + 1;
    end = mutable_end;
    reason = strchr(mutable_end, ' ');
    if (reason != NULL) {
        *reason = '\0';
        if (!sidecar_safe_text(reason + 1)) return 0;
    }
    if (!sidecar_decimal(end, &value) || value < 100U || value > 599U) return 0;
    *version = line;
    *status = (int)value;
    return strcmp(*version, "HTTP/1.1") == 0;
}

static int sidecar_parse_header_field(char *line, size_t line_size,
                                      int is_request, sidecar_headers *out,
                                      size_t count) {
    char *colon;
    if (line == NULL || line_size == 0U) return 0;
    line[line_size] = '\0';
    colon = strchr(line, ':');
    if (colon == NULL || colon == line) return 0;
    *colon = '\0';
    if (!sidecar_token(line)) return 0;
    out->items[count].name = line;
    out->items[count].name_size = strlen(line);
    out->items[count].value = sidecar_trim(colon + 1);
    out->items[count].value_size = strlen(out->items[count].value);
    if (!sidecar_safe_text(out->items[count].value) || sidecar_hop_by_hop(line)) return 0;
    if (strcasecmp(line, "Connection") == 0 &&
        !sidecar_connection_value_allowed(out->items[count].value)) return 0;
    if (strcasecmp(line, "Content-Length") == 0) {
        size_t length;
        if (out->has_content_length ||
            !sidecar_decimal(out->items[count].value, &length)) return 0;
        if (!is_request && out->status_code == 204 && length != 0U) return 0;
        out->content_length = length;
        out->has_content_length = 1;
    } else if (strcasecmp(line, "Host") == 0) {
        if (out->items[count].value[0] == '\0') return 0;
        ++out->host_count;
    }
    return 1;
}

static int sidecar_parse_request_headers_start(char *cursor, sidecar_headers *out) {
    char *parsed_method;
    char *parsed_uri;
    char *parsed_version;
    if (!sidecar_parse_request_start(cursor, &parsed_method, &parsed_uri, &parsed_version) ||
        strlen(parsed_method) >= sizeof(out->method) ||
        strlen(parsed_uri) >= sizeof(out->uri) ||
        strlen(parsed_version) >= sizeof(out->version)) {
        return 0;
    }
    (void)snprintf(out->method, sizeof(out->method), "%s", parsed_method);
    (void)snprintf(out->uri, sizeof(out->uri), "%s", parsed_uri);
    (void)snprintf(out->version, sizeof(out->version), "%s", parsed_version);
    return 1;
}

static int sidecar_parse_response_headers_start(char *cursor, int response_no_body,
                                                sidecar_headers *out) {
    int status;
    char version[16];
    char start_line[1024];
    char *parsed_version;
    size_t start_size = strlen(cursor);
    if (start_size == 0U || start_size >= sizeof(start_line)) return 0;
    (void)snprintf(start_line, sizeof(start_line), "%s", cursor);
    if (!sidecar_parse_response_start(start_line, &parsed_version, &status) ||
        strlen(parsed_version) >= sizeof(version) || !sidecar_safe_text(start_line)) {
        return 0;
    }
    (void)snprintf(version, sizeof(version), "%s", parsed_version);
    (void)snprintf(out->version, sizeof(out->version), "%s", version);
    out->status_code = status;
    out->no_body = response_no_body || status < 200 || status == 204 || status == 304;
    return 1;
}

static int sidecar_parse_header_lines(char *cursor, size_t count_limit,
                                      int is_request, sidecar_headers *out) {
    size_t count = 0U;
    while (*cursor != '\r') {
        char *line_end = strstr(cursor, "\r\n");
        size_t line_size = 0U;
        if (line_end != NULL) line_size = (size_t)(line_end - cursor);
        if (line_end == NULL || count == count_limit ||
            !sidecar_parse_header_field(cursor, line_size, is_request, out, count)) {
            sidecar_headers_release(out);
            return 0;
        }
        ++count;
        cursor = line_end + 2;
    }
    out->count = count;
    return 1;
}

static int sidecar_headers_has_name(const sidecar_headers *headers,
                                    const char *name) {
    if (headers == NULL || name == NULL) return 0;
    for (size_t index = 0U; index < headers->count; ++index) {
        if (strcasecmp(headers->items[index].name, name) == 0) return 1;
    }
    return 0;
}

/* Parses an already complete header block. CR/LF framing is normalized in
 * place; pointers never escape the request/response exchange. */
static int sidecar_parse_headers(char *block, size_t block_size,
                                 size_t header_limit, size_t count_limit,
                                 int is_request, int response_no_body,
                                 sidecar_headers *out) {
    char *cursor = block;
    char *line_end;
    memset(out, 0, sizeof(*out));
    if (block_size < 4U || memcmp(block + block_size - 4U, "\r\n\r\n", 4U) != 0 ||
        block_size > header_limit || count_limit == 0U) {
        return 0;
    }
    out->storage = block;
    out->storage_size = block_size;
    line_end = strstr(cursor, "\r\n");
    if (line_end == NULL) return 0;
    *line_end = '\0';
    if ((is_request && !sidecar_parse_request_headers_start(cursor, out)) ||
        (!is_request && !sidecar_parse_response_headers_start(cursor, response_no_body, out))) {
        return 0;
    }
    cursor = line_end + 2;
    out->items = calloc(count_limit, sizeof(*out->items));
    if (out->items == NULL) {
        return 0;
    }
    if (!sidecar_parse_header_lines(cursor, count_limit,
                                    is_request, out)) return 0;
    if (is_request && out->host_count != 1U) {
        sidecar_headers_release(out);
        return 0;
    }
    if (!is_request && !out->has_content_length && !out->no_body &&
        out->status_code != 204 && out->status_code != 304) {
        sidecar_headers_release(out);
        return 0;
    }
    return 1;
}

static size_t sidecar_header_terminator_advance(size_t matched,
                                                unsigned char value) {
    switch (matched) {
    case 0U:
        return value == '\r' ? 1U : 0U;
    case 1U:
        if (value == '\n') {
            return 2U;
        }
        if (value == '\r') {
            return 1U;
        }
        return 0U;
    case 2U:
        return value == '\r' ? 3U : 0U;
    case 3U:
        if (value == '\n') {
            return 4U;
        }
        if (value == '\r') {
            return 1U;
        }
        return 0U;
    default:
        return 0U;
    }
}

static int sidecar_read_header_block(int fd, const sidecar_deadline *deadline,
                                     size_t limit, char **out, size_t *out_size) {
    size_t used = 0U;
    size_t matched = 0U;
    char *buffer;
    if (limit == 0U || limit > SIDECAR_HEADER_BUFFER) {
        return 0;
    }
    buffer = calloc(1U, limit + 1U);
    if (buffer == NULL) {
        return 0;
    }
    for (;;) {
        unsigned char probe[SIDECAR_IO_CHUNK];
        size_t received;
        size_t probe_size;
        size_t wanted;
        size_t probe_matched;

        if (used == limit) {
            free(buffer);
            return 0;
        }
        wanted = limit - used;
        if (wanted > sizeof(probe)) {
            wanted = sizeof(probe);
        }
        if (!sidecar_peek_some(fd, probe, wanted, deadline, &probe_size)) {
            free(buffer);
            return 0;
        }
        probe_matched = matched;
        for (size_t index = 0U; index < probe_size; ++index) {
            probe_matched = sidecar_header_terminator_advance(probe_matched,
                                                               probe[index]);
            if (probe_matched == 4U) {
                wanted = index + 1U;
                break;
            }
        }
        if (!sidecar_recv_some(fd, (unsigned char *)buffer + used, wanted,
                               deadline, &received)) {
            free(buffer);
            return 0;
        }
        for (size_t index = 0U; index < received; ++index) {
            matched = sidecar_header_terminator_advance(matched,
                (unsigned char)buffer[used + index]);
        }
        used += received;
        buffer[used] = '\0';
        if (matched == 4U) {
            *out_size = used;
            *out = buffer;
            return 1;
        }
    }
}

static int sidecar_connect(const char *spec, const sidecar_deadline *deadline) {
    char host[256];
    char service[16];
    const char *colon = strrchr(spec, ':');
    struct addrinfo hints;
    struct addrinfo *results = NULL;
    int fd = -1;
    if (!sidecar_private_spec(spec) || colon == NULL || colon == spec || strlen(colon + 1U) >= sizeof(service) ||
        (size_t)(colon - spec) >= sizeof(host)) {
        return -1;
    }
    memcpy(host, spec, (size_t)(colon - spec));
    host[colon - spec] = '\0';
    (void)snprintf(service, sizeof(service), "%s", colon + 1U);
    memset(&hints, 0, sizeof(hints));
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_family = AF_UNSPEC;
    if (getaddrinfo(host, service, &hints, &results) != 0) {
        return -1;
    }
    for (struct addrinfo *entry = results; entry != NULL; entry = entry->ai_next) {
        int flags;
        fd = socket(entry->ai_family, entry->ai_socktype | SOCK_CLOEXEC, entry->ai_protocol);
        if (fd < 0) {
            continue;
        }
        flags = fcntl(fd, F_GETFL, 0);
        if (flags < 0 || fcntl(fd, F_SETFL, flags | O_NONBLOCK) < 0 ||
            (connect(fd, entry->ai_addr, entry->ai_addrlen) < 0 && errno != EINPROGRESS)) {
            close(fd);
            fd = -1;
            continue;
        }
        if (!sidecar_wait(fd, POLLOUT, deadline)) {
            close(fd);
            fd = -1;
            continue;
        }
        {
            int socket_error = 0;
            socklen_t socket_error_size = sizeof(socket_error);
            if (getsockopt(fd, SOL_SOCKET, SO_ERROR, &socket_error,
                           &socket_error_size) != 0 || socket_error != 0) {
                close(fd);
                fd = -1;
                continue;
            }
        }
        break;
    }
    freeaddrinfo(results);
    return fd;
}

static int sidecar_listener(const char *spec) {
    int enabled = 1;
    int fd;
    {
        char host[256];
        char service[16];
        const char *colon = strrchr(spec, ':');
        struct addrinfo hints;
        struct addrinfo *results = NULL;
        if (!sidecar_private_spec(spec) || colon == NULL || colon == spec || (size_t)(colon - spec) >= sizeof(host) ||
            strlen(colon + 1U) >= sizeof(service)) {
            return -1;
        }
        memcpy(host, spec, (size_t)(colon - spec));
        host[colon - spec] = '\0';
        (void)snprintf(service, sizeof(service), "%s", colon + 1U);
        memset(&hints, 0, sizeof(hints));
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_family = AF_UNSPEC;
        hints.ai_flags = AI_PASSIVE;
        if (getaddrinfo(host, service, &hints, &results) != 0) {
            return -1;
        }
        fd = -1;
        for (struct addrinfo *entry = results; entry != NULL; entry = entry->ai_next) {
            fd = socket(entry->ai_family, entry->ai_socktype | SOCK_CLOEXEC, entry->ai_protocol);
            if (fd < 0) continue;
            (void)setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &enabled, sizeof(enabled));
            if (bind(fd, entry->ai_addr, entry->ai_addrlen) == 0 && listen(fd, SIDECAR_BACKLOG) == 0) break;
            close(fd);
            fd = -1;
        }
        freeaddrinfo(results);
    }
    return fd;
}

static int sidecar_write_error(int fd, int status, const sidecar_deadline *deadline) {
    char response[160];
    sidecar_deadline reply_deadline;
    int length = snprintf(response, sizeof(response),
                          "HTTP/1.1 %d Error\r\nConnection: close\r\nContent-Length: 0\r\n\r\n", status);

    /* A phase deadline is intentionally absolute.  Once it has elapsed, use
     * a small, independent best-effort budget for the fail-closed status
     * rather than silently dropping an otherwise observable 504/502/413. */
    if (deadline == NULL || sidecar_remaining(deadline) == 0) {
        reply_deadline.at_ms = sidecar_now_ms() + 1000U;
        deadline = &reply_deadline;
    }
    return length > 0 && (size_t)length < sizeof(response) &&
        sidecar_send_all(fd, (const unsigned char *)response, (size_t)length, deadline);
}

static int sidecar_write_decision(int fd, const msconnector_decision *decision,
                                  const sidecar_deadline *deadline) {
    msconnector_decision_action action = msconnector_decision_action_from_decision(decision);
    const char *location = decision->redirect_url;
    char response[1024];
    int length;
    if (action == MSCONNECTOR_DECISION_ACTION_DROP ||
        action == MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION) {
        (void)shutdown(fd, SHUT_RDWR);
        return 1;
    }
    if (location != NULL && (strchr(location, '\r') != NULL || strchr(location, '\n') != NULL ||
                             strlen(location) > 700U)) return 0;
    if (action == MSCONNECTOR_DECISION_ACTION_REDIRECT &&
        (location == NULL || location[0] == '\0')) return 0;
    if (action == MSCONNECTOR_DECISION_ACTION_REDIRECT) {
        length = snprintf(response, sizeof(response),
                          "HTTP/1.1 %d Redirect\r\nLocation: %s\r\nConnection: close\r\nContent-Length: 0\r\n\r\n",
                          msconnector_decision_http_status(decision), location);
    } else {
        length = snprintf(response, sizeof(response),
                          "HTTP/1.1 %d Decision\r\nConnection: close\r\nContent-Length: 0\r\n\r\n",
                          msconnector_decision_http_status(decision));
    }
    return length > 0 && (size_t)length < sizeof(response) &&
        sidecar_send_all(fd, (const unsigned char *)response, (size_t)length, deadline);
}

static void sidecar_record_action(msconnector_runtime_transaction *transaction,
                                  const msconnector_decision *decision,
                                  msconnector_error *error) {
    msconnector_decision_action action = msconnector_decision_action_from_decision(decision);
    int aborted = action == MSCONNECTOR_DECISION_ACTION_DROP ||
        action == MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
    (void)msconnector_runtime_transaction_record_host_action(
        transaction, decision, action, aborted ? 0 : msconnector_decision_http_status(decision),
        aborted ? "connection_aborted" : "http_status", aborted, error);
}

static msconnector_late_intervention_action sidecar_phase4_action(
    int response_committed, enum msconnector_phase4_mode phase4_mode) {
    msconnector_late_intervention_policy policy;

    msconnector_late_intervention_policy_init(&policy);
    return msconnector_late_intervention_resolve(&policy, response_committed,
        response_committed, phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
}

/* A disruptive engine decision is already terminal before the host attempts
 * its response.  If the peer disconnects during that response, do not try to
 * overwrite the rule decision with a second terminal failure: retain its
 * rule correlation and record the observed host action as an abort. */
static void sidecar_record_decision_delivery_failure(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    msconnector_error *error) {
    if (transaction == NULL || decision == NULL) return;
    (void)msconnector_runtime_transaction_record_host_action(
        transaction, decision, MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION,
        0, "connection_aborted", 1, error);
}

static void sidecar_record_failure_action(
    msconnector_runtime_transaction *transaction,
    int visible_http_status,
    int response_written,
    msconnector_error *error) {
    if (transaction == NULL) return;
    (void)msconnector_runtime_transaction_record_failure_host_action(
        transaction, response_written ? visible_http_status : 0,
        response_written ? 0 : 1, error);
}

static msconnector_transaction_error_class sidecar_failure_error_class(
    sidecar_failure_origin origin) {
    switch (origin) {
    case SIDECAR_FAILURE_CLIENT:
        return MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL;
    case SIDECAR_FAILURE_UPSTREAM:
        return MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT;
    case SIDECAR_FAILURE_PROTOCOL:
        return MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
    case SIDECAR_FAILURE_CONNECTOR:
    default:
        return MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
    }
}

static int sidecar_write_header_field(int fd, const msconnector_header *header,
                                      const sidecar_deadline *deadline) {
    static const unsigned char separator[] = ": ";
    static const unsigned char terminator[] = "\r\n";
    return sidecar_send_all(fd, (const unsigned char *)header->name,
                            header->name_size, deadline) &&
        sidecar_send_all(fd, separator, sizeof(separator) - 1U, deadline) &&
        sidecar_send_all(fd, (const unsigned char *)header->value,
                         header->value_size, deadline) &&
        sidecar_send_all(fd, terminator, sizeof(terminator) - 1U, deadline);
}

/* Response ownership turns on at the first byte observed on the client
 * socket, not only after a whole header block has been accepted.  Keep that
 * accounting private to the downstream response writer: upstream request
 * writes have no client-response fallback to suppress. */
static int sidecar_send_all_accumulated(int fd, const unsigned char *data,
                                        size_t size,
                                        const sidecar_deadline *deadline,
                                        size_t *bytes_sent) {
    size_t sent = 0U;
    int complete;

    if (bytes_sent == NULL) return 0;
    complete = sidecar_send_all_observed(fd, data, size, deadline, &sent);
    if (sent > SIZE_MAX - *bytes_sent) {
        *bytes_sent = SIZE_MAX;
        return 0;
    }
    *bytes_sent += sent;
    return complete;
}

static int sidecar_write_header_field_observed(int fd,
                                               const msconnector_header *header,
                                               const sidecar_deadline *deadline,
                                               size_t *bytes_sent) {
    static const unsigned char separator[] = ": ";
    static const unsigned char terminator[] = "\r\n";

    return sidecar_send_all_accumulated(fd, (const unsigned char *)header->name,
                                        header->name_size, deadline, bytes_sent) &&
        sidecar_send_all_accumulated(fd, separator, sizeof(separator) - 1U,
                                     deadline, bytes_sent) &&
        sidecar_send_all_accumulated(fd, (const unsigned char *)header->value,
                                     header->value_size, deadline, bytes_sent) &&
        sidecar_send_all_accumulated(fd, terminator, sizeof(terminator) - 1U,
                                     deadline, bytes_sent);
}

static int sidecar_write_upstream_request(int upstream, const char *request_line,
                                          const sidecar_headers *headers,
                                          const unsigned char *body, size_t body_size,
                                          const sidecar_deadline *deadline) {
    if (!sidecar_send_all(upstream, (const unsigned char *)request_line,
                          strlen(request_line), deadline)) return 0;
    for (size_t i = 0U; i < headers->count; ++i) {
        if (strcasecmp(headers->items[i].name, "Connection") == 0 ||
            strcasecmp(headers->items[i].name, "Keep-Alive") == 0) continue;
        if (!sidecar_write_header_field(upstream, &headers->items[i], deadline)) return 0;
    }
    if (!sidecar_send_all(upstream, (const unsigned char *)"Connection: close\r\n\r\n", 21U, deadline)) return 0;
    return body_size == 0U || sidecar_send_all(upstream, body, body_size, deadline);
}

static int sidecar_write_upstream_response_headers_observed(
    int client, const char *status_line, const sidecar_headers *headers,
    const sidecar_deadline *deadline, size_t *bytes_sent) {
    if (bytes_sent == NULL) return 0;
    *bytes_sent = 0U;
    if (!sidecar_send_all_accumulated(client, (const unsigned char *)status_line,
                                      strlen(status_line), deadline, bytes_sent)) return 0;
    for (size_t i = 0U; i < headers->count; ++i) {
        if (strcasecmp(headers->items[i].name, "Connection") == 0 ||
            strcasecmp(headers->items[i].name, "Keep-Alive") == 0) continue;
        if (!sidecar_write_header_field_observed(client, &headers->items[i],
                                                 deadline, bytes_sent)) return 0;
    }
    return sidecar_send_all_accumulated(client,
        (const unsigned char *)"Connection: close\r\n\r\n", 21U, deadline,
        bytes_sent);
}

/* Informational responses are deliberately translated before the final
 * response enters Common P3. Do not add Connection: close or Content-Length:
 * a 1xx response has no body and must not alter the following final response. */
static int sidecar_write_interim_response_headers_observed(
    int client, const sidecar_headers *headers, const sidecar_deadline *deadline,
    size_t *bytes_sent) {
    char status_line[64];
    int length;

    if (headers == NULL || bytes_sent == NULL || headers->status_code < 100 ||
        headers->status_code >= 200 || headers->status_code == 101) {
        return 0;
    }
    *bytes_sent = 0U;
    length = snprintf(status_line, sizeof(status_line), "HTTP/1.1 %d Informational\r\n",
                      headers->status_code);
    if (length <= 0 || (size_t)length >= sizeof(status_line) ||
        !sidecar_send_all_accumulated(client, (const unsigned char *)status_line,
                                      (size_t)length, deadline, bytes_sent)) {
        return 0;
    }
    for (size_t i = 0U; i < headers->count; ++i) {
        if (strcasecmp(headers->items[i].name, "Connection") == 0 ||
            strcasecmp(headers->items[i].name, "Keep-Alive") == 0 ||
            strcasecmp(headers->items[i].name, "Content-Length") == 0) {
            continue;
        }
        if (!sidecar_write_header_field_observed(client, &headers->items[i], deadline,
                                                 bytes_sent)) {
            return 0;
        }
    }
    return sidecar_send_all_accumulated(client, (const unsigned char *)"\r\n", 2U,
                                        deadline, bytes_sent);
}

typedef struct sidecar_exchange_payload {
    char *request_block;
    char *response_block;
    size_t request_size;
    size_t response_size;
    sidecar_headers request_headers;
    sidecar_headers response_headers;
    unsigned char *request_body;
    size_t body_read;
} sidecar_exchange_payload;

typedef struct sidecar_exchange_state {
    int client;
    const sidecar_options *options;
    msconnector_runtime *runtime;
    sidecar_deadline deadline;
    size_t header_limit;
    size_t count_limit;
    size_t request_limit;
    size_t response_limit;
    sidecar_exchange_payload payload;
    msconnector_runtime_transaction *transaction;
    msconnector_decision decision;
    msconnector_error error;
    int upstream;
    int result;
    int request_is_head;
    int response_blocked;
    int client_response_started;
    int failure_status;
    int handled;
    sidecar_failure_origin failure_origin;
} sidecar_exchange_state;

static void sidecar_exchange_state_init(sidecar_exchange_state *state, int client,
                                        const sidecar_options *options,
                                        msconnector_runtime *runtime) {
    memset(state, 0, sizeof(*state));
    state->client = client;
    state->options = options;
    state->runtime = runtime;
    state->deadline.at_ms = sidecar_now_ms() + options->timeout_ms;
    state->header_limit = msconnector_runtime_total_header_limit(runtime);
    state->count_limit = msconnector_runtime_header_count_limit(runtime);
    state->request_limit = msconnector_runtime_request_body_limit(runtime);
    state->response_limit = msconnector_runtime_response_body_limit(runtime);
    state->upstream = -1;
    state->failure_status = 502;
    state->failure_origin = SIDECAR_FAILURE_CONNECTOR;
}

static int sidecar_read_final_response_headers(sidecar_exchange_state *state) {
    for (;;) {
        char *block = NULL;
        size_t block_size = 0U;
        size_t bytes_sent = 0U;
        sidecar_headers headers;

        memset(&headers, 0, sizeof(headers));
        if (!sidecar_read_header_block(state->upstream, &state->deadline, state->header_limit,
                                       &block, &block_size)) {
            state->failure_origin = SIDECAR_FAILURE_UPSTREAM;
            return 0;
        }
        if (!sidecar_parse_headers(block, block_size, state->header_limit, state->count_limit,
                                   0, state->request_is_head, &headers) || headers.chunked ||
            headers.upgrade || headers.status_code == 101) {
            sidecar_headers_release(&headers);
            free(block);
            state->failure_origin = SIDECAR_FAILURE_PROTOCOL;
            return 0;
        }
        if (headers.status_code >= 200) {
            state->payload.response_block = block;
            state->payload.response_size = block_size;
            state->payload.response_headers = headers;
            return 1;
        }
        if (!sidecar_write_interim_response_headers_observed(state->client, &headers,
                &state->deadline, &bytes_sent)) {
            if (bytes_sent > 0U) {
                state->client_response_started = 1;
            }
            sidecar_headers_release(&headers);
            free(block);
            state->failure_origin = SIDECAR_FAILURE_CLIENT;
            return 0;
        }
        sidecar_headers_release(&headers);
        free(block);
    }
}

static int sidecar_runtime_limits_supported(const msconnector_runtime *runtime) {
    return runtime != NULL &&
        msconnector_runtime_header_count_limit(runtime) <= MSCONNECTOR_MAX_HEADER_COUNT &&
        msconnector_runtime_total_header_limit(runtime) <= MSCONNECTOR_MAX_TOTAL_HEADER_BYTES &&
        msconnector_runtime_request_body_limit(runtime) <= MSCONNECTOR_MAX_BODY_BUFFER_SIZE &&
        msconnector_runtime_response_body_limit(runtime) <=
            MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE;
}

static int sidecar_read_request_body(sidecar_exchange_state *state) {
    while (state->payload.body_read < state->payload.request_headers.content_length) {
        size_t received;
        size_t wanted = state->payload.request_headers.content_length - state->payload.body_read;
        if (wanted > SIDECAR_IO_CHUNK) {
            wanted = SIDECAR_IO_CHUNK;
        }
        if (!sidecar_recv_some(state->client, state->payload.request_body + state->payload.body_read,
                               wanted, &state->deadline, &received)) {
            state->failure_origin = SIDECAR_FAILURE_CLIENT;
            return 0;
        }
        if (!msconnector_runtime_transaction_append_request_body_chunk(
                state->transaction, state->payload.request_body + state->payload.body_read, received,
                &state->error)) {
            state->failure_status = msconnector_runtime_error_http_status(
                state->runtime, state->error.code);
            return 0;
        }
        state->payload.body_read += received;
    }
    return 1;
}

static int sidecar_read_response_body(sidecar_exchange_state *state) {
    unsigned char chunk[SIDECAR_IO_CHUNK];
    while (state->payload.body_read < state->payload.response_headers.content_length) {
        size_t received;
        size_t wanted = state->payload.response_headers.content_length - state->payload.body_read;
        if (wanted > SIDECAR_IO_CHUNK) {
            wanted = SIDECAR_IO_CHUNK;
        }
        if (!sidecar_recv_some(state->upstream, chunk, wanted, &state->deadline, &received)) {
            state->failure_origin = SIDECAR_FAILURE_UPSTREAM;
            return 0;
        }
        if (!msconnector_runtime_transaction_append_response_body_chunk(
                state->transaction, chunk, received,
                &state->error)) {
            state->failure_origin = SIDECAR_FAILURE_CONNECTOR;
            return 0;
        }
        {
            size_t bytes_sent = 0U;
            if (!sidecar_send_all_observed(state->client, chunk, received,
                                           &state->deadline, &bytes_sent)) {
                if (bytes_sent > 0U) {
                    (void)msconnector_runtime_transaction_set_response_commit_state_checked(
                        state->transaction, 1, 1, &state->error);
                }
                state->failure_origin = SIDECAR_FAILURE_CLIENT;
                return 0;
            }
        }
        if (!msconnector_runtime_transaction_set_response_commit_state_checked(
                state->transaction, 1, 1, &state->error)) {
            state->failure_status = msconnector_runtime_error_http_status(
                state->runtime, state->error.code);
            return 0;
        }
        state->payload.body_read += received;
    }
    return 1;
}

static void sidecar_finish_decision(sidecar_exchange_state *state) {
    if (!sidecar_write_decision(state->client, &state->decision, &state->deadline)) {
        sidecar_record_decision_delivery_failure(state->transaction, &state->decision,
                                                  &state->error);
    } else {
        sidecar_record_action(state->transaction, &state->decision, &state->error);
    }
    (void)msconnector_runtime_transaction_finish(state->transaction, &state->error);
    state->handled = 1;
}

static int sidecar_forward_response(sidecar_exchange_state *state) {
    char status_line[64];
    size_t header_bytes_sent = 0U;

    (void)snprintf(status_line, sizeof(status_line), "HTTP/1.1 %d Proxied\r\n",
                   state->payload.response_headers.status_code);
    if (!sidecar_write_upstream_response_headers_observed(state->client, status_line,
            &state->payload.response_headers, &state->deadline, &header_bytes_sent)) {
        /* A partial downstream header is already an owned response stream.
         * Do not let the generic exchange error append a second 5xx response;
         * the worker closes this client after recording the typed failure. */
        if (header_bytes_sent > 0U) {
            state->client_response_started = 1;
            (void)msconnector_runtime_transaction_set_response_commit_state_checked(
                state->transaction, 1, 0, &state->error);
        }
        state->failure_origin = SIDECAR_FAILURE_CLIENT;
        return 0;
    }
    state->client_response_started = 1;
    if (!msconnector_runtime_transaction_set_response_commit_state_checked(
            state->transaction, 1, 0, &state->error)) {
        state->failure_status = msconnector_runtime_error_http_status(
            state->runtime, state->error.code);
        return 0;
    }
    return 1;
}

static int sidecar_receipt_sha256(const char *value,
                                  char encoded[SIDECAR_RECEIPT_HEX_SIZE + 1U]) {
    static const char hexadecimal[] = "0123456789abcdef";
    unsigned char digest[SHA256_DIGEST_LENGTH];
    size_t length;

    if (value == NULL || encoded == NULL || value[0] == '\0') {
        return 0;
    }
    length = strlen(value);
    if (SHA256((const unsigned char *)value, length, digest) == NULL) {
        return 0;
    }
    for (size_t index = 0U; index < SHA256_DIGEST_LENGTH; ++index) {
        encoded[index * 2U] = hexadecimal[digest[index] >> 4U];
        encoded[index * 2U + 1U] = hexadecimal[digest[index] & 0x0fU];
    }
    encoded[SIDECAR_RECEIPT_HEX_SIZE] = '\0';
    return 1;
}

static int sidecar_receipt_binding_valid(const char *binding) {
    if (binding == NULL || strlen(binding) != SIDECAR_RECEIPT_BINDING_SIZE) {
        return 0;
    }
    for (size_t index = 0U; index < SIDECAR_RECEIPT_BINDING_SIZE; ++index) {
        if ((binding[index] < '0' || binding[index] > '9') &&
            (binding[index] < 'a' || binding[index] > 'f')) {
            return 0;
        }
    }
    return 1;
}

static int sidecar_publish_receipt(const char *path, const char *encoded, int length) {
    struct stat parent_info;
    char temporary[1024];
    int descriptor = -1;
    int descriptor_flags;
    int temporary_length;
    int result = 0;

    if (path == NULL || path[0] != '/' || encoded == NULL || length <= 0 ||
        strlen(path) >= sizeof(temporary) - sizeof(".tmp.XXXXXX")) return 0;
    {
        const char *slash = strrchr(path, '/');
        char parent[1024];
        size_t parent_length = slash == path ? 1U : (size_t)(slash - path);
        if (parent_length >= sizeof(parent)) return 0;
        memcpy(parent, path, parent_length);
        parent[parent_length] = '\0';
        if (lstat(parent, &parent_info) != 0 || parent_info.st_uid != geteuid() ||
            (parent_info.st_mode & 0077) != 0 || !S_ISDIR(parent_info.st_mode)) return 0;
    }
    temporary_length = snprintf(temporary, sizeof(temporary), "%s.tmp.XXXXXX", path);
    if (temporary_length < 0 || (size_t)temporary_length >= sizeof(temporary)) return 0;
    descriptor = mkstemp(temporary);
    if (descriptor < 0) return 0;
    descriptor_flags = fcntl(descriptor, F_GETFD, 0);
    if (fchmod(descriptor, 0600) != 0 || descriptor_flags < 0 ||
        fcntl(descriptor, F_SETFD, descriptor_flags | FD_CLOEXEC) != 0 ||
        write(descriptor, encoded, (size_t)length) != (ssize_t)length ||
        fsync(descriptor) != 0) {
        (void)close(descriptor);
        (void)unlink(temporary);
        return 0;
    }
    if (close(descriptor) != 0) {
        (void)unlink(temporary);
        return 0;
    }
    /* link() gives the final name atomically without allowing replacement of
     * an existing receipt, unlike rename(). */
    if (link(temporary, path) == 0) result = 1;
    (void)unlink(temporary);
    return result;
}

static const char *sidecar_receipt_phase_sequence(unsigned int phase_mask) {
    switch (phase_mask) {
    case 0U:
        return "[]";
    case MSCONNECTOR_TRANSACTION_PHASE_MASK_P1:
        return "[\"P1\"]";
    case MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 |
            MSCONNECTOR_TRANSACTION_PHASE_MASK_P2:
        return "[\"P1\",\"P2\"]";
    case MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 |
            MSCONNECTOR_TRANSACTION_PHASE_MASK_P2 |
            MSCONNECTOR_TRANSACTION_PHASE_MASK_P3:
        return "[\"P1\",\"P2\",\"P3\"]";
    case MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL:
        return "[\"P1\",\"P2\",\"P3\",\"P4\"]";
    default:
        return NULL;
    }
}

static const char *sidecar_receipt_last_completed_phase(int phase) {
    switch (phase) {
    case -1:
        return "none";
    case MSCONNECTOR_PHASE_REQUEST_HEADERS:
        return "P1";
    case MSCONNECTOR_PHASE_REQUEST_BODY:
        return "P2";
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS:
        return "P3";
    case MSCONNECTOR_PHASE_RESPONSE_BODY:
        return "P4";
    default:
        return NULL;
    }
}

static int sidecar_write_allow_receipt(
    const msconnector_runtime_transaction_snapshot *snapshot, int visible_status) {
    const char *path = getenv("STOCK_SIDECAR_RECEIPT_PATH");
    const char *binding = getenv("STOCK_SIDECAR_RECEIPT_BINDING");
    char encoded[4096];
    char transaction_digest[SIDECAR_RECEIPT_HEX_SIZE + 1U];
    char binding_digest[SIDECAR_RECEIPT_HEX_SIZE + 1U];
    int length;

    if (path == NULL || *path == '\0') return 1;
    if (snapshot == NULL || !sidecar_receipt_binding_valid(binding) ||
        snapshot->contract.completed_phase_mask != MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL ||
        snapshot->contract.engine_decision != MSCONNECTOR_TRANSACTION_DECISION_ALLOW ||
        snapshot->contract.action != MSCONNECTOR_DECISION_ACTION_ALLOW ||
        snapshot->contract.status != MSCONNECTOR_TRANSACTION_STATUS_CLEANED ||
        !snapshot->contract.cleanup_started || !snapshot->contract.cleanup_complete ||
        !snapshot->finished || !snapshot->response_headers_processed ||
        !snapshot->response_headers_sent || !snapshot->response_body.finished ||
        !snapshot->contract.response_committed || visible_status < 100 ||
        visible_status > 599 ||
        !sidecar_receipt_sha256(snapshot->contract.transaction_id, transaction_digest) ||
        !sidecar_receipt_sha256(binding, binding_digest)) return 0;
    length = snprintf(encoded, sizeof(encoded),
        "{\"schema_version\":1,\"connector\":\"lighttpd\","
        "\"connector_profile\":\"lighttpd-stock-sidecar\","
        "\"integration_mode\":\"traffic-owning-sidecar\","
        "\"transport_version\":\"HTTP/1.1\","
        "\"phase_observation\":\"runtime_snapshot_after_cleanup\","
        "\"observed_phase_sequence\":[\"P1\",\"P2\",\"P3\",\"P4\"],"
        "\"transaction_id_sha256\":\"%s\","
        "\"receipt_binding_sha256\":\"%s\","
        "\"request_body_bytes\":%zu,\"response_body_bytes\":%zu,"
        "\"engine_decision\":\"allow\",\"actual_host_action\":\"allow\","
        "\"original_http_status\":%d,\"visible_http_status\":%d,"
        "\"response_committed\":true,\"cleanup_status\":\"complete\","
        "\"cleanup_complete\":true,"
        "\"payloads_persisted\":false,\"opaque_handles_persisted\":false}\n",
        transaction_digest, binding_digest, snapshot->request_body.bytes_seen,
        snapshot->response_body.bytes_seen, snapshot->response_original_status,
        visible_status);
    if (length < 0 || (size_t)length >= sizeof(encoded)) return 0;
    return sidecar_publish_receipt(path, encoded, length);
}

static int sidecar_write_non_allow_receipt(
    const msconnector_runtime_transaction_snapshot *snapshot) {
    const char *path = getenv("STOCK_SIDECAR_RECEIPT_PATH");
    const char *binding = getenv("STOCK_SIDECAR_RECEIPT_BINDING");
    const char *phase_sequence;
    const char *last_phase;
    const char *engine_decision;
    const char *contract_action;
    const char *error_class;
    const char *mode;
    char encoded[4096];
    char transaction_digest[SIDECAR_RECEIPT_HEX_SIZE + 1U];
    char binding_digest[SIDECAR_RECEIPT_HEX_SIZE + 1U];
    int length;

    if (path == NULL || *path == '\0') return 1;
    if (snapshot == NULL || !sidecar_receipt_binding_valid(binding) ||
        snapshot->contract.status != MSCONNECTOR_TRANSACTION_STATUS_CLEANED ||
        !snapshot->contract.cleanup_started || !snapshot->contract.cleanup_complete ||
        !snapshot->finished || snapshot->response_original_status < 0 ||
        snapshot->response_original_status > 599) return 0;
    phase_sequence = sidecar_receipt_phase_sequence(snapshot->contract.completed_phase_mask);
    last_phase = sidecar_receipt_last_completed_phase(snapshot->contract.last_completed_phase);
    engine_decision = msconnector_transaction_decision_kind_name(
        snapshot->contract.engine_decision);
    contract_action = msconnector_decision_action_name(snapshot->contract.action);
    error_class = msconnector_transaction_error_class_name(snapshot->contract.error_class);
    if (snapshot->contract.mode == MSCONNECTOR_TRANSACTION_MODE_SAFE) {
        mode = "safe";
    } else if (snapshot->contract.mode == MSCONNECTOR_TRANSACTION_MODE_STRICT) {
        mode = "strict";
    } else {
        mode = NULL;
    }
    if (phase_sequence == NULL || last_phase == NULL || mode == NULL ||
        strcmp(engine_decision, "unknown") == 0 ||
        strcmp(contract_action, "unknown") == 0 ||
        strcmp(error_class, "unknown") == 0 ||
        (snapshot->contract.engine_decision == MSCONNECTOR_TRANSACTION_DECISION_ALLOW &&
         snapshot->contract.action == MSCONNECTOR_DECISION_ACTION_ALLOW &&
         snapshot->contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE) ||
        !sidecar_receipt_sha256(snapshot->contract.transaction_id, transaction_digest) ||
        !sidecar_receipt_sha256(binding, binding_digest)) return 0;
    length = snprintf(encoded, sizeof(encoded),
        "{\"schema_version\":2,\"receipt_kind\":\"non_allow\","
        "\"connector\":\"lighttpd\","
        "\"connector_profile\":\"lighttpd-stock-sidecar\","
        "\"integration_mode\":\"traffic-owning-sidecar\","
        "\"transport_version\":\"HTTP/1.1\","
        "\"phase_observation\":\"runtime_snapshot_after_cleanup\","
        "\"observed_phase_sequence\":%s,\"last_completed_phase\":\"%s\","
        "\"transaction_id_sha256\":\"%s\","
        "\"receipt_binding_sha256\":\"%s\","
        "\"request_body_bytes\":%zu,\"request_body_truncated\":%s,"
        "\"response_body_bytes\":%zu,\"response_body_truncated\":%s,"
        "\"engine_decision\":\"%s\",\"contract_action\":\"%s\","
        "\"error_class\":\"%s\",\"mode\":\"%s\","
        "\"original_http_status\":%d,\"response_committed\":%s,"
        "\"response_headers_processed\":%s,\"response_headers_sent\":%s,"
        "\"response_body_finished\":%s,"
        "\"created_at_ms\":%llu,\"completed_at_ms\":%llu,"
        "\"cleanup_at_ms\":%llu,\"cleanup_status\":\"complete\","
        "\"cleanup_complete\":true,\"payloads_persisted\":false,"
        "\"opaque_handles_persisted\":false}\n",
        phase_sequence, last_phase, transaction_digest, binding_digest,
        snapshot->request_body.bytes_seen,
        snapshot->request_body.truncated ? "true" : "false",
        snapshot->response_body.bytes_seen,
        snapshot->response_body.truncated ? "true" : "false",
        engine_decision, contract_action, error_class, mode,
        snapshot->response_original_status,
        snapshot->contract.response_committed ? "true" : "false",
        snapshot->response_headers_processed ? "true" : "false",
        snapshot->response_headers_sent ? "true" : "false",
        snapshot->response_body.finished ? "true" : "false",
        (unsigned long long)snapshot->contract.created_at_ms,
        (unsigned long long)snapshot->contract.completed_at_ms,
        (unsigned long long)snapshot->contract.cleanup_at_ms);
    if (length < 0 || (size_t)length >= sizeof(encoded)) return 0;
    return sidecar_publish_receipt(path, encoded, length);
}

static int sidecar_exchange_request(sidecar_exchange_state *state) {
    msconnector_request request;
    const char *host = "";
    if (!sidecar_read_header_block(state->client, &state->deadline, state->header_limit,
                                   &state->payload.request_block, &state->payload.request_size) ||
        !sidecar_parse_headers(state->payload.request_block, state->payload.request_size, state->header_limit,
                                state->count_limit, 1, 0, &state->payload.request_headers) ||
        state->payload.request_headers.chunked || state->payload.request_headers.upgrade) {
        (void)sidecar_write_error(state->client, 400, &state->deadline);
        state->handled = 1;
        return 0;
    }
    if (sidecar_headers_has_name(&state->payload.request_headers, "Expect")) {
        (void)sidecar_write_error(state->client, 417, &state->deadline);
        state->handled = 1;
        return 0;
    }
    state->request_is_head = strcmp(state->payload.request_headers.method, "HEAD") == 0;
    for (size_t i = 0U; i < state->payload.request_headers.count; ++i) {
        if (strcasecmp(state->payload.request_headers.items[i].name, "Host") == 0) {
            host = state->payload.request_headers.items[i].value;
            break;
        }
    }
    memset(&request, 0, sizeof(request));
    request.method = state->payload.request_headers.method;
    request.uri = state->payload.request_headers.uri;
    request.http_version = state->payload.request_headers.version;
    request.hostname = host;
    request.headers = state->payload.request_headers.items;
    request.header_count = state->payload.request_headers.count;
    if (!msconnector_runtime_transaction_begin(state->runtime, &request, NULL,
                                               &state->transaction, &state->decision,
                                               &state->error)) {
        return 0;
    }
    if (msconnector_decision_is_disruptive(&state->decision)) {
        sidecar_finish_decision(state);
        return 0;
    }
    if (state->payload.request_headers.content_length > state->request_limit) {
        int status = msconnector_runtime_error_http_status(state->runtime,
            MSCONNECTOR_ERROR_BODY_TOO_LARGE);
        int written;
        (void)msconnector_runtime_transaction_fail(state->transaction,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, &state->error);
        written = sidecar_write_error(state->client, status, &state->deadline);
        sidecar_record_failure_action(state->transaction, status, written, &state->error);
        (void)msconnector_runtime_transaction_finish(state->transaction, &state->error);
        state->handled = 1;
        return 0;
    }
    if (state->payload.request_headers.content_length > 0U) {
        state->payload.request_body = malloc(state->payload.request_headers.content_length);
        if (state->payload.request_body == NULL) return 0;
        if (!sidecar_read_request_body(state)) return 0;
    }
    if (!msconnector_runtime_transaction_finish_request_body(state->transaction,
                                                              &state->decision,
                                                              &state->error)) return 0;
    if (msconnector_decision_is_disruptive(&state->decision)) {
        sidecar_finish_decision(state);
        return 0;
    }
    return 1;
}

static int sidecar_exchange_response(sidecar_exchange_state *state) {
    msconnector_response response;
    state->upstream = sidecar_connect(state->options->upstream, &state->deadline);
    if (state->upstream < 0) {
        state->failure_origin = SIDECAR_FAILURE_UPSTREAM;
        return 0;
    }
    {
        char request_line[MSCONNECTOR_TRANSACTION_CONTRACT_METHOD_SIZE +
            MSCONNECTOR_TRANSACTION_CONTRACT_URI_SIZE + sizeof(" HTTP/1.1\r\n")];
        int request_line_size = snprintf(request_line, sizeof(request_line),
            "%s %s HTTP/1.1\r\n", state->payload.request_headers.method,
            state->payload.request_headers.uri);
        if (request_line_size < 0 || (size_t)request_line_size >= sizeof(request_line)) {
            state->failure_origin = SIDECAR_FAILURE_PROTOCOL;
            return 0;
        }
        if (!sidecar_write_upstream_request(state->upstream, request_line,
                &state->payload.request_headers, state->payload.request_body, state->payload.body_read,
                &state->deadline)) {
            state->failure_origin = SIDECAR_FAILURE_UPSTREAM;
            return 0;
        }
    }
    if (!sidecar_read_final_response_headers(state)) return 0;
    if (!state->payload.response_headers.no_body &&
        state->payload.response_headers.content_length > state->response_limit) {
        int status = msconnector_runtime_error_http_status(state->runtime,
            MSCONNECTOR_ERROR_BODY_TOO_LARGE);
        int written;
        (void)msconnector_runtime_transaction_fail(state->transaction,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, &state->error);
        written = sidecar_write_error(state->client, status, &state->deadline);
        sidecar_record_failure_action(state->transaction, status, written, &state->error);
        (void)msconnector_runtime_transaction_finish(state->transaction, &state->error);
        state->handled = 1;
        return 0;
    }
    memset(&response, 0, sizeof(response));
    response.status = state->payload.response_headers.status_code;
    response.http_version = state->payload.response_headers.version;
    response.headers = state->payload.response_headers.items;
    response.header_count = state->payload.response_headers.count;
    if (!msconnector_runtime_transaction_process_response_headers(state->transaction,
            &response, &state->decision, &state->error)) return 0;
    state->response_blocked = msconnector_decision_is_disruptive(&state->decision);
    if (state->response_blocked) {
        sidecar_finish_decision(state);
        return 0;
    }
    if (!sidecar_forward_response(state)) return 0;
    state->payload.body_read = 0U;
    if (!state->payload.response_headers.no_body && !sidecar_read_response_body(state)) return 0;
    if (!msconnector_runtime_transaction_finish_response_body(state->transaction,
            &state->decision, &state->error)) return 0;
    if (msconnector_decision_is_disruptive(&state->decision)) {
        msconnector_late_intervention_action action = sidecar_phase4_action(
            state->client_response_started,
            msconnector_runtime_phase4_mode(state->runtime));

        state->decision.late_intervention = state->client_response_started != 0;
        if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION) {
            (void)shutdown(state->client, SHUT_RDWR);
            sidecar_record_decision_delivery_failure(state->transaction, &state->decision,
                                                      &state->error);
            (void)msconnector_runtime_transaction_finish(state->transaction, &state->error);
            state->handled = 1;
            return 0;
        }
        if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY) {
            (void)msconnector_runtime_transaction_record_host_action(
                state->transaction, &state->decision,
                MSCONNECTOR_DECISION_ACTION_LOG_ONLY,
                state->payload.response_headers.status_code, "log_only", 0,
                &state->error);
        } else {
            sidecar_record_action(state->transaction, &state->decision, &state->error);
        }
    }
    return 1;
}

static void sidecar_exchange_error(sidecar_exchange_state *state) {
    int status;
    int response_written = 0;
    if (state->transaction == NULL) {
        (void)sidecar_write_error(state->client,
            sidecar_remaining(&state->deadline) == 0 ? 504 : 502, &state->deadline);
        return;
    }
    status = sidecar_remaining(&state->deadline) == 0 ? 504 : state->failure_status;
    if (sidecar_remaining(&state->deadline) == 0) {
        (void)msconnector_runtime_transaction_timeout(state->transaction, &state->error);
    } else {
        (void)msconnector_runtime_transaction_fail(state->transaction,
            sidecar_failure_error_class(state->failure_origin), &state->error);
    }
    if (!state->client_response_started) {
        response_written = sidecar_write_error(state->client, status, &state->deadline);
    }
    sidecar_record_failure_action(state->transaction, status, response_written, &state->error);
    (void)msconnector_runtime_transaction_finish(state->transaction, &state->error);
}

static int sidecar_exchange(int client, const sidecar_options *options,
                            msconnector_runtime *runtime) {
    sidecar_exchange_state state;
    msconnector_runtime_transaction_snapshot receipt_snapshot;
    int receipt_ready = 0;
    sidecar_exchange_state_init(&state, client, options, runtime);
    if (!(sidecar_exchange_request(&state) && sidecar_exchange_response(&state)) &&
        !state.handled) {
        sidecar_exchange_error(&state);
    }
    if (state.transaction != NULL) {
        receipt_ready = msconnector_runtime_transaction_finalize_and_snapshot(
            &state.transaction, &receipt_snapshot, &state.error);
    }
    if (state.upstream >= 0) close(state.upstream);
    if (receipt_ready) {
        state.result = receipt_snapshot.contract.engine_decision ==
                MSCONNECTOR_TRANSACTION_DECISION_ALLOW &&
                receipt_snapshot.contract.action == MSCONNECTOR_DECISION_ACTION_ALLOW &&
                receipt_snapshot.contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE ?
            sidecar_write_allow_receipt(&receipt_snapshot,
                state.payload.response_headers.status_code) :
            sidecar_write_non_allow_receipt(&receipt_snapshot);
    }
    msconnector_runtime_transaction_destroy(&state.transaction);
    sidecar_headers_release(&state.payload.request_headers);
    sidecar_headers_release(&state.payload.response_headers);
    free(state.payload.request_body);
    free(state.payload.response_block);
    free(state.payload.request_block);
    return state.result;
}

/* The exchange above deliberately keeps each phase in a separate bounded
 * helper.  This is the host adapter's transaction boundary: request parsing
 * and P1/P2 complete before upstream I/O, and response P3/P4 complete before
 * the response is committed to the client. */
#if 0
static int sidecar_exchange_legacy(int client, const sidecar_options *options,
                            msconnector_runtime *runtime) {
    sidecar_deadline deadline = { sidecar_now_ms() + options->timeout_ms };
    size_t header_limit = msconnector_runtime_total_header_limit(runtime);
    size_t count_limit = msconnector_runtime_header_count_limit(runtime);
    size_t request_limit = msconnector_runtime_request_body_limit(runtime);
    size_t response_limit = msconnector_runtime_response_body_limit(runtime);
    char *request_block = NULL;
    char *response_block = NULL;
    size_t request_size = 0U;
    size_t response_size = 0U;
    sidecar_headers request_headers;
    sidecar_headers response_headers;
    msconnector_runtime_transaction *transaction = NULL;
    msconnector_decision decision;
    msconnector_error error;
    unsigned char *request_body = NULL;
    unsigned char *response_body = NULL;
    size_t body_read = 0U;
    int upstream = -1;
    int result = 0;
    int request_is_head = 0;
    int response_blocked = 0;
    int client_response_started = 0;
    int failure_status = 502;
    sidecar_failure_origin failure_origin = SIDECAR_FAILURE_CONNECTOR;
    memset(&request_headers, 0, sizeof(request_headers));
    memset(&response_headers, 0, sizeof(response_headers));
    if (!sidecar_read_header_block(client, &deadline, header_limit, &request_block, &request_size)) {
        (void)sidecar_write_error(client, 400, &deadline);
        goto cleanup;
    }
    if (!sidecar_parse_headers(request_block, request_size, header_limit, count_limit, 1, 0, &request_headers)) {
        (void)sidecar_write_error(client, 400, &deadline);
        goto cleanup;
    }
    if (request_headers.chunked || request_headers.upgrade) {
        (void)sidecar_write_error(client, 400, &deadline);
        goto cleanup;
    }
    {
        msconnector_request request;
        const char *host = "";
        request_is_head = strcasecmp(request_headers.method, "HEAD") == 0;
        {
            for (size_t i = 0U; i < request_headers.count; ++i) {
                if (strcasecmp(request_headers.items[i].name, "Host") == 0) {
                    host = request_headers.items[i].value;
                    break;
                }
            }
        }
        memset(&request, 0, sizeof(request));
        request.method = request_headers.method;
        request.uri = request_headers.uri;
        request.http_version = request_headers.version;
        request.hostname = host;
        request.headers = request_headers.items;
        request.header_count = request_headers.count;
        request.body.data = NULL;
        request.body.size = 0U;
        if (!msconnector_runtime_transaction_begin(runtime, &request, NULL, &transaction,
                                                    &decision, &error)) goto runtime_error;
        if (msconnector_decision_is_disruptive(&decision)) {
            if (!sidecar_write_decision(client, &decision, &deadline)) {
                sidecar_record_decision_delivery_failure(transaction, &decision, &error);
                (void)msconnector_runtime_transaction_finish(transaction, &error);
                goto cleanup;
            }
            sidecar_record_action(transaction, &decision, &error);
            (void)msconnector_runtime_transaction_finish(transaction, &error);
            goto cleanup;
        }
    }
    if (request_headers.content_length > request_limit) {
        int response_written;
        failure_status = msconnector_runtime_error_http_status(runtime,
            MSCONNECTOR_ERROR_BODY_TOO_LARGE);
        (void)msconnector_runtime_transaction_fail(transaction,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, &error);
        response_written = sidecar_write_error(client, failure_status, &deadline);
        sidecar_record_failure_action(transaction, failure_status, response_written, &error);
        (void)msconnector_runtime_transaction_finish(transaction, &error);
        goto cleanup;
    }
    if (request_headers.content_length > 0U) {
        request_body = malloc(request_headers.content_length);
        if (request_body == NULL) goto transaction_error;
        while (body_read < request_headers.content_length) {
            size_t received;
            size_t wanted = request_headers.content_length - body_read;
            if (wanted > SIDECAR_IO_CHUNK) wanted = SIDECAR_IO_CHUNK;
            if (!sidecar_recv_some(client, request_body + body_read, wanted, &deadline, &received)) { failure_origin = SIDECAR_FAILURE_CLIENT; goto transaction_error; }
            if (!msconnector_runtime_transaction_append_request_body_chunk(transaction, request_body + body_read, received, &error)) {
                failure_status = msconnector_runtime_error_http_status(runtime, error.code);
                goto transaction_error;
            }
            body_read += received;
        }
    }
    if (!msconnector_runtime_transaction_finish_request_body(transaction, &decision, &error)) goto transaction_error;
    if (msconnector_decision_is_disruptive(&decision)) {
        if (!sidecar_write_decision(client, &decision, &deadline)) {
            sidecar_record_decision_delivery_failure(transaction, &decision, &error);
            (void)msconnector_runtime_transaction_finish(transaction, &error);
            goto cleanup;
        }
        sidecar_record_action(transaction, &decision, &error);
        (void)msconnector_runtime_transaction_finish(transaction, &error);
        goto cleanup;
    }
    upstream = sidecar_connect(options->upstream, &deadline);
    if (upstream < 0) { failure_origin = SIDECAR_FAILURE_UPSTREAM; goto transaction_error; }
    {
        char request_line[600];
        (void)snprintf(request_line, sizeof(request_line), "%s %s HTTP/1.1\r\n",
                       request_headers.method, request_headers.uri);
        if (!sidecar_write_upstream_request(upstream, request_line, &request_headers, request_body, body_read, &deadline)) { failure_origin = SIDECAR_FAILURE_UPSTREAM; goto transaction_error; }
    }
    if (!sidecar_read_header_block(upstream, &deadline, header_limit, &response_block, &response_size)) {
        failure_origin = SIDECAR_FAILURE_UPSTREAM;
        goto transaction_error;
    }
    if (!sidecar_parse_headers(response_block, response_size, header_limit, count_limit, 0,
                               request_is_head, &response_headers) || response_headers.chunked ||
        response_headers.upgrade) {
        failure_origin = SIDECAR_FAILURE_PROTOCOL;
        goto transaction_error;
    }
    if (response_headers.content_length > response_limit) {
        int response_written;
        failure_status = msconnector_runtime_error_http_status(runtime, MSCONNECTOR_ERROR_BODY_TOO_LARGE);
        (void)msconnector_runtime_transaction_fail(transaction,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, &error);
        response_written = sidecar_write_error(client, failure_status, &deadline);
        sidecar_record_failure_action(transaction, failure_status, response_written, &error);
        (void)msconnector_runtime_transaction_finish(transaction, &error);
        goto cleanup;
    }
    {
        msconnector_response response;
        memset(&response, 0, sizeof(response));
        response.status = response_headers.status_code;
        response.http_version = response_headers.version;
        response.headers = response_headers.items;
        response.header_count = response_headers.count;
        if (!msconnector_runtime_transaction_process_response_headers(transaction, &response, &decision, &error)) {
            failure_origin = SIDECAR_FAILURE_CONNECTOR;
            goto transaction_error;
        }
        response_blocked = msconnector_decision_is_disruptive(&decision);
        if (response_blocked) {
            if (!sidecar_write_decision(client, &decision, &deadline)) {
                sidecar_record_decision_delivery_failure(transaction, &decision, &error);
                (void)msconnector_runtime_transaction_finish(transaction, &error);
                goto cleanup;
            }
            sidecar_record_action(transaction, &decision, &error);
            (void)msconnector_runtime_transaction_finish(transaction, &error);
            goto cleanup;
        }
    }
    if (response_headers.content_length > 0U && !response_headers.no_body) {
        response_body = malloc(response_headers.content_length);
        if (response_body == NULL) goto transaction_error;
        body_read = 0U;
        while (body_read < response_headers.content_length) {
            size_t received;
            size_t wanted = response_headers.content_length - body_read;
            if (wanted > SIDECAR_IO_CHUNK) wanted = SIDECAR_IO_CHUNK;
            if (!sidecar_recv_some(upstream, response_body + body_read, wanted, &deadline, &received)) {
                failure_origin = SIDECAR_FAILURE_UPSTREAM;
                goto transaction_error;
            }
            if (!msconnector_runtime_transaction_append_response_body_chunk(transaction, response_body + body_read, received, &error)) {
                failure_origin = SIDECAR_FAILURE_CONNECTOR;
                goto transaction_error;
            }
            body_read += received;
        }
    }
    if (!msconnector_runtime_transaction_finish_response_body(transaction, &decision, &error)) goto transaction_error;
    if (response_blocked || msconnector_decision_is_disruptive(&decision)) {
        if (!sidecar_write_decision(client, &decision, &deadline)) {
            sidecar_record_decision_delivery_failure(transaction, &decision, &error);
            (void)msconnector_runtime_transaction_finish(transaction, &error);
            goto cleanup;
        }
        sidecar_record_action(transaction, &decision, &error);
    } else {
        char status_line[64];
        size_t response_body_size = response_headers.no_body ? 0U :
            response_headers.content_length;
        (void)snprintf(status_line, sizeof(status_line), "HTTP/1.1 %d Proxied\r\n",
                       response_headers.status_code);
        if (!sidecar_write_upstream_response_headers(client, status_line,
                                                     &response_headers, &deadline)) {
            failure_origin = SIDECAR_FAILURE_CLIENT;
            goto transaction_error;
        }
        client_response_started = 1;
        if (!msconnector_runtime_transaction_set_response_commit_state_checked(transaction, 1, 0,
                                                                                &error)) {
            failure_status = msconnector_runtime_error_http_status(runtime, error.code);
            goto transaction_error;
        }
        if (response_body_size > 0U) {
            size_t bytes_sent = 0U;
            if (!sidecar_send_all_observed(client, response_body, response_body_size,
                                           &deadline, &bytes_sent)) {
                if (bytes_sent > 0U) {
                    (void)msconnector_runtime_transaction_set_response_commit_state_checked(
                        transaction, 1, 1, &error);
                }
                failure_origin = SIDECAR_FAILURE_CLIENT;
                goto transaction_error;
            }
            if (!msconnector_runtime_transaction_set_response_commit_state_checked(transaction, 1, 1,
                                                                                    &error)) {
                failure_status = msconnector_runtime_error_http_status(runtime, error.code);
                goto transaction_error;
            }
        }
    }
    (void)msconnector_runtime_transaction_finish(transaction, &error);
    result = 1;
    goto cleanup;
runtime_error:
    if (transaction != NULL) {
        int status = sidecar_remaining(&deadline) == 0 ? 504 : 502;
        int response_written;
        if (sidecar_remaining(&deadline) == 0) (void)msconnector_runtime_transaction_timeout(transaction, &error);
        else (void)msconnector_runtime_transaction_fail(transaction,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, &error);
        response_written = sidecar_write_error(client, status, &deadline);
        sidecar_record_failure_action(transaction, status, response_written, &error);
        (void)msconnector_runtime_transaction_finish(transaction, &error);
    } else {
        (void)sidecar_write_error(client, sidecar_remaining(&deadline) == 0 ? 504 : 502, &deadline);
    }
    goto cleanup;
transaction_error:
    if (transaction != NULL) {
        int status = sidecar_remaining(&deadline) == 0 ? 504 : failure_status;
        int response_written = 0;
        if (sidecar_remaining(&deadline) == 0) (void)msconnector_runtime_transaction_timeout(transaction, &error);
        else (void)msconnector_runtime_transaction_fail(transaction,
            sidecar_failure_error_class(failure_origin), &error);
        if (!client_response_started) {
            response_written = sidecar_write_error(client, status, &deadline);
        }
        sidecar_record_failure_action(transaction, status, response_written, &error);
        (void)msconnector_runtime_transaction_finish(transaction, &error);
    }
cleanup:
    if (upstream >= 0) close(upstream);
    msconnector_runtime_transaction_destroy(&transaction);
    sidecar_headers_release(&request_headers);
    sidecar_headers_release(&response_headers);
    free(request_body);
    free(response_body);
    free(response_block);
    return result;
}
#endif

static void *sidecar_worker_main(void *argument) {
    sidecar_worker *worker = argument;
    sidecar_runtime_context *context = worker->context;
    (void)sidecar_exchange(worker->client, context->options, context->runtime);
    (void)shutdown(worker->client, SHUT_RDWR);
    close(worker->client);
    (void)pthread_mutex_lock(&context->lock);
    --context->active;
    (void)pthread_mutex_unlock(&context->lock);
    free(worker);
    return NULL;
}

static int sidecar_parse_args(int argc, char **argv, sidecar_options *options) {
    memset(options, 0, sizeof(*options));
    options->timeout_ms = SIDECAR_DEFAULT_TIMEOUT_MS;
    for (size_t i = 1U; i < (size_t)argc; i += 2U) {
        if (i + 1U >= (size_t)argc) return 0;
        if (strcmp(argv[i], "--config") == 0) options->config = argv[i + 1U];
        else if (strcmp(argv[i], "--listen") == 0) options->listen = argv[i + 1U];
        else if (strcmp(argv[i], "--upstream") == 0) options->upstream = argv[i + 1U];
        else if (strcmp(argv[i], "--timeout-ms") == 0) {
            size_t value;
            if (!sidecar_decimal(argv[i + 1U], &value) || value == 0U) return 0;
            options->timeout_ms = value;
        } else return 0;
    }
    return options->config != NULL && options->listen != NULL && options->upstream != NULL;
}

static void sidecar_close_client(int client, int write_error) {
    if (write_error) {
        (void)sidecar_write_error(client, 503,
            &(sidecar_deadline){ sidecar_now_ms() + 1000U });
    }
    (void)shutdown(client, SHUT_RDWR);
    close(client);
}

static int sidecar_prepare_client(int client) {
    int flags = fcntl(client, F_GETFD, 0);
    if (flags >= 0) (void)fcntl(client, F_SETFD, flags | FD_CLOEXEC);
    flags = fcntl(client, F_GETFL, 0);
    if (flags < 0 || fcntl(client, F_SETFL, flags | O_NONBLOCK) < 0) {
        sidecar_close_client(client, 1);
        return 0;
    }
    return 1;
}

static int sidecar_dispatch_client(sidecar_runtime_context *context, int client) {
    pthread_t thread;
    sidecar_worker *worker;
    int create_result;
    (void)pthread_mutex_lock(&context->lock);
    if (context->active >= SIDECAR_MAX_PARALLEL) {
        (void)pthread_mutex_unlock(&context->lock);
        sidecar_close_client(client, 1);
        return 0;
    }
    ++context->active;
    (void)pthread_mutex_unlock(&context->lock);
    worker = calloc(1U, sizeof(*worker));
    if (worker != NULL) {
        worker->context = context;
        worker->client = client;
        create_result = pthread_create(&thread, NULL, sidecar_worker_main, worker);
    } else {
        create_result = ENOMEM;
    }
    if (worker == NULL || create_result != 0) {
        free(worker);
        (void)pthread_mutex_lock(&context->lock);
        --context->active;
        (void)pthread_mutex_unlock(&context->lock);
        sidecar_close_client(client, 1);
        return 0;
    }
    (void)pthread_detach(thread);
    return 1;
}

static void sidecar_wait_for_workers(sidecar_runtime_context *context) {
    for (;;) {
        unsigned int active;
        struct timespec pause = { 0, 1000000L };
        (void)pthread_mutex_lock(&context->lock);
        active = context->active;
        (void)pthread_mutex_unlock(&context->lock);
        if (active == 0U) return;
        (void)nanosleep(&pause, NULL);
    }
}

int msconnector_stock_sidecar_main(int argc, char **argv) {
    sidecar_options options;
    msconnector_runtime *runtime = NULL;
    msconnector_error error;
    int listener;
    sidecar_runtime_context context;
    if (!sidecar_parse_args(argc, argv, &options)) return 64;
    if (!msconnector_runtime_create(SIDECAR_RUNTIME_CONNECTOR, options.config, &runtime, (char[256]){0}, 256U) ||
        !msconnector_runtime_set_event_integration_mode(runtime, "stock-lighttpd-sidecar") ||
        !msconnector_runtime_set_transaction_profile(runtime,
            msconnector_profile_registry_find("lighttpd-stock"))) {
        msconnector_runtime_destroy(&runtime);
        return 78;
    }
    if (msconnector_runtime_request_body_mode(runtime) != MSCONNECTOR_BODY_MODE_STREAMING ||
        msconnector_runtime_response_body_mode(runtime) != MSCONNECTOR_BODY_MODE_STREAMING ||
        !sidecar_runtime_limits_supported(runtime)) {
        msconnector_runtime_destroy(&runtime);
        return 78;
    }
    listener = sidecar_listener(options.listen);
    if (listener < 0) {
        msconnector_runtime_destroy(&runtime);
        return 69;
    }
    memset(&context, 0, sizeof(context));
    context.options = &options;
    context.runtime = runtime;
    (void)pthread_mutex_init(&context.lock, NULL);
    (void)signal(SIGPIPE, SIG_IGN);
    int accept_status = 0;
    for (;;) {
        int client = accept(listener, NULL, NULL);
        if (client < 0) {
            if (errno == EINTR) continue;
            accept_status = 69;
            break;
        }
        if (!sidecar_prepare_client(client)) continue;
        (void)sidecar_dispatch_client(&context, client);
    }
    close(listener);
    sidecar_wait_for_workers(&context);
    (void)pthread_mutex_destroy(&context.lock);
    msconnector_error_init(&error);
    msconnector_runtime_destroy(&runtime);
    return accept_status;
}

#ifdef MSCONNECTOR_STOCK_SIDECAR_MAIN
int main(int argc, char **argv) { return msconnector_stock_sidecar_main(argc, argv); }
#endif
