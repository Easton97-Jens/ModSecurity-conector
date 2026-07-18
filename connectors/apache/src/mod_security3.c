
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mod_security3.h"
#include "msc_utils.h"
#include "msc_config.h"
#include "msconnector/limits.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"

/*
 *
 */
msc_global *msc_apache;

static apr_status_t msc_module_cleanup(void *data);
static int hook_connection_early(conn_rec *conn);
static int msc_hook_pre_config(apr_pool_t *mp, apr_pool_t *mp_log,
    apr_pool_t *mp_temp);
static int msc_hook_post_config(apr_pool_t *mp, apr_pool_t *mp_log,
    apr_pool_t *mp_temp, server_rec *s);
static int hook_request_late(request_rec *r);
static int hook_request_early(request_rec *r);
static int hook_log_transaction(request_rec *r);
static void hook_insert_filter(request_rec *r);
static int process_request_headers(request_rec *r, msc_t *msr);


static int apache_phase4_redirect_has_local_error_document_proof(
    const msc_t *msr, request_rec *r)
{
    const char *redirect_status;
    const char *previous_status;

    if (msr == NULL || r == NULL || r->prev == NULL)
    {
        return 0;
    }

    /* ap_die() marks a local ErrorDocument predecessor no_local_copy and
     * records its status in REDIRECT_STATUS. Require that Apache-core-derived
     * pair, even when the Phase-4 gate itself initiated the error. 3xx is
     * included for a legitimate redirect intervention with a local
     * ErrorDocument; 1xx/2xx cannot be a terminal intervention. An
     * unconditional gate-failed exception would let a nested or unrelated
     * producer redirect escape while the protocol guard is EMITTING. */
    if (!r->prev->no_local_copy || r->subprocess_env == NULL ||
        !(ap_is_HTTP_ERROR(r->prev->status) ||
            (r->prev->status >= HTTP_MULTIPLE_CHOICES &&
                r->prev->status < HTTP_BAD_REQUEST)))
    {
        return 0;
    }
    redirect_status = apr_table_get(r->subprocess_env, "REDIRECT_STATUS");
    previous_status = apr_itoa(r->pool, r->prev->status);
    return redirect_status != NULL && previous_status != NULL &&
        strcmp(redirect_status, previous_status) == 0 &&
        !msr->response_phase4_terminal_error_redirect_seen;
}


static int apache_phase4_redirect_is_terminal_error_emission(msc_t *msr,
    request_rec *r)
{
    if (msr == NULL || msr->response_phase4_terminal_output !=
            MSC_PHASE4_TERMINAL_OUTPUT_EMITTING ||
        !apache_phase4_redirect_has_local_error_document_proof(msr, r))
    {
        return 0;
    }
    msr->response_phase4_terminal_error_redirect_seen = 1;
    return 1;
}


static void apache_phase4_fail_normal_redirect(msc_t *msr,
    request_rec *r, const char *reason)
{
    if (msr != NULL)
    {
        msc_discard_response_brigade(msr);
        msr->response_phase4_gate_failed = 1;
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
    }
    if (r == NULL || r->connection == NULL)
    {
        return;
    }
    ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
        "ModSecurity: refusing normal internal redirect across the Phase 4 response boundary: %s",
        reason != NULL ? reason : "request transaction cannot be safely rebound");
    r->connection->keepalive = AP_CONN_CLOSE;
    r->connection->aborted = 1;
}


void modsecurity_log_cb(void *log, const void* data)
{
    const char *msg;
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH + 1U];
    if (log == NULL || data == NULL) {
        return;
    }
    msg = (const char *) data;
    request_rec *r = (request_rec *) log;
    msc_conf_t *conf = NULL;
    msc_t *msr = NULL;

    msr = (msc_t *)apr_table_get(r->notes, NOTE_MSR);
    rule_id[0] = '\0';
    if (msr != NULL && msr->native_event_phase_active &&
        (msr->native_event_phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
         msr->native_event_phase == MSCONNECTOR_PHASE_REQUEST_BODY) &&
        msconnector_rule_id_extract_from_message(msg, rule_id,
            sizeof(rule_id)) > 0)
    {
        apache_log_rule_match_event(msr, r, msr->native_event_phase, rule_id);
    }

    if (r->per_dir_config != NULL) {
        conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
                &security3_module);
        if (conf != NULL && conf->common_config.use_error_log == MSCONNECTOR_BOOL_OFF) {
            return;
        }
    }

#if AP_SERVER_MAJORVERSION_NUMBER > 1 && AP_SERVER_MINORVERSION_NUMBER > 2
    ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
        "%s", msg);

#else
    ap_log_error(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r->server,
        "%s", msg);
#endif

}

int process_intervention (Transaction *t, request_rec *r)
{
    ModSecurityIntervention intervention;
    msc_t *msr = NULL;
    intervention.status = N_INTERVENTION_STATUS;
    intervention.url = NULL;
    intervention.log = NULL;
    intervention.disruptive = 0;

    int z = msc_intervention(t, &intervention);

    if (z == 0)
    {
        return N_INTERVENTION_STATUS;
    }

    if (intervention.log == NULL)
    {
        intervention.log = "(no log message was specified)";
    }

    msr = (msc_t *)apr_table_get(r->notes, NOTE_MSR);
    if (msr != NULL)
    {
        msr->last_intervention_status = intervention.status;
        msr->last_intervention_log = apr_pstrdup(r->pool, intervention.log);
        msr->phase4_intervention = intervention.disruptive ? 1 : msr->phase4_intervention;
    }

    if (intervention.status == 301 || intervention.status == 302
        ||intervention.status == 303 || intervention.status == 307)
    {
        if (intervention.url != NULL)
        {
            apr_table_setn(r->headers_out, "Location", intervention.url);
            return HTTP_MOVED_TEMPORARILY;
        }
    }

    if (intervention.status != N_INTERVENTION_STATUS)
    {
        return intervention.status;
    }

    return N_INTERVENTION_STATUS;
}


/*
 * Called only once. Used to initialise the ModSecurity
 *
 */
int msc_apache_init(apr_pool_t *mp)
{
    msc_apache = apr_pcalloc(mp, sizeof(msc_global));
    if (msc_apache == NULL)
    {
        goto err_no_mem;
    }

    msc_apache->modsec = msc_init();

    msc_set_connector_info(msc_apache->modsec, MSC_APACHE_CONNECTOR);

    apr_pool_cleanup_register(mp, NULL, msc_module_cleanup, apr_pool_cleanup_null);

    msc_set_log_cb(msc_apache->modsec, modsecurity_log_cb);

    return 0;

err_no_mem:
    return -1;
}


/*
 * Called only once. Used to cleanup ModSecurity
 *
 */
int msc_apache_cleanup()
{
    msc_cleanup(msc_apache->modsec);
}


/*
 * Used to cleanup the module
 *
 */
static apr_status_t msc_module_cleanup(void *data)
{
    msc_apache_cleanup();
    return APR_SUCCESS;
}



/**
 * Stores transaction context where it can be found in subsequent
 * phases, redirections, or subrequests.
 */
static void store_tx_context(msc_t *msr, request_rec *r)
{
    apr_table_setn(r->notes, NOTE_MSR, (void *)msr);
}


static msc_t *create_tx_context(request_rec *r) {
    msc_t *msr = NULL;
    msc_conf_t *z = NULL;
    char *unique_id = NULL;
    const char *transaction_id = NULL;
    const char *expr_error = NULL;

    z = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
            &security3_module);

    if (z == NULL || z->common_config.enable != MSCONNECTOR_BOOL_ON) {
        return NULL;
    }

    msr = (msc_t *)apr_pcalloc(r->pool, sizeof(msc_t));
    if (msr == NULL) {
        return NULL;
    }

    msr->r = r;
    if (z->transaction_id_expr != NULL) {
        transaction_id = ap_expr_str_exec(r, z->transaction_id_expr,
            &expr_error);
        if (expr_error != NULL) {
            ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                "ModSecurity: Failed to evaluate "
                "modsecurity_transaction_id_expr: %s", expr_error);
            transaction_id = NULL;
        }
    } else if (z->common_config.transaction_id != NULL
        && z->common_config.transaction_id[0] != '\0') {
        transaction_id = z->common_config.transaction_id;
    }

    if (transaction_id == NULL || transaction_id[0] == '\0') {
        unique_id = getenv("UNIQUE_ID");
        if (unique_id != NULL && unique_id[0] != '\0') {
            transaction_id = unique_id;
        }
    }

    if (transaction_id != NULL && transaction_id[0] != '\0') {
        msr->t = msc_new_transaction_with_id(msc_apache->modsec,
            z->rules_set, transaction_id, (void *)r);
    } else {
        msr->t = msc_new_transaction(msc_apache->modsec,
            z->rules_set, (void *)r);
    }
    if (msr->t == NULL)
    {
        return NULL;
    }
    if (transaction_id != NULL && transaction_id[0] != '\0') {
        msr->event_transaction_id = apr_pstrdup(r->pool, transaction_id);
    } else {
        msr->event_transaction_id = apr_psprintf(r->pool, "%ld-%ld",
            (long)r->request_time, (long)r->connection->id);
    }

    msr->owner_request = r;
    store_tx_context(msr, r);
    apr_pool_cleanup_register(r->pool, msr,
        msc_cleanup_request_transaction, apr_pool_cleanup_null);

    return msr;
}


/**
 * Retrieves a previously stored transaction context by
 * looking at the main request, and the previous requests.
 */
static msc_t *retrieve_tx_context(request_rec *r) {
    msc_t *msr = NULL;
    request_rec *rx = NULL;

    /* Look in the current request first. */
    msr = (msc_t *)apr_table_get(r->notes, NOTE_MSR);
    if (msr != NULL)
    {
        msr->r = r;
        return msr;
    }

    /* If this is a subrequest then look in the main request. */
    if (r->main != NULL)
    {
        msr = (msc_t *)apr_table_get(r->main->notes, NOTE_MSR);
        if (msr != NULL)
        {
            msr->r = r;
            return msr;
        }
    }

    /* If the request was redirected then look in the previous requests. */
    rx = r->prev;
    while (rx != NULL)
    {
        msr = (msc_t *)apr_table_get(rx->notes, NOTE_MSR);
        if (msr != NULL)
        {
            msr->r = r;
            return msr;
        }
        rx = rx->prev;
    }

    return NULL;
}


static int msc_hook_pre_config(apr_pool_t *mp, apr_pool_t *mp_log,
    apr_pool_t *mp_temp)
{
    void *data = NULL;
    const char *key = "modsecurity-pre-config-init-flag";
    int first_time = 0;

    /* Figure out if we are here for the first time */
    apr_pool_userdata_get(&data, key, mp);
    if (data == NULL)
    {
        apr_pool_userdata_set((const void *) 1, key,
                apr_pool_cleanup_null, mp);
        first_time = 1;
    }

    if (!first_time)
    {
        return OK;
    }

    // Code to run only at the very first call.
    int ret = msc_apache_init(mp);

    if (ret == -1)
    {
        ap_log_error(APLOG_MARK, APLOG_STARTUP, 0, NULL,
                "ModSecurity: Failed to initialise.");
        return HTTP_INTERNAL_SERVER_ERROR;
    }

    return OK;
}


static int msc_hook_post_config(apr_pool_t *mp, apr_pool_t *mp_log,
    apr_pool_t *mp_temp, server_rec *s)
{
    void *data = NULL;
    const char *key = "modsecurity-post-config-init-flag";
    int first_time = 0;

    /* Figure out if we are here for the first time */
    apr_pool_userdata_get(&data, key, s->process->pool);
    if (data == NULL)
    {
        apr_pool_userdata_set((const void *) 1, key,
            apr_pool_cleanup_null, s->process->pool);
        first_time = 1;
    }

    if (!first_time)
    {
        return OK;
    }

    // Code to run only at the very first call.
    ap_log_error(APLOG_MARK, APLOG_NOTICE | APLOG_NOERRNO, 0, s,
                "ModSecurity: %s configured.", MSC_APACHE_CONNECTOR);

    return OK;
}



static int hook_connection_early(conn_rec *conn)
{
    // At this point there isn't a request_rec attached to the request,
    // therefore we can't create the config yet, lets wait till next phase.

    return DECLINED;
}


#if AP_SERVER_MAJORVERSION_NUMBER > 1 && AP_SERVER_MINORVERSION_NUMBER < 3
static const char *msc_apache_client_ip(request_rec *r)
{
    return r->connection->remote_ip;
}


static int msc_apache_client_port(request_rec *r)
{
    return r->connection->remote_addr->port;
}
#else
static const char *msc_apache_client_ip(request_rec *r)
{
    if (r->useragent_ip != NULL) {
        return r->useragent_ip;
    }

    return r->connection->client_ip;
}


static int msc_apache_client_port(request_rec *r)
{
    if (r->useragent_addr != NULL) {
        return r->useragent_addr->port;
    }

    if (r->connection->client_addr != NULL) {
        return r->connection->client_addr->port;
    }

    return 0;
}
#endif


/**
 * Initial request processing, executed immediatelly after
 * Apache receives the request headers. This function wil create
 * a transaction context.
 */
static int hook_request_early(request_rec *r) {
    msc_t *msr = NULL;
    int rc = DECLINED;
    const char *client_ip = msc_apache_client_ip(r);
    int client_port = msc_apache_client_port(r);

    /* This function needs to run only once per transaction
     * (i.e. subrequests and redirects are excluded).
     */
    if ((r->main != NULL) || (r->prev != NULL)) {
        return DECLINED;
    }

    /* Initialise transaction context and
     * create the initial configuration.
     */
#ifdef REQUEST_EARLY
#error "Request Early is not ready for v3 yet."
    msr = create_tx_context(r);
    if (msr == NULL)
    {
        return DECLINED;
    }
#endif

#ifndef LATE_CONNECTION_PROCESS
#error "Currently in v3 connection can only be processed late."
    msc_process_connection(msr->t, client_ip,
        client_port,
        r->server->server_hostname,
        (int) r->server->port);

    it = process_intervention(msr->t, r);
    if (it != N_INTERVENTION_STATUS)
    {
        return it;
    }
#endif

#ifdef REQUEST_EARLY
    it = process_request_headers(r, msr);
    if (it != N_INTERVENTION_STATUS)
    {
        return it;
    }
#endif

    return rc;
}

/**
 * Invoked as the first hook in the handler chain, this function
 * executes the second phase of ModSecurity request processing.
 */
static int hook_request_late(request_rec *r)
{
    msc_t *msr = NULL;
    int it;
    const char *client_ip = msc_apache_client_ip(r);
    int client_port = msc_apache_client_port(r);

    /* This function needs to run only once per transaction
     * (i.e. subrequests and redirects are excluded).
     */
    if ((r->main != NULL) || (r->prev != NULL))
    {
        return DECLINED;
    }

    /* Find the transaction context and make sure
     * we are supposed to proceed.
     */
#ifdef REQUEST_EARLY
    msr = retrieve_tx_context(r);
#else
    msr = create_tx_context(r);
#endif
    if (msr == NULL)
    {
        /* If we can't find the context that probably means it's
         * a subrequest that was not initiated from the outside.
         */
        return DECLINED;
    }

#ifdef LATE_CONNECTION_PROCESS
    msc_process_connection(msr->t, client_ip,
        client_port,
        r->server->server_hostname,
        (int) r->server->port);

    it = process_intervention(msr->t, r);
    if (it != N_INTERVENTION_STATUS)
    {
        return it;
    }
#endif

#ifndef REQUEST_EARLY
    it = process_request_headers(r, msr);
    if (it != N_INTERVENTION_STATUS)
    {
        return it;
    }
#endif

    /* No-body requests have no input EOS to drive the filter.  Complete P2
     * here; requests that advertise a body remain streaming until
     * MODSECURITY_IN receives EOS (or Apache drains an unread body). */
    if (!ap_request_has_body(r))
    {
        it = msc_finalize_request_body(msr, r);
        if (it != N_INTERVENTION_STATUS)
        {
            return it;
        }
    }

    return DECLINED;
}


/**
 * Invoked at the end of each transaction.
 */
static int hook_log_transaction(request_rec *r)
{
    const apr_array_header_t *arr = NULL;
    request_rec *origr = NULL;
    msc_t *msr = NULL;
    int it;

    msr = retrieve_tx_context(r);
    if (msr == NULL)
    {
        return DECLINED;
    }

    msc_update_status_code(msr->t, r->status);
    msc_process_logging(msr->t);
    it = process_intervention(msr->t, r);
    if (it != N_INTERVENTION_STATUS)
    {
        return it;
    }

    return DECLINED;
}


/**
 * Invoked right before request processing begins. This is
 * when we need to decide if we want to hook into the output
 * filter chain.
 */
static void hook_insert_filter(request_rec *r)
{
    msc_t *msr = NULL;

    /* Find the transaction context first. */
    msr = retrieve_tx_context(r);
    if (msr == NULL)
    {
        return;
    }

#if 1
    /* Add the input filter, but only if we need it to run. */
    ap_add_input_filter("MODSECURITY_IN", msr, r, r->connection);
#endif

    /* A subrequest must not share the primary response lifecycle. */
    if (r->main != NULL)
    {
        return;
    }

    /* Apache internal redirects preserve protocol filters but replace the
     * resource/content chain and request target. The native transaction has
     * already processed the source URI, request headers, and body; the C API
     * cannot rewind or safely rebind it to the target request. Reattaching
     * MODSECURITY_OUT would therefore evaluate target response bytes against
     * stale request variables or a stale RulesSet. Fail closed for every
     * normal redirect. Apache's own synchronous ErrorDocument is the only
     * exception: it is a bounded terminal emission already protected by the
     * existing protocol guard while it is EMITTING. */
    if (r->prev != NULL)
    {
        if (!apache_phase4_redirect_is_terminal_error_emission(msr, r))
        {
            apache_phase4_fail_normal_redirect(msr, r,
                "request transaction cannot be safely rebound to the target URI");
        }
        return;
    }


    /* Keep a terminal Phase-4 guard in the protocol chain as well as the
     * body filter in the content chain. Apache discards resource filters when
     * it emits an error response, while the protocol guard remains attached
     * to this request and seals invalid later producer output. */
    if (ap_add_output_filter("MODSECURITY_PHASE4_GUARD", msr, r,
            r->connection) == NULL)
    {
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: unable to install the mandatory Phase 4 terminal guard; aborting request");
        r->connection->aborted = 1;
        return;
    }
    if (ap_add_output_filter("MODSECURITY_OUT", msr, r,
            r->connection) == NULL)
    {
        /* The protocol guard alone cannot perform the Phase-4 body decision.
         * Keep it sealed and fail closed rather than allowing an unavailable
         * content filter to turn the response path into an uninspected pass. */
        msr->response_phase4_gate_failed = 1;
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: unable to install the mandatory Phase 4 content filter; aborting request");
        r->connection->keepalive = AP_CONN_CLOSE;
        r->connection->aborted = 1;
        return;
    }
}


static int process_request_headers(request_rec *r, msc_t *msr) {
    /* process uri */
    {
        int it;
        int offset = (r->protocol != NULL
            && r->protocol[0] == 'H'
            && r->protocol[1] != '\0'
            && r->protocol[2] != '\0'
            && r->protocol[3] != '\0'
            && r->protocol[4] != '\0'
            && r->protocol[5] != '\0') ? 5 : 0;

        msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
        msr->native_event_phase_active = 1;
        msc_process_uri(msr->t, r->unparsed_uri, r->method, r->protocol + offset);
        msr->native_event_phase_active = 0;
        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            const char *action = msr->last_intervention_status >= 300 &&
                msr->last_intervention_status < 400 ? "redirect" : "deny";

            apache_emit_intervention_event(msr, r, "phase1_intervention",
                MSCONNECTOR_PHASE_REQUEST_HEADERS, action, action,
                "request_uri_before_request_headers", r->status, 0);
            return it;
        }
    }

    /* add request headers */
    {
        const apr_array_header_t *arr = NULL;
        const apr_table_entry_t *te = NULL;
        int i;
        int it;

        arr = apr_table_elts(r->headers_in);
        te = (apr_table_entry_t *)arr->elts;
        for (i = 0; i < arr->nelts; i++)
        {
            const char *key = te[i].key;
            const char *val = te[i].val;
            msc_add_request_header(msr->t, key, val);
        }
        msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
        msr->native_event_phase_active = 1;
        msc_process_request_headers(msr->t);
        msr->native_event_phase_active = 0;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            const char *action = msr->last_intervention_status >= 300 &&
                msr->last_intervention_status < 400 ? "redirect" : "deny";

            /* The native request-header hook has not handed control to a
             * handler yet.  Write this bounded event in the same real host
             * path that returns the HTTP intervention to Apache. */
            apache_emit_intervention_event(msr, r, "phase1_intervention",
                MSCONNECTOR_PHASE_REQUEST_HEADERS, action, action,
                "request_headers_before_handler", r->status, 0);
            return it;
        }
    }

    return N_INTERVENTION_STATUS;
}



static void msc_register_hooks(apr_pool_t *pool)
{
    static const char *const postconfig_beforeme_list[] = {
        "mod_unique_id.c",
        "mod_ssl.c",
        NULL
    };

    static const char *const postconfig_afterme_list[] = {
        "mod_fcgid.c",
        "mod_cgid.c",
        NULL
    };

    static const char *const postread_beforeme_list[] = {
        "mod_rpaf.c",
        "mod_rpaf-2.0.c",
        "mod_extract_forwarded.c",
        "mod_extract_forwarded2.c",
        "mod_remoteip.c",
        "mod_custom_header.c",
        "mod_breach_realip.c",
        "mod_breach_trans.c",
        "mod_unique_id.c",
        NULL
    };

    static const char *const postread_afterme_list[] = {
        "mod_log_forensic.c",
        NULL
    };

    static const char *const transaction_afterme_list[] = {
        "mod_log_config.c",
        NULL
    };

    static const char *const fixups_beforeme_list[] = {
        "mod_env.c",
        NULL
    };

    /* Module initialization */
    ap_hook_pre_config(msc_hook_pre_config, NULL, NULL, APR_HOOK_FIRST);
    ap_hook_post_config(msc_hook_post_config, postconfig_beforeme_list,
        postconfig_afterme_list, APR_HOOK_REALLY_LAST);


    /* Connection processing hooks - only global configuration. */
    ap_hook_post_read_request(hook_request_early,
        postread_beforeme_list, postread_afterme_list, APR_HOOK_REALLY_FIRST);

    /* still, we don't have location configuration yet. */
    ap_hook_process_connection(hook_connection_early, NULL, NULL, APR_HOOK_FIRST);

    ap_hook_fixups(hook_request_late, fixups_beforeme_list, NULL, APR_HOOK_REALLY_FIRST);

    /* Lets add the remaining hooks */
    ap_hook_insert_filter(hook_insert_filter, NULL, NULL, APR_HOOK_FIRST);

    /* Logging */
    /* ap_hook_error_log is called for every error log entry that apache writes.
     * may not be necessary in our particular case. Disabling for now.
     *
     * ap_hook_error_log(hook_error_log, NULL, NULL, APR_HOOK_MIDDLE);
     *
     */
    ap_hook_log_transaction(hook_log_transaction, NULL, transaction_afterme_list, APR_HOOK_MIDDLE);

    /* request body */
    ap_register_input_filter("MODSECURITY_IN", input_filter,
        NULL, AP_FTYPE_CONTENT_SET);

    /* response body */
    ap_register_output_filter("MODSECURITY_OUT", output_filter,
        NULL, AP_FTYPE_CONTENT_SET - 3);
    ap_register_output_filter("MODSECURITY_PHASE4_GUARD",
        phase4_terminal_guard_filter, NULL, AP_FTYPE_PROTOCOL);
}



module AP_MODULE_DECLARE_DATA security3_module =
{
    STANDARD20_MODULE_STUFF,
    msc_hook_create_config_directory,  // Per-directory configuration.
    msc_hook_merge_config_directory,   // Merge handler for per-directory.
    NULL,                              // Per-server conf handler.
    NULL,                              // Merge handler for per-server
                                       // configurations.
    module_directives,
    msc_register_hooks
};
