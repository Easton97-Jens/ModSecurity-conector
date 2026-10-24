//go:build libmodsecurity

#include "common_runtime_bridge.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "msconnector/memory.h"
#include "common/runtime/msconnector_runtime.h"
#include "connectors/profile_registry.h"

/* Same lifetime as MSCONNECTOR_ENVOY_EXT_AUTHZ_COMPANION_TTL_MS and
 * MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_TTL_MS in the canonical route adapters.
 * This is not the optional late-intervention deadline, whose default is 0. */
#define MSC_COMPOSITE_COMPANION_TTL_MS 30000ULL

struct msc_envoy_ext_proc_runtime {
    msconnector_runtime *runtime;
    unsigned int profile_id;
    msconnector_runtime_response_companion_registry *companion_registry;
};

struct msc_envoy_ext_proc_transaction {
    msconnector_runtime_transaction *transaction;
    msconnector_runtime *runtime;
    msconnector_runtime_response_companion_registry *companion_registry;
    msconnector_runtime_response_companion_session companion_session;
    char companion_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
    char transaction_id[129];
    int handed_off;
    int companion_claimed;
    int companion_consumed;
    int native_request_body_limit;
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

static void msc_transaction_set_decision(
    msc_envoy_ext_proc_transaction *transaction,
    msc_envoy_ext_proc_decision *out,
    const msconnector_decision *decision)
{
    msc_envoy_ext_proc_set_decision(out, decision, transaction->transaction);
    if (out != NULL) {
        msc_envoy_ext_proc_copy_text(out->transaction_id,
            sizeof(out->transaction_id), transaction->transaction_id);
    }
}

static void msc_transaction_observe_session_ownership(
    msc_envoy_ext_proc_transaction *transaction)
{
    if (transaction->companion_claimed && !transaction->companion_session.active) {
        /* Expiry/shutdown may destroy the session's native transaction on an
         * unsuccessful operation. Never retain its borrowed rule pointers. */
        memset(&transaction->disruptive_decision, 0,
            sizeof(transaction->disruptive_decision));
        transaction->has_disruptive_decision = 0;
        transaction->terminal = 1;
    }
}

static int msc_transaction_claim_companion(
    msc_envoy_ext_proc_transaction *transaction,
    char *error, size_t error_len)
{
    msconnector_error runtime_error;
    if (transaction->companion_claimed) {
        if (transaction->companion_session.active) {
            return 1;
        }
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common response companion session is no longer active");
        return 0;
    }
    if (!transaction->handed_off) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "Common response companion has not been handed off");
        return 0;
    }
    msconnector_error_init(&runtime_error);
    if (!msconnector_runtime_response_companion_claim_handle(
            transaction->companion_registry, transaction->companion_handle,
            &transaction->companion_session, &runtime_error)) {
        /* The handle is generated internally, never exposed, and consumed
         * only through this serialized wrapper. Missing + inactive therefore
         * proves expiry already detached/destroyed the unclaimed entry. */
        if (runtime_error.code == MSCONNECTOR_ERROR_CORRELATION_MISSING &&
            !transaction->companion_session.active) {
            transaction->companion_consumed = 1;
            transaction->terminal = 1;
            msconnector_secure_zero(transaction->companion_handle,
                sizeof(transaction->companion_handle));
        }
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response companion claim failed");
        return 0;
    }
    transaction->companion_claimed = 1;
    msconnector_secure_zero(transaction->companion_handle,
        sizeof(transaction->companion_handle));
    return 1;
}

int msc_envoy_ext_proc_transaction_claim_response_companion(
    msc_envoy_ext_proc_transaction *transaction, char *error, size_t error_len)
{
    if (transaction == NULL) {
        msc_envoy_ext_proc_set_error(error, error_len, "Common transaction is missing");
        return 0;
    }
    if (transaction->companion_registry == NULL) {
        return 1; /* compatibility: direct ext_proc has no companion registry */
    }
    return msc_transaction_claim_companion(transaction, error, error_len);
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
    msc_transaction_set_decision(transaction, decision, &native_decision);
    if (transaction->companion_registry != NULL && !transaction->terminal) {
        if (!msconnector_runtime_response_companion_handoff_with_handle(
                transaction->companion_registry, transaction->transaction,
                MSC_COMPOSITE_COMPANION_TTL_MS,
                transaction->companion_handle, &runtime_error)) {
            msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
                "Common response companion handoff failed");
            return 0;
        }
        transaction->handed_off = 1;
        transaction->transaction = NULL; /* registry owns the native transaction */
    }
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

    if (transaction == NULL ||
        (transaction->transaction == NULL && !transaction->companion_session.active)) {
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
    const int result = transaction->companion_registry != NULL ?
        msconnector_runtime_response_companion_session_finish_response_body(
            &transaction->companion_session, &native_decision, &runtime_error) :
        msconnector_runtime_transaction_finish_response_body(
            transaction->transaction, &native_decision, &runtime_error);
    if (!result) {
        msc_transaction_observe_session_ownership(transaction);
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response body finalization failed");
        return 0;
    }
    transaction->response_finished = 1;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_transaction_set_decision(transaction, decision, &native_decision);
    return 1;
}

static int msc_runtime_create_for_route(
    const char *config_path,
    const char *connector,
    const char *integration,
    const char *profile,
    msconnector_body_mode request_body_mode,
    msc_envoy_ext_proc_runtime **out,
    char *error,
    size_t error_len)
{
    msc_envoy_ext_proc_runtime *runtime;
    const msconnector_transaction_profile *selected_profile;

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
    if (!msconnector_runtime_create(connector, config_path,
            &runtime->runtime, error, error_len)) {
        free(runtime);
        return 0;
    }
    if (!msconnector_runtime_set_event_integration_mode(runtime->runtime,
            integration)) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "could not set Common event integration mode");
        msconnector_runtime_destroy(&runtime->runtime);
        free(runtime);
        return 0;
    }
    selected_profile = msconnector_profile_registry_find(profile);
    if (!msconnector_runtime_set_transaction_profile(runtime->runtime,
            selected_profile)) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "could not inject Common transaction profile");
        msconnector_runtime_destroy(&runtime->runtime);
        free(runtime);
        return 0;
    }
    runtime->profile_id = selected_profile->profile_id;
    if (msconnector_runtime_request_body_mode(runtime->runtime) !=
            request_body_mode ||
        msconnector_runtime_response_body_mode(runtime->runtime) !=
            MSCONNECTOR_BODY_MODE_STREAMING) {
        msc_envoy_ext_proc_set_error(error, error_len,
            request_body_mode == MSCONNECTOR_BODY_MODE_STREAMING ?
                "Envoy ext_proc Common runtime requires streaming request and response bodies" :
                "Composite Common runtime requires buffered request and streaming response bodies");
        msconnector_runtime_destroy(&runtime->runtime);
        free(runtime);
        return 0;
    }
    if (request_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED) {
        runtime->companion_registry = calloc(1U, sizeof(*runtime->companion_registry));
        if (runtime->companion_registry == NULL) {
            msc_envoy_ext_proc_set_error(error, error_len,
                "Common response companion registry allocation failed");
            msconnector_runtime_destroy(&runtime->runtime);
            free(runtime);
            return 0;
        }
        msconnector_runtime_response_companion_registry_init(runtime->companion_registry);
    }
    *out = runtime;
    return 1;
}

unsigned int msc_envoy_ext_proc_runtime_profile_id(
    const msc_envoy_ext_proc_runtime *runtime)
{
    return runtime == NULL ? 0U : runtime->profile_id;
}

int msc_envoy_ext_proc_runtime_create(
    const char *config_path,
    msc_envoy_ext_proc_runtime **out,
    char *error,
    size_t error_len)
{
    return msc_runtime_create_for_route(config_path, "envoy", "ext_proc",
        "envoy-ext-proc", MSCONNECTOR_BODY_MODE_STREAMING,
        out, error, error_len);
}

int msc_composite_runtime_create(
    const char *config_path,
    enum msc_composite_mode mode,
    msc_envoy_ext_proc_runtime **out,
    char *error,
    size_t error_len)
{
    switch (mode) {
        case MSC_COMPOSITE_ENVOY:
            return msc_runtime_create_for_route(config_path, "envoy", "ext_authz",
                "envoy-ext-authz", MSCONNECTOR_BODY_MODE_BUFFERED,
                out, error, error_len);
        case MSC_COMPOSITE_TRAEFIK:
            return msc_runtime_create_for_route(config_path, "traefik", "forwardAuth",
                "traefik-forwardauth", MSCONNECTOR_BODY_MODE_BUFFERED,
                out, error, error_len);
        default:
            if (out != NULL) {
                *out = NULL;
            }
            msc_envoy_ext_proc_set_error(error, error_len,
                "unsupported Composite runtime mode");
            return 0;
    }
}

int msc_envoy_ext_proc_runtime_quiesce(
    msc_envoy_ext_proc_runtime *runtime, char *error, size_t error_len)
{
    msconnector_error runtime_error;
    if (runtime == NULL || runtime->companion_registry == NULL) {
        return 1;
    }
    msconnector_error_init(&runtime_error);
    if (!msconnector_runtime_response_companion_registry_shutdown(
            runtime->companion_registry, &runtime_error)) {
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response companion registry did not quiesce");
        return 0;
    }
    return 1;
}

void msc_envoy_ext_proc_runtime_destroy(msc_envoy_ext_proc_runtime **runtime)
{
    msconnector_error runtime_error;
    if (runtime == NULL || *runtime == NULL) {
        return;
    }
    if ((*runtime)->companion_registry != NULL) {
        msconnector_error_init(&runtime_error);
        if (!msconnector_runtime_response_companion_registry_shutdown(
                (*runtime)->companion_registry, &runtime_error)) {
            return; /* fail closed: never free a leased native transaction */
        }
        free((*runtime)->companion_registry);
    }
    msconnector_runtime_destroy(&(*runtime)->runtime);
    free(*runtime);
    *runtime = NULL;
}

int msc_envoy_ext_proc_runtime_phase4_mode(
    const msc_envoy_ext_proc_runtime *runtime)
{
    if (runtime == NULL || runtime->runtime == NULL) {
        return MSC_ENVOY_EXT_PROC_PHASE4_MODE_UNSET;
    }
    switch (msconnector_runtime_phase4_mode(runtime->runtime)) {
      case MSCONNECTOR_PHASE4_MODE_OFF:
        return MSC_ENVOY_EXT_PROC_PHASE4_MODE_OFF;
      case MSCONNECTOR_PHASE4_MODE_SAFE:
        return MSC_ENVOY_EXT_PROC_PHASE4_MODE_SAFE;
      case MSCONNECTOR_PHASE4_MODE_STRICT:
        return MSC_ENVOY_EXT_PROC_PHASE4_MODE_STRICT;
      case MSCONNECTOR_PHASE4_MODE_UNSET:
      default:
        return MSC_ENVOY_EXT_PROC_PHASE4_MODE_UNSET;
    }
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
    result = runtime->companion_registry != NULL ?
        msconnector_runtime_transaction_begin_request_headers(runtime->runtime,
            &native_request, request->transaction_id, &transaction->transaction,
            &native_decision, &runtime_error) :
        msconnector_runtime_transaction_begin(runtime->runtime,
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
    transaction->companion_registry = runtime->companion_registry;
    msc_envoy_ext_proc_copy_text(transaction->transaction_id,
        sizeof(transaction->transaction_id),
        msconnector_runtime_transaction_id(transaction->transaction));
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_transaction_set_decision(transaction, decision, &native_decision);
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

    if (transaction == NULL ||
        (transaction->transaction == NULL && !transaction->handed_off) ||
        response == NULL || decision == NULL || response->protocol == NULL ||
        transaction->terminal || !transaction->request_finished ||
        transaction->response_headers_processed) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Common response-header lifecycle");
        return 0;
    }
    if (transaction->companion_registry != NULL &&
        !msc_transaction_claim_companion(transaction, error, error_len)) {
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
    result = transaction->companion_registry != NULL ?
        msconnector_runtime_response_companion_session_process_response_headers(
            &transaction->companion_session, &native_response, &native_decision,
            &runtime_error) :
        msconnector_runtime_transaction_process_response_headers(
            transaction->transaction, &native_response, &native_decision,
            &runtime_error);
    free(headers);
    if (!result) {
        msc_transaction_observe_session_ownership(transaction);
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response-header processing failed");
        return 0;
    }
    transaction->response_headers_processed = 1;
    transaction->terminal = native_decision.disruptive != 0;
	msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
    msc_transaction_set_decision(transaction, decision, &native_decision);
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
    const msc_envoy_ext_proc_body *body,
    msc_envoy_ext_proc_decision *decision,
    char *error,
    size_t error_len)
{
    msconnector_error runtime_error;
    msconnector_decision native_decision;
    int result;

    if (transaction == NULL ||
        (transaction->transaction == NULL && !transaction->handed_off) ||
        body == NULL || decision == NULL || transaction->terminal ||
        (body->body_size > 0U && body->body == NULL)) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "invalid Common body lifecycle");
        return 0;
    }
    if ((!body->response_direction && transaction->request_finished) ||
        (body->response_direction && (!transaction->response_headers_processed ||
            transaction->response_finished))) {
        msc_envoy_ext_proc_set_error(error, error_len,
            "body arrived after Common end-of-stream");
        return 0;
    }
    if (body->response_direction) {
        if (!msc_envoy_ext_proc_transaction_mark_response_committed(transaction,
                1, error, error_len)) {
            return 0;
        }
    }
    msconnector_error_init(&runtime_error);
    if (body->response_direction) {
        result = transaction->companion_registry != NULL ?
            msconnector_runtime_response_companion_session_append_response_body_chunk(
                &transaction->companion_session, body->body, body->body_size, &runtime_error) :
            msconnector_runtime_transaction_append_response_body_chunk(
                transaction->transaction, body->body, body->body_size, &runtime_error);
    } else {
        result = msconnector_runtime_transaction_append_request_body_chunk(
            transaction->transaction, body->body, body->body_size, &runtime_error);
    }
    if (!result) {
        if (!body->response_direction &&
            runtime_error.code == MSCONNECTOR_ERROR_BODY_TOO_LARGE) {
            msconnector_runtime_transaction_snapshot snapshot;
            if (msconnector_runtime_transaction_snapshot_get(transaction->transaction,
                    &snapshot) &&
                snapshot.contract.status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL &&
                snapshot.contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT) {
                transaction->terminal = 1;
                transaction->native_request_body_limit = 1;
                msconnector_decision_set_body_limit(&native_decision,
                    "request body exceeds configured limit");
                native_decision.phase = MSCONNECTOR_PHASE_REQUEST_BODY;
                msc_envoy_ext_proc_remember_disruptive_decision(transaction, &native_decision);
                msc_transaction_set_decision(transaction, decision, &native_decision);
                return 1;
            }
        }
        msc_transaction_observe_session_ownership(transaction);
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            body->response_direction ? "Common response-body append failed" :
            "Common request-body append failed");
        return 0;
    }
    msconnector_decision_init(&native_decision);
    native_decision.phase = body->response_direction ? MSCONNECTOR_PHASE_RESPONSE_BODY :
        MSCONNECTOR_PHASE_REQUEST_BODY;
    msc_transaction_set_decision(transaction, decision, &native_decision);
    if (!body->end_of_stream) {
        return 1;
    }
    if (body->response_direction) {
        return msc_envoy_ext_proc_finish_response(transaction, decision, error,
            error_len);
    }
    return msc_envoy_ext_proc_finish_request(transaction, decision, error,
        error_len);
}

int msc_envoy_ext_proc_transaction_mark_response_committed(
    msc_envoy_ext_proc_transaction *transaction,
    int body_started, char *error, size_t error_len)
{
    msconnector_error runtime_error;
    int result;
    if (transaction == NULL || !transaction->response_headers_processed) {
        msc_envoy_ext_proc_set_error(error, error_len, "response commitment before headers");
        return 0;
    }
    msconnector_error_init(&runtime_error);
    result = transaction->companion_registry != NULL ?
        msconnector_runtime_response_companion_session_set_response_commit_state(
            &transaction->companion_session, 1, body_started != 0, &runtime_error) :
        msconnector_runtime_transaction_set_response_commit_state_checked(
            transaction->transaction, 1, body_started != 0, &runtime_error);
    if (!result) {
        msc_transaction_observe_session_ownership(transaction);
        msc_envoy_ext_proc_set_runtime_error(error, error_len, &runtime_error,
            "Common response commitment failed");
    }
    return result;
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

    if (transaction == NULL ||
        (transaction->transaction == NULL && !transaction->companion_session.active) ||
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
    const int result = transaction->companion_claimed ?
        msconnector_runtime_response_companion_session_record_host_action(
            &transaction->companion_session, &transaction->disruptive_decision,
            native_action, visible_status, transport_result, 0, &runtime_error) :
        msconnector_runtime_transaction_record_host_action(
            transaction->transaction, &transaction->disruptive_decision,
            native_action, visible_status, transport_result, 0, &runtime_error);
    if (!result) {
        msc_transaction_observe_session_ownership(transaction);
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
    return transaction == NULL ? NULL : transaction->transaction_id;
}

static int msc_transaction_close_session(
    msc_envoy_ext_proc_transaction *transaction, int completed,
    msconnector_error *error)
{
    const int result = completed ?
        msconnector_runtime_response_companion_session_release(
            &transaction->companion_session, error) :
        msconnector_runtime_response_companion_session_cancel(
            &transaction->companion_session, 0, error);
    /* A failed release/cancel may have consumed ownership. Success alone
     * cannot authorize freeing the wrapper while the session stays active. */
    if (transaction->companion_session.active) {
        return MSC_COMMON_CLOSE_UNRESOLVED;
    }
    return result ? MSC_COMMON_CLOSE_OK : MSC_COMMON_CLOSE_CONSUMED_ERROR;
}

int msc_envoy_ext_proc_transaction_close(
    msc_envoy_ext_proc_transaction *transaction, int request_rejected)
{
    msconnector_error runtime_error;
    int close_result = MSC_COMMON_CLOSE_OK;

    if (transaction == NULL) {
        return 1;
    }
    if (transaction->handed_off && !transaction->companion_consumed) {
        msconnector_error_init(&runtime_error);
        if (transaction->companion_session.active) {
            close_result = msc_transaction_close_session(transaction,
                    transaction->terminal || transaction->response_finished,
                    &runtime_error);
            if (close_result == MSC_COMMON_CLOSE_UNRESOLVED) {
                return 0; /* caller must stop the runtime, ownership is unresolved */
            }
        } else if (!transaction->companion_claimed) {
            /* Closing before P3 is still a cancellation, not a successful
             * companion finish. Claim privately to preserve that outcome. */
            char claim_error[512];
            if (msc_transaction_claim_companion(transaction, claim_error,
                    sizeof(claim_error))) {
                close_result = msc_transaction_close_session(transaction, 0, &runtime_error);
                if (close_result == MSC_COMMON_CLOSE_UNRESOLVED) {
                    return 0;
                }
            } else if (!transaction->companion_consumed) {
                if (!msconnector_runtime_response_companion_revoke_handle(
                        transaction->companion_registry, transaction->companion_handle,
                        &runtime_error)) {
                    return 0; /* cannot prove registry ownership was consumed */
                }
            }
        }
    }
    if (transaction->native_request_body_limit) {
        msconnector_runtime_transaction_snapshot snapshot;
        if (transaction->transaction == NULL ||
            !msconnector_runtime_transaction_snapshot_get(transaction->transaction,
                &snapshot) ||
            snapshot.contract.status != MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ||
            snapshot.contract.error_class != MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT) {
            return MSC_COMMON_CLOSE_UNRESOLVED;
        }
        /* A failed/cancelled 413 Send has no host-action receipt, but the
         * native budget decision is already terminal and ownership is known.
         * Cancellation cannot rewrite that terminal contract. Finish logging
         * without inventing a receipt, then release the owned transaction.
         */
        if (!msconnector_runtime_transaction_finish_host_rejected_request_body(
                transaction->transaction, &runtime_error)) {
            return MSC_COMMON_CLOSE_UNRESOLVED;
        }
    } else if (transaction->transaction != NULL &&
        !transaction->terminal && !transaction->response_finished) {
        msconnector_error_init(&runtime_error);
        if (transaction->companion_registry != NULL && request_rejected &&
            !transaction->request_finished) {
            if (!msconnector_runtime_transaction_fail(transaction->transaction,
                    MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, &runtime_error) ||
                !msconnector_runtime_transaction_record_failure_host_action(
                    transaction->transaction, 413, 0, &runtime_error) ||
                !msconnector_runtime_transaction_finish_host_rejected_request_body(
                    transaction->transaction, &runtime_error)) {
                return 0;
            }
        } else {
            if (!msconnector_runtime_transaction_cancel(transaction->transaction,
                    0, &runtime_error)) {
                return 0;
            }
        }
    } else if (transaction->transaction != NULL &&
        (transaction->terminal || (transaction->request_finished &&
            (!transaction->response_headers_processed ||
                transaction->response_finished)))) {
        msconnector_error_init(&runtime_error);
        if (!msconnector_runtime_transaction_finish(transaction->transaction,
                &runtime_error)) {
            return 0;
        }
    }
    msconnector_runtime_transaction_destroy(&transaction->transaction);
    msconnector_secure_zero(transaction, sizeof(*transaction));
    free(transaction);
    return close_result;
}
