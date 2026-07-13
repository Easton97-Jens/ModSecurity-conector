#ifndef MSCONNECTOR_CONFIG_H
#define MSCONNECTOR_CONFIG_H

#include "msconnector/body_policy.h"
#include "msconnector/options.h"
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral configuration model.
 *
 * This structure does not own pointer fields. A host connector remains
 * responsible for parsing server configuration and keeping referenced strings
 * alive for the configuration scope in which this model is used. The helpers
 * below store and validate values only; they do not integrate any connector.
 */
typedef struct msconnector_config {
    enum msconnector_bool_option enable;
    enum msconnector_bool_option use_error_log;
    const char *rules_inline;
    const char *rules_file;
    const char *rules_remote_key;
    const char *rules_remote_url;
    const char *transaction_id;
    const char *transaction_id_expr;
    enum msconnector_phase4_mode phase4_mode;
    const char *phase4_content_types_file;
    const char *phase4_log_path;
    size_t phase4_body_limit;
    size_t request_body_limit;
    size_t response_body_limit;
    msconnector_body_limit_action body_limit_action;
    /* Zero disables the optional host-side budget. Common stores this value
     * but has no host timer or cancellation primitive with which to enforce
     * it. The unset sentinel preserves an explicit zero during config merge. */
    size_t late_intervention_timeout_ms;
    int default_block_status;
    int default_error_status;
    int unsupported_status;
} msconnector_config;

#define MSCONNECTOR_LATE_INTERVENTION_TIMEOUT_UNSET ((size_t)-1)

void msconnector_config_init(msconnector_config *config);
void msconnector_config_apply_defaults(msconnector_config *config);
int msconnector_config_merge(msconnector_config *out, const msconnector_config *parent, const msconnector_config *child);
int msconnector_config_validate(const msconnector_config *config, char *error, size_t error_len);

#ifdef __cplusplus
}
#endif

#endif
