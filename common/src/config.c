#include "msconnector/config.h"
#include "msconnector/block_statuses.h"
#include <stdio.h>

static void set_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0) {
        (void)snprintf(error, error_len, "%s", message);
    }
}

static enum msconnector_bool_option merge_bool_option(
    enum msconnector_bool_option parent,
    enum msconnector_bool_option child) {
    if (child != MSCONNECTOR_BOOL_UNSET) {
        return child;
    }

    return parent;
}

static enum msconnector_phase4_mode merge_phase4_mode(
    enum msconnector_phase4_mode parent,
    enum msconnector_phase4_mode child) {
    if (child != MSCONNECTOR_PHASE4_MODE_UNSET) {
        return child;
    }

    return parent;
}

static msconnector_body_limit_action merge_body_limit_action(
    msconnector_body_limit_action parent,
    msconnector_body_limit_action child) {
    if (child != MSCONNECTOR_BODY_LIMIT_ACTION_UNSET) {
        return child;
    }
    return parent;
}


static int string_empty(const char *value) {
    return value == 0 || value[0] == '\0';
}

static int remote_pair_requested(const msconnector_config *config) {
    return !string_empty(config->rules_remote_key) || !string_empty(config->rules_remote_url);
}

static int remote_pair_complete(const msconnector_config *config) {
    return !string_empty(config->rules_remote_key) && !string_empty(config->rules_remote_url);
}

static const char *merge_string(const char *parent, const char *child) {
    if (child != 0) {
        return child;
    }

    return parent;
}

static int merge_status_value(int parent, int child) {
    if (child != 0) {
        return child;
    }

    return parent;
}

static size_t merge_size_value(size_t parent, size_t child) {
    if (child != 0U) {
        return child;
    }

    return parent;
}

static size_t merge_late_intervention_timeout(
    size_t parent,
    size_t child) {
    if (child != MSCONNECTOR_LATE_INTERVENTION_TIMEOUT_UNSET) {
        return child;
    }
    return parent;
}

static int validate_bool_option(
    enum msconnector_bool_option value,
    const char *message,
    char *error,
    size_t error_len) {
    if (value < MSCONNECTOR_BOOL_UNSET || value > MSCONNECTOR_BOOL_ON) {
        set_error(error, error_len, message);
        return 0;
    }

    return 1;
}

static int validate_block_status_value(
    int value,
    const char *message,
    char *error,
    size_t error_len) {
    if (value != 0 && !msconnector_block_status_is_allowed(value)) {
        set_error(error, error_len, message);
        return 0;
    }

    return 1;
}

static int validate_error_status_value(
    int value,
    const char *message,
    char *error,
    size_t error_len) {
    if (value != 0 && (!msconnector_http_status_is_valid(value) || !msconnector_http_status_is_error(value))) {
        set_error(error, error_len, message);
        return 0;
    }

    return 1;
}

static void merge_remote_rules_pair(
    msconnector_config *out,
    const msconnector_config *parent,
    const msconnector_config *child) {
    if (child->rules_remote_key != 0 || child->rules_remote_url != 0) {
        out->rules_remote_key = child->rules_remote_key;
        out->rules_remote_url = child->rules_remote_url;
        return;
    }

    out->rules_remote_key = parent->rules_remote_key;
    out->rules_remote_url = parent->rules_remote_url;
}

static void merge_transaction_id_pair(
    msconnector_config *out,
    const msconnector_config *parent,
    const msconnector_config *child) {
    if (child->transaction_id != 0) {
        out->transaction_id = child->transaction_id;
        out->transaction_id_expr = 0;
        return;
    }
    if (child->transaction_id_expr != 0) {
        out->transaction_id = 0;
        out->transaction_id_expr = child->transaction_id_expr;
        return;
    }

    out->transaction_id = parent->transaction_id;
    out->transaction_id_expr = parent->transaction_id_expr;
}

void msconnector_config_init(msconnector_config *config) {
    if (config == 0) {
        return;
    }

    config->enable = MSCONNECTOR_BOOL_UNSET;
    config->use_error_log = MSCONNECTOR_BOOL_UNSET;
    config->rules_inline = 0;
    config->rules_file = 0;
    config->rules_remote_key = 0;
    config->rules_remote_url = 0;
    config->transaction_id = 0;
    config->transaction_id_expr = 0;
    config->phase4_mode = MSCONNECTOR_PHASE4_MODE_UNSET;
    config->phase4_content_types_file = 0;
    config->phase4_log_path = 0;
    config->phase4_body_limit = 0;
    config->request_body_limit = 0;
    config->response_body_limit = 0;
    config->body_limit_action = MSCONNECTOR_BODY_LIMIT_ACTION_UNSET;
    config->late_intervention_timeout_ms =
        MSCONNECTOR_LATE_INTERVENTION_TIMEOUT_UNSET;
    config->default_block_status = 0;
    config->default_error_status = 0;
    config->unsupported_status = 0;
}

void msconnector_config_apply_defaults(msconnector_config *config) {
    if (config == 0) {
        return;
    }

    if (config->enable == MSCONNECTOR_BOOL_UNSET) {
        config->enable = MSCONNECTOR_DEFAULT_ENABLE;
    }

    if (config->use_error_log == MSCONNECTOR_BOOL_UNSET) {
        config->use_error_log = MSCONNECTOR_DEFAULT_USE_ERROR_LOG;
    }

    if (config->phase4_mode == MSCONNECTOR_PHASE4_MODE_UNSET) {
        config->phase4_mode = MSCONNECTOR_DEFAULT_PHASE4_MODE;
    }

    if (config->phase4_body_limit == 0U) {
        config->phase4_body_limit = MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT;
    }

    if (config->request_body_limit == 0U) {
        config->request_body_limit = MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT;
    }

    if (config->response_body_limit == 0U) {
        config->response_body_limit = config->phase4_body_limit;
    }

    if (config->body_limit_action == MSCONNECTOR_BODY_LIMIT_ACTION_UNSET) {
        config->body_limit_action = MSCONNECTOR_BODY_LIMIT_ACTION_REJECT;
    }

    if (config->late_intervention_timeout_ms ==
        MSCONNECTOR_LATE_INTERVENTION_TIMEOUT_UNSET) {
        config->late_intervention_timeout_ms = 0U;
    }

    if (config->default_block_status == 0) {
        config->default_block_status = MSCONNECTOR_DEFAULT_BLOCK_STATUS;
    }

    if (config->default_error_status == 0) {
        config->default_error_status = MSCONNECTOR_DEFAULT_ERROR_STATUS;
    }

    if (config->unsupported_status == 0) {
        config->unsupported_status = MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS;
    }
}

int msconnector_config_merge(
    msconnector_config *out,
    const msconnector_config *parent,
    const msconnector_config *child) {
    msconnector_config parent_config;
    msconnector_config child_config;

    if (out == 0) {
        return 0;
    }

    if (parent == 0) {
        msconnector_config_init(&parent_config);
        parent = &parent_config;
    }

    if (child == 0) {
        msconnector_config_init(&child_config);
        child = &child_config;
    }

    out->enable = merge_bool_option(parent->enable, child->enable);
    out->use_error_log = merge_bool_option(parent->use_error_log, child->use_error_log);
    out->rules_inline = merge_string(parent->rules_inline, child->rules_inline);
    out->rules_file = merge_string(parent->rules_file, child->rules_file);
    merge_remote_rules_pair(out, parent, child);
    merge_transaction_id_pair(out, parent, child);
    out->phase4_mode = merge_phase4_mode(parent->phase4_mode, child->phase4_mode);
    out->phase4_content_types_file = merge_string(
        parent->phase4_content_types_file,
        child->phase4_content_types_file);
    out->phase4_log_path = merge_string(parent->phase4_log_path, child->phase4_log_path);
    out->phase4_body_limit = merge_size_value(parent->phase4_body_limit, child->phase4_body_limit);
    out->request_body_limit = merge_size_value(
        parent->request_body_limit, child->request_body_limit);
    out->response_body_limit = merge_size_value(
        parent->response_body_limit, child->response_body_limit);
    out->body_limit_action = merge_body_limit_action(
        parent->body_limit_action, child->body_limit_action);
    out->late_intervention_timeout_ms = merge_late_intervention_timeout(
        parent->late_intervention_timeout_ms,
        child->late_intervention_timeout_ms);
    out->default_block_status = merge_status_value(parent->default_block_status, child->default_block_status);
    out->default_error_status = merge_status_value(parent->default_error_status, child->default_error_status);
    out->unsupported_status = merge_status_value(parent->unsupported_status, child->unsupported_status);

    msconnector_config_apply_defaults(out);
    return msconnector_config_validate(out, 0, 0);
}

int msconnector_config_validate(const msconnector_config *config, char *error, size_t error_len) {
    if (config == 0) {
        set_error(error, error_len, "config is required");
        return 0;
    }

    if (!validate_bool_option(config->enable, "invalid enable option", error, error_len)) {
        return 0;
    }

    if (!validate_bool_option(config->use_error_log, "invalid error log option", error, error_len)) {
        return 0;
    }

    if (config->phase4_mode < MSCONNECTOR_PHASE4_MODE_UNSET ||
        config->phase4_mode > MSCONNECTOR_PHASE4_MODE_STRICT) {
        set_error(error, error_len, "invalid phase4 mode");
        return 0;
    }

    if (config->body_limit_action != MSCONNECTOR_BODY_LIMIT_ACTION_UNSET &&
        !msconnector_body_limit_action_is_supported(config->body_limit_action)) {
        set_error(error, error_len, "invalid body limit action");
        return 0;
    }

    if (remote_pair_requested(config) && !remote_pair_complete(config)) {
        set_error(error, error_len, "incomplete remote rules pair");
        return 0;
    }

    if (config->transaction_id != 0 && config->transaction_id_expr != 0) {
        set_error(error, error_len, "transaction id and expression are mutually exclusive");
        return 0;
    }

    if (!validate_block_status_value(config->default_block_status, "invalid default block status", error, error_len)) {
        return 0;
    }

    if (!validate_error_status_value(config->default_error_status, "invalid default error status", error, error_len)) {
        return 0;
    }

    if (!validate_error_status_value(config->unsupported_status, "invalid unsupported status", error, error_len)) {
        return 0;
    }

    set_error(error, error_len, "");
    return 1;
}
