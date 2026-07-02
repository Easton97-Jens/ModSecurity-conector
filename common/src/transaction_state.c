#include "msconnector/transaction_state.h"

void msconnector_transaction_state_init(
    msconnector_transaction_state *state,
    const char *transaction_id) {
    if (state == 0) {
        return;
    }

    state->transaction_id = transaction_id;
    state->connection_processed = 0;
    state->uri_processed = 0;
    state->request_headers_processed = 0;
    state->request_body_processed = 0;
    state->response_headers_processed = 0;
    state->response_body_processed = 0;
    state->logging_processed = 0;
    state->response_headers_committed = 0;
    state->response_body_started = 0;
    state->response_body_truncated = 0;
}

int msconnector_transaction_state_mark_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (state == 0) {
        return 0;
    }

    switch (phase) {
    case MSCONNECTOR_PHASE_CONNECTION:
        state->connection_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_URI:
        state->uri_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_REQUEST_HEADERS:
        state->request_headers_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_REQUEST_BODY:
        state->request_body_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS:
        state->response_headers_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_RESPONSE_BODY:
        state->response_body_processed = 1;
        return 1;
    case MSCONNECTOR_PHASE_LOGGING:
        state->logging_processed = 1;
        return 1;
    default:
        return 0;
    }
}

int msconnector_transaction_state_phase_processed(
    const msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (state == 0) {
        return 0;
    }

    switch (phase) {
    case MSCONNECTOR_PHASE_CONNECTION:
        return state->connection_processed;
    case MSCONNECTOR_PHASE_URI:
        return state->uri_processed;
    case MSCONNECTOR_PHASE_REQUEST_HEADERS:
        return state->request_headers_processed;
    case MSCONNECTOR_PHASE_REQUEST_BODY:
        return state->request_body_processed;
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS:
        return state->response_headers_processed;
    case MSCONNECTOR_PHASE_RESPONSE_BODY:
        return state->response_body_processed;
    case MSCONNECTOR_PHASE_LOGGING:
        return state->logging_processed;
    default:
        return 0;
    }
}

const char *msconnector_phase_name(enum msconnector_phase phase) {
    switch (phase) {
    case MSCONNECTOR_PHASE_CONNECTION:
        return "connection";
    case MSCONNECTOR_PHASE_URI:
        return "uri";
    case MSCONNECTOR_PHASE_REQUEST_HEADERS:
        return "request_headers";
    case MSCONNECTOR_PHASE_REQUEST_BODY:
        return "request_body";
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS:
        return "response_headers";
    case MSCONNECTOR_PHASE_RESPONSE_BODY:
        return "response_body";
    case MSCONNECTOR_PHASE_LOGGING:
        return "logging";
    default:
        return "unknown";
    }
}
