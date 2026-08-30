#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "response_companion_transport.h"

#include "msconnector/decision_action.h"
#include "msconnector/limits.h"
#include "msconnector/memory.h"
#include "msconnector/response_helpers.h"

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <poll.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/un.h>
#include <time.h>
#include <unistd.h>

#define RESPONSE_COMPANION_MAGIC "MRC1"
#define RESPONSE_COMPANION_VERSION \
    MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_PROTOCOL_VERSION
#define RESPONSE_COMPANION_FRAME_HEADER_SIZE 12U
#define RESPONSE_COMPANION_LISTEN_BACKLOG 32
#define RESPONSE_COMPANION_ACCEPT_POLL_MS 250
#define RESPONSE_COMPANION_MAX_HTTP_VERSION \
    MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_HTTP_VERSION_SIZE
#define RESPONSE_COMPANION_MAX_HEADER_NAME 256U
#define RESPONSE_COMPANION_MAX_HEADER_VALUE 8192U
#define RESPONSE_COMPANION_MAX_RULE_ID 256U
#define RESPONSE_COMPANION_MAX_REDIRECT 4096U
#define RESPONSE_COMPANION_MAX_DECISION_TEXT MSCONNECTOR_MAX_LOG_MESSAGE_LENGTH

enum response_companion_opcode {
    RESPONSE_COMPANION_CLAIM = 1U,
    RESPONSE_COMPANION_RESPONSE_HEADERS = 2U,
    RESPONSE_COMPANION_RESPONSE_BODY = 3U,
    RESPONSE_COMPANION_RESPONSE_EOS = 4U,
    RESPONSE_COMPANION_COMMIT = 5U,
    RESPONSE_COMPANION_CANCEL = 6U,
    RESPONSE_COMPANION_RELEASE = 7U,
    RESPONSE_COMPANION_OUTCOME = 8U,
    RESPONSE_COMPANION_RESULT = 128U
};

static size_t response_companion_max_payload_for_opcode(uint8_t opcode)
{
    return opcode == RESPONSE_COMPANION_RESPONSE_HEADERS ?
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_RESPONSE_HEADER_FRAME :
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_FRAME;
}

typedef enum response_companion_io_result {
    RESPONSE_COMPANION_IO_READY = 0,
    RESPONSE_COMPANION_IO_TIMEOUT,
    RESPONSE_COMPANION_IO_PEER_CLOSED,
    RESPONSE_COMPANION_IO_ERROR
} response_companion_io_result;

typedef enum response_companion_frame_result {
    RESPONSE_COMPANION_FRAME_OK = 0,
    RESPONSE_COMPANION_FRAME_TIMEOUT,
    RESPONSE_COMPANION_FRAME_PEER_CLOSED,
    RESPONSE_COMPANION_FRAME_MALFORMED,
    RESPONSE_COMPANION_FRAME_IO_ERROR
} response_companion_frame_result;

typedef struct response_companion_frame {
    uint8_t opcode;
    unsigned char *payload;
    size_t payload_size;
} response_companion_frame;

typedef struct response_companion_reader {
    const unsigned char *data;
    size_t size;
    size_t offset;
} response_companion_reader;

typedef struct response_companion_response_input {
    msconnector_response response;
    msconnector_header *headers;
    char **names;
    char **values;
    char *http_version;
    size_t header_count;
} response_companion_response_input;

typedef struct response_companion_session_state {
    msconnector_response_companion_decision_storage decision_storage;
    msconnector_response_companion_backend_session session;
    msconnector_decision latest_decision;
    char latest_redirect[RESPONSE_COMPANION_MAX_REDIRECT + 1U];
    char latest_rule_id[RESPONSE_COMPANION_MAX_RULE_ID + 1U];
    char latest_reason[RESPONSE_COMPANION_MAX_DECISION_TEXT + 1U];
    char latest_log_message[RESPONSE_COMPANION_MAX_DECISION_TEXT + 1U];
    char latest_intervention_redirect[RESPONSE_COMPANION_MAX_REDIRECT + 1U];
    char latest_intervention_log_message[
        RESPONSE_COMPANION_MAX_DECISION_TEXT + 1U];
    int claimed;
    int response_headers;
    int response_eos;
    int committed;
    int has_decision;
    int outcome_recorded;
    size_t response_body_bytes;
} response_companion_session_state;

static void response_companion_reset_session_state(
    response_companion_session_state *state)
{
    if (state == NULL) {
        return;
    }
    memset(state, 0, sizeof(*state));
    state->session.decision_storage = &state->decision_storage;
}

struct msconnector_response_companion_transport_worker {
    msconnector_response_companion_transport *transport;
    int socket_fd;
    struct msconnector_response_companion_transport_worker *next;
};

static uint16_t response_companion_read_u16(const unsigned char *value)
{
    return (uint16_t)(((uint16_t)value[0] << 8U) | (uint16_t)value[1]);
}

static uint32_t response_companion_read_u32(const unsigned char *value)
{
    return ((uint32_t)value[0] << 24U) |
        ((uint32_t)value[1] << 16U) |
        ((uint32_t)value[2] << 8U) |
        (uint32_t)value[3];
}

static void response_companion_write_u16(unsigned char *value, uint16_t number)
{
    value[0] = (unsigned char)(number >> 8U);
    value[1] = (unsigned char)number;
}

static void response_companion_write_u32(unsigned char *value, uint32_t number)
{
    value[0] = (unsigned char)(number >> 24U);
    value[1] = (unsigned char)(number >> 16U);
    value[2] = (unsigned char)(number >> 8U);
    value[3] = (unsigned char)number;
}

static uint64_t response_companion_now_ms(void)
{
    struct timespec now;

    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0 || now.tv_sec < 0) {
        return 0U;
    }
    return (uint64_t)now.tv_sec * UINT64_C(1000) +
        (uint64_t)now.tv_nsec / UINT64_C(1000000);
}

static int response_companion_error(msconnector_error *error,
    msconnector_error_code code, const char *message)
{
    msconnector_error_set(error, code, message, "response_companion_transport");
    return 0;
}

static int response_companion_path_is_safe(const char *path)
{
    const char *cursor;

    if (path == NULL || path[0] != '/' || strlen(path) >=
        MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE) {
        return 0;
    }
    for (cursor = path; *cursor != '\0'; ++cursor) {
        if (*cursor == '\r' || *cursor == '\n') {
            return 0;
        }
    }
    cursor = path;
    while (*cursor != '\0') {
        const char *next = strchr(cursor + 1, '/');
        const size_t component_size = next == NULL ? strlen(cursor + 1) :
            (size_t)(next - (cursor + 1));
        if (component_size == 2U && cursor[1] == '.' && cursor[2] == '.') {
            return 0;
        }
        if (next == NULL) {
            break;
        }
        cursor = next;
    }
    return 1;
}

static int response_companion_private_parent_is_safe(const char *socket_path)
{
    char parent[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_SOCKET_SIZE];
    char canonical[PATH_MAX];
    char *separator;
    struct stat path_stat;
    size_t size;

    if (!response_companion_path_is_safe(socket_path)) {
        return 0;
    }
    size = strlen(socket_path);
    if (size == 0U || size >= sizeof(parent)) {
        return 0;
    }
    memcpy(parent, socket_path, size + 1U);
    separator = strrchr(parent, '/');
    if (separator == NULL || separator == parent) {
        return 0;
    }
    *separator = '\0';
    if (realpath(parent, canonical) == NULL || strcmp(parent, canonical) != 0 ||
        lstat(parent, &path_stat) != 0 || !S_ISDIR(path_stat.st_mode) ||
        path_stat.st_uid != geteuid() || (path_stat.st_mode & 0077U) != 0U ||
        (path_stat.st_mode & 0700U) != 0700U) {
        return 0;
    }
    return 1;
}

static int response_companion_set_nonblocking(int socket_fd)
{
    const int flags = fcntl(socket_fd, F_GETFL, 0);

    return flags >= 0 && fcntl(socket_fd, F_SETFL, flags | O_NONBLOCK) == 0;
}

static response_companion_io_result response_companion_wait_fd(int socket_fd, short events,
    uint64_t deadline_ms)
{
    struct pollfd descriptor;

    for (;;) {
        uint64_t now_ms = response_companion_now_ms();
        int timeout;
        int result;

        if (now_ms == 0U || now_ms >= deadline_ms) {
            return RESPONSE_COMPANION_IO_TIMEOUT;
        }
        timeout = deadline_ms - now_ms > (uint64_t)INT_MAX ? INT_MAX :
            (int)(deadline_ms - now_ms);
        memset(&descriptor, 0, sizeof(descriptor));
        descriptor.fd = socket_fd;
        descriptor.events = events;
        result = poll(&descriptor, 1U, timeout);
        if (result > 0) {
            if ((descriptor.revents & events) != 0) {
                return RESPONSE_COMPANION_IO_READY;
            }
            if ((descriptor.revents & POLLHUP) != 0) {
                return RESPONSE_COMPANION_IO_PEER_CLOSED;
            }
            return RESPONSE_COMPANION_IO_ERROR;
        }
        if (result == 0) {
            return RESPONSE_COMPANION_IO_TIMEOUT;
        }
        if (errno != EINTR) {
            return RESPONSE_COMPANION_IO_ERROR;
        }
    }
}

static response_companion_io_result response_companion_receive_all(int socket_fd,
    unsigned char *data,
    size_t size, uint64_t deadline_ms)
{
    size_t offset = 0U;

    while (offset < size) {
        ssize_t received;

        const response_companion_io_result ready = response_companion_wait_fd(
            socket_fd, POLLIN, deadline_ms);

        if (ready != RESPONSE_COMPANION_IO_READY) {
            return ready;
        }
        received = recv(socket_fd, data + offset, size - offset, 0);
        if (received > 0) {
            offset += (size_t)received;
            continue;
        }
        if (received < 0 && (errno == EINTR || errno == EAGAIN ||
            errno == EWOULDBLOCK)) {
            continue;
        }
        return received == 0 ? RESPONSE_COMPANION_IO_PEER_CLOSED :
            RESPONSE_COMPANION_IO_ERROR;
    }
    return RESPONSE_COMPANION_IO_READY;
}

static response_companion_frame_result response_companion_frame_from_io(
    response_companion_io_result result)
{
    if (result == RESPONSE_COMPANION_IO_TIMEOUT) {
        return RESPONSE_COMPANION_FRAME_TIMEOUT;
    }
    if (result == RESPONSE_COMPANION_IO_PEER_CLOSED) {
        return RESPONSE_COMPANION_FRAME_PEER_CLOSED;
    }
    return RESPONSE_COMPANION_FRAME_IO_ERROR;
}

static int response_companion_send_all(int socket_fd, const unsigned char *data,
    size_t size, uint64_t deadline_ms)
{
    size_t offset = 0U;

    while (offset < size) {
        ssize_t sent;

        if (response_companion_wait_fd(socket_fd, POLLOUT, deadline_ms) !=
            RESPONSE_COMPANION_IO_READY) {
            return 0;
        }
        sent = send(socket_fd, data + offset, size - offset, MSG_NOSIGNAL);
        if (sent > 0) {
            offset += (size_t)sent;
            continue;
        }
        if (sent < 0 && (errno == EINTR || errno == EAGAIN ||
            errno == EWOULDBLOCK)) {
            continue;
        }
        return 0;
    }
    return 1;
}

static uint64_t response_companion_deadline(
    const msconnector_response_companion_transport *transport)
{
    const uint64_t now_ms = response_companion_now_ms();

    if (transport == NULL || now_ms == 0U ||
        UINT64_MAX - now_ms < transport->config.operation_timeout_ms) {
        return 0U;
    }
    return now_ms + transport->config.operation_timeout_ms;
}

static void response_companion_frame_destroy(response_companion_frame *frame)
{
    if (frame != NULL) {
        free(frame->payload);
        memset(frame, 0, sizeof(*frame));
    }
}

static response_companion_frame_result response_companion_receive_frame(
    const msconnector_response_companion_transport *transport,
    int socket_fd, response_companion_frame *frame)
{
    unsigned char header[RESPONSE_COMPANION_FRAME_HEADER_SIZE];
    const uint64_t deadline_ms = response_companion_deadline(transport);
    response_companion_io_result io_result;
    uint32_t payload_size;

    if (frame == NULL || deadline_ms == 0U) {
        return RESPONSE_COMPANION_FRAME_IO_ERROR;
    }
    memset(frame, 0, sizeof(*frame));
    io_result = response_companion_receive_all(socket_fd, header, sizeof(header),
        deadline_ms);
    if (io_result != RESPONSE_COMPANION_IO_READY) {
        return response_companion_frame_from_io(io_result);
    }
    if (memcmp(header, RESPONSE_COMPANION_MAGIC, 4U) != 0 ||
        header[4] != RESPONSE_COMPANION_VERSION || header[6] != 0U ||
        header[7] != 0U) {
        return RESPONSE_COMPANION_FRAME_MALFORMED;
    }
    payload_size = response_companion_read_u32(header + 8U);
    if (payload_size > response_companion_max_payload_for_opcode(header[5])) {
        return RESPONSE_COMPANION_FRAME_MALFORMED;
    }
    if (payload_size > 0U) {
        frame->payload = malloc(payload_size);
        if (frame->payload == NULL) {
            return RESPONSE_COMPANION_FRAME_IO_ERROR;
        }
        io_result = response_companion_receive_all(socket_fd, frame->payload,
            payload_size, deadline_ms);
        if (io_result != RESPONSE_COMPANION_IO_READY) {
            response_companion_frame_destroy(frame);
            return response_companion_frame_from_io(io_result);
        }
    }
    frame->opcode = header[5];
    frame->payload_size = payload_size;
    return RESPONSE_COMPANION_FRAME_OK;
}

static int response_companion_send_frame(
    const msconnector_response_companion_transport *transport,
    int socket_fd, uint8_t opcode, const unsigned char *payload,
    size_t payload_size)
{
    unsigned char header[RESPONSE_COMPANION_FRAME_HEADER_SIZE];
    const uint64_t deadline_ms = response_companion_deadline(transport);

    if (deadline_ms == 0U || payload_size >
        response_companion_max_payload_for_opcode(opcode) ||
        (payload_size > 0U && payload == NULL)) {
        return 0;
    }
    memset(header, 0, sizeof(header));
    memcpy(header, RESPONSE_COMPANION_MAGIC, 4U);
    header[4] = RESPONSE_COMPANION_VERSION;
    header[5] = opcode;
    response_companion_write_u32(header + 8U, (uint32_t)payload_size);
    return response_companion_send_all(socket_fd, header, sizeof(header), deadline_ms) &&
        (payload_size == 0U || response_companion_send_all(socket_fd, payload,
            payload_size, deadline_ms));
}

static size_t response_companion_bounded_text_size(const char *value,
    size_t maximum)
{
    size_t size = 0U;

    if (value == NULL) {
        return 0U;
    }
    while (size < maximum && value[size] != '\0') {
        ++size;
    }
    return size;
}

static int response_companion_copy_decision_text(char *destination,
    size_t capacity, const char *source)
{
    const size_t size = response_companion_bounded_text_size(source, capacity);

    if (destination == NULL || capacity == 0U || size >= capacity) {
        return 0;
    }
    if (size > 0U) {
        memcpy(destination, source, size);
    }
    destination[size] = '\0';
    return 1;
}

/* A backend decision's pointer fields are borrowed. MRC1 can need the latest
 * P3/P4 decision after that callback returns, so retain a bounded value copy
 * at the wire/session boundary rather than relying on a backend lifetime. */
static int response_companion_store_latest_decision(
    response_companion_session_state *state, const msconnector_decision *source,
    msconnector_error *error)
{
    msconnector_decision copy;

    if (state == NULL || source == NULL ||
        !response_companion_copy_decision_text(state->latest_redirect,
            sizeof(state->latest_redirect), source->redirect_url) ||
        !response_companion_copy_decision_text(state->latest_rule_id,
            sizeof(state->latest_rule_id), source->rule_id) ||
        !response_companion_copy_decision_text(state->latest_reason,
            sizeof(state->latest_reason), source->reason) ||
        !response_companion_copy_decision_text(state->latest_log_message,
            sizeof(state->latest_log_message), source->log_message) ||
        !response_companion_copy_decision_text(state->latest_intervention_redirect,
            sizeof(state->latest_intervention_redirect),
            source->intervention.redirect_url) ||
        !response_companion_copy_decision_text(state->latest_intervention_log_message,
            sizeof(state->latest_intervention_log_message),
            source->intervention.log_message)) {
        return response_companion_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response companion backend decision metadata is invalid");
    }
    copy = *source;
    copy.redirect_url = source->redirect_url == NULL ? NULL : state->latest_redirect;
    copy.rule_id = source->rule_id == NULL ? NULL : state->latest_rule_id;
    copy.reason = source->reason == NULL ? NULL : state->latest_reason;
    copy.log_message = source->log_message == NULL ? NULL : state->latest_log_message;
    copy.intervention.redirect_url = source->intervention.redirect_url == NULL ? NULL :
        state->latest_intervention_redirect;
    copy.intervention.log_message = source->intervention.log_message == NULL ? NULL :
        state->latest_intervention_log_message;
    state->latest_decision = copy;
    return 1;
}

static int response_companion_send_result(
    const msconnector_response_companion_transport *transport,
    int socket_fd, uint8_t request_opcode, int success,
    const msconnector_decision *decision, const msconnector_error *error)
{
    unsigned char payload[12U + RESPONSE_COMPANION_MAX_REDIRECT +
        RESPONSE_COMPANION_MAX_RULE_ID];
    const char *redirect = decision == NULL ? NULL : decision->redirect_url;
    const char *rule_id = decision == NULL ? NULL : decision->rule_id;
    size_t redirect_size = response_companion_bounded_text_size(redirect,
        RESPONSE_COMPANION_MAX_REDIRECT + 1U);
    size_t rule_size = response_companion_bounded_text_size(rule_id,
        RESPONSE_COMPANION_MAX_RULE_ID + 1U);
    msconnector_decision_kind kind = decision == NULL ?
        MSCONNECTOR_DECISION_KIND_ERROR : decision->kind;
    int status = decision == NULL ? 0 : msconnector_decision_http_status(decision);
    const msconnector_error_code error_code = error == NULL ?
        MSCONNECTOR_ERROR_NONE : error->code;
    size_t offset = 12U;

    /* A missing optional string is encoded as an empty field, never as a
     * non-zero length with a NULL source pointer. */
    if (redirect == NULL) {
        redirect_size = 0U;
    }
    if (rule_id == NULL) {
        rule_size = 0U;
    }
    if (redirect_size > RESPONSE_COMPANION_MAX_REDIRECT ||
        rule_size > RESPONSE_COMPANION_MAX_RULE_ID || kind >
        MSCONNECTOR_DECISION_KIND_UNSUPPORTED || status < 0 || status > UINT16_MAX) {
        redirect_size = 0U;
        rule_size = 0U;
        kind = MSCONNECTOR_DECISION_KIND_ERROR;
        status = 0;
    }
    memset(payload, 0, sizeof(payload));
    payload[0] = request_opcode;
    payload[1] = success ? 0U : 1U;
    payload[2] = (unsigned char)kind;
    response_companion_write_u16(payload + 4U, (uint16_t)status);
    response_companion_write_u16(payload + 6U, (uint16_t)error_code);
    response_companion_write_u16(payload + 8U, (uint16_t)redirect_size);
    response_companion_write_u16(payload + 10U, (uint16_t)rule_size);
    if (redirect_size > 0U && redirect != NULL) {
        memcpy(payload + offset, redirect, redirect_size);
        offset += redirect_size;
    }
    if (rule_size > 0U && rule_id != NULL) {
        memcpy(payload + offset, rule_id, rule_size);
        offset += rule_size;
    }
    return response_companion_send_frame(transport, socket_fd,
        RESPONSE_COMPANION_RESULT, payload, offset);
}

static int response_companion_reader_u16(response_companion_reader *reader,
    uint16_t *out)
{
    if (reader == NULL || out == NULL || reader->offset > reader->size ||
        reader->size - reader->offset < 2U) {
        return 0;
    }
    *out = response_companion_read_u16(reader->data + reader->offset);
    reader->offset += 2U;
    return 1;
}

static int response_companion_valid_text(const unsigned char *value, size_t size,
    int header_name)
{
    if (value == NULL || size == 0U || memchr(value, '\0', size) != NULL) {
        return 0;
    }
    for (size_t index = 0U; index < size; ++index) {
        const unsigned char character = value[index];
        if (character < 32U || character == 127U || character == '\r' ||
            character == '\n' || (header_name && character == ':')) {
            return 0;
        }
    }
    return 1;
}

static int response_companion_valid_header_name(const unsigned char *value,
    size_t size)
{
    if (size == sizeof(":status") - 1U &&
        memcmp(value, ":status", sizeof(":status") - 1U) == 0) {
        return 1;
    }
    return response_companion_valid_text(value, size, 1);
}

static int response_companion_reader_text(response_companion_reader *reader,
    size_t maximum, int required, int header_name, char **out, size_t *out_size)
{
    uint16_t size_u16;
    char *copy;

    if (reader == NULL || out == NULL || out_size == NULL ||
        !response_companion_reader_u16(reader, &size_u16) || size_u16 > maximum ||
        reader->offset > reader->size || reader->size - reader->offset < size_u16 ||
        (required && size_u16 == 0U) || (size_u16 > 0U &&
            (header_name ? !response_companion_valid_header_name(
                reader->data + reader->offset, size_u16) :
                !response_companion_valid_text(reader->data + reader->offset,
                    size_u16, 0)))) {
        return 0;
    }
    copy = calloc((size_t)size_u16 + 1U, 1U);
    if (copy == NULL) {
        return 0;
    }
    if (size_u16 > 0U) {
        memcpy(copy, reader->data + reader->offset, size_u16);
    }
    reader->offset += size_u16;
    *out = copy;
    *out_size = size_u16;
    return 1;
}

static int response_companion_status_text_matches(const char *value,
    size_t value_size, uint16_t status)
{
    char expected[4];
    const int expected_size = snprintf(expected, sizeof(expected), "%u",
        (unsigned int)status);

    return expected_size > 0 && (size_t)expected_size == value_size &&
        memcmp(value, expected, value_size) == 0;
}

static void response_companion_response_input_destroy(
    response_companion_response_input *input)
{
    if (input == NULL) {
        return;
    }
    for (size_t index = 0U; index < input->header_count; ++index) {
        free(input->names == NULL ? NULL : input->names[index]);
        free(input->values == NULL ? NULL : input->values[index]);
    }
    free(input->headers);
    free(input->names);
    free(input->values);
    free(input->http_version);
    memset(input, 0, sizeof(*input));
}

static int response_companion_parse_response_headers(
    const msconnector_response_companion_transport *transport,
    const response_companion_frame *frame,
    response_companion_response_input *input,
    msconnector_error *error)
{
    response_companion_reader reader;
    uint16_t status;
    uint16_t header_count;
    size_t output_header_count = 0U;
    int status_pseudoheader_seen = 0;
    size_t header_bytes = 0U;
    size_t http_version_size;

    if (transport == NULL || frame == NULL || input == NULL ||
        frame->opcode != RESPONSE_COMPANION_RESPONSE_HEADERS) {
        return response_companion_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion expected response headers");
    }
    memset(input, 0, sizeof(*input));
    memset(&reader, 0, sizeof(reader));
    reader.data = frame->payload;
    reader.size = frame->payload_size;
    if (!response_companion_reader_u16(&reader, &status) || status < 100U ||
        status > 999U || !response_companion_reader_text(&reader,
            RESPONSE_COMPANION_MAX_HTTP_VERSION, 1, 0, &input->http_version,
            &http_version_size) ||
        !response_companion_reader_u16(&reader, &header_count) ||
        header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
        header_count > transport->config.max_header_count) {
        response_companion_response_input_destroy(input);
        return response_companion_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "response companion response headers are invalid");
    }
    /* reader_text returns a size through its output argument. Reuse the local
     * counter only for this one field, then reset it for header accounting. */
    header_bytes = 0U;
    if (header_count > 0U) {
        input->headers = calloc(header_count, sizeof(*input->headers));
        input->names = calloc(header_count, sizeof(*input->names));
        input->values = calloc(header_count, sizeof(*input->values));
        if (input->headers == NULL || input->names == NULL || input->values == NULL) {
            response_companion_response_input_destroy(input);
            return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                "response companion header allocation failed");
        }
    }
    for (size_t index = 0U; index < header_count; ++index) {
        size_t name_size;
        size_t value_size;
        char *name = NULL;
        char *value = NULL;
        if (!response_companion_reader_text(&reader,
                RESPONSE_COMPANION_MAX_HEADER_NAME, 1, 1,
                &name, &name_size) ||
            !response_companion_reader_text(&reader,
                RESPONSE_COMPANION_MAX_HEADER_VALUE, 0, 0,
                &value, &value_size) ||
            header_bytes > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES ||
            name_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - header_bytes ||
            value_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - header_bytes - name_size ||
            header_bytes > transport->config.max_header_bytes ||
            name_size > transport->config.max_header_bytes - header_bytes ||
            value_size > transport->config.max_header_bytes - header_bytes - name_size) {
            free(name);
            free(value);
            response_companion_response_input_destroy(input);
            return response_companion_error(error, MSCONNECTOR_ERROR_HEADER_TOO_LARGE,
                "response companion response headers exceed their limit");
        }
        header_bytes += name_size + value_size;
        if (name_size == sizeof(":status") - 1U &&
            memcmp(name, ":status", sizeof(":status") - 1U) == 0) {
            if (status_pseudoheader_seen ||
                !response_companion_status_text_matches(value, value_size,
                    status)) {
                free(name);
                free(value);
                response_companion_response_input_destroy(input);
                return response_companion_error(error, MSCONNECTOR_ERROR_PROTOCOL,
                    "response companion response status pseudoheader is invalid");
            }
            status_pseudoheader_seen = 1;
            free(name);
            free(value);
            continue;
        }
        input->names[output_header_count] = name;
        input->values[output_header_count] = value;
        input->headers[output_header_count].name = name;
        input->headers[output_header_count].name_size = name_size;
        input->headers[output_header_count].value = value;
        input->headers[output_header_count].value_size = value_size;
        output_header_count++;
        input->header_count = output_header_count;
    }
    if (reader.offset != reader.size) {
        response_companion_response_input_destroy(input);
        return response_companion_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "response companion response header framing has trailing data");
    }
    input->header_count = output_header_count;
    input->response.status = status;
    input->response.http_version = input->http_version;
    input->response.headers = input->headers;
    input->response.header_count = input->header_count;
    input->response.body.data = NULL;
    input->response.body.size = 0U;
    if (!msconnector_response_validate(&input->response)) {
        response_companion_response_input_destroy(input);
        return response_companion_error(error, MSCONNECTOR_ERROR_PROTOCOL,
            "response companion response metadata is invalid");
    }
    return 1;
}

static int response_companion_parse_claim(const response_companion_frame *frame,
    char handle[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE])
{
    if (frame == NULL || handle == NULL || frame->opcode != RESPONSE_COMPANION_CLAIM ||
        frame->payload_size != MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE - 1U ||
        frame->payload == NULL) {
        return 0;
    }
    for (size_t index = 0U;
         index < MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE - 1U;
         ++index) {
        const unsigned char character = frame->payload[index];
        if (!((character >= (unsigned char)'0' && character <= (unsigned char)'9') ||
              (character >= (unsigned char)'a' && character <= (unsigned char)'f'))) {
            return 0;
        }
        handle[index] = (char)character;
    }
    handle[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE - 1U] = '\0';
    return 1;
}

static int response_companion_parse_commit(const response_companion_frame *frame,
    int *headers_sent, int *body_started)
{
    if (frame == NULL || headers_sent == NULL || body_started == NULL ||
        frame->opcode != RESPONSE_COMPANION_COMMIT || frame->payload_size != 2U ||
        frame->payload == NULL || frame->payload[0] > 1U || frame->payload[1] > 1U) {
        return 0;
    }
    *headers_sent = frame->payload[0] != 0U;
    *body_started = frame->payload[1] != 0U;
    return *headers_sent;
}

static int response_companion_parse_cancel(const response_companion_frame *frame,
    msconnector_response_companion_cancel_cause *cause)
{
    if (frame == NULL || cause == NULL || frame->opcode != RESPONSE_COMPANION_CANCEL ||
        frame->payload_size != 1U || frame->payload == NULL) {
        return 0;
    }
    switch (frame->payload[0]) {
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_PROTOCOL_ERROR:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_TIMEOUT:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_UNAVAILABLE:
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_INVALID_ENGINE_RESPONSE:
        *cause = (msconnector_response_companion_cancel_cause)frame->payload[0];
        return 1;
    default:
        return 0;
    }
}

static int response_companion_cancel_error_class(
    msconnector_response_companion_cancel_cause cause,
    msconnector_transaction_error_class *error_class)
{
    if (error_class == NULL) {
        return 0;
    }
    switch (cause) {
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CONNECTOR_ERROR:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_PROTOCOL_ERROR:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_TIMEOUT:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_ENGINE_UNAVAILABLE:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE;
        return 1;
    case MSCONNECTOR_RESPONSE_COMPANION_CANCEL_INVALID_ENGINE_RESPONSE:
        *error_class = MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE;
        return 1;
    default:
        return 0;
    }
}

static int response_companion_parse_outcome(const response_companion_frame *frame,
    msconnector_decision_action *actual_action, int *visible_status,
    int *connection_aborted)
{
    if (frame == NULL || actual_action == NULL || visible_status == NULL ||
        connection_aborted == NULL || frame->opcode != RESPONSE_COMPANION_OUTCOME ||
        frame->payload_size != 4U || frame->payload == NULL ||
        frame->payload[0] > MSCONNECTOR_DECISION_ACTION_RATE_LIMIT ||
        (frame->payload[1] & ~1U) != 0U) {
        return 0;
    }
    *actual_action = (msconnector_decision_action)frame->payload[0];
    *connection_aborted = (frame->payload[1] & 1U) != 0U;
    *visible_status = response_companion_read_u16(frame->payload + 2U);
    return 1;
}

static const char *response_companion_transport_result(
    msconnector_decision_action action, int connection_aborted)
{
    if (action == MSCONNECTOR_DECISION_ACTION_STREAM_RESET) {
        return "stream_reset";
    }
    if (connection_aborted) {
        return "connection_aborted";
    }
    if (action == MSCONNECTOR_DECISION_ACTION_LOG_ONLY) {
        return "log_only";
    }
    return "http_status";
}

static msconnector_transaction_error_class
response_companion_error_class_from_error(const msconnector_error *error)
{
    const msconnector_error_code code = error == NULL ? MSCONNECTOR_ERROR_INTERNAL :
        error->code;

    switch (code) {
    case MSCONNECTOR_ERROR_BODY_TOO_LARGE:
        return MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT;
    case MSCONNECTOR_ERROR_EVENT_TOO_LARGE:
        return MSCONNECTOR_TRANSACTION_ERROR_EVENT_LIMIT;
    case MSCONNECTOR_ERROR_TIMEOUT:
        return MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT;
    case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE:
        return MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE;
    case MSCONNECTOR_ERROR_CORRELATION_MISSING:
        return MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISSING;
    case MSCONNECTOR_ERROR_CORRELATION_EXPIRED:
        return MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED;
    case MSCONNECTOR_ERROR_CORRELATION_MISMATCH:
        return MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISMATCH;
    case MSCONNECTOR_ERROR_PHASE_SEQUENCE:
        return MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE;
    case MSCONNECTOR_ERROR_PROTOCOL:
    case MSCONNECTOR_ERROR_HEADER_TOO_LARGE:
        return MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
    default:
        return MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
    }
}

static int response_companion_peer_is_expected(
    const msconnector_response_companion_transport *transport, int socket_fd)
{
#if defined(__linux__)
    struct ucred credentials;
    socklen_t credentials_size = sizeof(credentials);

    if (transport == NULL || socket_fd < 0) {
        return 0;
    }
    memset(&credentials, 0, sizeof(credentials));
    return getsockopt(socket_fd, SOL_SOCKET, SO_PEERCRED, &credentials,
        &credentials_size) == 0 && credentials_size == sizeof(credentials) &&
        credentials.uid == transport->config.expected_uid &&
        credentials.gid == transport->config.expected_gid;
#else
    (void)transport;
    (void)socket_fd;
    return 0;
#endif
}

static int response_companion_self_probe(int listener_fd, const char *socket_path,
    uid_t expected_uid, gid_t expected_gid)
{
#if defined(__linux__)
    struct sockaddr_un address;
    struct ucred credentials;
    socklen_t credentials_size = sizeof(credentials);
    int client_fd;
    int accepted_fd;
    size_t path_size;
    int result = 0;

    if (listener_fd < 0 || socket_path == NULL ||
        !response_companion_path_is_safe(socket_path)) {
        return 0;
    }
    path_size = strlen(socket_path);
    client_fd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (client_fd < 0) {
        return 0;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, socket_path, path_size + 1U);
    if (connect(client_fd, (const struct sockaddr *)&address, sizeof(address)) != 0) {
        (void)close(client_fd);
        return 0;
    }
    accepted_fd = accept4(listener_fd, NULL, NULL, SOCK_CLOEXEC);
    if (accepted_fd >= 0) {
        memset(&credentials, 0, sizeof(credentials));
        result = getsockopt(accepted_fd, SOL_SOCKET, SO_PEERCRED, &credentials,
            &credentials_size) == 0 && credentials_size == sizeof(credentials) &&
            credentials.pid == getpid() && credentials.uid == expected_uid &&
            credentials.gid == expected_gid;
        (void)close(accepted_fd);
    }
    (void)close(client_fd);
    return result;
#else
    (void)listener_fd;
    (void)socket_path;
    (void)expected_uid;
    (void)expected_gid;
    return 0;
#endif
}

static int response_companion_capture_socket_identity(
    msconnector_response_companion_transport *transport, int listener_fd)
{
    struct stat path_stat;

    if (transport == NULL || lstat(transport->config.socket_path, &path_stat) != 0 ||
        !S_ISSOCK(path_stat.st_mode) || path_stat.st_uid != transport->config.expected_uid ||
        (path_stat.st_mode & 0077U) != 0U) {
        return 0;
    }
    /* Record the exact inode before probing it.  If the probe fails, the
     * caller can still unlink only this socket rather than leaving a stale
     * path or deleting a replacement. */
    transport->listener.socket_device = (uint64_t)path_stat.st_dev;
    transport->listener.socket_inode = (uint64_t)path_stat.st_ino;
    transport->listener.socket_owner = path_stat.st_uid;
    transport->listener.identity_valid = 1;
    return response_companion_self_probe(listener_fd, transport->config.socket_path,
        transport->config.expected_uid, transport->config.expected_gid);
}

static int response_companion_remove_owned_socket(
    const msconnector_response_companion_transport *transport);

static int response_companion_create_listener(
    msconnector_response_companion_transport *transport)
{
    struct sockaddr_un address;
    struct stat existing;
    int listener_fd;
    size_t path_size;

    if (transport == NULL || !response_companion_private_parent_is_safe(
            transport->config.socket_path) || lstat(transport->config.socket_path, &existing) == 0 ||
        errno != ENOENT) {
        return -1;
    }
    path_size = strlen(transport->config.socket_path);
    if (path_size == 0U || path_size >= sizeof(address.sun_path)) {
        return -1;
    }
    listener_fd = socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (listener_fd < 0) {
        return -1;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, transport->config.socket_path, path_size + 1U);
    if (bind(listener_fd, (const struct sockaddr *)&address, sizeof(address)) != 0 ||
        chmod(transport->config.socket_path, 0600) != 0 ||
        listen(listener_fd, RESPONSE_COMPANION_LISTEN_BACKLOG) != 0 ||
        !response_companion_capture_socket_identity(transport, listener_fd) ||
        !response_companion_set_nonblocking(listener_fd)) {
        (void)close(listener_fd);
        (void)response_companion_remove_owned_socket(transport);
        transport->listener.identity_valid = 0;
        return -1;
    }
    return listener_fd;
}

static int response_companion_remove_owned_socket(
    const msconnector_response_companion_transport *transport)
{
    struct stat path_stat;

    if (transport == NULL || !transport->listener.identity_valid) {
        return 1;
    }
    if (lstat(transport->config.socket_path, &path_stat) != 0) {
        return errno == ENOENT;
    }
    if (!S_ISSOCK(path_stat.st_mode) || path_stat.st_uid != transport->listener.socket_owner ||
        (uint64_t)path_stat.st_dev != transport->listener.socket_device ||
        (uint64_t)path_stat.st_ino != transport->listener.socket_inode) {
        return 0;
    }
    return unlink(transport->config.socket_path) == 0 || errno == ENOENT;
}

static msconnector_runtime_response_companion_session *
response_companion_runtime_backend_session(
    const msconnector_response_companion_backend_session *session)
{
    return session == NULL ? NULL :
        (msconnector_runtime_response_companion_session *)session->opaque;
}

static int response_companion_runtime_backend_claim(void *context,
    const char *handle, msconnector_response_companion_backend_session *session,
    msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session;

    if (context == NULL || handle == NULL || session == NULL || session->opaque != NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion Runtime backend claim is invalid");
    }
    runtime_session = calloc(1U, sizeof(*runtime_session));
    if (runtime_session == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion Runtime backend session allocation failed");
    }
    if (!msconnector_runtime_response_companion_claim_handle(
            (msconnector_runtime_response_companion_registry *)context, handle,
            runtime_session, error)) {
        free(runtime_session);
        return 0;
    }
    session->opaque = runtime_session;
    return 1;
}

static int response_companion_runtime_backend_process_response_headers(
    void *context, const msconnector_response_companion_backend_session *session,
    const msconnector_response *response, msconnector_decision *decision,
    msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);

    (void)context;
    return runtime_session != NULL &&
        msconnector_runtime_response_companion_session_process_response_headers(
            runtime_session, response, decision, error);
}

static int response_companion_runtime_backend_append_response_body_chunk(
    void *context, const msconnector_response_companion_backend_session *session,
    const unsigned char *data, size_t size, msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);

    (void)context;
    return runtime_session != NULL &&
        msconnector_runtime_response_companion_session_append_response_body_chunk(
            runtime_session, data, size, error);
}

static int response_companion_runtime_backend_finish_response_body(void *context,
    const msconnector_response_companion_backend_session *session,
    msconnector_decision *decision, msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);

    (void)context;
    return runtime_session != NULL &&
        msconnector_runtime_response_companion_session_finish_response_body(
            runtime_session, decision, error);
}

static int response_companion_runtime_backend_set_response_commit_state(
    void *context, const msconnector_response_companion_backend_session *session,
    int headers_sent, int body_started, msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);

    (void)context;
    return runtime_session != NULL &&
        msconnector_runtime_response_companion_session_set_response_commit_state(
            runtime_session, headers_sent, body_started, error);
}

static int response_companion_runtime_backend_record_host_action(void *context,
    const msconnector_response_companion_backend_session *session,
    const msconnector_response_companion_host_action *action,
    msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);

    (void)context;
    return runtime_session != NULL && action != NULL &&
        msconnector_runtime_response_companion_session_record_host_action(
            runtime_session, action->decision, action->actual_action,
            action->visible_http_status, action->transport_result,
            action->connection_aborted, error);
}

static int response_companion_runtime_backend_cancel(void *context,
    msconnector_response_companion_backend_session *session,
    int upstream_disconnect, msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);
    int result;

    (void)context;
    if (runtime_session == NULL) {
        return 0;
    }
    result = msconnector_runtime_response_companion_session_cancel(runtime_session,
        upstream_disconnect, error);
    if (!runtime_session->active) {
        free(runtime_session);
        session->opaque = NULL;
    }
    return result;
}

static int response_companion_runtime_backend_release(void *context,
    msconnector_response_companion_backend_session *session,
    msconnector_error *error)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);
    int result;

    (void)context;
    if (runtime_session == NULL) {
        return 0;
    }
    result = msconnector_runtime_response_companion_session_release(runtime_session,
        error);
    if (!runtime_session->active) {
        free(runtime_session);
        session->opaque = NULL;
    }
    return result;
}

static void response_companion_runtime_backend_fail(void *context,
    msconnector_response_companion_backend_session *session,
    msconnector_transaction_error_class error_class)
{
    msconnector_runtime_response_companion_session *runtime_session =
        response_companion_runtime_backend_session(session);
    msconnector_error ignored;

    (void)context;
    if (runtime_session == NULL) {
        return;
    }
    msconnector_error_init(&ignored);
    (void)msconnector_runtime_response_companion_session_fail(runtime_session,
        error_class, &ignored);
    if (!runtime_session->active) {
        free(runtime_session);
        session->opaque = NULL;
    }
}

static void response_companion_runtime_backend_expire(void *context,
    uint64_t now_ms)
{
    if (context != NULL) {
        (void)msconnector_runtime_response_companion_expire(
            (msconnector_runtime_response_companion_registry *)context, now_ms);
    }
}

static const msconnector_response_companion_backend
response_companion_runtime_backend = {
    .context = NULL,
    .claim = response_companion_runtime_backend_claim,
    .process_response_headers =
        response_companion_runtime_backend_process_response_headers,
    .append_response_body_chunk =
        response_companion_runtime_backend_append_response_body_chunk,
    .finish_response_body = response_companion_runtime_backend_finish_response_body,
    .set_response_commit_state =
        response_companion_runtime_backend_set_response_commit_state,
    .record_host_action = response_companion_runtime_backend_record_host_action,
    .cancel = response_companion_runtime_backend_cancel,
    .release = response_companion_runtime_backend_release,
    .fail = response_companion_runtime_backend_fail,
    .expire = response_companion_runtime_backend_expire
};

static void response_companion_backend_fault(
    msconnector_response_companion_transport *transport)
{
    if (transport != NULL) {
        atomic_store_explicit(&transport->synchronization.backend_faulted, 1, memory_order_release);
    }
}

static int response_companion_backend_claim(
    msconnector_response_companion_transport *transport, const char *handle,
    msconnector_response_companion_backend_session *session,
    msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL || atomic_load_explicit(&transport->synchronization.backend_faulted,
            memory_order_acquire)) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend is faulted");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    /* The initial check only avoids taking the lock for an already-faulted
     * backend. A concurrent terminal callback can quarantine the backend
     * while this claimant waits for the generic callback lock, so re-check
     * the acquire-side state before invoking the foreign callback. */
    if (atomic_load_explicit(&transport->synchronization.backend_faulted,
            memory_order_acquire)) {
        if (backend_locked) {
            (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
        }
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend is faulted");
    }
    result = transport->config.backend.claim(transport->config.backend.context, handle, session,
        error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_process_response_headers(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend_session *session,
    const msconnector_response *response, msconnector_decision *decision,
    msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.process_response_headers(transport->config.backend.context,
        session, response, decision, error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_append_response_body_chunk(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend_session *session,
    const unsigned char *data, size_t size, msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.append_response_body_chunk(
        transport->config.backend.context, session, data, size, error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_finish_response_body(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend_session *session,
    msconnector_decision *decision, msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.finish_response_body(transport->config.backend.context,
        session, decision, error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_set_response_commit_state(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend_session *session, int headers_sent,
    int body_started, msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.set_response_commit_state(
        transport->config.backend.context, session, headers_sent, body_started, error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_record_host_action(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend_session *session,
    const msconnector_response_companion_host_action *action,
    msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL || session == NULL || action == NULL) {
        return 0;
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.record_host_action(transport->config.backend.context,
        session, action, error);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

/* The caller holds the generic backend lock unless this backend explicitly
 * opted into parallel callbacks and supplies its own serialization. Keeping
 * the compensating fail callback in that same critical section makes a
 * successful-but-retained terminal session impossible to race with another
 * generic backend callback. */
static int response_companion_backend_require_terminal_release_locked(
    msconnector_response_companion_transport *transport,
    msconnector_response_companion_backend_session *session,
    msconnector_error *error)
{
    if (session == NULL || session->opaque == NULL) {
        return 1;
    }
    response_companion_backend_fault(transport);
    if (transport != NULL && transport->config.backend.fail != NULL) {
        transport->config.backend.fail(transport->config.backend.context, session,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
    }
    session->opaque = NULL;
    return response_companion_error(error, MSCONNECTOR_ERROR_INTERNAL,
        "response companion backend retained a terminal session");
}

static int response_companion_backend_cancel(
    msconnector_response_companion_transport *transport,
    msconnector_response_companion_backend_session *session,
    int upstream_disconnect, msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.cancel(transport->config.backend.context, session,
        upstream_disconnect, error);
    if (result && !response_companion_backend_require_terminal_release_locked(
            transport, session, error)) {
        result = 0;
    }
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static int response_companion_backend_release(
    msconnector_response_companion_transport *transport,
    msconnector_response_companion_backend_session *session,
    msconnector_error *error)
{
    int result;
    int backend_locked;

    if (transport == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization failed");
    }
    result = transport->config.backend.release(transport->config.backend.context, session, error);
    if (result && !response_companion_backend_require_terminal_release_locked(
            transport, session, error)) {
        result = 0;
    }
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
    return result;
}

static void response_companion_backend_fail(
    msconnector_response_companion_transport *transport,
    msconnector_response_companion_backend_session *session,
    msconnector_transaction_error_class error_class)
{
    int backend_locked;

    if (transport == NULL || session == NULL || session->opaque == NULL) {
        return;
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        response_companion_backend_fault(transport);
        session->opaque = NULL;
        return;
    }
    transport->config.backend.fail(transport->config.backend.context, session, error_class);
    if (session->opaque != NULL) {
        /* There is no safe way for the generic transport to free a foreign
         * native session. Quarantine the backend so it cannot service another
         * claim, then invalidate the borrowed opaque capability. Keep both
         * operations inside the callback critical section so a waiting CLAIM
         * cannot pass the fault check before quarantine becomes visible. */
        response_companion_backend_fault(transport);
        session->opaque = NULL;
    }
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
}

static void response_companion_backend_expire(
    msconnector_response_companion_transport *transport, uint64_t now_ms)
{
    int backend_locked;

    if (transport == NULL || transport->config.backend.expire == NULL) {
        return;
    }
    backend_locked = !transport->config.backend.allow_parallel_callbacks;
    if (backend_locked && pthread_mutex_lock(&transport->synchronization.backend_lock) != 0) {
        return;
    }
    transport->config.backend.expire(transport->config.backend.context, now_ms);
    if (backend_locked) {
        (void)pthread_mutex_unlock(&transport->synchronization.backend_lock);
    }
}

static void response_companion_abort_session(
    msconnector_response_companion_transport *transport,
    response_companion_session_state *state,
    msconnector_transaction_error_class error_class)
{
    msconnector_error ignored;
    int cancel_result;

    if (transport == NULL || state == NULL || state->session.opaque == NULL) {
        return;
    }
    if (error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        error_class = MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
    }
    if (error_class == MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL ||
        error_class == MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT) {
        msconnector_error_init(&ignored);
        cancel_result = response_companion_backend_cancel(transport, &state->session,
            error_class == MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT,
            &ignored);
        if (state->session.opaque != NULL) {
            /* A backend that could not cancel must still make the session terminal
             * before the worker forgets it. Its fail callback owns any native
             * cleanup or owner-thread dispatch required for that transition. */
            if (cancel_result) {
                response_companion_backend_fault(transport);
            }
            response_companion_backend_fail(transport, &state->session, error_class);
        }
    } else {
        response_companion_backend_fail(transport, &state->session, error_class);
    }
    /* Backends own the native release, but the transport must never retain a
     * stale opaque capability after any terminal cleanup callback. */
    state->session.opaque = NULL;
    msconnector_secure_zero(&state->latest_decision, sizeof(state->latest_decision));
    state->has_decision = 0;
}

static void response_companion_fail_session(
    msconnector_response_companion_transport *transport,
    response_companion_session_state *state,
    msconnector_transaction_error_class error_class)
{
    if (transport == NULL || state == NULL || state->session.opaque == NULL) {
        return;
    }
    response_companion_backend_fail(transport, &state->session, error_class);
    msconnector_secure_zero(&state->latest_decision, sizeof(state->latest_decision));
    state->has_decision = 0;
}

static int response_companion_handle_claim(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    char handle[MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_HANDLE_SIZE];
    msconnector_error error;
    int result;

    msconnector_secure_zero(handle, sizeof(handle));
    msconnector_error_init(&error);
    state->session.decision_storage = &state->decision_storage;
    result = response_companion_parse_claim(frame, handle) &&
        response_companion_backend_claim(worker->transport, handle, &state->session,
            &error);
    msconnector_secure_zero(handle, sizeof(handle));
    if (!result && state->session.opaque != NULL) {
        /* A backend must not leave a partially claimed native session live
         * after a failed CLAIM.  Give it one terminal cleanup callback and
         * then invalidate the transport's borrowed capability. */
        response_companion_backend_fail(worker->transport, &state->session,
            MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL);
    }
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PROTOCOL,
            "response companion capability framing is invalid",
            "response_companion_transport");
    }
    if (result) {
        msconnector_decision_set_allow(&state->latest_decision);
        state->claimed = 1;
        state->has_decision = 1;
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, result ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_headers(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    response_companion_response_input input;
    msconnector_decision decision;
    msconnector_error error;
    int result;

    memset(&input, 0, sizeof(input));
    msconnector_decision_init(&decision);
    msconnector_error_init(&error);
    result = !state->response_headers && response_companion_parse_response_headers(
        worker->transport, frame, &input, &error) &&
        response_companion_backend_process_response_headers(worker->transport,
            &state->session, &input.response, &decision, &error) &&
        response_companion_store_latest_decision(state, &decision, &error);
    response_companion_response_input_destroy(&input);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion response headers are duplicated or invalid",
            "response_companion_transport");
    }
    if (result) {
        state->response_headers = 1;
        state->has_decision = 1;
    } else {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, result ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_body(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_error error;
    int result;

    msconnector_error_init(&error);
    result = state->response_headers && state->committed && !state->response_eos &&
        frame->payload_size <= MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK &&
        state->response_body_bytes <= worker->transport->config.max_response_body_bytes &&
        frame->payload_size <= worker->transport->config.max_response_body_bytes -
            state->response_body_bytes &&
        response_companion_backend_append_response_body_chunk(worker->transport,
            &state->session, frame->payload, frame->payload_size, &error);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, frame->payload_size >
            MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_MAX_BODY_CHUNK ||
            state->response_body_bytes > worker->transport->config.max_response_body_bytes ||
            frame->payload_size > worker->transport->config.max_response_body_bytes -
                state->response_body_bytes ?
                MSCONNECTOR_ERROR_BODY_TOO_LARGE : MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion response body operation is invalid",
            "response_companion_transport");
    }
    if (result) {
        state->response_body_bytes += frame->payload_size;
    }
    if (!result) {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, state->has_decision ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_eos(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_decision decision;
    msconnector_error error;
    int result;

    msconnector_decision_init(&decision);
    msconnector_error_init(&error);
    result = state->response_headers && state->committed && !state->response_eos &&
        frame->payload_size == 0U &&
        response_companion_backend_finish_response_body(worker->transport,
            &state->session, &decision, &error) &&
        response_companion_store_latest_decision(state, &decision, &error);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion response end-of-stream is invalid",
            "response_companion_transport");
    }
    if (result) {
        state->response_eos = 1;
        state->has_decision = 1;
    } else {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, result ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_commit(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_error error;
    int headers_sent;
    int body_started;
    int result;

    msconnector_error_init(&error);
    result = state->response_headers && !state->committed &&
        !state->response_eos && response_companion_parse_commit(frame,
            &headers_sent, &body_started) &&
        response_companion_backend_set_response_commit_state(worker->transport,
            &state->session, headers_sent, body_started, &error);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion commit is invalid", "response_companion_transport");
    }
    if (result) {
        state->committed = 1;
    } else {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, state->has_decision ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_outcome(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_error error;
    msconnector_decision_action actual_action;
    int visible_status;
    int connection_aborted;
    int result;

    msconnector_error_init(&error);
    /* A CLAIM supplies only a provisional allow so the peer can continue its
     * P3 exchange. It is never authority to report a host action. Require
     * completed response-header processing before accepting an OUTCOME; this
     * keeps raw peers at least as strict as the typed client and prevents a
     * custom backend from recording a pre-P3 action. */
    result = state->response_headers && state->has_decision && !state->outcome_recorded &&
        response_companion_parse_outcome(frame,
        &actual_action, &visible_status, &connection_aborted) &&
        response_companion_backend_record_host_action(worker->transport,
            &state->session,
            &(msconnector_response_companion_host_action){
                .decision = &state->latest_decision,
                .actual_action = actual_action,
                .visible_http_status = visible_status,
                .transport_result = response_companion_transport_result(
                    actual_action, connection_aborted),
                .connection_aborted = connection_aborted},
            &error);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        const char *message = "response companion outcome is invalid";

        if (state->outcome_recorded) {
            message = "response companion host outcome is duplicated";
        } else if (!state->response_headers) {
            message = "response companion host outcome requires P3";
        }
        msconnector_error_set(&error,
            state->outcome_recorded || !state->response_headers ?
                MSCONNECTOR_ERROR_PHASE_SEQUENCE : MSCONNECTOR_ERROR_PROTOCOL,
            message,
            "response_companion_transport");
    }
    if (result) {
        state->outcome_recorded = 1;
    } else {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, state->has_decision ? &state->latest_decision : NULL,
            &error)) {
        return 0;
    }
    return result;
}

static int response_companion_handle_cancel(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_error error;
    msconnector_response_companion_cancel_cause cause;
    msconnector_transaction_error_class error_class;
    int result;

    msconnector_error_init(&error);
    result = response_companion_parse_cancel(frame, &cause) &&
        response_companion_cancel_error_class(cause, &error_class);
    if (result && (cause == MSCONNECTOR_RESPONSE_COMPANION_CANCEL_CLIENT_CANCEL ||
            cause == MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT)) {
        result = response_companion_backend_cancel(worker->transport, &state->session,
            cause == MSCONNECTOR_RESPONSE_COMPANION_CANCEL_UPSTREAM_DISCONNECT,
            &error);
    } else if (result) {
        /* A typed local observer failure must reach the Common transaction
         * contract as its actual cause.  This terminal path is distinct from
         * CANCEL's client/upstream lifecycle acknowledgement. */
        response_companion_fail_session(worker->transport, state, error_class);
        result = state->session.opaque == NULL;
        if (!result) {
            msconnector_error_set(&error, MSCONNECTOR_ERROR_INTERNAL,
                "response companion typed cancel did not release its session",
                "response_companion_transport");
        }
    }
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PROTOCOL,
            "response companion cancel is invalid", "response_companion_transport");
    }
    if (!result) {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, NULL, &error)) {
        return 0;
    }
    if (result) {
        /* CANCEL performs deterministic ownership release. A connection may
         * carry another transaction only after that release, never while a
         * session is active. */
        response_companion_reset_session_state(state);
        return 1;
    }
    return 0;
}

static int response_companion_handle_release(
    msconnector_response_companion_transport_worker *worker,
    response_companion_session_state *state,
    const response_companion_frame *frame)
{
    msconnector_error error;
    int result;

    msconnector_error_init(&error);
    result = state->response_eos && frame->payload_size == 0U &&
        response_companion_backend_release(worker->transport, &state->session,
            &error);
    if (!result && error.code == MSCONNECTOR_ERROR_NONE) {
        msconnector_error_set(&error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion release before P4 end-of-stream is invalid",
            "response_companion_transport");
    }
    if (!result) {
        response_companion_fail_session(worker->transport, state,
            response_companion_error_class_from_error(&error));
    }
    if (!response_companion_send_result(worker->transport, worker->socket_fd,
            frame->opcode, result, NULL, &error)) {
        return 0;
    }
    if (result) {
        /* RELEASE has finished P4 and detached the exact claimed registry
         * entry. Reset every per-session bit before admitting the next CLAIM
         * on this trusted connection. */
        response_companion_reset_session_state(state);
        return 1;
    }
    return 0;
}

static void response_companion_remove_worker(
    msconnector_response_companion_transport_worker *worker)
{
    msconnector_response_companion_transport *transport;
    msconnector_response_companion_transport_worker **cursor;

    if (worker == NULL || worker->transport == NULL) {
        return;
    }
    transport = worker->transport;
    if (pthread_mutex_lock(&transport->synchronization.worker_lock) != 0) {
        return;
    }
    cursor = &transport->workers.workers;
    while (*cursor != NULL && *cursor != worker) {
        cursor = &(*cursor)->next;
    }
    if (*cursor == worker) {
        *cursor = worker->next;
        if (transport->workers.worker_count > 0U) {
            --transport->workers.worker_count;
        }
    }
    (void)pthread_cond_broadcast(&transport->synchronization.workers_idle);
    (void)pthread_mutex_unlock(&transport->synchronization.worker_lock);
}

static void *response_companion_worker_main(void *argument)
{
    msconnector_response_companion_transport_worker *worker = argument;
    response_companion_session_state state;
    int keep_running = 1;
    msconnector_transaction_error_class abort_error_class =
        MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;

    if (worker == NULL || worker->transport == NULL) {
        return NULL;
    }
    response_companion_reset_session_state(&state);
    while (keep_running && !atomic_load_explicit(&worker->transport->listener.stopping,
            memory_order_acquire)) {
        response_companion_frame frame;
        const response_companion_frame_result frame_result =
            response_companion_receive_frame(worker->transport, worker->socket_fd,
                &frame);

        if (frame_result != RESPONSE_COMPANION_FRAME_OK) {
            if (!atomic_load_explicit(&worker->transport->listener.stopping,
                    memory_order_acquire) &&
                frame_result == RESPONSE_COMPANION_FRAME_TIMEOUT) {
                abort_error_class = MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT;
            } else if (!atomic_load_explicit(&worker->transport->listener.stopping,
                    memory_order_acquire) &&
                frame_result == RESPONSE_COMPANION_FRAME_MALFORMED) {
                abort_error_class = MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
            }
            /* A private observer that closes without a typed terminal cause
             * may have crashed or lost its local transport.  It is never safe
             * to manufacture an upstream disconnect from that ambiguity. */
            response_companion_fail_session(worker->transport, &state,
                abort_error_class);
            break;
        }
        if (!state.claimed) {
            keep_running = frame.opcode == RESPONSE_COMPANION_CLAIM &&
                response_companion_handle_claim(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_RESPONSE_HEADERS) {
            keep_running = response_companion_handle_headers(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_RESPONSE_BODY) {
            keep_running = response_companion_handle_body(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_RESPONSE_EOS) {
            keep_running = response_companion_handle_eos(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_COMMIT) {
            keep_running = response_companion_handle_commit(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_OUTCOME) {
            keep_running = response_companion_handle_outcome(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_CANCEL) {
            keep_running = response_companion_handle_cancel(worker, &state, &frame);
        } else if (frame.opcode == RESPONSE_COMPANION_RELEASE) {
            keep_running = response_companion_handle_release(worker, &state, &frame);
        } else {
            msconnector_error error;
            msconnector_error_init(&error);
            msconnector_error_set(&error, MSCONNECTOR_ERROR_PROTOCOL,
                "response companion opcode is invalid", "response_companion_transport");
            response_companion_fail_session(worker->transport, &state,
                MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL);
            abort_error_class = MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
            (void)response_companion_send_result(worker->transport, worker->socket_fd,
                frame.opcode, 0, NULL, &error);
            keep_running = 0;
        }
        response_companion_frame_destroy(&frame);
    }
    response_companion_abort_session(worker->transport, &state,
        abort_error_class);
    (void)close(worker->socket_fd);
    response_companion_remove_worker(worker);
    free(worker);
    return NULL;
}

static int response_companion_start_worker(
    msconnector_response_companion_transport *transport, int socket_fd)
{
    msconnector_response_companion_transport_worker *worker;
    pthread_attr_t attributes;
    pthread_t thread;
    int result;

    if (transport == NULL || socket_fd < 0) {
        if (socket_fd >= 0) {
            (void)close(socket_fd);
        }
        return 0;
    }
    worker = calloc(1U, sizeof(*worker));
    if (worker == NULL) {
        (void)close(socket_fd);
        return 0;
    }
    worker->transport = transport;
    worker->socket_fd = socket_fd;
    if (pthread_mutex_lock(&transport->synchronization.worker_lock) != 0) {
        (void)close(socket_fd);
        free(worker);
        return 0;
    }
    if (atomic_load_explicit(&transport->listener.stopping, memory_order_acquire) ||
        transport->workers.worker_count >= MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY) {
        (void)pthread_mutex_unlock(&transport->synchronization.worker_lock);
        (void)close(socket_fd);
        free(worker);
        return 0;
    }
    worker->next = transport->workers.workers;
    transport->workers.workers = worker;
    ++transport->workers.worker_count;
    (void)pthread_mutex_unlock(&transport->synchronization.worker_lock);
    if (pthread_attr_init(&attributes) != 0) {
        response_companion_remove_worker(worker);
        (void)close(socket_fd);
        free(worker);
        return 0;
    }
    result = pthread_attr_setdetachstate(&attributes, PTHREAD_CREATE_DETACHED);
    if (result == 0) {
        result = pthread_create(&thread, &attributes,
            response_companion_worker_main, worker);
    }
    (void)pthread_attr_destroy(&attributes);
    if (result != 0) {
        response_companion_remove_worker(worker);
        (void)close(socket_fd);
        free(worker);
        return 0;
    }
    return 1;
}

static void *response_companion_listener_main(void *argument)
{
    msconnector_response_companion_transport *transport = argument;
    int running = 1;

    if (transport == NULL) {
        return NULL;
    }
    while (running && !atomic_load_explicit(&transport->listener.stopping,
            memory_order_acquire)) {
        struct pollfd descriptor;
        int polled;
        int client_fd;

        response_companion_backend_expire(transport, response_companion_now_ms());
        memset(&descriptor, 0, sizeof(descriptor));
        descriptor.fd = transport->listener.listener_fd;
        descriptor.events = POLLIN;
        polled = poll(&descriptor, 1U, RESPONSE_COMPANION_ACCEPT_POLL_MS);
        if (polled == 0 || (polled < 0 && errno == EINTR)) {
            continue;
        }
        if (polled < 0 || (descriptor.revents & POLLIN) == 0 ||
            atomic_load_explicit(&transport->listener.stopping, memory_order_acquire)) {
            running = 0;
            continue;
        }
        client_fd = accept4(transport->listener.listener_fd, NULL, NULL, SOCK_CLOEXEC);
        if (client_fd < 0) {
            if (errno == EINTR || errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;
            }
            running = 0;
            continue;
        }
        if (!response_companion_peer_is_expected(transport, client_fd)) {
            (void)close(client_fd);
            continue;
        }
        (void)response_companion_start_worker(transport, client_fd);
    }
    atomic_store_explicit(&transport->listener.running, 0, memory_order_release);
    return NULL;
}

static int response_companion_header_limits_are_valid(size_t max_header_count,
    size_t max_header_bytes)
{
    return max_header_count > 0U &&
        max_header_count <= MSCONNECTOR_MAX_HEADER_COUNT &&
        max_header_bytes > 0U &&
        max_header_bytes <= MSCONNECTOR_MAX_TOTAL_HEADER_BYTES;
}

static int response_companion_backend_is_valid(
    const msconnector_response_companion_backend *backend)
{
    return backend != NULL && backend->claim != NULL &&
        backend->process_response_headers != NULL &&
        backend->append_response_body_chunk != NULL &&
        backend->finish_response_body != NULL &&
        backend->set_response_commit_state != NULL &&
        backend->record_host_action != NULL && backend->cancel != NULL &&
        backend->release != NULL && backend->fail != NULL;
}

int msconnector_response_companion_transport_init_with_backend(
    msconnector_response_companion_transport *transport,
    const msconnector_response_companion_backend *backend,
    const msconnector_response_companion_transport_options *options,
    msconnector_error *error)
{
    size_t connector_size;
    size_t path_size;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    connector_size = options == NULL || options->connector_id == NULL ? 0U :
        strlen(options->connector_id);
    path_size = options == NULL || options->socket_path == NULL ? 0U :
        strlen(options->socket_path);
    if (transport == NULL || !response_companion_backend_is_valid(backend) ||
        connector_size == 0U ||
        connector_size >= sizeof(transport->config.connector_id) || path_size == 0U ||
        path_size >= sizeof(transport->config.socket_path) || !response_companion_path_is_safe(
        options->socket_path) || !response_companion_header_limits_are_valid(
            options->max_header_count, options->max_header_bytes) ||
        options->max_response_body_bytes == 0U || options->operation_timeout_ms == 0U ||
        options->operation_timeout_ms > UINT64_C(600000)) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion transport configuration is invalid");
    }
    memset(transport, 0, sizeof(*transport));
    transport->config.backend = *backend;
    memcpy(transport->config.connector_id, options->connector_id, connector_size + 1U);
    memcpy(transport->config.socket_path, options->socket_path, path_size + 1U);
    transport->config.max_header_count = options->max_header_count;
    transport->config.max_header_bytes = options->max_header_bytes;
    transport->config.max_response_body_bytes = options->max_response_body_bytes;
    transport->config.operation_timeout_ms = options->operation_timeout_ms;
    transport->config.expected_uid = geteuid();
    transport->config.expected_gid = getegid();
    transport->listener.listener_fd = -1;
    atomic_init(&transport->listener.running, 0);
    atomic_init(&transport->listener.stopping, 0);
    atomic_init(&transport->synchronization.backend_faulted, 0);
    if (pthread_mutex_init(&transport->synchronization.worker_lock, NULL) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion transport synchronization setup failed");
    }
    if (pthread_cond_init(&transport->synchronization.workers_idle, NULL) != 0) {
        (void)pthread_mutex_destroy(&transport->synchronization.worker_lock);
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion transport synchronization setup failed");
    }
    if (pthread_mutex_init(&transport->synchronization.backend_lock, NULL) != 0) {
        (void)pthread_cond_destroy(&transport->synchronization.workers_idle);
        (void)pthread_mutex_destroy(&transport->synchronization.worker_lock);
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion backend synchronization setup failed");
    }
    transport->synchronization.initialized = 1;
    return 1;
}

int msconnector_response_companion_transport_init(
    msconnector_response_companion_transport *transport,
    msconnector_runtime_response_companion_registry *registry,
    const msconnector_response_companion_transport_options *options,
    msconnector_error *error)
{
    msconnector_response_companion_backend backend =
        response_companion_runtime_backend;
    int result;

    if (registry == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion Runtime registry is required");
    }
    backend.context = registry;
    result = msconnector_response_companion_transport_init_with_backend(transport,
        &backend, options, error);
    if (result) {
        transport->config.registry = registry;
    }
    return result;
}

int msconnector_response_companion_transport_ensure_running(
    msconnector_response_companion_transport *transport,
    msconnector_error *error)
{
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transport == NULL || !transport->synchronization.initialized) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion transport is not initialized");
    }
    if (atomic_load_explicit(&transport->listener.stopping, memory_order_acquire)) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion transport cleanup is incomplete");
    }
    if (atomic_load_explicit(&transport->listener.running, memory_order_acquire)) {
        return 1;
    }
    if (transport->listener.listener_started ||
        transport->listener.listener_fd >= 0 || transport->listener.identity_valid) {
        if (!msconnector_response_companion_transport_stop(transport, error)) {
            return 0;
        }
    }
    return msconnector_response_companion_transport_start(transport, error);
}

int msconnector_response_companion_transport_ensure_started(
    msconnector_response_companion_transport *transport,
    msconnector_runtime_response_companion_registry *registry,
    int *transport_initialized,
    int *transport_ready,
    const msconnector_response_companion_transport_options *options,
    msconnector_error *error)
{
    if (transport == NULL || registry == NULL || transport_initialized == NULL ||
        transport_ready == NULL || options == NULL) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion transport startup requires complete host state");
    }
    if (*transport_ready && !*transport_initialized) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion transport startup flags are inconsistent");
    }
    if (!*transport_initialized) {
        if (!msconnector_response_companion_transport_init(transport, registry, options, error)) {
            return 0;
        }
        *transport_initialized = 1;
    }
    if (!msconnector_response_companion_transport_ensure_running(transport, error)) {
        *transport_ready = 0;
        return 0;
    }
    *transport_ready = 1;
    return 1;
}

int msconnector_response_companion_transport_start(
    msconnector_response_companion_transport *transport,
    msconnector_error *error)
{
    int listener_fd;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transport == NULL || !transport->synchronization.initialized ||
        !response_companion_backend_is_valid(&transport->config.backend) ||
        !response_companion_header_limits_are_valid(
            transport->config.max_header_count, transport->config.max_header_bytes) ||
        atomic_load_explicit(&transport->listener.running, memory_order_acquire) ||
        atomic_load_explicit(&transport->listener.stopping, memory_order_acquire) ||
        atomic_load_explicit(&transport->synchronization.backend_faulted, memory_order_acquire)) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion transport is not startable");
    }
#if !defined(__linux__)
    return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
        "response companion transport requires Linux SO_PEERCRED");
#endif
    listener_fd = response_companion_create_listener(transport);
    if (listener_fd < 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion private UDS listener setup failed");
    }
    transport->listener.listener_fd = listener_fd;
    atomic_store_explicit(&transport->listener.running, 1, memory_order_release);
    if (pthread_create(&transport->listener.listener_thread, NULL,
            response_companion_listener_main, transport) != 0) {
        atomic_store_explicit(&transport->listener.running, 0, memory_order_release);
        (void)close(transport->listener.listener_fd);
        transport->listener.listener_fd = -1;
        (void)response_companion_remove_owned_socket(transport);
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion listener worker setup failed");
    }
    transport->listener.listener_started = 1;
    return 1;
}

int msconnector_response_companion_transport_stop(
    msconnector_response_companion_transport *transport,
    msconnector_error *error)
{
    int cleanup_result = 1;
    int join_result;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transport == NULL || !transport->synchronization.initialized) {
        return response_companion_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion transport is required");
    }
    atomic_store_explicit(&transport->listener.stopping, 1, memory_order_release);
    if (transport->listener.listener_fd >= 0) {
        (void)shutdown(transport->listener.listener_fd, SHUT_RDWR);
    }
    if (transport->listener.listener_started) {
        join_result = pthread_join(transport->listener.listener_thread, NULL);
        if (join_result != 0) {
            return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                "response companion listener join failed during cleanup");
        }
        transport->listener.listener_started = 0;
    }
    /* The listener is the only thread that polls/accepts this descriptor.
     * Stop wakes it with shutdown and closes it only after join, preventing
     * descriptor reuse from racing with poll/accept. */
    if (transport->listener.listener_fd >= 0) {
        (void)close(transport->listener.listener_fd);
        transport->listener.listener_fd = -1;
    }
    if (pthread_mutex_lock(&transport->synchronization.worker_lock) != 0) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion worker lock failed during cleanup");
    }
    for (msconnector_response_companion_transport_worker *worker = transport->workers.workers;
        worker != NULL; worker = worker->next) {
        (void)shutdown(worker->socket_fd, SHUT_RDWR);
    }
    while (transport->workers.worker_count > 0U) {
        if (pthread_cond_wait(&transport->synchronization.workers_idle, &transport->synchronization.worker_lock) != 0) {
            cleanup_result = 0;
            break;
        }
    }
    (void)pthread_mutex_unlock(&transport->synchronization.worker_lock);
    if (!response_companion_remove_owned_socket(transport)) {
        cleanup_result = 0;
    }
    transport->listener.identity_valid = 0;
    atomic_store_explicit(&transport->listener.running, 0, memory_order_release);
    if (!cleanup_result) {
        return response_companion_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion transport cleanup was incomplete");
    }
    /* A successful complete cleanup leaves the initialized transport
     * restartable.  Failed cleanup deliberately retains `stopping` so no
     * caller can reuse a transport whose listener or workers may still live. */
    atomic_store_explicit(&transport->listener.stopping, 0, memory_order_release);
    return 1;
}
