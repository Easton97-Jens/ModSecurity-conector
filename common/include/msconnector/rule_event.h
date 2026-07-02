#ifndef MSCONNECTOR_RULE_EVENT_H
#define MSCONNECTOR_RULE_EVENT_H
#include "msconnector/error.h"
#include "msconnector/event.h"
#include "msconnector/rule_load_stats.h"
#ifdef __cplusplus
extern "C" {
#endif
int msconnector_rule_load_event(const msconnector_rule_load_stats *stats, msconnector_event *event, const char *connector, const char *transaction_id);
int msconnector_rule_error_event(const msconnector_error *error, msconnector_event *event, const char *connector, const char *transaction_id);
#ifdef __cplusplus
}
#endif
#endif
