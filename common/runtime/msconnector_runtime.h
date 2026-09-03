#ifndef MSCONNECTOR_RUNTIME_H
#define MSCONNECTOR_RUNTIME_H

#include <stddef.h>
#include <stdint.h>
#include <stdatomic.h>

#include "msconnector/body_policy.h"
#include "msconnector/decision.h"
#include "msconnector/decision_action.h"
#include "msconnector/error.h"
#include "msconnector/options.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"
#include "msconnector/transaction_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral, libmodsecurity-backed runtime used by external-service
 * and native-module adapters. Host API types deliberately do not cross this
 * boundary. The runtime owns its engine, rules and configuration strings;
 * request/response objects and body chunks are borrowed only for their
 * corresponding call. A transaction retains bounded metadata, never a host
 * request, response, or body pointer.
 */
typedef struct msconnector_runtime msconnector_runtime;
typedef struct msconnector_runtime_transaction msconnector_runtime_transaction;

/* A request-only adapter transfers ownership of a live native transaction to
 * this fixed-capacity in-process registry. It retains no host request,
 * response, or body pointer between calls; only the opaque native transaction
 * and its metadata-only contract snapshot are retained until P3/P4 completes
 * or the TTL expires. */
#define MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY \
    MSCONNECTOR_TRANSACTION_CORRELATION_CAPACITY
#define MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_BYTES 32U
#define MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE \
    (MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_BYTES * 2U + 1U)
typedef struct msconnector_runtime_response_companion_entry {
    int occupied;
    int in_use;
    int transport_claimed;
    uint64_t expires_at_ms;
    uint64_t ttl_ms;
    msconnector_runtime_transaction *transaction;
    msconnector_transaction_contract correlation;
    /* A server-generated, cryptographically random, single-claim capability.
     * It is never derived from a request ID and is used only by the private
     * response-observer transport; transaction/host IDs remain internal. */
    char response_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];
} msconnector_runtime_response_companion_entry;
typedef struct msconnector_runtime_response_companion_registry {
    atomic_flag lock;
    int shutting_down;
    msconnector_runtime_response_companion_entry entries[
        MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY];
} msconnector_runtime_response_companion_registry;

/* A live claimed observer connection. The entry is leased for the entire
 * connection so another stream cannot reuse the capability. It is intentionally
 * opaque to host adapters: use only the session operations below. */
typedef struct msconnector_runtime_response_companion_session {
    msconnector_runtime_response_companion_registry *registry;
    msconnector_runtime_response_companion_entry *entry;
    int active;
} msconnector_runtime_response_companion_session;

/*
 * Body chunks are borrowed from the host.  The runtime never retains a chunk
 * pointer after append_*_body_chunk() returns.  Counters describe metadata
 * only and are safe to place in events or result records.
 */
typedef struct msconnector_runtime_body_progress {
    size_t bytes_seen;
    size_t bytes_inspected;
    int truncated;
    int finished;
    msconnector_body_limit_outcome limit_outcome;
} msconnector_runtime_body_progress;

/* A bounded, payload-free copy of the Common-owned transaction state. */
typedef struct msconnector_runtime_transaction_snapshot {
    msconnector_transaction_contract contract;
    msconnector_runtime_body_progress request_body;
    msconnector_runtime_body_progress response_body;
    int response_original_status;
    int response_headers_processed;
    int response_headers_sent;
    int response_body_started;
    int finished;
} msconnector_runtime_transaction_snapshot;

int msconnector_runtime_config_check(
    const char *connector_name,
    const char *config_path,
    char *error,
    size_t error_len);

int msconnector_runtime_create(
    const char *connector_name,
    const char *config_path,
    msconnector_runtime **out,
    char *error,
    size_t error_len);

/*
 * Sets the bounded, connector-specific integration mode copied into every
 * Common decision event produced by this runtime. Call this during adapter
 * setup, before beginning transactions; the runtime copies the value and
 * never derives it from request metadata.
 */
int msconnector_runtime_set_event_integration_mode(
    msconnector_runtime *runtime,
    const char *integration_mode);

/* Inject the immutable adapter-selected profile before the first
 * transaction. The runtime never resolves a profile from connector or mode
 * strings. NULL is rejected so an unset profile remains fail-closed. A
 * phase4_mode=strict runtime also rejects a profile without a source-proven
 * strict_post_commit_action; it must not start and later downgrade a late
 * disruptive decision to log_only. */
int msconnector_runtime_set_transaction_profile(
    msconnector_runtime *runtime,
    const msconnector_transaction_profile *profile);

void msconnector_runtime_destroy(msconnector_runtime **runtime);

void msconnector_runtime_request_contract(
    const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract);

void msconnector_runtime_response_contract(
    const msconnector_runtime *runtime,
    msconnector_response_mapper_contract *contract);

size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime);
size_t msconnector_runtime_response_body_limit(const msconnector_runtime *runtime);
msconnector_body_limit_action msconnector_runtime_body_limit_action(
    const msconnector_runtime *runtime);
msconnector_body_mode msconnector_runtime_request_body_mode(
    const msconnector_runtime *runtime);
msconnector_body_mode msconnector_runtime_response_body_mode(
    const msconnector_runtime *runtime);
/* Returns the parsed common policy mode so a connector does not need a
 * connector-local copy of Phase-4 configuration. */
enum msconnector_phase4_mode msconnector_runtime_phase4_mode(
    const msconnector_runtime *runtime);
size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime);
size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime);
/* A request-only service may write a sanitized Common error classification to
 * its host error log when this configured diagnostic is enabled.  It must
 * never log the request, response, or a body payload here. */
int msconnector_runtime_error_log_enabled(const msconnector_runtime *runtime);

/* The parsed budget is in milliseconds. A zero value disables it. Common
 * stores this adapter-facing value but does not own a host timer or a
 * cancellation primitive, so callers must not treat the getter as proof that
 * their transport enforces a deadline. */
size_t msconnector_runtime_late_intervention_timeout_ms(
    const msconnector_runtime *runtime);

/*
 * Maps a concrete runtime error to the configured HTTP error policy while
 * preserving protocol-specific statuses such as body-limit and timeout
 * failures.
 */
int msconnector_runtime_error_http_status(
    const msconnector_runtime *runtime,
    msconnector_error_code code);

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error);

/*
 * Explicit low-latency lifecycle operations.  Request/response headers are
 * processed once.  Body chunks are ingested incrementally and phase 2/4 is
 * finalized exactly once at end of stream.  libmodsecurity may evaluate body
 * rules during the finish call rather than on an individual chunk.
 */
int msconnector_runtime_transaction_append_request_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error);

int msconnector_runtime_transaction_finish_request_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_process_response_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_append_response_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error);

int msconnector_runtime_transaction_finish_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error);

/*
 * Close a response lifecycle that deliberately has no decoded entity-body
 * input.  This is only valid with response_body_mode=none and never invokes
 * libmodsecurity's response-body processing or produces Phase-4 evidence.
 * A host must call it only after its real response stream has ended or has
 * been abandoned.
 */
int msconnector_runtime_transaction_finish_unobserved_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error);

/*
 * Close a native streaming transaction after the host has rejected its
 * incomplete request body before EOS. This records the logging phase exactly
 * once, but never processes or finalizes the request body, marks request-body
 * EOS, or produces a Phase-2 decision. It is only for a terminal host-side
 * rejection, not an alternative to the normal EOS-enforcing finish path.
 */
int msconnector_runtime_transaction_finish_host_rejected_request_body(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error);

/*
 * Hosts call this immediately before or after handing bytes to their next
 * filter.  It records only commit metadata; it cannot retroactively change a
 * response and does not retain any host buffer.
 */
/* Checked form used by all new adapters. It rejects a response commit before
 * P3 completed and a commit after the transaction reached a terminal state. */
int msconnector_runtime_transaction_set_response_commit_state_checked(
    msconnector_runtime_transaction *transaction,
    int headers_sent,
    int body_started,
    msconnector_error *error);

/* Compatibility wrapper. On an invalid transition it terminally marks the
 * canonical contract; new adapters must use the checked form above. */
void msconnector_runtime_transaction_set_response_commit_state(
    msconnector_runtime_transaction *transaction,
    int headers_sent,
    int body_started);

/*
 * Records a second, host-confirmed outcome for a disruptive engine decision.
 * The normal decision event is deliberately retained: it records what the
 * rule engine requested, while this call records what the host actually did
 * after applying (or intentionally downgrading) that request.  Call it only
 * after the host action has succeeded or the host has deliberately selected a
 * late log-only outcome.  `visible_http_status` is the status observable by
 * the client; it may be zero only for a transport-only connection abort or a
 * stream-local reset.  A stream reset must use actual action
 * `MSCONNECTOR_DECISION_ACTION_STREAM_RESET`, `transport_result="stream_reset"`,
 * and `connection_aborted=0`; it is not a substitute for a connection abort.
 * The runtime never retains `transport_result`.
 */
int msconnector_runtime_transaction_record_host_action(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    msconnector_decision_action actual_action,
    int visible_http_status,
    const char *transport_result,
    int connection_aborted,
    msconnector_error *error);

/* Records a host-observed cancellation or an engine deadline expiry in the
 * same canonical state machine. The caller translates the resulting policy
 * into its protocol-specific action. */
int msconnector_runtime_transaction_cancel(
    msconnector_runtime_transaction *transaction,
    int upstream_disconnect,
    msconnector_error *error);
int msconnector_runtime_transaction_timeout(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error);

/* Records a typed non-engine terminal outcome without collapsing protocol,
 * connector, body-limit, client-cancel, and upstream-disconnect failures into
 * one host-specific cancellation path.  Adapters use this when they observe
 * a failure at their protocol boundary after a Common transaction exists. */
int msconnector_runtime_transaction_fail(
    msconnector_runtime_transaction *transaction,
    msconnector_transaction_error_class error_class,
    msconnector_error *error);

/* Records the action that actually reached the host boundary after a typed
 * terminal failure.  Unlike record_host_action(), this has no rule-engine
 * decision or rule correlation: it represents a bounded protocol/connector
 * failure, a body-limit rejection, or an observed connection abort. */
int msconnector_runtime_transaction_record_failure_host_action(
    msconnector_runtime_transaction *transaction,
    int visible_http_status,
    int connection_aborted,
    msconnector_error *error);

/*
 * Live response companion registry. `handoff()` transfers transaction
 * ownership on success, so the request service must not finish or destroy it.
 * The response observer invokes P3/P4 through this registry; no raw native
 * pointer is exposed and each lookup verifies transaction, connector, host,
 * TTL, and the companion-only profile route.
 */
void msconnector_runtime_response_companion_registry_init(
    msconnector_runtime_response_companion_registry *registry);
/* Secure transport handoff. On success `handle` receives a 64-character
 * lower-case hexadecimal opaque capability plus NUL. The caller may pass the
 * handle only to its trusted local observer; it must never substitute a
 * client-supplied transaction or host identifier for this value. */
int msconnector_runtime_response_companion_handoff_with_handle(
    msconnector_runtime_response_companion_registry *registry,
    msconnector_runtime_transaction *transaction,
    uint64_t ttl_ms,
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error);
/* Revokes an unclaimed opaque capability after authorization delivery fails.
 * Claimed sessions are never detached through this path. */
int msconnector_runtime_response_companion_revoke_handle(
    msconnector_runtime_response_companion_registry *registry,
    const char *handle,
    msconnector_error *error);
/* Claims an opaque transport capability exactly once. A claimed session owns
 * the registry lease until release/cancel/expiry; no transaction or host ID
 * crosses this boundary. */
int msconnector_runtime_response_companion_claim_handle(
    msconnector_runtime_response_companion_registry *registry,
    const char *handle,
    msconnector_runtime_response_companion_session *session,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_process_response_headers(
    msconnector_runtime_response_companion_session *session,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_append_response_body_chunk(
    msconnector_runtime_response_companion_session *session,
    const unsigned char *data,
    size_t size,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_finish_response_body(
    msconnector_runtime_response_companion_session *session,
    msconnector_decision *decision,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_set_response_commit_state(
    msconnector_runtime_response_companion_session *session,
    int headers_sent,
    int body_started,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_record_host_action(
    msconnector_runtime_response_companion_session *session,
    const msconnector_decision *decision,
    msconnector_decision_action actual_action,
    int visible_http_status,
    const char *transport_result,
    int connection_aborted,
    msconnector_error *error);
/* Fails the claimed transaction with a precise canonical error class and
 * releases its lease. This is used for malformed/invalid observer protocol
 * input; a peer disconnect instead uses session_cancel(). */
int msconnector_runtime_response_companion_session_fail(
    msconnector_runtime_response_companion_session *session,
    msconnector_transaction_error_class error_class,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_cancel(
    msconnector_runtime_response_companion_session *session,
    int upstream_disconnect,
    msconnector_error *error);
int msconnector_runtime_response_companion_session_release(
    msconnector_runtime_response_companion_session *session,
    msconnector_error *error);
size_t msconnector_runtime_response_companion_expire(
    msconnector_runtime_response_companion_registry *registry,
    uint64_t now_ms);
/* Stop accepting new companion operations and deterministically release all
 * entries after the response observer has quiesced. A nonzero in-use entry is
 * reported as an error rather than being freed while a native call may still
 * access it. */
int msconnector_runtime_response_companion_registry_shutdown(
    msconnector_runtime_response_companion_registry *registry,
    msconnector_error *error);

void msconnector_runtime_transaction_request_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress);

void msconnector_runtime_transaction_response_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress);

int msconnector_runtime_transaction_snapshot_get(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_transaction_snapshot *snapshot);

/* Finish and clean up a transaction, then return a bounded, payload-free
 * snapshot of the final cleaned state.  The transaction pointer is consumed
 * only on success.  On failure the caller retains ownership and must use the
 * normal destroy path; this prevents evidence publication from claiming a
 * cleanup that did not complete. */
int msconnector_runtime_transaction_finalize_and_snapshot(
    msconnector_runtime_transaction **transaction,
    msconnector_runtime_transaction_snapshot *snapshot,
    msconnector_error *error);

/* Buffered compatibility helper. Prefer the explicit header/chunk/finish API
 * for full-lifecycle paths. */
int msconnector_runtime_transaction_process_response(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_finish(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error);

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction);

void msconnector_runtime_transaction_destroy(
    msconnector_runtime_transaction **transaction);

#ifdef __cplusplus
}
#endif

#endif
