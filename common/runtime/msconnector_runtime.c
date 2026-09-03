#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200809L
#endif

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
#include "msconnector/intervention.h"
#include "msconnector/transaction_contract.h"
#include "msconnector/limits.h"
#include "msconnector/memory.h"
#include "msconnector/modsecurity_engine.h"
#include "msconnector/path_policy.h"
#include "msconnector/rule_id.h"
#include "msconnector/rule_loader.h"
#include "msconnector/transaction_id.h"

#include <ctype.h>
#include <errno.h>
#include <sched.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#if defined(__linux__)
#include <sys/random.h>
#endif

#if !defined(_WIN32)
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#endif

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
#define RESPONSE_COMPANION_PRECLAIM_TTL_MS 5000ULL
#define RUNTIME_EVENT_CLIENT_IP_SIZE 64U
#define RUNTIME_EVENT_CONTENT_TYPE_SIZE 256U
#define RUNTIME_INTEGRATION_MODE_SIZE 64U

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

typedef struct msconnector_runtime_event_metadata {
    char transaction_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    char request_method[RUNTIME_EVENT_METHOD_SIZE];
    char request_uri[RUNTIME_EVENT_URI_SIZE];
    char request_client_ip[RUNTIME_EVENT_CLIENT_IP_SIZE];
    char response_content_type[RUNTIME_EVENT_CONTENT_TYPE_SIZE];
    int truncated;
} msconnector_runtime_event_metadata;

struct msconnector_runtime {
    char connector_name[RUNTIME_NAME_SIZE];
    char integration_mode[RUNTIME_INTEGRATION_MODE_SIZE];
    const msconnector_transaction_profile *profile;
    msconnector_config config;
    msconnector_runtime_owned_config owned;
    msconnector_body_policy body_policy;
    msconnector_resource_limits limits;
    msconnector_modsecurity_engine engine;
    ModSecurity *modsecurity;
    FILE *event_file;
    /* Serializes mutable engine/event state shared by independently owned
     * transactions. Adapter-local locks are insufficient once a request-only
     * route hands a transaction to a response companion. */
    atomic_flag operation_lock;
    uint64_t previous_event_hash;
    unsigned long transaction_counter;
};

struct msconnector_runtime_transaction {
    msconnector_runtime *runtime;
    msconnector_modsecurity_transaction modsecurity;
    msconnector_flow_guard flow;
    msconnector_transaction_contract contract;
    msconnector_runtime_event_metadata metadata;
    msconnector_runtime_body_progress request_body;
    msconnector_runtime_body_progress response_body;
    int response_original_status;
    int native_started;
    int request_blocked;
    int response_headers_processed;
    int response_headers_sent;
    int response_body_started;
    int host_action_event_emitted;
    int terminal_event_emitted;
    int response_companion_handed_off;
    int finish_attempted;
    int finished;
};

typedef struct msconnector_runtime_host_action {
    msconnector_decision_action actual_action;
    int visible_http_status;
    const char *transport_result;
    int connection_aborted;
} msconnector_runtime_host_action;

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

/* The final event-file descriptor policy is shared with native hosts.  Keep
 * FILE ownership local to the runtime after the Common helper establishes the
 * no-follow, regular-file, owner, and private-mode invariant. */
static FILE *open_event_file_secure(const char *path) {
    int fd = -1;
    FILE *file;

    if (!msconnector_open_private_event_file(path, &fd)) {
        return NULL;
    }
    file = fdopen(fd, "a");
    if (file == NULL) {
        const int saved_errno = errno;
        (void)close(fd);
        errno = saved_errno;
    }
    return file;
}

static uint64_t transaction_now_ms(void) {
    struct timespec now;

    if (clock_gettime(CLOCK_MONOTONIC, &now) != 0 || now.tv_sec < 0) {
        return 0U;
    }
    return (uint64_t)now.tv_sec * UINT64_C(1000) +
        (uint64_t)now.tv_nsec / UINT64_C(1000000);
}

static int contract_error(
    msconnector_error *error,
    int transition,
    const char *message) {
    return runtime_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
        message == NULL ? msconnector_transaction_transition_name(transition) : message,
        "transaction_contract");
}

static int string_is_empty(const char *value) {
    return value == NULL || value[0] == '\0';
}

static void runtime_operation_lock(msconnector_runtime *runtime) {
    while (atomic_flag_test_and_set_explicit(&runtime->operation_lock,
            memory_order_acquire)) {
        (void)sched_yield();
    }
}

static void runtime_operation_unlock(msconnector_runtime *runtime) {
    atomic_flag_clear_explicit(&runtime->operation_lock, memory_order_release);
}

static msconnector_runtime *transaction_mutable_runtime(
    msconnector_runtime_transaction *transaction) {
    return transaction == NULL ? NULL : transaction->runtime;
}

static int append_request_body_to_engine(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t append_size,
    msconnector_error *error) {
    msconnector_runtime *runtime = transaction_mutable_runtime(transaction);
    int appended;

    runtime_operation_lock(runtime);
    appended = msconnector_modsecurity_append_request_body(
        &transaction->modsecurity, data, append_size, error);
    runtime_operation_unlock(runtime);
    return appended;
}

static int finish_request_body_in_engine(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime *runtime = transaction_mutable_runtime(transaction);
    int finished;

    runtime_operation_lock(runtime);
    finished = msconnector_modsecurity_finish_request_body(
        &transaction->modsecurity, decision, error);
    runtime_operation_unlock(runtime);
    return finished;
}

static int valid_host_action(msconnector_decision_action action) {
    switch (action) {
      case MSCONNECTOR_DECISION_ACTION_DENY:
      case MSCONNECTOR_DECISION_ACTION_REDIRECT:
      case MSCONNECTOR_DECISION_ACTION_DROP:
      case MSCONNECTOR_DECISION_ACTION_RATE_LIMIT:
      case MSCONNECTOR_DECISION_ACTION_LOG_ONLY:
      case MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION:
      case MSCONNECTOR_DECISION_ACTION_STREAM_RESET:
      case MSCONNECTOR_DECISION_ACTION_ERROR:
      case MSCONNECTOR_DECISION_ACTION_UNSUPPORTED:
        return 1;
      default:
        return 0;
    }
}

static int valid_host_transport_result(const char *value) {
    return value != NULL && (
        strcmp(value, "completed") == 0 ||
        strcmp(value, "http_status") == 0 ||
        strcmp(value, "log_only") == 0 ||
        strcmp(value, "connection_aborted") == 0 ||
        strcmp(value, "stream_reset") == 0 ||
        strcmp(value, "client_cancelled") == 0 ||
        strcmp(value, "client_disconnected") == 0 ||
        strcmp(value, "upstream_reset") == 0 ||
        strcmp(value, "upstream_disconnected") == 0 ||
        strcmp(value, "timeout") == 0 ||
        strcmp(value, "short_write") == 0 ||
        strcmp(value, "write_would_block") == 0 ||
        strcmp(value, "engine_error") == 0 ||
        strcmp(value, "host_error") == 0 ||
        strcmp(value, "not_observable") == 0
    );
}

static const char *phase4_mode_name(enum msconnector_phase4_mode mode) {
    switch (mode) {
      case MSCONNECTOR_PHASE4_MODE_MINIMAL:
        return "minimal";
      case MSCONNECTOR_PHASE4_MODE_SAFE:
        return "safe";
      case MSCONNECTOR_PHASE4_MODE_STRICT:
        return "strict";
      case MSCONNECTOR_PHASE4_MODE_UNSET:
      default:
        return NULL;
    }
}

static int bounded_c_string(
    const char *value,
    size_t capacity,
    int required) {
    if (value == NULL) {
        return required == 0;
    }
    for (size_t index = 0U; index < capacity; ++index) {
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
        !bounded_c_string(request->client.address, RUNTIME_ADDRESS_SIZE, 1) ||
        !bounded_c_string(request->server.address, RUNTIME_ADDRESS_SIZE, 1)) {
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

static size_t header_bytes(const msconnector_header *headers, size_t header_count) {
    size_t total = 0U;

    for (size_t index = 0U; index < header_count; ++index) {
        if (headers[index].name_size > SIZE_MAX - total) {
            return SIZE_MAX;
        }
        total += headers[index].name_size;
        if (headers[index].value_size > SIZE_MAX - total) {
            return SIZE_MAX;
        }
        total += headers[index].value_size;
    }
    return total;
}

/* Host instance IDs leave the runtime in response-companion correlation and
 * (for the request-only compatibility service) an HTTP response header.  Do
 * not copy arbitrary host metadata into that boundary. */
static int safe_host_instance_component(const char *value) {
    if (string_is_empty(value)) {
        return 0;
    }
    for (size_t index = 0U; value[index] != '\0'; ++index) {
        const unsigned char character = (unsigned char)value[index];
        if (!(isalnum(character) || character == '.' || character == ':' ||
              character == '-' || character == '_' || character == '[' ||
              character == ']')) {
            return 0;
        }
    }
    return 1;
}

static int contract_host_id_for_request(
    const msconnector_runtime *runtime,
    const msconnector_transaction_profile *profile,
    const msconnector_request *request,
    char out[MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE]) {
    const char *adapter_id;
    int written;

    if (runtime == NULL || request == NULL || out == NULL) {
        return 0;
    }
    if (profile != NULL) {
        adapter_id = profile->host_adapter_id;
    } else if (string_is_empty(runtime->integration_mode)) {
        adapter_id = "runtime";
    } else {
        adapter_id = runtime->integration_mode;
    }
    if (!safe_host_instance_component(adapter_id)) {
        return 0;
    }
    if (string_is_empty(request->server.address)) {
        written = snprintf(out, MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE,
            "%s", adapter_id);
    } else if (!safe_host_instance_component(request->server.address)) {
        return 0;
    } else {
        written = snprintf(out, MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE,
            "%s@%s:%d", adapter_id, request->server.address,
            request->server.port);
    }
    return written >= 0 && (size_t)written <
        MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE;
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
    if (strcmp(value, "streaming") == 0) {
        *out = MSCONNECTOR_BODY_MODE_STREAMING;
        return 1;
    }
    return 0;
}

static int assign_boolean_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    enum msconnector_bool_option *target;
    const char *message;
    enum msconnector_bool_option parsed;

    if (strcmp(key, "enabled") == 0) {
        target = &runtime->config.enable;
        message = "invalid enabled value";
    } else if (strcmp(key, "use_error_log") == 0) {
        target = &runtime->config.use_error_log;
        message = "invalid use_error_log value";
    } else {
        return -1;
    }
    if (!msconnector_parse_bool(value, &parsed)) {
        set_text_error(error, error_len, message);
        return 0;
    }
    *target = parsed;
    return 1;
}

static int assign_owned_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    char *destination;
    size_t destination_size;
    const char **config_value = NULL;

    if (strcmp(key, "rules_inline") == 0) {
        destination = runtime->owned.rules_inline;
        destination_size = sizeof(runtime->owned.rules_inline);
        config_value = &runtime->config.rules_inline;
    } else if (strcmp(key, "rules_file") == 0) {
        destination = runtime->owned.rules_file;
        destination_size = sizeof(runtime->owned.rules_file);
        config_value = &runtime->config.rules_file;
    } else if (strcmp(key, "rules_remote_key") == 0) {
        destination = runtime->owned.rules_remote_key;
        destination_size = sizeof(runtime->owned.rules_remote_key);
        config_value = &runtime->config.rules_remote_key;
    } else if (strcmp(key, "rules_remote_url") == 0) {
        destination = runtime->owned.rules_remote_url;
        destination_size = sizeof(runtime->owned.rules_remote_url);
        config_value = &runtime->config.rules_remote_url;
    } else if (strcmp(key, "transaction_id") == 0) {
        destination = runtime->owned.transaction_id;
        destination_size = sizeof(runtime->owned.transaction_id);
        config_value = &runtime->config.transaction_id;
    } else if (strcmp(key, "transaction_id_header") == 0) {
        destination = runtime->owned.transaction_id_header;
        destination_size = sizeof(runtime->owned.transaction_id_header);
    } else if (strcmp(key, "phase4_content_types_file") == 0) {
        destination = runtime->owned.phase4_content_types_file;
        destination_size = sizeof(runtime->owned.phase4_content_types_file);
        config_value = &runtime->config.phase4_content_types_file;
    } else if (strcmp(key, "event_path") == 0 ||
        strcmp(key, "phase4_event_log") == 0) {
        destination = runtime->owned.event_path;
        destination_size = sizeof(runtime->owned.event_path);
        config_value = &runtime->config.phase4_log_path;
    } else {
        return -1;
    }
    if (!copy_config_value(destination, destination_size, value, key, error, error_len)) {
        return 0;
    }
    if (config_value != NULL) {
        *config_value = destination;
    }
    return 1;
}

static int assign_body_mode_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    msconnector_body_mode *target;
    msconnector_body_mode parsed;

    if (strcmp(key, "request_body_mode") == 0) {
        target = &runtime->body_policy.request_body_mode;
    } else if (strcmp(key, "response_body_mode") == 0) {
        target = &runtime->body_policy.response_body_mode;
    } else {
        return -1;
    }
    if (!parse_body_mode(value, &parsed)) {
        set_text_error(error, error_len,
            strcmp(key, "request_body_mode") == 0
                ? "request_body_mode must be none, buffered or streaming"
                : "response_body_mode must be none, buffered or streaming");
        return 0;
    }
    *target = parsed;
    return 1;
}

static int assign_limit_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    size_t parsed;
    size_t *target;
    const char *message;

    if (strcmp(key, "request_body_limit") == 0) {
        target = &runtime->body_policy.request_body_limit;
        message = "invalid request_body_limit value";
    } else if (strcmp(key, "response_body_limit") == 0) {
        target = &runtime->body_policy.response_body_limit;
        message = "invalid response_body_limit value";
    } else if (strcmp(key, "max_header_count") == 0) {
        target = &runtime->limits.max_header_count;
        message = "invalid max_header_count value";
    } else if (strcmp(key, "max_header_name_size") == 0) {
        target = &runtime->limits.max_header_name_size;
        message = "invalid max_header_name_size value";
    } else if (strcmp(key, "max_header_value_size") == 0) {
        target = &runtime->limits.max_header_value_size;
        message = "invalid max_header_value_size value";
    } else if (strcmp(key, "max_total_header_bytes") == 0) {
        target = &runtime->limits.max_total_header_bytes;
        message = "invalid max_total_header_bytes value";
    } else if (strcmp(key, "max_event_json_bytes") == 0) {
        target = &runtime->limits.max_event_json_bytes;
        message = "invalid max_event_json_bytes value";
    } else {
        return -1;
    }
    if (!msconnector_parse_size(value, &parsed) || parsed == 0U) {
        set_text_error(error, error_len, message);
        return 0;
    }
    *target = parsed;
    if (target == &runtime->body_policy.request_body_limit) {
        runtime->config.request_body_limit = parsed;
        runtime->limits.max_request_body_bytes = parsed;
    } else if (target == &runtime->body_policy.response_body_limit) {
        runtime->config.response_body_limit = parsed;
        runtime->limits.max_response_body_bytes = parsed;
        runtime->config.phase4_body_limit = parsed;
    }
    return 1;
}

static int assign_special_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    size_t parsed_size;
    int parsed_status;
    enum msconnector_phase4_mode parsed_phase4;
    msconnector_body_limit_action parsed_body_limit_action;

    if (strcmp(key, "phase4_mode") == 0) {
        if (!msconnector_parse_phase4_mode(value, &parsed_phase4)) {
            set_text_error(error, error_len, "invalid phase4_mode value");
            return 0;
        }
        runtime->config.phase4_mode = parsed_phase4;
    } else if (strcmp(key, "body_limit_action") == 0) {
        if (!msconnector_body_limit_action_parse(value,
                &parsed_body_limit_action)) {
            set_text_error(error, error_len,
                "body_limit_action must be reject or process_partial");
            return 0;
        }
        runtime->body_policy.body_limit_action = parsed_body_limit_action;
        runtime->config.body_limit_action = parsed_body_limit_action;
    } else if (strcmp(key, "late_intervention_timeout") == 0) {
        if (!msconnector_parse_nonnegative_size(value, &parsed_size)) {
            set_text_error(error, error_len,
                "late_intervention_timeout must be a nonnegative millisecond value");
            return 0;
        }
        runtime->config.late_intervention_timeout_ms = parsed_size;
    } else if (strcmp(key, "default_block_status") == 0 ||
        strcmp(key, "default_error_status") == 0) {
        if (!msconnector_parse_http_status(value, &parsed_status)) {
            set_text_error(error, error_len,
                strcmp(key, "default_block_status") == 0
                    ? "invalid default_block_status value"
                    : "invalid default_error_status value");
            return 0;
        }
        if (strcmp(key, "default_block_status") == 0) {
            runtime->config.default_block_status = parsed_status;
        } else {
            runtime->config.default_error_status = parsed_status;
        }
    } else {
        return -1;
    }
    return 1;
}

static int assign_config_value(
    msconnector_runtime *runtime,
    const char *key,
    const char *value,
    char *error,
    size_t error_len) {
    int result;

    result = assign_boolean_config_value(runtime, key, value, error, error_len);
    if (result >= 0) {
        return result;
    }
    result = assign_owned_config_value(runtime, key, value, error, error_len);
    if (result >= 0) {
        return result;
    }
    result = assign_body_mode_config_value(runtime, key, value, error, error_len);
    if (result >= 0) {
        return result;
    }
    result = assign_limit_config_value(runtime, key, value, error, error_len);
    if (result >= 0) {
        return result;
    }
    result = assign_special_config_value(runtime, key, value, error, error_len);
    if (result >= 0) {
        return result;
    }
    if (error != NULL && error_len > 0U) {
        (void)snprintf(error, error_len, "unknown configuration key: %s", key);
    }
    return 0;
}

static void runtime_defaults(msconnector_runtime *runtime) {
    memset(runtime, 0, sizeof(*runtime));
    atomic_flag_clear_explicit(&runtime->operation_lock, memory_order_release);
    msconnector_config_init(&runtime->config);
    msconnector_body_policy_init(&runtime->body_policy);
    msconnector_resource_limits_init(&runtime->limits);
    runtime->body_policy.request_body_mode = MSCONNECTOR_BODY_MODE_BUFFERED;
    runtime->body_policy.response_body_mode = MSCONNECTOR_BODY_MODE_NONE;
    runtime->body_policy.request_body_limit = runtime->limits.max_request_body_bytes;
    runtime->body_policy.response_body_limit = runtime->limits.max_response_body_bytes;
    runtime->config.request_body_limit = runtime->body_policy.request_body_limit;
    runtime->config.response_body_limit = runtime->body_policy.response_body_limit;
    runtime->config.body_limit_action = runtime->body_policy.body_limit_action;
    (void)snprintf(runtime->owned.transaction_id_header,
        sizeof(runtime->owned.transaction_id_header), "%s", "x-request-id");
}

static int validate_runtime_limits(
    const msconnector_runtime *runtime,
    char *error,
    size_t error_len) {
    if (!msconnector_resource_limits_validate(&runtime->limits)) {
        set_text_error(error, error_len, "invalid resource limits");
        return 0;
    }
    if (runtime->limits.max_event_json_bytes > SIZE_MAX - 2U) {
        set_text_error(error, error_len, "max_event_json_bytes is too large");
        return 0;
    }
    return 1;
}

static int validate_runtime_body_policy(
    const msconnector_runtime *runtime,
    char *error,
    size_t error_len) {
    if (!msconnector_body_mode_is_supported(runtime->body_policy.request_body_mode) ||
        !msconnector_body_mode_is_supported(runtime->body_policy.response_body_mode) ||
        !msconnector_body_limit_action_is_supported(
            runtime->body_policy.body_limit_action)) {
        set_text_error(error, error_len, "invalid body policy");
        return 0;
    }
    if (runtime->body_policy.request_body_limit == 0U ||
        runtime->body_policy.response_body_limit == 0U) {
        set_text_error(error, error_len, "body limits must be nonzero");
        return 0;
    }
    return 1;
}

static int validate_runtime_rule_source(
    const msconnector_runtime *runtime,
    char *error,
    size_t error_len) {
    if (!string_is_empty(runtime->config.rules_remote_key) ||
        !string_is_empty(runtime->config.rules_remote_url)) {
        set_text_error(error, error_len,
            "remote rule loading is disabled by security policy");
        return 0;
    }
    if (runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        string_is_empty(runtime->config.rules_inline) &&
        string_is_empty(runtime->config.rules_file)) {
        set_text_error(error, error_len, "enabled connector requires inline or file rules");
        return 0;
    }
    return 1;
}

static int validate_runtime_event_path(
    const msconnector_runtime *runtime,
    char *error,
    size_t error_len) {
    const char *path = runtime->config.phase4_log_path;
    if (!string_is_empty(path)) {
        const size_t path_length = strlen(path);
        size_t index;
        if (path_length >= RUNTIME_PATH_SIZE || path[path_length - 1U] == '/') {
            set_text_error(error, error_len, "event_path must be a normalized path");
            return 0;
        }
        for (index = 0U; index < path_length; ++index) {
            if (iscntrl((unsigned char)path[index]) || path[index] == '\\' ||
                (path[index] == '/' && (index + 1U == path_length || path[index + 1U] == '/'))) {
                set_text_error(error, error_len, "event_path contains an unsafe path character");
                return 0;
            }
        }
        if (msconnector_path_has_parent_reference(path) ||
            strstr(path, "/./") != NULL || strncmp(path, "./", 2U) == 0 ||
            (path_length >= 2U && strcmp(path + path_length - 2U, "/.") == 0) ||
            strcmp(path, ".") == 0 || strcmp(path, "..") == 0) {
            set_text_error(error, error_len, "event_path must not contain a parent or dot segment");
            return 0;
        }
    }
    return 1;
}

static int validate_runtime_config(
    const msconnector_runtime *runtime,
    char *error,
    size_t error_len) {
    if (!msconnector_config_validate(&runtime->config, error, error_len) ||
        !validate_runtime_limits(runtime, error, error_len) ||
        !validate_runtime_body_policy(runtime, error, error_len) ||
        !validate_runtime_rule_source(runtime, error, error_len) ||
        !validate_runtime_event_path(runtime, error, error_len)) {
        return 0;
    }
    return msconnector_directive_adapter_validate_all(error, error_len);
}

static int parse_runtime_config_line(
    msconnector_runtime *runtime,
    char *line,
    unsigned long line_number,
    int is_last_line,
    char *error,
    size_t error_len) {
    char *key;
    char *value;
    char *separator;

    if (strchr(line, '\n') == NULL && !is_last_line) {
        set_text_error(error, error_len, "configuration line is too long");
        return 0;
    }
    trim_right(line);
    key = trim_left(line);
    if (*key == '\0' || *key == '#') {
        return 1;
    }
    separator = strchr(key, '=');
    if (separator == NULL) {
        if (error != NULL && error_len > 0U) {
            (void)snprintf(error, error_len, "invalid configuration line %lu", line_number);
        }
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
        ++line_number;
        if (!parse_runtime_config_line(
                runtime, line, line_number, feof(file), error, error_len)) {
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
    runtime->body_policy.request_body_limit = runtime->config.request_body_limit;
    runtime->body_policy.response_body_limit = runtime->config.response_body_limit;
    runtime->body_policy.body_limit_action = runtime->config.body_limit_action;
    runtime->limits.max_request_body_bytes = runtime->config.request_body_limit;
    runtime->limits.max_response_body_bytes = runtime->config.response_body_limit;
    return validate_runtime_config(runtime, error, error_len);
}

static int native_init(void *userdata, msconnector_error *error) {
    msconnector_runtime *runtime = userdata;

    if (runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "runtime is required", "runtime");
    }
    runtime_operation_lock(runtime);
    runtime->modsecurity = msc_init();
    if (runtime->modsecurity == NULL) {
        runtime_operation_unlock(runtime);
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "msc_init failed", "libmodsecurity");
    }
    msc_set_connector_info(runtime->modsecurity, runtime->connector_name);
    runtime_operation_unlock(runtime);
    return 1;
}

static void native_cleanup(void *userdata) {
    msconnector_runtime *runtime = userdata;
    if (runtime != NULL && runtime->modsecurity != NULL) {
        runtime_operation_lock(runtime);
        msc_cleanup(runtime->modsecurity);
        runtime->modsecurity = NULL;
        runtime_operation_unlock(runtime);
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
        msconnector_secure_zero(native, sizeof(*native));
        free(native);
    }
}

/*
 * libmodsecurity reports SecRequestBodyLimitAction Reject as a disruptive
 * request-body intervention, but uses 403 for its status. Preserve all
 * ordinary rule actions: only the exact no-redirect body-limit signature has
 * the HTTP request-entity semantics of 413 and is rule-ID-free.
 */
static int native_is_request_body_limit_rejection(
    enum msconnector_phase phase,
    const ModSecurityIntervention *intervention) {
    msconnector_intervention common_intervention;

    if (intervention == NULL) {
        return 0;
    }
    common_intervention = msconnector_intervention_make(
        intervention->disruptive, intervention->status, intervention->url,
        intervention->log);
    return msconnector_intervention_is_request_body_limit_rejection(phase,
        &common_intervention);
}

static int native_intervention_status(
    enum msconnector_phase phase,
    const ModSecurityIntervention *intervention) {
    if (native_is_request_body_limit_rejection(phase, intervention)) {
        return 413;
    }
    return intervention == NULL ? 0 : intervention->status;
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
    int body_limit;
    int redirect_length;

    memset(&intervention, 0, sizeof(intervention));
    intervention.status = 200;
    intervention_result = msc_intervention(native->transaction, &intervention);
    disruptive = intervention_result != 0 || intervention.disruptive != 0;
    body_limit = native_is_request_body_limit_rejection(phase, &intervention);
    native->rule_id[0] = '\0';
    native->reason[0] = '\0';
    native->redirect_url[0] = '\0';
    if (intervention.log != NULL) {
        (void)msconnector_rule_id_extract_from_message(
            intervention.log, native->rule_id, sizeof(native->rule_id));
    }
    if (disruptive) {
        int intervention_status = msconnector_intervention_normalize_status(
            intervention.url, native_intervention_status(phase, &intervention),
            runtime->config.default_block_status);
        (void)snprintf(native->reason, sizeof(native->reason), "%s",
            "ModSecurity rule requested an intervention");
        if (msconnector_intervention_has_redirect_url(intervention.url)) {
            redirect_length = snprintf(native->redirect_url,
                sizeof(native->redirect_url), "%s", intervention.url);
            if (redirect_length < 0 ||
                (size_t)redirect_length >= sizeof(native->redirect_url)) {
                msc_intervention_cleanup(&intervention);
                return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
                    "redirect target exceeds the native runtime limit", "runtime");
            }
        }
        if (body_limit) {
            msconnector_decision_set_body_limit(decision, native->reason);
        } else {
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
    msconnector_runtime *runtime = userdata;
    if (msc_process_connection(native->transaction,
            request->client.address, request->client.port,
            request->server.address, request->server.port) != 1 ||
        msc_process_uri(native->transaction, request->uri, request->method,
            http_version_without_prefix(request->http_version)) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "connection or URI processing failed", "libmodsecurity");
    }
    if (!string_is_empty(request->hostname)) {
        if (msc_set_request_hostname(native->transaction,
                (const unsigned char *)request->hostname) != 1) {
            return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
                "request hostname mapping failed", "libmodsecurity");
        }
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
                (const unsigned char *)header->value, header->value_size) != 1) {
            return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
                "request header mapping failed", "libmodsecurity");
        }
    }
    if (msc_process_request_headers(native->transaction) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request header processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_REQUEST_HEADERS, decision, error);
}

static int native_append_request_body(
    void *userdata,
    void *native_transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    (void)userdata;
    if (size > 0U &&
        msc_append_request_body(native->transaction, data, size) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request body append failed", "libmodsecurity");
    }
    return 1;
}

static int native_finish_request_body(
    void *userdata,
    void *native_transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    msconnector_runtime *runtime = userdata;
    if (msc_process_request_body(native->transaction) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "request body processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_REQUEST_BODY,
        decision, error);
}

static int native_process_request_body(
    void *userdata,
    void *native_transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    return native_append_request_body(userdata, native_transaction,
               request->body.data, request->body.size, error) &&
        native_finish_request_body(userdata, native_transaction, decision, error);
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
                (const unsigned char *)header->value, header->value_size) != 1) {
            return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
                "response header mapping failed", "libmodsecurity");
        }
    }
    if (msc_process_response_headers(native->transaction, response->status,
            http_version_without_prefix(response->http_version)) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response header processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_RESPONSE_HEADERS, decision, error);
}

static int native_append_response_body(
    void *userdata,
    void *native_transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    (void)userdata;
    if (size > 0U &&
        msc_append_response_body(native->transaction, data, size) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response body append failed", "libmodsecurity");
    }
    return 1;
}

static int native_finish_response_body(
    void *userdata,
    void *native_transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    msconnector_runtime *runtime = userdata;
    if (msc_process_response_body(native->transaction) != 1) {
        return runtime_error(error, MSCONNECTOR_ERROR_MODSECURITY_FAILURE,
            "response body processing failed", "libmodsecurity");
    }
    return native_decision(runtime, native, MSCONNECTOR_PHASE_RESPONSE_BODY,
        decision, error);
}

static int native_process_response_body(
    void *userdata,
    void *native_transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    return native_append_response_body(userdata, native_transaction,
               response->body.data, response->body.size, error) &&
        native_finish_response_body(userdata, native_transaction, decision, error);
}

static int native_process_logging(
    void *userdata,
    void *native_transaction,
    msconnector_error *error) {
    msconnector_native_transaction *native = native_transaction;
    (void)userdata;
    if (msc_process_logging(native->transaction) != 1) {
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
    ops.append_request_body = native_append_request_body;
    ops.finish_request_body = native_finish_request_body;
    ops.process_response_headers = native_process_response_headers;
    ops.process_response_body = native_process_response_body;
    ops.append_response_body = native_append_response_body;
    ops.finish_response_body = native_finish_response_body;
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
    msconnector_rule_loader_init(&loader, runtime->engine.rules_set, &rule_backend);
    if (!msconnector_rule_loader_load_config(&loader, &runtime->config, &common_error)) {
        set_text_error(error, error_len, common_error.message);
        return 0;
    }
    if (!string_is_empty(runtime->config.phase4_log_path)) {
        runtime->event_file = open_event_file_secure(runtime->config.phase4_log_path);
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

int msconnector_runtime_set_event_integration_mode(
    msconnector_runtime *runtime,
    const char *integration_mode) {
    size_t size;

    if (runtime == NULL || runtime->transaction_counter != 0U ||
        !bounded_c_string(integration_mode,
            RUNTIME_INTEGRATION_MODE_SIZE, 1)) {
        return 0;
    }
    size = strlen(integration_mode);
    memcpy(runtime->integration_mode, integration_mode, size + 1U);
    return 1;
}

int msconnector_runtime_set_transaction_profile(
    msconnector_runtime *runtime,
    const msconnector_transaction_profile *profile) {
    if (runtime == NULL || profile == NULL || runtime->transaction_counter != 0U ||
        profile->profile_id == 0U || profile->connector_id == NULL ||
        profile->host_adapter_id == NULL || profile->direct_phase_mask == 0U ||
        (runtime->config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT &&
            profile->strict_post_commit_action == 0)) {
        return 0;
    }
    runtime->profile = profile;
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
    msconnector_secure_zero(runtime, sizeof(*runtime));
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

msconnector_body_limit_action msconnector_runtime_body_limit_action(
    const msconnector_runtime *runtime) {
    return runtime == NULL ? MSCONNECTOR_BODY_LIMIT_ACTION_UNSET
        : runtime->body_policy.body_limit_action;
}

msconnector_body_mode msconnector_runtime_request_body_mode(
    const msconnector_runtime *runtime) {
    return runtime == NULL ? MSCONNECTOR_BODY_MODE_NONE
        : runtime->body_policy.request_body_mode;
}

msconnector_body_mode msconnector_runtime_response_body_mode(
    const msconnector_runtime *runtime) {
    return runtime == NULL ? MSCONNECTOR_BODY_MODE_NONE
        : runtime->body_policy.response_body_mode;
}

enum msconnector_phase4_mode msconnector_runtime_phase4_mode(
    const msconnector_runtime *runtime) {
    return runtime == NULL ? MSCONNECTOR_PHASE4_MODE_UNSET
        : runtime->config.phase4_mode;
}

size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_total_header_bytes;
}

size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->limits.max_header_count;
}

int msconnector_runtime_error_log_enabled(const msconnector_runtime *runtime) {
    return runtime != NULL && runtime->config.use_error_log == MSCONNECTOR_BOOL_ON;
}

size_t msconnector_runtime_late_intervention_timeout_ms(
    const msconnector_runtime *runtime) {
    return runtime == NULL ? 0U : runtime->config.late_intervention_timeout_ms;
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

static int utc_calendar_time(time_t now, struct tm *utc) {
    if (utc == NULL) {
        return 0;
    }
#if defined(_POSIX_VERSION)
    return gmtime_r(&now, utc) != NULL;
#elif defined(_WIN32)
    return gmtime_s(utc, &now) == 0;
#else
    return gmtime_r(&now, utc) != NULL;
#endif
}

static void timestamp_now(char *buffer, size_t size) {
    time_t now = time(NULL);
    struct tm utc;
    if (buffer == NULL || size == 0U) {
        return;
    }
    buffer[0] = '\0';
    if (!utc_calendar_time(now, &utc)) {
        return;
    }
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

static int copy_event_metadata_slice(
    const char *source,
    size_t source_size,
    char *destination,
    size_t destination_size) {
    size_t source_index = 0U;
    size_t destination_index = 0U;
    size_t escaped_size = 0U;
    if (destination == NULL || destination_size == 0U) {
        return source != NULL && source_size > 0U;
    }
    destination[0] = '\0';
    if (source == NULL || source_size == 0U) {
        return 0;
    }
    while (source_index < source_size && source[source_index] != '\0') {
        size_t next_size = event_escape_size((unsigned char)source[source_index]);
        if (destination_index + 1U >= destination_size ||
            next_size > destination_size - 1U - escaped_size) {
            break;
        }
        destination[destination_index++] = source[source_index++];
        escaped_size += next_size;
    }
    destination[destination_index] = '\0';
    return source_index != source_size;
}

static void record_request_event_metadata(
    msconnector_runtime_transaction *transaction,
    const msconnector_request *request) {
    if (transaction == NULL || request == NULL) {
        return;
    }
    transaction->metadata.truncated |= copy_event_metadata(
        request->method, transaction->metadata.request_method,
        sizeof(transaction->metadata.request_method));
    transaction->metadata.truncated |= copy_event_metadata(request->uri,
        transaction->metadata.request_uri,
        sizeof(transaction->metadata.request_uri));
    transaction->metadata.truncated |= copy_event_metadata(
        request->client.address,
        transaction->metadata.request_client_ip,
        sizeof(transaction->metadata.request_client_ip));
}

static void record_response_event_metadata(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response) {
    const char *content_type = NULL;
    size_t content_type_size = 0U;
    if (transaction == NULL || response == NULL) {
        return;
    }
    transaction->response_original_status = response->status;
    (void)msconnector_headers_find_value_slice(response->headers,
        response->header_count, "content-type", &content_type,
        &content_type_size);
    transaction->metadata.truncated |= copy_event_metadata_slice(
        content_type, content_type_size,
        transaction->metadata.response_content_type,
        sizeof(transaction->metadata.response_content_type));
}

static void populate_event_body(
    msconnector_event *event,
    const msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision) {
    if (decision->phase == MSCONNECTOR_PHASE_REQUEST_BODY) {
        event->body.bytes_seen = transaction->request_body.bytes_seen;
        event->body.bytes_inspected = transaction->request_body.bytes_inspected;
        event->body.limit_outcome = msconnector_body_limit_outcome_name(
            transaction->request_body.limit_outcome);
        event->flags.body_truncated = transaction->request_body.truncated;
        return;
    }
    event->body.content_type = transaction->metadata.response_content_type;
    event->body.bytes_seen = transaction->response_body.bytes_seen;
    event->body.bytes_inspected = transaction->response_body.bytes_inspected;
    event->body.limit_outcome = msconnector_body_limit_outcome_name(
        transaction->response_body.limit_outcome);
    event->flags.body_truncated = transaction->response_body.truncated;
}

static void populate_event_response_state(
    msconnector_event *event,
    const msconnector_runtime_transaction *transaction) {
    event->flags.truncated = transaction->metadata.truncated ||
        event->flags.body_truncated;
    event->flags.response_started = transaction->response_headers_sent ||
        transaction->response_body_started;
    event->flags.response_committed = transaction->response_headers_sent;
    event->flags.headers_sent = transaction->response_headers_sent;
    event->flags.body_started = transaction->response_body_started;
    if (transaction->response_original_status != 0) {
        event->http.original_http_status = transaction->response_original_status;
        if (event->http.visible_http_status == 0) {
            event->http.visible_http_status = transaction->response_original_status;
        }
    }
}

static void populate_event_host_action(
    msconnector_event *event,
    const msconnector_runtime_host_action *host_action) {
    if (host_action == NULL) {
        return;
    }
    event->decision.actual_action = msconnector_decision_action_name(
        host_action->actual_action);
    if (host_action->visible_http_status != 0) {
        event->http.visible_http_status = host_action->visible_http_status;
    }
    event->http.transport_result = host_action->transport_result;
    event->flags.connection_aborted = host_action->connection_aborted != 0;
    event->protocol.stream_reset = host_action->actual_action ==
        MSCONNECTOR_DECISION_ACTION_STREAM_RESET;
}

static int write_event_jsonl(
    const msconnector_runtime *runtime,
    const msconnector_event *event,
    msconnector_error *error) {
    msconnector_allocator allocator;
    char *json = NULL;
    size_t json_size = runtime->limits.max_event_json_bytes + 2U;
    size_t written_size;
    int truncated = 0;

    msconnector_allocator_init(&allocator, json_size);
    if (!msconnector_alloc_checked(&allocator, json_size, (void **)&json)) {
        return runtime_error(error, MSCONNECTOR_ERROR_EVENT_TOO_LARGE,
            "event buffer allocation failed", "runtime");
    }
    (void)msconnector_event_write_jsonl_line(event, json, json_size, &truncated);
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
    msconnector_free_checked(&allocator, (void **)&json, json_size);
    return 1;
}

static int emit_decision_event(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    const msconnector_runtime_host_action *host_action,
    msconnector_error *error) {
    msconnector_runtime *runtime;
    msconnector_event event;
    char timestamp[RUNTIME_TIMESTAMP_SIZE];
    int success = 1;

    if (transaction == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "event input is required", "runtime");
    }
    runtime = transaction->runtime;
    if (runtime->event_file == NULL ||
        !msconnector_decision_to_event(decision, &event, runtime->connector_name,
            transaction->metadata.transaction_id)) {
        return 1;
    }
    runtime_operation_lock(runtime);
    timestamp_now(timestamp, sizeof(timestamp));
    event.meta.timestamp = timestamp;
    event.meta.event = event.meta.message_id;
    event.meta.integration_mode = runtime->integration_mode;
    event.flags.truncated = transaction->metadata.truncated;
    event.request.method = transaction->metadata.request_method;
    event.request.uri = transaction->metadata.request_uri;
    event.request.client_ip = transaction->metadata.request_client_ip;
    populate_event_body(&event, transaction, decision);
    populate_event_response_state(&event, transaction);
    if (decision->late_intervention) {
        event.flags.late_intervention_mode = phase4_mode_name(
            runtime->config.phase4_mode);
    }
    populate_event_host_action(&event, host_action);
    if (msconnector_flow_guard_next_sequence(&transaction->flow,
            &event.integrity.sequence) != MSCONNECTOR_FLOW_GUARD_OK) {
        success = runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "event sequence failed", "runtime");
    } else {
        event.integrity.previous_hash = runtime->previous_event_hash;
        event.integrity.event_hash = msconnector_integrity_event_hash(
            &event, event.integrity.previous_hash);
        if (!write_event_jsonl(runtime, &event, error)) {
            success = 0;
        } else {
            runtime->previous_event_hash = event.integrity.event_hash;
        }
    }
    runtime_operation_unlock(runtime);
    return success;
}

static const char *contract_terminal_message_id(
    const msconnector_transaction_contract *contract) {
    msconnector_transaction_decision_kind kind;

    if (contract == NULL) return MSCONN_EVENT_CONNECTOR_ERROR;
    if (contract->error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT) {
        return MSCONN_EVENT_BODY_LIMIT;
    }
    kind = contract->engine_decision;
    switch (kind) {
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT:
        return MSCONN_EVENT_ENGINE_TIMEOUT;
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE:
        return MSCONN_EVENT_ENGINE_UNAVAILABLE;
    case MSCONNECTOR_TRANSACTION_DECISION_INVALID_ENGINE_RESPONSE:
        return MSCONN_EVENT_INVALID_ENGINE_RESPONSE;
    case MSCONNECTOR_TRANSACTION_DECISION_PROTOCOL_ERROR:
        return MSCONN_EVENT_PROTOCOL_ERROR;
    case MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL:
        return MSCONN_EVENT_CLIENT_CANCEL;
    case MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT:
        return MSCONN_EVENT_UPSTREAM_DISCONNECT;
    case MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR:
    default:
        return MSCONN_EVENT_CONNECTOR_ERROR;
    }
}

static enum msconnector_phase contract_terminal_phase(
    const msconnector_transaction_contract *contract) {
    if (contract != NULL && contract->active_phase >= MSCONNECTOR_PHASE_REQUEST_HEADERS &&
        contract->active_phase <= MSCONNECTOR_PHASE_RESPONSE_BODY) {
        return (enum msconnector_phase)contract->active_phase;
    }
    if (contract != NULL && contract->last_completed_phase >=
            MSCONNECTOR_PHASE_REQUEST_HEADERS &&
        contract->last_completed_phase <= MSCONNECTOR_PHASE_RESPONSE_BODY) {
        return (enum msconnector_phase)contract->last_completed_phase;
    }
    return MSCONNECTOR_PHASE_CONNECTION;
}

static int contract_terminal_http_status(
    const msconnector_transaction_contract *contract) {
    msconnector_transaction_decision_kind kind = contract == NULL ?
        MSCONNECTOR_TRANSACTION_DECISION_CONNECTOR_ERROR : contract->engine_decision;

    if (contract != NULL &&
        contract->error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT) {
        return 413;
    }
    switch (kind) {
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT:
        return 504;
    case MSCONNECTOR_TRANSACTION_DECISION_ENGINE_UNAVAILABLE:
        return 503;
    case MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL:
    case MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT:
        return 0;
    default:
        return MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }
}

/* Contract-originated terminal outcomes do not necessarily originate as an
 * engine intervention, but they still require the same bounded, integrity
 * chained JSONL event as a rule decision. */
static int emit_contract_terminal_event(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    msconnector_runtime *runtime;
    msconnector_transaction_decision_policy policy;
    msconnector_event event;
    msconnector_decision body_decision;
    const char *message_id;
    const char *message;
    char timestamp[RUNTIME_TIMESTAMP_SIZE];
    int success = 1;

    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "terminal event transaction is required", "runtime");
    }
    if (transaction->terminal_event_emitted) {
        return 1;
    }
    runtime = transaction->runtime;
    if (!msconnector_transaction_contract_decision_policy(&transaction->contract,
            transaction->contract.engine_decision, &policy)) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "terminal event decision policy is unavailable", "runtime");
    }
    if (runtime->event_file == NULL) {
        transaction->terminal_event_emitted = 1;
        return 1;
    }
    message_id = contract_terminal_message_id(&transaction->contract);
    message = msconnector_event_default_message(message_id);
    msconnector_event_init(&event);
    msconnector_decision_init(&body_decision);
    body_decision.phase = contract_terminal_phase(&transaction->contract);
    timestamp_now(timestamp, sizeof(timestamp));
    event.meta.timestamp = timestamp;
    event.meta.message_id = message_id;
    event.meta.message = message;
    event.meta.event = policy.event_type;
    event.meta.level = msconnector_event_default_level(message_id);
    event.meta.connector = runtime->connector_name;
    event.meta.integration_mode = runtime->integration_mode;
    event.meta.transaction_id = transaction->metadata.transaction_id;
    event.decision.phase = body_decision.phase;
    event.decision.status = policy.host_action == MSCONNECTOR_DECISION_ACTION_LOG_ONLY ?
        MSCONNECTOR_STATUS_ERROR : MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = msconnector_decision_action_name(policy.host_action);
    event.decision.requested_action = event.decision.action;
    event.decision.actual_action = event.decision.action;
    event.decision.rule_id = transaction->contract.rule_id;
    event.decision.reason = message;
    event.http.http_status = contract_terminal_http_status(&transaction->contract);
    event.http.http_reason_phrase = msconnector_http_status_reason_phrase(
        event.http.http_status);
    event.http.http_default_message = msconnector_http_status_default_message(
        event.http.http_status);
    event.flags.timeout_stage = transaction->contract.engine_decision ==
        MSCONNECTOR_TRANSACTION_DECISION_ENGINE_TIMEOUT ? "transaction" : NULL;
    event.flags.client_disconnected = transaction->contract.engine_decision ==
        MSCONNECTOR_TRANSACTION_DECISION_CLIENT_CANCEL;
    event.flags.upstream_disconnected = transaction->contract.engine_decision ==
        MSCONNECTOR_TRANSACTION_DECISION_UPSTREAM_DISCONNECT;
    event.flags.cancelled = event.flags.client_disconnected ||
        event.flags.upstream_disconnected;
    populate_event_body(&event, transaction, &body_decision);
    populate_event_response_state(&event, transaction);

    runtime_operation_lock(runtime);
    if (msconnector_flow_guard_next_sequence(&transaction->flow,
            &event.integrity.sequence) != MSCONNECTOR_FLOW_GUARD_OK) {
        success = runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "terminal event sequence failed", "runtime");
    } else {
        event.integrity.previous_hash = runtime->previous_event_hash;
        event.integrity.event_hash = msconnector_integrity_event_hash(
            &event, event.integrity.previous_hash);
        if (!write_event_jsonl(runtime, &event, error)) {
            success = 0;
        } else {
            runtime->previous_event_hash = event.integrity.event_hash;
            transaction->terminal_event_emitted = 1;
        }
    }
    runtime_operation_unlock(runtime);
    return success;
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

static int begin_contract_phase(
    msconnector_runtime_transaction *transaction,
    enum msconnector_phase phase,
    msconnector_error *error) {
    int result = msconnector_transaction_contract_begin_phase(&transaction->contract,
        phase, transaction_now_ms());

    return result == MSCONNECTOR_TRANSACTION_TRANSITION_OK ? 1 :
        contract_error(error, result, NULL);
}

static int begin_companion_contract_phase(
    msconnector_runtime_transaction *transaction,
    enum msconnector_phase phase,
    msconnector_error *error) {
    int result = msconnector_transaction_contract_begin_companion_phase(
        &transaction->contract, phase, transaction_now_ms());

    return result == MSCONNECTOR_TRANSACTION_TRANSITION_OK ? 1 :
        contract_error(error, result, NULL);
}

/* P2 and P4 remain active while a streaming host supplies successive data
 * chunks.  Beginning the same phase for each chunk would turn every second
 * chunk into a duplicate-phase violation instead of preserving the one phase
 * through its explicit EOS finalizer. */
static int begin_or_resume_streaming_body_phase(
    msconnector_runtime_transaction *transaction,
    enum msconnector_phase phase,
    int companion,
    msconnector_error *error) {
    if (transaction->contract.active_phase == (int)phase) {
        return 1;
    }
    return companion ? begin_companion_contract_phase(transaction, phase, error) :
        begin_contract_phase(transaction, phase, error);
}

static int complete_contract_phase(
    msconnector_runtime_transaction *transaction,
    enum msconnector_phase phase,
    msconnector_error *error) {
    int result = msconnector_transaction_contract_complete_phase(&transaction->contract,
        phase, transaction_now_ms());

    return result == MSCONNECTOR_TRANSACTION_TRANSITION_OK ? 1 :
        contract_error(error, result, NULL);
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
    if (!emit_decision_event(transaction, decision, NULL, error)) {
        return 0;
    }
    /* The regular disruptive decision already emitted the authoritative
     * terminal event. Prevent transaction_finish() from adding a synthetic
     * connector-error event for the same decision. */
    if (msconnector_transaction_contract_is_terminal(&transaction->contract)) {
        transaction->terminal_event_emitted = 1;
    }
    *terminal = 1;
    return 1;
}

static int abort_transaction_begin(
    msconnector_runtime_transaction **transaction) {
    msconnector_runtime_transaction_destroy(transaction);
    return 0;
}

static void set_invalid_request_decision(
    const msconnector_runtime *runtime,
    msconnector_decision *decision,
    const msconnector_error *error) {
    msconnector_decision_set_error(decision,
        msconnector_runtime_error_http_status(runtime,
            error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code),
        error == NULL ? "invalid request" : error->message);
}

static int validate_transaction_begin_request(
    const msconnector_runtime *runtime,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_request headers_only;

    if (!validate_request_input(request, error)) {
        set_invalid_request_decision(runtime, decision, error);
        return 0;
    }
    headers_only = *request;
    headers_only.body.data = NULL;
    headers_only.body.size = 0U;
    if (!msconnector_dos_guard_check_request(&headers_only, &runtime->limits,
            error)) {
        set_invalid_request_decision(runtime, decision, error);
        return 0;
    }
    return 1;
}

static msconnector_runtime_transaction *create_runtime_transaction(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;
    msconnector_transaction_id_context id_context;
    msconnector_transaction_id_result id_result;
    const msconnector_transaction_profile *profile;
    char fallback_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    char contract_host_id[MSCONNECTOR_TRANSACTION_CONTRACT_HOST_ID_SIZE];

    transaction = calloc(1U, sizeof(*transaction));
    if (transaction == NULL) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction allocation failed", "runtime");
        return NULL;
    }
    transaction->runtime = runtime;
    record_request_event_metadata(transaction, request);
    runtime_operation_lock(runtime);
    ++runtime->transaction_counter;
    (void)snprintf(fallback_id, sizeof(fallback_id), "%s-%lu",
        runtime->connector_name, runtime->transaction_counter);
    runtime_operation_unlock(runtime);
    memset(&id_context, 0, sizeof(id_context));
    id_context.config = &runtime->config;
    id_context.request = request;
    id_context.host_request_id = string_is_empty(host_request_id) ? NULL : host_request_id;
    id_context.fallback_id = fallback_id;
    id_context.header_name = runtime->owned.transaction_id_header;
    if (!msconnector_transaction_id_resolve(&id_context, &id_result, error) ||
        !msconnector_transaction_id_copy(id_result.value,
            transaction->metadata.transaction_id,
            sizeof(transaction->metadata.transaction_id))) {
        free(transaction);
        return NULL;
    }
    profile = runtime->profile;
    /* A named integration mode represents one of the host-facing contract
     * routes.  Do not silently fall back to the permissive generic profile
     * when a connector advertises an unknown or misspelled route: that would
     * make phase/capability enforcement connector-dependent.  The generic
     * Common embedding intentionally remains available only when no route
     * was selected at setup time. */
    if (profile == NULL) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_CAPABILITY,
            "integration mode has no canonical transaction-contract profile",
            "transaction_contract");
        msconnector_secure_zero(transaction, sizeof(*transaction));
        free(transaction);
        return NULL;
    }
    if (!contract_host_id_for_request(runtime, profile, request, contract_host_id)) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "host instance ID is invalid or exceeds the canonical bound", "runtime");
        msconnector_secure_zero(transaction, sizeof(*transaction));
        free(transaction);
        return NULL;
    }
    if (msconnector_transaction_contract_init(&transaction->contract, profile,
            transaction->metadata.transaction_id, runtime->connector_name,
            contract_host_id,
            runtime->config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT ?
                MSCONNECTOR_TRANSACTION_MODE_STRICT : MSCONNECTOR_TRANSACTION_MODE_SAFE,
            transaction_now_ms()) != MSCONNECTOR_TRANSACTION_TRANSITION_OK ||
        msconnector_transaction_contract_record_request_metadata(&transaction->contract,
            request->method, request->uri, NULL, request->header_count,
            header_bytes(request->headers, request->header_count),
            runtime->body_policy.request_body_limit) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "shared transaction contract initialization failed", "runtime");
        msconnector_secure_zero(transaction, sizeof(*transaction));
        free(transaction);
        return NULL;
    }
    msconnector_flow_guard_init(&transaction->flow, transaction->metadata.transaction_id);
    return transaction;
}

static int process_transaction_connection(
    msconnector_runtime_transaction *transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    int *terminal,
    msconnector_error *error) {
    int processed;

    runtime_operation_lock(transaction->runtime);
    processed = msconnector_modsecurity_process_connection(
        &transaction->modsecurity, request, decision, error);
    runtime_operation_unlock(transaction->runtime);
    if (!processed ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_CONNECTION, error) ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_URI, error)) {
        return 0;
    }
    return handle_decision(transaction, decision, error, terminal);
}

static int process_transaction_request_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    int *terminal,
    msconnector_error *error) {
    int processed;

    runtime_operation_lock(transaction->runtime);
    processed = msconnector_modsecurity_process_request_headers(
        &transaction->modsecurity, request, decision, error);
    runtime_operation_unlock(transaction->runtime);
    if (!processed ||
        !mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_HEADERS, error)) {
        return 0;
    }
    return handle_decision(transaction, decision, error, terminal);
}

static int begin_request_body_processing(
    msconnector_runtime_transaction *transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    const msconnector_runtime *runtime = transaction->runtime;

    if (runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_NONE) {
        if (request->body.size > 0U) {
            (void)runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
                "request body is disabled", "runtime");
            return 0;
        }
        return msconnector_runtime_transaction_finish_request_body(
            transaction, decision, error);
    }
    if (runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_BUFFERED) {
        return msconnector_runtime_transaction_append_request_body_chunk(
                   transaction, request->body.data, request->body.size, error) &&
            msconnector_runtime_transaction_finish_request_body(
                transaction, decision, error);
    }
    return msconnector_runtime_transaction_append_request_body_chunk(
        transaction, request->body.data, request->body.size, error);
}

static int begin_native_transaction(
    msconnector_runtime_transaction *transaction,
    const msconnector_request *request,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime *runtime = transaction->runtime;
    int terminal;

    if (runtime->config.enable != MSCONNECTOR_BOOL_ON) {
        /* Disabled rule evaluation does not remove the lifecycle contract.
         * Keep the same observed P1/P2 route so a later response callback,
         * cleanup, or host diagnostic cannot silently use a different phase
         * model merely because the engine was disabled. */
        if (!mark_flow(transaction, MSCONNECTOR_PHASE_CONNECTION, error) ||
            !mark_flow(transaction, MSCONNECTOR_PHASE_URI, error) ||
            !begin_contract_phase(transaction,
                MSCONNECTOR_PHASE_REQUEST_HEADERS, error) ||
            !complete_contract_phase(transaction,
                MSCONNECTOR_PHASE_REQUEST_HEADERS, error) ||
            !mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_HEADERS, error)) {
            return 0;
        }
        return begin_request_body_processing(transaction, request, decision, error);
    }
    runtime_operation_lock(runtime);
    const int initialized = msconnector_modsecurity_transaction_init(
        &transaction->modsecurity, &runtime->engine,
        transaction->metadata.transaction_id, error);
    runtime_operation_unlock(runtime);
    if (!initialized) {
        return 0;
    }
    msconnector_modsecurity_transaction_bind_contract(&transaction->modsecurity,
        &transaction->contract);
    transaction->native_started = 1;
    if (!process_transaction_connection(transaction, request, decision,
            &terminal, error)) {
        return 0;
    }
    if (terminal) {
        return 1;
    }
    if (!process_transaction_request_headers(transaction, request, decision,
            &terminal, error)) {
        return 0;
    }
    if (terminal) {
        return 1;
    }
    return begin_request_body_processing(transaction, request, decision, error);
}

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;

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
    if (!validate_transaction_begin_request(runtime, request, decision, error)) {
        return 0;
    }
    transaction = create_runtime_transaction(runtime, request, host_request_id, error);
    if (transaction == NULL) {
        return 0;
    }
    *out = transaction;
    if (!begin_native_transaction(transaction, request, decision, error)) {
        return abort_transaction_begin(out);
    }
    return 1;
}

static int apply_body_limit_plan(
    msconnector_runtime_body_progress *progress,
    const msconnector_body_policy *body_policy,
    size_t body_limit,
    size_t chunk_size,
    size_t *append_size,
    msconnector_error *error,
    const char *label) {
    msconnector_body_limit_plan plan;
    int accepted;

    if (progress == NULL || body_policy == NULL || append_size == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "body progress storage is required", "runtime");
    }
    accepted = msconnector_body_limit_plan_chunk(progress->bytes_seen,
        progress->bytes_inspected, body_limit,
        body_policy->body_limit_action, chunk_size, &plan);
    progress->bytes_seen = plan.bytes_seen;
    progress->truncated |= plan.truncated;
    progress->limit_outcome = plan.outcome;
    *append_size = plan.append_size;
    if (!accepted) {
        return runtime_error(error, MSCONNECTOR_ERROR_BODY_TOO_LARGE,
            label, "runtime");
    }
    return 1;
}

int msconnector_runtime_transaction_append_request_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    const msconnector_runtime *runtime;
    size_t append_size;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    runtime = transaction->runtime;
    if (transaction->finish_attempted || transaction->request_body.finished) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "request body append after finalization is not allowed", "runtime");
    }
    if (size > 0U && data == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "request body data is required when size is nonzero", "runtime");
    }
    if (runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_NONE) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "request body is disabled", "runtime");
        return 0;
    }
    if (!msconnector_transaction_contract_can_append_body(&transaction->contract, 0)) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE,
            "request body append is outside P2");
    }
    if (!apply_body_limit_plan(&transaction->request_body, &runtime->body_policy,
            runtime->body_policy.request_body_limit, size, &append_size, error,
            "request body exceeds configured limit")) {
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, transaction_now_ms());
        transaction->request_blocked = 1;
        return 0;
    }
    if (append_size > 0U &&
        !begin_or_resume_streaming_body_phase(transaction,
            MSCONNECTOR_PHASE_REQUEST_BODY, 0, error)) {
        return 0;
    }
    if (append_size > 0U &&
        msconnector_transaction_contract_record_body(&transaction->contract, 0,
            append_size) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_INVALID,
            "request body metadata update failed");
    }
    if (append_size > 0U && runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        !transaction->request_blocked &&
        !append_request_body_to_engine(transaction, data, append_size, error)) {
        return 0;
    }
    if (append_size > 0U && runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        !transaction->request_blocked) {
        transaction->request_body.bytes_inspected += append_size;
    }
    return 1;
}

int msconnector_runtime_transaction_finish_request_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    const msconnector_runtime *runtime;
    int terminal;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction and decision are required", "runtime");
    }
    runtime = transaction->runtime;
    msconnector_decision_set_allow(decision);
    if (transaction->finish_attempted || transaction->request_body.finished) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "request body may only be finalized once", "runtime");
    }
    if (transaction->request_blocked) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "request body finalization after a terminal decision is not allowed");
    }
    if (runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        !transaction->request_blocked &&
        !finish_request_body_in_engine(transaction, decision, error)) {
        return 0;
    }
    if (runtime->config.enable != MSCONNECTOR_BOOL_ON &&
        ((transaction->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&
          !begin_contract_phase(transaction, MSCONNECTOR_PHASE_REQUEST_BODY, error)) ||
         !complete_contract_phase(transaction, MSCONNECTOR_PHASE_REQUEST_BODY, error))) {
        return 0;
    }
    transaction->request_body.finished = 1;
    if (!mark_flow(transaction, MSCONNECTOR_PHASE_REQUEST_BODY, error)) {
        return 0;
    }
    return handle_decision(transaction, decision, error, &terminal);
}

static int process_response_headers_in_engine(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error,
    int companion) {
    msconnector_runtime *runtime = transaction_mutable_runtime(transaction);
    int processed;

    runtime_operation_lock(runtime);
    if (companion) {
        processed = msconnector_modsecurity_process_response_headers_companion(
            &transaction->modsecurity, response, decision, error);
    } else {
        processed = msconnector_modsecurity_process_response_headers(
            &transaction->modsecurity, response, decision, error);
    }
    runtime_operation_unlock(runtime);
    return processed;
}

static int validate_and_record_response_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    const msconnector_runtime *runtime = transaction->runtime;
    msconnector_response headers_only = *response;
    int status;

    headers_only.body.data = NULL;
    headers_only.body.size = 0U;
    if (!validate_response_input(response, error) ||
        !msconnector_dos_guard_check_response(&headers_only, &runtime->limits,
            error)) {
        status = msconnector_runtime_error_http_status(runtime,
            error == NULL ? MSCONNECTOR_ERROR_INTERNAL : error->code);
        msconnector_decision_set_error(decision, status,
            error == NULL ? "invalid response" : error->message);
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR, transaction_now_ms());
        return 0;
    }
    record_response_event_metadata(transaction, response);
    if (msconnector_transaction_contract_record_response_metadata(
            &transaction->contract, response->status, NULL,
            response->header_count,
            header_bytes(response->headers, response->header_count),
            runtime->body_policy.response_body_limit) !=
            MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_INVALID,
            "response metadata violates the shared transaction contract");
    }
    return 1;
}

static int process_response_headers_phase(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error,
    int companion) {
    const msconnector_runtime *runtime = transaction->runtime;

    if (runtime->config.enable == MSCONNECTOR_BOOL_ON) {
        return process_response_headers_in_engine(transaction, response, decision,
                error, companion) &&
            mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_HEADERS, error);
    }
    if (companion ? !begin_companion_contract_phase(transaction,
                MSCONNECTOR_PHASE_RESPONSE_HEADERS, error) :
            !begin_contract_phase(transaction,
                MSCONNECTOR_PHASE_RESPONSE_HEADERS, error)) {
        return 0;
    }
    return complete_contract_phase(transaction,
        MSCONNECTOR_PHASE_RESPONSE_HEADERS, error) &&
        mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_HEADERS, error);
}

static int process_response_headers_internal(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error,
    int companion) {
    int terminal;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL ||
        response == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction, response and decision are required", "runtime");
    }
    msconnector_decision_set_allow(decision);
    if (transaction->finish_attempted || transaction->response_headers_processed ||
        (companion && !transaction->response_companion_handed_off) ||
        (!companion && transaction->response_companion_handed_off)) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response headers use an invalid response-companion route", "runtime");
    }
    if (transaction->request_blocked) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "response headers after a terminal decision are not allowed");
    }
    if (!validate_and_record_response_headers(transaction, response, decision, error) ||
        !process_response_headers_phase(transaction, response, decision, error,
            companion)) {
        return 0;
    }
    transaction->response_headers_processed = 1;
    return handle_decision(transaction, decision, error, &terminal);
}

int msconnector_runtime_transaction_process_response_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    return process_response_headers_internal(transaction, response, decision, error, 0);
}

static int process_companion_response_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    return process_response_headers_internal(transaction, response, decision, error, 1);
}

static int append_response_body_to_engine(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t append_size,
    msconnector_error *error,
    int companion) {
    msconnector_runtime *runtime = transaction_mutable_runtime(transaction);
    int appended;

    if (append_size == 0U || runtime->config.enable != MSCONNECTOR_BOOL_ON ||
        transaction->request_blocked) {
        return 1;
    }
    runtime_operation_lock(runtime);
    appended = companion ? msconnector_modsecurity_append_response_body_companion(
            &transaction->modsecurity, data, append_size, error) :
        msconnector_modsecurity_append_response_body(
            &transaction->modsecurity, data, append_size, error);
    runtime_operation_unlock(runtime);
    return appended;
}

static int validate_response_body_append(
    const msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error,
    int companion) {
    const msconnector_runtime *runtime = transaction->runtime;

    if (transaction->finish_attempted || transaction->response_body.finished ||
        (companion && !transaction->response_companion_handed_off) ||
        (!companion && transaction->response_companion_handed_off)) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response body append uses an invalid response-companion route", "runtime");
    }
    if (!transaction->response_headers_processed) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response headers must be processed before response body chunks",
            "runtime");
    }
    if (transaction->request_blocked) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "response body append after a terminal decision is not allowed");
    }
    if (size > 0U && data == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "response body data is required when size is nonzero", "runtime");
    }
    if (runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_NONE &&
        !companion) {
        return runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "response body is disabled", "runtime");
    }
    if (!msconnector_transaction_contract_can_append_body(&transaction->contract, 1)) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_LATE_PHASE,
            "response body append is outside P4");
    }
    return 1;
}

static int append_response_body_chunk_internal(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error,
    int companion) {
    const msconnector_runtime *runtime;
    size_t append_size;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    runtime = transaction->runtime;
    /* A direct host configured with response_body_mode=none has no decoded
     * entity-body stream, so it can only close the contract.  A response
     * companion, however, exists specifically to observe P4; it must still
     * deliver the zero-length EOS to the native engine even when there were
     * no chunks. */
    if (!validate_response_body_append(transaction, data, size, error, companion)) {
        return 0;
    }
    if (!apply_body_limit_plan(&transaction->response_body, &runtime->body_policy,
            runtime->body_policy.response_body_limit, size, &append_size, error,
            "response body exceeds configured limit")) {
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT, transaction_now_ms());
        transaction->request_blocked = 1;
        return 0;
    }
    if (append_size > 0U &&
        !begin_or_resume_streaming_body_phase(transaction,
            MSCONNECTOR_PHASE_RESPONSE_BODY, companion, error)) {
        return 0;
    }
    if (append_size > 0U &&
        msconnector_transaction_contract_record_body(&transaction->contract, 1,
            append_size) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_INVALID,
            "response body metadata update failed");
    }
    if (!append_response_body_to_engine(transaction, data, append_size, error,
            companion)) {
        return 0;
    }
    if (append_size > 0U && runtime->config.enable == MSCONNECTOR_BOOL_ON &&
        !transaction->request_blocked) {
        transaction->response_body.bytes_inspected += append_size;
    }
    return 1;
}

int msconnector_runtime_transaction_append_response_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    return append_response_body_chunk_internal(transaction, data, size, error, 0);
}

static int append_companion_response_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    return append_response_body_chunk_internal(transaction, data, size, error, 1);
}

static int begin_response_body_phase(
    msconnector_runtime_transaction *transaction,
    int companion,
    msconnector_error *error) {
    return companion ? begin_companion_contract_phase(transaction,
                MSCONNECTOR_PHASE_RESPONSE_BODY, error) :
        begin_contract_phase(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error);
}

static int finish_response_body_in_engine(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error,
    int companion) {
    msconnector_runtime *runtime = transaction_mutable_runtime(transaction);
    int finished;

    if (runtime->config.enable != MSCONNECTOR_BOOL_ON ||
        transaction->request_blocked) {
        return 1;
    }
    runtime_operation_lock(runtime);
    finished = companion ? msconnector_modsecurity_finish_response_body_companion(
            &transaction->modsecurity, decision, error) :
        msconnector_modsecurity_finish_response_body(
            &transaction->modsecurity, decision, error);
    runtime_operation_unlock(runtime);
    return finished;
}

static int finish_response_body_internal(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error,
    int companion) {
    const msconnector_runtime *runtime;
    int terminal;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction and decision are required", "runtime");
    }
    runtime = transaction->runtime;
    msconnector_decision_set_allow(decision);
    if (transaction->finish_attempted || transaction->response_body.finished ||
        (companion && !transaction->response_companion_handed_off) ||
        (!companion && transaction->response_companion_handed_off)) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response body finalization uses an invalid response-companion route", "runtime");
    }
    if (!transaction->response_headers_processed) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response headers must be processed before response body finalization",
            "runtime");
    }
    if (transaction->request_blocked) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "response body finalization after a terminal decision is not allowed");
    }
    /* A direct host configured with response_body_mode=none has no decoded
     * entity-body stream, so it can only close the contract. A response
     * companion exists to observe P4 and must deliver its zero-length EOS to
     * the native engine even when no body chunks were received. */
    if (runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_NONE &&
        !companion) {
        if (!begin_response_body_phase(transaction, companion, error) ||
            !complete_contract_phase(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error)) {
            return 0;
        }
        transaction->response_body.finished = 1;
        return mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error);
    }
    if (!finish_response_body_in_engine(transaction, decision, error, companion)) {
        return 0;
    }
    if (runtime->config.enable != MSCONNECTOR_BOOL_ON &&
        ((transaction->contract.active_phase != MSCONNECTOR_PHASE_RESPONSE_BODY &&
          !begin_response_body_phase(transaction, companion, error)) ||
         !complete_contract_phase(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error))) {
        return 0;
    }
    transaction->response_body.finished = 1;
    if (!mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error)) {
        return 0;
    }
    return handle_decision(transaction, decision, error, &terminal);
}

int msconnector_runtime_transaction_finish_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    return finish_response_body_internal(transaction, decision, error, 0);
}

static int finish_companion_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error) {
    return finish_response_body_internal(transaction, decision, error, 1);
}

int msconnector_runtime_transaction_finish_unobserved_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    const msconnector_runtime *runtime;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    runtime = transaction->runtime;
    if (transaction->finish_attempted || transaction->response_body.finished) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "unobserved response body may only be finalized once", "runtime");
    }
    if (!transaction->response_headers_processed) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response headers must be processed before unobserved response completion",
            "runtime");
    }
    if (runtime->body_policy.response_body_mode != MSCONNECTOR_BODY_MODE_NONE) {
        return runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "unobserved response completion requires response_body_mode=none",
            "runtime");
    }
    if (transaction->request_blocked ||
        !begin_contract_phase(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error) ||
        !complete_contract_phase(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error)) {
        return transaction->request_blocked ?
            contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
                "unobserved response completion after a terminal decision is not allowed") : 0;
    }
    transaction->response_body.finished = 1;
    return mark_flow(transaction, MSCONNECTOR_PHASE_RESPONSE_BODY, error);
}

int msconnector_runtime_transaction_set_response_commit_state_checked(
    msconnector_runtime_transaction *transaction,
    int headers_sent,
    int body_started,
    msconnector_error *error) {
    int result;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    if (transaction->finish_attempted || transaction->finished) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "response commit after transaction finish is not allowed");
    }
    if ((transaction->response_headers_sent && headers_sent == 0) ||
        (transaction->response_body_started && body_started == 0)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "response commitment state must be monotonic", "runtime");
    }
    result = msconnector_transaction_contract_set_response_committed(
        &transaction->contract, headers_sent != 0 || body_started != 0);
    if (result != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, result,
            "response commit must follow a completed P3");
    }
    transaction->response_headers_sent = headers_sent != 0;
    transaction->response_body_started = body_started != 0;
    transaction->modsecurity.state.response_headers_committed =
        transaction->response_headers_sent;
    transaction->modsecurity.state.response_body_started =
        transaction->response_body_started;
    return 1;
}

void msconnector_runtime_transaction_set_response_commit_state(
    msconnector_runtime_transaction *transaction,
    int headers_sent,
    int body_started) {
    msconnector_error ignored;

    msconnector_error_init(&ignored);
    if (!msconnector_runtime_transaction_set_response_commit_state_checked(transaction,
            headers_sent, body_started, &ignored) && transaction != NULL) {
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE, transaction_now_ms());
    }
}

int msconnector_runtime_transaction_record_host_action(
    msconnector_runtime_transaction *transaction,
    const msconnector_decision *decision,
    msconnector_decision_action actual_action,
    int visible_http_status,
    const char *transport_result,
    int connection_aborted,
    msconnector_error *error) {
    msconnector_runtime_host_action host_action;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction and disruptive decision are required", "runtime");
    }
    if (transaction->finish_attempted || transaction->finished) {
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_AFTER_TERMINAL,
            "host action after transaction finish is not allowed");
    }
    if (!msconnector_decision_is_disruptive(decision)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a host outcome requires a disruptive engine decision", "runtime");
    }
    if (transaction->host_action_event_emitted) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "host action may only be recorded once", "runtime");
    }
    if (!valid_host_action(actual_action) ||
        !bounded_c_string(transport_result, 64U, 1) ||
        !valid_host_transport_result(transport_result)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "host action metadata is invalid or not bounded", "runtime");
    }
    if (visible_http_status != 0 &&
        !msconnector_http_status_is_valid(visible_http_status)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "visible HTTP status is invalid", "runtime");
    }
    if (visible_http_status == 0 && !connection_aborted &&
        actual_action != MSCONNECTOR_DECISION_ACTION_STREAM_RESET) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a non-abort host action requires a visible HTTP status", "runtime");
    }
    if (connection_aborted &&
        actual_action != MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION &&
        actual_action != MSCONNECTOR_DECISION_ACTION_DROP) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a connection abort requires an abort or drop host action", "runtime");
    }
    if (actual_action == MSCONNECTOR_DECISION_ACTION_STREAM_RESET &&
        connection_aborted) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a stream reset must not be reported as a connection abort", "runtime");
    }
    if (actual_action == MSCONNECTOR_DECISION_ACTION_STREAM_RESET &&
        strcmp(transport_result, "stream_reset") != 0) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a stream reset requires transport_result=stream_reset", "runtime");
    }
    if (strcmp(transport_result, "stream_reset") == 0 &&
        actual_action != MSCONNECTOR_DECISION_ACTION_STREAM_RESET) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "transport_result=stream_reset requires a stream-reset action", "runtime");
    }
    if (msconnector_decision_is_body_limit(decision) &&
        (actual_action != MSCONNECTOR_DECISION_ACTION_DENY ||
         visible_http_status != 413 || connection_aborted ||
         strcmp(transport_result, "http_status") != 0)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a body-limit decision requires an HTTP 413 deny action", "runtime");
    }
    host_action.actual_action = actual_action;
    host_action.visible_http_status = visible_http_status;
    host_action.transport_result = transport_result;
    host_action.connection_aborted = connection_aborted != 0;
    if (!emit_decision_event(transaction, decision, &host_action, error)) {
        return 0;
    }
    transaction->host_action_event_emitted = 1;
    return 1;
}

int msconnector_runtime_transaction_record_failure_host_action(
    msconnector_runtime_transaction *transaction,
    int visible_http_status,
    int connection_aborted,
    msconnector_error *error) {
    msconnector_decision decision;
    const char *reason;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || transaction->runtime == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    if (transaction->contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE ||
        (visible_http_status == 0 && !connection_aborted)) {
        return runtime_error(error, MSCONNECTOR_ERROR_HOST_API_FAILURE,
            "a typed terminal failure and an observed host action are required",
            "runtime");
    }
    reason = msconnector_transaction_error_class_name(
        transaction->contract.error_class);
    if (connection_aborted) {
        msconnector_decision_set_connection_abort(&decision, NULL, reason);
    } else {
        msconnector_decision_set_error(&decision, visible_http_status, reason);
    }
    decision.phase = contract_terminal_phase(&transaction->contract);
    return msconnector_runtime_transaction_record_host_action(transaction,
        &decision,
        connection_aborted ? MSCONNECTOR_DECISION_ACTION_ABORT_CONNECTION :
            MSCONNECTOR_DECISION_ACTION_DENY,
        connection_aborted ? 0 : visible_http_status,
        connection_aborted ? "connection_aborted" : "http_status",
        connection_aborted, error);
}

int msconnector_runtime_transaction_cancel(
    msconnector_runtime_transaction *transaction,
    int upstream_disconnect,
    msconnector_error *error) {
    int result;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    result = msconnector_transaction_contract_cancel(&transaction->contract,
        upstream_disconnect, transaction_now_ms());
    if (result != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, result, "transaction cancel violates the shared contract");
    }
    transaction->request_blocked = 1;
    return emit_contract_terminal_event(transaction, error);
}

int msconnector_runtime_transaction_timeout(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    int result;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    result = msconnector_transaction_contract_timeout(&transaction->contract,
        transaction_now_ms());
    if (result != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, result, "transaction timeout violates the shared contract");
    }
    transaction->request_blocked = 1;
    return emit_contract_terminal_event(transaction, error);
}

int msconnector_runtime_transaction_fail(
    msconnector_runtime_transaction *transaction,
    msconnector_transaction_error_class error_class,
    msconnector_error *error) {
    int result;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    result = msconnector_transaction_contract_fail(&transaction->contract,
        error_class, transaction_now_ms());
    if (result != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, result,
            "transaction failure violates the shared contract");
    }
    transaction->request_blocked = 1;
    return emit_contract_terminal_event(transaction, error);
}

static void response_companion_registry_lock(
    msconnector_runtime_response_companion_registry *registry) {
    while (atomic_flag_test_and_set_explicit(&registry->lock,
            memory_order_acquire)) {
        /* The registry has a fixed upper bound and never invokes a host
         * callback while waiting for this ownership lock. */
        (void)sched_yield();
    }
}

static void response_companion_registry_unlock(
    msconnector_runtime_response_companion_registry *registry) {
    atomic_flag_clear_explicit(&registry->lock, memory_order_release);
}

static void response_companion_clear_entry(
    msconnector_runtime_response_companion_entry *entry) {
    if (entry != NULL) {
        msconnector_secure_zero(entry, sizeof(*entry));
    }
}

static int response_companion_handle_is_valid(const char *handle) {
    if (handle == NULL) {
        return 0;
    }
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE - 1U;
         ++index) {
        const unsigned char character = (unsigned char)handle[index];
        if (!((character >= (unsigned char)'0' && character <= (unsigned char)'9') ||
              (character >= (unsigned char)'a' && character <= (unsigned char)'f'))) {
            return 0;
        }
    }
    return handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE - 1U] == '\0';
}

static int response_companion_handle_matches(
    const char expected[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    const char *actual) {
    unsigned char difference = 0U;

    if (expected == NULL || !response_companion_handle_is_valid(actual)) {
        return 0;
    }
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE - 1U;
         ++index) {
        difference |= (unsigned char)expected[index] ^ (unsigned char)actual[index];
    }
    return difference == 0U;
}

static int response_companion_generate_handle(
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error) {
    static const char hexadecimal[] = "0123456789abcdef";
    unsigned char random_bytes[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_BYTES];
    size_t offset = 0U;

    if (handle == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion handle output is required", "runtime");
    }
    msconnector_secure_zero(handle,
        MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE);
#if defined(__linux__)
    while (offset < sizeof(random_bytes)) {
        const ssize_t read_count = getrandom(random_bytes + offset,
            sizeof(random_bytes) - offset, 0);
        if (read_count > 0) {
            offset += (size_t)read_count;
            continue;
        }
        if (read_count < 0 && errno == EINTR) {
            continue;
        }
        msconnector_secure_zero(random_bytes, sizeof(random_bytes));
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "secure opaque response handles require Linux getrandom", "runtime");
    }
#else
    (void)offset;
    return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
        "secure opaque response handles require an explicitly supported random source",
        "runtime");
#endif
    for (size_t index = 0U; index < sizeof(random_bytes); ++index) {
        handle[index * 2U] = hexadecimal[random_bytes[index] >> 4U];
        handle[index * 2U + 1U] = hexadecimal[random_bytes[index] & 0x0fU];
    }
    handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE - 1U] = '\0';
    msconnector_secure_zero(random_bytes, sizeof(random_bytes));
    return 1;
}

static void response_companion_destroy_detached_entry(
    msconnector_runtime_response_companion_entry *entry,
    int timeout) {
    msconnector_error ignored;

    if (entry == NULL || !entry->occupied) {
        return;
    }
    msconnector_error_init(&ignored);
    if (entry->transaction != NULL) {
        if (timeout) {
            (void)msconnector_runtime_transaction_timeout(entry->transaction, &ignored);
        }
        (void)msconnector_runtime_transaction_finish(entry->transaction, &ignored);
        entry->transaction->response_companion_handed_off = 0;
        msconnector_runtime_transaction_destroy(&entry->transaction);
    }
    response_companion_clear_entry(entry);
}

/* A registry lock protects only ownership metadata. Native engine processing
 * runs while the entry is leased (in_use), never while the fixed-capacity
 * registry lock is held. */
static int response_companion_registry_take_expired_locked(
    msconnector_runtime_response_companion_registry *registry,
    uint64_t now_ms,
    msconnector_runtime_response_companion_entry *out) {

    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY; ++index) {
        msconnector_runtime_response_companion_entry *entry =
            &registry->entries[index];
        if (entry->occupied && !entry->in_use && entry->expires_at_ms <= now_ms) {
            *out = *entry;
            response_companion_clear_entry(entry);
            return 1;
        }
    }
    return 0;
}

static int response_companion_registry_detach_in_use(
    msconnector_runtime_response_companion_registry *registry,
    msconnector_runtime_response_companion_entry *entry,
    msconnector_runtime_response_companion_entry *detached) {
    int result = 0;

    if (registry == NULL || entry == NULL || detached == NULL) {
        return 0;
    }
    response_companion_registry_lock(registry);
    if (entry->occupied && entry->in_use) {
        *detached = *entry;
        response_companion_clear_entry(entry);
        result = 1;
    }
    response_companion_registry_unlock(registry);
    return result;
}

void msconnector_runtime_response_companion_registry_init(
    msconnector_runtime_response_companion_registry *registry) {
    if (registry != NULL) {
        memset(registry, 0, sizeof(*registry));
        atomic_flag_clear_explicit(&registry->lock, memory_order_release);
    }
}

int msconnector_runtime_response_companion_handoff_with_handle(
    msconnector_runtime_response_companion_registry *registry,
    msconnector_runtime_transaction *transaction,
    uint64_t ttl_ms,
    char handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error) {
    const msconnector_transaction_profile *profile;
    size_t free_index = MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY;
    uint64_t now_ms;
    char generated_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE];

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (handle != NULL) {
        msconnector_secure_zero(handle,
            MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE);
    }
    if (registry == NULL || transaction == NULL || transaction->runtime == NULL ||
        ttl_ms == 0U || transaction->finish_attempted || transaction->finished ||
        transaction->response_companion_handed_off || handle == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion handoff requires a live transaction and handle output",
            "runtime");
    }
    profile = transaction->runtime->profile;
    if (profile == NULL ||
        msconnector_transaction_profile_phase_route(profile,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS) !=
            MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED ||
        msconnector_transaction_profile_phase_route(profile,
            MSCONNECTOR_PHASE_RESPONSE_BODY) !=
            MSCONNECTOR_TRANSACTION_PHASE_ROUTE_COMPANION_REQUIRED ||
        transaction->contract.active_phase >= 0 ||
        transaction->contract.completed_phase_mask !=
            (MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 |
             MSCONNECTOR_TRANSACTION_PHASE_MASK_P2) ||
        transaction->contract.status !=
            MSCONNECTOR_TRANSACTION_STATUS_WAITING_FOR_NEXT_PHASE) {
        return runtime_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion handoff requires completed P1 and P2", "runtime");
    }
    now_ms = transaction_now_ms();
    if (UINT64_MAX - now_ms < ttl_ms) {
        return runtime_error(error, MSCONNECTOR_ERROR_INVALID_CONFIG,
            "response companion TTL overflows the monotonic clock", "runtime");
    }
    if (!response_companion_generate_handle(generated_handle, error)) {
        return 0;
    }
    (void)msconnector_runtime_response_companion_expire(registry, now_ms);
    response_companion_registry_lock(registry);
    if (registry->shutting_down) {
        response_companion_registry_unlock(registry);
        msconnector_secure_zero(generated_handle, sizeof(generated_handle));
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion registry is shutting down", "runtime");
    }
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY; ++index) {
        const msconnector_runtime_response_companion_entry *entry =
            &registry->entries[index];
        if (!entry->occupied && free_index ==
                MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY) {
            free_index = index;
        } else if (entry->occupied && strcmp(
                entry->correlation.canonical_transaction_id,
                transaction->contract.canonical_transaction_id) == 0) {
            response_companion_registry_unlock(registry);
            msconnector_secure_zero(generated_handle, sizeof(generated_handle));
            return runtime_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
                "response companion canonical transaction ID is already registered",
                "runtime");
        } else if (entry->occupied && response_companion_handle_matches(
                entry->response_handle, generated_handle)) {
            response_companion_registry_unlock(registry);
            msconnector_secure_zero(generated_handle, sizeof(generated_handle));
            return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                "secure response companion handle collision", "runtime");
        }
    }
    if (free_index == MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY) {
        response_companion_registry_unlock(registry);
        msconnector_secure_zero(generated_handle, sizeof(generated_handle));
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion registry capacity is exhausted", "runtime");
    }
    registry->entries[free_index].occupied = 1;
    registry->entries[free_index].ttl_ms = ttl_ms;
    registry->entries[free_index].expires_at_ms = now_ms +
        (ttl_ms < RESPONSE_COMPANION_PRECLAIM_TTL_MS ?
            ttl_ms : RESPONSE_COMPANION_PRECLAIM_TTL_MS);
    registry->entries[free_index].transaction = transaction;
    if (msconnector_transaction_contract_handoff_response_companion(
            &transaction->contract, now_ms) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        response_companion_clear_entry(&registry->entries[free_index]);
        response_companion_registry_unlock(registry);
        msconnector_secure_zero(generated_handle, sizeof(generated_handle));
        return runtime_error(error, MSCONNECTOR_ERROR_PHASE_SEQUENCE,
            "response companion handoff violates the shared contract", "runtime");
    }
    registry->entries[free_index].correlation = transaction->contract;
    memcpy(registry->entries[free_index].response_handle, generated_handle,
        sizeof(generated_handle));
    transaction->response_companion_handed_off = 1;
    memcpy(handle, generated_handle, sizeof(generated_handle));
    response_companion_registry_unlock(registry);
    msconnector_secure_zero(generated_handle, sizeof(generated_handle));
    return 1;
}

int msconnector_runtime_response_companion_revoke_handle(
    msconnector_runtime_response_companion_registry *registry,
    const char *handle,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry detached;
    int revoked = 0;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (registry == NULL || !response_companion_handle_is_valid(handle)) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion capability is missing or invalid", "runtime");
    }
    memset(&detached, 0, sizeof(detached));
    response_companion_registry_lock(registry);
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY; ++index) {
        msconnector_runtime_response_companion_entry *entry = &registry->entries[index];
        if (!entry->occupied || !response_companion_handle_matches(
                entry->response_handle, handle)) {
            continue;
        }
        if (!entry->in_use && !entry->transport_claimed) {
            detached = *entry;
            response_companion_clear_entry(entry);
            revoked = 1;
        }
        break;
    }
    response_companion_registry_unlock(registry);
    if (revoked) {
        response_companion_destroy_detached_entry(&detached, 1);
        return 1;
    }
    return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
        "response companion capability is unavailable", "runtime");
}

static int response_companion_claim_live_transaction(
    msconnector_runtime_response_companion_entry *entry,
    msconnector_error *error) {
    int result;

    if (entry == NULL || entry->transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion transaction is unavailable", "runtime");
    }
    if (entry->transaction->contract.status !=
        MSCONNECTOR_TRANSACTION_STATUS_HANDED_OFF) {
        return 1;
    }
    result = msconnector_transaction_contract_claim_response_companion(
        &entry->transaction->contract, transaction_now_ms());
    return result == MSCONNECTOR_TRANSACTION_TRANSITION_OK ? 1 :
        contract_error(error, result,
            "response companion claim violates the shared contract");
}

/* A wire session owns its entry's in-use lease from opaque-handle CLAIM until
 * terminal cleanup. The registry never exposes the legacy transaction/host
 * tuple to a transport caller. */
static msconnector_runtime_response_companion_entry *
response_companion_session_acquire(
    msconnector_runtime_response_companion_session *session,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry detached;
    msconnector_runtime_response_companion_entry *entry;
    uint64_t now_ms;

    if (session == NULL || !session->active || session->registry == NULL ||
        session->entry == NULL) {
        (void)runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion session is not active", "runtime");
        return NULL;
    }
    memset(&detached, 0, sizeof(detached));
    now_ms = transaction_now_ms();
    response_companion_registry_lock(session->registry);
    entry = session->entry;
    if (session->registry->shutting_down || !entry->occupied || !entry->in_use ||
        !entry->transport_claimed) {
        response_companion_registry_unlock(session->registry);
        session->active = 0;
        session->entry = NULL;
        (void)runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion session is no longer available", "runtime");
        return NULL;
    }
    if (entry->expires_at_ms <= now_ms) {
        detached = *entry;
        response_companion_clear_entry(entry);
        session->active = 0;
        session->entry = NULL;
        response_companion_registry_unlock(session->registry);
        response_companion_destroy_detached_entry(&detached, 1);
        (void)runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion session expired", "runtime");
        return NULL;
    }
    response_companion_registry_unlock(session->registry);
    return entry;
}

static int response_companion_session_expire_after_operation(
    msconnector_runtime_response_companion_session *session) {
    msconnector_runtime_response_companion_entry detached;
    msconnector_runtime_response_companion_entry *entry;
    int expired = 0;

    if (session == NULL || !session->active || session->registry == NULL ||
        session->entry == NULL) {
        return 0;
    }
    memset(&detached, 0, sizeof(detached));
    response_companion_registry_lock(session->registry);
    entry = session->entry;
    if (entry->occupied && entry->in_use && entry->transport_claimed &&
        entry->expires_at_ms <= transaction_now_ms()) {
        detached = *entry;
        response_companion_clear_entry(entry);
        session->active = 0;
        session->entry = NULL;
        expired = 1;
    }
    response_companion_registry_unlock(session->registry);
    if (expired) {
        response_companion_destroy_detached_entry(&detached, 1);
    }
    return expired;
}

int msconnector_runtime_response_companion_claim_handle(
    msconnector_runtime_response_companion_registry *registry,
    const char *handle,
    msconnector_runtime_response_companion_session *session,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry detached;
    uint64_t now_ms;
    int matched = 0;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (session != NULL) {
        memset(session, 0, sizeof(*session));
    }
    if (registry == NULL || session == NULL ||
        !response_companion_handle_is_valid(handle)) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion capability is missing or invalid", "runtime");
    }
    now_ms = transaction_now_ms();
    (void)msconnector_runtime_response_companion_expire(registry, now_ms);
    memset(&detached, 0, sizeof(detached));
    response_companion_registry_lock(registry);
    if (registry->shutting_down) {
        response_companion_registry_unlock(registry);
        return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
            "response companion registry is shutting down", "runtime");
    }
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY;
         ++index) {
        msconnector_runtime_response_companion_entry *entry = &registry->entries[index];

        if (!entry->occupied || !response_companion_handle_matches(
                entry->response_handle, handle)) {
            continue;
        }
        if (entry->expires_at_ms <= now_ms) {
            detached = *entry;
            response_companion_clear_entry(entry);
        } else if (!(entry->in_use || entry->transport_claimed)) {
            entry->in_use = 1;
            entry->transport_claimed = 1;
            entry->expires_at_ms = now_ms + entry->ttl_ms;
            session->registry = registry;
            session->entry = entry;
            session->active = 1;
            matched = 1;
        }
        break;
    }
    response_companion_registry_unlock(registry);
    if (detached.occupied) {
        response_companion_destroy_detached_entry(&detached, 1);
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion capability is unavailable", "runtime");
    }
    if (!matched) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_MISSING,
            "response companion capability is unavailable", "runtime");
    }
    if (!response_companion_claim_live_transaction(session->entry, error)) {
        msconnector_secure_zero(&detached, sizeof(detached));
        if (response_companion_registry_detach_in_use(registry, session->entry,
                &detached)) {
            session->active = 0;
            session->entry = NULL;
            response_companion_destroy_detached_entry(&detached, 1);
        }
        return 0;
    }
    return 1;
}

int msconnector_runtime_response_companion_session_process_response_headers(
    msconnector_runtime_response_companion_session *session,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    int result = entry != NULL && process_companion_response_headers(
        entry->transaction, response, decision, error);

    if (entry != NULL && response_companion_session_expire_after_operation(session) &&
        result) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion TTL expired during response headers", "runtime");
    }
    return result;
}

int msconnector_runtime_response_companion_session_append_response_body_chunk(
    msconnector_runtime_response_companion_session *session,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    int result = entry != NULL && append_companion_response_body_chunk(
        entry->transaction, data, size, error);

    if (entry != NULL && response_companion_session_expire_after_operation(session) &&
        result) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion TTL expired during response body", "runtime");
    }
    return result;
}

int msconnector_runtime_response_companion_session_finish_response_body(
    msconnector_runtime_response_companion_session *session,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    int result = entry != NULL && finish_companion_response_body(
        entry->transaction, decision, error);

    if (entry != NULL && response_companion_session_expire_after_operation(session) &&
        result) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion TTL expired at response end-of-stream", "runtime");
    }
    return result;
}

int msconnector_runtime_response_companion_session_set_response_commit_state(
    msconnector_runtime_response_companion_session *session,
    int headers_sent,
    int body_started,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    int result = entry != NULL &&
        msconnector_runtime_transaction_set_response_commit_state_checked(
            entry->transaction, headers_sent, body_started, error);

    if (entry != NULL && response_companion_session_expire_after_operation(session) &&
        result) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion TTL expired at response commitment", "runtime");
    }
    return result;
}

int msconnector_runtime_response_companion_session_record_host_action(
    msconnector_runtime_response_companion_session *session,
    const msconnector_decision *decision,
    msconnector_decision_action actual_action,
    int visible_http_status,
    const char *transport_result,
    int connection_aborted,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    int result = entry != NULL && msconnector_runtime_transaction_record_host_action(
        entry->transaction, decision, actual_action, visible_http_status,
        transport_result, connection_aborted, error);

    if (entry != NULL && response_companion_session_expire_after_operation(session) &&
        result) {
        return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
            "response companion TTL expired while recording host action", "runtime");
    }
    return result;
}

int msconnector_runtime_response_companion_session_fail(
    msconnector_runtime_response_companion_session *session,
    msconnector_transaction_error_class error_class,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    msconnector_runtime_response_companion_entry detached;
    int result;

    if (entry == NULL || error_class == MSCONNECTOR_TRANSACTION_ERROR_NONE) {
        return 0;
    }
    memset(&detached, 0, sizeof(detached));
    result = msconnector_transaction_contract_fail(&entry->transaction->contract,
        error_class, transaction_now_ms()) == MSCONNECTOR_TRANSACTION_TRANSITION_OK;
    if (result) {
        entry->transaction->request_blocked = 1;
        if (!emit_contract_terminal_event(entry->transaction, error)) {
            result = 0;
        }
    } else {
        (void)contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_INVALID,
            "response companion failure violates the shared contract");
    }
    if (response_companion_registry_detach_in_use(session->registry, entry,
            &detached)) {
        session->active = 0;
        session->entry = NULL;
        response_companion_destroy_detached_entry(&detached, 0);
    }
    return result;
}

int msconnector_runtime_response_companion_session_cancel(
    msconnector_runtime_response_companion_session *session,
    int upstream_disconnect,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    msconnector_runtime_response_companion_entry detached;
    int result;

    if (entry == NULL) {
        return 0;
    }
    memset(&detached, 0, sizeof(detached));
    /* A disruptive decision is terminal before its host translation is
     * reported.  The observer's subsequent CANCEL is the deterministic
     * ownership-release acknowledgement, not a second business decision.
     * Treat it as successful cleanup so a valid P3 deny cannot be recast as
     * a protocol failure, then detach the exact claimed entry below. */
    if (entry->transaction->contract.status ==
        MSCONNECTOR_TRANSACTION_STATUS_TERMINAL) {
        result = 1;
    } else {
        result = msconnector_runtime_transaction_cancel(entry->transaction,
            upstream_disconnect, error);
    }
    if (response_companion_registry_detach_in_use(session->registry, entry,
            &detached)) {
        session->active = 0;
        session->entry = NULL;
        response_companion_destroy_detached_entry(&detached, 0);
    }
    return result;
}

int msconnector_runtime_response_companion_session_release(
    msconnector_runtime_response_companion_session *session,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry =
        response_companion_session_acquire(session, error);
    msconnector_runtime_response_companion_entry detached;
    int result;

    if (entry == NULL) {
        return 0;
    }
    memset(&detached, 0, sizeof(detached));
    result = msconnector_runtime_transaction_finish(entry->transaction, error);
    if (response_companion_registry_detach_in_use(session->registry, entry,
            &detached)) {
        session->active = 0;
        session->entry = NULL;
        response_companion_destroy_detached_entry(&detached, 0);
    }
    return result;
}

/*
 * The former tuple-keyed response companion entry points are deliberately
 * disabled.  Response observers must use the single-claim opaque-handle
 * session API above; retaining a transaction/connector/host lookup path would
 * allow a client-controlled identity to bypass the MRC1 capability boundary.
 */
#if 0
int msconnector_runtime_response_companion_process_response_headers(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry expired;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&expired, 0, sizeof(expired));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    result = entry != NULL && response_companion_claim_live_transaction(entry, error) &&
        process_companion_response_headers(entry->transaction, response, decision, error);
    if (entry != NULL && response_companion_registry_release_or_expire_use(registry,
            entry, transaction_now_ms(), &expired)) {
        response_companion_destroy_detached_entry(&expired, 1);
        if (result) {
            return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
                "response companion TTL expired during response headers", "runtime");
        }
    }
    return result;
}

int msconnector_runtime_response_companion_append_response_body_chunk(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    const unsigned char *data,
    size_t size,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry expired;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&expired, 0, sizeof(expired));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    result = entry != NULL && append_companion_response_body_chunk(entry->transaction,
        data, size, error);
    if (entry != NULL && response_companion_registry_release_or_expire_use(registry,
            entry, transaction_now_ms(), &expired)) {
        response_companion_destroy_detached_entry(&expired, 1);
        if (result) {
            return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
                "response companion TTL expired during response body", "runtime");
        }
    }
    return result;
}

int msconnector_runtime_response_companion_finish_response_body(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    msconnector_decision *decision,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry expired;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&expired, 0, sizeof(expired));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    result = entry != NULL && finish_companion_response_body(entry->transaction,
        decision, error);
    if (entry != NULL && response_companion_registry_release_or_expire_use(registry,
            entry, transaction_now_ms(), &expired)) {
        response_companion_destroy_detached_entry(&expired, 1);
        if (result) {
            return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
                "response companion TTL expired at response end-of-stream", "runtime");
        }
    }
    return result;
}

int msconnector_runtime_response_companion_set_response_commit_state(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    int headers_sent,
    int body_started,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry expired;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&expired, 0, sizeof(expired));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    result = entry != NULL && msconnector_runtime_transaction_set_response_commit_state_checked(
        entry->transaction, headers_sent, body_started, error);
    if (entry != NULL && response_companion_registry_release_or_expire_use(registry,
            entry, transaction_now_ms(), &expired)) {
        response_companion_destroy_detached_entry(&expired, 1);
        if (result) {
            return runtime_error(error, MSCONNECTOR_ERROR_CORRELATION_EXPIRED,
                "response companion TTL expired at response commitment", "runtime");
        }
    }
    return result;
}

int msconnector_runtime_response_companion_cancel(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    int upstream_disconnect,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry detached;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&detached, 0, sizeof(detached));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    result = entry != NULL && msconnector_runtime_transaction_cancel(entry->transaction,
        upstream_disconnect, error);
    if (entry != NULL && response_companion_registry_detach_in_use(registry,
            entry, &detached)) {
        response_companion_destroy_detached_entry(&detached, 1);
    }
    return result;
}

int msconnector_runtime_response_companion_release(
    msconnector_runtime_response_companion_registry *registry,
    const char *transaction_id,
    const char *connector_id,
    const char *host_id,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry *entry;
    msconnector_runtime_response_companion_entry detached;
    int result;

    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    memset(&detached, 0, sizeof(detached));
    (void)msconnector_runtime_response_companion_expire(registry, transaction_now_ms());
    entry = response_companion_registry_acquire(registry, transaction_id,
        connector_id, host_id, error);
    if (entry == NULL) {
        return 0;
    }
    result = msconnector_runtime_transaction_finish(entry->transaction, error);
    if (response_companion_registry_detach_in_use(registry, entry, &detached)) {
        response_companion_destroy_detached_entry(&detached, 0);
    }
    return result;
}

#endif

size_t msconnector_runtime_response_companion_expire(
    msconnector_runtime_response_companion_registry *registry,
    uint64_t now_ms) {
    size_t expired = 0U;
    msconnector_runtime_response_companion_entry detached;

    if (registry == NULL) {
        return 0U;
    }
    for (;;) {
        memset(&detached, 0, sizeof(detached));
        response_companion_registry_lock(registry);
        if (!response_companion_registry_take_expired_locked(registry, now_ms,
                &detached)) {
            response_companion_registry_unlock(registry);
            break;
        }
        response_companion_registry_unlock(registry);
        response_companion_destroy_detached_entry(&detached, 1);
        ++expired;
    }
    return expired;
}

int msconnector_runtime_response_companion_registry_shutdown(
    msconnector_runtime_response_companion_registry *registry,
    msconnector_error *error) {
    msconnector_runtime_response_companion_entry detached;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (registry == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response companion registry is required", "runtime");
    }
    response_companion_registry_lock(registry);
    registry->shutting_down = 1;
    for (size_t index = 0U;
         index < MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_CAPACITY; ++index) {
        if (registry->entries[index].occupied && registry->entries[index].in_use) {
            response_companion_registry_unlock(registry);
            return runtime_error(error, MSCONNECTOR_ERROR_RUNTIME_UNAVAILABLE,
                "response observer must quiesce before companion shutdown", "runtime");
        }
    }
    response_companion_registry_unlock(registry);

    for (;;) {
        int found = 0;

        memset(&detached, 0, sizeof(detached));
        response_companion_registry_lock(registry);
        found = response_companion_registry_take_expired_locked(registry,
            UINT64_MAX, &detached);
        response_companion_registry_unlock(registry);
        if (!found) {
            return 1;
        }
        response_companion_destroy_detached_entry(&detached, 0);
    }
}

void msconnector_runtime_transaction_request_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress) {
    if (progress == NULL) {
        return;
    }
    memset(progress, 0, sizeof(*progress));
    if (transaction != NULL) {
        progress->bytes_seen = transaction->request_body.bytes_seen;
        progress->bytes_inspected = transaction->request_body.bytes_inspected;
        progress->truncated = transaction->request_body.truncated;
        progress->finished = transaction->request_body.finished;
        progress->limit_outcome = transaction->request_body.limit_outcome;
    }
}

void msconnector_runtime_transaction_response_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress) {
    if (progress == NULL) {
        return;
    }
    memset(progress, 0, sizeof(*progress));
    if (transaction != NULL) {
        progress->bytes_seen = transaction->response_body.bytes_seen;
        progress->bytes_inspected = transaction->response_body.bytes_inspected;
        progress->truncated = transaction->response_body.truncated;
        progress->finished = transaction->response_body.finished;
        progress->limit_outcome = transaction->response_body.limit_outcome;
    }
}

int msconnector_runtime_transaction_snapshot_get(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_transaction_snapshot *snapshot) {
    if (snapshot == NULL) return 0;
    memset(snapshot, 0, sizeof(*snapshot));
    if (transaction == NULL) return 0;
    snapshot->contract = transaction->contract;
    snapshot->request_body = transaction->request_body;
    snapshot->response_body = transaction->response_body;
    snapshot->response_original_status = transaction->response_original_status;
    snapshot->response_headers_processed = transaction->response_headers_processed;
    snapshot->response_headers_sent = transaction->response_headers_sent;
    snapshot->response_body_started = transaction->response_body_started;
    snapshot->finished = transaction->finished;
    return 1;
}

static int runtime_transaction_cleanup_checked(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    int cleanup_result;

    if (transaction == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction is required", "runtime");
    }
    if (!msconnector_runtime_transaction_finish(transaction, error)) {
        return 0;
    }
    if (transaction->native_started) {
        runtime_operation_lock(transaction->runtime);
        msconnector_modsecurity_transaction_cleanup(&transaction->modsecurity);
        runtime_operation_unlock(transaction->runtime);
        transaction->native_started = 0;
    }
    cleanup_result = msconnector_transaction_contract_cleanup(&transaction->contract,
        transaction_now_ms());
    if (cleanup_result != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        return contract_error(error, cleanup_result,
            "transaction cleanup did not complete");
    }
    return 1;
}

static void runtime_transaction_cleanup_best_effort(
    msconnector_runtime_transaction *transaction) {
    msconnector_error ignored;

    if (transaction == NULL) {
        return;
    }
    msconnector_error_init(&ignored);
    if (!transaction->finish_attempted) {
        (void)msconnector_runtime_transaction_finish(transaction, &ignored);
    }
    if (transaction->native_started) {
        runtime_operation_lock(transaction->runtime);
        msconnector_modsecurity_transaction_cleanup(&transaction->modsecurity);
        runtime_operation_unlock(transaction->runtime);
        transaction->native_started = 0;
    }
    (void)msconnector_transaction_contract_cleanup(&transaction->contract,
        transaction_now_ms());
}

int msconnector_runtime_transaction_finalize_and_snapshot(
    msconnector_runtime_transaction **transaction_pointer,
    msconnector_runtime_transaction_snapshot *snapshot,
    msconnector_error *error) {
    msconnector_runtime_transaction *transaction;

    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction_pointer == NULL || *transaction_pointer == NULL || snapshot == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction and snapshot are required", "runtime");
    }
    transaction = *transaction_pointer;
    if (!runtime_transaction_cleanup_checked(transaction, error) ||
        !msconnector_runtime_transaction_snapshot_get(transaction, snapshot) ||
        !snapshot->finished || !snapshot->contract.cleanup_started ||
        !snapshot->contract.cleanup_complete ||
        snapshot->contract.status != MSCONNECTOR_TRANSACTION_STATUS_CLEANED) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction cleanup snapshot is incomplete", "runtime");
    }
    msconnector_secure_zero(transaction, sizeof(*transaction));
    free(transaction);
    *transaction_pointer = NULL;
    return 1;
}

int msconnector_runtime_transaction_process_response(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error) {
    const msconnector_runtime *runtime;
    if (error != NULL) {
        msconnector_error_init(error);
    }
    if (transaction == NULL || response == NULL || decision == NULL) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction, response and decision are required", "runtime");
    }
    runtime = transaction->runtime;
    msconnector_decision_set_allow(decision);
    if (transaction->finish_attempted || transaction->response_headers_processed) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "response processing may only be attempted once", "runtime");
    }
    if (transaction->request_blocked) {
        return 1;
    }
    if (!msconnector_runtime_transaction_process_response_headers(
            transaction, response, decision, error)) {
        return 0;
    }
    if (transaction->request_blocked) {
        return 1;
    }
    if (runtime->body_policy.response_body_mode == MSCONNECTOR_BODY_MODE_NONE &&
        response->body.size > 0U) {
        return runtime_error(error, MSCONNECTOR_ERROR_UNSUPPORTED_PHASE,
            "response body is disabled", "runtime");
    }
    if (runtime->body_policy.response_body_mode != MSCONNECTOR_BODY_MODE_NONE &&
        !msconnector_runtime_transaction_append_response_body_chunk(
            transaction, response->body.data, response->body.size, error)) {
        return 0;
    }
    return msconnector_runtime_transaction_finish_response_body(
        transaction, decision, error);
}

static int finish_transaction_with_logging(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error) {
    transaction->finish_attempted = 1;
    if (msconnector_flow_guard_mark_immutable(&transaction->flow) !=
        MSCONNECTOR_FLOW_GUARD_OK) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "transaction could not be made immutable", "flow_guard");
    }
    if (transaction->native_started) {
        int logged;

        runtime_operation_lock(transaction->runtime);
        logged = msconnector_modsecurity_process_logging(&transaction->modsecurity, error);
        runtime_operation_unlock(transaction->runtime);
        if (!logged) {
            return 0;
        }
    }
    transaction->finished = 1;
    return 1;
}

int msconnector_runtime_transaction_finish_host_rejected_request_body(
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
    if (!transaction->native_started) {
        return finish_transaction_with_logging(transaction, error);
    }
    if (transaction->runtime->body_policy.request_body_mode !=
            MSCONNECTOR_BODY_MODE_STREAMING ||
        transaction->request_body.finished || transaction->response_headers_processed) {
        return runtime_error(error, MSCONNECTOR_ERROR_INTERNAL,
            "host-rejected request body must be incomplete streaming before response processing",
            "runtime");
    }
    return finish_transaction_with_logging(transaction, error);
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
    if (transaction->native_started && !transaction->request_blocked &&
        transaction->runtime->body_policy.request_body_mode == MSCONNECTOR_BODY_MODE_STREAMING &&
        !transaction->request_body.finished) {
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE, transaction_now_ms());
        transaction->request_blocked = 1;
        if (!emit_contract_terminal_event(transaction, error)) {
            return 0;
        }
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE,
            "streaming request body reached transaction finish without end-of-stream");
    }
    if (transaction->native_started && transaction->response_headers_processed &&
        !transaction->request_blocked &&
        !transaction->response_body.finished) {
        (void)msconnector_transaction_contract_fail(&transaction->contract,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE, transaction_now_ms());
        transaction->request_blocked = 1;
        if (!emit_contract_terminal_event(transaction, error)) {
            return 0;
        }
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE,
            "response reached transaction finish without response-body end-of-stream");
    }
    if (msconnector_transaction_contract_finish(&transaction->contract,
            transaction_now_ms()) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
        if (!emit_contract_terminal_event(transaction, error)) {
            return 0;
        }
        return contract_error(error, MSCONNECTOR_TRANSACTION_TRANSITION_SKIPPED_PHASE,
            "transaction finish requires P1 through P4 or a terminal decision");
    }
    if (transaction->contract.status == MSCONNECTOR_TRANSACTION_STATUS_TERMINAL &&
        !emit_contract_terminal_event(transaction, error)) {
        return 0;
    }
    return finish_transaction_with_logging(transaction, error);
}

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction) {
    return transaction == NULL ? NULL : transaction->metadata.transaction_id;
}

void msconnector_runtime_transaction_destroy(
    msconnector_runtime_transaction **transaction_pointer) {
    msconnector_runtime_transaction *transaction;
    if (transaction_pointer == NULL || *transaction_pointer == NULL) {
        return;
    }
    transaction = *transaction_pointer;
    runtime_transaction_cleanup_best_effort(transaction);
    msconnector_secure_zero(transaction, sizeof(*transaction));
    free(transaction);
    *transaction_pointer = NULL;
}
