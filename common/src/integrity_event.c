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

uint64_t msconnector_non_crypto_hash_bytes(const unsigned char *data, size_t size) { return hash_bytes_continue(FNV_OFFSET, data, size); }
uint64_t msconnector_non_crypto_hash_string(const char *value) { return hash_string_continue(FNV_OFFSET, value); }

uint64_t msconnector_integrity_event_hash(const msconnector_event *event, uint64_t previous_hash) {
    uint64_t hash = hash_bytes_continue(FNV_OFFSET, (const unsigned char *)&previous_hash, sizeof(previous_hash));
    if (event == 0) { return hash; }
    hash = hash_string_continue(hash, event->meta.timestamp);
    hash = hash_string_continue(hash, event->meta.level);
    hash = hash_string_continue(hash, event->meta.message_id);
    hash = hash_string_continue(hash, event->meta.event);
    hash = hash_string_continue(hash, event->meta.connector);
    hash = hash_string_continue(hash, event->meta.integration_mode);
    hash = hash_string_continue(hash, event->meta.transaction_id);
    hash = hash_int_continue(hash, (int)event->decision.phase);
    hash = hash_int_continue(hash, (int)event->decision.status);
    hash = hash_string_continue(hash, event->decision.action);
    hash = hash_string_continue(hash, event->decision.rule_id);
    hash = hash_string_continue(hash, event->decision.reason);
    hash = hash_int_continue(hash, event->http.http_status);
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
    return hash;
}

int msconnector_integrity_event_chain_verify(uint64_t previous_hash, uint64_t event_hash, const msconnector_event *event) { return msconnector_integrity_event_hash(event, previous_hash) == event_hash; }
