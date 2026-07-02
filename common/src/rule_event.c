#include "msconnector/rule_event.h"
#include <stdio.h>
static char rule_event_reason[128];
int msconnector_rule_load_event(const msconnector_rule_load_stats *stats, msconnector_event *event, const char *connector, const char *transaction_id) {
    if (stats == 0 || event == 0) { return 0; }
    msconnector_event_init(event); event->meta.level = "info"; event->meta.message_id = "MSCONN_EVENT_RULE_LOAD"; event->meta.message = "Rules loaded by common rule loader."; event->meta.event = "rule_load"; event->meta.connector = connector; event->meta.transaction_id = transaction_id; event->decision.status = MSCONNECTOR_STATUS_OK;
    (void)snprintf(rule_event_reason, sizeof(rule_event_reason), "inline=%u file=%u remote=%u", stats->inline_rules, stats->file_rules, stats->remote_rules); event->decision.reason = rule_event_reason; return 1;
}
int msconnector_rule_error_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id) {
    if (error == 0 || event == 0) { return 0; }
    return msconnector_error_to_event(error, event, connector, transaction_id);
}
