#include "msconnector/integrity_event.h"
#include "msconnector/phase.h"
#include <string.h>

#define FNV_OFFSET UINT64_C(14695981039346656037)
#define FNV_PRIME UINT64_C(1099511628211)

static uint64_t hash_bytes_continue(uint64_t hash, const unsigned char *data, size_t size) {
    if (data == 0 && size > 0U) { return hash; }
    for (size_t i = 0; i < size; ++i) { hash ^= (uint64_t)data[i]; hash *= FNV_PRIME; }
    return hash;
}
static uint64_t hash_string_continue(uint64_t hash, const char *value) { return value == 0 ? hash_bytes_continue(hash, (const unsigned char *)"", 1U) : hash_bytes_continue(hash, (const unsigned char *)value, strlen(value) + 1U); }
static uint64_t hash_int_continue(uint64_t hash, int value) { return hash_bytes_continue(hash, (const unsigned char *)&value, sizeof(value)); }

static int is_nonreversible_quic_connection_id(const char *value) {
    size_t index;
    size_t length;
    if (value == NULL || strncmp(value, "sha256:", 7U) != 0) { return 0; }
    length = strlen(value + 7U);
    if (length < 16U || length > 64U) { return 0; }
    for (index = 7U; value[index] != '\0'; ++index) {
        if (!((value[index] >= '0' && value[index] <= '9') ||
                (value[index] >= 'a' && value[index] <= 'f'))) { return 0; }
    }
    return 1;
}

static int is_bounded_transport_case_id(const char *value) {
    size_t index;
    size_t length;
    if (value == NULL || value[0] == '\0') { return 0; }
    length = strlen(value);
    if (length > 128U) { return 0; }
    for (index = 0U; index < length; ++index) {
        const char character = value[index];
        if (!((character >= 'a' && character <= 'z') ||
                (character >= 'A' && character <= 'Z') ||
                (character >= '0' && character <= '9') ||
                character == ':' || character == '.' || character == '_' ||
                character == '-')) { return 0; }
    }
    return 1;
}

static const char *safe_connection_id_for_event_hash(const msconnector_event *event) {
    const char *value = event->protocol.connection_id;
    if (value == NULL) { return NULL; }
    if ((event->protocol.negotiated_protocol != NULL &&
            strcmp(event->protocol.negotiated_protocol, "h3") == 0) ||
        (event->protocol.downstream_protocol != NULL &&
            strcmp(event->protocol.downstream_protocol, "h3") == 0) ||
        (event->protocol.transport != NULL &&
            strcmp(event->protocol.transport, "quic_udp") == 0)) {
        return is_nonreversible_quic_connection_id(value) ? value : NULL;
    }
    return value;
}

uint64_t msconnector_non_crypto_hash_bytes(const unsigned char *data, size_t size) { return hash_bytes_continue(FNV_OFFSET, data, size); }
uint64_t msconnector_non_crypto_hash_string(const char *value) { return hash_string_continue(FNV_OFFSET, value); }

uint64_t msconnector_integrity_event_hash(const msconnector_event *event, uint64_t previous_hash) {
    uint64_t hash = hash_bytes_continue(FNV_OFFSET, (const unsigned char *)&previous_hash, sizeof(previous_hash));
    const char *connection_id;
    const char *transport_case_id;
    if (event == 0) { return hash; }
    connection_id = safe_connection_id_for_event_hash(event);
    transport_case_id = is_bounded_transport_case_id(event->meta.transport_case_id)
        ? event->meta.transport_case_id : NULL;
    hash = hash_string_continue(hash, event->meta.timestamp);
    hash = hash_string_continue(hash, event->meta.level);
    hash = hash_string_continue(hash, event->meta.message_id);
    hash = hash_string_continue(hash, event->meta.event);
    hash = hash_string_continue(hash, event->meta.connector);
    hash = hash_string_continue(hash, event->meta.integration_mode);
    hash = hash_string_continue(hash, event->meta.run_id);
    hash = hash_string_continue(hash, transport_case_id);
    hash = hash_string_continue(hash, event->meta.transaction_id);
    hash = hash_int_continue(hash, (int)event->decision.phase);
    hash = hash_int_continue(hash, (int)event->decision.status);
    hash = hash_string_continue(hash, event->decision.action);
    hash = hash_string_continue(hash, event->decision.rule_id);
    hash = hash_string_continue(hash, event->decision.reason);
    hash = hash_int_continue(hash, event->http.http_status);
    hash = hash_int_continue(hash, event->http.original_http_status);
    hash = hash_int_continue(hash, event->http.visible_http_status);
    hash = hash_string_continue(hash, event->http.transport_result);
    hash = hash_string_continue(hash, event->protocol.requested_protocol);
    hash = hash_string_continue(hash, event->protocol.downstream_protocol);
    hash = hash_string_continue(hash, event->protocol.upstream_protocol);
    hash = hash_string_continue(hash, event->protocol.negotiated_protocol);
    hash = hash_string_continue(hash, event->protocol.transport);
    hash = hash_string_continue(hash, event->protocol.alpn);
    hash = hash_string_continue(hash, event->protocol.stream_id);
    hash = hash_string_continue(hash, connection_id);
    hash = hash_string_continue(hash, event->protocol.quic_version);
    hash = hash_string_continue(hash, event->protocol.stream_reset_code);
    hash = hash_string_continue(hash, event->protocol.reset_by);
    hash = hash_string_continue(hash, event->protocol.reset_code);
    hash = hash_int_continue(hash, event->protocol.connection_reused);
    hash = hash_int_continue(hash, event->protocol.quic_connection_id_present);
    hash = hash_int_continue(hash, event->protocol.fallback_used);
    hash = hash_int_continue(hash, event->protocol.stream_reset);
    hash = hash_string_continue(hash, event->request.method);
    hash = hash_string_continue(hash, event->request.uri);
    hash = hash_string_continue(hash, event->request.client_ip);
    hash = hash_string_continue(hash, event->body.content_type);
    hash = hash_string_continue(hash, event->body.limit_outcome);
    hash = hash_bytes_continue(hash, (const unsigned char *)&event->body.bytes_seen,
        sizeof(event->body.bytes_seen));
    hash = hash_bytes_continue(hash, (const unsigned char *)&event->body.bytes_inspected,
        sizeof(event->body.bytes_inspected));
    hash = hash_int_continue(hash, event->flags.late_intervention);
    hash = hash_string_continue(hash, event->flags.late_intervention_mode);
    hash = hash_int_continue(hash, event->flags.response_started);
    hash = hash_int_continue(hash, event->flags.response_committed);
    hash = hash_int_continue(hash, event->flags.headers_sent);
    hash = hash_int_continue(hash, event->flags.body_started);
    hash = hash_int_continue(hash, event->flags.body_truncated);
    hash = hash_int_continue(hash, event->flags.connection_aborted);
    hash = hash_int_continue(hash, event->flags.client_disconnected);
    hash = hash_int_continue(hash, event->flags.upstream_disconnected);
    hash = hash_int_continue(hash, event->flags.cancelled);
    hash = hash_int_continue(hash, event->flags.eos_seen);
    hash = hash_string_continue(hash, event->flags.timeout_stage);
    hash = hash_string_continue(hash, event->flags.write_result);
    hash = hash_string_continue(hash, event->flags.cleanup_reason);
    return hash;
}

int msconnector_integrity_event_chain_verify(uint64_t previous_hash, uint64_t event_hash, const msconnector_event *event) { return msconnector_integrity_event_hash(event, previous_hash) == event_hash; }
