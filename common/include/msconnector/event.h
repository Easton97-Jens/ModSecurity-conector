#ifndef MSCONNECTOR_EVENT_H
#define MSCONNECTOR_EVENT_H

#include "msconnector/status.h"
#include "msconnector/transaction.h"
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define MSCONN_EVENT_REQUEST_BLOCKED "MSCONN_EVENT_REQUEST_BLOCKED"
#define MSCONN_EVENT_RESPONSE_BLOCKED "MSCONN_EVENT_RESPONSE_BLOCKED"
#define MSCONN_EVENT_PHASE4_LATE_INTERVENTION "MSCONN_EVENT_PHASE4_LATE_INTERVENTION"
#define MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200 "MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200"
#define MSCONN_EVENT_UNSUPPORTED_CAPABILITY "MSCONN_EVENT_UNSUPPORTED_CAPABILITY"
#define MSCONN_EVENT_INTERNAL_ERROR "MSCONN_EVENT_INTERNAL_ERROR"
#define MSCONN_EVENT_CONFIG_ERROR "MSCONN_EVENT_CONFIG_ERROR"
#define MSCONN_EVENT_RULE_PARSE_ERROR "MSCONN_EVENT_RULE_PARSE_ERROR"

/*
 * Connector-neutral event metadata.
 *
 * Pointer fields are borrowed. The caller owns their lifetime.
 * This structure is connector-neutral metadata only and does not own strings.
 * It does not include request or response bodies.
 */
typedef struct msconnector_event_meta {
    const char *timestamp;
    const char *level;
    const char *message_id;
    const char *message;
    const char *event;
    const char *connector;
    const char *integration_mode;
    /* Run identity is bounded metadata supplied by the canonical harness. */
    const char *run_id;
    /* Bounded client-to-host correlation token for a transport case. */
    const char *transport_case_id;
    const char *transaction_id;
} msconnector_event_meta;

/*
 * Connector-neutral decision metadata for an event.
 *
 * Pointer fields are borrowed. The caller owns their lifetime.
 * This structure is connector-neutral metadata only and does not own strings.
 * It does not include request or response bodies.
 */
typedef struct msconnector_event_decision {
    enum msconnector_phase phase;
    enum msconnector_status status;
    const char *action;
    const char *requested_action;
    const char *actual_action;
    const char *rule_id;
    const char *reason;
} msconnector_event_decision;

/*
 * Connector-neutral HTTP metadata for an event.
 *
 * Pointer fields are borrowed. The caller owns their lifetime.
 * This structure is connector-neutral metadata only and does not own strings.
 * It does not include request or response bodies.
 */
typedef struct msconnector_event_http {
    int http_status;
    int original_http_status;
    int visible_http_status;
    const char *transport_result;
    const char *http_reason_phrase;
    const char *http_default_message;
} msconnector_event_http;

/*
 * Connector-neutral downstream/upstream protocol provenance.
 *
 * All pointer fields are borrowed bounded metadata.  ``connection_id`` is
 * only an opaque non-reversible token for non-QUIC transports; a raw QUIC
 * connection ID must never be stored here.  HTTP/3 records use only
 * ``quic_connection_id_present`` and (when available) ``quic_version``.
 */
typedef struct msconnector_event_protocol {
    const char *requested_protocol;
    const char *downstream_protocol;
    const char *upstream_protocol;
    const char *negotiated_protocol;
    const char *transport;
    const char *alpn;
    const char *stream_id;
    const char *connection_id;
    const char *quic_version;
    const char *stream_reset_code;
    /* Actor and code are bounded transport metadata, never raw frames. */
    const char *reset_by;
    const char *reset_code;
    int connection_reused;
    int quic_connection_id_present;
    int fallback_used;
    int stream_reset;
} msconnector_event_protocol;

/*
 * Connector-neutral request-identifying metadata for an event.
 *
 * Pointer fields are borrowed. The caller owns their lifetime.
 * This structure is connector-neutral metadata only and does not own strings.
 * It does not include request or response bodies.
 */
typedef struct msconnector_event_request {
    const char *method;
    const char *uri;
    const char *client_ip;
} msconnector_event_request;

/*
 * Connector-neutral boolean event flags.
 *
 * This structure is connector-neutral metadata only. The flags describe how a
 * connector may classify a future event record; they do not imply runtime
 * integration in any existing connector.
 */
typedef struct msconnector_event_integrity {
    unsigned long sequence;
    uint64_t previous_hash;
    uint64_t event_hash;
} msconnector_event_integrity;

typedef struct msconnector_event_flags {
    int late_intervention;
    /* Optional selected late-action policy (`minimal`, `safe`, or `strict`).
     * It is metadata, never a request or response body fragment. */
    const char *late_intervention_mode;
    int response_started;
    int response_committed;
    int headers_sent;
    int body_started;
    int body_truncated;
    int connection_aborted;
    /* Transport lifecycle observations are explicit so an internal callback
     * failure cannot be mislabeled as a client-visible transport result. */
    int client_disconnected;
    int upstream_disconnected;
    int cancelled;
    int eos_seen;
    /* Bounded canonical values such as `response_body`, `short_write`, and
     * `normal`; they never retain request/response bytes. */
    const char *timeout_stage;
    const char *write_result;
    const char *cleanup_reason;
    int redacted;
    int truncated;
} msconnector_event_flags;

/*
 * Body observations are bounded, payload-free metadata.  ``content_type`` is
 * borrowed and must be a header value, never a body-derived string.  The
 * counters describe bytes observed by the host and bytes supplied to the
 * engine; they do not retain body memory.
 */
typedef struct msconnector_event_body {
    const char *content_type;
    /* Optional canonical limit result (`at_limit`, `over_limit`,
     * `process_partial`, or `reject`); never body data. */
    const char *limit_outcome;
    uint64_t bytes_seen;
    uint64_t bytes_inspected;
} msconnector_event_body;

/*
 * Connector-neutral event model for metadata-only log records.
 *
 * Pointer fields in nested structures are borrowed. The caller owns their
 * lifetime. This structure is connector-neutral metadata only and does not own
 * strings. It does not include request or response bodies.
 */
typedef struct msconnector_event {
    msconnector_event_meta meta;
    msconnector_event_decision decision;
    msconnector_event_http http;
    msconnector_event_protocol protocol;
    msconnector_event_request request;
    msconnector_event_flags flags;
    msconnector_event_body body;
    msconnector_event_integrity integrity;
} msconnector_event;

void msconnector_event_init(msconnector_event *event);
const char *msconnector_event_status_name(const msconnector_event *event);
const char *msconnector_event_default_message(const char *message_id);
const char *msconnector_event_default_level(const char *message_id);
int msconnector_event_write_json_ex(
    const msconnector_event *event,
    char *dst,
    size_t dst_size,
    int *truncated);
int msconnector_event_write_json(const msconnector_event *event, char *dst, size_t dst_size);
void msconnector_event_set_phase4_hard_abort_after_200(
    msconnector_event *event,
    const char *connector,
    const char *transaction_id,
    const char *rule_id,
    const char *reason);

#ifdef __cplusplus
}
#endif

#endif
