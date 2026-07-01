#ifndef MSCONNECTOR_EVENT_H
#define MSCONNECTOR_EVENT_H

#include "msconnector/status.h"
#include "msconnector/transaction.h"
#include <stddef.h>

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
 * Connector-neutral event model for metadata-only log records.
 *
 * Pointer fields are borrowed. The caller owns their lifetime. This structure
 * does not own strings and does not include request or response body payloads.
 * Connectors remain responsible for not passing sensitive payloads.
 */
typedef struct msconnector_event {
    const char *timestamp;
    const char *level;
    const char *message_id;
    const char *message;
    const char *event;
    const char *connector;
    const char *transaction_id;
    enum msconnector_phase phase;
    enum msconnector_status status;
    const char *action;
    const char *requested_action;
    const char *actual_action;
    int http_status;
    int original_http_status;
    int visible_http_status;
    const char *http_reason_phrase;
    const char *http_default_message;
    const char *rule_id;
    const char *reason;
    const char *method;
    const char *uri;
    const char *client_ip;
    int late_intervention;
    int response_started;
    int headers_sent;
    int body_started;
    int connection_aborted;
    int redacted;
    int truncated;
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
