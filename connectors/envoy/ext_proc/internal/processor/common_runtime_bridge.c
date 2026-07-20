//go:build libmodsecurity

#include "common_runtime_bridge.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "common/runtime/msconnector_runtime.h"

struct msc_envoy_ext_proc_runtime {
    msconnector_runtime *runtime;
};

struct msc_envoy_ext_proc_transaction {
    msconnector_runtime_transaction *transaction;
    msconnector_runtime *runtime;
    msconnector_decision disruptive_decision;
    int request_finished;
    int response_headers_processed;
    int response_finished;
    int terminal;
    int has_disruptive_decision;
    int host_action_recorded;
};

static void msc_envoy_ext_proc_set_error(char *error, size_t error_len,
    const char *message)
{
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s",
            message == NULL || message[0] == '\0' ? "Common runtime failure" : message);
    }
}

static void msc_envoy_ext_proc_set_runtime_error(char *error, size_t error_len,
    const msconnector_error *runtime_error, const char *fallback)
{
    if (runtime_error != NULL && runtime_error->message != NULL &&
        runtime_error->message[0] != '\0') {
        msc_envoy_ext_proc_set_error(error, error_len, runtime_error->message);
        return;
    }
    msc_envoy_ext_proc_set_error(error, error_len, fallback);
}

static void msc_envoy_ext_proc_copy_text(char *destination,
    size_t destination_size, const char *source)
{
    if (destination == NULL || destination_size == 0U) {
        return;
    }
    (void)snprintf(destination, destination_size, "%s",
        source == NULL ? "" : source);
}

static void msc_envoy_ext_proc_set_decision(
    msc_envoy_ext_proc_decision *out,
    const msconnector_decision *decision,
    const msconnector_runtime_transaction *transaction)
{
    if (out == NULL) {
        return;
    }
    memset(out, 0, sizeof(*out));
    out->action = MSC_ENVOY_EXT_PROC_ALLOW;
    if (decision != NULL) {
        out->status = msconnector_decision_http_status(decision);
        out->phase = (int)decision->phase;
        out->disruptive = decision->disruptive != 0;
        if (decision->kind == MSCONNECTOR_DECISION_KIND_REDIRECT) {
            out->action = MSC_ENVOY_EXT_PROC_REDIRECT;
        } else if (decision->kind != MSCONNECTOR_DECISION_KIND_ALLOW &&
            decision->kind != MSCONNECTOR_DECISION_KIND_LOG_ONLY) {
            out->action = MSC_ENVOY_EXT_PROC_DENY;
        }
        msc_envoy_ext_proc_copy_text(out->rule_id, sizeof(out->rule_id),
            decision->rule_id);
        msc_envoy_ext_proc_copy_text(out->redirect_url,
            sizeof(out->redirect_url), decision->redirect_url);
    }
    if (transaction != NULL) {
        msc_envoy_ext_proc_copy_text(out->transaction_id,
            sizeof(out->transaction_id),
            msconnector_runtime_transaction_id(transaction));
    }
}

static void msc_envoy_ext_proc_remember_disruptive_decision(
    msc_envoy_ext_proc_transaction *transaction,
    const msconnector_decision *decision)
{
    if (transaction == NULL || decision == NULL || !decision->disruptive) {
        return;
    }
    transaction->disruptive_decision = *decision;
    transaction->has_disruptive_decision = 1;
}

static int msc_envoy_ext_proc_headers(
    const msc_envoy_ext_proc_header *source,
    size_t count,
    msconnector_header **out,
    char *error,
    size_t error_len)
{
    msconnector_header *headers;

    if (out == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common header output is required");
        return 0;
    }
    *out = NULL;
    if (count == 0U) {
        return 1;
    }
    if (source == NULL || count > SIZE_MAX / sizeof(*headers)) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Envoy header input");
        return 0;
    }
    headers = calloc(count, sizeof(*headers));
    if (headers == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common header allocation failed");
        return 0;
    }
    for (size_t index = 0U; index < count; ++index) {
        if (source[index].name == NULL || source[index].name_size == 0U ||
            (source[index].value == NULL && source[index].value_size != 0U)) {
            free(headers);
            msc_envoy_ext_proc_set_error(error, error_len,
                "invalid Envoy header field");
            return 0;
        }
        headers[index].name = source[index].name;
        headers[index].name_size = source[index].name_size;
        headers[index].value = source[index].value;
        headers[index].value_size = source[index].value_size;
    }
    *out = headers;
    return 1;
}

static int msc_envoy_ext_proc_finish_request(
    msc_envoy_ext_proc_transaction *transaction,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_error runtime_error;
    msconnector_decision native_decision;

    if (transaction == NULL || transaction->transaction == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common request transaction is missing");
        return 0;
    }
    if (transaction->request_finished) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "request body end-of-stream was already processed");
        return 0;
    }
    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&native_decision);
    if (!msconnector_runtime_transaction_finish_request_body(
            transaction->transaction, &native_decision, &runtime_error)) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common request body finalization failed");
        return 0;
    }
    transaction->request_finished = 1;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_envoy_ext_proc_set_decision(decision, &native_decision,
        transaction->transaction);
    return 1;
}

static int msc_envoy_ext_proc_finish_response(
    msc_envoy_ext_proc_transaction *transaction,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_error runtime_error;
    msconnector_decision native_decision;

    if (transaction == NULL || transaction->transaction == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common response transaction is missing");
        return 0;
    }
    if (transaction->response_finished) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "response body end-of-stream was already processed");
        return 0;
    }
    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&native_decision);
    if (!msconnector_runtime_transaction_finish_response_body(
            transaction->transaction, &native_decision, &runtime_error)) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response body finalization failed");
        return 0;
    }
    transaction->response_finished = 1;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_envoy_ext_proc_set_decision(decision, &native_decision,
        transaction->transaction);
    return 1;
}

int msc_envoy_ext_proc_runtime_create(
    const char *config_path,
    msc_envoy_ext_proc_runtime **out,
    char *error,
    size_t error_len)
{
    msc_envoy_ext_proc_runtime *runtime;

    if (out != NULL) {
        *out = NULL;
    }
    if (out == NULL || config_path == NULL || config_path[0] == '\0') {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common runtime configuration path is required");
        return 0;
    }
    runtime = calloc(1U, sizeof(*runtime));
    if (runtime == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common runtime allocation failed");
        return 0;
    }
    /* Common event identity must remain the canonical connector name. The
     * ext_proc label belongs in integration_mode, never in connector. */
    if (!msconnector_runtime_create("envoy", config_path,
            &runtime->runtime, error, error_len)) {
        free(runtime);
        return 0;
    }
    if (!msconnector_runtime_set_event_integration_mode(runtime->runtime,
            "ext_proc")) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "could not set Common event integration mode");
        msconnector_runtime_destroy(&runtime->runtime);
        free(runtime);
        return 0;
    }
    if (msconnector_runtime_request_body_mode(runtime->runtime) !=
            MSCONNECTOR_BODY_MODE_STREAMING ||
        msconnector_runtime_response_body_mode(runtime->runtime) !=
            MSCONNECTOR_BODY_MODE_STREAMING) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Envoy ext_proc Common runtime requires streaming request and response bodies");
        msconnector_runtime_destroy(&runtime->runtime);
        free(runtime);
        return 0;
    }
    *out = runtime;
    return 1;
}

void msc_envoy_ext_proc_runtime_destroy(msc_envoy_ext_proc_runtime **runtime)
{
    if (runtime == NULL || *runtime == NULL) {
        return;
    }
    msconnector_runtime_destroy(&(*runtime)->runtime);
    free(*runtime);
    *runtime = NULL;
}

int msc_envoy_ext_proc_transaction_begin(
    msc_envoy_ext_proc_runtime *runtime,
    const msc_envoy_ext_proc_request *request,
    int end_of_stream,
    msc_envoy_ext_proc_transaction **out,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_request native_request;
    msconnector_header *headers = NULL;
    msconnector_error runtime_error;
    msconnector_decision native_decision;
    msc_envoy_ext_proc_transaction *transaction;
    int result;

    if (out != NULL) {
        *out = NULL;
    }
    if (runtime == NULL || runtime->runtime == NULL || request == NULL ||
        out == NULL || decision == NULL || request->method == NULL ||
        request->uri == NULL || request->protocol == NULL ||
        request->client_address == NULL || request->server_address == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common request metadata is incomplete");
        return 0;
    }
    if (!msc_envoy_ext_proc_headers(request->headers, request->header_count,
            &headers, error, error_len)) {
        return 0;
    }
    memset(&native_request, 0, sizeof(native_request));
    native_request.method = request->method;
    native_request.uri = request->uri;
    native_request.http_version = request->protocol;
    native_request.hostname = request->hostname;
    native_request.client.address = request->client_address;
    native_request.client.port = request->client_port;
    native_request.server.address = request->server_address;
    native_request.server.port = request->server_port;
    native_request.headers = headers;
    native_request.header_count = request->header_count;
    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&native_decision);
    transaction = calloc(1U, sizeof(*transaction));
    if (transaction == NULL) {
        free(headers);
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common transaction allocation failed");
        return 0;
    }
    result = msconnector_runtime_transaction_begin(runtime->runtime,
        &native_request, request->transaction_id, &transaction->transaction,
        &native_decision, &runtime_error);
    free(headers);
    if (!result || transaction->transaction == NULL) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common request-header processing failed");
        msconnector_runtime_transaction_destroy(&transaction->transaction);
        free(transaction);
        return 0;
    }
    transaction->runtime = runtime->runtime;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_envoy_ext_proc_set_decision(decision, &native_decision,
        transaction->transaction);
    if (end_of_stream) {
        if (msconnector_runtime_request_body_mode(runtime->runtime) ==
            MSCONNECTOR_BODY_MODE_NONE) {
            transaction->request_finished = 1;
        } else if (!transaction->terminal && !msc_envoy_ext_proc_finish_request(
                transaction, decision, error, error_len)) {
            msconnector_runtime_transaction_destroy(&transaction->transaction);
            free(transaction);
            return 0;
        } else if (transaction->terminal) {
            transaction->request_finished = 1;
        }
    }
    *out = transaction;
    return 1;
}

int msc_envoy_ext_proc_transaction_process_response_headers(
    msc_envoy_ext_proc_transaction *transaction,
    const msc_envoy_ext_proc_response *response,
    int end_of_stream,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_response native_response;
    msconnector_header *headers = NULL;
    msconnector_error runtime_error;
    msconnector_decision native_decision;
    int result;

    if (transaction == NULL || transaction->transaction == NULL ||
        response == NULL || decision == NULL || response->protocol == NULL ||
        transaction->terminal || !transaction->request_finished ||
        transaction->response_headers_processed) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Common response-header lifecycle");
        return 0;
    }
    if (!msc_envoy_ext_proc_headers(response->headers, response->header_count,
            &headers, error, error_len)) {
        return 0;
    }
    memset(&native_response, 0, sizeof(native_response));
    native_response.status = response->status;
    native_response.http_version = response->protocol;
    native_response.headers = headers;
    native_response.header_count = response->header_count;
    msconnector_error_init(&runtime_error);
    msconnector_decision_init(&native_decision);
    result = msconnector_runtime_transaction_process_response_headers(
        transaction->transaction, &native_response, &native_decision,
        &runtime_error);
    free(headers);
    if (!result) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response-header processing failed");
        return 0;
    }
    transaction->response_headers_processed = 1;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_envoy_ext_proc_set_decision(decision, &native_decision,
        transaction->transaction);
    if (end_of_stream) {
        if (msconnector_runtime_response_body_mode(transaction->runtime) ==
            MSCONNECTOR_BODY_MODE_NONE) {
            transaction->response_finished = 1;
        } else if (!transaction->terminal && !msc_envoy_ext_proc_finish_response(
                transaction, decision, error, error_len)) {
            return 0;
        } else if (transaction->terminal) {
            transaction->response_finished = 1;
        }
    }
    return 1;
}

int msc_envoy_ext_proc_transaction_process_body(
    msc_envoy_ext_proc_transaction *transaction,
    int response_direction,
    const unsigned char *body,
    size_t body_size,
    int end_of_stream,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_error runtime_error;
    msconnector_decision native_decision;
    int result;

    if (transaction == NULL || transaction->transaction == NULL ||
        decision == NULL || transaction->terminal ||
        (body_size > 0U && body == NULL)) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Common body lifecycle");
        return 0;
    }
    if ((!response_direction && transaction->request_finished) ||
        (response_direction && (!transaction->response_headers_processed ||
            transaction->response_finished))) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "body arrived after Common end-of-stream");
        return 0;
    }
    if (response_direction) {
        msc_envoy_ext_proc_transaction_mark_response_committed(transaction, 1);
    }
    msconnector_error_init(&runtime_error);
    if (response_direction) {
        result = msconnector_runtime_transaction_append_response_body_chunk(
            transaction->transaction, body, body_size, &runtime_error);
    } else {
        result = msconnector_runtime_transaction_append_request_body_chunk(
            transaction->transaction, body, body_size, &runtime_error);
    }
    if (!result) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            response_direction ? "Common response-body append failed" :
            "Common request-body append failed");
        return 0;
    }
    msconnector_decision_init(&native_decision);
    native_decision.phase = response_direction ? MSCONNECTOR_PHASE_RESPONSE_BODY :
        MSCONNECTOR_PHASE_REQUEST_BODY;
    msc_envoy_ext_proc_set_decision(decision, &native_decision,
        transaction->transaction);
    if (!end_of_stream) {
        return 1;
    }
    if (response_direction) {
        return msc_envoy_ext_proc_finish_response(transaction, decision, error,
            error_len);
    }
    return msc_envoy_ext_proc_finish_request(transaction, decision, error,
        error_len);
}

void msc_envoy_ext_proc_transaction_mark_response_committed(
    msc_envoy_ext_proc_transaction *transaction,
    int body_started)
{
    if (transaction == NULL || transaction->transaction == NULL) {
        return;
    }
    msconnector_runtime_transaction_set_response_commit_state(
        transaction->transaction, 1, body_started != 0);
}

int msc_envoy_ext_proc_transaction_record_host_action(
    msc_envoy_ext_proc_transaction *transaction,
    int action,
    int visible_status,
    const char *transport_result,
    char *error,
    size_t error_len)
{
    msconnector_error runtime_error;
    msconnector_decision_action native_action;

    if (transaction == NULL || transaction->transaction == NULL ||
        !transaction->has_disruptive_decision ||
        transaction->host_action_recorded) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common host action has no pending disruptive decision");
        return 0;
    }
    switch (action) {
      case MSC_ENVOY_EXT_PROC_DENY:
        native_action = MSCONNECTOR_DECISION_ACTION_DENY;
        break;
      case MSC_ENVOY_EXT_PROC_REDIRECT:
        native_action = MSCONNECTOR_DECISION_ACTION_REDIRECT;
        break;
      case MSC_ENVOY_EXT_PROC_LOG_ONLY:
        native_action = MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
        /* The engine decision was discovered after the real response commit;
         * this confirmation records the adapter's actual late log-only outcome. */
        transaction->disruptive_decision.late_intervention = 1;
        break;
      default:
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Envoy host action");
        return 0;
    }
    msconnector_error_init(&runtime_error);
    if (!msconnector_runtime_transaction_record_host_action(
            transaction->transaction, &transaction->disruptive_decision,
            native_action, visible_status, transport_result, 0,
            &runtime_error)) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common host action recording failed");
        return 0;
    }
    transaction->host_action_recorded = 1;
    return 1;
}

const char *msc_envoy_ext_proc_transaction_id(
    const msc_envoy_ext_proc_transaction *transaction)
{
    return transaction == NULL || transaction->transaction == NULL ? NULL :
        msconnector_runtime_transaction_id(transaction->transaction);
}

void msc_envoy_ext_proc_transaction_close(
    msc_envoy_ext_proc_transaction *transaction)
{
    msconnector_error runtime_error;

    if (transaction == NULL) {
        return;
    }
    if (transaction->transaction != NULL &&
        (transaction->terminal || (transaction->request_finished &&
            (!transaction->response_headers_processed ||
                transaction->response_finished)))) {
        msconnector_error_init(&runtime_error);
        (void)msconnector_runtime_transaction_finish(transaction->transaction,
            &runtime_error);
    }
    msconnector_runtime_transaction_destroy(&transaction->transaction);
    memset(transaction, 0, sizeof(*transaction));
    free(transaction);
}
