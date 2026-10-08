#ifndef NGX_HTTP_MODSECURITY_PHASE4_OBSERVATION_H
#define NGX_HTTP_MODSECURITY_PHASE4_OBSERVATION_H

#include "msconnector/event.h"
#include "msconnector/transaction_contract.h"
#include <inttypes.h>
#include <stdio.h>

/* Caller supplies actual native/API counters and a completed Common contract,
 * never fixture expectations. Event/reason storage remains caller-owned.
 * Common bytes_inspected retains its meaning: bytes supplied to the Engine;
 * retained inspection length is separately labeled in bounded metadata. */
static inline int
ngx_http_modsecurity_phase4_observation(msconnector_event *event,
    char *reason, size_t reason_size, int native_result,
    const msconnector_transaction_contract *contract, uint64_t retained,
    uint64_t seen, uint64_t supplied, uint64_t append_calls,
    const char *actual_content_type)
{
    int length;
    if (event == NULL || reason == NULL || reason_size == 0 ||
        contract == NULL || native_result != 1 ||
        contract->active_phase != -1 ||
        contract->last_completed_phase != MSCONNECTOR_PHASE_RESPONSE_BODY ||
        (contract->completed_phase_mask &
            MSCONNECTOR_TRANSACTION_PHASE_MASK_P4) == 0U ||
        retained > supplied || supplied > seen || seen > INT64_MAX ||
        append_calls > INT64_MAX ||
        (append_calls == 0 && (seen != 0 || supplied != 0 || retained != 0))) {
        return 0;
    }
    length = snprintf(reason, reason_size,
        "engine_retained_bytes=%" PRIu64 ";append_calls=%" PRIu64,
        retained, append_calls);
    if (length < 0 || (size_t)length >= reason_size) return 0;
    event->meta.event = "phase4_completion";
    event->meta.message = "Native response body processing completed.";
    event->decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event->decision.reason = reason;
    event->flags.eos_seen = 1;
    event->body.content_type = actual_content_type;
    event->body.bytes_seen = seen;
    event->body.bytes_inspected = supplied;
    return 1;
}

#endif
