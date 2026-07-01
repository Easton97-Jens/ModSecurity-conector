#include "msconnector/config.h"
#include "msconnector/block_statuses.h"
#include <stdio.h>

static void set_error(char *error, size_t error_len, const char *message) {
    if (error != 0 && error_len > 0) {
        (void)snprintf(error, error_len, "%s", message);
    }
}

void msconnector_config_init(msconnector_config *config) {
    if (config == 0) return;
    config->enable = MSCONNECTOR_BOOL_UNSET;
    config->use_error_log = MSCONNECTOR_BOOL_UNSET;
    config->rules_inline = 0; config->rules_file = 0;
    config->rules_remote_key = 0; config->rules_remote_url = 0;
    config->transaction_id = 0; config->transaction_id_expr = 0;
    config->phase4_mode = (enum msconnector_phase4_mode)-1;
    config->phase4_content_types_file = 0; config->phase4_log_path = 0;
    config->phase4_body_limit = 0;
    config->default_block_status = 0; config->default_error_status = 0; config->unsupported_status = 0;
}

void msconnector_config_apply_defaults(msconnector_config *config) {
    if (config == 0) return;
    if (config->enable == MSCONNECTOR_BOOL_UNSET) config->enable = MSCONNECTOR_DEFAULT_ENABLE;
    if (config->use_error_log == MSCONNECTOR_BOOL_UNSET) config->use_error_log = MSCONNECTOR_DEFAULT_USE_ERROR_LOG;
    if ((int)config->phase4_mode < 0) config->phase4_mode = MSCONNECTOR_DEFAULT_PHASE4_MODE;
    if (config->phase4_body_limit == 0) config->phase4_body_limit = MSCONNECTOR_DEFAULT_PHASE4_BODY_LIMIT;
    if (config->default_block_status == 0) config->default_block_status = MSCONNECTOR_DEFAULT_BLOCK_STATUS;
    if (config->default_error_status == 0) config->default_error_status = MSCONNECTOR_DEFAULT_ERROR_STATUS;
    if (config->unsupported_status == 0) config->unsupported_status = MSCONNECTOR_DEFAULT_UNSUPPORTED_STATUS;
}

#define PICK_ENUM(field, unset) out->field = (child && child->field != (unset)) ? child->field : ((parent && parent->field != (unset)) ? parent->field : out->field)
#define PICK_PTR(field) out->field = (child && child->field) ? child->field : ((parent && parent->field) ? parent->field : out->field)
#define PICK_INT(field) out->field = (child && child->field != 0) ? child->field : ((parent && parent->field != 0) ? parent->field : out->field)

int msconnector_config_merge(msconnector_config *out, const msconnector_config *parent, const msconnector_config *child) {
    if (out == 0) return 0;
    msconnector_config_init(out);
    PICK_ENUM(enable, MSCONNECTOR_BOOL_UNSET); PICK_ENUM(use_error_log, MSCONNECTOR_BOOL_UNSET);
    PICK_PTR(rules_inline); PICK_PTR(rules_file); PICK_PTR(rules_remote_key); PICK_PTR(rules_remote_url);
    PICK_PTR(transaction_id); PICK_PTR(transaction_id_expr);
    PICK_ENUM(phase4_mode, (enum msconnector_phase4_mode)-1);
    PICK_PTR(phase4_content_types_file); PICK_PTR(phase4_log_path);
    PICK_INT(phase4_body_limit); PICK_INT(default_block_status); PICK_INT(default_error_status); PICK_INT(unsupported_status);
    msconnector_config_apply_defaults(out);
    return msconnector_config_validate(out, 0, 0);
}

int msconnector_config_validate(const msconnector_config *config, char *error, size_t error_len) {
    if (config == 0) { set_error(error, error_len, "config is required"); return 0; }
    if (config->enable < MSCONNECTOR_BOOL_UNSET || config->enable > MSCONNECTOR_BOOL_ON) { set_error(error, error_len, "invalid enable option"); return 0; }
    if (config->use_error_log < MSCONNECTOR_BOOL_UNSET || config->use_error_log > MSCONNECTOR_BOOL_ON) { set_error(error, error_len, "invalid error log option"); return 0; }
    if ((int)config->phase4_mode < -1 || config->phase4_mode > MSCONNECTOR_PHASE4_MODE_STRICT) { set_error(error, error_len, "invalid phase4 mode"); return 0; }
    if (config->default_block_status && !msconnector_http_status_is_valid(config->default_block_status)) { set_error(error, error_len, "invalid default block status"); return 0; }
    if (config->default_error_status && !msconnector_http_status_is_valid(config->default_error_status)) { set_error(error, error_len, "invalid default error status"); return 0; }
    if (config->unsupported_status && !msconnector_http_status_is_valid(config->unsupported_status)) { set_error(error, error_len, "invalid unsupported status"); return 0; }
    set_error(error, error_len, ""); return 1;
}
