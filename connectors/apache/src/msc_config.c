
#include "mod_security3.h"
#include "msc_config.h"
#include "msc_filters.h"
#include "msconnector/config.h"
#include "msconnector/config_parser.h"
#include "msconnector/directive_adapter.h"
#include "msconnector/directives.h"
#include "msconnector/options.h"

#include <stdlib.h>
#include <string.h>


static const msconnector_directive_adapter_entry *apache_directive_adapter(const char *name)
{
    return msconnector_directive_adapter_find(name);
}

const command_rec module_directives[] =
{
    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_MODSECURITY,
        msc_config_modsec_state,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "The argument must be either 'On' or 'Off'"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_RULES,
        msc_config_load_rules,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Please ensure that the arugment is specified correctly, including line continuations."
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_RULES_FILE,
        msc_config_load_rules_file,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Load ModSecurity rules from a file"
    ),

    AP_INIT_TAKE2(
        MSCONNECTOR_DIRECTIVE_RULES_REMOTE,
        msc_config_load_rules_remote,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Load ModSecurity rules from a remote server"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_TRANSACTION_ID,
        msc_config_transaction_id,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Set a static ModSecurity transaction ID for this Apache context"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_TRANSACTION_ID_EXPR,
        msc_config_transaction_id_expr,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Set a per-request Apache expression for the ModSecurity transaction ID"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_USE_ERROR_LOG,
        msc_config_use_error_log,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Enable or disable forwarding libmodsecurity log messages to the Apache error log"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_PHASE4_MODE,
        msc_config_phase4_mode,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Phase 4 handling mode: minimal, safe, or strict"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_PHASE4_CONTENT_TYPES_FILE,
        msc_config_phase4_content_types_file,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Load Phase 4 response body MIME types from a file"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_PHASE4_LOG,
        msc_config_phase4_log,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Write Phase 4 connector decisions as JSON lines"
    ),

    AP_INIT_TAKE1(
        MSCONNECTOR_DIRECTIVE_PHASE4_BODY_LIMIT,
        msc_config_phase4_body_limit,
        NULL,
        RSRC_CONF | ACCESS_CONF,
        "Bound Apache connector response-body buffering for Phase 4"
    ),

    {NULL}
};


static const char *msc_config_modsec_state(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    (void)apache_directive_adapter(MSCONNECTOR_DIRECTIVE_MODSECURITY);

    if (!msconnector_parse_bool(p1, &cnf->common_config.enable))
    {
        return "ModSecurity state must be either 'On' or 'Off'";
    }

    return NULL;
}


static const char *msc_config_load_rules(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    const char *error = NULL;
    int ret;

    ret = msc_rules_add(cnf->rules_set, p1, &error);

    if (ret < 0)
    {
        return error;
    }

    msconnector_rule_load_stats_add_inline(&cnf->rule_load_stats,
        (unsigned) ret);

    return NULL;
}


static const char *msc_config_load_rules_file(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    const char *error = NULL;
    int ret;

    ret = msc_rules_add_file(cnf->rules_set, p1, &error);

    if (ret < 0)
    {
        return error;
    }

    msconnector_rule_load_stats_add_file(&cnf->rule_load_stats,
        (unsigned) ret);

    return NULL;
}


static const char *msc_config_load_rules_remote(cmd_parms *cmd, void *_cnf,
    const char *p1, const char *p2)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    const char *error = NULL;
    int ret;

    ret = msc_rules_add_remote(cnf->rules_set, p1, p2, &error);

    if (ret < 0)
    {
        return error;
    }

    msconnector_rule_load_stats_add_remote(&cnf->rule_load_stats,
        (unsigned) ret);

    return NULL;
}


static const char *msc_config_transaction_id(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;

    if (p1 == NULL || p1[0] == '\0')
    {
        return "modsecurity_transaction_id must not be empty";
    }

    if (cnf->transaction_id_expr != NULL)
    {
        return "modsecurity_transaction_id and modsecurity_transaction_id_expr are mutually exclusive";
    }

    cnf->common_config.transaction_id = apr_pstrdup(cmd->pool, p1);
    return NULL;
}


static const char *msc_config_transaction_id_expr(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    const char *error = NULL;
    ap_expr_info_t *expr = NULL;

    if (p1 == NULL || p1[0] == '\0')
    {
        return "modsecurity_transaction_id_expr must not be empty";
    }

    if (cnf->common_config.transaction_id != NULL)
    {
        return "modsecurity_transaction_id and modsecurity_transaction_id_expr are mutually exclusive";
    }

    expr = ap_expr_parse_cmd(cmd, p1, AP_EXPR_FLAG_STRING_RESULT,
        &error, NULL);
    if (error != NULL)
    {
        return apr_pstrcat(cmd->pool,
            "modsecurity_transaction_id_expr parse error: ", error, NULL);
    }

    cnf->transaction_id_expr = expr;
    cnf->common_config.transaction_id_expr = p1;
    return NULL;
}


static const char *msc_config_use_error_log(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    enum msconnector_bool_option parsed;

    if (!msconnector_parse_bool(p1, &parsed))
    {
        return "modsecurity_use_error_log must be either 'on' or 'off'";
    }

    cnf->common_config.use_error_log = parsed;
    return NULL;
}


static const char *msc_config_phase4_mode(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    enum msconnector_phase4_mode parsed;

    if (!msconnector_parse_phase4_mode(p1, &parsed))
    {
        return "modsecurity_phase4_mode must be minimal, safe, or strict";
    }

    cnf->common_config.phase4_mode = parsed;
    return NULL;
}


static const char *msc_config_phase4_content_types_file(cmd_parms *cmd,
    void *_cnf, const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    apr_file_t *file = NULL;
    char line[512];
    apr_status_t rc;

    if (p1 == NULL || p1[0] == '\0')
    {
        return "modsecurity_phase4_content_types_file must not be empty";
    }

    cnf->common_config.phase4_content_types_file = apr_pstrdup(cmd->pool, p1);
    cnf->phase4_content_types = apr_array_make(cmd->pool, 8,
        sizeof(const char *));
    if (cnf->phase4_content_types == NULL)
    {
        return "failed to allocate phase4 content-type list";
    }

    rc = apr_file_open(&file, p1, APR_READ, APR_OS_DEFAULT, cmd->pool);
    if (rc != APR_SUCCESS)
    {
        return apr_psprintf(cmd->pool,
            "failed to open modsecurity_phase4_content_types_file: %s", p1);
    }

    while (apr_file_gets(line, sizeof(line), file) == APR_SUCCESS)
    {
        char *start = line;
        char *end;
        char *comment;

        while (*start != '\0' && apr_isspace(*start))
        {
            start++;
        }
        comment = strchr(start, '#');
        if (comment != NULL)
        {
            *comment = '\0';
        }
        comment = strchr(start, ';');
        if (comment != NULL)
        {
            *comment = '\0';
        }
        for (end = start; *end != '\0'; end++)
        {
            /* Advance to the end so trailing whitespace can be trimmed below. */
        }
        while (end > start && apr_isspace(*(end - 1)))
        {
            end--;
        }
        *end = '\0';
        if (*start == '\0')
        {
            continue;
        }
        *(const char **)apr_array_push(cnf->phase4_content_types) =
            apr_pstrdup(cmd->pool, start);
    }

    apr_file_close(file);
    return NULL;
}


static const char *msc_config_phase4_log(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;

    if (p1 == NULL || p1[0] == '\0')
    {
        return "modsecurity_phase4_log must not be empty";
    }

    cnf->common_config.phase4_log_path = apr_pstrdup(cmd->pool, p1);
    return NULL;
}


static const char *msc_config_phase4_body_limit(cmd_parms *cmd, void *_cnf,
    const char *p1)
{
    msc_conf_t *cnf = (msc_conf_t *) _cnf;
    size_t value;

    if (!msconnector_parse_size(p1, &value) || value == 0U)
    {
        return "modsecurity_phase4_body_limit must be a positive integer";
    }

    cnf->common_config.phase4_body_limit = value;
    return NULL;
}



void *msc_hook_create_config_directory(apr_pool_t *mp, char *path)
{
    msc_conf_t *cnf = NULL;

    cnf = apr_pcalloc(mp, sizeof(msc_conf_t));
    if (cnf == NULL)
    {
        goto end;
    }
#if 0
    ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
        "ModSecurity: Created directory config for path: %s [%pp]", path, cnf);
#endif

    cnf->rules_set = msc_create_rules_set();
    msconnector_config_init(&cnf->common_config);
    cnf->transaction_id_expr = NULL;
    cnf->phase4_content_types = NULL;
    msconnector_rule_load_stats_init(&cnf->rule_load_stats);
    if (cnf->rules_set == NULL)
    {
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Failed to create rules set for directory config");
        return NULL;
    }

    if (path != NULL)
    {
        cnf->name_for_debug = strdup(path);
    }
#if 0
    ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
        "ModSecurity: Config for path: %s is at: %pp", path, cnf);
#endif

end:
    return cnf;
}


void *msc_hook_merge_config_directory(apr_pool_t *mp, void *parent,
    void *child)
{
    msc_conf_t *cnf_p = parent;
    msc_conf_t *cnf_c = child;
    msc_conf_t *cnf_new = (msc_conf_t *)msc_hook_create_config_directory(mp,
        (cnf_c != NULL) ? cnf_c->name_for_debug : NULL);

    if (cnf_new == NULL)
    {
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Failed to create merged directory config");
        return NULL;
    }

    if (cnf_p && cnf_c)
    {
        const char *error = NULL;
        int ret;
#if 0
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Merge parent %pp [%s] child %pp [%s]" \
            "into: %pp", cnf_p,
            cnf_p->name_for_debug,
            child, cnf_c->name_for_debug, cnf_new);
#endif
        cnf_new->name_for_debug = cnf_c->name_for_debug;

        ret = msc_rules_merge(cnf_new->rules_set, cnf_c->rules_set, &error);
        if (ret < 0)
        {
            ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
                "ModSecurity: Rule merge failed: %s", error);
            return NULL;
        }

        ret = msc_rules_merge(cnf_new->rules_set, cnf_p->rules_set, &error);
        if (ret < 0)
        {
            ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
                "ModSecurity: Rule merge failed: %s", error);
            return NULL;
        }
#if 0
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
                "ModSecurity: Merge OK");
#endif
    }
    else if (cnf_c && !cnf_p)
    {
#if 0
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Merge parent -NULL- [-NULL-] child %pp [%s]",
            cnf_c, cnf_c->name_for_debug);
#endif
    }
    else if (cnf_p && !cnf_c)
    {
#if 0
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Merge parent %pp [%s] child -NULL- [-NULL-]",
            cnf_p, cnf_p->name_for_debug);
#endif
    }

    if (!msconnector_config_merge(&cnf_new->common_config,
        cnf_p != NULL ? &cnf_p->common_config : NULL,
        cnf_c != NULL ? &cnf_c->common_config : NULL))
    {
        char error[256];
        (void)msconnector_config_validate(&cnf_new->common_config,
            error, sizeof(error));
        ap_log_perror(APLOG_MARK, APLOG_STARTUP|APLOG_NOERRNO, 0, mp,
            "ModSecurity: Common config merge failed: %s", error);
        return NULL;
    }

    if (cnf_c != NULL && cnf_c->transaction_id_expr != NULL)
    {
        cnf_new->transaction_id_expr = cnf_c->transaction_id_expr;
    }
    else if (cnf_p != NULL && cnf_p->transaction_id_expr != NULL)
    {
        cnf_new->transaction_id_expr = cnf_p->transaction_id_expr;
    }

    if (cnf_c != NULL && cnf_c->phase4_content_types != NULL)
    {
        cnf_new->phase4_content_types = cnf_c->phase4_content_types;
    }
    else if (cnf_p != NULL && cnf_p->phase4_content_types != NULL)
    {
        cnf_new->phase4_content_types = cnf_p->phase4_content_types;
    }

    if (cnf_p != NULL)
    {
        msconnector_rule_load_stats_add(&cnf_new->rule_load_stats,
            &cnf_p->rule_load_stats);
    }

    if (cnf_c != NULL)
    {
        msconnector_rule_load_stats_add(&cnf_new->rule_load_stats,
            &cnf_c->rule_load_stats);
    }

    return cnf_new;
}
