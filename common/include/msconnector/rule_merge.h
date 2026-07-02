#ifndef MSCONNECTOR_RULE_MERGE_H
#define MSCONNECTOR_RULE_MERGE_H
#include "msconnector/config.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct msconnector_rule_collection { const char *inline_rules; const char *rules_file; const char *rules_remote_key; const char *rules_remote_url; } msconnector_rule_collection;
void msconnector_rule_collection_init(msconnector_rule_collection *rules);
int msconnector_rule_collection_from_config(msconnector_rule_collection *out, const msconnector_config *config);
int msconnector_rule_collection_merge(msconnector_rule_collection *out, const msconnector_rule_collection *parent, const msconnector_rule_collection *child);
#ifdef __cplusplus
}
#endif
#endif
