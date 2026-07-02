#include "msconnector/rule_loader.h"
#include "msconnector/path_policy.h"
#include <string.h>

static int empty(const char *value) { return value == 0 || value[0] == '\0'; }
static int fail_error(msconnector_error *error, msconnector_error_code code, const char *message) { msconnector_error_set(error, code, message, "rule_loader"); return 0; }
void msconnector_rule_loader_init(msconnector_rule_loader *loader, void *rules_set, const msconnector_rule_loader_backend *backend) {
    if (loader == 0) { return; }
    loader->rules_set = rules_set; msconnector_rule_load_stats_init(&loader->stats);
    if (backend != 0) { loader->backend = *backend; } else { memset(&loader->backend, 0, sizeof(loader->backend)); }
}
int msconnector_rule_loader_add_inline(msconnector_rule_loader *loader, const char *rules, msconnector_error *error) {
    if (loader == 0) { return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "rule loader is required"); }
    if (empty(rules)) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "inline rules are required"); }
    if (loader->backend.add_inline == 0) { return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "inline rule loading is unsupported"); }
    if (!loader->backend.add_inline(loader->backend.userdata, loader->rules_set, rules, error)) { return 0; }
    msconnector_rule_load_stats_add_inline(&loader->stats, 1); return 1;
}
int msconnector_rule_loader_add_file(msconnector_rule_loader *loader, const char *path, msconnector_error *error) {
    if (loader == 0) { return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "rule loader is required"); }
    if (empty(path) || msconnector_path_has_parent_reference(path)) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "valid rule file path is required"); }
    if (loader->backend.add_file == 0) { return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "file rule loading is unsupported"); }
    if (!loader->backend.add_file(loader->backend.userdata, loader->rules_set, path, error)) { return 0; }
    msconnector_rule_load_stats_add_file(&loader->stats, 1); return 1;
}
int msconnector_rule_loader_add_remote(msconnector_rule_loader *loader, const char *key, const char *url, msconnector_error *error) {
    if (loader == 0) { return fail_error(error, MSCONNECTOR_ERROR_INTERNAL, "rule loader is required"); }
    if (empty(key) || empty(url)) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "remote rule key and url are required"); }
    if (loader->backend.add_remote == 0) { return fail_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY, "remote rule loading is unsupported"); }
    if (!loader->backend.add_remote(loader->backend.userdata, loader->rules_set, key, url, error)) { return 0; }
    msconnector_rule_load_stats_add_remote(&loader->stats, 1); return 1;
}
static int remote_pair_requested(const msconnector_config *config) {
    return !empty(config->rules_remote_key) || !empty(config->rules_remote_url);
}

static int remote_pair_complete(const msconnector_config *config) {
    return !empty(config->rules_remote_key) && !empty(config->rules_remote_url);
}

int msconnector_rule_loader_load_config(msconnector_rule_loader *loader, const msconnector_config *config, msconnector_error *error) {
    if (config == 0) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "config is required"); }
    if (remote_pair_requested(config) && !remote_pair_complete(config)) { return fail_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG, "incomplete remote rules pair"); }
    if (config->rules_inline != 0 && !msconnector_rule_loader_add_inline(loader, config->rules_inline, error)) { return 0; }
    if (config->rules_file != 0 && !msconnector_rule_loader_add_file(loader, config->rules_file, error)) { return 0; }
    if (remote_pair_complete(config) && !msconnector_rule_loader_add_remote(loader, config->rules_remote_key, config->rules_remote_url, error)) { return 0; }
    return 1;
}
const msconnector_rule_load_stats *msconnector_rule_loader_stats(const msconnector_rule_loader *loader) { return loader == 0 ? 0 : &loader->stats; }
