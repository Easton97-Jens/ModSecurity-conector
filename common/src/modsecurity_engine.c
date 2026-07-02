#include "msconnector/modsecurity_engine.h"
#include <string.h>

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
    msconnector_transaction_state_init(&tx->state, transaction_id);
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

void msconnector_modsecurity_transaction_cleanup(msconnector_modsecurity_transaction *tx)
{
    if (tx == 0) {
        return;
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
    if (!fn(tx->engine->ops.userdata, tx->native_transaction, request, decision, error)) {
        return 0;
    }
    return msconnector_transaction_state_mark_phase(&tx->state, phase);
}

static int call_response(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error,
    enum msconnector_phase phase,
    int (*fn)(void *, void *, const msconnector_response *, msconnector_decision *, msconnector_error *))
{
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (fn == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "response phase is unsupported");
    }
    if (decision != 0) {
        msconnector_decision_set_allow(decision);
    }
    if (!fn(tx->engine->ops.userdata, tx->native_transaction, response, decision, error)) {
        return 0;
    }
    return msconnector_transaction_state_mark_phase(&tx->state, phase);
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

int msconnector_modsecurity_process_response_headers(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_response(tx, response, decision, error, MSCONNECTOR_PHASE_RESPONSE_HEADERS, response_op(tx, MSCONNECTOR_PHASE_RESPONSE_HEADERS));
}

int msconnector_modsecurity_process_response_body(
    msconnector_modsecurity_transaction *tx,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error)
{
    return call_response(tx, response, decision, error, MSCONNECTOR_PHASE_RESPONSE_BODY, response_op(tx, MSCONNECTOR_PHASE_RESPONSE_BODY));
}

int msconnector_modsecurity_process_logging(msconnector_modsecurity_transaction *tx, msconnector_error *error)
{
    if (!tx_ready(tx, error)) {
        return 0;
    }
    if (tx->engine->ops.process_logging == 0) {
        return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "logging is unsupported");
    }
    if (!tx->engine->ops.process_logging(tx->engine->ops.userdata, tx->native_transaction, error)) {
        return 0;
    }
    return msconnector_transaction_state_mark_phase(&tx->state, MSCONNECTOR_PHASE_LOGGING);
}
