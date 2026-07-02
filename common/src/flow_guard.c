#include "msconnector/flow_guard.h"

static int phase_valid(enum msconnector_phase phase) { return phase >= MSCONNECTOR_PHASE_CONNECTION && phase <= MSCONNECTOR_PHASE_LOGGING; }
static unsigned long phase_bit(enum msconnector_phase phase) { return 1UL << (unsigned int)phase; }

void msconnector_flow_guard_init(msconnector_flow_guard *guard, const char *transaction_id) {
    if (guard == 0) { return; }
    guard->transaction_id = transaction_id;
    guard->current_phase = MSCONNECTOR_PHASE_CONNECTION;
    guard->last_completed_phase = MSCONNECTOR_PHASE_CONNECTION;
    guard->sequence = 0UL;
    guard->immutable = 0;
    guard->validated = 0;
    guard->previous_event_hash = 0U;
    guard->event_hash = 0U;
    guard->completed_mask = 0UL;
}

int msconnector_flow_guard_can_enter_phase(const msconnector_flow_guard *guard, enum msconnector_phase phase) {
    if (guard == 0 || !phase_valid(phase)) { return MSCONNECTOR_FLOW_GUARD_INVALID; }
    if (guard->immutable) { return MSCONNECTOR_FLOW_GUARD_IMMUTABLE; }
    if ((guard->completed_mask & phase_bit(phase)) != 0UL) { return MSCONNECTOR_FLOW_GUARD_DUPLICATE_MUTATION; }
    if (phase != MSCONNECTOR_PHASE_CONNECTION && (guard->completed_mask & phase_bit((enum msconnector_phase)(phase - 1))) == 0UL) { return MSCONNECTOR_FLOW_GUARD_PHASE_ORDER; }
    return MSCONNECTOR_FLOW_GUARD_OK;
}

int msconnector_flow_guard_mark_validated(msconnector_flow_guard *guard, enum msconnector_phase phase) {
    int rc = msconnector_flow_guard_can_enter_phase(guard, phase);
    if (rc != MSCONNECTOR_FLOW_GUARD_OK) { return rc; }
    guard->current_phase = phase;
    guard->last_completed_phase = phase;
    guard->completed_mask |= phase_bit(phase);
    guard->validated = 1;
    return MSCONNECTOR_FLOW_GUARD_OK;
}

int msconnector_flow_guard_mark_immutable(msconnector_flow_guard *guard) { if (guard == 0) { return MSCONNECTOR_FLOW_GUARD_INVALID; } guard->immutable = 1; return MSCONNECTOR_FLOW_GUARD_OK; }
int msconnector_flow_guard_next_sequence(msconnector_flow_guard *guard, unsigned long *sequence) { if (guard == 0 || sequence == 0) { return MSCONNECTOR_FLOW_GUARD_INVALID; } ++guard->sequence; *sequence = guard->sequence; return MSCONNECTOR_FLOW_GUARD_OK; }

const char *msconnector_flow_guard_error_name(int code) {
    switch (code) {
        case MSCONNECTOR_FLOW_GUARD_OK: return "ok";
        case MSCONNECTOR_FLOW_GUARD_INVALID: return "invalid";
        case MSCONNECTOR_FLOW_GUARD_PHASE_ORDER: return "phase_order";
        case MSCONNECTOR_FLOW_GUARD_IMMUTABLE: return "immutable";
        case MSCONNECTOR_FLOW_GUARD_DUPLICATE_MUTATION: return "duplicate_mutation";
        default: return "unknown";
    }
}
