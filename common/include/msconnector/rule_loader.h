#ifndef MSCONNECTOR_RULE_LOADER_H
#define MSCONNECTOR_RULE_LOADER_H

#include "msconnector/config.h"
#include "msconnector/error.h"
#include "msconnector/rule_load_stats.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_rule_loader_backend {
    void *userdata;
    int (*add_inline)(void *userdata, void *rules_set, const char *rules, msconnector_error *error);
    int (*add_file)(void *userdata, void *rules_set, const char *path, msconnector_error *error);
    int (*add_remote)(void *userdata, void *rules_set, const char *key, const char *url, msconnector_error *error);
} msconnector_rule_loader_backend;

typedef struct msconnector_rule_loader { void *rules_set; msconnector_rule_loader_backend backend; msconnector_rule_load_stats stats; } msconnector_rule_loader;
void msconnector_rule_loader_init(msconnector_rule_loader *loader, void *rules_set, const msconnector_rule_loader_backend *backend);
int msconnector_rule_loader_add_inline(msconnector_rule_loader *loader, const char *rules, msconnector_error *error);
int msconnector_rule_loader_add_file(msconnector_rule_loader *loader, const char *path, msconnector_error *error);
int msconnector_rule_loader_add_remote(msconnector_rule_loader *loader, const char *key, const char *url, msconnector_error *error);
int msconnector_rule_loader_load_config(msconnector_rule_loader *loader, const msconnector_config *config, msconnector_error *error);
const msconnector_rule_load_stats *msconnector_rule_loader_stats(const msconnector_rule_loader *loader);

#ifdef __cplusplus
}
#endif

#endif
