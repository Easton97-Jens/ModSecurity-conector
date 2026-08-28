#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200809L
#endif

#include "msconnector/modsecurity_engine.h"

#include <stdint.h>
#include <string.h>
#include <time.h>

/* The native-engine adapter owns several contract transitions itself.  Keep
 * their timestamps on the same monotonic clock as the Common Runtime rather
 * than writing the historical zero placeholder into a terminal snapshot. */
static uint64_t engine_contract_now_ms(void)
{
    struct timespec now;

#if defined(_WIN32)
    if (timespec_get(&now, TIME_UTC) != TIME_UTC || now.tv_sec < 0) {
#else
    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0 || now.tv_sec < 0) {
#endif
        return 0U;
    }
    return (uint64_t)now.tv_sec * UINT64_C(1000) +
        (uint64_t)now.tv_nsec / UINT64_C(1000000);
}

static int fail_error(msconnector_error *error, msconnector_error_code code, const char *message)
{
    msconnector_error_set(error, code, message, "modsecurity_engine");
    return 0;
}

static int tx_ready(const msconnector_modsecurity_transaction *tx, msconnector_error *error)
{
    if (tx == 0 || tx->engine == 0 || tx->native_transaction == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "transaction is not initialized");
    }
    if (!tx->engine->initialized) {
        return fail_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, "engine is not initialized");
    }
    return 1;
}

static int is_business_phase(enum msconnector_phase phase)
{
    return phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase == MSCONNECTOR_PHASE_REQUEST_BODY ||
        phase == MSCONNECTOR_PHASE_RESPONSE_HEADERS ||
        phase == MSCONNECTOR_PHASE_RESPONSE_BODY;
}

static msconnector_transaction_contract *canonical_contract(
    msconnector_modsecurity_transaction *tx)
{
    if (tx == 0) {
        return 0;
    }
    if (tx->contract != 0) {
        return tx->contract;
    }
    return &tx->state.contract;
}

static const msconnector_transaction_contract *canonical_contract_const(
    const msconnector_modsecurity_transaction *tx)
{
    if (tx == 0) {
        return 0;
    }
    if (tx->contract != 0) {
        return tx->contract;
    }
    return &tx->state.contract;
}

static int contract_phase_is_active(const msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase)
{
    const msconnector_transaction_contract *contract = canonical_contract_const(tx);

    return is_business_phase(phase) && contract != 0 &&
        contract->active_phase == (int)phase;
}

static void fail_contract_from_error(msconnector_modsecurity_transaction *tx,
    const msconnector_error *error)
{
    msconnector_transaction_error_class error_class =
        MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;

    if (tx == 0) {
        return;
    }
    if (error != 0) {
        switch (error->code) {
        case MSCONNECTOR_ERROR_TIMEOUT:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT;
            break;
        case MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE;
            break;
        case MSCONNECTOR_ERROR_BODY_TOO_LARGE:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT;
            break;
        case MSCONNECTOR_ERROR_EVENT_TOO_LARGE:
        case MSCONNECTOR_ERROR_LOG_MESSAGE_TOO_LARGE:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_EVENT_LIMIT;
            break;
        case MSCONNECTOR_ERROR_HEADER_TOO_LARGE:
        case MSCONNECTOR_ERROR_PROTOCOL:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
            break;
        case MSCONNECTOR_ERROR_PHASE_SEQUENCE:
            error_class = MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE;
            break;
        default:
            break;
        }
    }
    (void)msconnector_transaction_contract_fail(canonical_contract(tx), error_class,
        engine_contract_now_ms());
}

static int begin_contract_phase_for_route(
    msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase,
    int companion,
    msconnector_error *error)
{
    if (is_business_phase(phase) && tx->contract != 0) {
        if ((companion ? msconnector_transaction_contract_begin_companion_phase(
                canonical_contract(tx), phase, engine_contract_now_ms()) :
                msconnector_transaction_contract_begin_phase(
                    canonical_contract(tx), phase, engine_contract_now_ms())) ==
            MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
            return 1;
        }
    } else if (msconnector_transaction_state_begin_phase(&tx->state, phase)) {
        return 1;
    }
    {
        return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "transaction phase is duplicate, skipped, late, or terminal");
    }
}

static int begin_contract_phase(msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase, msconnector_error *error)
{
    return begin_contract_phase_for_route(tx, phase, 0, error);
}

static int begin_companion_contract_phase(msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase, msconnector_error *error)
{
    return begin_contract_phase_for_route(tx, phase, 1, error);
}

/* A streaming append opens P2/P4 at the first observed chunk.  The matching
 * EOS callback must then resume that active phase and complete it exactly
 * once, rather than trying to begin a duplicate phase. */
static int begin_or_resume_contract_phase(
    msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase,
    msconnector_error *error)
{
    return contract_phase_is_active(tx, phase) ? 1 :
        begin_contract_phase(tx, phase, error);
}

static int begin_or_resume_companion_contract_phase(
    msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase,
    msconnector_error *error)
{
    return contract_phase_is_active(tx, phase) ? 1 :
        begin_companion_contract_phase(tx, phase, error);
}

static int complete_contract_phase(
    msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase,
    msconnector_error *error)
{
    if (is_business_phase(phase) && tx->contract != 0) {
        if (msconnector_transaction_contract_complete_phase(canonical_contract(tx), phase,
                engine_contract_now_ms()) ==
            MSCONNECTOR_TRANSACTION_TRANSITION_OK &&
            msconnector_transaction_state_note_phase(&tx->state, phase)) {
            return 1;
        }
    } else if (msconnector_transaction_state_complete_phase(&tx->state, phase)) {
        return 1;
    }
    {
        return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "transaction phase could not be completed");
    }
}

static int record_engine_decision(
    msconnector_modsecurity_transaction *tx,
    const msconnector_decision *decision,
    msconnector_error *error)
{
    if (decision == 0) {
        return 1;
    }
    if (decision->body_limit != 0) {
        if (!msconnector_decision_is_body_limit(decision)) {
            (void)msconnector_transaction_contract_fail(canonical_contract(tx),
                MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
                engine_contract_now_ms());
            return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
                "body-limit decision violates the shared transaction contract");
        }
        if (msconnector_transaction_contract_fail(canonical_contract(tx),
                MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT,
                engine_contract_now_ms()) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
            return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
                "body-limit decision could not terminate the shared transaction contract");
        }
        return 1;
    }
    if (msconnector_transaction_contract_record_decision(canonical_contract(tx),
            msconnector_transaction_decision_kind_from_engine(decision),
            decision->rule_id, engine_contract_now_ms()) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "engine decision violates the shared transaction contract");
    }
    return 1;
}

void msconnector_modsecurity_engine_init(
    msconnector_modsecurity_engine *engine,
    const msconnector_modsecurity_engine_ops *ops)
{
    if (engine == 0) {
        return;
    }
    memset(engine, 0, sizeof(*engine));
    if (ops != 0) {
        engine->ops = *ops;
    }
}

int msconnector_modsecurity_engine_start(msconnector_modsecurity_engine *engine, msconnector_error *error)
{
    if (engine == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "engine is required");
    }
    if (engine->ops.init == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "engine init is unsupported");
    }
    if (!engine->ops.init(engine->ops.userdata, error)) {
        return 0;
    }
    engine->initialized = 1;
    return 1;
}

void msconnector_modsecurity_engine_destroy_rules(msconnector_modsecurity_engine *engine)
{
    if (engine != 0 && engine->rules_set != 0) {
        if (engine->ops.destroy_rules_set != 0) {
            engine->ops.destroy_rules_set(engine->ops.userdata, engine->rules_set);
        }
        engine->rules_set = 0;
    }
}

void msconnector_modsecurity_engine_cleanup(msconnector_modsecurity_engine *engine)
{
    if (engine == 0) {
        return;
    }
    msconnector_modsecurity_engine_destroy_rules(engine);
    if (engine->initialized && engine->ops.cleanup != 0) {
        engine->ops.cleanup(engine->ops.userdata);
    }
    engine->initialized = 0;
}

int msconnector_modsecurity_engine_create_rules(msconnector_modsecurity_engine *engine, msconnector_error *error)
{
    void *new_rules_set;
    void *old_rules_set;

    if (engine == 0 || !engine->initialized) {
        return fail_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, "engine is not initialized");
    }
    if (engine->ops.create_rules_set == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "rules set creation is unsupported");
    }

    new_rules_set = engine->ops.create_rules_set(engine->ops.userdata, error);
    if (new_rules_set == 0) {
        return 0;
    }

    old_rules_set = engine->rules_set;
    engine->rules_set = new_rules_set;
    if (old_rules_set != 0 && engine->ops.destroy_rules_set != 0) {
        engine->ops.destroy_rules_set(engine->ops.userdata, old_rules_set);
    }
    return 1;
}

int msconnector_modsecurity_transaction_init(
    msconnector_modsecurity_transaction *tx,
    msconnector_modsecurity_engine *engine,
    const char *transaction_id,
    msconnector_error *error)
{
    if (tx == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "transaction is required");
    }
    memset(tx, 0, sizeof(*tx));
    if (!msconnector_transaction_state_init(&tx->state, transaction_id)) {
        return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "invalid canonical transaction identifier");
    }
    if (engine == 0 || !engine->initialized || engine->rules_set == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE, "engine rules are not initialized");
    }
    if (engine->ops.new_transaction == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "new transaction is unsupported");
    }
    tx->engine = engine;
    tx->native_transaction = engine->ops.new_transaction(
        engine->ops.userdata,
        engine->rules_set,
        transaction_id,
        error);
    return tx->native_transaction != 0;
}

void msconnector_modsecurity_transaction_bind_contract(
    msconnector_modsecurity_transaction *tx,
    msconnector_transaction_contract *contract)
{
    if (tx != 0) {
        tx->contract = contract;
    }
}

void msconnector_modsecurity_transaction_cleanup(msconnector_modsecurity_transaction *tx)
{
    if (tx == 0) {
        return;
    }
    if (tx->contract == 0) {
        (void)msconnector_transaction_contract_cleanup(&tx->state.contract,
            engine_contract_now_ms());
    }
    if (tx->engine != 0 && tx->native_transaction != 0 && tx->engine->ops.free_transaction != 0) {
        tx->engine->ops.free_transaction(tx->engine->ops.userdata, tx->native_transaction);
    }
    tx->native_transaction = 0;
}

static int call_request(
    msconnector_modsecurity_transaction *tx,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error,
    enum msconnector_phase phase,
    int (*fn)(void *, void *, const msconnector_request *, msconnector_decision *, msconnector_error *))
{
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (fn == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "request phase is unsupported");
    }
    if (decision != 0) {
        msconnector_decision_set_allow(decision);
    }
    if (!begin_contract_phase(tx, phase, error)) {
        return 0;
    }
    if (!fn(tx->engine->ops.userdata, tx->native_transaction, request, decision, error)) {
        fail_contract_from_error(tx, error);
        return 0;
    }
    return complete_contract_phase(tx, phase, error) &&
        record_engine_decision(tx, decision, error);
}

typedef struct response_call {
    const msconnector_response *response;
    msconnector_decision *decision;
    msconnector_error *error;
    enum msconnector_phase phase;
    int companion;
    int (*fn)(void *, void *, const msconnector_response *, msconnector_decision *,
        msconnector_error *);
} response_call;

static int call_response(
    msconnector_modsecurity_transaction *tx,
    const response_call *call)
{
    if (call == 0) {
        return 0;
    }
    const msconnector_response *response = call->response;
    msconnector_decision *decision = call->decision;
    msconnector_error *error = call->error;
    const enum msconnector_phase phase = call->phase;
    const int companion = call->companion;
    int (*fn)(void *, void *, const msconnector_response *, msconnector_decision *,
        msconnector_error *) = call->fn;
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (fn == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "response phase is unsupported");
    }
    /* Buffered response-body adapters dereference the response while copying
     * its body into the native engine.  Reject a missing response at this
     * boundary so malformed callers cannot turn a phase error into a native
     * callback crash. */
    if (phase == MSCONNECTOR_PHASE_RESPONSE_BODY && response == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response is required for buffered response-body processing");
    }
    if (decision != 0) {
        msconnector_decision_set_allow(decision);
    }
    if (companion != 0) {
        if (!begin_companion_contract_phase(tx, phase, error)) {
            return 0;
        }
    } else if (!begin_contract_phase(tx, phase, error)) {
        return 0;
    }
    if (!fn(tx->engine->ops.userdata, tx->native_transaction, response, decision, error)) {
        fail_contract_from_error(tx, error);
        return 0;
    }
    return complete_contract_phase(tx, phase, error) &&
        record_engine_decision(tx, decision, error);
}

typedef struct append_call {
    const unsigned char *data;
    size_t size;
    msconnector_error *error;
    enum msconnector_phase phase;
    int companion;
    int (*fn)(void *, void *, const unsigned char *, size_t, msconnector_error *);
    const char *unsupported_message;
} append_call;

static int call_append(
    msconnector_modsecurity_transaction *tx,
    const append_call *call)
{
    if (call == 0) {
        return 0;
    }
    if (!tx_ready(tx, call->error)) {
        return 0;
    }
    if (call->size > 0U && call->data == 0) {
        return fail_error(call->error, MSCONNECTOR_ERROR_INTERNAL,
            "body data is required when size is nonzero");
    }
    if (call->fn == 0) {
        return fail_error(call->error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY,
            call->unsupported_message);
    }
    if (!(call->companion ? begin_or_resume_companion_contract_phase(tx,
                call->phase, call->error) :
            begin_or_resume_contract_phase(tx, call->phase, call->error)) ||
        !msconnector_transaction_contract_can_append_body(canonical_contract(tx),
            call->phase == MSCONNECTOR_PHASE_RESPONSE_BODY)) {
        return fail_error(call->error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "body append is outside its active transaction phase");
    }
    if (!call->fn(tx->engine->ops.userdata, tx->native_transaction,
            call->data, call->size, call->error)) {
        fail_contract_from_error(tx, call->error);
        return 0;
    }
    return 1;
}

static int call_finish(
    msconnector_modsecurity_transaction *tx,
    msconnector_decision *decision,
    msconnector_error *error,
    enum msconnector_phase phase,
    int companion,
    int (*fn)(void *, void *, msconnector_decision *, msconnector_error *),
    const char *unsupported_message)
{
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (fn == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, unsupported_message);
    }
    if (decision != 0) {
        msconnector_decision_set_allow(decision);
    }
    if (!(companion ? begin_or_resume_companion_contract_phase(tx, phase, error) :
            begin_or_resume_contract_phase(tx, phase, error))) {
        return 0;
    }
    if (!fn(tx->engine->ops.userdata, tx->native_transaction, decision, error)) {
        fail_contract_from_error(tx, error);
        return 0;
    }
    return complete_contract_phase(tx, phase, error) &&
        record_engine_decision(tx, decision, error);
}

static int (*request_op(
    const msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase))(void *, void *, const msconnector_request *, msconnector_decision *, msconnector_error *)
{
    if (tx == 0 || tx->engine == 0) {
        return 0;
    }
    if (phase == MSCONNECTOR_PHASE_CONNECTION) {
        return tx->engine->ops.process_connection;
    }
    if (phase == MSCONNECTOR_PHASE_REQUEST_HEADERS) {
        return tx->engine->ops.process_request_headers;
    }
    if (phase == MSCONNECTOR_PHASE_REQUEST_BODY) {
        return tx->engine->ops.process_request_body;
    }
    return 0;
}

static int (*response_op(
    const msconnector_modsecurity_transaction *tx,
    enum msconnector_phase phase))(void *, void *, const msconnector_response *, msconnector_decision *, msconnector_error *)
{
    if (tx == 0 || tx->engine == 0) {
        return 0;
    }
    if (phase == MSCONNECTOR_PHASE_RESPONSE_HEADERS) {
        return tx->engine->ops.process_response_headers;
    }
    if (phase == MSCONNECTOR_PHASE_RESPONSE_BODY) {
        return tx->engine->ops.process_response_body;
    }
    return 0;
}

int msconnector_modsecurity_process_connection(
    msconnector_modsecurity_transaction *tx,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_request(tx, request, decision, error, MSCONNECTOR_PHASE_CONNECTION, request_op(tx, MSCONNECTOR_PHASE_CONNECTION));
}

int msconnector_modsecurity_process_request_headers(
    msconnector_modsecurity_transaction *tx,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_request(tx, request, decision, error, MSCONNECTOR_PHASE_REQUEST_HEADERS, request_op(tx, MSCONNECTOR_PHASE_REQUEST_HEADERS));
}

int msconnector_modsecurity_process_request_body(
    msconnector_modsecurity_transaction *tx,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_request(tx, request, decision, error, MSCONNECTOR_PHASE_REQUEST_BODY, request_op(tx, MSCONNECTOR_PHASE_REQUEST_BODY));
}

int msconnector_modsecurity_append_request_body(
    msconnector_modsecurity_transaction *tx,
    const unsigned char *data,
    size_t size,
    msconnector_error *error)
{
    const append_call call = {
        data, size, error, MSCONNECTOR_PHASE_REQUEST_BODY, 0,
        tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.append_request_body,
        "incremental request body ingestion is unsupported"
    };
    return call_append(tx, &call);
}

int msconnector_modsecurity_finish_request_body(
    msconnector_modsecurity_transaction *tx,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_finish(tx, decision, error, MSCONNECTOR_PHASE_REQUEST_BODY,
        0,
        tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.finish_request_body,
        "request body finalization is unsupported");
}

int msconnector_modsecurity_process_response_headers(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    response_call call = {
        response, decision, error, MSCONNECTOR_PHASE_RESPONSE_HEADERS, 0,
        response_op(tx, MSCONNECTOR_PHASE_RESPONSE_HEADERS)
    };
    return call_response(tx, &call);
}

int msconnector_modsecurity_process_response_headers_companion(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    response_call call = {
        response, decision, error, MSCONNECTOR_PHASE_RESPONSE_HEADERS, 1,
        response_op(tx, MSCONNECTOR_PHASE_RESPONSE_HEADERS)
    };
    return call_response(tx, &call);
}

int msconnector_modsecurity_process_response_body(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    response_call call = {
        response, decision, error, MSCONNECTOR_PHASE_RESPONSE_BODY, 0,
        response_op(tx, MSCONNECTOR_PHASE_RESPONSE_BODY)
    };
    return call_response(tx, &call);
}

int msconnector_modsecurity_process_response_body_companion(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    response_call call = {
        response, decision, error, MSCONNECTOR_PHASE_RESPONSE_BODY, 1,
        response_op(tx, MSCONNECTOR_PHASE_RESPONSE_BODY)
    };
    return call_response(tx, &call);
}

int msconnector_modsecurity_append_response_body(
    msconnector_modsecurity_transaction *tx,
    const unsigned char *data,
    size_t size,
    msconnector_error *error)
{
    const append_call call = {
        data, size, error, MSCONNECTOR_PHASE_RESPONSE_BODY, 0,
        tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.append_response_body,
        "incremental response body ingestion is unsupported"
    };
    return call_append(tx, &call);
}

int msconnector_modsecurity_append_response_body_companion(
    msconnector_modsecurity_transaction *tx,
    const unsigned char *data,
    size_t size,
    msconnector_error *error)
{
    const append_call call = {
        data, size, error, MSCONNECTOR_PHASE_RESPONSE_BODY, 1,
        tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.append_response_body,
        "incremental companion response body ingestion is unsupported"
    };
    return call_append(tx, &call);
}

int msconnector_modsecurity_finish_response_body(
    msconnector_modsecurity_transaction *tx,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_finish(tx, decision, error, MSCONNECTOR_PHASE_RESPONSE_BODY,
        0,
        tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.finish_response_body,
        "response body finalization is unsupported");
}

int msconnector_modsecurity_finish_response_body_companion(
    msconnector_modsecurity_transaction *tx,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_finish(tx, decision, error, MSCONNECTOR_PHASE_RESPONSE_BODY,
        1, tx == 0 || tx->engine == 0 ? 0 : tx->engine->ops.finish_response_body,
        "companion response body finalization is unsupported");
}

int msconnector_modsecurity_process_logging(msconnector_modsecurity_transaction *tx, msconnector_error *error)
{
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (tx->engine->ops.process_logging == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "logging is unsupported");
    }
    if (!begin_contract_phase(tx, MSCONNECTOR_PHASE_LOGGING, error)) {
        return 0;
    }
    if (msconnector_transaction_contract_finish(canonical_contract(tx),
            engine_contract_now_ms()) !=
        MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return fail_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "transaction cannot log before completion or terminal decision");
    }
    if (!tx->engine->ops.process_logging(tx->engine->ops.userdata, tx->native_transaction, error)) {
        return 0;
    }
    return complete_contract_phase(tx, MSCONNECTOR_PHASE_LOGGING, error);
}
