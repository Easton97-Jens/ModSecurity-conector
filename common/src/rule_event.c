#include "msconnector/rule_event.h"
#include <stdio.h>

int msconnector_rule_load_event_ex(
    const msconnector_rule_load_stats *stats,
    msconnector_event *event,
    const char *connector,
    const char *transaction_id,
    char *reason_buffer,
    size_t reason_buffer_size) {
    int written;
    if (stats == 0 || event == 0 || reason_buffer == 0 || reason_buffer_size == 0U) { return 0; }
    written = snprintf(reason_buffer, reason_buffer_size, "inline=%u file=%u remote=%u", stats->inline_rules, stats->file_rules, stats->remote_rules);
    if (written < 0 || (size_t)written >= reason_buffer_size) { reason_buffer[0] = '\0'; return 0; }
    msconnector_event_init(event);
    event->meta.level = "info";
    event->meta.message_id = "MSCONN_EVENT_RULE_LOAD";
    event->meta.message = "Rules loaded by common rule loader.";
    event->meta.event = "rule_load";
    event->meta.connector = connector;
    event->meta.transaction_id = transaction_id;
    event->decision.status = MSCONNECTOR_STATUS_OK;
    event->decision.reason = reason_buffer;
    return 1;
}

int msconnector_rule_load_event(const msconnector_rule_load_stats *stats, const msconnector_event *event, const char *connector, const char *transaction_id) {
    (void)stats;
    (void)event;
    (void)connector;
    (void)transaction_id;
    return 0;
}

int msconnector_rule_error_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id) {
    if (error == 0 || event == 0) { return 0; }
    return msconnector_error_to_event(error, event, connector, transaction_id);
}
