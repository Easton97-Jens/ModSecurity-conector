
#include "msc_filters.h"
#include "msc_utils.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"

#include <apr_file_io.h>
#include <string.h>
#include <strings.h>


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
        apr_bucket *pbktOut;
        const char *data;
        apr_size_t len;
        int it;

        if (APR_BUCKET_IS_EOS(pbktIn))
        {
            APR_BUCKET_REMOVE(pbktIn);
            APR_BRIGADE_INSERT_TAIL(pbbOut, pbktIn);
            break;
        }

        ret=apr_bucket_read(pbktIn, &data, &len, block);
        if (ret != APR_SUCCESS)
        {
            return ret;
        }

        msc_append_request_body(msr->t, (const unsigned char *)data, len);
        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            ap_remove_input_filter(f);
            return send_error_bucket(msr, f, it);
        }

        // FIXME: Now we should have the body. Is this sane?
        msc_process_request_body(msr->t);

        pbktOut = apr_bucket_heap_create(data, len, 0, c->bucket_alloc);
        APR_BRIGADE_INSERT_TAIL(pbbOut, pbktOut);
        apr_bucket_delete(pbktIn);
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
    event.meta.event = MSCONN_EVENT_PHASE4_LATE_INTERVENTION;
    event.meta.connector = MSC_APACHE_CONNECTOR;
    event.decision.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = actual;
    event.decision.requested_action = wanted;
    event.decision.actual_action = actual;
    event.decision.rule_id = rule_id;
    event.decision.reason = reason;
    event.http.http_status = msr->last_intervention_status;
    event.http.original_http_status = r->status;
    event.http.visible_http_status = r->status;
    event.request.method = r->method;
    event.request.uri = r->unparsed_uri;
    event.flags.late_intervention = 1;
    event.flags.response_started = msr->response_committed;
    event.flags.headers_sent = msr->response_headers_seen;
    event.flags.body_started = msr->response_body_seen;
    event.flags.connection_aborted = msr->phase4_strict_abort;
    event.flags.body_truncated = msr->response_body_truncated;

    if (msconnector_event_write_jsonl_line(&event, line, sizeof(line),
        &json_truncated))
    {
        apr_file_puts(line, file);
    }
    else
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, 0, r,
            "ModSecurity: failed to serialize common phase4 event");
    }

    apr_file_close(file);
}


static apr_status_t apache_phase4_buffer_bucket(ap_filter_t *f,
    msc_t *msr, msc_conf_t *conf, apr_bucket *bucket)
{
    apr_bucket *copy = NULL;
    const char *data = NULL;
    apr_size_t len = 0;
    apr_size_t remaining;
    apr_status_t rc;

    if (APR_BUCKET_IS_EOS(bucket) || APR_BUCKET_IS_METADATA(bucket))
    {
        rc = apr_bucket_copy(bucket, &copy);
        if (rc != APR_SUCCESS)
        {
            return rc;
        }
        APR_BRIGADE_INSERT_TAIL(msr->response_brigade, copy);
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
        remaining = conf->common_config.phase4_body_limit > msr->response_body_bytes_inspected
            ? conf->common_config.phase4_body_limit - msr->response_body_bytes_inspected
            : 0;
        if (remaining > 0)
        {
            apr_size_t inspect_len = len < remaining ? len : remaining;
            msc_append_response_body(msr->t, (const unsigned char *)data, inspect_len);
            msr->response_body_bytes_inspected += inspect_len;
        }
        if (len > remaining)
        {
            msr->response_body_truncated = 1;
        }
    }

    rc = apr_bucket_copy(bucket, &copy);
    if (rc != APR_SUCCESS)
    {
        copy = apr_bucket_heap_create(data, len, NULL,
            f->r->connection->bucket_alloc);
    }
    if (copy == NULL)
    {
        return APR_EGENERAL;
    }
    APR_BRIGADE_INSERT_TAIL(msr->response_brigade, copy);
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

    if (msr->response_brigade == NULL)
    {
        msr->response_brigade = apr_brigade_create(r->pool,
            r->connection->bucket_alloc);
        if (msr->response_brigade == NULL)
        {
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, HTTP_INTERNAL_SERVER_ERROR);
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
        msc_process_response_headers(msr->t, r->status, "HTTP 1.1");
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
        rc = apache_phase4_buffer_bucket(f, msr, conf, pbktIn);
        if (rc != APR_SUCCESS)
        {
            return rc;
        }
    }

    apr_brigade_cleanup(bb_in);
    if (!eos_seen)
    {
        return APR_SUCCESS;
    }

    if (!msr->response_body_processed)
    {
        msc_process_response_body(msr->t);
        msr->response_body_processed = 1;

        it = process_intervention(msr->t, r);
        if (it != N_INTERVENTION_STATUS)
        {
            msr->phase4_intervention = 1;
            msr->response_committed = r->sent_bodyct > 0 ? 1 : 0;
            if (!apache_phase4_in_scope(conf, r))
            {
                apache_phase4_log_event(msr, r, "deny", "log_only",
                    "content_type_not_in_scope");
                msr->response_committed = 1;
                return ap_pass_brigade(f->next, msr->response_brigade);
            }
            if (conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_MINIMAL)
            {
                apache_phase4_log_event(msr, r, "deny", "log_only",
                    "phase4_mode_minimal");
                msr->response_committed = 1;
                return ap_pass_brigade(f->next, msr->response_brigade);
            }
            if (msr->response_committed)
            {
                msr->phase4_strict_abort = 1;
                msr->response_committed = 1;
                apache_phase4_log_event(msr, r, "deny",
                    "connection_abort", "headers_or_body_already_sent");
                ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                    "ModSecurity: phase4 intervention after response commit, action=connection_abort");
                ap_remove_output_filter(f);
                return APR_ECONNABORTED;
            }
            apache_phase4_log_event(msr, r, "deny", "deny_status",
                "buffered_before_commit");
            apr_brigade_cleanup(msr->response_brigade);
            ap_remove_output_filter(f);
            return send_error_bucket(msr, f, it);
        }
    }

    msr->response_committed = 1;
    return ap_pass_brigade(f->next, msr->response_brigade);
}
