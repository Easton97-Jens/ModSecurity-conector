#ifndef MSCONNECTOR_TRANSACTION_CONTRACT_H
#define MSCONNECTOR_TRANSACTION_CONTRACT_H

#include <stddef.h>
#include <stdint.h>

#include "msconnector/decision.h"
#include "msconnector/decision_action.h"
#include "msconnector/limits.h"

#ifdef __cplusplus
#include <atomic>
typedef std::atomic_flag msconnector_atomic_flag;
extern "C" {
#else
#include <stdatomic.h>
typedef atomic_flag msconnector_atomic_flag;
#endif

/*
 * The contract stores metadata only.  Request and response bodies are
 * deliberately represented by counters and limits; no body pointer or
 * payload may cross this transaction boundary.
 */
#define MSCONNECTOR_TRANSACTION_CONTRACT_CONNECTOR_ID_SIZE 48U
#define MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE 96U
#define MSCONNECTOR_TRANSACTION_CONTRACT_METHOD_SIZE 32U
#define MSCONNECTOR_TRANSACTION_CONTRACT_URI_SIZE 16384U
/* Content-Type is retained as bounded metadata and follows the same accepted
 * value limit as every other header field. The extra byte is the NUL
 * terminator required by the C-only adapter boundary. */
#define MSCONNECTOR_TRANSACTION_CONTRACT_CONTENT_TYPE_SIZE \
    (MSCONNECTOR_MAX_HEADER_VALUE_LENGTH + 1U)
#define MSCONNECTOR_TRANSACTION_CANONICAL_ID_SIZE 64U
#define MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY 64U

#define MSCONNECTOR_TRANSACTION_PHASE_P1 MSCONNECTOR_PHASE_REQUEST_HEADERS
#define MSCONNECTOR_TRANSACTION_PHASE_P2 MSCONNECTOR_PHASE_REQUEST_BODY
#define MSCONNECTOR_TRANSACTION_PHASE_P3 MSCONNECTOR_PHASE_RESPONSE_HEADERS
#define MSCONNECTOR_TRANSACTION_PHASE_P4 MSCONNECTOR_PHASE_RESPONSE_BODY

#define MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 (1U << 0)
#define MSCONNECTOR_TRANSACTION_PHASE_MASK_P2 (1U << 1)
#define MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 (1U << 2)
#define MSCONNECTOR_TRANSACTION_PHASE_MASK_P4 (1U << 3)
#define MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL \
    (MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | \
     MSCONNECTOR_TRANSACTION_PHASE_MASK_P2 | \
     MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 | \
     MSCONNECTOR_TRANSACTION_PHASE_MASK_P4)

typedef enum msconnector_transaction_contract_status {
    MSCONNECTOR_TRANSACTION_STATUS_NEW = 0,
    MSCONNECTOR_TRANSACTION_STATUS_PHASE_ACTIVE,
    MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE,
    MSCONNECTOR_TRANSACTION_STATUS_COMPLETED,
    /* Request-only protocol component transferred its P1/P2 snapshot to the
     * bounded response companion, which now owns P3/P4. */
    MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF,
    MSCONNECTOR_TRANSACTION_STATUS_TERMINAL,
    MSCONNECTOR_TRANSACTION_STATUS_CLEANED
} msconnector_transaction_contract_status;

typedef enum msconnector_transaction_mode {
    MSCONNECTOR_TRANSACTION_MODE_SAFE = 0,
    MSCONNECTOR_TRANSACTION_MODE_STRICT = 1
} msconnector_transaction_mode;

typedef enum msconnector_transaction_error_class {
    MSCONNECTOR_TRANSACTION_ERROR_NONE = 0,
    MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
    MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT,
    MSCONNECTOR_TRANSACTION_ERROR_EVENT_LIMIT,
    MSCONNECTOR_TRANSACTION_ERROR_ENGINE_TIMEOUT,
    MSCONNECTOR_TRANSACTION_ERROR_ENGINE_UNAVAILABLE,
    MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
    MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
    MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL,
    MSCONNECTOR_TRANSACTION_ERROR_CLIENT_CANCEL,
    MSCONNECTOR_TRANSACTION_ERROR_UPSTREAM_DISCONNECT,
    MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISSING,
    MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_EXPIRED,
    MSCONNECTOR_TRANSACTION_ERROR_CORRELATION_MISMATCH,
    MSCONNECTOR_TRANSACTION_ERROR_CLEANUP_INCOMPLETE
} msconnector_transaction_error_class;

typedef enum msconnector_transaction_transition {
    MSCONNECTOR_TRANSACTION_TRANSITION_OK = 0,
    MSCONNECTOR_TRANSACTION_TRANSITION_INVALID = -1,
    MSCONNECTOR_TRANSACTION_TRANSITION_DUPLICATE_PHASE = -2,
    MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE = -3,
    MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE = -4,
    MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL = -5,
    MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_CLEANUP = -6,
    MSCONNECTOR_TRANSACTION_TRANSITION_PHASE_ACTIVE = -7,
    MSCONNECTOR_TRANSACTION_TRANSITION_PREMATURE_CLEANUP = -8,
    MSCONNECTOR_TRANSACTION_TRANSITION_CAPACITY = -9,
    MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISSING = -10,
    MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_EXPIRED = -11,
    MSCONNECTOR_TRANSACTION_TRANSITION_CORRELATION_MISMATCH = -12,
    MSCONNECTOR_TRANSACTION_TRANSITION_UNSUPPORTED_PHASE = -13
} msconnector_transaction_transition;

typedef enum msconnector_transaction_decision_kind {
    MSCONNECTOR_TRANSACTION_DECISION_ALLOW = 0,
    MSCONNECTOR_TRANSACTION_DECISION_BLOCK,
    MSCONNECTOR_TRANSACTION_DECISION_REDIRECT,
    MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT,
    MSCONNECTOR_TRANSACTION_DECISION_LOG_ONLY,
    MSCONNECTOR_TRANSACTION_DECISION_ENFORCE,
    MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT,
    MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE,
    MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE,
    MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR,
    MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR,
    MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL,
    MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT
} msconnector_transaction_decision_kind;

typedef enum msconnector_transaction_fail_policy {
    MSCONNECTOR_TRANSACTION_FAIL_NONE = 0,
    MSCONNECTOR_TRANSACTION_FAIL_OPEN,
    MSCONNECTOR_TRANSACTION_FAIL_CLOSED,
    MSCONNECTOR_TRANSACTION_FAIL_STOP_IO
} msconnector_transaction_fail_policy;

typedef enum msconnector_transaction_phase_route {
    MSCONNECTOR_TRANSACTION_PHASE_ROUTE_DIRECT = 0,
    MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED,
    MSCONNECTOR_TRANSACTION_PHASE_ROUTE_UNSUPPORTED
} msconnector_transaction_phase_route;

typedef struct msconnector_transaction_profile {
    unsigned int profile_id;
    const char *profile_name;
    const char *connector_id;
    /* Stable adapter-route identity used only during adapter setup. It is
     * deliberately distinct from transaction_contract.host_id, which
     * identifies the actual host instance participating in one transaction. */
    const char *host_adapter_id;
    unsigned int direct_phase_mask;
    unsigned int companion_phase_mask;
    int strict_post_commit_action;
    int private_default_binding;
} msconnector_transaction_profile;

typedef struct msconnector_transaction_decision_policy {
    msconnector_transaction_decision_kind kind;
    msconnector_decision_action host_action;
    const char *event_type;
    int rule_correlation_required;
    msconnector_transaction_fail_policy fail_policy;
    int terminal;
    int cleanup_required;
} msconnector_transaction_decision_policy;

typedef struct msconnector_transaction_contract {
    /* Anonymous value groups preserve the established field spelling for C
     * and C++ adapters while giving analyzers a small coherent top-level
     * contract shape. Every bound remains attached to its value group. */
    struct {
        char transaction_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
        char canonical_transaction_id[MSCONNECTOR_TRANSACTION_CANONICAL_ID_SIZE];
        char connector_id[MSCONNECTOR_TRANSACTION_CONTRACT_CONNECTOR_ID_SIZE];
        char host_id[MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE];
    };
    struct {
        char request_method[MSCONNECTOR_TRANSACTION_CONTRACT_METHOD_SIZE];
        char request_uri[MSCONNECTOR_TRANSACTION_CONTRACT_URI_SIZE];
        char request_content_type[MSCONNECTOR_TRANSACTION_CONTRACT_CONTENT_TYPE_SIZE];
        size_t request_header_count;
        size_t request_header_bytes;
        size_t request_body_bytes;
        size_t request_body_limit;
    };
    struct {
        char response_content_type[MSCONNECTOR_TRANSACTION_CONTRACT_CONTENT_TYPE_SIZE];
        size_t response_header_count;
        size_t response_header_bytes;
        size_t response_body_bytes;
        size_t response_body_limit;
        int response_status;
        int response_committed;
    };
    struct {
        char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH];
        unsigned int profile_id;
        unsigned int direct_phase_mask;
        unsigned int companion_phase_mask;
        int strict_post_commit_action;
    };
    struct {
        msconnector_transaction_contract_status status;
        msconnector_transaction_mode mode;
        msconnector_transaction_error_class error_class;
        msconnector_transaction_decision_kind engine_decision;
        msconnector_decision_action action;
    };
    struct {
        int active_phase;
        int last_completed_phase;
        unsigned int completed_phase_mask;
    };
    struct {
        int cleanup_started;
        int cleanup_complete;
    };
    struct {
        uint64_t created_at_ms;
        uint64_t phase_started_at_ms;
        uint64_t completed_at_ms;
        uint64_t cleanup_at_ms;
    };
} msconnector_transaction_contract;

typedef struct msconnector_transaction_correlation_entry {
    int occupied;
    int claimed;
    uint64_t expires_at_ms;
    msconnector_transaction_contract transaction;
} msconnector_transaction_correlation_entry;

typedef struct msconnector_transaction_correlation_registry {
    /* Registry operations are serialized. A claimed response is copied out,
     * so expiry/release can never invalidate a caller-owned phase record. */
    msconnector_atomic_flag lock;
    msconnector_transaction_correlation_entry entries[
        MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY];
} msconnector_transaction_correlation_registry;

/* P1 is request headers; P2/P4 complete only at their respective EOS; P3
 * precedes response commitment. Connection, URI, and logging remain native
 * lifecycle prerequisites/epilogue rather than additional business phases. */
const char *msconnector_transaction_phase_contract_semantics(
    enum msconnector_phase phase);
const char *msconnector_transaction_contract_status_name(
    msconnector_transaction_contract_status status);
const char *msconnector_transaction_error_class_name(
    msconnector_transaction_error_class error_class);
const char *msconnector_transaction_transition_name(int transition);
const char *msconnector_transaction_decision_kind_name(
    msconnector_transaction_decision_kind kind);
const char *msconnector_transaction_fail_policy_name(
    msconnector_transaction_fail_policy policy);

msconnector_transaction_phase_route msconnector_transaction_profile_phase_route(
    const msconnector_transaction_profile *profile,
    enum msconnector_phase phase);

/* Validate an exact-length, host-supplied transaction identifier before an
 * adapter retains it or presents it to a native engine. The value must be a
 * non-empty printable-ASCII key shorter than the contract storage, with no
 * leading/trailing whitespace or embedded control/NUL bytes. */
int msconnector_transaction_contract_validate_transaction_id_bytes(
    const char *transaction_id, size_t transaction_id_length);

/* A zero transition timestamp is normalized by the Common contract to a
 * nonzero local value and never moves a retained lifecycle timestamp backwards. */
int msconnector_transaction_contract_init(msconnector_transaction_contract *contract,
    const msconnector_transaction_profile *profile,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    msconnector_transaction_mode mode,
    uint64_t now_ms);
int msconnector_transaction_contract_record_request_metadata(
    msconnector_transaction_contract *contract,
    const char *method,
    const char *uri,
    const char *content_type,
    size_t header_count,
    size_t header_bytes,
    size_t body_limit);
int msconnector_transaction_contract_record_response_metadata(
    msconnector_transaction_contract *contract,
    int status,
    const char *content_type,
    size_t header_count,
    size_t header_bytes,
    size_t body_limit);
int msconnector_transaction_contract_record_body(msconnector_transaction_contract *contract,
    int response_direction,
    size_t bytes);
int msconnector_transaction_contract_set_response_committed(
    msconnector_transaction_contract *contract,
    int committed);
int msconnector_transaction_contract_begin_phase(msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms);
/*
 * Starts a phase delivered by the response-capable companion of a
 * request-only protocol.  It is deliberately separate from begin_phase() so
 * a direct adapter cannot silently consume a companion-only phase.
 */
int msconnector_transaction_contract_begin_companion_phase(
    msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms);
int msconnector_transaction_contract_complete_phase(msconnector_transaction_contract *contract,
    enum msconnector_phase phase,
    uint64_t now_ms);
int msconnector_transaction_contract_can_append_body(
    const msconnector_transaction_contract *contract,
    int response_direction);
int msconnector_transaction_contract_record_decision(
    msconnector_transaction_contract *contract,
    msconnector_transaction_decision_kind kind,
    const char *rule_id,
    uint64_t now_ms);
int msconnector_transaction_contract_cancel(msconnector_transaction_contract *contract,
    int upstream_disconnect,
    uint64_t now_ms);
int msconnector_transaction_contract_timeout(msconnector_transaction_contract *contract,
    uint64_t now_ms);
int msconnector_transaction_contract_handoff_response_companion(
    msconnector_transaction_contract *contract,
    uint64_t now_ms);
/* Claims a live handoff exactly once at the trusted response observer. It
 * changes HANDOFF back to the next-phase waiting state; only companion P3/P4
 * may then advance the FSM. */
int msconnector_transaction_contract_claim_response_companion(
    msconnector_transaction_contract *contract,
    uint64_t now_ms);
int msconnector_transaction_contract_fail(msconnector_transaction_contract *contract,
    msconnector_transaction_error_class error_class,
    uint64_t now_ms);
int msconnector_transaction_contract_finish(msconnector_transaction_contract *contract,
    uint64_t now_ms);
/* An incomplete non-terminal lifecycle first becomes a terminal
 * connector-error decision with CLEANUP_INCOMPLETE before it is marked
 * CLEANED. Callers must treat PREMATURE_CLEANUP as an observable lifecycle
 * failure, not a successful normal completion. */
int msconnector_transaction_contract_cleanup(msconnector_transaction_contract *contract,
    uint64_t now_ms);
int msconnector_transaction_contract_is_terminal(
    const msconnector_transaction_contract *contract);
int msconnector_transaction_contract_decision_policy(
    const msconnector_transaction_contract *contract,
    msconnector_transaction_decision_kind kind,
    msconnector_transaction_decision_policy *out);
msconnector_transaction_decision_kind
msconnector_transaction_decision_kind_from_engine(const msconnector_decision *decision);

void msconnector_transaction_correlation_registry_init(
    msconnector_transaction_correlation_registry *registry);
int msconnector_transaction_correlation_register_request(
    msconnector_transaction_correlation_registry *registry,
    const msconnector_transaction_contract *transaction,
    uint64_t now_ms,
    uint64_t ttl_ms);
int msconnector_transaction_correlation_claim_response(
    msconnector_transaction_correlation_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    uint64_t now_ms,
    msconnector_transaction_contract *out);
/* Releases only a claimed, caller-owned response snapshot. It rejects an
 * unclaimed mapping and wipes the bounded registry entry after deterministic
 * cleanup of the supplied snapshot. */
int msconnector_transaction_correlation_release(
    msconnector_transaction_correlation_registry *registry,
    msconnector_transaction_contract *transaction,
    uint64_t now_ms);
/* Removes a request mapping only before a response claim; used to roll back a
 * failed request-to-companion handoff without granting arbitrary release of a
 * live claimed response. */
int msconnector_transaction_correlation_revoke_request(
    msconnector_transaction_correlation_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    uint64_t now_ms);
size_t msconnector_transaction_correlation_expire(
    msconnector_transaction_correlation_registry *registry,
    uint64_t now_ms);

#ifdef __cplusplus
}
#endif

#endif
