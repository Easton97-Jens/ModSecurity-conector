#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "response_companion_client.h"

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

#define MRC1_MAGIC "MRC1"
#define MRC1_VERSION MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_PROTOCOL_VERSION
#define MRC1_FRAME_HEADER_SIZE 12U
#define MRC1_MAX_REDIRECT 4096U
#define MRC1_MAX_RULE_ID 256U
#define MRC1_MAX_HTTP_VERSION 64U
#define MRC1_MAX_HEADER_NAME 256U
#define MRC1_MAX_HEADER_VALUE 8192U

enum mrc1_opcode {
    MRC1_CLAIM = 1U,
    MRC1_RESPONSE_HEADERS = 2U,
    MRC1_RESPONSE_BODY = 3U,
    MRC1_RESPONSE_EOS = 4U,
    MRC1_COMMIT = 5U,
    MRC1_CANCEL = 6U,
    MRC1_RELEASE = 7U,
    MRC1_OUTCOME = 8U,
    MRC1_RESULT = 128U
};

enum mrc1_result_code { MRC1_RESULT_OK = 0U, MRC1_RESULT_ERROR = 1U };

typedef enum mrc1_io_result {
    MRC1_IO_RESULT_OK = 0,
    MRC1_IO_RESULT_TIMEOUT,
    MRC1_IO_RESULT_PEER_CLOSED,
    MRC1_IO_RESULT_ERROR
} mrc1_io_result;

static void set_error(msconnector_error *error, msconnector_error_code code,
    const char *message)
{
    if (error != NULL) {
        msconnector_error_set(error, code, message, "response_companion_client");
    }
}

static int client_is_open(const msconnector_response_companion_client *client)
{
    return client != NULL && client->opened && !client->closed &&
        client->socket_fd >= 0;
}

static void client_reset_transaction(msconnector_response_companion_client *client)
{
    if (client == NULL) {
        return;
    }
    client->claimed = 0;
    client->response_headers = 0;
    client->committed = 0;
    client->body_started = 0;
    client->response_eos = 0;
    client->outcome_recorded = 0;
}

static void client_mark_closed(msconnector_response_companion_client *client)
{
    client_reset_transaction(client);
    if (client != NULL) {
        client->closed = 1;
    }
}

static uint64_t now_ms(void)
{
    struct timespec value;
    if (clock_gettime(CLOCK_MONOTONIC, &value) != 0) {
        return 0U;
    }
    return (uint64_t)value.tv_sec * 1000U +
        (uint64_t)value.tv_nsec / 1000000U;
}

static uint64_t deadline(const msconnector_response_companion_client *client)
{
    uint64_t current;
    if (client == NULL || client->timeout_ms == 0U) {
        return 0U;
    }
    current = now_ms();
    if (current == 0U || UINT64_MAX - current < client->timeout_ms) {
        return 0U;
    }
    return current + client->timeout_ms;
}

static mrc1_io_result wait_fd(int fd, short events, uint64_t end)
{
    struct pollfd descriptor;
    uint64_t current;
    int timeout;
    int value;

    if (fd < 0 || end == 0U) {
        return MRC1_IO_RESULT_ERROR;
    }
    current = now_ms();
    if (current == 0U || current >= end) {
        return current == 0U ? MRC1_IO_RESULT_ERROR : MRC1_IO_RESULT_TIMEOUT;
    }
    timeout = end - current > (uint64_t)INT_MAX ? INT_MAX :
        (int)(end - current);
    memset(&descriptor, 0, sizeof(descriptor));
    descriptor.fd = fd;
    descriptor.events = events;
    do {
        value = poll(&descriptor, 1U, timeout);
    } while (value < 0 && errno == EINTR);
    if (value == 0) {
        return MRC1_IO_RESULT_TIMEOUT;
    }
    if (value < 0 || (descriptor.revents & (POLLERR | POLLNVAL)) != 0) {
        return MRC1_IO_RESULT_ERROR;
    }
    if ((descriptor.revents & events) != 0) {
        return MRC1_IO_RESULT_OK;
    }
    if ((descriptor.revents & POLLHUP) != 0) {
        return MRC1_IO_RESULT_PEER_CLOSED;
    }
    value = -1;
    return value < 0 ? MRC1_IO_RESULT_ERROR : MRC1_IO_RESULT_OK;
}

static mrc1_io_result write_all(const msconnector_response_companion_client *client,
    const unsigned char *data, size_t size, uint64_t end)
{
    size_t offset = 0U;
    while (offset < size) {
        ssize_t written;
        const mrc1_io_result wait_result = wait_fd(client->socket_fd, POLLOUT, end);

        if (wait_result != MRC1_IO_RESULT_OK) {
            return wait_result;
        }
        written = send(client->socket_fd, data + offset, size - offset,
            MSG_NOSIGNAL);
        if (written > 0) {
            offset += (size_t)written;
        } else if (written < 0 && (errno == EINTR || errno == EAGAIN ||
            errno == EWOULDBLOCK)) {
            continue;
        } else if (written == 0) {
            return MRC1_IO_RESULT_PEER_CLOSED;
        } else {
            return MRC1_IO_RESULT_ERROR;
        }
    }
    return offset == size ? MRC1_IO_RESULT_OK : MRC1_IO_RESULT_ERROR;
}

static mrc1_io_result read_all(const msconnector_response_companion_client *client,
    unsigned char *data, size_t size, uint64_t end)
{
    size_t offset = 0U;
    while (offset < size) {
        ssize_t received;
        const mrc1_io_result wait_result = wait_fd(client->socket_fd, POLLIN, end);

        if (wait_result != MRC1_IO_RESULT_OK) {
            return wait_result;
        }
        received = recv(client->socket_fd, data + offset, size - offset, 0);
        if (received > 0) {
            offset += (size_t)received;
        } else if (received < 0 && (errno == EINTR || errno == EAGAIN ||
            errno == EWOULDBLOCK)) {
            continue;
        } else if (received == 0) {
            return MRC1_IO_RESULT_PEER_CLOSED;
        } else {
            return MRC1_IO_RESULT_ERROR;
        }
    }
    return MRC1_IO_RESULT_OK;
}

static void set_io_result_error(msconnector_error *error,
    mrc1_io_result result, const char *timeout_message,
    const char *io_message)
{
    set_error(error, result == MRC1_IO_RESULT_TIMEOUT ?
        MSCONNECTOR_ERROR_TIMEOUT : MSCONNECTOR_ERROR_IO,
        result == MRC1_IO_RESULT_TIMEOUT ? timeout_message : io_message);
}

static void put_u16(unsigned char *value, uint16_t number)
{
    value[0] = (unsigned char)(number >> 8U);
    value[1] = (unsigned char)number;
}

static uint16_t get_u16(const unsigned char *value)
{
    return (uint16_t)(((uint16_t)value[0] << 8U) | value[1]);
}

static void put_u32(unsigned char *value, uint32_t number)
{
    value[0] = (unsigned char)(number >> 24U);
    value[1] = (unsigned char)(number >> 16U);
    value[2] = (unsigned char)(number >> 8U);
    value[3] = (unsigned char)number;
}

static uint32_t get_u32(const unsigned char *value)
{
    return ((uint32_t)value[0] << 24U) | ((uint32_t)value[1] << 16U) |
        ((uint32_t)value[2] << 8U) | value[3];
}

static int send_frame(const msconnector_response_companion_client *client,
    uint8_t opcode, const unsigned char *payload, size_t payload_size,
    uint64_t end, msconnector_error *error)
{
    unsigned char header[MRC1_FRAME_HEADER_SIZE];
    mrc1_io_result io_result;
    if (!client_is_open(client)) {
        set_error(error, MSCONNECTOR_ERROR_IO,
            "MRC1 client connection is not open");
        return 0;
    }
    if (payload_size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME ||
        (payload_size > 0U && payload == NULL)) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 client frame arguments are invalid");
        return 0;
    }
    if (end == 0U) {
        set_error(error, MSCONNECTOR_ERROR_TIMEOUT,
            "MRC1 client send deadline unavailable");
        return 0;
    }
    memset(header, 0, sizeof(header));
    memcpy(header, MRC1_MAGIC, 4U);
    header[4] = MRC1_VERSION;
    header[5] = opcode;
    put_u32(header + 8U, (uint32_t)payload_size);
    io_result = write_all(client, header, sizeof(header), end);
    if (io_result == MRC1_IO_RESULT_OK && payload_size > 0U) {
        io_result = write_all(client, payload, payload_size, end);
    }
    if (io_result != MRC1_IO_RESULT_OK) {
        set_io_result_error(error, io_result, "MRC1 client write timed out",
            "MRC1 client write failed");
        return 0;
    }
    return 1;
}

static int valid_status_for_success(uint8_t opcode, msconnector_decision_kind kind,
    uint16_t status)
{
    if (status >= 100U && status <= 599U) {
        return 1;
    }
    if ((opcode == MRC1_CANCEL || opcode == MRC1_RELEASE) &&
        kind == MSCONNECTOR_DECISION_KIND_ERROR) {
        return status == 0U;
    }
    return status == 0U && (kind == MSCONNECTOR_DECISION_KIND_ALLOW ||
        kind == MSCONNECTOR_DECISION_KIND_LOG_ONLY ||
        kind == MSCONNECTOR_DECISION_KIND_DROP ||
        kind == MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT);
}

static int valid_result_text(const unsigned char *value, size_t size)
{
    for (size_t index = 0U; index < size; ++index) {
        if (value[index] < 32U || value[index] == 127U ||
            value[index] == '\r' || value[index] == '\n' ||
            value[index] == '\0') {
            return 0;
        }
    }
    return 1;
}

static int receive_result(const msconnector_response_companion_client *client,
    uint8_t request_opcode, msconnector_response_companion_result *result,
    uint64_t end, msconnector_error *error)
{
    unsigned char header[MRC1_FRAME_HEADER_SIZE];
    unsigned char *payload = NULL;
    uint32_t size;
    uint16_t redirect_size;
    uint16_t rule_size;
    uint8_t code;
    uint8_t kind;
    uint16_t error_code;
    uint16_t status;
    mrc1_io_result io_result;
    int ok = 0;

    if (result == NULL) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 result output is required");
        return 0;
    }
    if (end == 0U) {
        set_error(error, MSCONNECTOR_ERROR_TIMEOUT,
            "MRC1 result deadline is unavailable");
        return 0;
    }
    io_result = read_all(client, header, sizeof(header), end);
    if (io_result != MRC1_IO_RESULT_OK) {
        set_io_result_error(error, io_result, "MRC1 result header timed out",
            "MRC1 result header could not be read");
        return 0;
    }
    if (memcmp(header, MRC1_MAGIC, 4U) != 0 || header[4] != MRC1_VERSION ||
        header[5] != MRC1_RESULT || header[6] != 0U || header[7] != 0U) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 result frame header is invalid");
        return 0;
    }
    size = get_u32(header + 8U);
    if (size < 12U || size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME) {
        set_error(error, MSCONNECTOR_ERROR_EVENT_TOO_LARGE,
            "MRC1 result frame exceeds its limit");
        return 0;
    }
    payload = calloc(size, 1U);
    if (payload == NULL) {
        set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "MRC1 result payload allocation failed");
        goto cleanup;
    }
    io_result = read_all(client, payload, size, end);
    if (io_result != MRC1_IO_RESULT_OK) {
        set_io_result_error(error, io_result, "MRC1 result payload timed out",
            "MRC1 result payload could not be read");
        goto cleanup;
    }
    code = payload[1];
    kind = payload[2];
    error_code = get_u16(payload + 6U);
    status = get_u16(payload + 4U);
    redirect_size = get_u16(payload + 8U);
    rule_size = get_u16(payload + 10U);
    if (payload[0] != request_opcode || payload[3] != 0U || code > MRC1_RESULT_ERROR ||
        kind > MSCONNECTOR_DECISION_KIND_UNSUPPORTED ||
        error_code > MSCONNECTOR_ERROR_INTERNAL ||
        (code == MRC1_RESULT_OK) != (error_code == 0U) ||
        12U + (size_t)redirect_size + (size_t)rule_size != size ||
        redirect_size > MRC1_MAX_REDIRECT || rule_size > MRC1_MAX_RULE_ID ||
        !valid_result_text(payload + 12U, redirect_size) ||
        !valid_result_text(payload + 12U + redirect_size, rule_size) ||
        (code == MRC1_RESULT_OK && !valid_status_for_success(request_opcode,
            (msconnector_decision_kind)kind, status)) ||
        ((msconnector_decision_kind)kind == MSCONNECTOR_DECISION_KIND_REDIRECT &&
            (status < 300U || status > 399U || redirect_size == 0U)) ||
        ((msconnector_decision_kind)kind != MSCONNECTOR_DECISION_KIND_REDIRECT &&
            redirect_size != 0U)) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 result payload is malformed");
        goto cleanup;
    }
    result->success = code == MRC1_RESULT_OK;
    result->decision = (msconnector_decision_kind)kind;
    result->status = status;
    result->error_code = (msconnector_error_code)error_code;
    result->redirect_url = calloc((size_t)redirect_size + 1U, 1U);
    result->rule_id = calloc((size_t)rule_size + 1U, 1U);
    if (result->redirect_url == NULL || result->rule_id == NULL) {
        set_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "MRC1 result text allocation failed");
        goto cleanup;
    }
    memcpy(result->redirect_url, payload + 12U, redirect_size);
    memcpy(result->rule_id, payload + 12U + redirect_size, rule_size);
    ok = 1;

cleanup:
    free(payload);
    if (!ok) {
        msconnector_response_companion_result_destroy(result);
    }
    return ok;
}

static int exchange(msconnector_response_companion_client *client, uint8_t opcode,
    const unsigned char *payload, size_t payload_size,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    uint64_t end;
    if (!client_is_open(client) || result == NULL) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "MRC1 client exchange is not available");
        return 0;
    }
    msconnector_response_companion_result_destroy(result);
    if ((end = deadline(client)) == 0U) {
        set_error(error, MSCONNECTOR_ERROR_TIMEOUT,
            "MRC1 client exchange deadline unavailable");
        client_mark_closed(client);
        return 0;
    }
    if (!send_frame(client, opcode, payload, payload_size, end, error) ||
        !receive_result(client, opcode, result, end, error)) {
        client_mark_closed(client);
        return 0;
    }
    if (!result->success) {
        set_error(error, result->error_code == MSCONNECTOR_ERROR_NONE ?
            MSCONNECTOR_ERROR_PROTOCOL : result->error_code,
            "MRC1 companion rejected the operation");
        client_mark_closed(client);
    }
    return result->success;
}

static size_t bounded_string_size(const char *value, size_t maximum)
{
    size_t size = 0U;
    if (value == NULL) {
        return 0U;
    }
    while (size <= maximum && value[size] != '\0') {
        ++size;
    }
    return size;
}

static int append_text(unsigned char *payload, size_t capacity, size_t *offset,
    const char *value, size_t maximum, int required)
{
    size_t size = bounded_string_size(value, maximum);
    if (size > maximum || (required && size == 0U) || *offset > capacity ||
        capacity - *offset < 2U + size) {
        return 0;
    }
    put_u16(payload + *offset, (uint16_t)size);
    *offset += 2U;
    if (size > 0U) {
        memcpy(payload + *offset, value, size);
        *offset += size;
    }
    return 1;
}

static int valid_header_text(const char *value, size_t size, int name)
{
    if (value == NULL || size == 0U) {
        return !name;
    }
    for (size_t index = 0U; index < size; ++index) {
        const unsigned char character = (unsigned char)value[index];
        if (character < 32U || character == 127U || character == '\r' ||
            character == '\n' || (name && character == ':')) {
            return 0;
        }
    }
    return 1;
}

static int valid_response_header_name(const char *value, size_t size)
{
    if (size == sizeof(":status") - 1U &&
        memcmp(value, ":status", sizeof(":status") - 1U) == 0) {
        return 1;
    }
    return valid_header_text(value, size, 1);
}

static int valid_status_pseudoheader(const msconnector_header *header, int status)
{
    char expected[4];
    int expected_size;

    if (header == NULL || header->name_size != sizeof(":status") - 1U ||
        memcmp(header->name, ":status", sizeof(":status") - 1U) != 0) {
        return 1;
    }
    expected_size = snprintf(expected, sizeof(expected), "%d", status);
    return expected_size > 0 && (size_t)expected_size == header->value_size &&
        memcmp(header->value, expected, header->value_size) == 0;
}

void msconnector_response_companion_result_destroy(
    msconnector_response_companion_result *result)
{
    if (result != NULL) {
        free(result->redirect_url);
        free(result->rule_id);
        memset(result, 0, sizeof(*result));
    }
}

int msconnector_response_companion_client_open(
    msconnector_response_companion_client *client, const char *socket_path,
    uint64_t timeout_ms, uid_t expected_uid, gid_t expected_gid,
    msconnector_error *error)
{
    struct sockaddr_un address;
    size_t path_size;
    uint64_t connect_deadline;
    int fd;

    if (client != NULL && client->opened) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "MRC1 client must be closed before reopening");
        return 0;
    }
    if (client == NULL || socket_path == NULL || timeout_ms == 0U) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 client arguments are invalid");
        return 0;
    }
    path_size = strlen(socket_path);
    if (path_size == 0U || path_size >= sizeof(address.sun_path)) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 client arguments are invalid");
        return 0;
    }
#if !defined(__linux__)
    set_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY,
        "MRC1 peer credential verification is unavailable");
    return 0;
#else
    if ((connect_deadline = now_ms()) == 0U ||
        UINT64_MAX - connect_deadline < timeout_ms) {
        set_error(error, MSCONNECTOR_ERROR_TIMEOUT,
            "MRC1 client connect deadline is unavailable");
        return 0;
    }
    connect_deadline += timeout_ms;
    fd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC | SOCK_NONBLOCK, 0);
    if (fd < 0) {
        set_error(error, MSCONNECTOR_ERROR_IO, "MRC1 client socket failed");
        return 0;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, socket_path, path_size + 1U);
    if (connect(fd, (const struct sockaddr *)&address, sizeof(address)) != 0) {
        int socket_error = 0;
        socklen_t socket_error_size = sizeof(socket_error);

        if (errno != EINPROGRESS || wait_fd(fd, POLLOUT, connect_deadline) !=
                MRC1_IO_RESULT_OK ||
            getsockopt(fd, SOL_SOCKET, SO_ERROR, &socket_error,
                &socket_error_size) != 0 || socket_error != 0) {
            const uint64_t current = now_ms();

            close(fd);
            set_error(error, current != 0U && current >= connect_deadline ?
                MSCONNECTOR_ERROR_TIMEOUT : MSCONNECTOR_ERROR_IO,
                "MRC1 client connect failed");
            return 0;
        }
    }
    {
        struct ucred peer;
        socklen_t peer_size = sizeof(peer);
        if (getsockopt(fd, SOL_SOCKET, SO_PEERCRED, &peer, &peer_size) != 0 ||
            peer_size != sizeof(peer) || peer.uid != expected_uid ||
            peer.gid != expected_gid) {
            close(fd);
            set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
                "MRC1 peer identity is not trusted");
            return 0;
        }
    }
    memset(client, 0, sizeof(*client));
    client->socket_fd = fd;
    client->timeout_ms = timeout_ms;
    client->expected_uid = expected_uid;
    client->expected_gid = expected_gid;
    client->opened = 1;
    return 1;
#endif
}

int msconnector_response_companion_client_claim(
    msconnector_response_companion_client *client, const char *handle,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    const size_t size = bounded_string_size(handle,
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE);
    if (!client_is_open(client) || handle == NULL || size !=
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE - 1U ||
        client->claimed) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "MRC1 CLAIM arguments are invalid");
        return 0;
    }
    for (size_t index = 0U; index < size; ++index) {
        if (!((handle[index] >= '0' && handle[index] <= '9') ||
            (handle[index] >= 'a' && handle[index] <= 'f'))) {
            set_error(error, MSCONNECTOR_ERROR_PROTOCOL, "MRC1 CLAIM handle is invalid");
            return 0;
        }
    }
    if (!exchange(client, MRC1_CLAIM, (const unsigned char *)handle, size,
        result, error)) {
        return 0;
    }
    client->claimed = 1;
    return 1;
}

int msconnector_response_companion_client_response_headers(
    msconnector_response_companion_client *client, const msconnector_response *response,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    unsigned char payload[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME];
    size_t offset = 0U;
    size_t version_size;
    size_t header_bytes = 0U;
    if (!client_is_open(client) || response == NULL || !client->claimed ||
        client->response_headers || client->committed || client->outcome_recorded ||
        client->response_eos || response->status < 100 || response->status > 999 ||
        response->header_count > UINT16_MAX ||
        (response->header_count > 0U && response->headers == NULL)) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "MRC1 response headers are out of sequence or invalid");
        return 0;
    }
    version_size = bounded_string_size(response->http_version, MRC1_MAX_HTTP_VERSION);
    if (version_size == 0U || version_size > MRC1_MAX_HTTP_VERSION ||
        !valid_header_text(response->http_version, version_size, 0) ||
        sizeof(payload) < 2U + 2U + version_size + 2U +
        response->header_count * 4U) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL, "MRC1 response version is invalid");
        return 0;
    }
    put_u16(payload + offset, (uint16_t)response->status); offset += 2U;
    if (!append_text(payload, sizeof(payload), &offset, response->http_version,
        MRC1_MAX_HTTP_VERSION, 1)) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL, "MRC1 response version is invalid");
        return 0;
    }
    put_u16(payload + offset, (uint16_t)response->header_count); offset += 2U;
    for (size_t index = 0U; index < response->header_count; ++index) {
        const msconnector_header *header = &response->headers[index];
        if (header->name == NULL || header->value == NULL ||
            header->name_size == 0U || header->name_size > MRC1_MAX_HEADER_NAME ||
            header->value_size > MRC1_MAX_HEADER_VALUE ||
            memchr(header->name, '\0', header->name_size) != NULL ||
            memchr(header->value, '\0', header->value_size) != NULL ||
            !valid_response_header_name(header->name, header->name_size) ||
            !valid_header_text(header->value, header->value_size, 0) ||
            !valid_status_pseudoheader(header, response->status) ||
            header_bytes > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME ||
            header->name_size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME - header_bytes ||
            header->value_size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME -
                header_bytes - header->name_size ||
            offset > sizeof(payload) - 4U - header->name_size - header->value_size) {
            set_error(error, MSCONNECTOR_ERROR_HEADER_TOO_LARGE,
                "MRC1 response header exceeds its limit");
            return 0;
        }
        put_u16(payload + offset, (uint16_t)header->name_size); offset += 2U;
        memcpy(payload + offset, header->name, header->name_size); offset += header->name_size;
        put_u16(payload + offset, (uint16_t)header->value_size); offset += 2U;
        memcpy(payload + offset, header->value, header->value_size); offset += header->value_size;
        header_bytes += header->name_size + header->value_size;
    }
    if (!exchange(client, MRC1_RESPONSE_HEADERS, payload, offset, result, error)) {
        return 0;
    }
    client->response_headers = 1;
    return 1;
}

int msconnector_response_companion_client_commit(
    msconnector_response_companion_client *client, int headers_sent,
    int body_started, msconnector_response_companion_result *result,
    msconnector_error *error)
{
    unsigned char payload[2];
    if (!client_is_open(client) || !client->claimed || !client->response_headers ||
        client->committed || client->outcome_recorded || client->response_eos ||
        !headers_sent || headers_sent > 1 ||
        body_started < 0 || body_started > 1) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 COMMIT is invalid");
        return 0;
    }
    payload[0] = (unsigned char)headers_sent;
    payload[1] = (unsigned char)body_started;
    if (!exchange(client, MRC1_COMMIT, payload, sizeof(payload), result, error)) {
        return 0;
    }
    client->committed = 1;
    client->body_started = body_started != 0;
    return 1;
}

int msconnector_response_companion_client_body_chunk(
    msconnector_response_companion_client *client, const unsigned char *data,
    size_t size, msconnector_response_companion_result *result,
    msconnector_error *error)
{
    if (!client_is_open(client) || !client->claimed || !client->response_headers ||
        !client->committed || client->outcome_recorded || client->response_eos) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "MRC1 response body chunk is out of sequence");
        return 0;
    }
    if (size > MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK ||
        (size > 0U && data == NULL)) {
        set_error(error, MSCONNECTOR_ERROR_BODY_TOO_LARGE,
            "MRC1 response body chunk is invalid");
        return 0;
    }
    if (!exchange(client, MRC1_RESPONSE_BODY, data, size, result, error)) {
        return 0;
    }
    client->body_started = 1;
    return 1;
}

int msconnector_response_companion_client_body_eos(
    msconnector_response_companion_client *client,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    if (!client_is_open(client) || !client->claimed || !client->response_headers ||
        !client->committed || client->outcome_recorded || client->response_eos) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 EOS is invalid");
        return 0;
    }
    if (!exchange(client, MRC1_RESPONSE_EOS, NULL, 0U, result, error)) {
        return 0;
    }
    client->response_eos = 1;
    return 1;
}

int msconnector_response_companion_client_outcome(
    msconnector_response_companion_client *client, msconnector_decision_action action,
    int visible_status, int connection_aborted,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    unsigned char payload[4];
    if (!client_is_open(client) || !client->claimed || !client->response_headers ||
        client->outcome_recorded || (client->committed && !client->response_eos) ||
        (int)action < 0 || action > MSCONNECTOR_DECISION_ACTION_RATE_LIMIT ||
        visible_status < 0 || visible_status > UINT16_MAX ||
        connection_aborted < 0 || connection_aborted > 1) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 OUTCOME is invalid");
        return 0;
    }
    payload[0] = (unsigned char)action;
    payload[1] = (unsigned char)connection_aborted;
    put_u16(payload + 2U, (uint16_t)visible_status);
    if (!exchange(client, MRC1_OUTCOME, payload, sizeof(payload), result, error)) {
        return 0;
    }
    client->outcome_recorded = 1;
    return 1;
}

static int valid_cancel_cause(msconnector_response_companion_cancel_cause cause)
{
    switch (cause) {
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_PROTOCOL_ERROR:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_TIMEOUT:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_UNAVAILABLE:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_INVALID_ENGINE_RESPONSE:
        return 1;
    default:
        return 0;
    }
}

int msconnector_response_companion_client_cancel_with_cause(
    msconnector_response_companion_client *client,
    msconnector_response_companion_cancel_cause cause,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    unsigned char payload;
    if (!client_is_open(client) || !client->claimed || client->response_eos ||
        !valid_cancel_cause(cause)) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 CANCEL is invalid");
        return 0;
    }
    payload = (unsigned char)cause;
    if (!exchange(client, MRC1_CANCEL, &payload, 1U, result, error)) {
        return 0;
    }
    client_reset_transaction(client);
    return 1;
}

int msconnector_response_companion_client_cancel(
    msconnector_response_companion_client *client, int upstream_disconnect,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    if (upstream_disconnect < 0 || upstream_disconnect > 1) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 CANCEL is invalid");
        return 0;
    }
    return msconnector_response_companion_client_cancel_with_cause(client,
        upstream_disconnect ? MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT :
            MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL,
        result, error);
}

int msconnector_response_companion_client_release(
    msconnector_response_companion_client *client,
    msconnector_response_companion_result *result, msconnector_error *error)
{
    if (!client_is_open(client) || !client->claimed || !client->response_eos) {
        set_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE, "MRC1 RELEASE is invalid");
        return 0;
    }
    if (!exchange(client, MRC1_RELEASE, NULL, 0U, result, error)) {
        return 0;
    }
    client_reset_transaction(client);
    return 1;
}

int msconnector_response_companion_client_close(
    msconnector_response_companion_client *client, msconnector_error *error)
{
    int result = 1;
    msconnector_error ignored;
    msconnector_response_companion_result response_result;
    if (client == NULL) {
        set_error(error, MSCONNECTOR_ERROR_PROTOCOL, "MRC1 client is null");
        return 0;
    }
    if (!client->opened) {
        return 1;
    }
    msconnector_error_init(&ignored);
    memset(&response_result, 0, sizeof(response_result));
    if (client_is_open(client) && client->claimed) {
        if (client->response_eos) {
            if (!msconnector_response_companion_client_release(client,
                &response_result, &ignored)) {
                result = 0;
            }
        } else if (!msconnector_response_companion_client_cancel(client, 0,
            &response_result, &ignored)) {
            result = 0;
        }
    }
    msconnector_response_companion_result_destroy(&response_result);
    if (client->socket_fd >= 0) {
        (void)close(client->socket_fd);
    }
    client->socket_fd = -1;
    client_reset_transaction(client);
    client->opened = 0;
    client->closed = 1;
    if (!result && error != NULL) {
        *error = ignored;
    }
    return result;
}
