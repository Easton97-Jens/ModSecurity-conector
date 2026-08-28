#ifndef MSCONNECTOR_TRANSACTION_STATE_H
#define MSCONNECTOR_TRANSACTION_STATE_H
#include "msconnector/transaction.h"
#include "msconnector/transaction_contract.h"
#ifdef __cplusplus
extern "C" {
#endif
/*
 * Compatibility phase flags plus the canonical P1–P4 contract.  The legacy
 * transaction_id remains borrowed for ABI compatibility; the contract owns a
 * bounded copy of its identifier and metadata.
 */
typedef struct msconnector_transaction_state {
    const char *transaction_id;
    /* Admission is distinct from the legacy phase flags. A failed canonical
     * contract initialization must never leave a state that legacy callers
     * can advance or use to allocate a native engine transaction. */
    int initialized;
    int connection_processed;
    int uri_processed;
    int request_headers_processed;
    int request_body_processed;
    int response_headers_processed;
    int response_body_processed;
    int logging_processed;
    int response_headers_committed;
    int response_body_started;
    int response_body_truncated;
    msconnector_transaction_contract contract;
} msconnector_transaction_state;
/* Returns nonzero only when the bounded canonical contract was admitted. */
int msconnector_transaction_state_init(msconnector_transaction_state *state,
    const char *transaction_id);
int msconnector_transaction_state_begin_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase);
int msconnector_transaction_state_complete_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase);
/* Records a legacy lifecycle flag after an externally owned canonical
 * transaction contract completed the corresponding phase. */
int msconnector_transaction_state_note_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase);
int msconnector_transaction_state_mark_phase(msconnector_transaction_state *state, enum msconnector_phase phase);
int msconnector_transaction_state_phase_processed(const msconnector_transaction_state *state, enum msconnector_phase phase);
const char *msconnector_phase_name(enum msconnector_phase phase);
#ifdef __cplusplus
}
#endif
#endif
