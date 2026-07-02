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


static int format_event_json(
    char *dst,
    size_t dst_size,
    const char *timestamp,
    const char *level,
    const char *message_id,
    const char *message,
    const char *event_name,
    const char *connector,
    const char *transaction_id,
    const char *phase,
    const char *status,
    const char *action,
    const char *requested_action,
    const char *actual_action,
    int http_status,
    int original_http_status,
    int visible_http_status,
    const char *http_reason_phrase,
    const char *http_default_message,
    const char *rule_id,
    const char *reason,
    const char *method,
    const char *uri,
    const char *client_ip,
    const char *late_intervention,
    const char *response_started,
    const char *headers_sent,
    const char *body_started,
    const char *connection_aborted,
    const char *redacted,
    const char *truncated_value) {
    return snprintf(
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
        phase,
        status,
        action,
        requested_action,
        actual_action,
        http_status,
        original_http_status,
        visible_http_status,
        http_reason_phrase,
        http_default_message,
        rule_id,
        reason,
        method,
        uri,
        client_ip,
        late_intervention,
        response_started,
        headers_sent,
        body_started,
        connection_aborted,
        redacted,
        truncated_value);
}

static void escape_field(const char *src, char *dst, size_t dst_size, int *truncated) {
    const size_t needed = msconnector_json_escape(src, dst, dst_size);
    if ((dst_size == 0 || needed >= dst_size) && truncated != 0) {
        *truncated = 1;
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

    event->meta.timestamp = 0;
    event->meta.level = "info";
    event->meta.message_id = 0;
    event->meta.message = 0;
    event->meta.event = 0;
    event->meta.connector = 0;
    event->meta.transaction_id = 0;
    event->decision.phase = MSCONNECTOR_PHASE_CONNECTION;
    event->decision.status = MSCONNECTOR_STATUS_OK;
    event->decision.action = 0;
    event->decision.requested_action = 0;
    event->decision.actual_action = 0;
    event->http.http_status = 0;
    event->http.original_http_status = 0;
    event->http.visible_http_status = 0;
    event->http.http_reason_phrase = 0;
    event->http.http_default_message = 0;
    event->decision.rule_id = 0;
    event->decision.reason = 0;
    event->request.method = 0;
    event->request.uri = 0;
    event->request.client_ip = 0;
    event->flags.late_intervention = 0;
    event->flags.response_started = 0;
    event->flags.headers_sent = 0;
    event->flags.body_started = 0;
    event->flags.connection_aborted = 0;
    event->flags.redacted = 0;
    event->flags.truncated = 0;
}

const char *msconnector_event_status_name(const msconnector_event *event) {
    if (event == 0) {
        return msconnector_status_name(MSCONNECTOR_STATUS_ERROR);
    }

    return msconnector_status_name(event->decision.status);
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
    if (dst != 0 && dst_size > 0) {
        dst[0] = '\0';
    }
    if (event == 0 || dst == 0 || dst_size == 0) {
        return 0;
    }

    was_truncated = event->flags.truncated != 0;
    escape_field(event->meta.timestamp, timestamp, sizeof(timestamp), &was_truncated);
    escape_field(event->meta.level, level, sizeof(level), &was_truncated);
    escape_field(event->meta.message_id, message_id, sizeof(message_id), &was_truncated);
    escape_field(event->meta.message, message, sizeof(message), &was_truncated);
    escape_field(event->meta.event, event_name, sizeof(event_name), &was_truncated);
    escape_field(event->meta.connector, connector, sizeof(connector), &was_truncated);
    escape_field(event->meta.transaction_id, transaction_id, sizeof(transaction_id), &was_truncated);
    escape_field(event->decision.action, action, sizeof(action), &was_truncated);
    escape_field(event->decision.requested_action, requested_action, sizeof(requested_action), &was_truncated);
    escape_field(event->decision.actual_action, actual_action, sizeof(actual_action), &was_truncated);
    escape_field(event->http.http_reason_phrase, http_reason_phrase, sizeof(http_reason_phrase), &was_truncated);
    escape_field(event->http.http_default_message, http_default_message, sizeof(http_default_message), &was_truncated);
    escape_field(event->decision.rule_id, rule_id, sizeof(rule_id), &was_truncated);
    escape_field(event->decision.reason, reason, sizeof(reason), &was_truncated);
    escape_field(event->request.method, method, sizeof(method), &was_truncated);
    escape_field(event->request.uri, uri, sizeof(uri), &was_truncated);
    escape_field(event->request.client_ip, client_ip, sizeof(client_ip), &was_truncated);

    written = format_event_json(
        0,
        0,
        timestamp,
        level,
        message_id,
        message,
        event_name,
        connector,
        transaction_id,
        msconnector_phase_name(event->decision.phase),
        msconnector_status_name(event->decision.status),
        action,
        requested_action,
        actual_action,
        event->http.http_status,
        event->http.original_http_status,
        event->http.visible_http_status,
        http_reason_phrase,
        http_default_message,
        rule_id,
        reason,
        method,
        uri,
        client_ip,
        json_bool(event->flags.late_intervention),
        json_bool(event->flags.response_started),
        json_bool(event->flags.headers_sent),
        json_bool(event->flags.body_started),
        json_bool(event->flags.connection_aborted),
        json_bool(event->flags.redacted),
        json_bool(was_truncated));

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }

    written = format_event_json(
        dst,
        dst_size,
        timestamp,
        level,
        message_id,
        message,
        event_name,
        connector,
        transaction_id,
        msconnector_phase_name(event->decision.phase),
        msconnector_status_name(event->decision.status),
        action,
        requested_action,
        actual_action,
        event->http.http_status,
        event->http.original_http_status,
        event->http.visible_http_status,
        http_reason_phrase,
        http_default_message,
        rule_id,
        reason,
        method,
        uri,
        client_ip,
        json_bool(event->flags.late_intervention),
        json_bool(event->flags.response_started),
        json_bool(event->flags.headers_sent),
        json_bool(event->flags.body_started),
        json_bool(event->flags.connection_aborted),
        json_bool(event->flags.redacted),
        json_bool(was_truncated));

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }
    if (truncated != 0) {
        *truncated = was_truncated;
    }
    return was_truncated ? 0 : 1;
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
    event->meta.level = msconnector_event_default_level(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->meta.message_id = MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200;
    event->meta.message = msconnector_event_default_message(MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200);
    event->meta.event = "phase4_hard_abort_after_200";
    event->meta.connector = connector;
    event->meta.transaction_id = transaction_id;
    event->decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event->decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event->decision.action = "connection_abort";
    event->decision.requested_action = "deny";
    event->decision.actual_action = "connection_abort";
    event->http.http_status = 200;
    event->http.original_http_status = 200;
    event->http.visible_http_status = 200;
    event->http.http_reason_phrase = msconnector_http_status_reason_phrase(200);
    event->http.http_default_message = msconnector_http_status_default_message(200);
    event->decision.rule_id = rule_id;
    event->decision.reason = reason;
    event->flags.late_intervention = 1;
    event->flags.response_started = 1;
    event->flags.headers_sent = 1;
    event->flags.body_started = 1;
    event->flags.connection_aborted = 1;
}
