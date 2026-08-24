#include "haproxy_modsecurity_binding.h"
#include "haproxy_modsecurity_mapper.h"

#include <dirent.h>
#include <errno.h>
#include <stdint.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include <modsecurity/modsecurity.h>
#include <modsecurity/rules_set.h>
#include <modsecurity/transaction.h>

#include "msconnector/config_parser.h"
#include "msconnector/decision.h"
#include "msconnector/directive_adapter.h"
#include "msconnector/directive_spec.h"
#include "msconnector/directives.h"
#include "msconnector/dos_guard.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/flow_guard.h"
#include "msconnector/headers.h"
#include "msconnector/integrity_event.h"
#include "msconnector/json_escape.h"
#include "msconnector/late_intervention.h"
#include "msconnector/log_sanitize.h"
#include "msconnector/redaction.h"
#include "msconnector/resource_limits.h"
#include "msconnector/rule_id.h"
#include "msconnector/rule_loader.h"
#include "msconnector/rule_load_stats.h"
#include "msconnector/status.h"

#define HAPROXY_MODSECURITY_EXPECTED_STATUS 403
#define HAPROXY_PATH_LIMIT 4096U

static int bounded_cstring_length(const char *value, size_t max_len, size_t *out_len) {
    const char *end = 0;

    if (value == 0 || out_len == 0 || max_len == 0) {
        return -1;
    }
    end = (const char *)memchr(value, '\0', max_len);
    if (end == 0) {
        return -1;
    }
    *out_len = (size_t)(end - value);
    return 0;
}

static void copy_message(char *dst, size_t dst_len, const char *src) {
    if (dst == 0 || dst_len == 0) {
        return;
    }
    if (src == 0) {
        dst[0] = '\0';
        return;
    }
    snprintf(dst, dst_len, "%s", src);
}

static void init_decision(haproxy_modsecurity_decision *decision, int phase) {
    msconnector_decision common_decision;
    msconnector_decision_init(&common_decision);
    if (decision == 0) {
        return;
    }
    memset(decision, 0, sizeof(*decision));
    decision->status = 200;
    decision->phase = phase;
    copy_message(decision->action, sizeof(decision->action), "pass");
}

static void init_intervention(ModSecurityIntervention *intervention) {
    intervention->status = 200;
    intervention->pause = 0;
    intervention->url = 0;
    intervention->log = 0;
    intervention->disruptive = 0;
}

struct haproxy_modsecurity_engine {
    msconnector_config common_config;
    ModSecurity *modsec;
    RulesSet *rules;
};

struct haproxy_modsecurity_transaction {
    haproxy_modsecurity_engine *engine;
    Transaction *transaction;
    int logging_done;
    int request_headers_processed;
    int request_body_processed;
    int request_body_started;
    size_t request_body_bytes_seen;
    size_t request_body_bytes_inspected;
    int response_headers_processed;
    int response_body_processed;
    int response_body_started;
    size_t response_body_bytes_seen;
    size_t response_body_bytes_inspected;
    char request_id[128];
};

typedef int (*haproxy_modsecurity_body_append)(
    Transaction *transaction,
    const unsigned char *body,
    size_t body_len);

typedef int (*haproxy_modsecurity_body_finish)(Transaction *transaction);

typedef struct haproxy_modsecurity_body_phase {
    int phase;
    int *headers_processed;
    int *body_processed;
    int *body_started;
    size_t *body_bytes_seen;
    size_t *body_bytes_inspected;
    const char *missing_message;
    const char *headers_required_message;
    const char *append_after_eos_message;
    const char *pointer_required_message;
    const char *append_failed_message;
    const char *finish_once_message;
    const char *finish_failed_message;
    haproxy_modsecurity_body_append append_body;
    haproxy_modsecurity_body_finish finish_body;
} haproxy_modsecurity_body_phase;

static int haproxy_common_sdk_probe_semantics(void) {
    enum msconnector_bool_option bool_value;
    enum msconnector_phase4_mode phase4_value;
    size_t size_value;
    int status_value;
    char adapter_error[128];

    if (msconnector_parse_bool("on", &bool_value) != 1 ||
            msconnector_parse_phase4_mode("safe", &phase4_value) != 1 ||
            msconnector_parse_size("1048576", &size_value) != 1 ||
            msconnector_parse_http_status("403", &status_value) != 1) {
        return -1;
    }
    if (msconnector_directive_spec_find(MSCONNECTOR_DIRECTIVE_RULES_FILE) == 0 ||
            msconnector_directive_adapter_validate_all(adapter_error, sizeof(adapter_error)) != 1) {
        return -1;
    }
    return bool_value == MSCONNECTOR_BOOL_UNSET || phase4_value == MSCONNECTOR_PHASE4_MODE_UNSET ||
        size_value == 0U || status_value == 0 ? -1 : 0;
}

static int file_exists(const char *path) {
    struct stat st;
    return path != 0 && path[0] != '\0' && stat(path, &st) == 0 && S_ISREG(st.st_mode);
}

static int dir_exists(const char *path) {
    struct stat st;
    return path != 0 && path[0] != '\0' && stat(path, &st) == 0 && S_ISDIR(st.st_mode);
}

static int has_conf_suffix(const char *name) {
    size_t len;

    if (name == 0) {
        return 0;
    }
    if (bounded_cstring_length(name, HAPROXY_PATH_LIMIT, &len) != 0) {
        return 0;
    }
    return len > 5U && strcmp(name + len - 5U, ".conf") == 0;
}

static int compare_strings(const void *left, const void *right) {
    const char *const *a = (const char *const *)left;
    const char *const *b = (const char *const *)right;
    return strcmp(*a, *b);
}

static void free_string_list(char **items, size_t count) {
    if (items == 0) {
        return;
    }
    for (size_t i = 0; i < count; ++i) {
        free(items[i]);
    }
    free(items);
}

static char *join_path(const char *dir, const char *name) {
    size_t dir_len;
    size_t name_len;
    char *path;

    if (dir == 0 || name == 0) {
        return 0;
    }
    if (bounded_cstring_length(dir, HAPROXY_PATH_LIMIT, &dir_len) != 0 ||
            bounded_cstring_length(name, HAPROXY_PATH_LIMIT, &name_len) != 0 ||
            dir_len > SIZE_MAX - name_len - 2U) {
        return 0;
    }
    path = (char *)calloc(dir_len + name_len + 2U, 1U);
    if (path == 0) {
        return 0;
    }
    memcpy(path, dir, dir_len);
    if (dir_len > 0 && dir[dir_len - 1U] != '/') {
        path[dir_len++] = '/';
    }
    memcpy(path + dir_len, name, name_len + 1U);
    return path;
}

static void capture_intervention(
        Transaction *transaction,
        int phase,
        haproxy_modsecurity_decision *decision) {
    ModSecurityIntervention intervention;
    char common_rule_id[64];
    int rule_id_result;
    int truncated = 0;
#if defined(HAPROXY_HAVE_MSC_GET_RULES_MESSAGES_RULE_IDS)
    int64_t ids[1];
    size_t id_count;
#endif

    init_decision(decision, phase);
    common_rule_id[0] = '\0';
    init_intervention(&intervention);
    if (msc_intervention(transaction, &intervention) != 0) {
        decision->disruptive = intervention.disruptive;
        decision->status = intervention.status > 0 ?
            intervention.status : HAPROXY_MODSECURITY_EXPECTED_STATUS;
        if (intervention.url != 0 && intervention.url[0] != '\0') {
            copy_message(decision->action, sizeof(decision->action), "redirect");
            copy_message(decision->redirect_url, sizeof(decision->redirect_url),
                intervention.url);
        } else {
            copy_message(decision->action, sizeof(decision->action), "deny");
        }
        copy_message(decision->log_message, sizeof(decision->log_message),
            intervention.log);
        msconnector_sanitize_log_message(intervention.log, intervention.log != 0 ? strlen(intervention.log) : 0U,
            decision->log_message, sizeof(decision->log_message), &truncated);
        rule_id_result = msconnector_rule_id_extract_from_message(intervention.log, common_rule_id,
            sizeof(common_rule_id));
        if (rule_id_result > 0) {
            char *end = 0;
            long parsed = strtol(common_rule_id, &end, 10);
            if (end != common_rule_id && end != 0 && *end == '\0' &&
                    parsed >= 0L && parsed <= (long)INT_MAX) {
                decision->rule_id = (int)parsed;
            }
        }
    }
#if defined(HAPROXY_HAVE_MSC_GET_RULES_MESSAGES_RULE_IDS)
    id_count = msc_get_rules_messages_rule_ids(transaction, ids, 1U);
    if (id_count > 0U && ids[0] > 0 && ids[0] <= (int64_t)INT_MAX) {
        decision->rule_id = (int)ids[0];
    }
#endif
    msc_intervention_cleanup(&intervention);
}

static int append_body_chunk(
        haproxy_modsecurity_transaction *transaction,
        const unsigned char *body,
        unsigned int body_len,
        haproxy_modsecurity_decision *decision,
        const haproxy_modsecurity_body_phase *phase) {
    init_decision(decision, phase->phase);
    if (transaction == 0 || transaction->transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->missing_message);
        return 1;
    }
    if (!*phase->headers_processed) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->headers_required_message);
        return 1;
    }
    if (*phase->body_processed) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->append_after_eos_message);
        return 1;
    }
    if (body_len > 0U && body == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->pointer_required_message);
        return 1;
    }
    *phase->body_bytes_seen += body_len;
    if (body_len > 0U && phase->append_body(transaction->transaction, body, (size_t)body_len) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->append_failed_message);
        return 1;
    }
    *phase->body_started = 1;
    *phase->body_bytes_inspected += body_len;
    return 0;
}

static int finish_body(
        haproxy_modsecurity_transaction *transaction,
        haproxy_modsecurity_decision *decision,
        const haproxy_modsecurity_body_phase *phase) {
    init_decision(decision, phase->phase);
    if (transaction == 0 || transaction->transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->missing_message);
        return 1;
    }
    if (!*phase->headers_processed) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->headers_required_message);
        return 1;
    }
    if (*phase->body_processed) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->finish_once_message);
        return 1;
    }
    if (phase->finish_body(transaction->transaction) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message), phase->finish_failed_message);
        return 1;
    }
    *phase->body_processed = 1;
    capture_intervention(transaction->transaction, phase->phase, decision);
    return 0;
}

static int load_rules_file(
        RulesSet *rules,
        const char *rules_file,
        haproxy_modsecurity_decision *decision) {
    const char *rules_error = 0;
    int rc;

    if (rules_file != 0 && rules_file[0] != '\0') {
        msconnector_rule_load_stats common_stats;
        msconnector_rule_load_stats_init(&common_stats);
        msconnector_rule_load_stats_add_file(&common_stats, 1U);
        (void)common_stats;
        rc = msc_rules_add_file(rules, rules_file, &rules_error);
        if (rc < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                rules_error != 0 ? rules_error : "failed to load rules file");
            if (rules_error != 0) {
                msc_rules_error_cleanup(rules_error);
            }
            return -1;
        }
    }
    return 0;
}

static int load_rules_text(
        RulesSet *rules,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    const char *rules_error = 0;
    int rc;

    rules_error = 0;
    if (rules_text != 0 && rules_text[0] != '\0') {
        rc = msc_rules_add(rules, rules_text, &rules_error);
        if (rc < 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                rules_error != 0 ? rules_error : "failed to load rules text");
            if (rules_error != 0) {
                msc_rules_error_cleanup(rules_error);
            }
            return -1;
        }
    }
    return 0;
}

static int load_rules_dir(
        RulesSet *rules,
        const char *rules_dir,
        haproxy_modsecurity_decision *decision) {
    DIR *dir;
    struct dirent *entry;
    char **paths = 0;
    size_t count = 0;
    size_t i;

    if (!dir_exists(rules_dir)) {
        return 0;
    }
    dir = opendir(rules_dir);
    if (dir == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            strerror(errno));
        return -1;
    }
    while ((entry = readdir(dir)) != 0) {
        char **next;
        char *path;
        if (entry->d_name[0] == '.' || !has_conf_suffix(entry->d_name)) {
            continue;
        }
        path = join_path(rules_dir, entry->d_name);
        if (path == 0) {
            closedir(dir);
            free_string_list(paths, count);
            copy_message(decision->log_message, sizeof(decision->log_message),
                "failed to allocate rules directory path");
            return -1;
        }
        next = (char **)realloc(paths, sizeof(*paths) * (count + 1U));
        if (next == 0) {
            free(path);
            closedir(dir);
            free_string_list(paths, count);
            copy_message(decision->log_message, sizeof(decision->log_message),
                "failed to allocate rules directory list");
            return -1;
        }
        paths = next;
        paths[count++] = path;
    }
    closedir(dir);
    qsort(paths, count, sizeof(*paths), compare_strings);
    for (i = 0; i < count; ++i) {
        if (load_rules_file(rules, paths[i], decision) != 0) {
            free_string_list(paths, count);
            return -1;
        }
    }
    free_string_list(paths, count);
    return 0;
}

static int load_crs_rules(
        RulesSet *rules,
        const char *crs_root,
        haproxy_modsecurity_decision *decision,
        int *loaded) {
    char *crs_setup;
    char *crs_setup_example;
    char *crs_rules;
    const char *setup_file = 0;
    int rc = 0;

    if (!dir_exists(crs_root)) {
        return 0;
    }
    crs_setup = join_path(crs_root, "crs-setup.conf");
    crs_setup_example = join_path(crs_root, "crs-setup.conf.example");
    crs_rules = join_path(crs_root, "rules");
    if (crs_setup != 0 && file_exists(crs_setup)) {
        setup_file = crs_setup;
    } else if (crs_setup_example != 0 && file_exists(crs_setup_example)) {
        setup_file = crs_setup_example;
    }
    if (setup_file != 0 && load_rules_file(rules, setup_file, decision) != 0) {
        rc = -1;
    } else if (setup_file != 0) {
        *loaded = 1;
    }
    if (rc == 0 && crs_rules != 0 && load_rules_dir(rules, crs_rules, decision) != 0) {
        rc = -1;
    }
    if (rc == 0 && crs_rules != 0 && dir_exists(crs_rules)) {
        *loaded = 1;
    }
    free(crs_setup);
    free(crs_setup_example);
    free(crs_rules);
    return rc;
}

static int load_configured_rules(
        RulesSet *rules,
        const haproxy_modsecurity_engine_config *config,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    int loaded = 0;

    if (config != 0 && file_exists(config->modsecurity_conf)) {
        if (load_rules_file(rules, config->modsecurity_conf, decision) != 0) {
            return -1;
        }
        loaded = 1;
    }
    if (config != 0 && load_crs_rules(rules, config->crs_root, decision, &loaded) != 0) {
        return -1;
    }
    if (config != 0 && dir_exists(config->rules_dir)) {
        if (load_rules_dir(rules, config->rules_dir, decision) != 0) {
            return -1;
        }
        loaded = 1;
    }
    if (config != 0 && config->rules_file != 0 && config->rules_file[0] != '\0') {
        if (load_rules_file(rules, config->rules_file, decision) != 0) {
            return -1;
        }
        loaded = 1;
    }
    if (rules_text != 0 && rules_text[0] != '\0') {
        if (load_rules_text(rules, rules_text, decision) != 0) {
            return -1;
        }
        loaded = 1;
    }
    if (!loaded) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "no ModSecurity rules or configuration loaded");
        return -1;
    }
    return 0;
}

static const char *request_text_or_default(const char *value, const char *fallback) {
    return value != 0 && value[0] != '\0' ? value : fallback;
}

static int load_request_rules(
        RulesSet *rules,
        const haproxy_modsecurity_request *request,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    haproxy_modsecurity_engine_config config;

    memset(&config, 0, sizeof(config));
    config.rules_file = request->rules_file;
    return load_configured_rules(rules, &config, rules_text, decision);
}

static Transaction *create_request_transaction(
        ModSecurity *modsec,
        RulesSet *rules,
        const haproxy_modsecurity_request *request) {
    if (request->request_id != 0 && request->request_id[0] != '\0') {
        return msc_new_transaction_with_id(modsec, rules, request->request_id, 0);
    }
    return msc_new_transaction(modsec, rules, 0);
}

static int process_request_connection(
        Transaction *transaction,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    const char *client_ip = request_text_or_default(request->client_ip, "127.0.0.1");
    const char *server_ip = request_text_or_default(request->server_ip, "127.0.0.1");
    int client_port = request->client_port > 0 ? request->client_port : 49152;
    int server_port = request->server_port > 0 ? request->server_port : 80;

    if (msc_process_connection(transaction, client_ip, client_port, server_ip, server_port) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_connection failed");
        return -1;
    }
    return 0;
}

static int process_request_headers(
        Transaction *transaction,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    unsigned int i;

    for (i = 0; i < request->header_count; ++i) {
        const char *name = request->headers[i].name;
        const char *value = request->headers[i].value;

        if (name == 0 || name[0] == '\0') {
            continue;
        }
        if (value == 0) {
            value = "";
        }
        if (msc_add_request_header(transaction, (const unsigned char *)name,
                (const unsigned char *)value) != 1) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                "msc_add_request_header failed");
            return -1;
        }
    }
    if (msc_process_request_headers(transaction) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_headers failed");
        return -1;
    }
    return 0;
}

static int process_request_body(
        Transaction *transaction,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    if (request->body != 0 && request->body_len > 0 &&
            msc_append_request_body(transaction, request->body,
                (size_t)request->body_len) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_append_request_body failed");
        return -1;
    }
    if (msc_process_request_body(transaction) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_request_body failed");
        return -1;
    }
    return 0;
}

static int eval_request_internal(
        const haproxy_modsecurity_request *request,
        const char *rules_text,
        haproxy_modsecurity_decision *decision) {
    ModSecurity *modsec = 0;
    RulesSet *rules = 0;
    Transaction *transaction = 0;
    int rc = 1;
    const char *safe_method;
    const char *safe_uri;

    if (decision == 0 || request == 0) {
        return 1;
    }
    init_decision(decision, 0);
    safe_method = request_text_or_default(request->method, "GET");
    safe_uri = request_text_or_default(request->uri, "/");

    modsec = msc_init();
    if (modsec == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_init returned null");
        goto cleanup;
    }
    msc_set_connector_info(modsec,
        "HAProxy SPOA live YAML runtime binding");

    rules = msc_create_rules_set();
    if (rules == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_create_rules_set returned null");
        goto cleanup;
    }
    if (load_request_rules(rules, request, rules_text, decision) != 0) {
        goto cleanup;
    }
    transaction = create_request_transaction(modsec, rules, request);
    if (transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_new_transaction returned null");
        goto cleanup;
    }
    if (process_request_connection(transaction, request, decision) != 0) {
        goto cleanup;
    }
    if (msc_process_uri(transaction, safe_uri, safe_method, "1.1") != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_uri failed");
        goto cleanup;
    }
    if (process_request_headers(transaction, request, decision) != 0) {
        goto cleanup;
    }
    capture_intervention(transaction, 1, decision);
    if (decision->disruptive != 0) {
        msc_process_logging(transaction);
        rc = 0;
        goto cleanup;
    }

    if (process_request_body(transaction, request, decision) != 0) {
        goto cleanup;
    }
    capture_intervention(transaction, 2, decision);
    msc_process_logging(transaction);
    rc = 0;

cleanup:
    if (transaction != 0) {
        msc_transaction_cleanup(transaction);
    }
    if (rules != 0) {
        msc_rules_cleanup(rules);
    }
    if (modsec != 0) {
        msc_cleanup(modsec);
    }
    return rc;
}

int haproxy_modsecurity_engine_create(
        const haproxy_modsecurity_engine_config *config,
        haproxy_modsecurity_engine **engine,
        haproxy_modsecurity_decision *decision) {
    haproxy_modsecurity_engine *created;

    if (engine == 0) {
        return 1;
    }
    *engine = 0;
    init_decision(decision, 0);
    created = (haproxy_modsecurity_engine *)calloc(1U, sizeof(*created));
    if (created == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "failed to allocate ModSecurity engine");
        return 1;
    }
    if (haproxy_common_sdk_probe_semantics() != 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "Common SDK directive/parser semantics unavailable");
        free(created);
        return 1;
    }
    msconnector_config_init(&created->common_config);
    msconnector_config_apply_defaults(&created->common_config);
    if (config != 0) {
        char config_error[256];
        config_error[0] = '\0';
        if (msconnector_config_merge(&created->common_config, &created->common_config,
                &config->common_config) != 1 ||
                msconnector_config_validate(&created->common_config, config_error,
                    sizeof(config_error)) != 1) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                config_error[0] != '\0' ? config_error : "Common config validation failed");
            haproxy_modsecurity_engine_destroy(created);
            return 1;
        }
    }
    created->modsec = msc_init();
    if (created->modsec == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_init returned null");
        haproxy_modsecurity_engine_destroy(created);
        return 1;
    }
    msc_set_connector_info(created->modsec,
        config != 0 && config->connector_info != 0 && config->connector_info[0] != '\0' ?
            config->connector_info : "HAProxy ModSecurity SPOA production agent");
    created->rules = msc_create_rules_set();
    if (created->rules == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_create_rules_set returned null");
        haproxy_modsecurity_engine_destroy(created);
        return 1;
    }
    if (load_configured_rules(created->rules, config, 0, decision) != 0) {
        haproxy_modsecurity_engine_destroy(created);
        return 1;
    }
    *engine = created;
    return 0;
}

void haproxy_modsecurity_engine_destroy(haproxy_modsecurity_engine *engine) {
    if (engine == 0) {
        return;
    }
    if (engine->rules != 0) {
        msc_rules_cleanup(engine->rules);
    }
    if (engine->modsec != 0) {
        msc_cleanup(engine->modsec);
    }
    free(engine);
}

static void transaction_cleanup(haproxy_modsecurity_transaction *transaction, int process_logging) {
    if (transaction == 0) {
        return;
    }
    if (transaction->transaction != 0) {
        if (process_logging && !transaction->logging_done) {
            msc_process_logging(transaction->transaction);
            transaction->logging_done = 1;
        }
        msc_transaction_cleanup(transaction->transaction);
    }
    free(transaction);
}

static void validate_common_mapped_request(
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    haproxy_modsecurity_mapped_request mapped_request;
    msconnector_request_mapper_contract contract;
    char mapper_error[256];

    mapper_error[0] = '\0';
    msconnector_request_mapper_contract_init(&contract);
    if (haproxy_modsecurity_map_owned_request(request, &contract, &mapped_request,
            mapper_error, sizeof(mapper_error)) != 1 &&
            decision->log_message[0] == '\0') {
        copy_message(decision->log_message, sizeof(decision->log_message),
            mapper_error[0] != '\0' ? mapper_error :
            "common request mapper validation skipped");
    }
    haproxy_modsecurity_mapped_request_cleanup(&mapped_request);
}

static int begin_transaction_protocol(
        haproxy_modsecurity_transaction *transaction,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    const char *safe_method = request_text_or_default(request->method, "GET");
    const char *safe_uri = request_text_or_default(request->uri, "/");

    if (process_request_connection(transaction->transaction, request, decision) != 0) {
        return -1;
    }
    if (msc_process_uri(transaction->transaction, safe_uri, safe_method, "1.1") != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_uri failed");
        return -1;
    }
    if (process_request_headers(transaction->transaction, request, decision) != 0) {
        return -1;
    }
    transaction->request_headers_processed = 1;
    capture_intervention(transaction->transaction, 1, decision);
    return 0;
}

int haproxy_modsecurity_transaction_begin_request(
        haproxy_modsecurity_engine *engine,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision,
        haproxy_modsecurity_transaction **transaction) {
    haproxy_modsecurity_transaction *created;

    if (transaction != 0) {
        *transaction = 0;
    }
    init_decision(decision, 0);
    if (engine == 0 || request == 0 || transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing engine, request, or transaction output");
        return 1;
    }
    validate_common_mapped_request(request, decision);
    created = (haproxy_modsecurity_transaction *)calloc(1U, sizeof(*created));
    if (created == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "failed to allocate ModSecurity transaction");
        return 1;
    }
    created->engine = engine;
    if (request->request_id != 0 && request->request_id[0] != '\0') {
        copy_message(created->request_id, sizeof(created->request_id),
            request->request_id);
    }
    created->transaction = create_request_transaction(engine->modsec, engine->rules, request);
    if (created->transaction == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_new_transaction returned null");
        transaction_cleanup(created, 0);
        return 1;
    }
    if (begin_transaction_protocol(created, request, decision) != 0) {
        transaction_cleanup(created, 0);
        return 1;
    }
    *transaction = created;
    return 0;
}

int haproxy_modsecurity_transaction_append_request_body_chunk(
        haproxy_modsecurity_transaction *transaction,
        const unsigned char *body,
        unsigned int body_len,
        haproxy_modsecurity_decision *decision) {
    if (transaction == 0) {
        init_decision(decision, 2);
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or request body");
        return 1;
    }
    const haproxy_modsecurity_body_phase phase = {
        2, &transaction->request_headers_processed, &transaction->request_body_processed,
        &transaction->request_body_started, &transaction->request_body_bytes_seen,
        &transaction->request_body_bytes_inspected, "missing transaction or request body",
        "request headers must be processed before request body chunks",
        "request body append after end-of-stream",
        "request body pointer is required when length is nonzero", "msc_append_request_body failed",
        "request body may only be finalized once", "msc_process_request_body failed",
        msc_append_request_body, msc_process_request_body
    };
    return append_body_chunk(transaction, body, body_len, decision, &phase);
}

int haproxy_modsecurity_transaction_finish_request_body(
        haproxy_modsecurity_transaction *transaction,
        haproxy_modsecurity_decision *decision) {
    if (transaction == 0) {
        init_decision(decision, 2);
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or request body");
        return 1;
    }
    const haproxy_modsecurity_body_phase phase = {
        2, &transaction->request_headers_processed, &transaction->request_body_processed,
        &transaction->request_body_started, &transaction->request_body_bytes_seen,
        &transaction->request_body_bytes_inspected, "missing transaction or request body",
        "request headers must be processed before request body finalization",
        "request body append after end-of-stream",
        "request body pointer is required when length is nonzero", "msc_append_request_body failed",
        "request body may only be finalized once", "msc_process_request_body failed",
        msc_append_request_body, msc_process_request_body
    };
    return finish_body(transaction, decision, &phase);
}

int haproxy_modsecurity_transaction_begin(
        haproxy_modsecurity_engine *engine,
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision,
        haproxy_modsecurity_transaction **transaction) {
    haproxy_modsecurity_transaction *created = 0;
    int rc;

    if (transaction == 0) {
        init_decision(decision, 0);
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction output");
        return 1;
    }
    *transaction = 0;
    rc = haproxy_modsecurity_transaction_begin_request(engine, request, decision,
        transaction);
    created = *transaction;
    if (rc != 0 || created == 0 || decision->disruptive != 0) {
        return rc;
    }
    if (request != 0 && request->body != 0 && request->body_len > 0U &&
            haproxy_modsecurity_transaction_append_request_body_chunk(created,
                request->body, request->body_len, decision) != 0) {
        return 1;
    }
    return haproxy_modsecurity_transaction_finish_request_body(created, decision);
}

int haproxy_modsecurity_transaction_process_response_headers(
        haproxy_modsecurity_transaction *transaction,
        const haproxy_modsecurity_response *response,
        haproxy_modsecurity_decision *decision) {
    const char *protocol;
    int status;
    unsigned int i;

    init_decision(decision, 3);
    if (transaction == 0 || transaction->transaction == 0 || response == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or response");
        return 1;
    }
    {
        haproxy_modsecurity_mapped_response mapped_response;
        msconnector_response_mapper_contract contract;
        char mapper_error[256];
        mapper_error[0] = '\0';
        msconnector_response_mapper_contract_init(&contract);
        if (haproxy_modsecurity_map_owned_response(response, &contract, &mapped_response,
                mapper_error, sizeof(mapper_error)) != 1 &&
                decision->log_message[0] == '\0') {
            copy_message(decision->log_message, sizeof(decision->log_message),
                mapper_error[0] != '\0' ? mapper_error :
                "common response mapper validation skipped");
        }
        haproxy_modsecurity_mapped_response_cleanup(&mapped_response);
    }
    for (i = 0; i < response->header_count; ++i) {
        const char *name = response->headers[i].name;
        const char *value = response->headers[i].value;
        if (name == 0 || name[0] == '\0') {
            continue;
        }
        if (value == 0) {
            value = "";
        }
        if (msc_add_response_header(transaction->transaction,
                (const unsigned char *)name,
                (const unsigned char *)value) != 1) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                "msc_add_response_header failed");
            return 1;
        }
    }
    status = response->status > 0 ? response->status : 200;
    protocol = response->protocol != 0 && response->protocol[0] != '\0' ?
        response->protocol : "HTTP/1.1";
    if (msc_process_response_headers(transaction->transaction, status, protocol) != 1) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "msc_process_response_headers failed");
        return 1;
    }
    transaction->response_headers_processed = 1;
    capture_intervention(transaction->transaction, 3, decision);
    return 0;
}

int haproxy_modsecurity_transaction_append_response_body_chunk(
        haproxy_modsecurity_transaction *transaction,
        const unsigned char *body,
        unsigned int body_len,
        haproxy_modsecurity_decision *decision) {
    if (transaction == 0) {
        init_decision(decision, 4);
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or response body");
        return 1;
    }
    const haproxy_modsecurity_body_phase phase = {
        4, &transaction->response_headers_processed, &transaction->response_body_processed,
        &transaction->response_body_started, &transaction->response_body_bytes_seen,
        &transaction->response_body_bytes_inspected, "missing transaction or response body",
        "response headers must be processed before response body chunks",
        "response body append after end-of-stream",
        "response body pointer is required when length is nonzero", "msc_append_response_body failed",
        "response body may only be finalized once", "msc_process_response_body failed",
        msc_append_response_body, msc_process_response_body
    };
    return append_body_chunk(transaction, body, body_len, decision, &phase);
}

int haproxy_modsecurity_transaction_finish_response_body(
        haproxy_modsecurity_transaction *transaction,
        haproxy_modsecurity_decision *decision) {
    if (transaction == 0) {
        init_decision(decision, 4);
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or response body");
        return 1;
    }
    const haproxy_modsecurity_body_phase phase = {
        4, &transaction->response_headers_processed, &transaction->response_body_processed,
        &transaction->response_body_started, &transaction->response_body_bytes_seen,
        &transaction->response_body_bytes_inspected, "missing transaction or response body",
        "response headers must be processed before response body finalization",
        "response body append after end-of-stream",
        "response body pointer is required when length is nonzero", "msc_append_response_body failed",
        "response body may only be finalized once", "msc_process_response_body failed",
        msc_append_response_body, msc_process_response_body
    };
    return finish_body(transaction, decision, &phase);
}

int haproxy_modsecurity_transaction_process_response_body(
        haproxy_modsecurity_transaction *transaction,
        const haproxy_modsecurity_response *response,
        haproxy_modsecurity_decision *decision) {
    init_decision(decision, 4);
    if (transaction == 0 || transaction->transaction == 0 || response == 0) {
        copy_message(decision->log_message, sizeof(decision->log_message),
            "missing transaction or response body");
        return 1;
    }
    if (!transaction->response_headers_processed) {
        if (haproxy_modsecurity_transaction_process_response_headers(
                transaction, response, decision) != 0 ||
                decision->disruptive != 0) {
            return decision->disruptive != 0 ? 0 : 1;
        }
        init_decision(decision, 4);
    }
    if (haproxy_modsecurity_transaction_append_response_body_chunk(
            transaction, response->body, response->body_len, decision) != 0) {
        return 1;
    }
    return haproxy_modsecurity_transaction_finish_response_body(
        transaction, decision);
}

void haproxy_modsecurity_transaction_finish(
        haproxy_modsecurity_transaction *transaction) {
    transaction_cleanup(transaction, 1);
}

void haproxy_modsecurity_transaction_abort(
        haproxy_modsecurity_transaction *transaction) {
    transaction_cleanup(transaction, 0);
}

const char *haproxy_modsecurity_binding_scope(void) {
    return "HAProxy libmodsecurity SPOA production binding with request, response-header, and bounded response-body support";
}

int haproxy_modsecurity_eval_request(
        const haproxy_modsecurity_request *request,
        haproxy_modsecurity_decision *decision) {
    return eval_request_internal(request, 0, decision);
}

int haproxy_modsecurity_phase1_header_eval(
        const char *method,
        const char *uri,
        const char *test_header_value,
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecRequestBodyAccess Off\n"
        "SecRule REQUEST_HEADERS:X-Haproxy-ModSecurity-Test "
        "\"@streq block\" "
        "\"id:1000001,phase:1,deny,status:403,"
        "msg:'HAProxy ModSecurity binding self-test block'\"\n";
    haproxy_modsecurity_header headers[1];
    haproxy_modsecurity_request request;

    headers[0].name = "X-Haproxy-ModSecurity-Test";
    headers[0].value = test_header_value != 0 ? test_header_value : "";
    memset(&request, 0, sizeof(request));
    request.method = method;
    request.uri = uri;
    request.headers = headers;
    request.header_count = test_header_value != 0 && test_header_value[0] != '\0' ? 1U : 0U;
    return eval_request_internal(&request, rules_text, decision);
}

int haproxy_modsecurity_phase1_header_self_test(
        haproxy_modsecurity_decision *decision) {
    int rc;

    rc = haproxy_modsecurity_phase1_header_eval("GET",
        "/haproxy-binding-self-test", "block", decision);
    if (rc != 0) {
        return rc;
    }
    if (decision != 0 && decision->disruptive != 0 &&
            decision->status == HAPROXY_MODSECURITY_EXPECTED_STATUS &&
            decision->rule_id == 1000001) {
        return 0;
    }
    if (decision != 0) {
        snprintf(decision->log_message, sizeof(decision->log_message),
            "expected disruptive status %d and Rule-ID 1000001, got disruptive=%d status=%d rule_id=%d",
            HAPROXY_MODSECURITY_EXPECTED_STATUS, decision->disruptive,
            decision->status, decision->rule_id);
    }
    return 1;
}

int haproxy_modsecurity_request_body_self_test(
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecRequestBodyAccess On\n"
        "SecRule ARGS:token \"@streq block\" "
        "\"id:1000002,phase:2,deny,status:403,"
        "msg:'HAProxy ModSecurity binding request-body self-test block'\"\n";
    static const unsigned char body[] = "token=block";
    haproxy_modsecurity_header headers[2];
    haproxy_modsecurity_request request;
    int rc;

    headers[0].name = "Content-Type";
    headers[0].value = "application/x-www-form-urlencoded";
    headers[1].name = "Content-Length";
    headers[1].value = "11";
    memset(&request, 0, sizeof(request));
    request.method = "POST";
    request.uri = "/haproxy-binding-body-self-test";
    request.headers = headers;
    request.header_count = 2U;
    request.body = body;
    request.body_len = (unsigned int)(sizeof(body) - 1U);
    rc = eval_request_internal(&request, rules_text, decision);
    if (rc != 0) {
        return rc;
    }
    if (decision != 0 && decision->disruptive != 0 &&
            decision->status == HAPROXY_MODSECURITY_EXPECTED_STATUS &&
            decision->rule_id == 1000002) {
        return 0;
    }
    if (decision != 0) {
        snprintf(decision->log_message, sizeof(decision->log_message),
            "expected request-body disruptive status %d and Rule-ID 1000002, got disruptive=%d status=%d rule_id=%d",
            HAPROXY_MODSECURITY_EXPECTED_STATUS, decision->disruptive,
            decision->status, decision->rule_id);
    }
    return 1;
}

int haproxy_modsecurity_crs_sqli_eval(
        const char *method,
        const char *uri,
        const char *host,
        const char *crs_preamble_file,
        haproxy_modsecurity_decision *decision) {
    static const char rules_text[] =
        "SecRuleEngine On\n"
        "SecAction \"id:199901,phase:2,pass,nolog\"\n";
    haproxy_modsecurity_header headers[1];
    haproxy_modsecurity_request request;

    headers[0].name = "Host";
    headers[0].value = host != 0 && host[0] != '\0' ? host : "localhost";
    memset(&request, 0, sizeof(request));
    request.method = method;
    request.uri = uri;
    request.headers = headers;
    request.header_count = 1U;
    request.rules_file = crs_preamble_file;
    return eval_request_internal(&request, rules_text, decision);
}

int haproxy_modsecurity_crs_sqli_self_test(
        const char *crs_preamble_file,
        haproxy_modsecurity_decision *decision) {
    haproxy_modsecurity_decision pass_decision;
    int rc;

    rc = haproxy_modsecurity_crs_sqli_eval("GET",
        "/?id=1%20UNION%20SELECT%20password%20FROM%20users",
        "localhost", crs_preamble_file, decision);
    if (rc != 0) {
        return rc;
    }
    if (decision == 0 || decision->disruptive == 0 ||
            decision->status != HAPROXY_MODSECURITY_EXPECTED_STATUS) {
        if (decision != 0) {
            snprintf(decision->log_message, sizeof(decision->log_message),
                "expected CRS disruptive status %d, got disruptive=%d status=%d",
                HAPROXY_MODSECURITY_EXPECTED_STATUS,
                decision->disruptive, decision->status);
        }
        return 1;
    }

    rc = haproxy_modsecurity_crs_sqli_eval("GET", "/diagnostic.txt",
        "localhost", crs_preamble_file, &pass_decision);
    if (rc != 0) {
        if (decision != 0) {
            copy_message(decision->log_message, sizeof(decision->log_message),
                pass_decision.log_message);
        }
        return rc;
    }
    if (pass_decision.disruptive != 0) {
        if (decision != 0) {
            snprintf(decision->log_message, sizeof(decision->log_message),
                "expected CRS pass probe to be non-disruptive, got status=%d",
                pass_decision.status);
        }
        return 1;
    }
    return 0;
}
