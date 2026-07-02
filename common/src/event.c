#include "msconnector/event.h"
#include "msconnector/http_status.h"
#include "msconnector/json_escape.h"
#include "msconnector/transaction_state.h"
#include <inttypes.h>
#include <stdio.h>
#include <string.h>

#define EVENT_TEXT_SIZE 256U
#define EVENT_JSON_TRUE "true"
#define EVENT_JSON_FALSE "false"

static const char *json_bool(int value) {
    return value ? EVENT_JSON_TRUE : EVENT_JSON_FALSE;
}


enum msconnector_event_json_text_index {
    EVENT_JSON_TIMESTAMP = 0,
    EVENT_JSON_LEVEL,
    EVENT_JSON_MESSAGE_ID,
    EVENT_JSON_MESSAGE,
    EVENT_JSON_EVENT_NAME,
    EVENT_JSON_CONNECTOR,
    EVENT_JSON_TRANSACTION_ID,
    EVENT_JSON_PHASE,
    EVENT_JSON_STATUS,
    EVENT_JSON_ACTION,
    EVENT_JSON_REQUESTED_ACTION,
    EVENT_JSON_ACTUAL_ACTION,
    EVENT_JSON_HTTP_REASON_PHRASE,
    EVENT_JSON_HTTP_DEFAULT_MESSAGE,
    EVENT_JSON_RULE_ID,
    EVENT_JSON_REASON,
    EVENT_JSON_METHOD,
    EVENT_JSON_URI,
    EVENT_JSON_CLIENT_IP,
    EVENT_JSON_TEXT_COUNT
};

enum msconnector_event_json_status_index {
    EVENT_JSON_HTTP_STATUS = 0,
    EVENT_JSON_ORIGINAL_HTTP_STATUS,
    EVENT_JSON_VISIBLE_HTTP_STATUS,
    EVENT_JSON_STATUS_COUNT
};

enum msconnector_event_json_flag_index {
    EVENT_JSON_LATE_INTERVENTION = 0,
    EVENT_JSON_RESPONSE_STARTED,
    EVENT_JSON_HEADERS_SENT,
    EVENT_JSON_BODY_STARTED,
    EVENT_JSON_CONNECTION_ABORTED,
    EVENT_JSON_REDACTED,
    EVENT_JSON_TRUNCATED,
    EVENT_JSON_FLAG_COUNT
};

typedef struct msconnector_event_json_parts {
    const char *text[EVENT_JSON_TEXT_COUNT];
    int statuses[EVENT_JSON_STATUS_COUNT];
    const char *flags[EVENT_JSON_FLAG_COUNT];
    unsigned long sequence;
    uint64_t previous_hash;
    uint64_t event_hash;
} msconnector_event_json_parts;

static int format_event_json(
    char *dst,
    size_t dst_size,
    const msconnector_event_json_parts *parts) {
    return snprintf(
        dst,
        dst_size,
        "{\"timestamp\":\"%s\",\"level\":\"%s\",\"message_id\":\"%s\",\"message\":\"%s\",\"event\":\"%s\",\"connector\":\"%s\",\"transaction_id\":\"%s\",\"phase\":\"%s\",\"status\":\"%s\",\"action\":\"%s\",\"requested_action\":\"%s\",\"actual_action\":\"%s\",\"http_status\":%d,\"original_http_status\":%d,\"visible_http_status\":%d,\"http_reason_phrase\":\"%s\",\"http_default_message\":\"%s\",\"rule_id\":\"%s\",\"reason\":\"%s\",\"method\":\"%s\",\"uri\":\"%s\",\"client_ip\":\"%s\",\"late_intervention\":%s,\"response_started\":%s,\"headers_sent\":%s,\"body_started\":%s,\"connection_aborted\":%s,\"redacted\":%s,\"truncated\":%s,\"sequence\":%lu,\"previous_event_hash\":%" PRIu64 ",\"event_hash\":%" PRIu64 "}",
        parts->text[EVENT_JSON_TIMESTAMP],
        parts->text[EVENT_JSON_LEVEL],
        parts->text[EVENT_JSON_MESSAGE_ID],
        parts->text[EVENT_JSON_MESSAGE],
        parts->text[EVENT_JSON_EVENT_NAME],
        parts->text[EVENT_JSON_CONNECTOR],
        parts->text[EVENT_JSON_TRANSACTION_ID],
        parts->text[EVENT_JSON_PHASE],
        parts->text[EVENT_JSON_STATUS],
        parts->text[EVENT_JSON_ACTION],
        parts->text[EVENT_JSON_REQUESTED_ACTION],
        parts->text[EVENT_JSON_ACTUAL_ACTION],
        parts->statuses[EVENT_JSON_HTTP_STATUS],
        parts->statuses[EVENT_JSON_ORIGINAL_HTTP_STATUS],
        parts->statuses[EVENT_JSON_VISIBLE_HTTP_STATUS],
        parts->text[EVENT_JSON_HTTP_REASON_PHRASE],
        parts->text[EVENT_JSON_HTTP_DEFAULT_MESSAGE],
        parts->text[EVENT_JSON_RULE_ID],
        parts->text[EVENT_JSON_REASON],
        parts->text[EVENT_JSON_METHOD],
        parts->text[EVENT_JSON_URI],
        parts->text[EVENT_JSON_CLIENT_IP],
        parts->flags[EVENT_JSON_LATE_INTERVENTION],
        parts->flags[EVENT_JSON_RESPONSE_STARTED],
        parts->flags[EVENT_JSON_HEADERS_SENT],
        parts->flags[EVENT_JSON_BODY_STARTED],
        parts->flags[EVENT_JSON_CONNECTION_ABORTED],
        parts->flags[EVENT_JSON_REDACTED],
        parts->flags[EVENT_JSON_TRUNCATED],
        parts->sequence,
        parts->previous_hash,
        parts->event_hash);
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
    event->integrity.sequence = 0UL;
    event->integrity.previous_hash = 0U;
    event->integrity.event_hash = 0U;
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
    msconnector_event_json_parts parts;
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

    parts.text[EVENT_JSON_TIMESTAMP] = timestamp;
    parts.text[EVENT_JSON_LEVEL] = level;
    parts.text[EVENT_JSON_MESSAGE_ID] = message_id;
    parts.text[EVENT_JSON_MESSAGE] = message;
    parts.text[EVENT_JSON_EVENT_NAME] = event_name;
    parts.text[EVENT_JSON_CONNECTOR] = connector;
    parts.text[EVENT_JSON_TRANSACTION_ID] = transaction_id;
    parts.text[EVENT_JSON_PHASE] = msconnector_phase_name(event->decision.phase);
    parts.text[EVENT_JSON_STATUS] = msconnector_status_name(event->decision.status);
    parts.text[EVENT_JSON_ACTION] = action;
    parts.text[EVENT_JSON_REQUESTED_ACTION] = requested_action;
    parts.text[EVENT_JSON_ACTUAL_ACTION] = actual_action;
    parts.statuses[EVENT_JSON_HTTP_STATUS] = event->http.http_status;
    parts.statuses[EVENT_JSON_ORIGINAL_HTTP_STATUS] = event->http.original_http_status;
    parts.statuses[EVENT_JSON_VISIBLE_HTTP_STATUS] = event->http.visible_http_status;
    parts.text[EVENT_JSON_HTTP_REASON_PHRASE] = http_reason_phrase;
    parts.text[EVENT_JSON_HTTP_DEFAULT_MESSAGE] = http_default_message;
    parts.text[EVENT_JSON_RULE_ID] = rule_id;
    parts.text[EVENT_JSON_REASON] = reason;
    parts.text[EVENT_JSON_METHOD] = method;
    parts.text[EVENT_JSON_URI] = uri;
    parts.text[EVENT_JSON_CLIENT_IP] = client_ip;
    parts.flags[EVENT_JSON_LATE_INTERVENTION] = json_bool(event->flags.late_intervention);
    parts.flags[EVENT_JSON_RESPONSE_STARTED] = json_bool(event->flags.response_started);
    parts.flags[EVENT_JSON_HEADERS_SENT] = json_bool(event->flags.headers_sent);
    parts.flags[EVENT_JSON_BODY_STARTED] = json_bool(event->flags.body_started);
    parts.flags[EVENT_JSON_CONNECTION_ABORTED] = json_bool(event->flags.connection_aborted);
    parts.flags[EVENT_JSON_REDACTED] = json_bool(event->flags.redacted);
    parts.flags[EVENT_JSON_TRUNCATED] = json_bool(was_truncated);
    parts.sequence = event->integrity.sequence;
    parts.previous_hash = event->integrity.previous_hash;
    parts.event_hash = event->integrity.event_hash;

    written = format_event_json(0, 0, &parts);

    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }

    parts.flags[EVENT_JSON_TRUNCATED] = json_bool(was_truncated);
    written = format_event_json(dst, dst_size, &parts);

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
