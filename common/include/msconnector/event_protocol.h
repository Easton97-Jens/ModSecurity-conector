#ifndef MSCONNECTOR_EVENT_PROTOCOL_H
#define MSCONNECTOR_EVENT_PROTOCOL_H

#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include <string.h>

#define MSCONN_EVENT_PHASE4_HARD_ABORT "MSCONN_EVENT_PHASE4_HARD_ABORT"
#define MSCONN_EVENT_PHASE4_STREAM_RESET "MSCONN_EVENT_PHASE4_STREAM_RESET"
#define MSCONN_EVENT_ENGINE_DECISION "MSCONN_EVENT_ENGINE_DECISION"
#define MSCONNECTOR_EVENT_ACTION_ABORT "abort_connection"

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

static inline int msconnector_event_protocol_has_observation(
    const msconnector_event *event)
{
    const char *result = event->http.transport_result;

    /* The explicit absence marker carries no more evidence than NULL or an
     * empty field. In particular, it cannot confirm an earlier abort request. */
    return result != NULL && result[0] != '\0' &&
        !msconnector_event_protocol_equal(result, "not_observable");
}

static inline const char *msconnector_event_protocol_action(const char *action)
{
    if (msconnector_event_protocol_equal(action, "pass")) {
        return "allow";
    }
    if (msconnector_event_protocol_equal(action, "abort") ||
        msconnector_event_protocol_equal(action, "connection_abort")) {
        return MSCONNECTOR_EVENT_ACTION_ABORT;
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
        msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_STREAM_RESET) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_ENGINE_DECISION);
}

static inline int msconnector_event_protocol_known(const char *id,
    const char *error_name)
{
    return error_name != NULL || msconnector_event_protocol_rule_event(id) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_BODY_LIMIT) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) ||
        msconnector_event_protocol_equal(id, "MSCONN_EVENT_RULE_MATCHED") ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_CLIENT_CANCEL) ||
        msconnector_event_protocol_equal(id, MSCONN_EVENT_UPSTREAM_DISCONNECT);
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
    if (!msconnector_event_protocol_has_observation(event)) {
        event->meta.event = "engine_decision";
        event->meta.message_id = MSCONN_EVENT_ENGINE_DECISION;
        event->decision.actual_action = "";
        event->decision.action = event->decision.requested_action;
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
    } else if (msconnector_event_protocol_equal(actual, MSCONNECTOR_EVENT_ACTION_ABORT)) {
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

static inline void msconnector_event_protocol_error_view(msconnector_event *event,
    const char *error_name)
{
    event->meta.event = error_name;
    event->decision.status = MSCONNECTOR_STATUS_ERROR;
    event->decision.reason = error_name;
    event->decision.requested_action = "error";
    event->decision.rule_id = "";
    if (!msconnector_event_protocol_has_observation(event)) {
        event->decision.action = "error";
        event->decision.actual_action = "";
    }
}

static inline void msconnector_event_protocol_decision_view(msconnector_event *event,
    const char *error_name)
{
    const char *id = event->meta.message_id;

    if (error_name != NULL) {
        msconnector_event_protocol_error_view(event, error_name);
    } else if (msconnector_event_protocol_rule_event(id)) {
        msconnector_event_protocol_rule_view(event);
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_BODY_LIMIT)) {
        event->meta.event = "body_limit";
        event->decision.reason = event->decision.phase == MSCONNECTOR_PHASE_RESPONSE_BODY
            ? "response_body_limit_exceeded" : "request_body_limit_exceeded";
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY)) {
        event->meta.event = "unsupported_capability";
        event->decision.status = MSCONNECTOR_STATUS_UNSUPPORTED;
        event->decision.reason = event->meta.event;
    } else {
        event->meta.event = msconnector_event_protocol_equal(id, MSCONN_EVENT_CLIENT_CANCEL)
            ? "client_cancel" : "upstream_disconnect";
    }
}

/* Policy limits, unsupported capabilities and cancellation events need the
 * same observation boundary as rule and engine errors. An event's existence
 * is not evidence that the host performed its requested transport action. */
static inline void msconnector_event_protocol_observed_action_view(
    msconnector_event *event)
{
    if (!msconnector_event_protocol_has_observation(event)) {
        event->decision.actual_action = "";
        event->decision.action = event->decision.requested_action;
    } else if (event->decision.actual_action != NULL &&
        event->decision.actual_action[0] != '\0') {
        event->decision.action = event->decision.actual_action;
    }
}

static inline void msconnector_event_protocol_message_view(msconnector_event *event)
{
    const char *id = event->meta.message_id;

    if (msconnector_event_protocol_equal(id, MSCONN_EVENT_ENGINE_DECISION)) {
        event->meta.message = "ModSecurity requested an intervention; host action is not observed.";
        event->meta.level = "warn";
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_HARD_ABORT)) {
        event->meta.message = "Phase 4 requested a connection abort after response commitment.";
        event->meta.level = "error";
    } else if (msconnector_event_protocol_equal(id, MSCONN_EVENT_PHASE4_STREAM_RESET)) {
        event->meta.message = "Phase 4 requested a stream reset after response commitment.";
        event->meta.level = "error";
    } else {
        event->meta.message = msconnector_event_default_message(id);
        event->meta.level = msconnector_event_default_level(id);
    }
    if (event->http.http_status > 0) {
        event->http.http_reason_phrase = msconnector_http_status_reason_phrase(event->http.http_status);
        event->http.http_default_message = msconnector_http_status_default_message(event->http.http_status);
    }
}

static inline int msconnector_event_protocol_view(const msconnector_event *source,
    msconnector_event *out)
{
    const char *error_name;

    if (source == NULL || out == NULL) {
        return 0;
    }
    *out = *source;
    error_name = msconnector_event_protocol_error_name(out->meta.message_id);
    if (!msconnector_event_protocol_known(out->meta.message_id, error_name)) {
        return 1;
    }
    out->decision.action = msconnector_event_protocol_action(out->decision.action);
    out->decision.requested_action = msconnector_event_protocol_action(out->decision.requested_action);
    out->decision.actual_action = msconnector_event_protocol_action(out->decision.actual_action);
    if (msconnector_event_protocol_equal(out->meta.message_id, "MSCONN_EVENT_RULE_MATCHED")) {
        out->meta.event = "rule_match";
        out->meta.message = "Non-disruptive ModSecurity rule match observed.";
        out->meta.level = "info";
        return 1;
    }
    msconnector_event_protocol_decision_view(out, error_name);
    msconnector_event_protocol_observed_action_view(out);
    msconnector_event_protocol_message_view(out);
    return 1;
}

#endif
