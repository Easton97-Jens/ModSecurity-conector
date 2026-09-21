#ifndef MSCONNECTOR_EVENT_PROTOCOL_H
#define MSCONNECTOR_EVENT_PROTOCOL_H

#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include <string.h>

#define MSCONN_EVENT_PHASE4_HARD_ABORT "MSCONN_EVENT_PHASE4_HARD_ABORT"
#define MSCONN_EVENT_PHASE4_STREAM_RESET "MSCONN_EVENT_PHASE4_STREAM_RESET"

/* A metadata-only, idempotent view shared by JSONL and the integrity hash.
 * It never changes byte counts, timestamps, HTTP status observations, EOS,
 * commitment, or transport flags. Validate the original event before writing
 * this view so normalization cannot conceal invalid/oversized source fields.
 * Unknown application events are preserved, not reclassified as WAF events.
 */
static inline int msconnector_event_protocol_equal(const char *left,
    const char *right)
{
    return left != NULL && right != NULL && strcmp(left, right) == 0;
}

static inline const char *msconnector_event_protocol_action(const char *action)
{
    if (msconnector_event_protocol_equal(action, "pass")) {
        return "allow";
    }
    if (msconnector_event_protocol_equal(action, "abort") ||
        msconnector_event_protocol_equal(action, "connection_abort")) {
        return "abort_connection";
    }
    return action;
}

static inline const char *msconnector_event_protocol_error_name(const char *id)
{
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_ENGINE_TIMEOUT)) {
        return "engine_timeout";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_ENGINE_UNAVAILABLE)) {
        return "engine_unavailable";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_INVALID_ENGINE_RESPONSE)) {
        return "invalid_engine_response";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_PROTOCOL_ERROR)) {
        return "protocol_error";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_CONFIG_ERROR)) {
        return "config_error";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_RULE_PARSE_ERROR)) {
        return "rule_parse_error";
    }
    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_INTERNAL_ERROR) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_CONNECTOR_ERROR)) {
        return "connector_error";
    }
    return NULL;
}

static inline int msconnector_event_protocol_rule_event(const char *id)
{
    return msconnector_event_protocol_equal(id, MSCONN_EVENT_REQUEST_BLOCKED) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_RESPONSE_BLOCKED) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_LATE_INTERVENTION) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_HARD_ABORT) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_STREAM_RESET);
}

static inline const char *msconnector_event_protocol_phase_event(
    enum msconnector_phase phase)
{
    switch (phase) {
    case MSCONNECTOR_PHASE_REQUEST_HEADERS: return "phase1_intervention";
    case MSCONNECTOR_PHASE_REQUEST_BODY: return "phase2_intervention";
    case MSCONNECTOR_PHASE_RESPONSE_HEADERS: return "phase3_intervention";
    case MSCONNECTOR_PHASE_RESPONSE_BODY: return "phase4_intervention";
    default: return "engine_decision";
    }
}

static inline void msconnector_event_protocol_rule_view(msconnector_event *event)
{
    const char *actual = event->decision.actual_action;
    const int late = event->flags.late_intervention ||
        event->flags.response_committed || event->flags.headers_sent;

    event->meta.event = msconnector_event_protocol_phase_event(event->decision.phase);
    /* A decision without a host transport observation is not an executed
     * deny/abort. A later host-action record carries that observation. */
    if (event->http.transport_result == NULL ||
        event->http.transport_result[0] == '\0') {
        event->meta.event = "engine_decision";
        event->decision.actual_action = "";
        return;
    }
    if (event->decision.phase != MSCONNECTOR_PHASE_RESPONSE_BODY || !late) {
        return;
    }
    if (msconnector_event_protocol_equal(actual, "log_only")) {
        event->meta.message_id = MSCONN_EVENT_PHASE4_LATE_INTERVENTION;
        if (msconnector_event_protocol_equal(event->flags.late_intervention_mode, "safe")) {
            event->decision.reason = "response_committed_safe";
        }
    } else if (msconnector_event_protocol_equal(actual, "abort_connection")) {
        event->meta.message_id = event->http.original_http_status == 200
            ? MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200
            : MSCONN_EVENT_PHASE4_HARD_ABORT;
        if (msconnector_event_protocol_equal(event->flags.late_intervention_mode, "strict")) {
            event->decision.reason = "response_committed_strict";
        }
    } else if (msconnector_event_protocol_equal(actual, "stream_reset")) {
        event->meta.message_id = MSCONN_EVENT_PHASE4_STREAM_RESET;
    }
}

static inline int msconnector_event_protocol_view(const msconnector_event *source,
    msconnector_event *out)
{
    const char *error_name;
    const char *id;
    int known;

    if (source == NULL || out == NULL) {
        return 0;
    }
    *out = *source;
    id = out->meta.message_id;
    error_name = msconnector_event_protocol_error_name(id);
    known = error_name != NULL || msconnector_event_protocol_rule_event(id) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_BODY_LIMIT) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) ||
        msconnector_event_protocol_equal(id, "MSCONN_EVENT_RULE_MATCHED") ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_CLIENT_CANCEL) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_UPSTREAM_DISCONNECT);
    if (!known) {
        return 1;
    }
    out->decision.action = msconnector_event_protocol_action(out->decision.action);
    out->decision.requested_action = msconnector_event_protocol_action(out->decision.requested_action);
    out->decision.actual_action = msconnector_event_protocol_action(out->decision.actual_action);
    if (error_name != NULL) {
        out->meta.event = error_name;
        out->decision.status = MSCONNECTOR_STATUS_ERROR;
        out->decision.reason = error_name;
        out->decision.requested_action = "error";
        out->decision.rule_id = "";
        if (out->http.transport_result == NULL || out->http.transport_result[0] == '\0') {
            out->decision.action = "error";
            out->decision.actual_action = "";
        }
    } else if (msconnector_event_protocol_rule_event(id)) {
        msconnector_event_protocol_rule_view(out);
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_BODY_LIMIT)) {
        out->meta.event = "body_limit";
        out->decision.reason = out->decision.phase == MSCONNECTOR_PHASE_RESPONSE_BODY
            ? "response_body_limit_exceeded" : "request_body_limit_exceeded";
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY)) {
        out->meta.event = "unsupported_capability";
        out->decision.status = MSCONNECTOR_STATUS_UNSUPPORTED;
        out->decision.reason = "unsupported_capability";
    } else if (msconnector_event_protocol_equal(id, "MSCONN_EVENT_RULE_MATCHED")) {
        out->meta.event = "rule_match";
        out->meta.message = "Non-disruptive ModSecurity rule match observed.";
        out->meta.level = "info";
        return 1;
    } else {
        out->meta.event = msconnector_event_protocol_equal(id, MSCONN_EVENT_CLIENT_CANCEL)
            ? "client_cancel" : "upstream_disconnect";
    }
    if (out->decision.actual_action != NULL && out->decision.actual_action[0] != '\0') {
        out->decision.action = out->decision.actual_action;
    }
    if (msconnector_event_protocol_equal(out->meta.message_id, MSCONN_EVENT_PHASE4_HARD_ABORT)) {
        out->meta.message = "Phase 4 requested a connection abort after response commitment.";
        out->meta.level = "error";
    } else if (msconnector_event_protocol_equal(out->meta.message_id, MSCONN_EVENT_PHASE4_STREAM_RESET)) {
        out->meta.message = "Phase 4 requested a stream reset after response commitment.";
        out->meta.level = "error";
    } else {
        out->meta.message = msconnector_event_default_message(out->meta.message_id);
        out->meta.level = msconnector_event_default_level(out->meta.message_id);
    }
    if (out->http.http_status > 0) {
        out->http.http_reason_phrase = msconnector_http_status_reason_phrase(out->http.http_status);
        out->http.http_default_message = msconnector_http_status_default_message(out->http.http_status);
    }
    return 1;
}

#endif
