#include "msconnector/rule_merge.h"
static int string_empty(const char *value) { return value == 0 || value[0] == '\0'; }
static int remote_pair_requested(const char *key, const char *url) { return !string_empty(key) || !string_empty(url); }
static int remote_pair_complete(const char *key, const char *url) { return !string_empty(key) && !string_empty(url); }
static int incomplete_remote(const char *key, const char *url) { return remote_pair_requested(key, url) && !remote_pair_complete(key, url); }
void msconnector_rule_collection_init(msconnector_rule_collection *rules) { if (rules != 0) { rules->inline_rules = 0; rules->rules_file = 0; rules->rules_remote_key = 0; rules->rules_remote_url = 0; } }
int msconnector_rule_collection_from_config(msconnector_rule_collection *out, const msconnector_config *config) {
    if (out == 0 || config == 0 || incomplete_remote(config->rules_remote_key, config->rules_remote_url)) { return 0; }
    out->inline_rules = config->rules_inline; out->rules_file = config->rules_file; out->rules_remote_key = config->rules_remote_key; out->rules_remote_url = config->rules_remote_url; return 1;
}
int msconnector_rule_collection_merge(msconnector_rule_collection *out, const msconnector_rule_collection *parent, const msconnector_rule_collection *child) {
    msconnector_rule_collection empty; msconnector_rule_collection_init(&empty);
    if (out == 0) { return 0; }
    if (parent == 0) { parent = &empty; }
    if (child == 0) { child = &empty; }
    out->inline_rules = child->inline_rules != 0 ? child->inline_rules : parent->inline_rules;
    out->rules_file = child->rules_file != 0 ? child->rules_file : parent->rules_file;
    if (remote_pair_requested(child->rules_remote_key, child->rules_remote_url)) { if (incomplete_remote(child->rules_remote_key, child->rules_remote_url)) { return 0; } out->rules_remote_key = child->rules_remote_key; out->rules_remote_url = child->rules_remote_url; }
    else { out->rules_remote_key = parent->rules_remote_key; out->rules_remote_url = parent->rules_remote_url; }
    return !incomplete_remote(out->rules_remote_key, out->rules_remote_url);
}
