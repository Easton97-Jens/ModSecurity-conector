#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200809L
#endif

#include "msconnector/transaction_state.h"

#include <ctype.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

static atomic_uint_fast64_t canonical_transaction_sequence = 0U;

/* A direct host adapter historically passed zero when it had no local clock
 * helper.  Do not retain that placeholder in the canonical record: receipt
 * consumers need a nonzero, nondecreasing lifecycle timeline even on those
 * paths. Explicit adapter timestamps remain authoritative when they advance
 * the record. */
static uint64_t contract_clock_now_ms(void) {
    struct timespec now;

#if defined(_WIN32)
    if (timespec_get(&now, TIME_UTC) != TIME_UTC || now.tv_sec < 0) {
#else
    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0 || now.tv_sec < 0) {
#endif
        return UINT64_C(1);
    }
    const uint64_t timestamp = (uint64_t)now.tv_sec * UINT64_C(1000) +
        (uint64_t)now.tv_nsec / UINT64_C(1000000);

    return timestamp == 0U ? UINT64_C(1) : timestamp;
}

static uint64_t contract_timestamp_floor(
    const msconnector_transaction_contract *contract) {
    uint64_t floor = 0U;

    if (contract == NULL) {
        return floor;
    }
    if (contract->created_at_ms > floor) {
        floor = contract->created_at_ms;
    }
    if (contract->phase_started_at_ms > floor) {
        floor = contract->phase_started_at_ms;
    }
    if (contract->completed_at_ms > floor) {
        floor = contract->completed_at_ms;
    }
    if (contract->cleanup_at_ms > floor) {
        floor = contract->cleanup_at_ms;
    }
    return floor;
}

static uint64_t contract_timestamp(
    const msconnector_transaction_contract *contract, uint64_t now_ms) {
    const uint64_t floor = contract_timestamp_floor(contract);

    if (now_ms == 0U) {
        now_ms = contract_clock_now_ms();
    }
    return now_ms < floor ? floor : now_ms;
}

static int text_is_empty(const char *value) {
    return value == NULL || value[0] == '\0';
}

static int copy_text(char *out, size_t out_size, const char *value, int required) {
    size_t index;

    if (out == NULL || out_size == 0U || (required && text_is_empty(value))) {
        return 0;
    }
    if (value == NULL) {
        out[0] = '\0';
        return required == 0;
    }
    for (index = 0U; index + 1U < out_size; ++index) {
        if (value[index] == '\0') {
            out[index] = '\0';
            return required == 0 || index > 0U;
        }
        out[index] = value[index];
    }
    if (value[index] != '\0') {
        out[0] = '\0';
        return 0;
    }
    out[index] = '\0';
    return required == 0 || index > 0U;
}

/*
 * The contract ID is also the lookup key for the bounded response-companion
 * registry.  Keep the host's conventional identifier byte-for-byte so that
 * existing MRC1 correlation remains valid, but never admit controls,
 * non-ASCII bytes, surrounding whitespace, or an unterminated value.  In
 * particular, do not "sanitize" an invalid value: two different host values
 * must never collapse to the same canonical lookup key.
 */
int msconnector_transaction_contract_validate_transaction_id_bytes(
    const char *value, size_t length) {
    if (value == NULL || length == 0U ||
        length >= MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH ||
        isspace((unsigned char)value[0]) ||
        isspace((unsigned char)value[length - 1U])) {
        return 0;
    }
    for (size_t index = 0U; index < length; ++index) {
        unsigned char character = (unsigned char)value[index];
        if (character < 32U || character == 127U || character > 126U) {
            return 0;
        }
    }
    return 1;
}

static int copy_canonical_transaction_id(char *out, size_t out_size,
    const char *value) {
    size_t length = 0U;

    if (out == NULL || out_size == 0U || value == NULL || value[0] == '\0') {
        return 0;
    }
    while (length + 1U < out_size && value[length] != '\0') {
        ++length;
    }
    if (value[length] != '\0' ||
        !msconnector_transaction_contract_validate_transaction_id_bytes(
            value, length)) {
        return 0;
    }
    memcpy(out, value, length);
    out[length] = '\0';
    return 1;
}

static int make_canonical_transaction_id(char *out, size_t out_size,
    uint64_t now_ms) {
    uint_fast64_t sequence;
    int written;

    if (out == NULL || out_size == 0U) {
        return 0;
    }
    sequence = atomic_load_explicit(&canonical_transaction_sequence,
        memory_order_relaxed);
    for (;;) {
        if (sequence == UINT_FAST64_MAX) {
            out[0] = '\0';
            return 0;
        }
        if (atomic_compare_exchange_weak_explicit(
                &canonical_transaction_sequence, &sequence, sequence + 1U,
                memory_order_relaxed, memory_order_relaxed)) {
            break;
        }
    }
    written = snprintf(out, out_size, "txc-%016" PRIx64 "-%016" PRIxFAST64,
        now_ms, sequence);
    if (written < 0 || (size_t)written >= out_size) {
        out[0] = '\0';
        return 0;
    }
    return 1;
}

static int same_text(const char *left, const char *right) {
    return left != NULL && right != NULL && strcmp(left, right) == 0;
}

static int phase_index(enum msconnector_phase phase) {
    switch (phase) {
    case MSCONNECTOR_TRANSACTION_PHASE_P1:
        return 0;
    case MSCONNECTOR_TRANSACTION_PHASE_P2:
        return 1;
    case MSCONNECTOR_TRANSACTION_PHASE_P3:
        return 2;
    case MSCONNECTOR_TRANSACTION_PHASE_P4:
        return 3;
    default:
        return -1;
    }
}

static unsigned int phase_mask(enum msconnector_phase phase) {
    int index = phase_index(phase);

    return index < 0 ? 0U : 1U << (unsigned int)index;
}

static msconnector_transaction_phase_route profile_phase_route(
    const msconnector_transaction_contract *contract,
    enum msconnector_phase phase) {
    const unsigned int mask = phase_mask(phase);

    if (contract == NULL || contract->profile_id == 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_DIRECT;
    }
    if ((contract->direct_phase_mask & mask) != 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_DIRECT;
    }
    if ((contract->companion_phase_mask & mask) != 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED;
    }
    return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_UNSUPPORTED;
}

static int first_missing_phase_index(unsigned int completed_mask) {
    for (int index = 0; index < 4; ++index) {
        if ((completed_mask & (1U << (unsigned int)index)) == 0U) {
            return index;
        }
    }
    return 4;
}

static int contract_is_cleaned(const msconnector_transaction_contract *contract) {
    return contract != NULL && contract->status == MSCONNECTOR_TRANSACTION_STATUS_CLEANED;
}

/* A failed contract initializer clears the record before returning INVALID.
 * Do not let that all-zero representation look mutable to metadata, decision,
 * terminal, or cleanup helpers: callers must first have a successfully
 * admitted, bounded identity and ownership record. */
static int contract_is_initialized(const msconnector_transaction_contract *contract) {
    return contract != NULL && contract->created_at_ms != 0U &&
        contract->transaction_id[0] != '\0' &&
        contract->canonical_transaction_id[0] != '\0' &&
        contract->connector_id[0] != '\0' && contract->host_id[0] != '\0' &&
        (contract->mode == MSCONNECTOR_TRANSACTION_MODE_SAFE ||
         contract->mode == MSCONNECTOR_TRANSACTION_MODE_STRICT);
}

static int contract_is_terminal_or_cleaned(const msconnector_transaction_contract *contract) {
    return contract != NULL &&
        (contract->status == MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF ||
         contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ||
         contract->status == MSCONNECTOR_TRANSACTION_STATUS_CLEANED);
}

static int contract_mutable(const msconnector_transaction_contract *contract) {
    return contract_is_initialized(contract) &&
        !contract_is_terminal_or_cleaned(contract);
}

/* A handoff is immutable for normal phase/metadata calls, but timeout,
 * cancellation, and explicit failure still have to be able to terminate the
 * retained transaction before the response observer claims it. */
static int contract_decision_mutable(const msconnector_transaction_contract *contract) {
    return contract_is_initialized(contract) && !contract_is_cleaned(contract) &&
        contract->status != MSCONNECTOR_TRANSACTION_STATUS_TERMINAL;
}

static int increment_size(size_t *value, size_t amount) {
    if (value == NULL || amount > SIZE_MAX - *value) {
        return 0;
    }
    *value += amount;
    return 1;
}

static msconnector_transaction_error_class error_for_decision(
    msconnector_transaction_decision_kind kind) {
    switch (kind) {
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT:
        return MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT;
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE:
        return MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE;
    case MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE:
        return MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE;
    case MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR:
        return MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
    case MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR:
        return MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL;
    case MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL:
        return MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL;
    case MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT:
        return MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT;
    default:
        return MSCONNECTOR_TRANSACTION_ERROR_NONE;
    }
}

const char *msconnector_transaction_phase_contract_semantics(
    enum msconnector_phase phase) {
    switch (phase) {
    case MSCONNECTOR_TRANSACTION_PHASE_P1:
        return "request headers after connection/URI prerequisites and before request commit";
    case MSCONNECTOR_TRANSACTION_PHASE_P2:
        return "request body append with one finalization at request end-of-stream";
    case MSCONNECTOR_TRANSACTION_PHASE_P3:
        return "response headers before response commitment while status remains original";
    case MSCONNECTOR_TRANSACTION_PHASE_P4:
        return "bounded response body append with one finalization at response end-of-stream";
    default:
        return "not a P1-P4 business phase";
    }
}

const char *msconnector_transaction_contract_status_name(
    msconnector_transaction_contract_status status) {
    switch (status) {
    case MSCONNECTOR_TRANSACTION_STATUS_NEW:
        return "new";
    case MSCONNECTOR_TRANSACTION_STATUS_PHASE_ACTIVE:
        return "phase_active";
    case MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE:
        return "waiting_for_next_phase";
    case MSCONNECTOR_TRANSACTION_STATUS_COMPLETED:
        return "completed";
    case MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF:
        return "handed_off";
    case MSCONNECTOR_TRANSACTION_STATUS_TERMINAL:
        return "terminal";
    case MSCONNECTOR_TRANSACTION_STATUS_CLEANED:
        return "cleaned";
    default:
        return "unknown";
    }
}

const char *msconnector_transaction_error_class_name(
    msconnector_transaction_error_class error_class) {
    switch (error_class) {
    case MSCONNECTOR_TRANSACTION_ERROR_NONE:
        return "none";
    case MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE:
        return "phase_sequence";
    case MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT:
        return "body_limit";
    case MSCONNECTOR_TRANSACTION_ERROR_EVENT_LIMIT:
        return "event_limit";
    case MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT:
        return "engine_timeout";
    case MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE:
        return "engine_unavailable";
    case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE:
        return "invalid_engine_response";
    case MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR:
        return "connector_error";
    case MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL:
        return "protocol_error";
    case MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL:
        return "client_cancel";
    case MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT:
        return "upstream_disconnect";
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISSING:
        return "correlation_missing";
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED:
        return "correlation_expired";
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISMATCH:
        return "correlation_mismatch";
    case MSCONNECTOR_TRANSACTION_ERROR_CLEANUP_INCOMPLETE:
        return "cleanup_incomplete";
    default:
        return "unknown";
    }
}

const char *msconnector_transaction_transition_name(int transition) {
    switch (transition) {
    case MSCONNECTOR_TRANSACTION_TRANSITION_OK:
        return "ok";
    case MSCONNECTOR_TRANSACTION_TRANSITION_INVALID:
        return "invalid";
    case MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE:
        return "duplicate_phase";
    case MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE:
        return "skipped_phase";
    case MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE:
        return "late_phase";
    case MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL:
        return "after_terminal";
    case MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP:
        return "after_cleanup";
    case MSCONNECTOR_TRANSACTION_TRANSITION_PHASE_ACTIVE:
        return "phase_active";
    case MSCONNECTOR_TRANSACTION_TRANSITION_PREMATURE_CLEANUP:
        return "premature_cleanup";
    case MSCONNECTOR_TRANSACTION_TRANSITION_CAPACITY:
        return "capacity";
    case MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISSING:
        return "correlation_missing";
    case MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_EXPIRED:
        return "correlation_expired";
    case MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISMATCH:
        return "correlation_mismatch";
    case MSCONNECTOR_TRANSACTION_TRANSITION_UNSUPPORTED_PHASE:
        return "unsupported_phase";
    default:
        return "unknown";
    }
}

const char *msconnector_transaction_decision_kind_name(
    msconnector_transaction_decision_kind kind) {
    switch (kind) {
    case MSCONNECTOR_TRANSACTION_DECISION_ALLOW:
        return "allow";
    case MSCONNECTOR_TRANSACTION_DECISION_BLOCK:
        return "block";
    case MSCONNECTOR_TRANSACTION_DECISION_REDIRECT:
        return "redirect";
    case MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT:
        return "rate_limit";
    case MSCONNECTOR_TRANSACTION_DECISION_LOG_ONLY:
        return "log_only";
    case MSCONNECTOR_TRANSACTION_DECISION_ENFORCE:
        return "enforce";
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT:
        return "engine_timeout";
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE:
        return "engine_unavailable";
    case MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE:
        return "invalid_engine_response";
    case MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR:
        return "connector_error";
    case MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR:
        return "protocol_error";
    case MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL:
        return "client_cancel";
    case MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT:
        return "upstream_disconnect";
    default:
        return "unknown";
    }
}

const char *msconnector_transaction_fail_policy_name(
    msconnector_transaction_fail_policy policy) {
    switch (policy) {
    case MSCONNECTOR_TRANSACTION_FAIL_NONE:
        return "none";
    case MSCONNECTOR_TRANSACTION_FAIL_OPEN:
        return "fail_open";
    case MSCONNECTOR_TRANSACTION_FAIL_CLOSED:
        return "fail_closed";
    case MSCONNECTOR_TRANSACTION_FAIL_STOP_IO:
        return "stop_io";
    default:
        return "unknown";
    }
}

msconnector_transaction_phase_route msconnector_transaction_profile_phase_route(
    const msconnector_transaction_profile *profile,
    enum msconnector_phase phase) {
    unsigned int mask = phase_mask(phase);

    if (profile == NULL || mask == 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_UNSUPPORTED;
    }
    if ((profile->direct_phase_mask & mask) != 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_DIRECT;
    }
    if ((profile->companion_phase_mask & mask) != 0U) {
        return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED;
    }
    return MSCONNECTOR_TRANSACTION_PHASE_ROUTE_UNSUPPORTED;
}

int msconnector_transaction_contract_init(msconnector_transaction_contract *contract,
    const msconnector_transaction_profile *profile,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    msconnector_transaction_mode mode,
    uint64_t now_ms) {
    const char *effective_connector;
    const char *effective_host;

    if (contract == NULL ||
        (mode != MSCONNECTOR_TRANSACTION_MODE_SAFE &&
         mode != MSCONNECTOR_TRANSACTION_MODE_STRICT)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    now_ms = contract_timestamp(NULL, now_ms);
    effective_connector = !text_is_empty(connector_id) ? connector_id : "common";
    effective_host = !text_is_empty(host_id) ? host_id : "common";
    if (profile != NULL) {
        if (text_is_empty(connector_id)) {
            effective_connector = profile->connector_id;
        }
        if (text_is_empty(host_id)) {
            effective_host = profile->host_adapter_id;
        }
    }
    memset(contract, 0, sizeof(*contract));
    if (!copy_canonical_transaction_id(contract->transaction_id,
            sizeof(contract->transaction_id), transaction_id) ||
        !make_canonical_transaction_id(contract->canonical_transaction_id,
            sizeof(contract->canonical_transaction_id), now_ms) ||
        !copy_text(contract->connector_id, sizeof(contract->connector_id),
            effective_connector, 1) ||
        !copy_text(contract->host_id, sizeof(contract->host_id), effective_host, 1)) {
        memset(contract, 0, sizeof(*contract));
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->profile_id = profile == NULL ? 0U : profile->profile_id;
    contract->direct_phase_mask = profile == NULL ?
        0U : profile->direct_phase_mask;
    contract->companion_phase_mask = profile == NULL ? 0U :
        profile->companion_phase_mask;
    contract->strict_post_commit_action = profile != NULL &&
        profile->strict_post_commit_action != 0;
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_NEW;
    contract->mode = mode;
    contract->error_class = MSCONNECTOR_TRANSACTION_ERROR_NONE;
    contract->engine_decision = MSCONNECTOR_TRANSACTION_DECISION_ALLOW;
    contract->action = MSCONNECTOR_DECISION_ACTION_ALLOW;
    contract->active_phase = -1;
    contract->last_completed_phase = -1;
    contract->created_at_ms = now_ms;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_record_request_metadata(
    msconnector_transaction_contract *contract,
    const char *method,
    const char *uri,
    const char *content_type,
    size_t header_count,
    size_t header_bytes,
    size_t body_limit) {
    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!contract_mutable(contract) || header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
        header_bytes > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES || body_limit == 0U ||
        !copy_text(contract->request_method, sizeof(contract->request_method), method, 1) ||
        !copy_text(contract->request_uri, sizeof(contract->request_uri), uri, 1) ||
        !copy_text(contract->request_content_type,
            sizeof(contract->request_content_type), content_type, 0)) {
        if (contract != NULL && contract_mutable(contract) &&
            (header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
             header_bytes > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES || body_limit == 0U)) {
            (void)msconnector_transaction_contract_fail(contract,
                MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL, contract->created_at_ms);
        }
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->request_header_count = header_count;
    contract->request_header_bytes = header_bytes;
    contract->request_body_limit = body_limit;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_record_response_metadata(
    msconnector_transaction_contract *contract,
    int status,
    const char *content_type,
    size_t header_count,
    size_t header_bytes,
    size_t body_limit) {
    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!contract_mutable(contract) || status < 100 || status > 599 ||
        header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
        header_bytes > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES || body_limit == 0U ||
        !copy_text(contract->response_content_type,
            sizeof(contract->response_content_type), content_type, 0)) {
        if (contract != NULL && contract_mutable(contract) &&
            (header_count > MSCONNECTOR_MAX_HEADER_COUNT ||
             header_bytes > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES || body_limit == 0U)) {
            (void)msconnector_transaction_contract_fail(contract,
                MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL, contract->created_at_ms);
        }
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->response_status = status;
    contract->response_header_count = header_count;
    contract->response_header_bytes = header_bytes;
    contract->response_body_limit = body_limit;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_record_body(msconnector_transaction_contract *contract,
    int response_direction,
    size_t bytes) {
    const enum msconnector_phase expected_phase = response_direction ?
        MSCONNECTOR_TRANSACTION_PHASE_P4 : MSCONNECTOR_TRANSACTION_PHASE_P2;

    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!contract_mutable(contract)) {
        if (contract_is_cleaned(contract)) {
            return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
        }
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    if (contract->active_phase != (int)expected_phase) {
        return contract->active_phase < 0 ? MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE :
            MSCONNECTOR_TRANSACTION_TRANSITION_PHASE_ACTIVE;
    }
    if (!increment_size(response_direction ? &contract->response_body_bytes :
            &contract->request_body_bytes, bytes) ||
        (response_direction && contract->response_body_limit > 0U &&
            contract->response_body_bytes > contract->response_body_limit) ||
        (!response_direction && contract->request_body_limit > 0U &&
            contract->request_body_bytes > contract->request_body_limit)) {
        (void)msconnector_transaction_contract_fail(contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, contract->phase_started_at_ms);
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_set_response_committed(
    msconnector_transaction_contract *contract,
    int committed) {
    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!contract_mutable(contract)) {
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    if (committed != 0 && (contract->completed_phase_mask &
            MSCONNECTOR_TRANSACTION_PHASE_MASK_P3) == 0U) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE;
    }
    if (contract->response_committed && committed == 0) {
        /* A host may advance its commitment evidence, but it can never undo
         * it.  Direct users of the Common contract get the same protection as
         * the runtime wrapper, so later Strict/Safe policy cannot be made to
         * believe a response is mutable again. */
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->response_committed = committed != 0;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

static int begin_phase_for_route(msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    int companion,
    uint64_t now_ms) {
    int index = phase_index(phase);
    int expected;
    msconnector_transaction_phase_route route;

    if (!contract_is_initialized(contract) || index < 0) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (contract_is_cleaned(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
    }
    if (contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ||
        contract->status == MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF ||
        contract->status == MSCONNECTOR_TRANSACTION_STATUS_COMPLETED) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    route = profile_phase_route(contract, phase);
    if ((companion && route != MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED) ||
        (!companion && route != MSCONNECTOR_TRANSACTION_PHASE_ROUTE_DIRECT)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_UNSUPPORTED_PHASE;
    }
    if (contract->active_phase >= 0) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_PHASE_ACTIVE;
    }
    if ((contract->completed_phase_mask & phase_mask(phase)) != 0U) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE;
    }
    expected = first_missing_phase_index(contract->completed_phase_mask);
    if (index > expected) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE;
    }
    if (index < expected) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE;
    }
    if (phase == MSCONNECTOR_TRANSACTION_PHASE_P3 && contract->response_committed) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE;
    }
    contract->active_phase = (int)phase;
    contract->phase_started_at_ms = now_ms;
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_PHASE_ACTIVE;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_begin_phase(msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms) {
    return begin_phase_for_route(contract, phase, 0, now_ms);
}

int msconnector_transaction_contract_begin_companion_phase(
    msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms) {
    return begin_phase_for_route(contract, phase, 1, now_ms);
}

int msconnector_transaction_contract_complete_phase(msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms) {
    if (!contract_is_initialized(contract) || phase_index(phase) < 0) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (contract_is_cleaned(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
    }
    if (contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ||
        contract->status == MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF ||
        contract->status == MSCONNECTOR_TRANSACTION_STATUS_COMPLETED) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    if ((contract->completed_phase_mask & phase_mask(phase)) != 0U) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE;
    }
    if (contract->active_phase != (int)phase) {
        return contract->active_phase < 0 ? MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE :
            MSCONNECTOR_TRANSACTION_TRANSITION_PHASE_ACTIVE;
    }
    contract->active_phase = -1;
    contract->last_completed_phase = (int)phase;
    contract->completed_phase_mask |= phase_mask(phase);
    contract->completed_at_ms = now_ms;
    contract->status = contract->completed_phase_mask == MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL ?
        MSCONNECTOR_TRANSACTION_STATUS_COMPLETED :
        MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_can_append_body(
    const msconnector_transaction_contract *contract,
    int response_direction) {
    enum msconnector_phase phase = response_direction ?
        MSCONNECTOR_TRANSACTION_PHASE_P4 : MSCONNECTOR_TRANSACTION_PHASE_P2;
    int expected;

    if (!contract_mutable(contract)) {
        return 0;
    }
    expected = first_missing_phase_index(contract->completed_phase_mask);
    return contract->active_phase == (int)phase ||
        (contract->active_phase < 0 && expected == phase_index(phase));
}

int msconnector_transaction_contract_decision_policy(
    const msconnector_transaction_contract *contract,
    msconnector_transaction_decision_kind kind,
    msconnector_transaction_decision_policy *out) {
    int strict;
    int committed;

    if (out == NULL || kind < MSCONNECTOR_TRANSACTION_DECISION_ALLOW ||
        kind > MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT) {
        return 0;
    }
    memset(out, 0, sizeof(*out));
    strict = contract != NULL && contract->mode == MSCONNECTOR_TRANSACTION_MODE_STRICT;
    committed = contract != NULL && contract->response_committed;
    out->kind = kind;
    out->host_action = MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
    out->event_type = msconnector_transaction_decision_kind_name(kind);
    out->cleanup_required = 1;

    switch (kind) {
    case MSCONNECTOR_TRANSACTION_DECISION_ALLOW:
        out->host_action = MSCONNECTOR_DECISION_ACTION_ALLOW;
        out->event_type = "allow";
        out->cleanup_required = 0;
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_BLOCK:
        out->host_action = MSCONNECTOR_DECISION_ACTION_DENY;
        out->event_type = "rule_block";
        out->rule_correlation_required = 1;
        out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_CLOSED;
        out->terminal = 1;
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_REDIRECT:
        out->host_action = MSCONNECTOR_DECISION_ACTION_REDIRECT;
        out->event_type = "rule_redirect";
        out->rule_correlation_required = 1;
        out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_CLOSED;
        out->terminal = 1;
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT:
        out->host_action = MSCONNECTOR_DECISION_ACTION_RATE_LIMIT;
        out->event_type = "rule_rate_limit";
        out->rule_correlation_required = 1;
        out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_CLOSED;
        out->terminal = 1;
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_LOG_ONLY:
        out->host_action = MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
        out->event_type = "log_only";
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_ENFORCE:
        out->rule_correlation_required = 1;
        if (!strict || (committed &&
                (contract == NULL || !contract->strict_post_commit_action))) {
            out->host_action = MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
            out->event_type = "enforce_downgraded_log_only";
            out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_OPEN;
            out->terminal = committed != 0;
        } else {
            out->host_action = MSCONNECTOR_DECISION_ACTION_DENY;
            out->event_type = "enforce";
            out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_CLOSED;
            out->terminal = 1;
        }
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT:
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE:
    case MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE:
    case MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR:
    case MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR:
        if (strict && !committed) {
            out->host_action = MSCONNECTOR_DECISION_ACTION_DENY;
            out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_CLOSED;
        } else {
            out->host_action = MSCONNECTOR_DECISION_ACTION_LOG_ONLY;
            out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_OPEN;
        }
        out->terminal = 1;
        return 1;
    case MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL:
    case MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT:
        out->host_action = MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION;
        out->fail_policy = MSCONNECTOR_TRANSACTION_FAIL_STOP_IO;
        out->terminal = 1;
        return 1;
    default:
        return 0;
    }
}

int msconnector_transaction_contract_record_decision(
    msconnector_transaction_contract *contract,
    msconnector_transaction_decision_kind kind,
    const char *rule_id,
    uint64_t now_ms) {
    msconnector_transaction_decision_policy policy;

    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!contract_decision_mutable(contract)) {
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (!msconnector_transaction_contract_decision_policy(contract, kind, &policy)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (policy.rule_correlation_required && text_is_empty(rule_id)) {
        contract->error_class = MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE;
        contract->engine_decision = MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE;
        (void)msconnector_transaction_contract_decision_policy(contract,
            MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE, &policy);
        contract->action = policy.host_action;
        contract->status = MSCONNECTOR_TRANSACTION_STATUS_TERMINAL;
        contract->completed_at_ms = now_ms;
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (!copy_text(contract->rule_id, sizeof(contract->rule_id), rule_id, 0)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->engine_decision = kind;
    contract->action = policy.host_action;
    contract->error_class = error_for_decision(kind);
    if (policy.terminal) {
        contract->active_phase = -1;
        contract->status = MSCONNECTOR_TRANSACTION_STATUS_TERMINAL;
        contract->completed_at_ms = now_ms;
    }
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_cancel(msconnector_transaction_contract *contract,
    int upstream_disconnect,
    uint64_t now_ms) {
    if (contract != NULL && contract->status ==
        MSCONNECTOR_TRANSACTION_STATUS_COMPLETED) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    return msconnector_transaction_contract_record_decision(contract,
        upstream_disconnect ? MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT :
            MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL,
        NULL, now_ms);
}

int msconnector_transaction_contract_timeout(msconnector_transaction_contract *contract,
    uint64_t now_ms) {
    if (contract != NULL && contract->status ==
        MSCONNECTOR_TRANSACTION_STATUS_COMPLETED) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    return msconnector_transaction_contract_record_decision(contract,
        MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT, NULL, now_ms);
}

int msconnector_transaction_contract_handoff_response_companion(
    msconnector_transaction_contract *contract,
    uint64_t now_ms) {
    if (!contract_mutable(contract)) {
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (contract->companion_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P4) ||
        contract->active_phase >= 0 ||
        contract->completed_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P2)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF;
    contract->completed_at_ms = now_ms;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_claim_response_companion(
    msconnector_transaction_contract *contract,
    uint64_t now_ms) {
    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (contract_is_cleaned(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
    }
    if (contract->status != MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF) {
        return contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL :
            MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (contract->companion_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 |
             MSCONNECTOR_TRANSACTION_PHASE_MASK_P4) ||
        contract->active_phase >= 0 ||
        contract->completed_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 |
             MSCONNECTOR_TRANSACTION_PHASE_MASK_P2)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE;
    contract->completed_at_ms = now_ms;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_fail(msconnector_transaction_contract *contract,
    msconnector_transaction_error_class error_class,
    uint64_t now_ms) {
    msconnector_transaction_decision_kind kind;

    if (!contract_decision_mutable(contract) ||
        error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        return contract_is_cleaned(contract) ?
            MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP :
            MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    now_ms = contract_timestamp(contract, now_ms);
    switch (error_class) {
    case MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT:
        kind = MSCONNECTOR_TRANSACTION_DECISION_BLOCK;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT:
        kind = MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE:
        kind = MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE:
        kind = MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE:
    case MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL:
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISSING:
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED:
    case MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISMATCH:
        kind = MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL:
        kind = MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL;
        break;
    case MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT:
        kind = MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT;
        break;
    default:
        kind = MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR;
        break;
    }
    if (kind == MSCONNECTOR_TRANSACTION_DECISION_BLOCK) {
        /* Limits are host policy errors, not a forged rule decision. */
        contract->error_class = error_class;
        contract->engine_decision = kind;
        contract->action = MSCONNECTOR_DECISION_ACTION_DENY;
        contract->rule_id[0] = '\0';
        contract->active_phase = -1;
        contract->status = MSCONNECTOR_TRANSACTION_STATUS_TERMINAL;
        contract->completed_at_ms = now_ms;
        return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
    }
    if (msconnector_transaction_contract_record_decision(contract, kind, NULL, now_ms) !=
        MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    /* Preserve the more specific local failure taxonomy after the common
     * decision mapping has selected its host action. */
    contract->error_class = error_class;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_finish(msconnector_transaction_contract *contract,
    uint64_t now_ms) {
    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (contract_is_cleaned(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
    }
    now_ms = contract_timestamp(contract, now_ms);
    if (contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
    }
    if (contract->status == MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF) {
        (void)msconnector_transaction_contract_fail(contract,
            MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL, now_ms);
        return MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE;
    }
    if (contract->active_phase >= 0 ||
        contract->completed_phase_mask != MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL) {
        (void)msconnector_transaction_contract_fail(contract,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE, now_ms);
        return MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE;
    }
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_COMPLETED;
    contract->completed_at_ms = now_ms;
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_cleanup(msconnector_transaction_contract *contract,
    uint64_t now_ms) {
    int incomplete;

    if (!contract_is_initialized(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (contract_is_cleaned(contract)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP;
    }
    now_ms = contract_timestamp(contract, now_ms);
    incomplete = contract->status != MSCONNECTOR_TRANSACTION_STATUS_TERMINAL &&
        contract->completed_phase_mask != MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL;
    if (incomplete) {
        /* Cleanup is a lifecycle boundary, not permission to discard an
         * incomplete transaction silently. Record the canonical terminal
         * connector-error decision while the contract is still mutable; keep
         * the more precise cleanup error class after cleanup for diagnostics.
         */
        (void)msconnector_transaction_contract_fail(contract,
            MSCONNECTOR_TRANSACTION_ERROR_CLEANUP_INCOMPLETE, now_ms);
    }
    contract->cleanup_started = 1;
    contract->cleanup_complete = 1;
    contract->active_phase = -1;
    contract->cleanup_at_ms = now_ms;
    contract->status = MSCONNECTOR_TRANSACTION_STATUS_CLEANED;
    return incomplete ? MSCONNECTOR_TRANSACTION_TRANSITION_PREMATURE_CLEANUP :
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_contract_is_terminal(
    const msconnector_transaction_contract *contract) {
    return contract_is_initialized(contract) &&
        (contract->status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL ||
         contract->status == MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF ||
         contract->status == MSCONNECTOR_TRANSACTION_STATUS_CLEANED ||
         contract->status == MSCONNECTOR_TRANSACTION_STATUS_COMPLETED);
}

msconnector_transaction_decision_kind
msconnector_transaction_decision_kind_from_engine(const msconnector_decision *decision) {
    if (decision == NULL) {
        return MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE;
    }
    switch (decision->kind) {
    case MSCONNECTOR_DECISION_KIND_ALLOW:
        return MSCONNECTOR_TRANSACTION_DECISION_ALLOW;
    case MSCONNECTOR_DECISION_KIND_LOG_ONLY:
        return MSCONNECTOR_TRANSACTION_DECISION_LOG_ONLY;
    case MSCONNECTOR_DECISION_KIND_DENY:
        return decision->http_status == 429 ? MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT :
            MSCONNECTOR_TRANSACTION_DECISION_BLOCK;
    case MSCONNECTOR_DECISION_KIND_REDIRECT:
        return MSCONNECTOR_TRANSACTION_DECISION_REDIRECT;
    case MSCONNECTOR_DECISION_KIND_DROP:
    case MSCONNECTOR_DECISION_KIND_CONNECTION_ABORT:
        return MSCONNECTOR_TRANSACTION_DECISION_ENFORCE;
    case MSCONNECTOR_DECISION_KIND_ERROR:
        return MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR;
    case MSCONNECTOR_DECISION_KIND_UNSUPPORTED:
    default:
        return MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE;
    }
}

static void correlation_registry_lock(
    msconnector_transaction_correlation_registry *registry) {
    while (atomic_flag_test_and_set_explicit(&registry->lock,
            memory_order_acquire)) {
        /* Fixed-capacity registry operations are short and never invoke host
         * callbacks, so a small local spin is sufficient here. */
    }
}

static void correlation_registry_unlock(
    msconnector_transaction_correlation_registry *registry) {
    atomic_flag_clear_explicit(&registry->lock, memory_order_release);
}

static size_t correlation_registry_expire_locked(
    msconnector_transaction_correlation_registry *registry,
    uint64_t now_ms) {
    size_t expired = 0U;

    for (size_t index = 0U; index < MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY;
         ++index) {
        msconnector_transaction_correlation_entry *entry = &registry->entries[index];
        if (entry->occupied && entry->expires_at_ms <= now_ms) {
            (void)msconnector_transaction_contract_fail(&entry->transaction,
                MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED, now_ms);
            (void)msconnector_transaction_contract_cleanup(&entry->transaction, now_ms);
            memset(entry, 0, sizeof(*entry));
            ++expired;
        }
    }
    return expired;
}

void msconnector_transaction_correlation_registry_init(
    msconnector_transaction_correlation_registry *registry) {
    if (registry != NULL) {
        memset(registry, 0, sizeof(*registry));
        atomic_flag_clear_explicit(&registry->lock, memory_order_release);
    }
}

size_t msconnector_transaction_correlation_expire(
    msconnector_transaction_correlation_registry *registry,
    uint64_t now_ms) {
    size_t expired;

    if (registry == NULL) {
        return 0U;
    }
    correlation_registry_lock(registry);
    expired = correlation_registry_expire_locked(registry, now_ms);
    correlation_registry_unlock(registry);
    return expired;
}

int msconnector_transaction_correlation_register_request(
    msconnector_transaction_correlation_registry *registry,
    const msconnector_transaction_contract *transaction,
    uint64_t now_ms,
    uint64_t ttl_ms) {
    size_t free_index = MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY;

    if (registry == NULL || transaction == NULL || ttl_ms == 0U ||
        transaction->completed_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P2) ||
        transaction->status != MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    if (transaction->companion_phase_mask == 0U ||
        UINT64_MAX - now_ms < ttl_ms) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    correlation_registry_lock(registry);
    (void)correlation_registry_expire_locked(registry, now_ms);
    for (size_t index = 0U;
         index < MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY; ++index) {
        const msconnector_transaction_correlation_entry *entry =
            &registry->entries[index];
        if (!entry->occupied && free_index == MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY) {
            free_index = index;
            continue;
        }
        if (entry->occupied && same_text(entry->transaction.transaction_id,
                transaction->transaction_id)) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE;
        }
    }
    if (free_index == MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY) {
        correlation_registry_unlock(registry);
        return MSCONNECTOR_TRANSACTION_TRANSITION_CAPACITY;
    }
    registry->entries[free_index].occupied = 1;
    registry->entries[free_index].expires_at_ms = now_ms + ttl_ms;
    registry->entries[free_index].transaction = *transaction;
    correlation_registry_unlock(registry);
    return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_correlation_claim_response(
    msconnector_transaction_correlation_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    uint64_t now_ms,
    msconnector_transaction_contract *out) {
    if (out != NULL) {
        memset(out, 0, sizeof(*out));
    }
    if (registry == NULL || out == NULL || text_is_empty(transaction_id) ||
        text_is_empty(connector_id) || text_is_empty(host_id)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    correlation_registry_lock(registry);
    for (size_t index = 0U; index < MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY;
         ++index) {
        msconnector_transaction_correlation_entry *entry = &registry->entries[index];
        if (!entry->occupied || !same_text(entry->transaction.transaction_id, transaction_id)) {
            continue;
        }
        if (entry->expires_at_ms <= now_ms) {
            const int failure_result = msconnector_transaction_contract_fail(&entry->transaction,
                MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED, now_ms);
            const int cleanup_result = msconnector_transaction_contract_cleanup(&entry->transaction, now_ms);
            if (failure_result == MSCONNECTOR_TRANSACTION_TRANSITION_INVALID ||
                cleanup_result == MSCONNECTOR_TRANSACTION_TRANSITION_INVALID) {
                correlation_registry_unlock(registry);
                return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
            }
            memset(entry, 0, sizeof(*entry));
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_EXPIRED;
        }
        {
            if (entry->transaction.companion_phase_mask == 0U ||
            !same_text(entry->transaction.connector_id, connector_id) ||
                !same_text(entry->transaction.host_id, host_id)) {
                correlation_registry_unlock(registry);
                return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISMATCH;
            }
        }
        if (entry->claimed) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE;
        }
        entry->claimed = 1;
        *out = entry->transaction;
        correlation_registry_unlock(registry);
        return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
    }
    (void)correlation_registry_expire_locked(registry, now_ms);
    correlation_registry_unlock(registry);
    return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISSING;
}

int msconnector_transaction_correlation_release(
    msconnector_transaction_correlation_registry *registry,
    msconnector_transaction_contract *transaction,
    uint64_t now_ms) {
    if (registry == NULL || transaction == NULL ||
        text_is_empty(transaction->transaction_id) ||
        text_is_empty(transaction->connector_id) ||
        text_is_empty(transaction->host_id)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    correlation_registry_lock(registry);
    for (size_t index = 0U; index < MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY;
         ++index) {
        msconnector_transaction_correlation_entry *entry = &registry->entries[index];
        int cleanup_result;
        if (!entry->occupied || !same_text(entry->transaction.transaction_id,
                transaction->transaction_id)) {
            continue;
        }
        if (!same_text(entry->transaction.connector_id, transaction->connector_id) ||
            !same_text(entry->transaction.host_id, transaction->host_id)) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISMATCH;
        }
        if (entry->expires_at_ms <= now_ms) {
            (void)msconnector_transaction_contract_fail(&entry->transaction,
                MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED, now_ms);
            (void)msconnector_transaction_contract_cleanup(&entry->transaction, now_ms);
            memset(entry, 0, sizeof(*entry));
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_EXPIRED;
        }
        if (!entry->claimed || !msconnector_transaction_contract_is_terminal(transaction)) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_PREMATURE_CLEANUP;
        }
        cleanup_result = msconnector_transaction_contract_cleanup(transaction, now_ms);
        memset(entry, 0, sizeof(*entry));
        correlation_registry_unlock(registry);
        return cleanup_result;
    }
    correlation_registry_unlock(registry);
    return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISSING;
}

int msconnector_transaction_correlation_revoke_request(
    msconnector_transaction_correlation_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    uint64_t now_ms) {
    if (registry == NULL || text_is_empty(transaction_id) ||
        text_is_empty(connector_id) || text_is_empty(host_id)) {
        return MSCONNECTOR_TRANSACTION_TRANSITION_INVALID;
    }
    correlation_registry_lock(registry);
    for (size_t index = 0U; index < MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY;
         ++index) {
        msconnector_transaction_correlation_entry *entry = &registry->entries[index];
        if (!entry->occupied || !same_text(entry->transaction.transaction_id,
                transaction_id)) {
            continue;
        }
        if (!same_text(entry->transaction.connector_id, connector_id) ||
            !same_text(entry->transaction.host_id, host_id)) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISMATCH;
        }
        if (entry->claimed) {
            correlation_registry_unlock(registry);
            return MSCONNECTOR_TRANSACTION_TRANSITION_PREMATURE_CLEANUP;
        }
        (void)msconnector_transaction_contract_fail(&entry->transaction,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, now_ms);
        (void)msconnector_transaction_contract_cleanup(&entry->transaction, now_ms);
        memset(entry, 0, sizeof(*entry));
        correlation_registry_unlock(registry);
        return MSCONNECTOR_TRANSACTION_TRANSITION_OK;
    }
    correlation_registry_unlock(registry);
    return MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISSING;
}

static int set_phase_flag(msconnector_transaction_state *state,
    enum msconnector_phase phase) {
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

static int transaction_state_is_initialized(
    const msconnector_transaction_state *state) {
    return state != NULL && state->initialized != 0 &&
        contract_is_initialized(&state->contract);
}

int msconnector_transaction_state_init(
    msconnector_transaction_state *state,
    const char *transaction_id) {
    if (state == NULL) {
        return 0;
    }
    memset(state, 0, sizeof(*state));
    if (msconnector_transaction_contract_init(&state->contract, NULL,
        transaction_id == NULL ? "common-transaction" : transaction_id,
        "common", "engine", MSCONNECTOR_TRANSACTION_MODE_SAFE, 0U) !=
        MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        memset(state, 0, sizeof(*state));
        return 0;
    }
    state->transaction_id = transaction_id;
    state->initialized = 1;
    return 1;
}

int msconnector_transaction_state_begin_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (!transaction_state_is_initialized(state)) {
        return 0;
    }
    if (phase_index(phase) < 0) {
        return !msconnector_transaction_state_phase_processed(state, phase);
    }
    return msconnector_transaction_contract_begin_phase(&state->contract, phase, 0U) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msconnector_transaction_state_complete_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (!transaction_state_is_initialized(state)) {
        return 0;
    }
    if (phase_index(phase) < 0) {
        return set_phase_flag(state, phase);
    }
    if (msconnector_transaction_contract_complete_phase(&state->contract, phase, 0U) !=
        MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return 0;
    }
    return set_phase_flag(state, phase);
}

int msconnector_transaction_state_note_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    return transaction_state_is_initialized(state) && set_phase_flag(state, phase);
}

int msconnector_transaction_state_mark_phase(
    msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (!transaction_state_is_initialized(state)) {
        return 0;
    }
    if (phase == MSCONNECTOR_PHASE_LOGGING) {
        if (msconnector_transaction_contract_finish(&state->contract, 0U) !=
            MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
            return 0;
        }
        return set_phase_flag(state, phase);
    }
    if (phase_index(phase) < 0) {
        return set_phase_flag(state, phase);
    }
    if (state->contract.active_phase != (int)phase &&
        !msconnector_transaction_state_begin_phase(state, phase)) {
        return 0;
    }
    return msconnector_transaction_state_complete_phase(state, phase);
}

int msconnector_transaction_state_phase_processed(
    const msconnector_transaction_state *state,
    enum msconnector_phase phase) {
    if (!transaction_state_is_initialized(state)) {
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
