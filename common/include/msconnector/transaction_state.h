#ifndef MSCONNECTOR_TRANSACTION_STATE_H
#define MSCONNECTOR_TRANSACTION_STATE_H
#include "msconnector/transaction.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Connector-neutral phase bookkeeping. It stores flags only and owns no strings. */
typedef struct msconnector_transaction_state { const char *transaction_id; int connection_processed; int uri_processed; int request_headers_processed; int request_body_processed; int response_headers_processed; int response_body_processed; int logging_processed; int response_headers_committed; int response_body_started; int response_body_truncated; } msconnector_transaction_state;
void msconnector_transaction_state_init(msconnector_transaction_state *state, const char *transaction_id);
int msconnector_transaction_state_mark_phase(msconnector_transaction_state *state, enum msconnector_phase phase);
int msconnector_transaction_state_phase_processed(const msconnector_transaction_state *state, enum msconnector_phase phase);
const char *msconnector_phase_name(enum msconnector_phase phase);
#ifdef __cplusplus
}
#endif
#endif
