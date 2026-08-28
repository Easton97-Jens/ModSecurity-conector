
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <apr_time.h>

#include "mod_security3.h"
#include "msc_utils.h"
#include "msc_config.h"
#include "msconnector/limits.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"
#include "connectors/profile_registry.h"

/*
 *
 */
msc_global *msc_apache;

/* Apache creates a new notes table for every internal redirect. Keep the
 * one permitted ErrorDocument transition bound to the exact request that
 * passed the core-derived proof below. */
static const char apache_phase4_terminal_error_redirect_note[] =
    "modsecurity-phase4-terminal-error-redirect";

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

static uint64_t apache_contract_now_ms(void)
{
    apr_time_t now = apr_time_now();

    /* APR exposes a wall-clock timestamp here, not a monotonic one.  It is
     * therefore retained only as bounded lifecycle evidence; the Common FSM
     * still owns ordering and never infers phase validity from this value. */
    if (now <= 0) {
        return 0U;
    }
    return (uint64_t)(now / (APR_USEC_PER_SEC / 1000));
}

int msc_apache_contract_begin(msc_t *msr, enum msconnector_phase phase)
{
    if (msr == NULL || !msr->contract_initialized)
        return 0;
    return msconnector_transaction_contract_begin_phase(&msr->contract,
        phase, apache_contract_now_ms()) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msc_apache_contract_complete(msc_t *msr, enum msconnector_phase phase)
{
    if (msr == NULL || !msr->contract_initialized)
        return 0;
    return msconnector_transaction_contract_complete_phase(&msr->contract,
        phase, apache_contract_now_ms()) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

static int apache_header_table_metrics(const apr_table_t *headers,
    size_t *count, size_t *bytes)
{
    const apr_array_header_t *entries;
    const apr_table_entry_t *header;
    int index;

    if (headers == NULL || count == NULL || bytes == NULL) {
        return headers == NULL;
    }
    entries = apr_table_elts(headers);
    if (entries == NULL || entries->elts == NULL) {
        return 1;
    }
    header = (const apr_table_entry_t *)entries->elts;
    for (index = 0; index < entries->nelts; ++index) {
        size_t name_size = header[index].key == NULL ? 0U : strlen(header[index].key);
        size_t value_size = header[index].val == NULL ? 0U : strlen(header[index].val);

        if (name_size == 0U || name_size > MSCONNECTOR_MAX_HEADER_NAME_LENGTH ||
            value_size > MSCONNECTOR_MAX_HEADER_VALUE_LENGTH ||
            *count >= MSCONNECTOR_MAX_HEADER_COUNT ||
            name_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes ||
            value_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes - name_size) {
            return 0;
        }
        ++*count;
        *bytes += name_size + value_size;
    }
    return 1;
}

int msc_apache_contract_record_request_metadata(msc_t *msr, request_rec *r)
{
    msc_conf_t *conf;
    size_t header_count = 0U;
    size_t header_bytes = 0U;
    const char *content_type;
    size_t body_limit;

    if (msr == NULL || r == NULL || !msr->contract_initialized ||
        r->per_dir_config == NULL) {
        return 0;
    }
    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL) {
        return 0;
    }
    if (!apache_header_table_metrics(r->headers_in, &header_count, &header_bytes)) {
        return 0;
    }
    content_type = r->headers_in == NULL ? NULL :
        apr_table_get(r->headers_in, "Content-Type");
    body_limit = conf->common_config.request_body_limit > 0U ?
        conf->common_config.request_body_limit : MSCONNECTOR_MAX_BODY_BUFFER_SIZE;
    return msconnector_transaction_contract_record_request_metadata(&msr->contract,
        r->method == NULL ? "GET" : r->method,
        r->unparsed_uri == NULL || r->unparsed_uri[0] == '\0' ? "/" : r->unparsed_uri,
        content_type, header_count, header_bytes, body_limit) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msc_apache_contract_record_body(msc_t *msr, int response_direction,
    size_t bytes)
{
    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    return msconnector_transaction_contract_record_body(&msr->contract,
        response_direction, bytes) == MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msc_apache_contract_mark_response_committed(msc_t *msr)
{
    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    return msconnector_transaction_contract_set_response_committed(&msr->contract, 1) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msc_apache_contract_record_decision(msc_t *msr,
    msconnector_transaction_decision_kind kind, const char *rule_id)
{
    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    return msconnector_transaction_contract_record_decision(&msr->contract,
        kind, rule_id, apache_contract_now_ms()) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

/* Keep this classification aligned with process_intervention().  Apache only
 * creates a Location header and returns its canonical redirect result for
 * these four statuses; arbitrary 3xx statuses are still a disruptive block,
 * not a redirect the host can actually perform. */
static msconnector_transaction_decision_kind apache_intervention_decision_kind(
    int status)
{
    switch (status)
    {
        case 301:
        case 302:
        case 303:
        case 307:
            return MSCONNECTOR_TRANSACTION_DECISION_REDIRECT;
        case HTTP_TOO_MANY_REQUESTS:
            return MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT;
        default:
            return MSCONNECTOR_TRANSACTION_DECISION_BLOCK;
    }
}

/* A libModSecurity intervention is disruptive only when it supplies a
 * terminal HTTP status. Treat 1xx/2xx, zero, and out-of-range values as an
 * invalid engine response; returning one of them to httpd could otherwise
 * stop the filter while exposing a successful response. */
static int apache_intervention_status_is_valid(int status)
{
    return status >= HTTP_MULTIPLE_CHOICES && status <= 599;
}

static enum msconnector_phase apache_intervention_failure_phase(
    const msc_t *msr)
{
    if (msr != NULL && msr->native_event_phase_active)
    {
        return msr->native_event_phase;
    }
    if (msr != NULL && msr->contract.active_phase >=
            MSCONNECTOR_PHASE_REQUEST_HEADERS &&
        msr->contract.active_phase <= MSCONNECTOR_PHASE_RESPONSE_BODY)
    {
        return (enum msconnector_phase)msr->contract.active_phase;
    }
    return MSCONNECTOR_PHASE_REQUEST_HEADERS;
}

/* process_intervention() retains the native log in request-pool storage
 * before it releases libModSecurity-owned buffers.  All business-phase
 * callers use this one mapper while that bounded rule correlation remains
 * available, so a disruptive native result cannot silently leave the Common
 * contract at its initial Allow decision. */
int msc_apache_contract_record_intervention_decision(msc_t *msr)
{
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH];
    msconnector_transaction_decision_kind kind;

    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    if (!apache_intervention_status_is_valid(msr->last_intervention_status)) {
        return 0;
    }
    rule_id[0] = '\0';
    if (msconnector_rule_id_extract_from_message(msr->last_intervention_log,
            rule_id, sizeof(rule_id)) <= 0) {
        return 0;
    }
    kind = apache_intervention_decision_kind(msr->last_intervention_status);
    return msc_apache_contract_record_decision(msr, kind, rule_id);
}

const char *msc_apache_contract_intervention_action(const msc_t *msr)
{
    if (msr == NULL) {
        return "deny";
    }
    switch (apache_intervention_decision_kind(msr->last_intervention_status))
    {
        case MSCONNECTOR_TRANSACTION_DECISION_REDIRECT:
            return "redirect";
        case MSCONNECTOR_TRANSACTION_DECISION_RATE_LIMIT:
            return "rate_limit";
        case MSCONNECTOR_TRANSACTION_DECISION_BLOCK:
        default:
            return "deny";
    }
}

int msc_apache_contract_fail(msc_t *msr,
    msconnector_transaction_error_class error_class)
{
    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    return msconnector_transaction_contract_fail(&msr->contract, error_class,
        apache_contract_now_ms()) == MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

int msc_apache_contract_finish(msc_t *msr)
{
    if (msr == NULL || !msr->contract_initialized) {
        return 0;
    }
    return msconnector_transaction_contract_finish(&msr->contract,
        apache_contract_now_ms()) == MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}


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
    if (msr == NULL || r == NULL || r->notes == NULL ||
        msr->response_phase4_terminal_output !=
            MSC_PHASE4_TERMINAL_OUTPUT_EMITTING)
    {
        return 0;
    }
    if (apr_table_get(r->notes,
            apache_phase4_terminal_error_redirect_note) != NULL)
    {
        return 1;
    }
    if (!apache_phase4_redirect_has_local_error_document_proof(msr, r))
    {
        return 0;
    }
    msr->response_phase4_terminal_error_redirect_seen = 1;
    apr_table_setn(r->notes, apache_phase4_terminal_error_redirect_note,
        "1");
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


/* libModSecurity v3.0.12 allocates URL and log with strdup but does not
 * export msc_intervention_cleanup(). Keep their release in the connector
 * after any values retained by Apache have been copied into
 * request-owned memory. This is equivalent to the older public C++ helper's
 * free-and-reset behavior and avoids coupling the module to a newer symbol. */
static void msc_release_intervention_buffers(ModSecurityIntervention *intervention)
{
    if (intervention == NULL)
    {
        return;
    }

    free(intervention->url);
    intervention->url = NULL;
    free(intervention->log);
    intervention->log = NULL;
    intervention->status = N_INTERVENTION_STATUS;
    intervention->pause = 0;
    intervention->disruptive = 0;
}


int process_intervention (Transaction *t, request_rec *r)
{
    ModSecurityIntervention intervention;
    msc_t *msr = NULL;
    const char *log;
    const char *location;
    int z;
    int result = N_INTERVENTION_STATUS;

    intervention.status = N_INTERVENTION_STATUS;
    intervention.pause = 0;
    intervention.url = NULL;
    intervention.log = NULL;
    intervention.disruptive = 0;

    z = msc_intervention(t, &intervention);

    if (z == 0)
    {
        return N_INTERVENTION_STATUS;
    }

    msr = (msc_t *)apr_table_get(r->notes, NOTE_MSR);
    if (!apache_intervention_status_is_valid(intervention.status))
    {
        if (msr != NULL)
        {
            (void)msc_apache_contract_fail(msr,
                MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
            apache_emit_contract_failure_event(msr, r,
                apache_intervention_failure_phase(msr),
                MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
                HTTP_INTERNAL_SERVER_ERROR);
        }
        result = HTTP_INTERNAL_SERVER_ERROR;
        goto cleanup;
    }

    log = intervention.log;
    if (log == NULL)
    {
        log = "(no log message was specified)";
    }

    if (msr != NULL)
    {
        msr->last_intervention_status = intervention.status;
        msr->last_intervention_log = apr_pstrdup(r->pool, log);
        msr->phase4_intervention = intervention.disruptive ? 1 : msr->phase4_intervention;
    }

    if (intervention.status == 301 || intervention.status == 302
        ||intervention.status == 303 || intervention.status == 307)
    {
        if (intervention.url != NULL)
        {
            location = apr_pstrdup(r->pool, intervention.url);
            apr_table_setn(r->headers_out, "Location", location);
            result = HTTP_MOVED_TEMPORARILY;
            goto cleanup;
        }
    }

    if (intervention.status != N_INTERVENTION_STATUS)
    {
        result = intervention.status;
    }

cleanup:
    msc_release_intervention_buffers(&intervention);
    return result;
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
    return 0;
}


/*
 * Used to cleanup the module
 *
 */
static apr_status_t msc_module_cleanup(void *data)
{
    (void)data;
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

static const char *apache_transaction_id_from_expression(request_rec *r,
    msc_conf_t *config)
{
    const char *transaction_id = NULL;
    const char *expr_error = NULL;

    transaction_id = ap_expr_str_exec(r, config->transaction_id_expr,
        &expr_error);
    if (expr_error != NULL) {
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: Failed to evaluate "
            "modsecurity_transaction_id_expr: %s", expr_error);
        return NULL;
    }
    return transaction_id;
}

static const char *apache_resolve_transaction_id(request_rec *r,
    msc_conf_t *config)
{
    const char *transaction_id = NULL;

    if (config->transaction_id_expr != NULL) {
        transaction_id = apache_transaction_id_from_expression(r, config);
    } else if (config->common_config.transaction_id != NULL &&
        config->common_config.transaction_id[0] != '\0') {
        transaction_id = config->common_config.transaction_id;
    }
    if (transaction_id == NULL || transaction_id[0] == '\0') {
        transaction_id = getenv("UNIQUE_ID");
    }
    return transaction_id;
}

static int apache_store_transaction_id(msc_t *msr, request_rec *r,
    const char *transaction_id)
{
    size_t length = 0U;

    if (transaction_id != NULL && transaction_id[0] != '\0') {
        while (length + 1U < MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH &&
            transaction_id[length] != '\0') {
            ++length;
        }
        if (transaction_id[length] != '\0') {
            ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                "ModSecurity: transaction identifier exceeds canonical limit");
            return 0;
        }
        msr->event_transaction_id = apr_pstrdup(r->pool, transaction_id);
    } else {
        msr->event_transaction_id = apr_psprintf(r->pool, "%ld-%ld",
            (long)r->request_time, (long)r->connection->id);
    }
    return msr->event_transaction_id != NULL;
}


static msc_t *create_tx_context(request_rec *r) {
    msc_t *msr = NULL;
    msc_conf_t *z = NULL;
    char *modsecurity_transaction_id = NULL;
    const char *transaction_id = NULL;

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
    transaction_id = apache_resolve_transaction_id(r, z);
    if (!apache_store_transaction_id(msr, r, transaction_id)) {
        return NULL;
    }

    {
        const msconnector_transaction_profile *profile =
            msconnector_profile_registry_find("apache");
        const char *host_id = r->server != NULL &&
            r->server->server_hostname != NULL
            ? r->server->server_hostname : "apache";
        if (profile == NULL || msconnector_transaction_contract_init(
                &msr->contract, profile, msr->event_transaction_id,
                "apache", host_id,
                z->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT
                    ? MSCONNECTOR_TRANSACTION_MODE_STRICT
                    : MSCONNECTOR_TRANSACTION_MODE_SAFE,
                apache_contract_now_ms()) != MSCONNECTOR_TRANSACTION_TRANSITION_OK) {
            ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                "ModSecurity: failed to initialize canonical transaction contract");
            return NULL;
        }
        msr->contract_initialized = 1;
    }

    if (transaction_id != NULL && transaction_id[0] != '\0') {
        /* Validate and copy the request-derived ID through the bounded
         * canonical contract before libModSecurity receives it.  This keeps
         * malformed or oversized request IDs from reaching the native engine
         * and avoids an unregistered native allocation on contract failure. */
        modsecurity_transaction_id = apr_pstrdup(r->pool,
            msr->event_transaction_id);
        if (modsecurity_transaction_id == NULL) {
            (void)msconnector_transaction_contract_cleanup(&msr->contract,
                apache_contract_now_ms());
            msr->contract_initialized = 0;
            return NULL;
        }
        msr->t = msc_new_transaction_with_id(msc_apache->modsec,
            z->rules_set, modsecurity_transaction_id, (void *)r);
    } else {
        msr->t = msc_new_transaction(msc_apache->modsec,
            z->rules_set, (void *)r);
    }
    if (msr->t == NULL)
    {
        (void)msconnector_transaction_contract_cleanup(&msr->contract,
            apache_contract_now_ms());
        msr->contract_initialized = 0;
        return NULL;
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


/* ap_internal_redirect() runs quick handlers before request processing and
 * before ap_invoke_handler(). Refuse unsafe redirected requests here so a
 * target quick handler cannot perform side effects before the normal handler
 * guard has a chance to run. */
static int hook_phase4_redirect_quick_handler(request_rec *r, int lookup)
{
    msc_t *msr = NULL;

    (void)lookup;
    if (r == NULL || r->main != NULL || r->prev == NULL)
    {
        return DECLINED;
    }
    msr = retrieve_tx_context(r);
    if (msr == NULL)
    {
        return DECLINED;
    }
    if (apache_phase4_redirect_is_terminal_error_emission(msr, r))
    {
        return DECLINED;
    }
    apache_phase4_fail_normal_redirect(msr, r,
        "request transaction cannot be safely rebound to the target URI");
    return DONE;
}


/* insert_filter is void, so sealing and aborting a connection there does not
 * stop ap_run_handler(). This hook is the final guard for paths that enter
 * ap_invoke_handler() without first reaching the quick-handler hook. */
static int hook_phase4_redirect_handler(request_rec *r)
{
    msc_t *msr = NULL;

    if (r == NULL || r->main != NULL || r->prev == NULL)
    {
        return DECLINED;
    }
    msr = retrieve_tx_context(r);
    if (msr == NULL)
    {
        return DECLINED;
    }
    if (apache_phase4_redirect_is_terminal_error_emission(msr, r))
    {
        return DECLINED;
    }
    if (msr->response_phase4_terminal_output !=
        MSC_PHASE4_TERMINAL_OUTPUT_SEALED)
    {
        apache_phase4_fail_normal_redirect(msr, r,
            "request transaction cannot be safely rebound to the target URI");
    }
    return DONE;
}


static int msc_hook_pre_config(apr_pool_t *mp, apr_pool_t *mp_log,
    apr_pool_t *mp_temp)
{
    void *data = NULL;
    const char *key = "modsecurity-pre-config-init-flag";
    int first_time = 0;

    (void)mp_log;
    (void)mp_temp;

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

    (void)mp;
    (void)mp_log;
    (void)mp_temp;

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
    (void)conn;
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

    return DECLINED;
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
    msc_t *msr = NULL;
    int it;

    msr = retrieve_tx_context(r);
    if (msr == NULL)
    {
        return DECLINED;
    }

    if (msr->contract_initialized && !msc_apache_contract_finish(msr))
    {
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: canonical transaction did not reach P1-P4 completion");
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

#if 1
    /* An internal redirect, including a local ErrorDocument, inherits the
     * primary transaction but must never re-enter its already terminal P2
     * input filter. Attach MODSECURITY_IN only after redirect exclusion. */
    ap_add_input_filter("MODSECURITY_IN", msr, r, r->connection);
#endif


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


static int apache_emit_phase1_intervention_event(msc_t *msr, request_rec *r,
    int intervention_status, const char *reason)
{
    apache_intervention_event_input event_input;
    const char *action = msc_apache_contract_intervention_action(msr);

    event_input.event_name = "phase1_intervention";
    event_input.phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
    event_input.wanted = action;
    event_input.actual = action;
    event_input.reason = reason;
    event_input.original_status = r->status;
    event_input.response_already_committed = 0;
    apache_emit_intervention_event(msr, r, &event_input);
    return intervention_status;
}


static int process_request_headers(request_rec *r, msc_t *msr) {
    /* P1 begins before URI processing because URI interventions are part of
     * the request-header phase.  This binds a terminal URI intervention to
     * bounded request metadata rather than leaving a partial transaction. */
    if (!msc_apache_contract_record_request_metadata(msr, r)) {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P1 request metadata");
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    if (!msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_REQUEST_HEADERS)) {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P1 transition");
        return HTTP_INTERNAL_SERVER_ERROR;
    }

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
            if (!msc_apache_contract_record_intervention_decision(msr)) {
                (void)msc_apache_contract_fail(msr,
                    MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
                apache_emit_contract_failure_event(msr, r,
                    MSCONNECTOR_PHASE_REQUEST_HEADERS,
                    MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
                    HTTP_INTERNAL_SERVER_ERROR);
                ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                    "ModSecurity: could not record canonical URI intervention decision");
                return HTTP_INTERNAL_SERVER_ERROR;
            }
            return apache_emit_phase1_intervention_event(msr, r, it,
                "request_uri_before_request_headers");
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
            /* Apache owns immutable NUL-terminated table strings while the
             * libmodsecurity C API declares the same header bytes as
             * unsigned. Keep the ownership and byte boundary explicit. */
            const unsigned char *key_bytes = (const unsigned char *)key;
            const unsigned char *val_bytes = (const unsigned char *)val;
            msc_add_request_header(msr->t, key_bytes, val_bytes);
        }
        msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_HEADERS;
        msr->native_event_phase_active = 1;
        msc_process_request_headers(msr->t);
        msr->native_event_phase_active = 0;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            /* The native request-header hook has not handed control to a
             * handler yet.  Write this bounded event in the same real host
             * path that returns the HTTP intervention to Apache. */
            (void)msc_apache_contract_complete(msr,
                MSCONNECTOR_PHASE_REQUEST_HEADERS);
            if (!msc_apache_contract_record_intervention_decision(msr)) {
                (void)msc_apache_contract_fail(msr,
                    MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
                apache_emit_contract_failure_event(msr, r,
                    MSCONNECTOR_PHASE_REQUEST_HEADERS,
                    MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
                    HTTP_INTERNAL_SERVER_ERROR);
                ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                    "ModSecurity: could not record canonical P1 intervention decision");
                return HTTP_INTERNAL_SERVER_ERROR;
            }
            return apache_emit_phase1_intervention_event(msr, r, it,
                "request_headers_before_handler");
        }
    }

    if (!msc_apache_contract_complete(msr,
            MSCONNECTOR_PHASE_REQUEST_HEADERS)) {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P1 completion");
        return HTTP_INTERNAL_SERVER_ERROR;
    }

    return N_INTERVENTION_STATUS;
}



static void msc_register_hooks(apr_pool_t *pool)
{
    (void)pool;
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
    ap_hook_quick_handler(hook_phase4_redirect_quick_handler, NULL, NULL,
        APR_HOOK_REALLY_FIRST);
    ap_hook_insert_filter(hook_insert_filter, NULL, NULL, APR_HOOK_FIRST);
    ap_hook_handler(hook_phase4_redirect_handler, NULL, NULL,
        APR_HOOK_REALLY_FIRST);

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
    msc_register_hooks,
    AP_MODULE_FLAG_NONE
};
