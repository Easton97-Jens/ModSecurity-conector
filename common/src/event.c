#include "msconnector/event.h"
#include "msconnector/json_escape.h"
#include "msconnector/transaction_state.h"
#include <stdio.h>

void msconnector_event_init(msconnector_event *event) {
    if (event == 0) {
        return;
    }

    event->event = 0;
    event->connector = 0;
    event->transaction_id = 0;
    event->phase = MSCONNECTOR_PHASE_CONNECTION;
    event->status = MSCONNECTOR_STATUS_OK;
    event->http_status = 0;
    event->rule_id = 0;
    event->reason = 0;
    event->action = 0;
}

const char *msconnector_event_status_name(const msconnector_event *event) {
    if (event == 0) {
        return msconnector_status_name(MSCONNECTOR_STATUS_ERROR);
    }

    return msconnector_status_name(event->status);
}

int msconnector_event_write_json(const msconnector_event *event, char *dst, size_t dst_size) {
    char event_name[64];
    char connector[64];
    char transaction_id[64];
    char rule_id[64];
    char reason[128];
    char action[64];
    int written;

    if (event == 0 || dst == 0 || dst_size == 0) {
        return 0;
    }

    (void)msconnector_json_escape(event->event, event_name, sizeof(event_name));
    (void)msconnector_json_escape(event->connector, connector, sizeof(connector));
    (void)msconnector_json_escape(event->transaction_id, transaction_id, sizeof(transaction_id));
    (void)msconnector_json_escape(event->rule_id, rule_id, sizeof(rule_id));
    (void)msconnector_json_escape(event->reason, reason, sizeof(reason));
    (void)msconnector_json_escape(event->action, action, sizeof(action));

    written = snprintf(
        dst,
        dst_size,
        "{\"event\":\"%s\",\"connector\":\"%s\",\"transaction_id\":\"%s\",\"phase\":\"%s\",\"status\":\"%s\",\"http_status\":%d,\"rule_id\":\"%s\",\"reason\":\"%s\",\"action\":\"%s\"}",
        event_name,
        connector,
        transaction_id,
        msconnector_phase_name(event->phase),
        msconnector_status_name(event->status),
        event->http_status,
        rule_id,
        reason,
        action);

    return written >= 0 && (size_t)written < dst_size;
}
