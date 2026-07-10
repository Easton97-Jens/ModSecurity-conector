#include "msconnector_runtime.h"

#include "modsecurity/modsecurity.h"
#include "modsecurity/rules_set.h"
#include "modsecurity/transaction.h"

#include "msconnector/body_policy.h"
#include "msconnector/block_statuses.h"
#include "msconnector/config.h"
#include "msconnector/config_parser.h"
#include "msconnector/decision_action.h"
#include "msconnector/directive_adapter.h"
#include "msconnector/dos_guard.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/flow_guard.h"
#include "msconnector/headers.h"
#include "msconnector/http_status.h"
#include "msconnector/integrity_event.h"
#include "msconnector/limits.h"
#include "msconnector/memory.h"
#include "msconnector/modsecurity_engine.h"
#include "msconnector/path_policy.h"
#include "msconnector/rule_id.h"
#include "msconnector/rule_loader.h"
#include "msconnector/transaction_id.h"

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define RUNTIME_NAME_SIZE 64U
#define RUNTIME_PATH_SIZE 4096U
#define RUNTIME_INLINE_RULE_SIZE 8192U
#define RUNTIME_HEADER_NAME_SIZE 256U
#define RUNTIME_CONFIG_LINE_SIZE 12288U
#define RUNTIME_REASON_SIZE 256U
#define RUNTIME_REDIRECT_SIZE 1024U
#define RUNTIME_TIMESTAMP_SIZE 32U
#define RUNTIME_METHOD_SIZE 256U
#define RUNTIME_URI_SIZE 16384U
#define RUNTIME_HTTP_VERSION_SIZE 64U
#define RUNTIME_ADDRESS_SIZE 1024U
#define RUNTIME_EVENT_METHOD_SIZE 64U
#define RUNTIME_EVENT_URI_SIZE 256U
#define RUNTIME_EVENT_CLIENT_IP_SIZE 64U

typedef struct msconnector_runtime_owned_config {
    char rules_inline[RUNTIME_INLINE_RULE_SIZE];
    char rules_file[RUNTIME_PATH_SIZE];
    char rules_remote_key[RUNTIME_HEADER_NAME_SIZE];
    char rules_remote_url[RUNTIME_PATH_SIZE];
    char transaction_id[RUNTIME_HEADER_NAME_SIZE];
    char transaction_id_header[RUNTIME_HEADER_NAME_SIZE];
    char phase4_content_types_file[RUNTIME_PATH_SIZE];
    char event_path[RUNTIME_PATH_SIZE];
} msconnector_runtime_owned_config;

typedef struct msconnector_native_transaction {
    Transaction *transaction;
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH];
    char reason[RUNTIME_REASON_SIZE];
    char redirect_url[RUNTIME_REDIRECT_SIZE];
} msconnector_native_transaction;

struct msconnector_runtime {
    char connector_name[RUNTIME_NAME_SIZE];
    msconnector_config config;
    msconnector_runtime_owned_config owned;
    msconnector_body_policy body_policy;
    msconnector_resource_limits limits;
    msconnector_modsecurity_engine engine;
    ModSecurity *modsecurity;
    FILE *event_file;
    uint64_t previous_event_hash;
    unsigned long transaction_counter;
};

struct msconnector_runtime_transaction {
    msconnector_runtime *runtime;
    const msconnector_request *request;
    const msconnector_response *response;
    msconnector_modsecurity_transaction modsecurity;
    msconnector_flow_guard flow;
    char transaction_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    int native_started;
    int request_blocked;
    int response_started;
    int finish_attempted;
    int finished;
};

static void set_text_error(char *error, size_t error_len, const char *message) {
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "%s", message == NULL ? "unknown error" : message);
    }
}

static int runtime_error(
    msconnector_error *error,
    msconnector_error_code code,
    const char *message,
    const char *source) {
    msconnector_error_set(error, code, message, source);
    return 0;
}

static int string_is_empty(const char *value) {
    return value == NULL || value[0] == '\0';
}

static int bounded_c_string(
    const char *value,
    size_t capacity,
    int required) {
    size_t index;
    if (value == NULL) {
        return required == 0;
    }
    for (index = 0U; index < capacity; ++index) {
        if (value[index] == '\0') {
            return required == 0 || index > 0U;
        }
    }
    return 0;
}

static int validate_request_input(
    const msconnector_request *request,
    msconnector_error *error) {
    if (!bounded_c_string(request->method, RUNTIME_METHOD_SIZE, 1) ||
        !bounded_c_string(request->uri, RUNTIME_URI_SIZE, 1) ||
        !bounded_c_string(request->http_version, RUNTIME_HTTP_VERSION_SIZE, 0) ||
        !bounded_c_string(request->hostname, RUNTIME_ADDRESS_SIZE, 0) ||
        !bounded_c_string(request->client.address, RUNTIME_ADDRESS_SIZE, 0) ||
        !bounded_c_string(request->server.address, RUNTIME_ADDRESS_SIZE, 0)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "request string metadata is missing or not bounded", "runtime");
    }
    if (request->client.port < 0 || request->client.port > 65535 ||
        request->server.port < 0 || request->server.port > 65535) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "request endpoint port is outside the valid range", "runtime");
    }
    if (request->header_count > 0U && request->headers == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "request headers are required when header_count is nonzero", "runtime");
    }
    if (request->body.size > 0U && request->body.data == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "request body data is required when body size is nonzero", "runtime");
    }
    return 1;
}

static int validate_response_input(
    const msconnector_response *response,
    msconnector_error *error) {
    if (!msconnector_http_status_is_valid(response->status) ||
        !bounded_c_string(response->http_version, RUNTIME_HTTP_VERSION_SIZE, 0)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "response status or HTTP version is invalid", "runtime");
    }
    if (response->header_count > 0U && response->headers == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "response headers are required when header_count is nonzero", "runtime");
    }
    if (response->body.size > 0U && response->body.data == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "response body data is required when body size is nonzero", "runtime");
    }
    return 1;
}

static char *trim_left(char *value) {
    while (*value != '\0' && isspace((unsigned char)*value)) {
        ++value;
    }
    return value;
}

static void trim_right(char *value) {
    size_t size = strlen(value);
    while (size > 0U && isspace((unsigned char)value[size - 1U])) {
        value[--size] = '\0';
    }
}

static int copy_config_value(
    char *destination,
    size_t destination_size,
    const char *value,
    const char *key,
    char *error,
    size_t error_len) {
    size_t size;
    if (destination == NULL || destination_size == 0U || value == NULL) {
        set_text_error(error, error_len, "invalid configuration destination");
        return 0;
    }
    size = strlen(value);
    if (size >= destination_size) {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "configuration value too long: %s", key);
        }
        return 0;
    }
    memcpy(destination, value, size + 1U);
    return 1;
}

static int parse_body_mode(const char *value, msconnector_body_mode *out) {
    if (value == NULL || out == NULL) {
        return 0;
    }
    if (strcmp(value, "none") == 0) {
        *out = MSCONNECTOR_BODY_MODE_NONE;
        return 1;
    }
    if (strcmp(value, "buffered") == 0) {
        *out = MSCONNECTOR_BODY_MODE_BUFFERED;
        return 1;
    }
    return 0;
}

static int assign_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    size_t parsed_size;
    int parsed_status;
    enum msconnector_bool_option parsed_bool;
    enum msconnector_phase4_mode parsed_phase4;
    msconnector_body_mode parsed_body_mode;

    if (strcmp(key, "enabled") == 0) {
        if (!msconnector_parse_bool(value, &parsed_bool)) {
            set_text_error(error, error_len, "invalid enabled value");
            return 0;
        }
        runtime->config.enable = parsed_bool;
    } else if (strcmp(key, "use_error_log") == 0) {
        if (!msconnector_parse_bool(value, &parsed_bool)) {
            set_text_error(error, error_len, "invalid use_error_log value");
            return 0;
        }
        runtime->config.use_error_log = parsed_bool;
    } else if (strcmp(key, "rules_inline") == 0) {
        if (!copy_config_value(runtime->owned.rules_inline, sizeof(runtime->owned.rules_inline), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.rules_inline = runtime->owned.rules_inline;
    } else if (strcmp(key, "rules_file") == 0) {
        if (!copy_config_value(runtime->owned.rules_file, sizeof(runtime->owned.rules_file), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.rules_file = runtime->owned.rules_file;
    } else if (strcmp(key, "rules_remote_key") == 0) {
        if (!copy_config_value(runtime->owned.rules_remote_key, sizeof(runtime->owned.rules_remote_key), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.rules_remote_key = runtime->owned.rules_remote_key;
    } else if (strcmp(key, "rules_remote_url") == 0) {
        if (!copy_config_value(runtime->owned.rules_remote_url, sizeof(runtime->owned.rules_remote_url), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.rules_remote_url = runtime->owned.rules_remote_url;
    } else if (strcmp(key, "transaction_id") == 0) {
        if (!copy_config_value(runtime->owned.transaction_id, sizeof(runtime->owned.transaction_id), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.transaction_id = runtime->owned.transaction_id;
    } else if (strcmp(key, "transaction_id_header") == 0) {
        if (!copy_config_value(runtime->owned.transaction_id_header, sizeof(runtime->owned.transaction_id_header), value, key, error, error_len)) {
            return 0;
        }
    } else if (strcmp(key, "phase4_mode") == 0) {
        if (!msconnector_parse_phase4_mode(value, &parsed_phase4)) {
            set_text_error(error, error_len, "invalid phase4_mode value");
            return 0;
        }
        runtime->config.phase4_mode = parsed_phase4;
    } else if (strcmp(key, "phase4_content_types_file") == 0) {
        if (!copy_config_value(runtime->owned.phase4_content_types_file, sizeof(runtime->owned.phase4_content_types_file), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.phase4_content_types_file = runtime->owned.phase4_content_types_file;
    } else if (strcmp(key, "event_path") == 0) {
        if (!copy_config_value(runtime->owned.event_path, sizeof(runtime->owned.event_path), value, key, error, error_len)) {
            return 0;
        }
        runtime->config.phase4_log_path = runtime->owned.event_path;
    } else if (strcmp(key, "request_body_mode") == 0) {
        if (!parse_body_mode(value, &parsed_body_mode)) {
            set_text_error(error, error_len, "request_body_mode must be none or buffered");
            return 0;
        }
        runtime->body_policy.request_body_mode = parsed_body_mode;
    } else if (strcmp(key, "response_body_mode") == 0) {
        if (!parse_body_mode(value, &parsed_body_mode)) {
            set_text_error(error, error_len, "response_body_mode must be none or buffered");
            return 0;
        }
        runtime->body_policy.response_body_mode = parsed_body_mode;
    } else if (strcmp(key, "request_body_limit") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid request_body_limit value");
            return 0;
        }
        runtime->body_policy.request_body_limit = parsed_size;
        runtime->limits.max_request_body_bytes = parsed_size;
    } else if (strcmp(key, "response_body_limit") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid response_body_limit value");
            return 0;
        }
        runtime->body_policy.response_body_limit = parsed_size;
        runtime->limits.max_response_body_bytes = parsed_size;
        runtime->config.phase4_body_limit = parsed_size;
    } else if (strcmp(key, "default_block_status") == 0) {
        if (!msconnector_parse_http_status(value, &parsed_status)) {
            set_text_error(error, error_len, "invalid default_block_status value");
            return 0;
        }
        runtime->config.default_block_status = parsed_status;
    } else if (strcmp(key, "default_error_status") == 0) {
        if (!msconnector_parse_http_status(value, &parsed_status)) {
            set_text_error(error, error_len, "invalid default_error_status value");
            return 0;
        }
        runtime->config.default_error_status = parsed_status;
    } else if (strcmp(key, "max_header_count") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid max_header_count value");
            return 0;
        }
        runtime->limits.max_header_count = parsed_size;
    } else if (strcmp(key, "max_header_name_size") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid max_header_name_size value");
            return 0;
        }
        runtime->limits.max_header_name_size = parsed_size;
    } else if (strcmp(key, "max_header_value_size") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid max_header_value_size value");
            return 0;
        }
        runtime->limits.max_header_value_size = parsed_size;
    } else if (strcmp(key, "max_total_header_bytes") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid max_total_header_bytes value");
            return 0;
        }
        runtime->limits.max_total_header_bytes = parsed_size;
    } else if (strcmp(key, "max_event_json_bytes") == 0) {
        if (!msconnector_parse_size(value, &parsed_size) || parsed_size == 0U) {
            set_text_error(error, error_len, "invalid max_event_json_bytes value");
            return 0;
        }
        runtime->limits.max_event_json_bytes = parsed_size;
    } else {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "unknown configuration key: %s", key);
        }
        return 0;
    }
    return 1;
}

static void runtime_defaults(msconnector_runtime *runtime) {
    memset(runtime, 0, sizeof(*runtime));
    msconnector_config_init(&runtime->config);
    msconnector_body_policy_init(&runtime->body_policy);
    msconnector_resource_limits_init(&runtime->limits);
    runtime->body_policy.request_body_mode = MSCONNECTOR_BODY_MODE_BUFFERED;
    runtime->body_policy.response_body_mode = MSCONNECTOR_BODY_MODE_NONE;
    runtime->body_policy.request_body_limit = runtime->limits.max_request_body_bytes;
    runtime->body_policy.response_body_limit = runtime->limits.max_response_body_bytes;
    (void)snprintf(runtime->owned.transaction_id_header,
        sizeof(runtime->owned.transaction_id_header), "%s", "x-request-id");
}

static int validate_runtime_config(msconnector_runtime *runtime, char *error, size_t error_len) {
    if (!msconnector_config_validate(&runtime->config, error, error_len)) {
        return 0;
    }
    if (!msconnector_resource_limits_validate(&runtime->limits)) {
        set_text_error(error, error_len, "invalid resource limits");
        return 0;
    }
    if (runtime->limits.max_event_json_bytes > SIZE_MAX - 2U) {
        set_text_error(error, error_len, "max_event_json_bytes is too large");
        return 0;
    }
    if (!msconnector_body_mode_is_supported(runtime->body_policy.request_body_mode) ||
        !msconnector_body_mode_is_supported(runtime->body_policy.response_body_mode)) {
        set_text_error(error, error_len, "invalid body policy");
        return 0;
    }
    if (runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_STREAMING ||
        runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_STREAMING) {
        set_text_error(error, error_len, "streaming body mode is not implemented");
        return 0;
    }
    if (runtime->body_policy.request_body_limit == 0U ||
        runtime->body_policy.response_body_limit == 0U) {
        set_text_error(error, error_len, "body limits must be nonzero");
        return 0;
    }
    if (runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        string_is_empty(runtime->config.rules_inline) &&
        string_is_empty(runtime->config.rules_file) &&
        string_is_empty(runtime->config.rules_remote_url)) {
        set_text_error(error, error_len, "enabled connector requires inline, file or remote rules");
        return 0;
    }
    if (!string_is_empty(runtime->config.phase4_log_path) &&
        msconnector_path_has_parent_reference(runtime->config.phase4_log_path)) {
        set_text_error(error, error_len, "event_path must not contain a parent-directory segment");
        return 0;
    }
    if (!msconnector_directive_adapter_validate_all(error, error_len)) {
        return 0;
    }
    return 1;
}

static int load_runtime_config(
    msconnector_runtime *runtime,
    const char *connector_name,
    const char *config_path,
    char *error,
    size_t error_len) {
    FILE *file;
    char line[RUNTIME_CONFIG_LINE_SIZE];
    unsigned long line_number = 0UL;

    if (runtime == NULL || string_is_empty(connector_name) || string_is_empty(config_path)) {
        set_text_error(error, error_len, "connector name and config path are required");
        return 0;
    }
    runtime_defaults(runtime);
    if (!copy_config_value(runtime->connector_name, sizeof(runtime->connector_name),
            connector_name, "connector_name", error, error_len)) {
        return 0;
    }
    file = fopen(config_path, "r");
    if (file == NULL) {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "cannot open config %s: %s", config_path, strerror(errno));
        }
        return 0;
    }
    while (fgets(line, sizeof(line), file) != NULL) {
        char *key;
        char *value;
        char *separator;
        ++line_number;
        if (strchr(line, '\n') == NULL && !feof(file)) {
            set_text_error(error, error_len, "configuration line is too long");
            (void)fclose(file);
            return 0;
        }
        trim_right(line);
        key = trim_left(line);
        if (*key == '\0' || *key == '#') {
            continue;
        }
        separator = strchr(key, '=');
        if (separator == NULL) {
            if (error != NULL && error_len > 0U) {
                (void)snprintf(error, error_len, "invalid configuration line %lu", line_number);
            }
            (void)fclose(file);
            return 0;
        }
        *separator = '\0';
        value = trim_left(separator + 1);
        trim_right(key);
        trim_right(value);
        if (*key == '\0' || *value == '\0' ||
            !assign_config_value(runtime, key, value, error, error_len)) {
            if (error != NULL && error_len > 0U && error[0] == '\0') {
                (void)snprintf(error, error_len, "invalid configuration line %lu", line_number);
            }
            (void)fclose(file);
            return 0;
        }
    }
    if (ferror(file)) {
        set_text_error(error, error_len, "failed while reading connector configuration");
        (void)fclose(file);
        return 0;
    }
    (void)fclose(file);
    msconnector_config_apply_defaults(&runtime->config);
    if (runtime->config.phase4_body_limit != 0U) {
        runtime->body_policy.response_body_limit = runtime->config.phase4_body_limit;
        runtime->limits.max_response_body_bytes = runtime->config.phase4_body_limit;
    }
    return validate_runtime_config(runtime, error, error_len);
}

static int native_init(void *userdata, msconnector_error *error) {
    msconnector_runtime *runtime = userdata;
    runtime->modsecurity = msc_init();
    if (runtime->modsecurity == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "msc_init failed", "libmodsecurity");
    }
    msc_set_connector_info(runtime->modsecurity, runtime->connector_name);
    return 1;
}

static void native_cleanup(void *userdata) {
    msconnector_runtime *runtime = userdata;
    if (runtime != NULL && runtime->modsecurity != NULL) {
        msc_cleanup(runtime->modsecurity);
        runtime->modsecurity = NULL;
    }
}

static void *native_create_rules(void *userdata, msconnector_error *error) {
    (void)userdata;
    RulesSet *rules = msc_create_rules_set();
    if (rules == NULL) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_RULE_LOAD_FAILED,
            "msc_create_rules_set failed", "libmodsecurity");
    }
    return rules;
}

static void native_destroy_rules(void *userdata, void *rules_set) {
    (void)userdata;
    if (rules_set != NULL) {
        (void)msc_rules_cleanup((RulesSet *)rules_set);
    }
}

static void *native_new_transaction(
    void *userdata,
    void *rules_set,
    const char *transaction_id,
    msconnector_error *error) {
    msconnector_runtime *runtime = userdata;
    msconnector_native_transaction *native;
    native = calloc(1U, sizeof(*native));
    if (native == NULL) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction allocation failed", "libmodsecurity");
        return NULL;
    }
    native->transaction = string_is_empty(transaction_id)
        ? msc_new_transaction(runtime->modsecurity, (RulesSet *)rules_set, NULL)
        : msc_new_transaction_with_id(runtime->modsecurity, (RulesSet *)rules_set,
              transaction_id, NULL);
    if (native->transaction == NULL) {
        free(native);
        (void)runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "msc_new_transaction failed", "libmodsecurity");
        return NULL;
    }
    return native;
}

static void native_free_transaction(void *userdata, void *native_transaction) {
    msconnector_native_transaction *native = native_transaction;
    (void)userdata;
    if (native != NULL) {
        if (native->transaction != NULL) {
            msc_transaction_cleanup(native->transaction);
        }
        memset(native, 0, sizeof(*native));
        free(native);
    }
}

static int native_decision(
    const msconnector_runtime *runtime,
    msconnector_native_transaction *native,
    enum msconnector_phase phase,
    msconnector_decision *decision,
    msconnector_error *error) {
    ModSecurityIntervention intervention;
    msconnector_intervention common_intervention;
    int intervention_result;
    int disruptive;

    memset(&intervention, 0, sizeof(intervention));
    intervention.status = 200;
    intervention_result = msc_intervention(native->transaction, &intervention);
    disruptive = intervention_result != 0 || intervention.disruptive != 0;
    native->rule_id[0] = '\0';
    native->reason[0] = '\0';
    native->redirect_url[0] = '\0';
    if (intervention.log != NULL) {
        (void)msconnector_rule_id_extract_from_message(
            intervention.log, native->rule_id, sizeof(native->rule_id));
    }
    if (disruptive) {
        int intervention_status = intervention.status;
        (void)snprintf(native->reason, sizeof(native->reason), "%s",
            "ModSecurity rule requested an intervention");
        if (intervention.url != NULL) {
            (void)snprintf(native->redirect_url, sizeof(native->redirect_url), "%s", intervention.url);
        } else if (!msconnector_block_status_is_allowed(intervention_status)) {
            intervention_status = runtime->config.default_block_status;
        }
        common_intervention = msconnector_intervention_make(
            1,
            intervention_status,
            native->redirect_url[0] == '\0' ? NULL : native->redirect_url,
            native->reason);
        if (!msconnector_decision_from_intervention(
                decision,
                &common_intervention,
                phase,
                native->rule_id[0] == '\0' ? NULL : native->rule_id,
                native->reason)) {
            msc_intervention_cleanup(&intervention);
            return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
                "failed to map intervention", "runtime");
        }
    } else {
        msconnector_decision_set_allow(decision);
        decision->phase = phase;
    }
    msc_intervention_cleanup(&intervention);
    return 1;
}

static const char *http_version_without_prefix(const char *version) {
    if (string_is_empty(version)) {
        return "1.1";
    }
    return strncmp(version, "HTTP/", 5U) == 0 ? version + 5 : version;
}

static int native_process_connection(
    void *userdata,
    void *native_transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    const char *client;
    const char *server;
    int client_port;
    int server_port;
    msconnector_runtime *runtime = userdata;
    client = string_is_empty(request->client.address) ? "127.0.0.1" : request->client.address;
    server = string_is_empty(request->server.address) ? "127.0.0.1" : request->server.address;
    client_port = request->client.port > 0 ? request->client.port : 0;
    server_port = request->server.port > 0 ? request->server.port : 0;
    if (msc_process_connection(native->transaction, client, client_port, server, server_port) < 0 ||
        msc_process_uri(native->transaction, request->uri, request->method,
            http_version_without_prefix(request->http_version)) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "connection or URI processing failed", "libmodsecurity");
    }
    if (!string_is_empty(request->hostname)) {
        (void)msc_set_request_hostname(native->transaction,
            (const unsigned char *)request->hostname);
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_URI, decision, error);
}

static int native_process_request_headers(
    void *userdata,
    void *native_transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    size_t index;
    msconnector_runtime *runtime = userdata;
    for (index = 0U; index < request->header_count; ++index) {
        const msconnector_header *header = &request->headers[index];
        if (msc_add_n_request_header(native->transaction,
                (const unsigned char *)header->name, header->name_size,
                (const unsigned char *)header->value, header->value_size) < 0) {
            return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
                "request header mapping failed", "libmodsecurity");
        }
    }
    if (msc_process_request_headers(native->transaction) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request header processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_REQUEST_HEADERS, decision, error);
}

static int native_process_request_body(
    void *userdata,
    void *native_transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    msconnector_runtime *runtime = userdata;
    if (request->body.size > 0U &&
        msc_append_request_body(native->transaction, request->body.data, request->body.size) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request body append failed", "libmodsecurity");
    }
    if (msc_process_request_body(native->transaction) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request body processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_REQUEST_BODY, decision, error);
}

static int native_process_response_headers(
    void *userdata,
    void *native_transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    size_t index;
    msconnector_runtime *runtime = userdata;
    for (index = 0U; index < response->header_count; ++index) {
        const msconnector_header *header = &response->headers[index];
        if (msc_add_n_response_header(native->transaction,
                (const unsigned char *)header->name, header->name_size,
                (const unsigned char *)header->value, header->value_size) < 0) {
            return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
                "response header mapping failed", "libmodsecurity");
        }
    }
    if (msc_process_response_headers(native->transaction, response->status,
            http_version_without_prefix(response->http_version)) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response header processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_RESPONSE_HEADERS, decision, error);
}

static int native_process_response_body(
    void *userdata,
    void *native_transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    msconnector_runtime *runtime = userdata;
    if (response->body.size > 0U &&
        msc_append_response_body(native->transaction, response->body.data, response->body.size) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response body append failed", "libmodsecurity");
    }
    if (msc_process_response_body(native->transaction) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response body processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_RESPONSE_BODY, decision, error);
}

static int native_process_logging(
    void *userdata,
    void *native_transaction,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    (void)userdata;
    if (msc_process_logging(native->transaction) < 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "logging phase failed", "libmodsecurity");
    }
    return 1;
}

static int rules_add_inline(
    void *userdata,
    void *rules_set,
    const char *rules,
    msconnector_error *error) {
    const char *native_error = NULL;
    int result;
    (void)userdata;
    result = msc_rules_add((RulesSet *)rules_set, rules, &native_error);
    if (result < 0) {
        if (native_error != NULL) {
            msc_rules_error_cleanup(native_error);
        }
        return runtime_error(error, MSCONNECTOR_ERROR_RULE_PARSE_FAILED,
            "libmodsecurity rejected inline rules", "libmodsecurity");
    }
    if (native_error != NULL) {
        msc_rules_error_cleanup(native_error);
    }
    return 1;
}

static int rules_add_file(
    void *userdata,
    void *rules_set,
    const char *path,
    msconnector_error *error) {
    const char *native_error = NULL;
    int result;
    (void)userdata;
    result = msc_rules_add_file((RulesSet *)rules_set, path, &native_error);
    if (result < 0) {
        if (native_error != NULL) {
            msc_rules_error_cleanup(native_error);
        }
        return runtime_error(error, MSCONNECTOR_ERROR_RULE_LOAD_FAILED,
            "libmodsecurity rejected rules file", "libmodsecurity");
    }
    if (native_error != NULL) {
        msc_rules_error_cleanup(native_error);
    }
    return 1;
}

static int rules_add_remote(
    void *userdata,
    void *rules_set,
    const char *key,
    const char *url,
    msconnector_error *error) {
    const char *native_error = NULL;
    int result;
    (void)userdata;
    result = msc_rules_add_remote((RulesSet *)rules_set, key, url, &native_error);
    if (result < 0) {
        if (native_error != NULL) {
            msc_rules_error_cleanup(native_error);
        }
        return runtime_error(error, MSCONNECTOR_ERROR_RULE_LOAD_FAILED,
            "libmodsecurity rejected remote rules", "libmodsecurity");
    }
    if (native_error != NULL) {
        msc_rules_error_cleanup(native_error);
    }
    return 1;
}

static int start_runtime(msconnector_runtime *runtime, char *error, size_t error_len) {
    msconnector_modsecurity_engine_ops ops;
    msconnector_rule_loader_backend rule_backend;
    msconnector_rule_loader loader;
    msconnector_error common_error;

    if (runtime->config.enable != MSCONNECTOR_BOOL_ON) {
        return 1;
    }
    memset(&ops, 0, sizeof(ops));
    ops.userdata = runtime;
    ops.init = native_init;
    ops.cleanup = native_cleanup;
    ops.create_rules_set = native_create_rules;
    ops.destroy_rules_set = native_destroy_rules;
    ops.new_transaction = native_new_transaction;
    ops.free_transaction = native_free_transaction;
    ops.process_connection = native_process_connection;
    ops.process_request_headers = native_process_request_headers;
    ops.process_request_body = native_process_request_body;
    ops.process_response_headers = native_process_response_headers;
    ops.process_response_body = native_process_response_body;
    ops.process_logging = native_process_logging;
    msconnector_modsecurity_engine_init(&runtime->engine, &ops);
    msconnector_error_init(&common_error);
    if (!msconnector_modsecurity_engine_start(&runtime->engine, &common_error) ||
        !msconnector_modsecurity_engine_create_rules(&runtime->engine, &common_error)) {
        set_text_error(error, error_len, common_error.message);
        return 0;
    }
    memset(&rule_backend, 0, sizeof(rule_backend));
    rule_backend.userdata = runtime;
    rule_backend.add_inline = rules_add_inline;
    rule_backend.add_file = rules_add_file;
    rule_backend.add_remote = rules_add_remote;
    msconnector_rule_loader_init(&loader, runtime->engine.rules_set, &rule_backend);
    if (!msconnector_rule_loader_load_config(&loader, &runtime->config, &common_error)) {
        set_text_error(error, error_len, common_error.message);
        return 0;
    }
    if (!string_is_empty(runtime->config.phase4_log_path)) {
        runtime->event_file = fopen(runtime->config.phase4_log_path, "a");
        if (runtime->event_file == NULL) {
            if (error != NULL && error_len > 0U) {
                (void)snprintf(error, error_len, "cannot open event_path %s: %s",
                    runtime->config.phase4_log_path, strerror(errno));
            }
            return 0;
        }
        (void)setvbuf(runtime->event_file, NULL, _IOLBF, 0U);
    }
    return 1;
}

int msconnector_runtime_create(
    const char *connector_name,
    const char *config_path,
    msconnector_runtime **out,
    char *error,
    size_t error_len) {
    msconnector_runtime *runtime;
    if (out != NULL) {
        *out = NULL;
    }
    if (out == NULL) {
        set_text_error(error, error_len, "runtime output is required");
        return 0;
    }
    if (error != NULL && error_len > 0U) {
        error[0] = '\0';
    }
    runtime = calloc(1U, sizeof(*runtime));
    if (runtime == NULL) {
        set_text_error(error, error_len, "runtime allocation failed");
        return 0;
    }
    if (!load_runtime_config(runtime, connector_name, config_path, error, error_len) ||
        !start_runtime(runtime, error, error_len)) {
        msconnector_runtime_destroy(&runtime);
        return 0;
    }
    *out = runtime;
    return 1;
}

int msconnector_runtime_config_check(
    const char *connector_name,
    const char *config_path,
    char *error,
    size_t error_len) {
    msconnector_runtime *runtime = NULL;
    int result = msconnector_runtime_create(
        connector_name, config_path, &runtime, error, error_len);
    msconnector_runtime_destroy(&runtime);
    return result;
}

void msconnector_runtime_destroy(msconnector_runtime **runtime_pointer) {
    msconnector_runtime *runtime;
    if (runtime_pointer == NULL || *runtime_pointer == NULL) {
        return;
    }
    runtime = *runtime_pointer;
    msconnector_modsecurity_engine_cleanup(&runtime->engine);
    if (runtime->event_file != NULL) {
        (void)fclose(runtime->event_file);
        runtime->event_file = NULL;
    }
    memset(runtime, 0, sizeof(*runtime));
    free(runtime);
    *runtime_pointer = NULL;
}

void msconnector_runtime_request_contract(
    const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract) {
    if (contract == NULL) {
        return;
    }
    msconnector_request_mapper_contract_init(contract);
    if (runtime != NULL) {
        contract->max_header_count = runtime->limits.max_header_count;
        contract->max_body_bytes = runtime->limits.max_request_body_bytes;
        contract->request_body = runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_NONE
            ? MSCONNECTOR_MAPPER_UNSUPPORTED : MSCONNECTOR_MAPPER_OPTIONAL;
    }
}

void msconnector_runtime_response_contract(
    const msconnector_runtime *runtime,
    msconnector_response_mapper_contract *contract) {
    if (contract == NULL) {
        return;
    }
    msconnector_response_mapper_contract_init(contract);
    if (runtime != NULL) {
        contract->max_header_count = runtime->limits.max_header_count;
        contract->max_body_bytes = runtime->limits.max_response_body_bytes;
        contract->response_body = runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_NONE
            ? MSCONNECTOR_MAPPER_UNSUPPORTED : MSCONNECTOR_MAPPER_OPTIONAL;
    }
}

size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_request_body_bytes;
}

size_t msconnector_runtime_response_body_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_response_body_bytes;
}

size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_total_header_bytes;
}

size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_header_count;
}

int msconnector_runtime_error_http_status(
    const msconnector_runtime *runtime,
    msconnector_error_code code) {
    switch (code) {
    case MSCONNECTOR_ERROR_INVALID_CONFIG:
    case MSCONNECTOR_ERROR_RULE_PARSE_FAILED:
    case MSCONNECTOR_ERROR_RULE_LOAD_FAILED:
    case MSCONNECTOR_ERROR_HOST_API_FAILURE:
    case MSCONNECTOR_ERROR_MODSECURITY_FAILURE:
    case MSCONNECTOR_ERROR_IO:
    case MSCONNECTOR_ERROR_INTERNAL:
        return runtime == NULL
            ? msconnector_error_http_status(code)
            : runtime->config.default_error_status;
    default:
        return msconnector_error_http_status(code);
    }
}

static void timestamp_now(char *buffer, size_t size) {
    time_t now = time(NULL);
    struct tm utc;
    if (buffer == NULL || size == 0U) {
        return;
    }
    buffer[0] = '\0';
#if defined(_POSIX_VERSION)
    if (gmtime_r(&now, &utc) == NULL) {
        return;
    }
#else
    {
        struct tm *value = gmtime(&now);
        if (value == NULL) {
            return;
        }
        utc = *value;
    }
#endif
    (void)strftime(buffer, size, "%Y-%m-%dT%H:%M:%SZ", &utc);
}

static size_t event_escape_size(unsigned char value) {
    if (value == '"' || value == '\\' || value == '\n' ||
        value == '\r' || value == '\t') {
        return 2U;
    }
    return value < 0x20U ? 6U : 1U;
}

/*
 * The common event serializer has fixed-size escaped metadata fields. Bound
 * dynamic request metadata before hashing so the integrity hash describes
 * exactly the value that is written, and preserve any shortening through the
 * event's truncated flag.
 */
static int copy_event_metadata(
    const char *source,
    char *destination,
    size_t destination_size) {
    size_t source_index = 0U;
    size_t destination_index = 0U;
    size_t escaped_size = 0U;
    if (destination == NULL || destination_size == 0U) {
        return source != NULL && source[0] != '\0';
    }
    destination[0] = '\0';
    if (source == NULL) {
        return 0;
    }
    while (source[source_index] != '\0') {
        size_t next_size = event_escape_size((unsigned char)source[source_index]);
        if (destination_index + 1U >= destination_size ||
            next_size > destination_size - 1U - escaped_size) {
            break;
        }
        destination[destination_index++] = source[source_index++];
        escaped_size += next_size;
    }
    destination[destination_index] = '\0';
    return source[source_index] != '\0';
}

static int emit_decision_event(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime *runtime;
    msconnector_event event;
    msconnector_allocator allocator;
    char timestamp[RUNTIME_TIMESTAMP_SIZE];
    char method[RUNTIME_EVENT_METHOD_SIZE];
    char uri[RUNTIME_EVENT_URI_SIZE];
    char client_ip[RUNTIME_EVENT_CLIENT_IP_SIZE];
    char *json = NULL;
    size_t json_size;
    size_t written_size;
    int metadata_truncated = 0;
    int truncated = 0;

    if (transaction == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "event input is required", "runtime");
    }
    runtime = transaction->runtime;
    if (runtime->event_file == NULL ||
        !msconnector_decision_to_event(decision, &event, runtime->connector_name,
            transaction->transaction_id)) {
        return 1;
    }
    timestamp_now(timestamp, sizeof(timestamp));
    event.meta.timestamp = timestamp;
    event.meta.event = event.meta.message_id;
    metadata_truncated |= copy_event_metadata(
        transaction->request == NULL ? NULL : transaction->request->method,
        method,
        sizeof(method));
    metadata_truncated |= copy_event_metadata(
        transaction->request == NULL ? NULL : transaction->request->uri,
        uri,
        sizeof(uri));
    metadata_truncated |= copy_event_metadata(
        transaction->request == NULL ? NULL : transaction->request->client.address,
        client_ip,
        sizeof(client_ip));
    event.flags.truncated = metadata_truncated;
    event.request.method = method;
    event.request.uri = uri;
    event.request.client_ip = client_ip;
    if (msconnector_flow_guard_next_sequence(&transaction->flow, &event.integrity.sequence) !=
        MSCONNECTOR_FLOW_GUARD_OK) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "event sequence failed", "runtime");
    }
    event.integrity.previous_hash = runtime->previous_event_hash;
    event.integrity.event_hash = msconnector_integrity_event_hash(
        &event, event.integrity.previous_hash);
    json_size = runtime->limits.max_event_json_bytes + 2U;
    msconnector_allocator_init(&allocator, json_size);
    if (!msconnector_alloc_checked(&allocator, json_size, (void **)&json)) {
        return runtime_error(error, MSCONNECTOR_ERROR_EVENT_TOO_LARGE,
            "event buffer allocation failed", "runtime");
    }
    (void)msconnector_event_write_jsonl_line(
        &event, json, json_size, &truncated);
    written_size = strlen(json);
    if (written_size == 0U || json[written_size - 1U] != '\n' ||
        !msconnector_dos_guard_check_event_json_size(
            written_size, &runtime->limits, error)) {
        msconnector_free_checked(&allocator, (void **)&json, json_size);
        if (error == NULL || error->code == MSCONNECTOR_ERROR_NONE) {
            return runtime_error(error, MSCONNECTOR_ERROR_EVENT_TOO_LARGE,
                "event JSONL serialization exceeded its configured limit", "runtime");
        }
        return 0;
    }
    if (fputs(json, runtime->event_file) == EOF || fflush(runtime->event_file) != 0) {
        msconnector_free_checked(&allocator, (void **)&json, json_size);
        return runtime_error(error, MSCONNECTOR_ERROR_IO,
            "event JSONL write failed", "runtime");
    }
    runtime->previous_event_hash = event.integrity.event_hash;
    msconnector_free_checked(&allocator, (void **)&json, json_size);
    return 1;
}

static int mark_flow(
    msconnector_runtime_transaction *transaction,
    enum msconnector_phase phase,
    msconnector_error *error) {
    int result = msconnector_flow_guard_mark_validated(&transaction->flow, phase);
    if (result != MSCONNECTOR_FLOW_GUARD_OK) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            msconnector_flow_guard_error_name(result), "flow_guard");
    }
    return 1;
}

static int handle_decision(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    msconnector_error *error,
    int *terminal) {
    if (terminal == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "terminal decision output is required", "runtime");
    }
    *terminal = 0;
    if (!msconnector_decision_action_is_disruptive(
            msconnector_decision_action_from_decision(decision))) {
        return 1;
    }
    transaction->request_blocked = 1;
    if (!emit_decision_event(transaction, decision, error)) {
        return 0;
    }
    *terminal = 1;
    return 1;
}

static int abort_transaction_begin(
    msconnector_runtime_transaction **transaction) {
    msconnector_runtime_transaction_destroy(transaction);
    return 0;
}

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;
    msconnector_transaction_id_context id_context;
    msconnector_transaction_id_result id_result;
    char fallback_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    int terminal;

    if (out != NULL) {
        *out = NULL;
    }
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (runtime == NULL || request == NULL || out == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "runtime, request, output and decision are required", "runtime");
    }
    msconnector_decision_set_allow(decision);
    if (!validate_request_input(request, error)) {
        msconnector_decision_set_error(decision,
            msconnector_runtime_error_http_status(
                runtime,
                error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code),
            error == NULL ? "invalid request" : error->message);
        return 0;
    }
    if (!msconnector_dos_guard_check_request(request, &runtime->limits, error)) {
        msconnector_decision_set_error(decision,
            msconnector_runtime_error_http_status(
                runtime,
                error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code),
            error == NULL ? "invalid request" : error->message);
        return 0;
    }
    transaction = calloc(1U, sizeof(*transaction));
    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction allocation failed", "runtime");
    }
    transaction->runtime = runtime;
    transaction->request = request;
    ++runtime->transaction_counter;
    (void)snprintf(fallback_id, sizeof(fallback_id), "%s-%lu",
        runtime->connector_name, runtime->transaction_counter);
    memset(&id_context, 0, sizeof(id_context));
    id_context.config = &runtime->config;
    id_context.request = request;
    id_context.host_request_id = string_is_empty(host_request_id) ? NULL : host_request_id;
    id_context.fallback_id = fallback_id;
    id_context.header_name = runtime->owned.transaction_id_header;
    if (!msconnector_transaction_id_resolve(&id_context, &id_result, error) ||
        !msconnector_transaction_id_copy(id_result.value,
            transaction->transaction_id, sizeof(transaction->transaction_id))) {
        free(transaction);
        return 0;
    }
    msconnector_flow_guard_init(&transaction->flow, transaction->transaction_id);
    *out = transaction;
    if (runtime->config.enable != MSCONNECTOR_BOOL_ON) {
        return 1;
    }
    if (!msconnector_modsecurity_transaction_init(&transaction->modsecurity,
            &runtime->engine, transaction->transaction_id, error)) {
        return abort_transaction_begin(out);
    }
    transaction->native_started = 1;
    if (!msconnector_modsecurity_process_connection(
            &transaction->modsecurity, request, decision, error) ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_CONNECTION, error) ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_URI, error)) {
        return abort_transaction_begin(out);
    }
    if (!handle_decision(transaction, decision, error, &terminal)) {
        return abort_transaction_begin(out);
    }
    if (terminal) {
        return 1;
    }
    if (!msconnector_modsecurity_process_request_headers(
            &transaction->modsecurity, request, decision, error) ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_HEADERS, error)) {
        return abort_transaction_begin(out);
    }
    if (!handle_decision(transaction, decision, error, &terminal)) {
        return abort_transaction_begin(out);
    }
    if (terminal) {
        return 1;
    }
    if (runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED) {
        if (!msconnector_modsecurity_process_request_body(
                &transaction->modsecurity, request, decision, error)) {
            return abort_transaction_begin(out);
        }
    } else if (request->body.size > 0U) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "request body is disabled", "runtime");
        return abort_transaction_begin(out);
    }
    if (!mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_BODY, error)) {
        return abort_transaction_begin(out);
    }
    if (!handle_decision(transaction, decision, error, &terminal)) {
        return abort_transaction_begin(out);
    }
    return 1;
}

int msconnector_runtime_transaction_process_response(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime *runtime;
    int terminal;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || response == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction, response and decision are required", "runtime");
    }
    runtime = transaction->runtime;
    msconnector_decision_set_allow(decision);
    if (transaction->finish_attempted) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response processing after transaction finish is not allowed", "runtime");
    }
    if (transaction->response_started) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response processing may only be attempted once", "runtime");
    }
    transaction->response_started = 1;
    if (transaction->request_blocked || runtime->config.enable != MSCONNECTOR_BOOL_ON) {
        return 1;
    }
    if (!validate_response_input(response, error)) {
        msconnector_decision_set_error(decision,
            msconnector_runtime_error_http_status(
                runtime,
                error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code),
            error == NULL ? "invalid response" : error->message);
        return 0;
    }
    if (!msconnector_dos_guard_check_response(response, &runtime->limits, error)) {
        msconnector_decision_set_error(decision,
            msconnector_runtime_error_http_status(
                runtime,
                error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code),
            error == NULL ? "invalid response" : error->message);
        return 0;
    }
    transaction->response = response;
    if (!msconnector_modsecurity_process_response_headers(
            &transaction->modsecurity, response, decision, error) ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_HEADERS, error)) {
        return 0;
    }
    if (!handle_decision(transaction, decision, error, &terminal)) {
        return 0;
    }
    if (terminal) {
        return 1;
    }
    if (runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED) {
        if (!msconnector_modsecurity_process_response_body(
                &transaction->modsecurity, response, decision, error)) {
            return 0;
        }
    } else if (response->body.size > 0U) {
        return runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "response body is disabled", "runtime");
    }
    if (!mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error)) {
        return 0;
    }
    return handle_decision(transaction, decision, error, &terminal);
}

int msconnector_runtime_transaction_finish(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    if (transaction->finished) {
        return 1;
    }
    if (transaction->finish_attempted) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction finish previously failed", "runtime");
    }
    transaction->finish_attempted = 1;
    if (msconnector_flow_guard_mark_immutable(&transaction->flow) !=
        MSCONNECTOR_FLOW_GUARD_OK) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction could not be made immutable", "flow_guard");
    }
    if (transaction->native_started &&
        !msconnector_modsecurity_process_logging(&transaction->modsecurity, error)) {
        return 0;
    }
    transaction->finished = 1;
    return 1;
}

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction) {
    return transaction == NULL ? NULL : transaction->transaction_id;
}

void msconnector_runtime_transaction_destroy(
    msconnector_runtime_transaction **transaction_pointer) {
    msconnector_runtime_transaction *transaction;
    msconnector_error ignored;
    if (transaction_pointer == NULL || *transaction_pointer == NULL) {
        return;
    }
    transaction = *transaction_pointer;
    msconnector_error_init(&ignored);
    if (!transaction->finish_attempted) {
        (void)msconnector_runtime_transaction_finish(transaction, &ignored);
    }
    if (transaction->native_started) {
        msconnector_modsecurity_transaction_cleanup(&transaction->modsecurity);
    }
    memset(transaction, 0, sizeof(*transaction));
    free(transaction);
    *transaction_pointer = NULL;
}
