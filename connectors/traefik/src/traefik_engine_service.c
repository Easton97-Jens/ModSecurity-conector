#define _GNU_SOURCE
#define _POSIX_C_SOURCE 200809L

#include "traefik_engine_protocol.h"

#include "common/runtime/msconnector_runtime.h"

#include <errno.h>
#include <fcntl.h>
#include <limits.h>
#include <pthread.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/poll.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

#define TRAEFIK_ENGINE_CONFIG_LINE_MAX 8192U
#define TRAEFIK_ENGINE_SOCKET_TIMEOUT_SECONDS 30
#define TRAEFIK_ENGINE_ACCEPT_POLL_MILLISECONDS 250
#define TRAEFIK_ENGINE_LISTEN_BACKLOG 32

typedef struct traefik_engine_frame {
    uint8_t opcode;
    unsigned char *payload;
    size_t payload_size;
} traefik_engine_frame;

typedef struct traefik_engine_reader {
    const unsigned char *data;
    size_t size;
    size_t offset;
} traefik_engine_reader;

typedef struct traefik_engine_headers {
    msconnector_header *items;
    char **names;
    char **values;
    size_t count;
} traefik_engine_headers;

typedef struct traefik_engine_request_input {
    msconnector_request request;
    char *method;
    char *uri;
    char *http_version;
    char *hostname;
    char *client_address;
    char *server_address;
    char *host_request_id;
    traefik_engine_headers headers;
} traefik_engine_request_input;

typedef struct traefik_engine_response_input {
    msconnector_response response;
    char *http_version;
    traefik_engine_headers headers;
} traefik_engine_response_input;

typedef struct traefik_engine_service {
    msconnector_runtime *runtime;
    pthread_mutex_t runtime_lock;
    pthread_mutex_t worker_lock;
    pthread_cond_t workers_idle;
    size_t worker_count;
    msconnector_body_mode request_body_mode;
    msconnector_body_mode response_body_mode;
} traefik_engine_service;

typedef struct traefik_engine_session {
    traefik_engine_service *service;
    msconnector_runtime_transaction *transaction;
    int begun;
    int request_eos;
    int response_headers;
    int response_eos;
    int response_headers_sent;
    int response_body_started;
    int finished;
    int destroyed;
    int terminal;
    int pending_disruptive;
    uint8_t pending_action;
    uint8_t pending_phase;
    uint16_t pending_status;
    int response_status;
    msconnector_decision pending_decision;
    char pending_rule_id[TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID + 1U];
    char pending_redirect[TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT + 1U];
    char pending_reason[512U];
} traefik_engine_session;

typedef struct traefik_engine_worker_arg {
    traefik_engine_service *service;
    int socket_fd;
} traefik_engine_worker_arg;

typedef struct traefik_engine_socket_identity {
    dev_t device;
    ino_t inode;
    uid_t owner;
    int valid;
} traefik_engine_socket_identity;

typedef int (*traefik_engine_listener_pre_bind_hook_fn)(const char *socket_path);

static volatile sig_atomic_t traefik_engine_stop_requested = 0;
static traefik_engine_listener_pre_bind_hook_fn
    traefik_engine_listener_pre_bind_hook = NULL;
static traefik_engine_listener_pre_bind_hook_fn
    traefik_engine_listener_post_bind_hook = NULL;
static traefik_engine_listener_pre_bind_hook_fn
    traefik_engine_listener_post_probe_hook = NULL;

static void traefik_engine_stop_handler(int signum)
{
    (void)signum;
    traefik_engine_stop_requested = 1;
}

static uint16_t traefik_engine_read_u16(const unsigned char *value)
{
    return (uint16_t)(((uint16_t)value[0] << 8) | (uint16_t)value[1]);
}

static uint32_t traefik_engine_read_u32(const unsigned char *value)
{
    return ((uint32_t)value[0] << 24) |
        ((uint32_t)value[1] << 16) |
        ((uint32_t)value[2] << 8) |
        (uint32_t)value[3];
}

static void traefik_engine_write_u16(unsigned char *value, uint16_t number)
{
    value[0] = (unsigned char)(number >> 8);
    value[1] = (unsigned char)number;
}

static void traefik_engine_write_u32(unsigned char *value, uint32_t number)
{
    value[0] = (unsigned char)(number >> 24);
    value[1] = (unsigned char)(number >> 16);
    value[2] = (unsigned char)(number >> 8);
    value[3] = (unsigned char)number;
}

static int traefik_engine_string_has_nul(const unsigned char *value, size_t size)
{
    return value != NULL && memchr(value, '\0', size) != NULL;
}

static size_t traefik_engine_bounded_string_size(const char *value, size_t maximum)
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

static uint16_t traefik_engine_clamp_u16(size_t value)
{
    return value > UINT16_MAX ? UINT16_MAX : (uint16_t)value;
}

static int traefik_engine_send_all(int socket_fd, const unsigned char *data,
    size_t size)
{
    size_t offset = 0U;
    while (offset < size) {
        ssize_t written = send(socket_fd, data + offset, size - offset,
            MSG_NOSIGNAL);
        if (written > 0) {
            offset += (size_t)written;
            continue;
        }
        if (written < 0 && errno == EINTR) {
            continue;
        }
        return 0;
    }
    return 1;
}

/* Returns 1 for a complete read, 0 for EOF, and -1 for an I/O failure. */
static int traefik_engine_receive_all(int socket_fd, unsigned char *data,
    size_t size)
{
    size_t offset = 0U;
    while (offset < size) {
        ssize_t received = recv(socket_fd, data + offset, size - offset, 0);
        if (received > 0) {
            offset += (size_t)received;
            continue;
        }
        if (received == 0) {
            return 0;
        }
        if (errno == EINTR) {
            continue;
        }
        return -1;
    }
    return 1;
}

static void traefik_engine_frame_reset(traefik_engine_frame *frame)
{
    if (frame == NULL) {
        return;
    }
    free(frame->payload);
    memset(frame, 0, sizeof(*frame));
}

/* Returns 1 for a valid frame, 0 for clean EOF, -1 for malformed/I/O input. */
static int traefik_engine_receive_frame(int socket_fd, traefik_engine_frame *frame)
{
    unsigned char header[TRAEFIK_ENGINE_PROTOCOL_HEADER_SIZE];
    uint32_t payload_size;
    int received;

    if (frame == NULL) {
        return -1;
    }
    traefik_engine_frame_reset(frame);
    received = traefik_engine_receive_all(socket_fd, header, sizeof(header));
    if (received != 1) {
        return received;
    }
    if (memcmp(header, "MSE1", 4U) != 0 ||
        header[4] != TRAEFIK_ENGINE_PROTOCOL_VERSION ||
        header[6] != 0U || header[7] != 0U) {
        return -1;
    }
    payload_size = traefik_engine_read_u32(header + 8U);
    if (payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD) {
        return -1;
    }
    frame->opcode = header[5];
    frame->payload_size = (size_t)payload_size;
    if (frame->payload_size == 0U) {
        return 1;
    }
    frame->payload = malloc(frame->payload_size);
    if (frame->payload == NULL) {
        traefik_engine_frame_reset(frame);
        return -1;
    }
    received = traefik_engine_receive_all(socket_fd, frame->payload,
        frame->payload_size);
    if (received != 1) {
        traefik_engine_frame_reset(frame);
        return -1;
    }
    return 1;
}

static int traefik_engine_send_frame(int socket_fd, uint8_t opcode,
    const unsigned char *payload, size_t payload_size)
{
    unsigned char header[TRAEFIK_ENGINE_PROTOCOL_HEADER_SIZE];
    if (payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD ||
        (payload_size > 0U && payload == NULL)) {
        return 0;
    }
    memcpy(header, "MSE1", 4U);
    header[4] = TRAEFIK_ENGINE_PROTOCOL_VERSION;
    header[5] = opcode;
    header[6] = 0U;
    header[7] = 0U;
    traefik_engine_write_u32(header + 8U, (uint32_t)payload_size);
    if (!traefik_engine_send_all(socket_fd, header, sizeof(header))) {
        return 0;
    }
    return payload_size == 0U ||
        traefik_engine_send_all(socket_fd, payload, payload_size);
}

static int traefik_engine_reader_u16(traefik_engine_reader *reader,
    uint16_t *out)
{
    if (reader == NULL || out == NULL || reader->offset > reader->size ||
        reader->size - reader->offset < 2U) {
        return 0;
    }
    *out = traefik_engine_read_u16(reader->data + reader->offset);
    reader->offset += 2U;
    return 1;
}

static int traefik_engine_reader_text(traefik_engine_reader *reader,
    size_t maximum, int required, char **out)
{
    uint16_t length;
    char *copy;

    if (reader == NULL || out == NULL ||
        !traefik_engine_reader_u16(reader, &length) ||
        (required && length == 0U) || (size_t)length > maximum ||
        reader->offset > reader->size ||
        reader->size - reader->offset < (size_t)length ||
        traefik_engine_string_has_nul(reader->data + reader->offset,
            (size_t)length)) {
        return 0;
    }
    copy = calloc((size_t)length + 1U, 1U);
    if (copy == NULL) {
        return 0;
    }
    if (length > 0U) {
        memcpy(copy, reader->data + reader->offset, (size_t)length);
    }
    reader->offset += (size_t)length;
    *out = copy;
    return 1;
}

static void traefik_engine_headers_free(traefik_engine_headers *headers)
{
    if (headers == NULL) {
        return;
    }
    for (size_t index = 0U; index < headers->count; ++index) {
        free(headers->names == NULL ? NULL : headers->names[index]);
        free(headers->values == NULL ? NULL : headers->values[index]);
    }
    free(headers->names);
    free(headers->values);
    free(headers->items);
    memset(headers, 0, sizeof(*headers));
}

static int traefik_engine_reader_headers(traefik_engine_reader *reader,
    uint16_t header_count, traefik_engine_headers *out)
{
    if (reader == NULL || out == NULL ||
        header_count > TRAEFIK_ENGINE_PROTOCOL_MAX_HEADERS) {
        return 0;
    }
    memset(out, 0, sizeof(*out));
    if (header_count == 0U) {
        return 1;
    }
    out->items = calloc((size_t)header_count, sizeof(*out->items));
    out->names = calloc((size_t)header_count, sizeof(*out->names));
    out->values = calloc((size_t)header_count, sizeof(*out->values));
    out->count = (size_t)header_count;
    if (out->items == NULL || out->names == NULL || out->values == NULL) {
        traefik_engine_headers_free(out);
        return 0;
    }
    for (size_t index = 0U; index < (size_t)header_count; ++index) {
        if (!traefik_engine_reader_text(reader,
                TRAEFIK_ENGINE_PROTOCOL_MAX_HEADER_NAME, 1,
                &out->names[index]) ||
            !traefik_engine_reader_text(reader,
                TRAEFIK_ENGINE_PROTOCOL_MAX_HEADER_VALUE, 0,
                &out->values[index])) {
            traefik_engine_headers_free(out);
            return 0;
        }
        out->items[index].name = out->names[index];
        out->items[index].name_size = strlen(out->names[index]);
        out->items[index].value = out->values[index];
        out->items[index].value_size = strlen(out->values[index]);
    }
    return 1;
}

static void traefik_engine_request_input_free(
    traefik_engine_request_input *input)
{
    if (input == NULL) {
        return;
    }
    free(input->method);
    free(input->uri);
    free(input->http_version);
    free(input->hostname);
    free(input->client_address);
    free(input->server_address);
    free(input->host_request_id);
    traefik_engine_headers_free(&input->headers);
    memset(input, 0, sizeof(*input));
}

static int traefik_engine_parse_begin(const unsigned char *payload,
    size_t payload_size, traefik_engine_request_input *out)
{
    traefik_engine_reader reader;
    uint16_t client_port;
    uint16_t server_port;
    uint16_t header_count;

    if (payload == NULL || out == NULL ||
        payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD) {
        return 0;
    }
    memset(out, 0, sizeof(*out));
    reader.data = payload;
    reader.size = payload_size;
    reader.offset = 0U;
    if (!traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_METHOD, 1, &out->method) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_URI, 1, &out->uri) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_HTTP_VERSION, 1, &out->http_version) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_HOSTNAME, 0, &out->hostname) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_ADDRESS, 0, &out->client_address) ||
        !traefik_engine_reader_u16(&reader, &client_port) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_ADDRESS, 0, &out->server_address) ||
        !traefik_engine_reader_u16(&reader, &server_port) ||
        !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_HOST_REQUEST_ID, 0,
            &out->host_request_id) ||
        !traefik_engine_reader_u16(&reader, &header_count) ||
        !traefik_engine_reader_headers(&reader, header_count, &out->headers) ||
        reader.offset != reader.size) {
        traefik_engine_request_input_free(out);
        return 0;
    }
    out->request.method = out->method;
    out->request.uri = out->uri;
    out->request.http_version = out->http_version;
    out->request.hostname = out->hostname;
    out->request.client.address = out->client_address;
    out->request.client.port = (int)client_port;
    out->request.server.address = out->server_address;
    out->request.server.port = (int)server_port;
    out->request.headers = out->headers.items;
    out->request.header_count = (size_t)header_count;
    out->request.body.data = NULL;
    out->request.body.size = 0U;
    return 1;
}

static void traefik_engine_response_input_free(
    traefik_engine_response_input *input)
{
    if (input == NULL) {
        return;
    }
    free(input->http_version);
    traefik_engine_headers_free(&input->headers);
    memset(input, 0, sizeof(*input));
}

static int traefik_engine_parse_response_headers(const unsigned char *payload,
    size_t payload_size, traefik_engine_response_input *out)
{
    traefik_engine_reader reader;
    uint16_t status;
    uint16_t header_count;

    if (payload == NULL || out == NULL ||
        payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_FRAME_PAYLOAD) {
        return 0;
    }
    memset(out, 0, sizeof(*out));
    reader.data = payload;
    reader.size = payload_size;
    reader.offset = 0U;
    if (!traefik_engine_reader_u16(&reader, &status) || status < 100U ||
        status > 999U || !traefik_engine_reader_text(&reader,
            TRAEFIK_ENGINE_PROTOCOL_MAX_HTTP_VERSION, 1, &out->http_version) ||
        !traefik_engine_reader_u16(&reader, &header_count) ||
        !traefik_engine_reader_headers(&reader, header_count, &out->headers) ||
        reader.offset != reader.size) {
        traefik_engine_response_input_free(out);
        return 0;
    }
    out->response.status = (int)status;
    out->response.http_version = out->http_version;
    out->response.headers = out->headers.items;
    out->response.header_count = (size_t)header_count;
    out->response.body.data = NULL;
    out->response.body.size = 0U;
    return 1;
}

static int traefik_engine_is_command_opcode(uint8_t opcode)
{
    return opcode >= TRAEFIK_ENGINE_PROTOCOL_BEGIN &&
        opcode <= TRAEFIK_ENGINE_PROTOCOL_OUTCOME;
}

static uint8_t traefik_engine_result_for_runtime_error(
    const msconnector_error *error)
{
    if (error != NULL && (error->code == MSCONNECTOR_ERROR_BODY_TOO_LARGE ||
        error->code == MSCONNECTOR_ERROR_HEADER_TOO_LARGE ||
        error->code == MSCONNECTOR_ERROR_EVENT_TOO_LARGE ||
        error->code == MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE)) {
        return TRAEFIK_ENGINE_PROTOCOL_RESULT_LIMIT;
    }
    return TRAEFIK_ENGINE_PROTOCOL_RESULT_RUNTIME;
}

static uint16_t traefik_engine_session_flags(
    const traefik_engine_session *session, const msconnector_decision *decision)
{
    uint16_t flags = 0U;
    if (decision != NULL && decision->disruptive) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_DISRUPTIVE;
    }
    if (decision != NULL && decision->late_intervention) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_LATE;
    }
    if (session == NULL) {
        return flags;
    }
    if (session->request_eos) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_REQUEST_EOS;
    }
    if (session->response_headers) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_RESPONSE_HEADERS;
    }
    if (session->response_eos) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_RESPONSE_EOS;
    }
    if (session->finished) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_FINISHED;
    }
    if (session->destroyed) {
        flags |= TRAEFIK_ENGINE_PROTOCOL_RESULT_DESTROYED;
    }
    return flags;
}

/* RESULT payload is fixed metadata followed by bounded transaction/rule/URL. */
static int traefik_engine_send_result(int socket_fd, uint8_t command,
    uint8_t result_code, const traefik_engine_session *session,
    const msconnector_decision *decision)
{
    const char *transaction_id = NULL;
    const char *rule_id = NULL;
    const char *redirect = NULL;
    size_t transaction_id_size;
    size_t rule_id_size;
    size_t redirect_size;
    size_t payload_size;
    unsigned char *payload;
    size_t offset;
    uint8_t action = MSCONNECTOR_DECISION_KIND_ALLOW;
    uint8_t phase = MSCONNECTOR_PHASE_CONNECTION;
    uint16_t status = 0U;

    if (session != NULL && session->transaction != NULL) {
        transaction_id = msconnector_runtime_transaction_id(session->transaction);
    }
    if (decision != NULL) {
        action = (uint8_t)decision->kind;
        phase = (uint8_t)decision->phase;
        if (decision->http_status > 0 && decision->http_status <= UINT16_MAX) {
            status = (uint16_t)decision->http_status;
        }
        rule_id = decision->rule_id;
        redirect = decision->redirect_url;
    }
    transaction_id_size = traefik_engine_bounded_string_size(transaction_id,
        TRAEFIK_ENGINE_PROTOCOL_MAX_TRANSACTION_ID);
    rule_id_size = traefik_engine_bounded_string_size(rule_id,
        TRAEFIK_ENGINE_PROTOCOL_MAX_RULE_ID);
    redirect_size = traefik_engine_bounded_string_size(redirect,
        TRAEFIK_ENGINE_PROTOCOL_MAX_REDIRECT);
    payload_size = 14U + transaction_id_size + rule_id_size + redirect_size;
    payload = calloc(payload_size, 1U);
    if (payload == NULL) {
        return 0;
    }
    payload[0] = command;
    payload[1] = result_code;
    payload[2] = action;
    payload[3] = phase;
    traefik_engine_write_u16(payload + 4U, status);
    traefik_engine_write_u16(payload + 6U,
        traefik_engine_session_flags(session, decision));
    traefik_engine_write_u16(payload + 8U,
        traefik_engine_clamp_u16(transaction_id_size));
    traefik_engine_write_u16(payload + 10U,
        traefik_engine_clamp_u16(rule_id_size));
    traefik_engine_write_u16(payload + 12U,
        traefik_engine_clamp_u16(redirect_size));
    offset = 14U;
    if (transaction_id != NULL && transaction_id_size > 0U) {
        memcpy(payload + offset, transaction_id, transaction_id_size);
        offset += transaction_id_size;
    }
    if (rule_id != NULL && rule_id_size > 0U) {
        memcpy(payload + offset, rule_id, rule_id_size);
        offset += rule_id_size;
    }
    if (redirect != NULL && redirect_size > 0U) {
        memcpy(payload + offset, redirect, redirect_size);
    }
    if (!traefik_engine_send_frame(socket_fd, TRAEFIK_ENGINE_PROTOCOL_RESULT,
            payload, payload_size)) {
        free(payload);
        return 0;
    }
    free(payload);
    return 1;
}

static void traefik_engine_set_allow_phase(msconnector_decision *decision,
    enum msconnector_phase phase)
{
    msconnector_decision_set_allow(decision);
    if (decision != NULL) {
        decision->phase = phase;
    }
}

static void traefik_engine_copy_pending_text(char *destination,
    size_t destination_size, const char *source)
{
    if (destination == NULL || destination_size == 0U) {
        return;
    }
    if (source == NULL) {
        destination[0] = '\0';
        return;
    }
    (void)snprintf(destination, destination_size, "%s", source);
}

static msconnector_decision_action traefik_engine_host_action(uint8_t action)
{
    switch ((msconnector_decision_kind)action) {
    case MSCONNECTOR_DECISION_KIND_DENY:
        return MSCONNECTOR_DECISION_ACTION_DENY;
    case MSCONNECTOR_DECISION_KIND_REDIRECT:
        return MSCONNECTOR_DECISION_ACTION_REDIRECT;
    case MSCONNECTOR_DECISION_KIND_DROP:
        return MSCONNECTOR_DECISION_ACTION_DROP;
    case MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT:
        return MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
    case MSCONNECTOR_DECISION_KIND_LOG_ONLY:
        return MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    case MSCONNECTOR_DECISION_KIND_ERROR:
        return MSCONNECTOR_DECISION_ACTION_ERROR;
    case MSCONNECTOR_DECISION_KIND_UNSUPPORTED:
        return MSCONNECTOR_DECISION_ACTION_UNSUPPORTED;
    case MSCONNECTOR_DECISION_KIND_ALLOW:
    default:
        return MSCONNECTOR_DECISION_ACTION_ALLOW;
    }
}

static void traefik_engine_record_decision(traefik_engine_session *session,
    const msconnector_decision *decision)
{
    if (session == NULL || decision == NULL || !decision->disruptive) {
        return;
    }
    session->terminal = 1;
    session->pending_disruptive = 1;
    session->pending_action = (uint8_t)decision->kind;
    session->pending_phase = (uint8_t)decision->phase;
    session->pending_status = decision->http_status > 0 &&
        decision->http_status <= UINT16_MAX ? (uint16_t)decision->http_status
        : 0U;
    session->pending_decision = *decision;
    traefik_engine_copy_pending_text(session->pending_rule_id,
        sizeof(session->pending_rule_id), decision->rule_id);
    traefik_engine_copy_pending_text(session->pending_redirect,
        sizeof(session->pending_redirect), decision->redirect_url);
    traefik_engine_copy_pending_text(session->pending_reason,
        sizeof(session->pending_reason), decision->reason);
    session->pending_decision.rule_id = session->pending_rule_id[0] == '\0'
        ? NULL : session->pending_rule_id;
    session->pending_decision.redirect_url = session->pending_redirect[0] == '\0'
        ? NULL : session->pending_redirect;
    session->pending_decision.reason = session->pending_reason[0] == '\0'
        ? NULL : session->pending_reason;
    session->pending_decision.log_message = session->pending_decision.reason;
}

static int traefik_engine_record_host_outcome(traefik_engine_session *session,
    msconnector_decision_action actual_action, int visible_http_status,
    const char *transport_result, msconnector_error *error)
{
    int success;
    if (session == NULL || session->transaction == NULL ||
        !session->pending_disruptive) {
        return 0;
    }
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        return 0;
    }
    success = msconnector_runtime_transaction_record_host_action(
        session->transaction, &session->pending_decision, actual_action,
        visible_http_status, transport_result, 0, error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    return success;
}

static void traefik_engine_session_destroy(traefik_engine_session *session)
{
    if (session == NULL || session->transaction == NULL) {
        return;
    }
    if (session->service != NULL &&
        pthread_mutex_lock(&session->service->runtime_lock) == 0) {
        msconnector_runtime_transaction_destroy(&session->transaction);
        (void)pthread_mutex_unlock(&session->service->runtime_lock);
    }
    session->destroyed = 1;
}

static int traefik_engine_handle_begin(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    traefik_engine_request_input input;
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || session->begun ||
        frame->payload_size == 0U ||
        !traefik_engine_parse_begin(frame->payload, frame->payload_size, &input)) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        traefik_engine_request_input_free(&input);
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_begin(session->service->runtime,
        &input.request, input.host_request_id, &session->transaction, decision,
        &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    traefik_engine_request_input_free(&input);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    session->begun = 1;
    /* Even a Common "none" body policy requires an explicit transport EOS. */
    session->request_eos = 0;
    traefik_engine_record_decision(session, decision);
    return 1;
}

static int traefik_engine_handle_request_chunk(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || session->terminal || session->request_eos ||
        frame->payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_CHUNK ||
        session->service->request_body_mode == MSCONNECTOR_BODY_MODE_NONE) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_append_request_body_chunk(
        session->transaction, frame->payload, frame->payload_size, &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_REQUEST_BODY);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    return 1;
}

static int traefik_engine_handle_request_eos(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || session->request_eos || frame->payload_size != 0U) {
        return 0;
    }
    if (session->service->request_body_mode == MSCONNECTOR_BODY_MODE_NONE) {
        traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_REQUEST_BODY);
        session->request_eos = 1;
        return 1;
    }
    if (session->terminal) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_finish_request_body(
        session->transaction, decision, &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    session->request_eos = 1;
    traefik_engine_record_decision(session, decision);
    return 1;
}

static int traefik_engine_handle_response_headers(
    traefik_engine_session *session, const traefik_engine_frame *frame,
    msconnector_decision *decision, uint8_t *result_code)
{
    traefik_engine_response_input input;
    msconnector_error error;
    int success;
    int response_status;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || session->terminal || !session->request_eos ||
        session->response_headers || frame->payload_size == 0U ||
        !traefik_engine_parse_response_headers(frame->payload,
            frame->payload_size, &input)) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        traefik_engine_response_input_free(&input);
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_process_response_headers(
        session->transaction, &input.response, decision, &error);
    response_status = input.response.status;
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    traefik_engine_response_input_free(&input);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    session->response_headers = 1;
    session->response_status = response_status;
    traefik_engine_record_decision(session, decision);
    return 1;
}

static int traefik_engine_handle_response_chunk(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || session->terminal || !session->response_headers ||
        session->response_eos ||
        frame->payload_size > TRAEFIK_ENGINE_PROTOCOL_MAX_CHUNK ||
        session->service->response_body_mode == MSCONNECTOR_BODY_MODE_NONE) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_append_response_body_chunk(
        session->transaction, frame->payload, frame->payload_size, &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_RESPONSE_BODY);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    return 1;
}

static int traefik_engine_handle_response_eos(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || !session->response_headers ||
        session->response_eos || frame->payload_size != 0U) {
        return 0;
    }
    if (session->terminal) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_finish_response_body(
        session->transaction, decision, &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    session->response_eos = 1;
    traefik_engine_record_decision(session, decision);
    return 1;
}

static int traefik_engine_handle_response_commit(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    unsigned char headers_sent;
    unsigned char body_started;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || (!session->response_headers && !session->terminal) ||
        frame->payload_size != 2U) {
        return 0;
    }
    headers_sent = frame->payload[0];
    body_started = frame->payload[1];
    if (headers_sent > 1U || body_started > 1U ||
        (session->response_headers_sent && !headers_sent) ||
        (session->response_body_started && !body_started)) {
        return 0;
    }
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    msconnector_runtime_transaction_set_response_commit_state(
        session->transaction, headers_sent != 0U, body_started != 0U);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    session->response_headers_sent = headers_sent != 0U;
    session->response_body_started = body_started != 0U;
    traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_RESPONSE_HEADERS);
    return 1;
}

static int traefik_engine_handle_finish(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    msconnector_error error;
    int success;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->finished ||
        session->destroyed || frame->payload_size != 0U ||
        (!session->terminal && !session->request_eos) ||
        (!session->terminal && session->response_headers && !session->response_eos)) {
        return 0;
    }
    msconnector_error_init(&error);
    if (session->service == NULL ||
        pthread_mutex_lock(&session->service->runtime_lock) != 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    success = msconnector_runtime_transaction_finish(session->transaction, &error);
    (void)pthread_mutex_unlock(&session->service->runtime_lock);
    traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_LOGGING);
    if (!success) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    session->finished = 1;
    return 1;
}

static int traefik_engine_parse_outcome(const traefik_engine_frame *frame,
    uint8_t *action, uint8_t *flags, uint16_t *visible_status)
{
    if (frame == NULL || action == NULL || flags == NULL ||
        visible_status == NULL || frame->payload_size != 4U) {
        return 0;
    }
    *action = frame->payload[0];
    *flags = frame->payload[1];
    *visible_status = traefik_engine_read_u16(frame->payload + 2U);
    return *action <= MSCONNECTOR_DECISION_KIND_UNSUPPORTED &&
        (*flags & ~TRAEFIK_ENGINE_PROTOCOL_OUTCOME_HOST_ACTION_APPLIED) == 0U;
}

static int traefik_engine_handle_outcome(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    uint8_t action;
    uint8_t flags;
    uint16_t visible_status;
    msconnector_error error;

    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || session->destroyed ||
        !session->pending_disruptive || !traefik_engine_parse_outcome(frame,
            &action, &flags, &visible_status)) {
        return 0;
    }
    /* A committed response has no verified abort path; only log-only is real. */
    if (session->pending_phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        (session->response_headers_sent || session->response_body_started)) {
        if (action != MSCONNECTOR_DECISION_KIND_LOG_ONLY || flags != 0U ||
            session->response_status <= 0 ||
            visible_status != (uint16_t)session->response_status) {
            return 0;
        }
        /* The host has already committed this response; preserve that fact in
         * the host-confirmed Common event rather than relabelling it as an
         * ordinary pre-commit deny. */
        session->pending_decision.late_intervention = 1;
        msconnector_error_init(&error);
        if (!traefik_engine_record_host_outcome(session,
                MSCONNECTOR_DECISION_ACTION_LOG_ONLY, (int)visible_status,
                "log_only", &error)) {
            *result_code = traefik_engine_result_for_runtime_error(&error);
            return -1;
        }
        traefik_engine_set_allow_phase(decision,
            MSCONNECTOR_PHASE_RESPONSE_BODY);
        decision->kind = MSCONNECTOR_DECISION_KIND_LOG_ONLY;
        decision->late_intervention = 1;
        session->pending_disruptive = 0;
        return 1;
    }
    if (action != session->pending_action ||
        flags != TRAEFIK_ENGINE_PROTOCOL_OUTCOME_HOST_ACTION_APPLIED ||
        visible_status != session->pending_status) {
        return 0;
    }
    msconnector_error_init(&error);
    if (!traefik_engine_record_host_outcome(session,
            traefik_engine_host_action(action), (int)visible_status,
            "http_status", &error)) {
        *result_code = traefik_engine_result_for_runtime_error(&error);
        return -1;
    }
    *decision = session->pending_decision;
    session->pending_disruptive = 0;
    return 1;
}

static int traefik_engine_handle_destroy(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    if (session == NULL || frame == NULL || decision == NULL ||
        result_code == NULL || !session->begun || !session->finished ||
        session->destroyed || frame->payload_size != 0U) {
        return 0;
    }
    traefik_engine_session_destroy(session);
    if (!session->destroyed) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_INTERNAL;
        return -1;
    }
    traefik_engine_set_allow_phase(decision, MSCONNECTOR_PHASE_LOGGING);
    return 1;
}

static int traefik_engine_dispatch(traefik_engine_session *session,
    const traefik_engine_frame *frame, msconnector_decision *decision,
    uint8_t *result_code)
{
    int handled;
    if (frame == NULL || decision == NULL || result_code == NULL ||
        !traefik_engine_is_command_opcode(frame->opcode)) {
        return 0;
    }
    *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_STATE;
    msconnector_decision_init(decision);
    switch (frame->opcode) {
    case TRAEFIK_ENGINE_PROTOCOL_BEGIN:
        handled = traefik_engine_handle_begin(session, frame, decision, result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_REQUEST_CHUNK:
        handled = traefik_engine_handle_request_chunk(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_REQUEST_EOS:
        handled = traefik_engine_handle_request_eos(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_RESPONSE_HEADERS:
        handled = traefik_engine_handle_response_headers(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_RESPONSE_CHUNK:
        handled = traefik_engine_handle_response_chunk(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_RESPONSE_EOS:
        handled = traefik_engine_handle_response_eos(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_RESPONSE_COMMIT:
        handled = traefik_engine_handle_response_commit(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_FINISH:
        handled = traefik_engine_handle_finish(session, frame, decision, result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_DESTROY:
        handled = traefik_engine_handle_destroy(session, frame, decision,
            result_code);
        break;
    case TRAEFIK_ENGINE_PROTOCOL_OUTCOME:
        handled = traefik_engine_handle_outcome(session, frame, decision,
            result_code);
        break;
    default:
        return 0;
    }
    if (handled > 0) {
        *result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_OK;
    }
    return handled;
}

static void traefik_engine_process_connection(traefik_engine_service *service,
    int socket_fd)
{
    traefik_engine_session session;
    traefik_engine_frame frame;
    int keep_running = 1;

    memset(&session, 0, sizeof(session));
    memset(&frame, 0, sizeof(frame));
    session.service = service;
    while (keep_running) {
        msconnector_decision decision;
        uint8_t result_code = TRAEFIK_ENGINE_PROTOCOL_RESULT_PROTOCOL;
        int received = traefik_engine_receive_frame(socket_fd, &frame);
        int handled;

        if (received != 1) {
            break;
        }
        handled = traefik_engine_dispatch(&session, &frame, &decision,
            &result_code);
        if (handled == 0) {
            result_code = frame.opcode == TRAEFIK_ENGINE_PROTOCOL_BEGIN ||
                !traefik_engine_is_command_opcode(frame.opcode)
                ? TRAEFIK_ENGINE_PROTOCOL_RESULT_PROTOCOL
                : TRAEFIK_ENGINE_PROTOCOL_RESULT_STATE;
            msconnector_decision_init(&decision);
        }
        if (!traefik_engine_send_result(socket_fd, frame.opcode, result_code,
                &session, &decision)) {
            break;
        }
        if (frame.opcode == TRAEFIK_ENGINE_PROTOCOL_DESTROY && handled == 1) {
            keep_running = 0;
        }
        traefik_engine_frame_reset(&frame);
    }
    traefik_engine_frame_reset(&frame);
    traefik_engine_session_destroy(&session);
}

static void *traefik_engine_worker(void *argument)
{
    traefik_engine_worker_arg *worker = argument;
    traefik_engine_service *service;
    int socket_fd;

    if (worker == NULL) {
        return NULL;
    }
    service = worker->service;
    socket_fd = worker->socket_fd;
    free(worker);
    traefik_engine_process_connection(service, socket_fd);
    (void)close(socket_fd);
    if (pthread_mutex_lock(&service->worker_lock) == 0) {
        if (service->worker_count > 0U) {
            --service->worker_count;
        }
        if (service->worker_count == 0U) {
            (void)pthread_cond_broadcast(&service->workers_idle);
        }
        (void)pthread_mutex_unlock(&service->worker_lock);
    }
    return NULL;
}

static int traefik_engine_socket_timeout(int socket_fd)
{
    struct timeval timeout;
    timeout.tv_sec = TRAEFIK_ENGINE_SOCKET_TIMEOUT_SECONDS;
    timeout.tv_usec = 0;
    return setsockopt(socket_fd, SOL_SOCKET, SO_RCVTIMEO, &timeout,
        sizeof(timeout)) == 0;
}

static int traefik_engine_start_worker(traefik_engine_service *service,
    int socket_fd)
{
    traefik_engine_worker_arg *worker;
    pthread_t thread;
    int thread_created;

    if (service == NULL || !traefik_engine_socket_timeout(socket_fd)) {
        return 0;
    }
    worker = calloc(1U, sizeof(*worker));
    if (worker == NULL) {
        return 0;
    }
    worker->service = service;
    worker->socket_fd = socket_fd;
    if (pthread_mutex_lock(&service->worker_lock) != 0) {
        free(worker);
        return 0;
    }
    ++service->worker_count;
    (void)pthread_mutex_unlock(&service->worker_lock);
    thread_created = pthread_create(&thread, NULL, traefik_engine_worker, worker);
    if (thread_created != 0) {
        if (pthread_mutex_lock(&service->worker_lock) == 0) {
            --service->worker_count;
            if (service->worker_count == 0U) {
                (void)pthread_cond_broadcast(&service->workers_idle);
            }
            (void)pthread_mutex_unlock(&service->worker_lock);
        }
        free(worker);
        return 0;
    }
    (void)pthread_detach(thread);
    return 1;
}

static char *traefik_engine_trim(char *text)
{
    char *end;
    while (*text == ' ' || *text == '\t' || *text == '\r' || *text == '\n') {
        ++text;
    }
    end = text + strlen(text);
    while (end > text && (end[-1] == ' ' || end[-1] == '\t' ||
        end[-1] == '\r' || end[-1] == '\n')) {
        --end;
    }
    *end = '\0';
    return text;
}

/* Require explicit streamable body modes; events are host-confirmed via OUTCOME. */
static int traefik_engine_config_supports_service(const char *config_path)
{
    FILE *stream;
    char line[TRAEFIK_ENGINE_CONFIG_LINE_MAX];
    int request_body_mode_seen = 0;
    int response_body_mode_seen = 0;

    if (config_path == NULL || config_path[0] == '\0') {
        return 0;
    }
    stream = fopen(config_path, "r");
    if (stream == NULL) {
        return 0;
    }
    while (fgets(line, sizeof(line), stream) != NULL) {
        char *key;
        const char *value;
        char *separator;
        size_t length = strlen(line);
        if (length == sizeof(line) - 1U && line[length - 1U] != '\n') {
            (void)fclose(stream);
            return 0;
        }
        key = traefik_engine_trim(line);
        if (*key == '\0' || *key == '#') {
            continue;
        }
        separator = strchr(key, '=');
        if (separator == NULL) {
            continue;
        }
        *separator = '\0';
        value = traefik_engine_trim(separator + 1);
        key = traefik_engine_trim(key);
        if (strcmp(key, "request_body_mode") == 0) {
            if (strcmp(value, "none") != 0 && strcmp(value, "streaming") != 0) {
                (void)fclose(stream);
                return 0;
            }
            request_body_mode_seen = 1;
        }
        if (strcmp(key, "response_body_mode") == 0) {
            if (strcmp(value, "none") != 0 && strcmp(value, "streaming") != 0) {
                (void)fclose(stream);
                return 0;
            }
            response_body_mode_seen = 1;
        }
    }
    if (ferror(stream)) {
        (void)fclose(stream);
        return 0;
    }
    (void)fclose(stream);
    return request_body_mode_seen && response_body_mode_seen;
}

static int traefik_engine_check_config(const char *config_path)
{
    char error[256];
    if (!traefik_engine_config_supports_service(config_path)) {
        return 0;
    }
    memset(error, 0, sizeof(error));
    return msconnector_runtime_config_check("traefik", config_path, error,
        sizeof(error));
}

static int traefik_engine_path_is_absolute(const char *path)
{
    return path != NULL && path[0] == '/';
}

static int traefik_engine_directory_is_current_user_private(
    const struct stat *path_stat)
{
    return path_stat != NULL && S_ISDIR(path_stat->st_mode) &&
        path_stat->st_uid == geteuid() && (path_stat->st_mode & 07777) == 0700;
}

static int traefik_engine_parent_protects_child_from_cross_uid_replacement(
    const struct stat *parent_stat, const struct stat *child_stat)
{
    if (parent_stat == NULL || child_stat == NULL ||
        !S_ISDIR(parent_stat->st_mode)) {
        return 0;
    }
    if ((parent_stat->st_mode & (S_IWGRP | S_IWOTH)) == 0) {
        return 1;
    }
    return (parent_stat->st_mode & S_ISVTX) != 0 &&
        child_stat->st_uid == geteuid();
}

static int traefik_engine_private_directory_ancestors_are_safe(const char *path)
{
    char child_path[PATH_MAX];
    char *separator;
    struct stat child_stat;
    struct stat parent_stat;
    size_t path_size;

    if (!traefik_engine_path_is_absolute(path)) {
        return 0;
    }
    path_size = strlen(path);
    if (path_size == 0U || path_size >= sizeof(child_path)) {
        return 0;
    }
    memcpy(child_path, path, path_size + 1U);
    if (lstat(child_path, &child_stat) != 0 || !S_ISDIR(child_stat.st_mode)) {
        return 0;
    }
    while (strcmp(child_path, "/") != 0) {
        separator = strrchr(child_path, '/');
        if (separator == NULL) {
            return 0;
        }
        if (separator == child_path) {
            child_path[1] = '\0';
        } else {
            *separator = '\0';
        }
        if (lstat(child_path, &parent_stat) != 0 ||
            !traefik_engine_parent_protects_child_from_cross_uid_replacement(
                &parent_stat, &child_stat)) {
            return 0;
        }
        child_stat = parent_stat;
    }
    return 1;
}

static int traefik_engine_private_directory_is_safe(const char *path)
{
    char canonical[PATH_MAX];
    struct stat path_stat;

    if (!traefik_engine_path_is_absolute(path) || realpath(path, canonical) == NULL ||
        strcmp(path, canonical) != 0 || lstat(path, &path_stat) != 0 ||
        !traefik_engine_directory_is_current_user_private(&path_stat)) {
        return 0;
    }
    return traefik_engine_private_directory_ancestors_are_safe(path);
}

static int traefik_engine_socket_parent_is_safe(const char *socket_path)
{
    char parent[sizeof(((struct sockaddr_un *)0)->sun_path)];
    char *separator;
    size_t path_size;

    if (!traefik_engine_path_is_absolute(socket_path)) {
        return 0;
    }
    path_size = strlen(socket_path);
    if (path_size == 0U || path_size >= sizeof(parent)) {
        return 0;
    }
    memcpy(parent, socket_path, path_size + 1U);
    separator = strrchr(parent, '/');
    if (separator == NULL || separator == parent) {
        return 0;
    }
    *separator = '\0';
    return traefik_engine_private_directory_is_safe(parent);
}

/*
 * Verify that a connection made through socket_path reaches socket_fd itself.
 *
 * bind(2) only reports that the listener owns its descriptor; it does not
 * atomically prove that a subsequent pathname lookup still reaches that
 * descriptor.  Before publishing the listener, compare the pathname identity
 * on both sides of a local probe connection and require the accepted peer to
 * be this process.  That makes a replacement between bind() and identity
 * capture fail closed instead of recording the replacement as service-owned.
 */
#if defined(__linux__)
static int traefik_engine_connect_self_probe(int client, const char *socket_path)
{
    struct sockaddr_un address;
    struct pollfd probe;
    socklen_t connection_error_size;
    int connection_error;
    int flags;
    size_t path_size;

    if (client < 0 || !traefik_engine_path_is_absolute(socket_path)) {
        return 0;
    }
    path_size = strlen(socket_path);
    if (path_size == 0U || path_size >= sizeof(address.sun_path)) {
        return 0;
    }
    flags = fcntl(client, F_GETFL, 0);
    if (flags < 0 || fcntl(client, F_SETFL, flags | O_NONBLOCK) != 0) {
        return 0;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, socket_path, path_size + 1U);
    if (connect(client, (const struct sockaddr *)&address, sizeof(address)) == 0) {
        return 1;
    }
    if (errno != EINPROGRESS) {
        return 0;
    }
    memset(&probe, 0, sizeof(probe));
    probe.fd = client;
    probe.events = POLLOUT;
    if (poll(&probe, 1U, TRAEFIK_ENGINE_ACCEPT_POLL_MILLISECONDS) <= 0) {
        return 0;
    }
    connection_error = 0;
    connection_error_size = sizeof(connection_error);
    return getsockopt(client, SOL_SOCKET, SO_ERROR, &connection_error,
        &connection_error_size) == 0 && connection_error_size ==
        sizeof(connection_error) && connection_error == 0;
}

static int traefik_engine_accepts_self_probe(int socket_fd)
{
    struct ucred credentials;
    socklen_t credentials_size;
    int accepted;
    size_t accepted_count = 0U;

    while (accepted_count <= TRAEFIK_ENGINE_LISTEN_BACKLOG) {
        accepted = accept(socket_fd, NULL, NULL);
        if (accepted < 0) {
            if (errno == EINTR) {
                continue;
            }
            return 0;
        }
        ++accepted_count;
        memset(&credentials, 0, sizeof(credentials));
        credentials_size = sizeof(credentials);
        if (getsockopt(accepted, SOL_SOCKET, SO_PEERCRED, &credentials,
                &credentials_size) == 0 && credentials_size ==
                sizeof(credentials) && credentials.pid == getpid() &&
            credentials.uid == geteuid()) {
            (void)close(accepted);
            return 1;
        }
        (void)close(accepted);
    }
    return 0;
}
#endif

static int traefik_engine_listener_accepts_self_probe(int socket_fd,
    const char *socket_path)
{
#if defined(__linux__)
    int client;
    int result;

    if (socket_fd < 0 || !traefik_engine_path_is_absolute(socket_path)) {
        return 0;
    }
    client = socket(AF_UNIX, SOCK_STREAM, 0);
    if (client < 0) {
        return 0;
    }
    result = traefik_engine_connect_self_probe(client, socket_path) &&
        traefik_engine_accepts_self_probe(socket_fd);
    (void)close(client);
    return result;
#else
    (void)socket_fd;
    (void)socket_path;
    return 0;
#endif
}

static int traefik_engine_capture_bound_socket_identity(int socket_fd,
    const char *socket_path, traefik_engine_socket_identity *identity)
{
    struct stat initial;
    struct stat path;

    if (socket_fd < 0 || socket_path == NULL || identity == NULL ||
        lstat(socket_path, &initial) != 0 || !S_ISSOCK(initial.st_mode) ||
        initial.st_uid != geteuid() ||
        !traefik_engine_listener_accepts_self_probe(socket_fd, socket_path) ||
        (traefik_engine_listener_post_probe_hook != NULL &&
            !traefik_engine_listener_post_probe_hook(socket_path)) ||
        lstat(socket_path, &path) != 0 || !S_ISSOCK(path.st_mode) ||
        path.st_uid != geteuid() || path.st_dev != initial.st_dev ||
        path.st_ino != initial.st_ino) {
        return 0;
    }
    identity->device = path.st_dev;
    identity->inode = path.st_ino;
    identity->owner = path.st_uid;
    identity->valid = 1;
    return 1;
}

static int traefik_engine_remove_owned_socket(const char *socket_path,
    const traefik_engine_socket_identity *identity)
{
    struct stat path;

    if (socket_path == NULL || identity == NULL || !identity->valid) {
        return 0;
    }
    if (lstat(socket_path, &path) != 0) {
        return errno == ENOENT;
    }
    if (!S_ISSOCK(path.st_mode) || path.st_dev != identity->device ||
        path.st_ino != identity->inode || path.st_uid != identity->owner) {
        return 0;
    }
    return unlink(socket_path) == 0 || errno == ENOENT;
}

static int traefik_engine_create_listener(const char *socket_path,
    traefik_engine_socket_identity *identity)
{
    struct sockaddr_un address;
    struct stat existing;
    int socket_fd;
    size_t path_size;
    int flags;

    if (!traefik_engine_path_is_absolute(socket_path) || identity == NULL ||
        !traefik_engine_socket_parent_is_safe(socket_path)) {
        return -1;
    }
    memset(identity, 0, sizeof(*identity));
    path_size = strlen(socket_path);
    if (path_size == 0U || path_size >= sizeof(address.sun_path) ||
        lstat(socket_path, &existing) == 0 || errno != ENOENT) {
        return -1;
    }
    if (traefik_engine_listener_pre_bind_hook != NULL &&
        !traefik_engine_listener_pre_bind_hook(socket_path)) {
        return -1;
    }
    socket_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        return -1;
    }
    flags = fcntl(socket_fd, F_GETFL, 0);
    if (flags < 0 || fcntl(socket_fd, F_SETFL, flags | O_NONBLOCK) != 0) {
        (void)close(socket_fd);
        return -1;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, socket_path, path_size + 1U);
    if (bind(socket_fd, (const struct sockaddr *)&address, sizeof(address)) != 0) {
        (void)close(socket_fd);
        return -1;
    }
    /* The socket pathname is reachable only through the current-user-owned
     * exact-0700 parent verified above. Do not use a process-global umask or
     * path-based chmod: neither adds cross-UID access control at this boundary. */
    if ((traefik_engine_listener_post_bind_hook != NULL &&
            !traefik_engine_listener_post_bind_hook(socket_path)) ||
        listen(socket_fd, TRAEFIK_ENGINE_LISTEN_BACKLOG) != 0 ||
        !traefik_engine_capture_bound_socket_identity(socket_fd, socket_path,
            identity)) {
        (void)close(socket_fd);
        (void)traefik_engine_remove_owned_socket(socket_path, identity);
        return -1;
    }
    return socket_fd;
}

static void traefik_engine_wait_for_workers(traefik_engine_service *service)
{
    if (service == NULL || pthread_mutex_lock(&service->worker_lock) != 0) {
        return;
    }
    while (service->worker_count > 0U) {
        (void)pthread_cond_wait(&service->workers_idle, &service->worker_lock);
    }
    (void)pthread_mutex_unlock(&service->worker_lock);
}

static int traefik_engine_serve(const char *config_path, const char *socket_path,
    size_t max_connections)
{
    traefik_engine_service service;
    char error[256];
    int listener = -1;
    size_t accepted_connections = 0U;
    int status = 1;
    traefik_engine_socket_identity listener_identity;
    struct sigaction action;
    const char *failure_stage = "initialization";

    memset(&service, 0, sizeof(service));
    memset(error, 0, sizeof(error));
    memset(&listener_identity, 0, sizeof(listener_identity));
    if (!traefik_engine_check_config(config_path) ||
        !traefik_engine_path_is_absolute(socket_path) ||
        pthread_mutex_init(&service.runtime_lock, NULL) != 0 ||
        pthread_mutex_init(&service.worker_lock, NULL) != 0 ||
        pthread_cond_init(&service.workers_idle, NULL) != 0) {
        return 1;
    }
    if (!msconnector_runtime_create("traefik", config_path, &service.runtime,
            error, sizeof(error))) {
        failure_stage = "runtime_create";
        goto cleanup;
    }
    if (!msconnector_runtime_set_event_integration_mode(service.runtime,
            "native-traefik-middleware")) {
        failure_stage = "integration_mode";
        goto cleanup;
    }
    service.request_body_mode = msconnector_runtime_request_body_mode(
        service.runtime);
    service.response_body_mode = msconnector_runtime_response_body_mode(
        service.runtime);
    memset(&action, 0, sizeof(action));
    action.sa_handler = traefik_engine_stop_handler;
    (void)sigemptyset(&action.sa_mask);
    if (sigaction(SIGTERM, &action, NULL) != 0 ||
        sigaction(SIGINT, &action, NULL) != 0) {
        failure_stage = "signal_setup";
        goto cleanup;
    }
    /* create_listener requires a private 0700 parent before bind(), so no
     * process-global umask state is needed for the listener boundary. */
    listener = traefik_engine_create_listener(socket_path, &listener_identity);
    if (listener < 0) {
        failure_stage = "socket_listener";
        goto cleanup;
    }
    (void)printf("traefik_engine_service=ready\n");
    (void)printf("socket=%s\n", socket_path);
    (void)fflush(stdout);
    while (!traefik_engine_stop_requested &&
        (max_connections == 0U || accepted_connections < max_connections)) {
        struct pollfd descriptor;
        int polled;
        int client;

        descriptor.fd = listener;
        descriptor.events = POLLIN;
        descriptor.revents = 0;
        polled = poll(&descriptor, 1U, TRAEFIK_ENGINE_ACCEPT_POLL_MILLISECONDS);
        if (polled < 0) {
            if (errno == EINTR) {
                continue;
            }
            failure_stage = "listener_poll";
            goto cleanup;
        }
        if (polled == 0) {
            continue;
        }
        client = accept(listener, NULL, NULL);
        if (client < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK || errno == EINTR) {
                continue;
            }
            failure_stage = "listener_accept";
            goto cleanup;
        }
        if (!traefik_engine_start_worker(&service, client)) {
            (void)close(client);
            failure_stage = "worker_start";
            goto cleanup;
        }
        ++accepted_connections;
    }
    status = 0;

cleanup:
    if (listener >= 0) {
        (void)close(listener);
    }
    traefik_engine_wait_for_workers(&service);
    if (listener_identity.valid &&
        !traefik_engine_remove_owned_socket(socket_path, &listener_identity)) {
        status = 1;
        failure_stage = "socket_cleanup";
    }
    msconnector_runtime_destroy(&service.runtime);
    (void)pthread_cond_destroy(&service.workers_idle);
    (void)pthread_mutex_destroy(&service.worker_lock);
    (void)pthread_mutex_destroy(&service.runtime_lock);
    if (status != 0) {
        (void)fprintf(stderr, "traefik_engine_service_failure_stage=%s\n",
            failure_stage);
    }
    return status;
}

static int traefik_engine_self_test_append_u16(unsigned char *buffer,
    size_t size, size_t *offset, uint16_t value)
{
    if (buffer == NULL || offset == NULL || *offset > size ||
        size - *offset < 2U) {
        return 0;
    }
    traefik_engine_write_u16(buffer + *offset, value);
    *offset += 2U;
    return 1;
}

static int traefik_engine_self_test_append_text(unsigned char *buffer,
    size_t size, size_t *offset, const char *value)
{
    size_t value_size = value == NULL ? 0U : strlen(value);
    if (value_size > UINT16_MAX || !traefik_engine_self_test_append_u16(buffer,
            size, offset, (uint16_t)value_size) || *offset > size ||
        size - *offset < value_size) {
        return 0;
    }
    if (value_size > 0U) {
        memcpy(buffer + *offset, value, value_size);
        *offset += value_size;
    }
    return 1;
}

static int traefik_engine_protocol_self_test(void)
{
    unsigned char begin[256];
    traefik_engine_request_input input;
    traefik_engine_frame frame;
    uint8_t action;
    uint8_t flags;
    uint16_t visible_status;
    size_t offset = 0U;
    int passed = 1;

    memset(begin, 0, sizeof(begin));
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "GET");
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "/health");
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "HTTP/1.1");
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "example.test");
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "127.0.0.1");
    passed &= traefik_engine_self_test_append_u16(begin, sizeof(begin),
        &offset, 12345U);
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "127.0.0.1");
    passed &= traefik_engine_self_test_append_u16(begin, sizeof(begin),
        &offset, 80U);
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "request-1");
    passed &= traefik_engine_self_test_append_u16(begin, sizeof(begin),
        &offset, 1U);
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "host");
    passed &= traefik_engine_self_test_append_text(begin, sizeof(begin),
        &offset, "example.test");
    if (!passed || !traefik_engine_parse_begin(begin, offset, &input)) {
        return 1;
    }
    passed = input.request.header_count == 1U &&
        strcmp(input.request.method, "GET") == 0 &&
        strcmp(input.request.headers[0].name, "host") == 0;
    traefik_engine_request_input_free(&input);
    if (!passed || traefik_engine_parse_begin(begin, offset - 1U, &input)) {
        return 1;
    }
    memset(&frame, 0, sizeof(frame));
    frame.opcode = TRAEFIK_ENGINE_PROTOCOL_OUTCOME;
    frame.payload = begin;
    frame.payload_size = 4U;
    frame.payload[0] = MSCONNECTOR_DECISION_KIND_DENY;
    frame.payload[1] = 2U;
    frame.payload[2] = 0U;
    frame.payload[3] = 0U;
    if (traefik_engine_parse_outcome(&frame, &action, &flags, &visible_status)) {
        return 1;
    }
    frame.payload[1] = 0U;
    if (!traefik_engine_parse_outcome(&frame, &action, &flags, &visible_status) ||
        action != MSCONNECTOR_DECISION_KIND_DENY || flags != 0U ||
        visible_status != 0U) {
        return 1;
    }
    frame.payload[0] = MSCONNECTOR_DECISION_KIND_LOG_ONLY;
    frame.payload[1] = 0U;
    frame.payload[2] = 0U;
    frame.payload[3] = 200U;
    if (!traefik_engine_parse_outcome(&frame, &action, &flags, &visible_status) ||
        action != MSCONNECTOR_DECISION_KIND_LOG_ONLY || flags != 0U ||
        visible_status != 200U) {
        return 1;
    }
    (void)printf("traefik_engine_protocol_self_test=pass\n");
    return 0;
}

static int traefik_engine_self_test_bind_foreign_socket(const char *socket_path)
{
    struct sockaddr_un address;
    int socket_fd;
    size_t path_size;

    if (!traefik_engine_path_is_absolute(socket_path)) {
        return 0;
    }
    path_size = strlen(socket_path);
    if (path_size == 0U || path_size >= sizeof(address.sun_path)) {
        return 0;
    }
    socket_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (socket_fd < 0) {
        return 0;
    }
    memset(&address, 0, sizeof(address));
    address.sun_family = AF_UNIX;
    memcpy(address.sun_path, socket_path, path_size + 1U);
    if (bind(socket_fd, (const struct sockaddr *)&address, sizeof(address)) != 0) {
        (void)close(socket_fd);
        return 0;
    }
    (void)close(socket_fd);
    return 1;
}

static int traefik_engine_self_test_pre_bind_foreign_socket(const char *socket_path)
{
    return traefik_engine_self_test_bind_foreign_socket(socket_path);
}

static int traefik_engine_self_test_post_bind_foreign_socket(const char *socket_path)
{
    if (unlink(socket_path) != 0) {
        return 0;
    }
    return traefik_engine_self_test_bind_foreign_socket(socket_path);
}

static int traefik_engine_socket_ownership_self_test(const char *socket_parent)
{
    char directory[sizeof(((struct sockaddr_un *)0)->sun_path)];
    char socket_path[sizeof(directory) + 16U];
    traefik_engine_socket_identity identity;
    struct stat path;
    int listener = -1;
    int result = 1;
    int written;

    memset(directory, 0, sizeof(directory));
    memset(socket_path, 0, sizeof(socket_path));
    memset(&identity, 0, sizeof(identity));
    if (!traefik_engine_private_directory_is_safe(socket_parent)) {
        return 1;
    }
    written = snprintf(directory, sizeof(directory),
        "%s/mct-engine-ownership.XXXXXX", socket_parent);
    if (written < 0 || (size_t)written >= sizeof(directory) ||
        mkdtemp(directory) == NULL || snprintf(socket_path, sizeof(socket_path),
            "%s/engine.sock", directory) < 0 ||
        strlen(socket_path) >= sizeof(socket_path)) {
        goto cleanup;
    }
    traefik_engine_listener_pre_bind_hook =
        traefik_engine_self_test_pre_bind_foreign_socket;
    listener = traefik_engine_create_listener(socket_path, &identity);
    traefik_engine_listener_pre_bind_hook = NULL;
    if (listener >= 0 || lstat(socket_path, &path) != 0 ||
        !S_ISSOCK(path.st_mode) || unlink(socket_path) != 0) {
        goto cleanup;
    }
    traefik_engine_listener_post_bind_hook =
        traefik_engine_self_test_post_bind_foreign_socket;
    listener = traefik_engine_create_listener(socket_path, &identity);
    traefik_engine_listener_post_bind_hook = NULL;
    if (listener >= 0 || lstat(socket_path, &path) != 0 ||
        !S_ISSOCK(path.st_mode) || unlink(socket_path) != 0) {
        goto cleanup;
    }
    traefik_engine_listener_post_probe_hook =
        traefik_engine_self_test_post_bind_foreign_socket;
    listener = traefik_engine_create_listener(socket_path, &identity);
    traefik_engine_listener_post_probe_hook = NULL;
    if (listener >= 0 || lstat(socket_path, &path) != 0 ||
        !S_ISSOCK(path.st_mode) || unlink(socket_path) != 0) {
        goto cleanup;
    }
    listener = traefik_engine_create_listener(socket_path, &identity);
    if (listener < 0 || close(listener) != 0) {
        listener = -1;
        goto cleanup;
    }
    listener = -1;
    if (unlink(socket_path) != 0 ||
        !traefik_engine_self_test_bind_foreign_socket(socket_path) ||
        traefik_engine_remove_owned_socket(socket_path, &identity) ||
        lstat(socket_path, &path) != 0 || !S_ISSOCK(path.st_mode)) {
        goto cleanup;
    }
    result = 0;

cleanup:
    traefik_engine_listener_pre_bind_hook = NULL;
    traefik_engine_listener_post_bind_hook = NULL;
    traefik_engine_listener_post_probe_hook = NULL;
    if (listener >= 0) {
        (void)close(listener);
    }
    if (socket_path[0] != '\0') {
        (void)unlink(socket_path);
    }
    if (directory[0] != '\0') {
        (void)rmdir(directory);
    }
    if (result == 0) {
        (void)printf("traefik_engine_socket_ownership_self_test=pass\n");
    }
    return result;
}

static int traefik_engine_parse_positive_size(const char *value, size_t *out)
{
    char *end = NULL;
    unsigned long parsed;
    if (value == NULL || value[0] == '\0' || out == NULL) {
        return 0;
    }
    errno = 0;
    parsed = strtoul(value, &end, 10);
    if (errno != 0 || end == value || *end != '\0' || parsed == 0UL ||
        parsed > SIZE_MAX) {
        return 0;
    }
    *out = (size_t)parsed;
    return 1;
}

static void traefik_engine_usage(const char *program)
{
    (void)fprintf(stderr,
        "usage: %s --self-test --socket-parent PATH | --check-config --config PATH | "
        "--serve --config PATH --socket PATH [--max-connections N]\n",
        program == NULL ? "traefik-engine-service" : program);
}

typedef struct traefik_engine_cli_options {
    const char *config_path;
    const char *socket_path;
    const char *self_test_socket_parent;
    size_t max_connections;
    int serve;
    int check_config;
    int self_test;
} traefik_engine_cli_options;

static int traefik_engine_consume_option_value(int argc, char **argv,
    int *index, const char **value)
{
    if (index == NULL || value == NULL || *index + 1 >= argc) {
        return 0;
    }
    ++*index;
    *value = argv[*index];
    return 1;
}

static int traefik_engine_parse_cli(int argc, char **argv,
    traefik_engine_cli_options *options)
{
    int index;

    if (argv == NULL || options == NULL) {
        return 0;
    }
    for (index = 1; index < argc; ++index) {
        if (strcmp(argv[index], "--self-test") == 0) {
            options->self_test = 1;
        } else if (strcmp(argv[index], "--serve") == 0) {
            options->serve = 1;
        } else if (strcmp(argv[index], "--check-config") == 0) {
            options->check_config = 1;
        } else if (strcmp(argv[index], "--config") == 0) {
            if (!traefik_engine_consume_option_value(argc, argv, &index,
                    &options->config_path)) {
                return 0;
            }
        } else if (strcmp(argv[index], "--socket") == 0) {
            if (!traefik_engine_consume_option_value(argc, argv, &index,
                    &options->socket_path)) {
                return 0;
            }
        } else if (strcmp(argv[index], "--socket-parent") == 0) {
            if (!traefik_engine_consume_option_value(argc, argv, &index,
                    &options->self_test_socket_parent)) {
                return 0;
            }
        } else if (strcmp(argv[index], "--max-connections") == 0) {
            if (index + 1 >= argc || !traefik_engine_parse_positive_size(
                    argv[++index], &options->max_connections)) {
                return 0;
            }
        } else {
            return 0;
        }
    }
    return 1;
}

static int traefik_engine_dispatch_cli(const char *program,
    const traefik_engine_cli_options *options)
{
    if (options == NULL) {
        return 2;
    }
    if (options->self_test) {
        if (options->serve || options->check_config || options->config_path != NULL ||
            options->socket_path != NULL || options->self_test_socket_parent == NULL) {
            traefik_engine_usage(program);
            return 2;
        }
        return traefik_engine_protocol_self_test() == 0 &&
            traefik_engine_socket_ownership_self_test(
                options->self_test_socket_parent) == 0 ? 0 : 1;
    }
    if (options->check_config && !options->serve && options->config_path != NULL &&
        options->socket_path == NULL && options->self_test_socket_parent == NULL) {
        if (!traefik_engine_check_config(options->config_path)) {
            (void)fprintf(stderr, "traefik_engine_config_check=fail\n");
            return 1;
        }
        (void)printf("traefik_engine_config_check=pass\n");
        return 0;
    }
    if (options->serve && !options->check_config && options->config_path != NULL &&
        options->socket_path != NULL && options->self_test_socket_parent == NULL) {
        if (traefik_engine_serve(options->config_path, options->socket_path,
                options->max_connections) != 0) {
            (void)fprintf(stderr, "traefik_engine_service=fail\n");
            return 1;
        }
        return 0;
    }
    traefik_engine_usage(program);
    return 2;
}

int main(int argc, char **argv)
{
    traefik_engine_cli_options options;

    memset(&options, 0, sizeof(options));
    if (!traefik_engine_parse_cli(argc, argv, &options)) {
        traefik_engine_usage(argc > 0 ? argv[0] : NULL);
        return 2;
    }
    return traefik_engine_dispatch_cli(argc > 0 ? argv[0] : NULL, &options);
}
