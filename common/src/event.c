#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include "msconnector/json_escape.h"
#include "msconnector/transaction_state.h"
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

#define EVENT_TEXT_SIZE 256U
#define EVENT_JSON_TRUE "true"
#define EVENT_JSON_FALSE "false"

static const char *json_bool(int value) {
    return value ? EVENT_JSON_TRUE : EVENT_JSON_FALSE;
}


enum msconnector_event_json_text_index {
    EVENT_JSON_TIMESTAMP = 0,
    EVENT_JSON_LEVEL,
    EVENT_JSON_MESSAGE_ID,
    EVENT_JSON_MESSAGE,
    EVENT_JSON_EVENT_NAME,
    EVENT_JSON_CONNECTOR,
    EVENT_JSON_INTEGRATION_MODE,
    EVENT_JSON_RUN_ID,
    EVENT_JSON_TRANSPORT_CASE_ID,
    EVENT_JSON_TRANSACTION_ID,
    EVENT_JSON_PHASE,
    EVENT_JSON_STATUS,
    EVENT_JSON_ACTION,
    EVENT_JSON_REQUESTED_ACTION,
    EVENT_JSON_ACTUAL_ACTION,
    EVENT_JSON_TRANSPORT_RESULT,
    EVENT_JSON_REQUESTED_PROTOCOL,
    EVENT_JSON_DOWNSTREAM_PROTOCOL,
    EVENT_JSON_UPSTREAM_PROTOCOL,
    EVENT_JSON_NEGOTIATED_PROTOCOL,
    EVENT_JSON_TRANSPORT,
    EVENT_JSON_ALPN,
    EVENT_JSON_STREAM_ID,
    EVENT_JSON_CONNECTION_ID,
    EVENT_JSON_QUIC_VERSION,
    EVENT_JSON_STREAM_RESET_CODE,
    EVENT_JSON_HTTP_REASON_PHRASE,
    EVENT_JSON_HTTP_DEFAULT_MESSAGE,
    EVENT_JSON_RULE_ID,
    EVENT_JSON_REASON,
    EVENT_JSON_METHOD,
    EVENT_JSON_URI,
    EVENT_JSON_CLIENT_IP,
    EVENT_JSON_CONTENT_TYPE,
    EVENT_JSON_BODY_LIMIT_OUTCOME,
    EVENT_JSON_LATE_INTERVENTION_MODE,
    EVENT_JSON_TEXT_COUNT
};

enum msconnector_event_json_status_index {
    EVENT_JSON_HTTP_STATUS = 0,
    EVENT_JSON_ORIGINAL_HTTP_STATUS,
    EVENT_JSON_VISIBLE_HTTP_STATUS,
    EVENT_JSON_STATUS_COUNT
};

enum msconnector_event_json_flag_index {
    EVENT_JSON_LATE_INTERVENTION = 0,
    EVENT_JSON_RESPONSE_STARTED,
    EVENT_JSON_RESPONSE_COMMITTED,
    EVENT_JSON_HEADERS_SENT,
    EVENT_JSON_BODY_STARTED,
    EVENT_JSON_BODY_TRUNCATED,
    EVENT_JSON_CONNECTION_ABORTED,
    EVENT_JSON_CLIENT_DISCONNECTED,
    EVENT_JSON_UPSTREAM_DISCONNECTED,
    EVENT_JSON_CANCELLED,
    EVENT_JSON_EOS_SEEN,
    EVENT_JSON_REDACTED,
    EVENT_JSON_TRUNCATED,
    EVENT_JSON_CONNECTION_REUSED,
    EVENT_JSON_QUIC_CONNECTION_ID_PRESENT,
    EVENT_JSON_FALLBACK_USED,
    EVENT_JSON_STREAM_RESET,
    EVENT_JSON_FLAG_COUNT
};

typedef struct msconnector_event_json_parts {
    const char *text[EVENT_JSON_TEXT_COUNT];
    int statuses[EVENT_JSON_STATUS_COUNT];
    const char *flags[EVENT_JSON_FLAG_COUNT];
    const char *body_limit_outcome_json;
    const char *late_intervention_mode_json;
    const char *provenance_json;
    unsigned long sequence;
    uint64_t body_bytes_seen;
    uint64_t body_bytes_inspected;
    uint64_t previous_hash;
    uint64_t event_hash;
} msconnector_event_json_parts;

static int format_event_json(
    char *dst,
    size_t dst_size,
    const msconnector_event_json_parts *parts) {
    return snprintf(
        dst,
        dst_size,
        "{\"timestamp\":\"%s\",\"level\":\"%s\",\"message_id\":\"%s\",\"message\":\"%s\",\"event\":\"%s\",\"connector\":\"%s\",\"integration_mode\":\"%s\"%s,\"transaction_id\":\"%s\",\"phase\":\"%s\",\"status\":\"%s\",\"action\":\"%s\",\"requested_action\":\"%s\",\"actual_action\":\"%s\",\"http_status\":%d,\"original_http_status\":%d,\"visible_http_status\":%d,\"transport_result\":\"%s\",\"http_reason_phrase\":\"%s\",\"http_default_message\":\"%s\",\"rule_id\":\"%s\",\"reason\":\"%s\",\"method\":\"%s\",\"uri\":\"%s\",\"client_ip\":\"%s\",\"content_type\":\"%s\",\"body_bytes_seen\":%" PRIu64 ",\"body_bytes_inspected\":%" PRIu64 "%s,\"late_intervention\":%s%s,\"response_started\":%s,\"response_committed\":%s,\"headers_sent\":%s,\"body_started\":%s,\"body_truncated\":%s,\"connection_aborted\":%s,\"client_disconnected\":%s,\"upstream_disconnected\":%s,\"cancelled\":%s,\"eos_seen\":%s,\"redacted\":%s,\"truncated\":%s,\"sequence\":%lu,\"previous_event_hash\":%" PRIu64 ",\"event_hash\":%" PRIu64 "}",
        parts->text[EVENT_JSON_TIMESTAMP],
        parts->text[EVENT_JSON_LEVEL],
        parts->text[EVENT_JSON_MESSAGE_ID],
        parts->text[EVENT_JSON_MESSAGE],
        parts->text[EVENT_JSON_EVENT_NAME],
        parts->text[EVENT_JSON_CONNECTOR],
        parts->text[EVENT_JSON_INTEGRATION_MODE],
        parts->provenance_json,
        parts->text[EVENT_JSON_TRANSACTION_ID],
        parts->text[EVENT_JSON_PHASE],
        parts->text[EVENT_JSON_STATUS],
        parts->text[EVENT_JSON_ACTION],
        parts->text[EVENT_JSON_REQUESTED_ACTION],
        parts->text[EVENT_JSON_ACTUAL_ACTION],
        parts->statuses[EVENT_JSON_HTTP_STATUS],
        parts->statuses[EVENT_JSON_ORIGINAL_HTTP_STATUS],
        parts->statuses[EVENT_JSON_VISIBLE_HTTP_STATUS],
        parts->text[EVENT_JSON_TRANSPORT_RESULT],
        parts->text[EVENT_JSON_HTTP_REASON_PHRASE],
        parts->text[EVENT_JSON_HTTP_DEFAULT_MESSAGE],
        parts->text[EVENT_JSON_RULE_ID],
        parts->text[EVENT_JSON_REASON],
        parts->text[EVENT_JSON_METHOD],
        parts->text[EVENT_JSON_URI],
        parts->text[EVENT_JSON_CLIENT_IP],
        parts->text[EVENT_JSON_CONTENT_TYPE],
        parts->body_bytes_seen,
        parts->body_bytes_inspected,
        parts->body_limit_outcome_json,
        parts->flags[EVENT_JSON_LATE_INTERVENTION],
        parts->late_intervention_mode_json,
        parts->flags[EVENT_JSON_RESPONSE_STARTED],
        parts->flags[EVENT_JSON_RESPONSE_COMMITTED],
        parts->flags[EVENT_JSON_HEADERS_SENT],
        parts->flags[EVENT_JSON_BODY_STARTED],
        parts->flags[EVENT_JSON_BODY_TRUNCATED],
        parts->flags[EVENT_JSON_CONNECTION_ABORTED],
        parts->flags[EVENT_JSON_CLIENT_DISCONNECTED],
        parts->flags[EVENT_JSON_UPSTREAM_DISCONNECTED],
        parts->flags[EVENT_JSON_CANCELLED],
        parts->flags[EVENT_JSON_EOS_SEEN],
        parts->flags[EVENT_JSON_REDACTED],
        parts->flags[EVENT_JSON_TRUNCATED],
        parts->sequence,
        parts->previous_hash,
        parts->event_hash);
}


static void escape_field(const char *src, char *dst, size_t dst_size, int *truncated) {
    const size_t needed = msconnector_json_escape(src, dst, dst_size);
    if ((dst_size == 0 || needed >= dst_size) && truncated != 0) {
        *truncated = 1;
    }
}

static int append_protocol_string(
    char *dst,
    size_t dst_size,
    size_t *offset,
    const char *name,
    const char *value) {
    int written;
    if (dst == NULL || offset == NULL || name == NULL || value == NULL || value[0] == '\0') {
        return 1;
    }
    if (*offset >= dst_size) {
        return 0;
    }
    written = snprintf(dst + *offset, dst_size - *offset, ",\"%s\":\"%s\"", name, value);
    if (written < 0 || (size_t)written >= dst_size - *offset) {
        return 0;
    }
    *offset += (size_t)written;
    return 1;
}

static int append_protocol_bool(
    char *dst,
    size_t dst_size,
    size_t *offset,
    const char *name,
    int value) {
    int written;
    if (dst == NULL || offset == NULL || name == NULL || *offset >= dst_size) {
        return 0;
    }
    written = snprintf(dst + *offset, dst_size - *offset, ",\"%s\":%s", name, json_bool(value));
    if (written < 0 || (size_t)written >= dst_size - *offset) {
        return 0;
    }
    *offset += (size_t)written;
    return 1;
}

static int is_nonreversible_quic_connection_id(const char *value) {
    size_t length;
    if (value == NULL || strncmp(value, "sha256:", 7U) != 0) {
        return 0;
    }
    length = strlen(value + 7U);
    if (length < 16U || length > 64U) {
        return 0;
    }
    for (size_t index = 7U; value[index] != '\0'; ++index) {
        if (!((value[index] >= '0' && value[index] <= '9') ||
                (value[index] >= 'a' && value[index] <= 'f'))) {
            return 0;
        }
    }
    return 1;
}

static int is_bounded_transport_token(const char *value, int allow_empty) {
    size_t length;
    if (value == NULL || value[0] == '\0') {
        return allow_empty != 0;
    }
    length = strlen(value);
    if (length > 128U) {
        return 0;
    }
    for (size_t index = 0U; index < length; ++index) {
        const char character = value[index];
        if (!((character >= 'a' && character <= 'z') ||
                (character >= 'A' && character <= 'Z') ||
                (character >= '0' && character <= '9') ||
                character == ':' || character == '.' || character == '_' ||
                character == '-')) {
            return 0;
        }
    }
    return 1;
}

static int is_bounded_transport_case_id(const char *value) {
    return is_bounded_transport_token(value, 0);
}

static int is_bounded_transport_value(const char *value) {
    return is_bounded_transport_token(value, 1);
}

const char *msconnector_event_default_message(const char *message_id) {
    if (message_id == 0) {
        return "";
    }
    if (strcmp(message_id, MSCONN_EVENT_REQUEST_BLOCKED) == 0) {
        return "Request blocked by ModSecurity rule.";
    }
    if (strcmp(message_id, MSCONN_EVENT_RESPONSE_BLOCKED) == 0) {
        return "Response blocked by ModSecurity rule.";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_LATE_INTERVENTION) == 0) {
        return "Phase 4 intervention occurred after response output started.";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0) {
        return "Response already started with HTTP 200; Phase 4 requested a block; connection was aborted.";
    }
    if (strcmp(message_id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) == 0) {
        return "Requested capability is not implemented.";
    }
    if (strcmp(message_id, MSCONN_EVENT_INTERNAL_ERROR) == 0) {
        return "Internal connector error.";
    }
    if (strcmp(message_id, MSCONN_EVENT_CONFIG_ERROR) == 0) {
        return "Connector configuration error.";
    }
    if (strcmp(message_id, MSCONN_EVENT_RULE_PARSE_ERROR) == 0) {
        return "ModSecurity rule parsing failed.";
    }
    return "";
}

const char *msconnector_event_default_level(const char *message_id) {
    if (message_id == 0) {
        return "info";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0 ||
        strcmp(message_id, MSCONN_EVENT_INTERNAL_ERROR) == 0 ||
        strcmp(message_id, MSCONN_EVENT_CONFIG_ERROR) == 0 ||
        strcmp(message_id, MSCONN_EVENT_RULE_PARSE_ERROR) == 0) {
        return "error";
    }
    if (strcmp(message_id, MSCONN_EVENT_REQUEST_BLOCKED) == 0 ||
        strcmp(message_id, MSCONN_EVENT_RESPONSE_BLOCKED) == 0 ||
        strcmp(message_id, MSCONN_EVENT_PHASE4_LATE_INTERVENTION) == 0 ||
        strcmp(message_id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) == 0) {
        return "warn";
    }
    return "info";
}

void msconnector_event_init(msconnector_event *event) {
    if (event == 0) {
        return;
    }

    event->meta.timestamp = 0;
    event->meta.level = "info";
    event->meta.message_id = 0;
    event->meta.message = 0;
    event->meta.event = 0;
    event->meta.connector = 0;
    event->meta.integration_mode = 0;
    event->meta.run_id = 0;
    event->meta.transport_case_id = 0;
    event->meta.transaction_id = 0;
    event->decision.phase = MSCONNECTOR_PHASE_CONNECTION;
    event->decision.status = MSCONNECTOR_STATUS_OK;
    event->decision.action = 0;
    event->decision.requested_action = 0;
    event->decision.actual_action = 0;
    event->http.http_status = 0;
    event->http.original_http_status = 0;
    event->http.visible_http_status = 0;
    event->http.transport_result = 0;
    event->http.http_reason_phrase = 0;
    event->http.http_default_message = 0;
    event->protocol.requested_protocol = 0;
    event->protocol.downstream_protocol = 0;
    event->protocol.upstream_protocol = 0;
    event->protocol.negotiated_protocol = 0;
    event->protocol.transport = 0;
    event->protocol.alpn = 0;
    event->protocol.stream_id = 0;
    event->protocol.connection_id = 0;
    event->protocol.quic_version = 0;
    event->protocol.stream_reset_code = 0;
    event->protocol.reset_by = 0;
    event->protocol.reset_code = 0;
    event->protocol.connection_reused = 0;
    event->protocol.quic_connection_id_present = 0;
    event->protocol.fallback_used = 0;
    event->protocol.stream_reset = 0;
    event->decision.rule_id = 0;
    event->decision.reason = 0;
    event->request.method = 0;
    event->request.uri = 0;
    event->request.client_ip = 0;
    event->flags.late_intervention = 0;
    event->flags.late_intervention_mode = 0;
    event->flags.response_started = 0;
    event->flags.response_committed = 0;
    event->flags.headers_sent = 0;
    event->flags.body_started = 0;
    event->flags.body_truncated = 0;
    event->flags.connection_aborted = 0;
    event->flags.client_disconnected = 0;
    event->flags.upstream_disconnected = 0;
    event->flags.cancelled = 0;
    event->flags.eos_seen = 0;
    event->flags.timeout_stage = 0;
    event->flags.write_result = 0;
    event->flags.cleanup_reason = 0;
    event->flags.redacted = 0;
    event->flags.truncated = 0;
    event->body.content_type = 0;
    event->body.limit_outcome = 0;
    event->body.bytes_seen = 0U;
    event->body.bytes_inspected = 0U;
    event->integrity.sequence = 0UL;
    event->integrity.previous_hash = 0U;
    event->integrity.event_hash = 0U;
}

const char *msconnector_event_status_name(const msconnector_event *event) {
    if (event == 0) {
        return msconnector_status_name(MSCONNECTOR_STATUS_ERROR);
    }

    return msconnector_status_name(event->decision.status);
}

int msconnector_event_write_json_ex(
    const msconnector_event *event,
    char *dst,
    size_t dst_size,
    int *truncated) {
    char timestamp[EVENT_TEXT_SIZE];
    char level[32];
    char message_id[EVENT_TEXT_SIZE];
    char message[EVENT_TEXT_SIZE];
    char event_name[EVENT_TEXT_SIZE];
    char connector[EVENT_TEXT_SIZE];
    char integration_mode[EVENT_TEXT_SIZE];
    char run_id[EVENT_TEXT_SIZE];
    char transport_case_id[EVENT_TEXT_SIZE];
    char transaction_id[EVENT_TEXT_SIZE];
    char action[64];
    char requested_action[64];
    char actual_action[64];
    char transport_result[64];
    char requested_protocol[32];
    char downstream_protocol[32];
    char upstream_protocol[32];
    char negotiated_protocol[32];
    char transport[32];
    char alpn[32];
    char stream_id[EVENT_TEXT_SIZE];
    char connection_id[EVENT_TEXT_SIZE];
    char quic_version[64];
    char stream_reset_code[64];
    char reset_by[64];
    char reset_code[64];
    char http_reason_phrase[EVENT_TEXT_SIZE];
    char http_default_message[EVENT_TEXT_SIZE];
    char rule_id[EVENT_TEXT_SIZE];
    char reason[EVENT_TEXT_SIZE];
    char method[64];
    char uri[EVENT_TEXT_SIZE];
    char client_ip[64];
    char content_type[EVENT_TEXT_SIZE];
    char body_limit_outcome[EVENT_TEXT_SIZE];
    char body_limit_outcome_json[EVENT_TEXT_SIZE * 2U];
    char late_intervention_mode[32];
    char timeout_stage[64];
    char write_result[64];
    char cleanup_reason[64];
    char late_intervention_mode_json[64];
    char provenance_json[EVENT_TEXT_SIZE * 12U];
    msconnector_event_json_parts parts;
    int was_truncated;
    int protocol_present;
    size_t provenance_offset;
    int written;

    if (truncated != 0) {
        *truncated = 0;
    }
    if (dst != 0 && dst_size > 0) {
        dst[0] = '\0';
    }
    if (event == 0 || dst == 0 || dst_size == 0) {
        return 0;
    }

    was_truncated = event->flags.truncated != 0;
    escape_field(event->meta.timestamp, timestamp, sizeof(timestamp), &was_truncated);
    escape_field(event->meta.level, level, sizeof(level), &was_truncated);
    escape_field(event->meta.message_id, message_id, sizeof(message_id), &was_truncated);
    escape_field(event->meta.message, message, sizeof(message), &was_truncated);
    escape_field(event->meta.event, event_name, sizeof(event_name), &was_truncated);
    escape_field(event->meta.connector, connector, sizeof(connector), &was_truncated);
    escape_field(event->meta.integration_mode, integration_mode,
        sizeof(integration_mode), &was_truncated);
    escape_field(event->meta.run_id, run_id, sizeof(run_id), &was_truncated);
    escape_field(event->meta.transport_case_id, transport_case_id,
        sizeof(transport_case_id), &was_truncated);
    if (transport_case_id[0] != '\0' &&
        !is_bounded_transport_case_id(event->meta.transport_case_id)) {
        /* Correlation IDs are metadata tokens, never request-derived text. */
        transport_case_id[0] = '\0';
        was_truncated = 1;
    }
    escape_field(event->meta.transaction_id, transaction_id, sizeof(transaction_id), &was_truncated);
    escape_field(event->decision.action, action, sizeof(action), &was_truncated);
    escape_field(event->decision.requested_action, requested_action, sizeof(requested_action), &was_truncated);
    escape_field(event->decision.actual_action, actual_action, sizeof(actual_action), &was_truncated);
    escape_field(event->http.transport_result, transport_result, sizeof(transport_result), &was_truncated);
    escape_field(event->protocol.requested_protocol, requested_protocol,
        sizeof(requested_protocol), &was_truncated);
    escape_field(event->protocol.downstream_protocol, downstream_protocol,
        sizeof(downstream_protocol), &was_truncated);
    escape_field(event->protocol.upstream_protocol, upstream_protocol,
        sizeof(upstream_protocol), &was_truncated);
    escape_field(event->protocol.negotiated_protocol, negotiated_protocol,
        sizeof(negotiated_protocol), &was_truncated);
    escape_field(event->protocol.transport, transport, sizeof(transport), &was_truncated);
    escape_field(event->protocol.alpn, alpn, sizeof(alpn), &was_truncated);
    escape_field(event->protocol.stream_id, stream_id, sizeof(stream_id), &was_truncated);
    escape_field(event->protocol.connection_id, connection_id, sizeof(connection_id), &was_truncated);
    escape_field(event->protocol.quic_version, quic_version, sizeof(quic_version), &was_truncated);
    escape_field(event->protocol.stream_reset_code, stream_reset_code,
        sizeof(stream_reset_code), &was_truncated);
    escape_field(event->protocol.reset_by, reset_by, sizeof(reset_by),
        &was_truncated);
    escape_field(event->protocol.reset_code, reset_code, sizeof(reset_code),
        &was_truncated);
    if ((strcmp(negotiated_protocol, "h3") == 0 ||
            strcmp(downstream_protocol, "h3") == 0 ||
            strcmp(transport, "quic_udp") == 0) &&
        connection_id[0] != '\0' && !is_nonreversible_quic_connection_id(connection_id)) {
        /* A raw QUIC CID is linkable transport data, not event metadata. */
        connection_id[0] = '\0';
    }
    escape_field(event->http.http_reason_phrase, http_reason_phrase, sizeof(http_reason_phrase), &was_truncated);
    escape_field(event->http.http_default_message, http_default_message, sizeof(http_default_message), &was_truncated);
    escape_field(event->decision.rule_id, rule_id, sizeof(rule_id), &was_truncated);
    escape_field(event->decision.reason, reason, sizeof(reason), &was_truncated);
    escape_field(event->request.method, method, sizeof(method), &was_truncated);
    escape_field(event->request.uri, uri, sizeof(uri), &was_truncated);
    escape_field(event->request.client_ip, client_ip, sizeof(client_ip), &was_truncated);
    escape_field(event->body.content_type, content_type, sizeof(content_type), &was_truncated);
    escape_field(event->body.limit_outcome, body_limit_outcome,
        sizeof(body_limit_outcome), &was_truncated);
    escape_field(event->flags.late_intervention_mode, late_intervention_mode,
        sizeof(late_intervention_mode), &was_truncated);
    escape_field(event->flags.timeout_stage, timeout_stage, sizeof(timeout_stage),
        &was_truncated);
    escape_field(event->flags.write_result, write_result, sizeof(write_result),
        &was_truncated);
    escape_field(event->flags.cleanup_reason, cleanup_reason,
        sizeof(cleanup_reason), &was_truncated);
    if (!is_bounded_transport_value(event->protocol.reset_by) ||
        !is_bounded_transport_value(event->protocol.reset_code) ||
        !is_bounded_transport_value(event->flags.timeout_stage) ||
        !is_bounded_transport_value(event->flags.write_result) ||
        !is_bounded_transport_value(event->flags.cleanup_reason)) {
        reset_by[0] = '\0';
        reset_code[0] = '\0';
        timeout_stage[0] = '\0';
        write_result[0] = '\0';
        cleanup_reason[0] = '\0';
        was_truncated = 1;
    }

    provenance_json[0] = '\0';
    provenance_offset = 0U;
    if (!append_protocol_string(provenance_json, sizeof(provenance_json),
            &provenance_offset, "run_id", run_id)) {
        was_truncated = 1;
    }
    if (!append_protocol_string(provenance_json, sizeof(provenance_json),
            &provenance_offset, "transport_case_id", transport_case_id)) {
        was_truncated = 1;
    }
    protocol_present = requested_protocol[0] != '\0' ||
        downstream_protocol[0] != '\0' || upstream_protocol[0] != '\0' ||
        negotiated_protocol[0] != '\0' || transport[0] != '\0' ||
        alpn[0] != '\0' || stream_id[0] != '\0' || connection_id[0] != '\0' ||
        quic_version[0] != '\0' || stream_reset_code[0] != '\0' ||
        reset_by[0] != '\0' || reset_code[0] != '\0' ||
        timeout_stage[0] != '\0' || write_result[0] != '\0' ||
        cleanup_reason[0] != '\0' ||
        event->protocol.connection_reused != 0 ||
        event->protocol.quic_connection_id_present != 0 ||
        event->protocol.fallback_used != 0 || event->protocol.stream_reset != 0;
    if (protocol_present) {
        if (!append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "requested_protocol", requested_protocol) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "downstream_protocol", downstream_protocol) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "upstream_protocol", upstream_protocol) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "negotiated_protocol", negotiated_protocol) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "transport", transport) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "alpn", alpn) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "stream_id", stream_id) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "connection_id", connection_id) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "quic_version", quic_version) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "stream_reset_code", stream_reset_code) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "reset_by", reset_by) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "reset_code", reset_code) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "timeout_stage", timeout_stage) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "write_result", write_result) ||
            !append_protocol_string(provenance_json, sizeof(provenance_json),
                &provenance_offset, "cleanup_reason", cleanup_reason) ||
            !append_protocol_bool(provenance_json, sizeof(provenance_json),
                &provenance_offset, "connection_reused", event->protocol.connection_reused) ||
            !append_protocol_bool(provenance_json, sizeof(provenance_json),
                &provenance_offset, "quic_connection_id_present",
                event->protocol.quic_connection_id_present) ||
            !append_protocol_bool(provenance_json, sizeof(provenance_json),
                &provenance_offset, "fallback_used", event->protocol.fallback_used) ||
            !append_protocol_bool(provenance_json, sizeof(provenance_json),
                &provenance_offset, "stream_reset", event->protocol.stream_reset)) {
            was_truncated = 1;
            provenance_json[0] = '\0';
        }
    }

    parts.text[EVENT_JSON_TIMESTAMP] = timestamp;
    parts.text[EVENT_JSON_LEVEL] = level;
    parts.text[EVENT_JSON_MESSAGE_ID] = message_id;
    parts.text[EVENT_JSON_MESSAGE] = message;
    parts.text[EVENT_JSON_EVENT_NAME] = event_name;
    parts.text[EVENT_JSON_CONNECTOR] = connector;
    parts.text[EVENT_JSON_INTEGRATION_MODE] = integration_mode;
    parts.text[EVENT_JSON_RUN_ID] = run_id;
    parts.text[EVENT_JSON_TRANSPORT_CASE_ID] = transport_case_id;
    parts.text[EVENT_JSON_TRANSACTION_ID] = transaction_id;
    parts.text[EVENT_JSON_PHASE] = msconnector_phase_name(event->decision.phase);
    parts.text[EVENT_JSON_STATUS] = msconnector_status_name(event->decision.status);
    parts.text[EVENT_JSON_ACTION] = action;
    parts.text[EVENT_JSON_REQUESTED_ACTION] = requested_action;
    parts.text[EVENT_JSON_ACTUAL_ACTION] = actual_action;
    parts.text[EVENT_JSON_TRANSPORT_RESULT] = transport_result;
    parts.text[EVENT_JSON_REQUESTED_PROTOCOL] = requested_protocol;
    parts.text[EVENT_JSON_DOWNSTREAM_PROTOCOL] = downstream_protocol;
    parts.text[EVENT_JSON_UPSTREAM_PROTOCOL] = upstream_protocol;
    parts.text[EVENT_JSON_NEGOTIATED_PROTOCOL] = negotiated_protocol;
    parts.text[EVENT_JSON_TRANSPORT] = transport;
    parts.text[EVENT_JSON_ALPN] = alpn;
    parts.text[EVENT_JSON_STREAM_ID] = stream_id;
    parts.text[EVENT_JSON_CONNECTION_ID] = connection_id;
    parts.text[EVENT_JSON_QUIC_VERSION] = quic_version;
    parts.text[EVENT_JSON_STREAM_RESET_CODE] = stream_reset_code;
    parts.statuses[EVENT_JSON_HTTP_STATUS] = event->http.http_status;
    parts.statuses[EVENT_JSON_ORIGINAL_HTTP_STATUS] = event->http.original_http_status;
    parts.statuses[EVENT_JSON_VISIBLE_HTTP_STATUS] = event->http.visible_http_status;
    parts.text[EVENT_JSON_HTTP_REASON_PHRASE] = http_reason_phrase;
    parts.text[EVENT_JSON_HTTP_DEFAULT_MESSAGE] = http_default_message;
    parts.text[EVENT_JSON_RULE_ID] = rule_id;
    parts.text[EVENT_JSON_REASON] = reason;
    parts.text[EVENT_JSON_METHOD] = method;
    parts.text[EVENT_JSON_URI] = uri;
    parts.text[EVENT_JSON_CLIENT_IP] = client_ip;
    parts.text[EVENT_JSON_CONTENT_TYPE] = content_type;
    parts.text[EVENT_JSON_BODY_LIMIT_OUTCOME] = body_limit_outcome;
    parts.text[EVENT_JSON_LATE_INTERVENTION_MODE] = late_intervention_mode;
    parts.body_bytes_seen = event->body.bytes_seen;
    parts.body_bytes_inspected = event->body.bytes_inspected;
    body_limit_outcome_json[0] = '\0';
    if (body_limit_outcome[0] != '\0') {
        int outcome_written = snprintf(body_limit_outcome_json,
            sizeof(body_limit_outcome_json),
            ",\"body_limit_outcome\":\"%s\"", body_limit_outcome);
        if (outcome_written < 0 || (size_t)outcome_written >=
            sizeof(body_limit_outcome_json)) {
            body_limit_outcome_json[0] = '\0';
            was_truncated = 1;
        }
    }
    parts.body_limit_outcome_json = body_limit_outcome_json;
    parts.provenance_json = provenance_json;
    late_intervention_mode_json[0] = '\0';
    if (late_intervention_mode[0] != '\0') {
        int mode_written = snprintf(late_intervention_mode_json,
            sizeof(late_intervention_mode_json),
            ",\"late_intervention_mode\":\"%s\"", late_intervention_mode);
        if (mode_written < 0 || (size_t)mode_written >=
            sizeof(late_intervention_mode_json)) {
            late_intervention_mode_json[0] = '\0';
            was_truncated = 1;
        }
    }
    parts.late_intervention_mode_json = late_intervention_mode_json;
    parts.flags[EVENT_JSON_LATE_INTERVENTION] = json_bool(event->flags.late_intervention);
    parts.flags[EVENT_JSON_RESPONSE_STARTED] = json_bool(event->flags.response_started);
    parts.flags[EVENT_JSON_RESPONSE_COMMITTED] = json_bool(event->flags.response_committed);
    parts.flags[EVENT_JSON_HEADERS_SENT] = json_bool(event->flags.headers_sent);
    parts.flags[EVENT_JSON_BODY_STARTED] = json_bool(event->flags.body_started);
    parts.flags[EVENT_JSON_BODY_TRUNCATED] = json_bool(event->flags.body_truncated);
    parts.flags[EVENT_JSON_CONNECTION_ABORTED] = json_bool(event->flags.connection_aborted);
    parts.flags[EVENT_JSON_CLIENT_DISCONNECTED] = json_bool(event->flags.client_disconnected);
    parts.flags[EVENT_JSON_UPSTREAM_DISCONNECTED] = json_bool(event->flags.upstream_disconnected);
    parts.flags[EVENT_JSON_CANCELLED] = json_bool(event->flags.cancelled);
    parts.flags[EVENT_JSON_EOS_SEEN] = json_bool(event->flags.eos_seen);
    parts.flags[EVENT_JSON_REDACTED] = json_bool(event->flags.redacted);
    parts.flags[EVENT_JSON_TRUNCATED] = json_bool(was_truncated);
    parts.flags[EVENT_JSON_CONNECTION_REUSED] = json_bool(event->protocol.connection_reused);
    parts.flags[EVENT_JSON_QUIC_CONNECTION_ID_PRESENT] = json_bool(
        event->protocol.quic_connection_id_present);
    parts.flags[EVENT_JSON_FALLBACK_USED] = json_bool(event->protocol.fallback_used);
    parts.flags[EVENT_JSON_STREAM_RESET] = json_bool(event->protocol.stream_reset);
    parts.sequence = event->integrity.sequence;
    parts.previous_hash = event->integrity.previous_hash;
    parts.event_hash = event->integrity.event_hash;

    written = format_event_json(0, 0, &parts);

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }

    parts.flags[EVENT_JSON_TRUNCATED] = json_bool(was_truncated);
    written = format_event_json(dst, dst_size, &parts);

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }
    if (truncated != 0) {
        *truncated = was_truncated;
    }
    return was_truncated ? 0 : 1;
}

int msconnector_event_write_json(const msconnector_event *event, char *dst, size_t dst_size) {
    int truncated = 0;
    return msconnector_event_write_json_ex(event, dst, dst_size, &truncated);
}

void msconnector_event_set_phase4_hard_abort_after_200(
    msconnector_event *event,
    const char *connector,
    const char *transaction_id,
    const char *rule_id,
    const char *reason) {
    if (event == 0) {
        return;
    }

    msconnector_event_init(event);
    event->meta.level = msconnector_event_default_level(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->meta.message_id = MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200;
    event->meta.message = msconnector_event_default_message(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->meta.event = "phase4_hard_abort_after_200";
    event->meta.connector = connector;
    event->meta.transaction_id = transaction_id;
    event->decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event->decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event->decision.action = "abort_connection";
    event->decision.requested_action = "deny";
    event->decision.actual_action = "abort_connection";
    event->http.http_status = 403;
    event->http.original_http_status = 200;
    event->http.visible_http_status = 200;
    event->http.transport_result = "connection_aborted";
    event->http.http_reason_phrase = msconnector_http_status_reason_phrase(403);
    event->http.http_default_message = msconnector_http_status_default_message(403);
    event->decision.rule_id = rule_id;
    event->decision.reason = reason;
    event->flags.late_intervention = 1;
    event->flags.late_intervention_mode = "strict";
    event->flags.response_started = 1;
    event->flags.response_committed = 1;
    event->flags.headers_sent = 1;
    event->flags.body_started = 1;
    event->flags.connection_aborted = 1;
}
