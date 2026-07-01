#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include "msconnector/json_escape.h"
#include "msconnector/transaction_state.h"
#include <stdio.h>
#include <string.h>

#define EVENT_TEXT_SIZE 256U
#define EVENT_JSON_TRUE "true"
#define EVENT_JSON_FALSE "false"

static const char *json_bool(int value) {
    return value ? EVENT_JSON_TRUE : EVENT_JSON_FALSE;
}

static void escape_field(const char *src, char *dst, size_t dst_size, int *truncated) {
    const size_t needed = msconnector_json_escape(src, dst, dst_size);
    if (dst_size == 0 || needed >= dst_size) {
        if (truncated != 0) {
            *truncated = 1;
        }
    }
}

const char *msconnector_event_default_message(const char *message_id) {
    if (message_id == 0) {
        return "";
    }
    if (strcmp(message_id, MSCONN_EVENT_REQUEST_BLOCKED) == 0) {
        return "Request blocked by ModSecurity rule.";
    }
    if (strcmp(message_id, MSCONN_EVENT_RESPONSE_BLOCKED) == 0) {
        return "Response blocked by ModSecurity rule.";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_LATE_INTERVENTION) == 0) {
        return "Phase 4 intervention occurred after response output started.";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0) {
        return "Response already started with HTTP 200; Phase 4 requested a block; connection was aborted.";
    }
    if (strcmp(message_id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) == 0) {
        return "Requested capability is not implemented.";
    }
    if (strcmp(message_id, MSCONN_EVENT_INTERNAL_ERROR) == 0) {
        return "Internal connector error.";
    }
    if (strcmp(message_id, MSCONN_EVENT_CONFIG_ERROR) == 0) {
        return "Connector configuration error.";
    }
    if (strcmp(message_id, MSCONN_EVENT_RULE_PARSE_ERROR) == 0) {
        return "ModSecurity rule parsing failed.";
    }
    return "";
}

const char *msconnector_event_default_level(const char *message_id) {
    if (message_id == 0) {
        return "info";
    }
    if (strcmp(message_id, MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200) == 0 ||
        strcmp(message_id, MSCONN_EVENT_INTERNAL_ERROR) == 0 ||
        strcmp(message_id, MSCONN_EVENT_CONFIG_ERROR) == 0 ||
        strcmp(message_id, MSCONN_EVENT_RULE_PARSE_ERROR) == 0) {
        return "error";
    }
    if (strcmp(message_id, MSCONN_EVENT_REQUEST_BLOCKED) == 0 ||
        strcmp(message_id, MSCONN_EVENT_RESPONSE_BLOCKED) == 0 ||
        strcmp(message_id, MSCONN_EVENT_PHASE4_LATE_INTERVENTION) == 0 ||
        strcmp(message_id, MSCONN_EVENT_UNSUPPORTED_CAPABILITY) == 0) {
        return "warn";
    }
    return "info";
}

void msconnector_event_init(msconnector_event *event) {
    if (event == 0) {
        return;
    }

    event->timestamp = 0;
    event->level = "info";
    event->message_id = 0;
    event->message = 0;
    event->event = 0;
    event->connector = 0;
    event->transaction_id = 0;
    event->phase = MSCONNECTOR_PHASE_CONNECTION;
    event->status = MSCONNECTOR_STATUS_OK;
    event->action = 0;
    event->requested_action = 0;
    event->actual_action = 0;
    event->http_status = 0;
    event->original_http_status = 0;
    event->visible_http_status = 0;
    event->http_reason_phrase = 0;
    event->http_default_message = 0;
    event->rule_id = 0;
    event->reason = 0;
    event->method = 0;
    event->uri = 0;
    event->client_ip = 0;
    event->late_intervention = 0;
    event->response_started = 0;
    event->headers_sent = 0;
    event->body_started = 0;
    event->connection_aborted = 0;
    event->redacted = 0;
    event->truncated = 0;
}

const char *msconnector_event_status_name(const msconnector_event *event) {
    if (event == 0) {
        return msconnector_status_name(MSCONNECTOR_STATUS_ERROR);
    }

    return msconnector_status_name(event->status);
}

int msconnector_event_write_json_ex(
    const msconnector_event *event,
    char *dst,
    size_t dst_size,
    int *truncated) {
    char timestamp[EVENT_TEXT_SIZE];
    char level[32];
    char message_id[EVENT_TEXT_SIZE];
    char message[EVENT_TEXT_SIZE];
    char event_name[EVENT_TEXT_SIZE];
    char connector[EVENT_TEXT_SIZE];
    char transaction_id[EVENT_TEXT_SIZE];
    char action[64];
    char requested_action[64];
    char actual_action[64];
    char http_reason_phrase[EVENT_TEXT_SIZE];
    char http_default_message[EVENT_TEXT_SIZE];
    char rule_id[EVENT_TEXT_SIZE];
    char reason[EVENT_TEXT_SIZE];
    char method[64];
    char uri[EVENT_TEXT_SIZE];
    char client_ip[64];
    int was_truncated;
    int written;

    if (truncated != 0) {
        *truncated = 0;
    }
    if (event == 0 || dst == 0 || dst_size == 0) {
        return 0;
    }

    was_truncated = event->truncated != 0;
    escape_field(event->timestamp, timestamp, sizeof(timestamp), &was_truncated);
    escape_field(event->level, level, sizeof(level), &was_truncated);
    escape_field(event->message_id, message_id, sizeof(message_id), &was_truncated);
    escape_field(event->message, message, sizeof(message), &was_truncated);
    escape_field(event->event, event_name, sizeof(event_name), &was_truncated);
    escape_field(event->connector, connector, sizeof(connector), &was_truncated);
    escape_field(event->transaction_id, transaction_id, sizeof(transaction_id), &was_truncated);
    escape_field(event->action, action, sizeof(action), &was_truncated);
    escape_field(event->requested_action, requested_action, sizeof(requested_action), &was_truncated);
    escape_field(event->actual_action, actual_action, sizeof(actual_action), &was_truncated);
    escape_field(event->http_reason_phrase, http_reason_phrase, sizeof(http_reason_phrase), &was_truncated);
    escape_field(event->http_default_message, http_default_message, sizeof(http_default_message), &was_truncated);
    escape_field(event->rule_id, rule_id, sizeof(rule_id), &was_truncated);
    escape_field(event->reason, reason, sizeof(reason), &was_truncated);
    escape_field(event->method, method, sizeof(method), &was_truncated);
    escape_field(event->uri, uri, sizeof(uri), &was_truncated);
    escape_field(event->client_ip, client_ip, sizeof(client_ip), &was_truncated);

    written = snprintf(
        dst,
        dst_size,
        "{\"timestamp\":\"%s\",\"level\":\"%s\",\"message_id\":\"%s\",\"message\":\"%s\",\"event\":\"%s\",\"connector\":\"%s\",\"transaction_id\":\"%s\",\"phase\":\"%s\",\"status\":\"%s\",\"action\":\"%s\",\"requested_action\":\"%s\",\"actual_action\":\"%s\",\"http_status\":%d,\"original_http_status\":%d,\"visible_http_status\":%d,\"http_reason_phrase\":\"%s\",\"http_default_message\":\"%s\",\"rule_id\":\"%s\",\"reason\":\"%s\",\"method\":\"%s\",\"uri\":\"%s\",\"client_ip\":\"%s\",\"late_intervention\":%s,\"response_started\":%s,\"headers_sent\":%s,\"body_started\":%s,\"connection_aborted\":%s,\"redacted\":%s,\"truncated\":%s}",
        timestamp,
        level,
        message_id,
        message,
        event_name,
        connector,
        transaction_id,
        msconnector_phase_name(event->phase),
        msconnector_status_name(event->status),
        action,
        requested_action,
        actual_action,
        event->http_status,
        event->original_http_status,
        event->visible_http_status,
        http_reason_phrase,
        http_default_message,
        rule_id,
        reason,
        method,
        uri,
        client_ip,
        json_bool(event->late_intervention),
        json_bool(event->response_started),
        json_bool(event->headers_sent),
        json_bool(event->body_started),
        json_bool(event->connection_aborted),
        json_bool(event->redacted),
        json_bool(was_truncated));

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }
    if (truncated != 0) {
        *truncated = was_truncated;
    }
    return !was_truncated;
}

int msconnector_event_write_json(const msconnector_event *event, char *dst, size_t dst_size) {
    int truncated = 0;
    return msconnector_event_write_json_ex(event, dst, dst_size, &truncated);
}

void msconnector_event_set_phase4_hard_abort_after_200(
    msconnector_event *event,
    const char *connector,
    const char *transaction_id,
    const char *rule_id,
    const char *reason) {
    if (event == 0) {
        return;
    }

    msconnector_event_init(event);
    event->level = msconnector_event_default_level(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->message_id = MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200;
    event->message = msconnector_event_default_message(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->event = "phase4_hard_abort_after_200";
    event->connector = connector;
    event->transaction_id = transaction_id;
    event->phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event->status = MSCONNECTOR_STATUS_BLOCKED;
    event->action = "connection_abort";
    event->requested_action = "deny";
    event->actual_action = "connection_abort";
    event->http_status = 200;
    event->original_http_status = 200;
    event->visible_http_status = 200;
    event->http_reason_phrase = msconnector_http_status_reason_phrase(200);
    event->http_default_message = msconnector_http_status_default_message(200);
    event->rule_id = rule_id;
    event->reason = reason;
    event->late_intervention = 1;
    event->response_started = 1;
    event->headers_sent = 1;
    event->body_started = 1;
    event->connection_aborted = 1;
}
