#ifndef MSCONNECTOR_TEST_HTTP_AUTHORIZATION_REQUEST_STREAM_STUBS_H
#define MSCONNECTOR_TEST_HTTP_AUTHORIZATION_REQUEST_STREAM_STUBS_H

#include <assert.h>
#include <stdint.h>

/* These three HTTP service fixtures share request-stream bookkeeping.
 * Their existing transaction structs supply these fields so the stubs model
 * complete offered-byte accounting and preserve EOS/terminal ordering. */
msconnector_body_mode msconnector_runtime_request_body_mode(const msconnector_runtime *runtime) {
    (void)runtime;
    return MSCONNECTOR_BODY_MODE_BUFFERED;
}

int msconnector_runtime_transaction_append_request_body_chunk(msconnector_runtime_transaction *transaction,
    const unsigned char *body, size_t size, msconnector_error *error) {
    msconnector_error_init(error);
    if (transaction == NULL) return 0;
    if (transaction->request_body_finished ||
        transaction->request_body_failure != MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        msconnector_error_set(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "request append after EOS or terminal failure", "fixture");
        return 0;
    }
    if ((size > 0U && body == NULL) || size > SIZE_MAX - transaction->request_body_bytes) {
        msconnector_error_set(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "invalid request chunk or accounting overflow", "fixture");
        return 0;
    }
    transaction->request_body_bytes += size;
    return 1;
}

int msconnector_runtime_transaction_finish_request_body(msconnector_runtime_transaction *transaction,
    msconnector_decision *decision, msconnector_error *error) {
    msconnector_error_init(error);
    if (transaction == NULL) return 0;
    if (transaction->request_body_finished ||
        transaction->request_body_failure != MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        msconnector_error_set(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "request EOS after EOS or terminal failure", "fixture");
        return 0;
    }
    transaction->request_body_finished = 1;
    msconnector_decision_set_allow(decision);
    return 1;
}

int msconnector_runtime_transaction_fail(msconnector_runtime_transaction *transaction,
    msconnector_transaction_error_class error_class, msconnector_error *error) {
    msconnector_error_init(error);
    if (transaction == NULL) return 0;
    if (transaction->request_body_failure == MSCONNECTOR_TRANSACTION_ERROR_NONE)
        transaction->request_body_failure = error_class;
    return 1;
}

static void msconnector_test_request_stream_stubs_smoke(void) {
    msconnector_runtime_transaction transaction = {0};
    msconnector_error error;
    msconnector_decision decision;
    const unsigned char body[] = "body";
    assert(msconnector_runtime_transaction_append_request_body_chunk(&transaction, body, 2U, &error));
    assert(msconnector_runtime_transaction_append_request_body_chunk(&transaction, body + 2U, 2U, &error));
    assert(transaction.request_body_bytes == 4U);
    assert(msconnector_runtime_transaction_finish_request_body(&transaction, &decision, &error));
    assert(transaction.request_body_finished == 1);
    assert(!msconnector_runtime_transaction_finish_request_body(&transaction, &decision, &error));
    assert(!msconnector_runtime_transaction_append_request_body_chunk(&transaction, body, 1U, &error));
    assert(transaction.request_body_bytes == 4U);
    transaction = (msconnector_runtime_transaction){0};
    assert(msconnector_runtime_transaction_fail(&transaction, MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL, &error));
    assert(msconnector_runtime_transaction_fail(&transaction, MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, &error));
    assert(transaction.request_body_failure == MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL);
    assert(!msconnector_runtime_transaction_append_request_body_chunk(&transaction, body, 1U, &error));
    assert(!msconnector_runtime_transaction_finish_request_body(&transaction, &decision, &error));
    assert(transaction.request_body_finished == 0);
    assert(transaction.request_body_bytes == 0U);
}
#endif
