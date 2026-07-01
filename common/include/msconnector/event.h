#ifndef MSCONNECTOR_EVENT_H
#define MSCONNECTOR_EVENT_H
#include "msconnector/status.h"
#include "msconnector/transaction.h"
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Connector-neutral event model for metadata-only log records; bodies are intentionally absent. */
typedef struct msconnector_event { const char *event; const char *connector; const char *transaction_id; enum msconnector_phase phase; enum msconnector_status status; int http_status; const char *rule_id; const char *reason; const char *action; } msconnector_event;
void msconnector_event_init(msconnector_event *event);
const char *msconnector_event_status_name(const msconnector_event *event);
int msconnector_event_write_json(const msconnector_event *event, char *dst, size_t dst_size);
#ifdef __cplusplus
}
#endif
#endif
