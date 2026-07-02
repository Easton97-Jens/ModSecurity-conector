#ifndef MSCONNECTOR_FLOW_GUARD_H
#define MSCONNECTOR_FLOW_GUARD_H

#include "msconnector/phase.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define MSCONNECTOR_FLOW_GUARD_OK 0
#define MSCONNECTOR_FLOW_GUARD_INVALID -1
#define MSCONNECTOR_FLOW_GUARD_PHASE_ORDER -2
#define MSCONNECTOR_FLOW_GUARD_IMMUTABLE -3
#define MSCONNECTOR_FLOW_GUARD_DUPLICATE_MUTATION -4

typedef struct msconnector_flow_guard {
    const char *transaction_id;
    enum msconnector_phase current_phase;
    enum msconnector_phase last_completed_phase;
    unsigned long sequence;
    int immutable;
    int validated;
    uint64_t previous_event_hash;
    uint64_t event_hash;
    unsigned long completed_mask;
} msconnector_flow_guard;

void msconnector_flow_guard_init(msconnector_flow_guard *guard, const char *transaction_id);
int msconnector_flow_guard_can_enter_phase(const msconnector_flow_guard *guard, enum msconnector_phase phase);
int msconnector_flow_guard_mark_validated(msconnector_flow_guard *guard, enum msconnector_phase phase);
int msconnector_flow_guard_mark_immutable(msconnector_flow_guard *guard);
int msconnector_flow_guard_next_sequence(msconnector_flow_guard *guard, unsigned long *sequence);
const char *msconnector_flow_guard_error_name(int code);

#ifdef __cplusplus
}
#endif

#endif
