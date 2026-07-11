
#include "msc_filters.h"
#include "msc_utils.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/late_intervention.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"

#include <apr_file_io.h>
#include <string.h>
#include <strings.h>


/*
 * Phase 2 has exactly one terminal transition.  Input buckets may arrive in
 * many filter calls, while a handler which does not consume its request body
 * may cause Apache to discard that body later.  Both paths share this helper
 * so libmodsecurity never observes an append after end-of-stream.
 */
int msc_finalize_request_body(msc_t *msr, request_rec *r)
{
    if (msr == NULL || r == NULL || msr->t == NULL)
    {
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    if (msr->request_body_processed)
    {
        return N_INTERVENTION_STATUS;
    }
    if (msc_process_request_body(msr->t) < 0)
    {
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    msr->request_body_processed = 1;
    return process_intervention(msr->t, r);
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
        return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
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
                    return send_error_bucket(msr, f, it);
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
            return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
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


static const char *apache_normalized_content_type(apr_pool_t *pool,
    const char *value)
{
    char *copy;
    char *semi;
    char *end;

    if (value == NULL || value[0] == '\0')
    {
        return "";
    }

    copy = apr_pstrdup(pool, value);
    semi = strchr(copy, ';');
    if (semi != NULL)
    {
        *semi = '\0';
    }
    for (end = copy; *end != '\0'; end++)
    {
        /* Advance to the end so trailing whitespace can be trimmed below. */
    }
    while (end > copy && apr_isspace(*(end - 1)))
    {
        end--;
    }
    *end = '\0';
    while (*copy != '\0' && apr_isspace(*copy))
    {
        copy++;
    }
    for (end = copy; *end != '\0'; end++)
    {
        *end = apr_tolower(*end);
    }

    return copy;
}


static int apache_phase4_in_scope(msc_conf_t *conf, request_rec *r)
{
    static const char *defaults[] = {
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_TEXT_HTML,
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_TEXT_PLAIN,
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_APPLICATION_JSON,
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_APPLICATION_XML,
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_TEXT_XML,
        MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_APPLICATION_XHTML_XML
    };
    const char *content_type = apache_normalized_content_type(r->pool,
        apache_response_content_type(r));
    int i;

    if (content_type == NULL || content_type[0] == '\0')
    {
        return 0;
    }

    if (conf != NULL && conf->phase4_content_types != NULL)
    {
        const char **items = (const char **)conf->phase4_content_types->elts;
        for (i = 0; i < conf->phase4_content_types->nelts; i++)
        {
            if (strcasecmp(content_type, items[i]) == 0)
            {
                return 1;
            }
        }
        return 0;
    }

    for (i = 0; i < MSCONNECTOR_DEFAULT_PHASE4_CONTENT_TYPE_COUNT; i++)
    {
        if (strcasecmp(content_type, defaults[i]) == 0)
        {
            return 1;
        }
    }

    return 0;
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


static void apache_phase4_log_event(msc_t *msr, request_rec *r,
    const char *wanted, const char *actual, const char *reason)
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
            "ModSecurity: failed to open phase4 log %s",
            conf->common_config.phase4_log_path);
        return;
    }

    rule_id[0] = '\0';
    (void)msconnector_rule_id_extract_from_message(msr->last_intervention_log,
        rule_id, sizeof(rule_id));

    msconnector_event_init(&event);
    event.meta.message_id = strcmp(actual, "abort_connection") == 0
        ? MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200
        : (strcmp(actual, "log_only") == 0
            ? MSCONN_EVENT_PHASE4_LATE_INTERVENTION
            : MSCONN_EVENT_RESPONSE_BLOCKED);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = "phase4_intervention";
    event.meta.connector = "apache";
    event.meta.transaction_id = msr->event_transaction_id;
    event.decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual;
    event.decision.requested_action = wanted;
    event.decision.actual_action = actual;
    event.decision.rule_id = rule_id;
    event.decision.reason = reason;
    event.http.http_status = msr->last_intervention_status;
    event.http.original_http_status = r->status;
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
    event.body.content_type = apache_response_content_type(r);
    event.body.bytes_seen = msr->response_body_bytes_seen;
    event.body.bytes_inspected = msr->response_body_bytes_inspected;
    event.flags.late_intervention = msr->response_committed;
    event.flags.response_started = msr->response_committed;
    event.flags.response_committed = msr->response_committed;
    event.flags.headers_sent = msr->response_committed;
    event.flags.body_started = msr->response_committed;
    event.flags.connection_aborted = msr->phase4_strict_abort;
    event.flags.body_truncated = msr->response_body_truncated;

    if (msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated))
    {
        rc = apr_file_puts(line, file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write phase4 log %s",
                conf->common_config.phase4_log_path);
        }
    }
    else if (json_truncated)
    {
        rc = apr_file_puts(
            "{\"event\":\"phase4_intervention\",\"phase\":\"response_body\","
            "\"status\":\"blocked\",\"reason\":\"event serialization truncated\","
            "\"truncated\":true}\n",
            file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write truncated phase4 log %s",
                conf->common_config.phase4_log_path);
        }
    }
    else
    {
        rc = apr_file_puts(
            "{\"event\":\"phase4_intervention\",\"phase\":\"response_body\","
            "\"status\":\"error\",\"reason\":\"event serialization failed\"}\n",
            file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write failed phase4 log %s",
                conf->common_config.phase4_log_path);
        }
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, 0, r,
            "ModSecurity: failed to serialize common phase4 event");
    }

    rc = apr_file_close(file);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to close phase4 log %s",
            conf->common_config.phase4_log_path);
    }
}


static apr_status_t apache_phase4_append_bucket(msc_t *msr,
    msc_conf_t *conf, request_rec *r, apr_bucket *bucket)
{
    const char *data = NULL;
    apr_size_t len = 0;
    apr_size_t remaining;
    apr_status_t rc;
    int in_scope;

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
        msr->response_body_bytes_seen += len;
        in_scope = apache_phase4_in_scope(conf, r);
        if (!in_scope)
        {
            return APR_SUCCESS;
        }
        remaining = conf->common_config.phase4_body_limit > msr->response_body_bytes_inspected
            ? conf->common_config.phase4_body_limit - msr->response_body_bytes_inspected
            : 0;
        if (remaining > 0)
        {
            apr_size_t inspect_len = len < remaining ? len : remaining;
            if (msc_append_response_body(msr->t,
                    (const unsigned char *)data, inspect_len) < 0)
            {
                return APR_EGENERAL;
            }
            msr->response_body_bytes_inspected += inspect_len;
        }
        if (len > remaining)
        {
            msr->response_body_truncated = 1;
        }
    }

    return APR_SUCCESS;
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
            return send_error_bucket(msr, f,
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
        return send_error_bucket(msr, f, it);
    }
    return APR_SUCCESS;
}


apr_status_t output_filter(ap_filter_t *f, apr_bucket_brigade *bb_in)
{
    request_rec *r = f->r;
    msc_t *msr = (msc_t *)f->ctx;
    msc_conf_t *conf = NULL;
    apr_bucket *pbktIn;
    int eos_seen = 0;
    int it;

    /* Do we have the context? */
    if (msr == NULL)
    {
        ap_log_error(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, f->r->server,
                "ModSecurity: Internal Error: msr is null in output filter.");
        ap_remove_output_filter(f);
        return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
    }

    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL)
    {
        ap_remove_output_filter(f);
        return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
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
        int i;

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
        if (msc_process_response_headers(msr->t, r->status, "HTTP 1.1") < 0)
        {
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
        }
        msr->response_headers_seen = 1;
        msr->response_headers_processed = 1;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, it);
        }
    }

    /* response body */
    for (pbktIn = APR_BRIGADE_FIRST(bb_in);
        pbktIn != APR_BRIGADE_SENTINEL(bb_in);
        pbktIn = APR_BUCKET_NEXT(pbktIn))
    {
        apr_status_t rc;
        if (APR_BUCKET_IS_EOS(pbktIn))
        {
            eos_seen = 1;
        }
        rc = apache_phase4_append_bucket(msr, conf, r, pbktIn);
        if (rc != APR_SUCCESS)
        {
            return rc;
        }
    }

    if (!eos_seen)
    {
        /* Do not retain a brigade across filter calls.  The currently
         * inspected buckets remain owned by Apache and are passed on before
         * the upstream response reaches end-of-stream. */
        return ap_pass_brigade(f->next, bb_in);
    }

    if (!msr->response_body_processed)
    {
        if (msc_process_response_body(msr->t) < 0)
        {
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
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
            msr->response_committed = r->sent_bodyct > 0 ? 1 : 0;
            wanted = msr->last_intervention_status >= 300 &&
                msr->last_intervention_status < 400 ? "redirect" : "deny";
            if (!apache_phase4_in_scope(conf, r))
            {
                apache_phase4_log_event(msr, r, wanted, "log_only",
                    "content_type_not_in_scope");
                return ap_pass_brigade(f->next, bb_in);
            }
            msconnector_late_intervention_policy_init(&policy);
            action = msconnector_late_intervention_resolve(&policy,
                msr->response_committed, msr->response_committed,
                conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
            actual = apache_phase4_actual_action(action, wanted);
            if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)
            {
                apache_phase4_log_event(msr, r, wanted, actual,
                    "response_committed_safe");
                return ap_pass_brigade(f->next, bb_in);
            }
            if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)
            {
                msr->phase4_strict_abort = 1;
                msr->response_committed = 1;
                apache_phase4_log_event(msr, r, wanted, actual,
                    "response_committed_strict");
                ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                    "ModSecurity: phase4 intervention after response commit, action=connection_abort");
                ap_remove_output_filter(f);
                return APR_ECONNABORTED;
            }
            apache_phase4_log_event(msr, r, wanted, actual,
                "response_not_committed");
            apr_brigade_cleanup(bb_in);
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, it);
        }
    }

    return ap_pass_brigade(f->next, bb_in);
}
