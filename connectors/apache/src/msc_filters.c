
#include "msc_filters.h"
#include "msc_utils.h"
#include "http_protocol.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/late_intervention.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"

#include <apr_file_io.h>
#include <string.h>


/* A one-megabyte payload can still be represented as one million individual
 * one-byte APR buckets. Hold a bounded number of normalized buckets pending
 * EOS so the Phase-4 byte cap also has a bounded object/setaside cost. */
#define MSCONNECTOR_PHASE4_MAX_HELD_BUCKETS 4096U


/* Kept private to this translation unit; Phase 2 reaches it before the
 * implementation below because input-filter EOS is handled near the start
 * of this file. */
static void apache_log_intervention_event(msc_t *msr, request_rec *r,
    const char *event_name, enum msconnector_phase phase,
    const char *wanted, const char *actual, const char *reason,
    int original_status, int response_committed);


/*
 * Phase 2 has exactly one terminal transition.  Input buckets may arrive in
 * many filter calls, while a handler which does not consume its request body
 * may cause Apache to discard that body later.  Both paths share this helper
 * so libmodsecurity never observes an append after end-of-stream.
 */
int msc_finalize_request_body(msc_t *msr, request_rec *r)
{
    int intervention;

    if (msr == NULL || r == NULL || msr->t == NULL)
    {
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    if (msr->request_body_processed)
    {
        return N_INTERVENTION_STATUS;
    }
    msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
    msr->native_event_phase_active = 1;
    if (msc_process_request_body(msr->t) < 0)
    {
        msr->native_event_phase_active = 0;
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    msr->native_event_phase_active = 0;
    msr->request_body_processed = 1;
    intervention = process_intervention(msr->t, r);
    if (intervention != N_INTERVENTION_STATUS)
    {
        const char *action = msr->last_intervention_status >= 300 &&
            msr->last_intervention_status < 400 ? "redirect" : "deny";

        /* This is the actual Apache input-filter terminal path.  Emit the
         * bounded decision metadata before returning the disruptive status to
         * httpd, rather than reconstructing Phase 2 from audit output. */
        apache_log_intervention_event(msr, r, "phase2_intervention",
            MSCONNECTOR_PHASE_REQUEST_BODY, action, action,
            "request_body_before_handler", r->status, 0);
    }
    return intervention;
}


apr_status_t input_filter(ap_filter_t *f, apr_bucket_brigade *pbbOut,
        ap_input_mode_t mode, apr_read_type_e block, apr_off_t nbytes)
{
    request_rec *r = f->r;
    conn_rec *c = r->connection;

    apr_bucket_brigade *pbbTmp;
    int ret;

    msc_t *msr = (msc_t *)f->ctx;

    /* Do we have the context? */
    if (msr == NULL)
    {
        ap_log_error(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, f->r->server,
                "ModSecurity: Internal Error: msr is null in input filter.");
        ap_remove_input_filter(f);
        return send_input_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
    }

    pbbTmp = apr_brigade_create(r->pool, c->bucket_alloc);
    if (APR_BRIGADE_EMPTY(pbbTmp))
    {
        ret = ap_get_brigade(f->next, pbbTmp, mode, block, nbytes);

        if (mode == AP_MODE_EATCRLF || ret != APR_SUCCESS)
            return ret;
    }

    while (!APR_BRIGADE_EMPTY(pbbTmp))
    {
        apr_bucket *pbktIn = APR_BRIGADE_FIRST(pbbTmp);
        const char *data;
        apr_size_t len;
        int it;

        if (APR_BUCKET_IS_EOS(pbktIn))
        {
            if (!msr->request_body_processed)
            {
                it = msc_finalize_request_body(msr, r);
                if (it != N_INTERVENTION_STATUS)
                {
                    msr->request_body_intervention_sent = 1;
                    ap_remove_input_filter(f);
                    return send_input_error_bucket(msr, f, it);
                }
            }
            APR_BUCKET_REMOVE(pbktIn);
            APR_BRIGADE_INSERT_TAIL(pbbOut, pbktIn);
            break;
        }

        ret=apr_bucket_read(pbktIn, &data, &len, block);
        if (ret != APR_SUCCESS)
        {
            return ret;
        }

        if (msc_append_request_body(msr->t,
                (const unsigned char *)data, len) < 0)
        {
            ap_remove_input_filter(f);
            return send_input_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
        }
        msr->request_body_bytes_seen += len;
        msr->request_body_bytes_inspected += len;

        /* The host owns this bucket. Move it through unchanged rather than
         * materializing a second request-body copy in the connector. */
        APR_BUCKET_REMOVE(pbktIn);
        APR_BRIGADE_INSERT_TAIL(pbbOut, pbktIn);
    }
    return APR_SUCCESS;
}

static const char *apache_response_content_type(request_rec *r)
{
    const char *value = r->content_type;

    if (value == NULL || value[0] == '\0')
    {
        value = apr_table_get(r->headers_out, "Content-Type");
    }
    if (value == NULL || value[0] == '\0')
    {
        value = apr_table_get(r->err_headers_out, "Content-Type");
    }

    return value;
}


static const char *apache_request_content_type(request_rec *r)
{
    if (r == NULL || r->headers_in == NULL)
    {
        return "";
    }
    return apr_table_get(r->headers_in, "Content-Type");
}


static const char *apache_event_phase_name(enum msconnector_phase phase)
{
    switch (phase)
    {
        case MSCONNECTOR_PHASE_REQUEST_HEADERS:
            return "request_headers";
        case MSCONNECTOR_PHASE_REQUEST_BODY:
            return "request_body";
        case MSCONNECTOR_PHASE_RESPONSE_HEADERS:
            return "response_headers";
        case MSCONNECTOR_PHASE_RESPONSE_BODY:
            return "response_body";
        default:
            return "unknown";
    }
}


static const char *apache_phase4_mode_name(enum msconnector_phase4_mode mode)
{
    switch (mode)
    {
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

static const char *apache_phase4_actual_action(
    msconnector_late_intervention_action action,
    const char *requested_action)
{
    const char *name = msconnector_late_intervention_action_name(action);

    if (strcmp(name, "deny_if_possible") == 0)
    {
        return requested_action != NULL &&
            strcmp(requested_action, "redirect") == 0
            ? "redirect" : "deny";
    }
    return name;
}


static void apache_log_intervention_event(msc_t *msr, request_rec *r,
    const char *event_name, enum msconnector_phase phase,
    const char *wanted, const char *actual, const char *reason,
    int original_status, int response_committed)
{
    msc_conf_t *conf;
    apr_file_t *file = NULL;
    apr_status_t rc;
    msconnector_event event;
    char line[4096];
    char rule_id[64];
    int json_truncated = 0;

    if (msr == NULL || r == NULL || r->per_dir_config == NULL)
    {
        return;
    }

    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL || conf->common_config.phase4_log_path == NULL)
    {
        return;
    }

    rc = apr_file_open(&file, conf->common_config.phase4_log_path,
        APR_WRITE | APR_CREATE | APR_APPEND, APR_OS_DEFAULT, r->pool);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to open intervention log %s",
            conf->common_config.phase4_log_path);
        return;
    }

    rule_id[0] = '\0';
    (void)msconnector_rule_id_extract_from_message(msr->last_intervention_log,
        rule_id, sizeof(rule_id));

    msconnector_event_init(&event);
    event.meta.message_id = phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? MSCONN_EVENT_REQUEST_BLOCKED
        : (phase == MSCONNECTOR_PHASE_RESPONSE_BODY
            ? (strcmp(actual, "abort_connection") == 0
                ? MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200
                : (strcmp(actual, "log_only") == 0
                    ? MSCONN_EVENT_PHASE4_LATE_INTERVENTION
                    : MSCONN_EVENT_RESPONSE_BLOCKED))
            : MSCONN_EVENT_RESPONSE_BLOCKED);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = event_name;
    event.meta.connector = "apache";
    event.meta.integration_mode = "native-httpd-module";
    event.meta.transaction_id = msr->event_transaction_id;
    event.decision.phase = phase;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual;
    event.decision.requested_action = wanted;
    event.decision.actual_action = actual;
    event.decision.rule_id = rule_id;
    event.decision.reason = reason;
    event.http.http_status = msr->last_intervention_status;
    event.http.original_http_status = original_status;
    if (strcmp(actual, "deny") == 0 || strcmp(actual, "redirect") == 0)
    {
        event.http.visible_http_status = msr->last_intervention_status;
        event.http.transport_result = "http_status";
    }
    else if (strcmp(actual, "abort_connection") == 0)
    {
        event.http.visible_http_status = r->status;
        event.http.transport_result = "connection_aborted";
    }
    else
    {
        event.http.visible_http_status = r->status;
        event.http.transport_result = "log_only";
    }
    event.request.method = r->method;
    event.request.uri = r->unparsed_uri;
    event.body.content_type = phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? apache_request_content_type(r) : apache_response_content_type(r);
    event.body.bytes_seen = phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? msr->request_body_bytes_seen
        : (phase == MSCONNECTOR_PHASE_RESPONSE_BODY
            ? msr->response_body_bytes_seen : 0U);
    event.body.bytes_inspected = phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? msr->request_body_bytes_inspected
        : (phase == MSCONNECTOR_PHASE_RESPONSE_BODY
            ? msr->response_body_bytes_inspected : 0U);
    event.flags.late_intervention = response_committed;
    if (response_committed)
    {
        event.flags.late_intervention_mode = apache_phase4_mode_name(
            conf->common_config.phase4_mode);
    }
    event.flags.response_started = response_committed;
    event.flags.response_committed = response_committed;
    event.flags.headers_sent = response_committed;
    event.flags.body_started = phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        response_committed;
    /* Phase-2/4 intervention records are emitted only after their explicit
     * body finish boundary; this is not a claim about client completion. */
    event.flags.eos_seen = phase == MSCONNECTOR_PHASE_REQUEST_BODY ||
        phase == MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.flags.connection_aborted = phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        msr->phase4_strict_abort;
    event.flags.body_truncated = phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        msr->response_body_truncated;

    if (msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated))
    {
        rc = apr_file_puts(line, file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to write intervention log %s",
                conf->common_config.phase4_log_path);
        }
    }
    else if (json_truncated)
    {
        rc = apr_file_puts(apr_psprintf(r->pool,
            "{\"event\":\"%s\",\"integration_mode\":\"native-httpd-module\",\"phase\":\"%s\","
            "\"status\":\"blocked\",\"reason\":\"event serialization truncated\","
            "\"truncated\":true}\n", event_name,
            apache_event_phase_name(phase)), file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write truncated intervention log %s",
                conf->common_config.phase4_log_path);
        }
    }
    else
    {
        rc = apr_file_puts(apr_psprintf(r->pool,
            "{\"event\":\"%s\",\"integration_mode\":\"native-httpd-module\",\"phase\":\"%s\","
            "\"status\":\"error\",\"reason\":\"event serialization failed\"}\n",
            event_name, apache_event_phase_name(phase)), file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write failed intervention log %s",
                conf->common_config.phase4_log_path);
        }
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, 0, r,
            "ModSecurity: failed to serialize common intervention event");
    }

    rc = apr_file_close(file);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to close intervention log %s",
            conf->common_config.phase4_log_path);
    }
}


void apache_emit_intervention_event(msc_t *msr, request_rec *r,
    const char *event_name, enum msconnector_phase phase,
    const char *wanted, const char *actual, const char *reason,
    int original_status, int response_committed)
{
    apache_log_intervention_event(msr, r, event_name, phase, wanted, actual,
        reason, original_status, response_committed);
}


void apache_log_rule_match_event(msc_t *msr, request_rec *r,
    enum msconnector_phase phase, const char *rule_id)
{
    msc_conf_t *conf;
    apr_file_t *file = NULL;
    apr_status_t rc;
    msconnector_event event;
    char line[4096];
    int json_truncated = 0;

    if (msr == NULL || r == NULL || r->per_dir_config == NULL ||
        !msconnector_rule_id_validate(rule_id))
    {
        return;
    }

    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL || conf->common_config.phase4_log_path == NULL)
    {
        return;
    }

    rc = apr_file_open(&file, conf->common_config.phase4_log_path,
        APR_WRITE | APR_CREATE | APR_APPEND, APR_OS_DEFAULT, r->pool);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to open native rule-match log %s",
            conf->common_config.phase4_log_path);
        return;
    }

    /* This record is emitted synchronously by the real libmodsecurity log
     * callback while Apache is in the named request phase.  It intentionally
     * preserves a non-disruptive match as `pass`, rather than pretending that
     * a rule with `log` was a deny or a late log-only intervention. */
    msconnector_event_init(&event);
    event.meta.level = "info";
    event.meta.message_id = "MSCONN_EVENT_RULE_MATCHED";
    event.meta.message = "Non-disruptive ModSecurity rule match observed in native Apache module.";
    event.meta.event = "request_rule_match";
    event.meta.connector = "apache";
    event.meta.integration_mode = "native-httpd-module";
    event.meta.transaction_id = msr->event_transaction_id;
    event.decision.phase = phase;
    event.decision.status = MSCONNECTOR_STATUS_OK;
    event.decision.action = "pass";
    event.decision.requested_action = "pass";
    event.decision.actual_action = "pass";
    event.decision.rule_id = rule_id;
    event.decision.reason = "non_disruptive_rule_match";
    event.http.transport_result = "not_observable";
    event.request.method = r->method;
    event.request.uri = r->unparsed_uri;
    event.body.content_type = phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? apache_request_content_type(r) : apache_response_content_type(r);
    event.body.bytes_seen = phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? msr->request_body_bytes_seen : 0U;
    event.body.bytes_inspected = phase == MSCONNECTOR_PHASE_REQUEST_BODY
        ? msr->request_body_bytes_inspected : 0U;

    if (msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated))
    {
        rc = apr_file_puts(line, file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write native rule-match log %s",
                conf->common_config.phase4_log_path);
        }
    }
    else
    {
        rc = apr_file_puts(apr_psprintf(r->pool,
            "{\"event\":\"request_rule_match\",\"integration_mode\":\"native-httpd-module\","
            "\"phase\":\"%s\",\"status\":\"error\","
            "\"reason\":\"native rule-match event serialization %s\"}\n",
            apache_event_phase_name(phase),
            json_truncated ? "truncated" : "failed"), file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write native rule-match fallback %s",
                conf->common_config.phase4_log_path);
        }
    }

    rc = apr_file_close(file);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to close native rule-match log %s",
            conf->common_config.phase4_log_path);
    }
}


static void apache_phase4_log_event(msc_t *msr, request_rec *r,
    const char *wanted, const char *actual, const char *reason)
{
    apache_log_intervention_event(msr, r, "phase4_intervention",
        MSCONNECTOR_PHASE_RESPONSE_BODY, wanted, actual, reason, r->status,
        msr != NULL ? msr->response_committed : 0);
}


static void apache_phase3_log_event(msc_t *msr, request_rec *r,
    const char *wanted, const char *actual, int original_status)
{
    apache_log_intervention_event(msr, r, "phase3_intervention",
        MSCONNECTOR_PHASE_RESPONSE_HEADERS, wanted, actual,
        "response_headers_before_commit", original_status, 0);
}


static apr_status_t apache_phase4_append_bucket(msc_t *msr,
    msc_conf_t *conf, apr_bucket *bucket)
{
    const char *data = NULL;
    apr_size_t len = 0;
    apr_status_t rc;
    msconnector_body_limit_plan plan;

    if (APR_BUCKET_IS_EOS(bucket) || APR_BUCKET_IS_METADATA(bucket))
    {
        return APR_SUCCESS;
    }

    rc = apr_bucket_read(bucket, &data, &len, APR_BLOCK_READ);
    if (rc != APR_SUCCESS)
    {
        return rc;
    }

    if (len > 0)
    {
        msr->response_body_seen = 1;
        /* Phase 4 has an EOS-only enforcement decision. libModSecurity owns
         * the effective SecResponseBodyMimeType policy, but its C API does
         * not expose a safe way for this connector to ask whether a response
         * can later match it. Therefore every response entering this output
         * filter stays behind the pre-commit gate. Processing only a bounded
         * prefix and releasing an uninspected tail would recreate the bypass,
         * so an oversize response is rejected before it can be saved or sent.
         */
        if (!msconnector_body_limit_plan_chunk(msr->response_body_bytes_seen,
                msr->response_body_bytes_inspected,
                conf->common_config.phase4_body_limit,
                MSCONNECTOR_BODY_LIMIT_ACTION_REJECT, len, &plan))
        {
            msr->response_body_bytes_seen = plan.bytes_seen;
            msr->response_body_truncated = 1;
            return APR_EGENERAL;
        }
        msr->response_body_bytes_seen = plan.bytes_seen;
        if (plan.append_size > 0 && msc_append_response_body(msr->t,
                (const unsigned char *)data, plan.append_size) != 1)
        {
            return APR_EGENERAL;
        }
        msr->response_body_bytes_inspected += plan.append_size;
        if (plan.truncated)
        {
            msr->response_body_truncated = 1;
        }
    }

    return APR_SUCCESS;
}


static int apache_phase4_normalize_response_brigade(
    apr_bucket_brigade *bb_in)
{
    apr_bucket *bucket;
    apr_bucket *next;
    int eos_seen = 0;

    for (bucket = APR_BRIGADE_FIRST(bb_in);
        bucket != APR_BRIGADE_SENTINEL(bb_in); bucket = next)
    {
        next = APR_BUCKET_NEXT(bucket);
        /* Apache output-filter ownership ends at the first EOS. No later
         * bucket belongs to this response, so never append, retain, or emit
         * it. This also ensures a malformed one-brigade suffix cannot bypass
         * the terminal Phase-4 decision. */
        if (eos_seen)
        {
            APR_BUCKET_REMOVE(bucket);
            apr_bucket_destroy(bucket);
            continue;
        }
        if (APR_BUCKET_IS_EOS(bucket))
        {
            eos_seen = 1;
            continue;
        }
        /* A pre-EOS FLUSH cannot retain its progressive delivery semantics
         * behind an EOS gate. Empty non-metadata buckets are likewise safe to
         * discard and otherwise let a peer retain unbounded zero-byte bucket
         * objects. Preserve all other pre-EOS metadata unchanged. */
        if (APR_BUCKET_IS_FLUSH(bucket) ||
            (!APR_BUCKET_IS_METADATA(bucket) && bucket->length == 0))
        {
            APR_BUCKET_REMOVE(bucket);
            apr_bucket_destroy(bucket);
        }
    }
    return eos_seen;
}


/* Apache error buckets cannot be set aside: Apache requires one to be the
 * first bucket emitted by its originating filter, so retaining it would both
 * violate that contract and turn a real downstream error into a generic
 * setaside failure. A valid incoming error is already terminal for the
 * original response; discard every protected byte and use the connector's
 * established pre-commit error bridge to preserve its HTTP status/ErrorDocument
 * path. An error bucket after any other bucket is malformed and fails closed. */
static int apache_phase4_error_bucket_status(apr_bucket_brigade *bb_in)
{
    apr_bucket *bucket;
    apr_bucket *first;
    ap_bucket_error *error;

    if (bb_in == NULL)
    {
        return 0;
    }
    first = APR_BRIGADE_FIRST(bb_in);
    for (bucket = first; bucket != APR_BRIGADE_SENTINEL(bb_in);
        bucket = APR_BUCKET_NEXT(bucket))
    {
        if (!AP_BUCKET_IS_ERROR(bucket))
        {
            continue;
        }
        if (bucket != first)
        {
            return -1;
        }
        error = (ap_bucket_error *)bucket->data;
        if (error == NULL || !ap_is_HTTP_ERROR(error->status))
        {
            return -1;
        }
        return error->status;
    }
    return 0;
}


static int apache_phase3_snapshot_table_value(apr_pool_t *pool,
    const apr_table_t *table, const char *key, int *was_set,
    const char **value)
{
    const char *source = table != NULL ? apr_table_get(table, key) : NULL;

    if (pool == NULL || key == NULL || was_set == NULL || value == NULL)
    {
        return 0;
    }
    *was_set = source != NULL;
    *value = source != NULL ? apr_pstrdup(pool, source) : NULL;
    return source == NULL || *value != NULL;
}


static apr_table_t *apache_phase3_clone_response_table(apr_pool_t *pool,
    const apr_table_t *table)
{
    if (pool == NULL)
    {
        return NULL;
    }
    return table != NULL ? apr_table_clone(pool, table)
        : apr_table_make(pool, 0);
}


static apr_array_header_t *apache_phase3_clone_content_languages(
    apr_pool_t *pool, const apr_array_header_t *languages)
{
    apr_array_header_t *copy;
    char **source;
    int i;

    if (pool == NULL || languages == NULL)
    {
        return NULL;
    }
    copy = apr_array_make(pool, languages->nelts, sizeof(char *));
    if (copy == NULL)
    {
        return NULL;
    }
    source = (char **)languages->elts;
    for (i = 0; i < languages->nelts; ++i)
    {
        char **value = apr_array_push(copy);

        if (value == NULL)
        {
            return NULL;
        }
        *value = source[i] != NULL ? apr_pstrdup(pool, source[i]) : NULL;
        if (source[i] != NULL && *value == NULL)
        {
            return NULL;
        }
    }
    return copy;
}


static int apache_phase3_restore_table_value(apr_pool_t *pool,
    apr_table_t **table, const char *key, int was_set, const char *value)
{
    if (pool == NULL || table == NULL || key == NULL)
    {
        return 0;
    }
    if (*table == NULL)
    {
        if (!was_set)
        {
            return 1;
        }
        *table = apr_table_make(pool, 1);
        if (*table == NULL)
        {
            return 0;
        }
    }
    if (was_set)
    {
        if (value == NULL)
        {
            return 0;
        }
        apr_table_setn(*table, key, value);
    }
    else
    {
        apr_table_unset(*table, key);
    }
    return 1;
}


static int apache_phase3_snapshot_response_state(msc_t *msr,
    request_rec *r)
{
    if (msr == NULL || r == NULL)
    {
        return 0;
    }
    msr->response_headers_snapshot = apache_phase3_clone_response_table(
        r->pool, r->headers_out);
    msr->response_err_headers_snapshot = apache_phase3_clone_response_table(
        r->pool, r->err_headers_out);
    if (msr->response_headers_snapshot == NULL ||
        msr->response_err_headers_snapshot == NULL)
    {
        return 0;
    }
    msr->response_status_snapshot = r->status;
    msr->response_status_line_snapshot = r->status_line != NULL
        ? apr_pstrdup(r->pool, r->status_line) : NULL;
    msr->response_content_type_snapshot = r->content_type != NULL
        ? apr_pstrdup(r->pool, r->content_type) : NULL;
    msr->response_content_encoding_snapshot = r->content_encoding != NULL
        ? apr_pstrdup(r->pool, r->content_encoding) : NULL;
    msr->response_content_languages_snapshot = apache_phase3_clone_content_languages(
        r->pool, r->content_languages);
    if (r->content_languages != NULL &&
        msr->response_content_languages_snapshot == NULL)
    {
        return 0;
    }
    msr->response_clength_snapshot = r->clength;
    msr->response_chunked_snapshot = r->chunked;
    msr->response_no_cache_snapshot = r->no_cache;
    if (!apache_phase3_snapshot_table_value(r->pool, r->notes, "no-etag",
            &msr->response_note_no_etag_snapshot_set,
            &msr->response_note_no_etag_snapshot) ||
        !apache_phase3_snapshot_table_value(r->pool, r->subprocess_env,
            "force-no-vary", &msr->response_env_force_no_vary_snapshot_set,
            &msr->response_env_force_no_vary_snapshot) ||
        !apache_phase3_snapshot_table_value(r->pool, r->subprocess_env,
            "downgrade-1.0", &msr->response_env_downgrade_1_0_snapshot_set,
            &msr->response_env_downgrade_1_0_snapshot) ||
        !apache_phase3_snapshot_table_value(r->pool, r->subprocess_env,
            "force-response-1.0",
            &msr->response_env_force_response_1_0_snapshot_set,
            &msr->response_env_force_response_1_0_snapshot) ||
        !apache_phase3_snapshot_table_value(r->pool, r->subprocess_env,
            "nokeepalive", &msr->response_env_nokeepalive_snapshot_set,
            &msr->response_env_nokeepalive_snapshot))
    {
        return 0;
    }
    msr->response_proto_num_snapshot = r->proto_num;
    msr->response_header_only_snapshot = r->header_only;
    msr->response_assbackwards_snapshot = r->assbackwards;
    msr->response_proxyreq_snapshot = r->proxyreq;
    msr->response_expecting_100_snapshot = r->expecting_100;
    msr->response_request_time_snapshot = r->request_time;
    msr->response_headers_snapshot_taken = 1;
    return 1;
}


static int apache_phase3_restore_response_state(msc_t *msr,
    request_rec *r)
{
    apr_table_t *headers;
    apr_table_t *err_headers;

    if (msr == NULL || r == NULL || !msr->response_headers_snapshot_taken ||
        msr->response_headers_snapshot == NULL ||
        msr->response_err_headers_snapshot == NULL)
    {
        return 0;
    }
    headers = apache_phase3_clone_response_table(r->pool,
        msr->response_headers_snapshot);
    err_headers = apache_phase3_clone_response_table(r->pool,
        msr->response_err_headers_snapshot);
    if (headers == NULL || err_headers == NULL)
    {
        return 0;
    }
    r->headers_out = headers;
    r->err_headers_out = err_headers;
    r->status = msr->response_status_snapshot;
    r->status_line = msr->response_status_line_snapshot;
    r->content_type = msr->response_content_type_snapshot;
    r->content_encoding = msr->response_content_encoding_snapshot;
    r->content_languages = apache_phase3_clone_content_languages(r->pool,
        msr->response_content_languages_snapshot);
    if (msr->response_content_languages_snapshot != NULL &&
        r->content_languages == NULL)
    {
        return 0;
    }
    r->clength = msr->response_clength_snapshot;
    r->chunked = msr->response_chunked_snapshot;
    r->no_cache = msr->response_no_cache_snapshot;
    if (!apache_phase3_restore_table_value(r->pool, &r->notes, "no-etag",
            msr->response_note_no_etag_snapshot_set,
            msr->response_note_no_etag_snapshot) ||
        !apache_phase3_restore_table_value(r->pool, &r->subprocess_env,
            "force-no-vary", msr->response_env_force_no_vary_snapshot_set,
            msr->response_env_force_no_vary_snapshot) ||
        !apache_phase3_restore_table_value(r->pool, &r->subprocess_env,
            "downgrade-1.0",
            msr->response_env_downgrade_1_0_snapshot_set,
            msr->response_env_downgrade_1_0_snapshot) ||
        !apache_phase3_restore_table_value(r->pool, &r->subprocess_env,
            "force-response-1.0",
            msr->response_env_force_response_1_0_snapshot_set,
            msr->response_env_force_response_1_0_snapshot) ||
        !apache_phase3_restore_table_value(r->pool, &r->subprocess_env,
            "nokeepalive", msr->response_env_nokeepalive_snapshot_set,
            msr->response_env_nokeepalive_snapshot))
    {
        return 0;
    }
    r->proto_num = msr->response_proto_num_snapshot;
    r->header_only = msr->response_header_only_snapshot;
    r->assbackwards = msr->response_assbackwards_snapshot;
    r->proxyreq = msr->response_proxyreq_snapshot;
    r->expecting_100 = msr->response_expecting_100_snapshot;
    r->request_time = msr->response_request_time_snapshot;
    return 1;
}


static apr_status_t apache_phase4_fail_closed(msc_t *msr, ap_filter_t *f,
    apr_bucket_brigade *bb_in, const char *reason);


static apr_status_t apache_phase4_release_response_brigade(msc_t *msr,
    ap_filter_t *f)
{
    apr_bucket_brigade *held;
    apr_status_t rc;

    if (msr == NULL || f == NULL || f->next == NULL)
    {
        msc_discard_response_brigade(msr);
        return APR_EGENERAL;
    }

    if (!apache_phase3_restore_response_state(msr, f->r))
    {
        return apache_phase4_fail_closed(msr, f, NULL,
            "missing Phase 3 response-state snapshot");
    }

    held = msr->response_brigade;
    msr->response_brigade = NULL;
    if (held == NULL)
    {
        return apache_phase4_fail_closed(msr, f, NULL,
            "missing saved response brigade");
    }

    /* ap_pass_brigade() is synchronous. Let the one valid, fully retained
     * response sequence traverse the protocol guard while it is EMITTING,
     * then seal the guard as soon as this terminal EOS has returned. A
     * downstream HTTP error raised reentrantly during the pass still sees
     * EMITTING and can emit its legitimate error/ErrorDocument response; any
     * producer that writes after the completed EOS is necessarily attempting
     * a second response sequence and must be contained. */
    msr->response_phase4_eos_released = 1;
    msr->response_phase4_terminal_output =
        MSC_PHASE4_TERMINAL_OUTPUT_EMITTING;
    rc = ap_pass_brigade(f->next, held);
    msr->response_phase4_terminal_output =
        MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
    apr_brigade_cleanup(held);
    msr->response_brigade_bucket_count = 0U;
    return rc;
}


apr_status_t phase4_terminal_guard_filter(ap_filter_t *f,
    apr_bucket_brigade *bb_in)
{
    msc_t *msr = f != NULL ? (msc_t *)f->ctx : NULL;

    /* This guard lives in r->proto_output_filters, which Apache preserves
     * when it resets a request's resource filters to emit an error response.
     * During the explicitly bounded synchronous terminal emission it passes
     * Apache's error/ErrorDocument body. Once sealed, it discards *every*
     * subsequent bucket, including EOS/FLUSH metadata, so an invalid producer
     * cannot append another response sequence through a reset chain. */
    if (msr != NULL && msr->response_phase4_terminal_output ==
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED)
    {
        if (bb_in != NULL)
        {
            apr_brigade_cleanup(bb_in);
        }
        return APR_EGENERAL;
    }
    if (f == NULL || f->next == NULL)
    {
        if (bb_in != NULL)
        {
            apr_brigade_cleanup(bb_in);
        }
        return APR_EGENERAL;
    }
    return ap_pass_brigade(f->next, bb_in);
}


static int apache_phase4_response_committed(const msc_t *msr,
    const request_rec *r)
{
    /* mod_proxy marks sent_bodyct before its brigade reaches this output
     * filter, and ap_pass_brigade() marks eos_sent before invoking this
     * filter. Neither one proves that MODSECURITY_OUT released the response.
     * bytes_sent is raised later in Apache's protocol output path, while
     * response_phase4_eos_released records only an EOS this filter itself
     * passed to f->next. The protected EOS remains saved until Phase 4 has
     * resolved, so both values are false at the normal decision boundary. */
    return (msr != NULL && msr->response_phase4_eos_released) ||
        (r != NULL && r->bytes_sent > 0);
}


static apr_status_t apache_phase4_abort_response_connection(ap_filter_t *f)
{
    request_rec *r = f != NULL ? f->r : NULL;

    if (r == NULL || r->connection == NULL)
    {
        return APR_EGENERAL;
    }

    /* Apache can reset the request output filter chain while it processes an
     * error bucket. Mark the connection terminal after that one error has
     * been passed so a producer that ignores our returned failure cannot send
     * another response through the reset chain. Core output rejects writes on
     * an aborted connection. */
    r->connection->keepalive = AP_CONN_CLOSE;
    r->connection->aborted = 1;
    return APR_ECONNABORTED;
}


static apr_status_t apache_send_precommit_terminal_error(msc_t *msr,
    ap_filter_t *f, apr_bucket_brigade *bb_in, int status)
{
    request_rec *r = f != NULL ? f->r : NULL;

    if (bb_in != NULL)
    {
        apr_brigade_cleanup(bb_in);
    }
    if (r == NULL || r->connection == NULL)
    {
        return APR_EGENERAL;
    }

    /* Use Apache's synchronous error-response API, not an error bucket passed
     * from inside the active content filter. The latter defers local
     * ErrorDocument processing until after the filter returns on some Apache
     * paths, at which point a sealed guard turns the configured ErrorDocument
     * into a recursive generic 500. Keep the protocol guard open exactly for
     * this API call, then seal it before the original producer can resume. */
    if (msr != NULL)
    {
        msc_discard_response_brigade(msr);
        msr->response_phase4_gate_failed = 1;
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_EMITTING;
    }
    /* ap_send_error_response() emits only Apache's generic response and
     * bypasses a configured local ErrorDocument.  Enter the core error path
     * instead, while the protocol guard is still in its one bounded EMITTING
     * state.  ap_die() uses the current request status as its recursion
     * indicator, so neutralize an earlier handler status first: a Phase-4
     * enforcement decision is a new terminal error, not a recursive failure.
     * ap_die() then sets status itself and synchronously performs the local
     * ErrorDocument redirect (when configured) before this helper seals the
     * guard and the original producer can resume. */
    r->status = HTTP_OK;
    r->status_line = NULL;
    ap_die(status, r);
    if (msr != NULL)
    {
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
    }
    return APR_EGENERAL;
}


static apr_status_t apache_phase4_fail_closed(msc_t *msr, ap_filter_t *f,
    apr_bucket_brigade *bb_in, const char *reason)
{
    request_rec *r = f != NULL ? f->r : NULL;

    if (bb_in != NULL)
    {
        apr_brigade_cleanup(bb_in);
    }
    msc_discard_response_brigade(msr);
    if (msr != NULL)
    {
        msr->response_phase4_gate_failed = 1;
    }
    if (f == NULL || r == NULL)
    {
        return APR_EGENERAL;
    }

    if (apache_phase4_response_committed(msr, r))
    {
        if (msr != NULL)
        {
            msr->response_committed = 1;
            msr->response_phase4_terminal_output =
                MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
        }
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: Phase 4 response gate failed after response commit: %s",
            reason != NULL ? reason : "unspecified failure");
        return apache_phase4_abort_response_connection(f);
    }

    ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
        "ModSecurity: Phase 4 response gate failed before response commit: %s",
        reason != NULL ? reason : "unspecified failure");
    /* Do not leave MODSECURITY_OUT in the resource chain while Apache turns
     * the terminal error bucket into a local ErrorDocument. The protocol
     * guard remains in the protocol chain and is deliberately EMITTING for
     * that one bounded response; retaining this content filter can instead
     * consume the ErrorDocument's first brigade as a second producer and turn
     * a configured error document into Apache's recursive generic 500. */
    ap_remove_output_filter(f);
    return apache_send_precommit_terminal_error(msr, f, NULL,
        HTTP_INTERNAL_SERVER_ERROR);
}


/*
 * A normal handler either consumes the request body or invokes
 * ap_discard_request_body() before it emits output.  This guard covers the
 * remaining host path: a handler that starts a response without doing either.
 * Discarding through Apache's input chain normally keeps the body streamed and
 * delivers EOS to MODSECURITY_IN. Apache may deliberately skip that drain
 * when the connection is already closing; in that case this filter aborts
 * rather than falsely finalizing an advertised body as empty before P3.
 */
static apr_status_t apache_finish_unread_request_body(ap_filter_t *f)
{
    request_rec *r = f->r;
    msc_t *msr = (msc_t *)f->ctx;
    int discard_status;
    int it;

    if (msr->request_body_processed)
    {
        return APR_SUCCESS;
    }
    if (ap_request_has_body(r))
    {
        discard_status = ap_discard_request_body(r);
        if (discard_status != OK)
        {
            ap_remove_output_filter(f);
            /* MODSECURITY_IN has already emitted its error bucket for a
             * disruptive Phase-2 decision; do not emit it a second time. */
            if (msr->request_body_intervention_sent)
            {
                return APR_EGENERAL;
            }
            return apache_send_precommit_terminal_error(msr, f, NULL,
                discard_status >= HTTP_BAD_REQUEST && discard_status <= 599
                    ? discard_status : HTTP_BAD_REQUEST);
        }
        if (!msr->request_body_processed)
        {
            /* ap_discard_request_body() is permitted to return OK without
             * reading when Apache is closing the connection. There is no
             * trustworthy EOS/P2 boundary in that path, so never enter P3. */
            ap_log_rerror(APLOG_MARK, APLOG_WARNING | APLOG_NOERRNO, 0, r,
                "ModSecurity: request body was not drained to EOS; aborting before response headers");
            ap_remove_output_filter(f);
            return APR_ECONNABORTED;
        }
        return APR_SUCCESS;
    }

    /* A request that does not advertise a body has no input EOS to drive the
     * filter, so complete its only valid empty terminal transition here. */
    it = msc_finalize_request_body(msr, r);
    if (it != N_INTERVENTION_STATUS)
    {
        ap_remove_output_filter(f);
        return apache_send_precommit_terminal_error(msr, f, NULL, it);
    }
    return APR_SUCCESS;
}


apr_status_t output_filter(ap_filter_t *f, apr_bucket_brigade *bb_in)
{
    request_rec *r = f->r;
    msc_t *msr = (msc_t *)f->ctx;
    msc_conf_t *conf = NULL;
    apr_bucket *pbktIn;
    apr_status_t rc;
    int error_status;
    int eos_seen = 0;
    int it;

    /* Do we have the context? */
    if (msr == NULL)
    {
        ap_log_error(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, f->r->server,
                "ModSecurity: Internal Error: msr is null in output filter.");
        ap_remove_output_filter(f);
        return apache_send_precommit_terminal_error(msr, f, NULL,
            HTTP_INTERNAL_SERVER_ERROR);
    }

    /* If the content chain still reaches this filter after Phase 4 has
     * resolved, discard the invalid later brigade. The protocol guard covers
     * the complementary reset-chain path. Only a true post-commit strict
     * intervention needs the transport abort fallback. */
    if (msr->response_phase4_gate_failed)
    {
        if (bb_in != NULL)
        {
            apr_brigade_cleanup(bb_in);
        }
        if (msr->phase4_strict_abort || msr->response_committed)
        {
            return apache_phase4_abort_response_connection(f);
        }
        return APR_EGENERAL;
    }
    if (msr->response_phase4_eos_released)
    {
        if (bb_in != NULL)
        {
            apr_brigade_cleanup(bb_in);
        }
        return APR_EGENERAL;
    }

    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL)
    {
        ap_remove_output_filter(f);
        return apache_send_precommit_terminal_error(msr, f, bb_in,
            HTTP_INTERNAL_SERVER_ERROR);
    }

    if (!msr->request_body_processed)
    {
        apr_status_t rc = apache_finish_unread_request_body(f);
        if (rc != APR_SUCCESS)
        {
            return rc;
        }
    }

    /* response headers */
    if (!msr->response_headers_processed)
    {
        const apr_array_header_t *arr = NULL;
        const apr_table_entry_t *te = NULL;
        const char *content_type;
        const char *wanted;
        int i;
        int original_status;

        arr = apr_table_elts(r->err_headers_out);
        te = (apr_table_entry_t *)arr->elts;
        for (i = 0; i < arr->nelts; i++)
        {
            const char *key = te[i].key;
            const char *val = te[i].val;
            msc_add_response_header(msr->t, (const unsigned char *)key,
                (const unsigned char *)val);
        }

        arr = apr_table_elts(r->headers_out);
        te = (apr_table_entry_t *)arr->elts;
        for (i = 0; i < arr->nelts; i++)
        {
            const char *key = te[i].key;
            const char *val = te[i].val;
            msc_add_response_header(msr->t, (const unsigned char *)key,
                (const unsigned char *)val);
        }

        content_type = apache_response_content_type(r);
        if (content_type != NULL && content_type[0] != '\0')
        {
            msc_add_response_header(msr->t,
                (const unsigned char *)"Content-Type",
                (const unsigned char *)content_type);
        }
        original_status = r->status;
        if (!apache_phase3_snapshot_response_state(msr, r))
        {
            ap_remove_output_filter(f);
            return apache_send_precommit_terminal_error(msr, f, bb_in,
                HTTP_INTERNAL_SERVER_ERROR);
        }
        if (msc_process_response_headers(msr->t, original_status, "HTTP 1.1") != 1)
        {
            ap_remove_output_filter(f);
            return apache_send_precommit_terminal_error(msr, f, bb_in,
                HTTP_INTERNAL_SERVER_ERROR);
        }
        msr->response_headers_seen = 1;
        msr->response_headers_processed = 1;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            wanted = msr->last_intervention_status >= 300 &&
                msr->last_intervention_status < 400 ? "redirect" : "deny";
            /* Header filtering runs before this output filter passes the
             * brigade downstream.  Record the exact status transition before
             * send_error_bucket can commit the visible response. */
            apache_phase3_log_event(msr, r, wanted, wanted, original_status);
            ap_remove_output_filter(f);
            return apache_send_precommit_terminal_error(msr, f, bb_in, it);
        }
    }

    if (bb_in == NULL)
    {
        return apache_phase4_fail_closed(msr, f, NULL,
            "missing response brigade");
    }

    error_status = apache_phase4_error_bucket_status(bb_in);
    if (error_status < 0)
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "malformed response error bucket before Phase 4 decision");
    }
    if (error_status > 0)
    {
        ap_remove_output_filter(f);
        return apache_send_precommit_terminal_error(msr, f, bb_in,
            error_status);
    }

    /* Response body. The C API does not expose libModSecurity's effective
     * SecResponseBodyMimeType selection, so a connector-side MIME list cannot
     * safely decide which responses may bypass this EOS-only Phase-4 gate.
     * Normalize Apache's one-response brigade contract before appending or
     * retaining it, then hold all valid response data through EOS. */
    eos_seen = apache_phase4_normalize_response_brigade(bb_in);
    for (pbktIn = APR_BRIGADE_FIRST(bb_in);
        pbktIn != APR_BRIGADE_SENTINEL(bb_in);
        pbktIn = APR_BUCKET_NEXT(pbktIn))
    {
        /* ap_save_brigade() sets aside and concatenates each retained APR
         * bucket. The payload byte limit therefore cannot bound the object
         * cost of a response fragmented into tiny data or metadata buckets. */
        if (msr->response_brigade_bucket_count >=
            MSCONNECTOR_PHASE4_MAX_HELD_BUCKETS)
        {
            return apache_phase4_fail_closed(msr, f, bb_in,
                "response brigade exceeds modsecurity_phase4_bucket_limit");
        }
        msr->response_brigade_bucket_count++;
        rc = apache_phase4_append_bucket(msr, conf, pbktIn);
        if (rc != APR_SUCCESS)
        {
            return apache_phase4_fail_closed(msr, f, bb_in,
                msr->response_body_truncated
                    ? "response body exceeds modsecurity_phase4_body_limit"
                    : "failed to append response body to libmodsecurity");
        }
    }

    /* Retain normalized data and terminal metadata across filter invocations.
     * ap_save_brigade() applies Apache's required setaside semantics and
     * empties bb_in on success. */
    rc = ap_save_brigade(f, &msr->response_brigade, &bb_in, r->pool);
    if (rc != APR_SUCCESS)
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "failed to set aside response brigade");
    }

    if (!eos_seen)
    {
        return APR_SUCCESS;
    }

    if (!msr->response_body_processed)
    {
        if (msc_process_response_body(msr->t) != 1)
        {
            return apache_phase4_fail_closed(msr, f, bb_in,
                "failed to finish response body in libmodsecurity");
        }
        msr->response_body_processed = 1;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            msconnector_late_intervention_policy policy;
            msconnector_late_intervention_action action;
            const char *wanted;
            const char *actual;

            msr->phase4_intervention = 1;
            msr->response_committed = apache_phase4_response_committed(msr, r);
            wanted = msr->last_intervention_status >= 300 &&
                msr->last_intervention_status < 400 ? "redirect" : "deny";
            msconnector_late_intervention_policy_init(&policy);
            action = msconnector_late_intervention_resolve(&policy,
                msr->response_committed, msr->response_committed,
                conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
            actual = apache_phase4_actual_action(action, wanted);
            if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)
            {
                apache_phase4_log_event(msr, r, wanted, actual,
                    "response_committed_safe");
                return apache_phase4_release_response_brigade(msr, f);
            }
            if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)
            {
                msr->phase4_strict_abort = 1;
                msr->response_committed = 1;
                msr->response_phase4_gate_failed = 1;
                msr->response_phase4_terminal_output =
                    MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
                apache_phase4_log_event(msr, r, wanted, actual,
                    "response_committed_strict");
                ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                    "ModSecurity: phase4 intervention after response commit, action=connection_abort");
                apr_brigade_cleanup(bb_in);
                msc_discard_response_brigade(msr);
                return apache_phase4_abort_response_connection(f);
            }
            apache_phase4_log_event(msr, r, wanted, actual,
                "response_not_committed");
            apr_brigade_cleanup(bb_in);
            msc_discard_response_brigade(msr);
            msr->response_phase4_gate_failed = 1;
            ap_remove_output_filter(f);
            return apache_send_precommit_terminal_error(msr, f, NULL, it);
        }
    }

    return apache_phase4_release_response_brigade(msr, f);
}
