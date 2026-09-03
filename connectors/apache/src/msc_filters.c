
#include "msc_filters.h"
#include "msc_utils.h"
#include "http_protocol.h"
#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/late_intervention.h"
#include "msconnector/limits.h"
#include "msconnector/options.h"
#include "msconnector/rule_id.h"

#include <apr_file_io.h>
#include <string.h>


/* Kept private to this translation unit; Phase 2 reaches it before the
 * implementation below because input-filter EOS is handled near the start
 * of this file. */
static void apache_log_intervention_event(msc_t *msr, request_rec *r,
    const apache_intervention_event_input *input);


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
    if (msr->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&
        !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_REQUEST_BODY))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P2 transition");
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
    msr->native_event_phase_active = 1;
    if (msc_process_request_body(msr->t) != 1)
    {
        msr->native_event_phase_active = 0;
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    msr->native_event_phase_active = 0;
    if (!msc_apache_contract_complete(msr,
            MSCONNECTOR_PHASE_REQUEST_BODY))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P2 completion");
        return HTTP_INTERNAL_SERVER_ERROR;
    }
    msr->request_body_processed = 1;
    /* process_intervention() may reject an invalid native status after P2
     * completed. Keep the immediately preceding business phase active while
     * it maps that error so the bounded failure event cannot fall back to P1. */
    msr->native_event_phase = MSCONNECTOR_PHASE_REQUEST_BODY;
    msr->native_event_phase_active = 1;
    intervention = process_intervention(msr->t, r);
    msr->native_event_phase_active = 0;
    if (intervention != N_INTERVENTION_STATUS)
    {
        if (!msc_apache_contract_record_intervention_decision(msr))
        {
            (void)msc_apache_contract_fail(msr,
                MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
            apache_emit_contract_failure_event(msr, r,
                MSCONNECTOR_PHASE_REQUEST_BODY,
                MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
                HTTP_INTERNAL_SERVER_ERROR);
            ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
                "ModSecurity: could not record canonical P2 intervention decision");
            return HTTP_INTERNAL_SERVER_ERROR;
        }

        if (msr->last_intervention_body_limit)
        {
            apache_emit_contract_failure_event(msr, r,
                MSCONNECTOR_PHASE_REQUEST_BODY,
                MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT,
                HTTP_REQUEST_ENTITY_TOO_LARGE);
        }
        else
        {
            apache_intervention_event_input event_input;
            const char *action = msc_apache_contract_intervention_action(msr);

            /* This is the actual Apache input-filter terminal path.  Emit the
             * bounded decision metadata before returning the disruptive status to
             * httpd, rather than reconstructing Phase 2 from audit output. */
            event_input.event_name = "phase2_intervention";
            event_input.phase = MSCONNECTOR_PHASE_REQUEST_BODY;
            event_input.wanted = action;
            event_input.actual = action;
            event_input.reason = "request_body_before_handler";
            event_input.original_status = r->status;
            event_input.response_already_committed = 0;
            apache_log_intervention_event(msr, r, &event_input);
        }
    }
    return intervention;
}


/*
 * Translate an input-filter terminal failure through Apache's core error
 * handler instead of driving the request output chain recursively while a
 * caller such as mod_proxy is synchronously prefetching the request body.
 * AP_FILTER_ERROR is Apache's handled-input-filter sentinel: ordinary APR
 * errors are remapped by body discard/prefetch callers to a generic error.
 *
 * The Phase-4 terminal-output member is a protocol-chain guard, not an
 * assertion that Phase 4 ran or failed. ap_die() resets resource filters and
 * retains that guard while it synchronously emits the one local error
 * response; do not set response_phase4_gate_failed for this P2 path.
 */
static apr_status_t apache_input_filter_terminal_error(msc_t *msr,
    request_rec *r, int status)
{
    if (r == NULL || r->connection == NULL)
    {
        return APR_EGENERAL;
    }
    if (msr != NULL)
    {
        msc_discard_response_brigade(msr);
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_EMITTING;
    }

    /* ap_die() treats an existing error status as recursive handling. A P2
     * intervention is a new terminal response, so start from the neutral
     * status and let the core install the selected response status. */
    r->status = HTTP_OK;
    r->status_line = NULL;
    ap_die(status, r);

    if (msr != NULL)
    {
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
    }
    return AP_FILTER_ERROR;
}


static apr_status_t apache_input_filter_handle_eos(msc_t *msr, request_rec *r,
    ap_filter_t *filter, apr_bucket_brigade *output, apr_bucket *bucket)
{
    int intervention;

    /* A repeated observed EOS is a host/protocol sequence error, not an
     * idempotent request-body completion. A no-body request legitimately
     * completes P2 before its first empty host EOS reaches this filter, so
     * distinguish that first forwarded EOS from a true duplicate. */
    if (msr->request_body_eos_released)
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_REQUEST_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: duplicate request-body EOS rejected");
        msr->request_body_intervention_sent = 1;
        ap_remove_input_filter(filter);
        return apache_input_filter_terminal_error(msr, r,
            HTTP_INTERNAL_SERVER_ERROR);
    }

    if (!msr->request_body_processed)
    {
        intervention = msc_finalize_request_body(msr, r);
        if (intervention != N_INTERVENTION_STATUS)
        {
            msr->request_body_intervention_sent = 1;
            ap_remove_input_filter(filter);
            return apache_input_filter_terminal_error(msr, r, intervention);
        }
    }
    msr->request_body_eos_released = 1;
    APR_BUCKET_REMOVE(bucket);
    APR_BRIGADE_INSERT_TAIL(output, bucket);

    /* mod_proxy can ask the core input chain to replay the terminal EOS after
     * this successful forwarding.  It is not another request-body phase or
     * another Common EOS.  Detach this adapter only after the one canonical
     * P2 EOS has moved downstream, so such host reads bypass the phase bridge
     * instead of being misclassified as a second client EOS. */
    ap_remove_input_filter(filter);
    return APR_SUCCESS;
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
        return apache_input_filter_terminal_error(msr, r,
            HTTP_INTERNAL_SERVER_ERROR);
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
        if (APR_BUCKET_IS_EOS(pbktIn))
        {
            return apache_input_filter_handle_eos(msr, r, f, pbbOut, pbktIn);
        }

        ret=apr_bucket_read(pbktIn, &data, &len, block);
        if (ret != APR_SUCCESS)
        {
            return ret;
        }

        if (msr->contract.active_phase != MSCONNECTOR_PHASE_REQUEST_BODY &&
            !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_REQUEST_BODY))
        {
            (void)msc_apache_contract_fail(msr,
                MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
            apache_emit_contract_failure_event(msr, r,
                MSCONNECTOR_PHASE_REQUEST_BODY,
                MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
                HTTP_INTERNAL_SERVER_ERROR);
            ap_remove_input_filter(f);
            return apache_input_filter_terminal_error(msr, r,
                HTTP_INTERNAL_SERVER_ERROR);
        }
        if (!msc_apache_contract_record_body(msr, 0, (size_t)len))
        {
            msconnector_transaction_error_class error_class =
                msr->contract.error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT
                ? MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT
                : MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE;
            int status = error_class == MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT
                ? HTTP_REQUEST_ENTITY_TOO_LARGE : HTTP_INTERNAL_SERVER_ERROR;

            msr->request_body_bytes_seen = msr->contract.request_body_bytes;
            (void)msc_apache_contract_fail(msr, error_class);
            apache_emit_contract_failure_event(msr, r,
                MSCONNECTOR_PHASE_REQUEST_BODY, error_class, status);
            ap_remove_input_filter(f);
            return apache_input_filter_terminal_error(msr, r,
                status);
        }
        if (msc_append_request_body(msr->t,
                (const unsigned char *)data, len) != 1)
        {
            (void)msc_apache_contract_fail(msr,
                MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
            apache_emit_contract_failure_event(msr, r,
                MSCONNECTOR_PHASE_REQUEST_BODY,
                MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
                HTTP_INTERNAL_SERVER_ERROR);
            ap_remove_input_filter(f);
            return apache_input_filter_terminal_error(msr, r,
                HTTP_INTERNAL_SERVER_ERROR);
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
        if (requested_action != NULL &&
            (strcmp(requested_action, "redirect") == 0 ||
            strcmp(requested_action, "rate_limit") == 0))
        {
            return requested_action;
        }
        return "deny";
    }
    return name;
}

static const char *apache_intervention_message_id(
    const apache_intervention_event_input *input)
{
    if (strcmp(input->event_name, "body_limit") == 0)
    {
        return MSCONN_EVENT_BODY_LIMIT;
    }
    if (strcmp(input->event_name, "invalid_engine_response") == 0)
    {
        return MSCONN_EVENT_INVALID_ENGINE_RESPONSE;
    }
    if (strcmp(input->event_name, "protocol_error") == 0)
    {
        return MSCONN_EVENT_PROTOCOL_ERROR;
    }
    if (strcmp(input->event_name, "connector_error") == 0)
    {
        return MSCONN_EVENT_CONNECTOR_ERROR;
    }
    if (input->phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        input->phase == MSCONNECTOR_PHASE_REQUEST_BODY)
    {
        return MSCONN_EVENT_REQUEST_BLOCKED;
    }
    if (input->phase != MSCONNECTOR_PHASE_RESPONSE_BODY)
    {
        return MSCONN_EVENT_RESPONSE_BLOCKED;
    }
    if (strcmp(input->actual, "abort_connection") == 0)
    {
        return MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200;
    }
    if (strcmp(input->actual, "log_only") == 0)
    {
        return MSCONN_EVENT_PHASE4_LATE_INTERVENTION;
    }
    return MSCONN_EVENT_RESPONSE_BLOCKED;
}

static const char *apache_intervention_content_type(request_rec *r,
    enum msconnector_phase phase)
{
    if (phase == MSCONNECTOR_PHASE_REQUEST_HEADERS ||
        phase == MSCONNECTOR_PHASE_REQUEST_BODY)
    {
        return apache_request_content_type(r);
    }
    return apache_response_content_type(r);
}

static apr_size_t apache_intervention_body_bytes_seen(const msc_t *msr,
    enum msconnector_phase phase)
{
    if (phase == MSCONNECTOR_PHASE_REQUEST_BODY)
    {
        return msr->request_body_bytes_seen;
    }
    if (phase == MSCONNECTOR_PHASE_RESPONSE_BODY)
    {
        return msr->response_body_bytes_seen;
    }
    return 0U;
}

static apr_size_t apache_intervention_body_bytes_inspected(const msc_t *msr,
    enum msconnector_phase phase)
{
    if (phase == MSCONNECTOR_PHASE_REQUEST_BODY)
    {
        return msr->request_body_bytes_inspected;
    }
    if (phase == MSCONNECTOR_PHASE_RESPONSE_BODY)
    {
        return msr->response_body_bytes_inspected;
    }
    return 0U;
}

static void apache_intervention_set_http(msconnector_event *event,
    const msc_t *msr, const request_rec *r,
    const apache_intervention_event_input *input)
{
    event->http.http_status = msr->last_intervention_status;
    event->http.original_http_status = input->original_status;
    if (strcmp(input->actual, "deny") == 0 ||
        strcmp(input->actual, "redirect") == 0 ||
        strcmp(input->actual, "rate_limit") == 0)
    {
        event->http.visible_http_status = msr->last_intervention_status;
        event->http.transport_result = "http_status";
    }
    else if (strcmp(input->actual, "abort_connection") == 0)
    {
        event->http.visible_http_status = input->original_status;
        event->http.transport_result = "connection_aborted";
    }
    else
    {
        event->http.visible_http_status = r->status;
        event->http.transport_result = "log_only";
    }
}

static void apache_intervention_write_event(apr_file_t *file,
    request_rec *r, const char *log_path,
    const apache_intervention_event_input *input,
    const msconnector_event *event)
{
    apr_status_t rc;
    char line[4096];
    int json_truncated = 0;

    if (msconnector_event_write_jsonl_line(event, line, sizeof(line),
        &json_truncated))
    {
        rc = apr_file_puts(line, file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write intervention log %s", log_path);
        }
        return;
    }
    if (json_truncated)
    {
        rc = apr_file_puts(apr_psprintf(r->pool,
            "{\"event\":\"%s\",\"integration_mode\":\"native-httpd-module\",\"phase\":\"%s\","
            "\"status\":\"blocked\",\"reason\":\"event serialization truncated\","
            "\"truncated\":true}\n", input->event_name,
            apache_event_phase_name(input->phase)), file);
        if (rc != APR_SUCCESS)
        {
            ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
                "ModSecurity: failed to write truncated intervention log %s",
                log_path);
        }
        return;
    }
    rc = apr_file_puts(apr_psprintf(r->pool,
        "{\"event\":\"%s\",\"integration_mode\":\"native-httpd-module\",\"phase\":\"%s\","
        "\"status\":\"error\",\"reason\":\"event serialization failed\"}\n",
        input->event_name, apache_event_phase_name(input->phase)), file);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to write failed intervention log %s", log_path);
    }
    ap_log_rerror(APLOG_MARK, APLOG_WARNING, 0, r,
        "ModSecurity: failed to serialize common intervention event");
}


static void apache_log_intervention_event(msc_t *msr, request_rec *r,
    const apache_intervention_event_input *input)
{
    msc_conf_t *conf;
    apr_file_t *file = NULL;
    apr_status_t rc;
    msconnector_event event;
    char rule_id[MSCONNECTOR_MAX_RULE_ID_LENGTH];

    if (msr == NULL || r == NULL || input == NULL ||
        r->per_dir_config == NULL)
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
    event.meta.message_id = apache_intervention_message_id(input);
    event.meta.level = msconnector_event_default_level(event.meta.message_id);
    event.meta.message = msconnector_event_default_message(event.meta.message_id);
    event.meta.event = input->event_name;
    event.meta.connector = "apache";
    event.meta.integration_mode = "native-httpd-module";
    event.meta.transaction_id = msr->event_transaction_id;
    event.decision.phase = input->phase;
    event.decision.status = MSCONNECTOR_STATUS_BLOCKED;
    event.decision.action = input->actual;
    event.decision.requested_action = input->wanted;
    event.decision.actual_action = input->actual;
    event.decision.rule_id = rule_id;
    event.decision.reason = input->reason;
    apache_intervention_set_http(&event, msr, r, input);
    event.request.method = r->method;
    event.request.uri = r->unparsed_uri;
    event.body.content_type = apache_intervention_content_type(r, input->phase);
    event.body.bytes_seen = apache_intervention_body_bytes_seen(msr,
        input->phase);
    event.body.bytes_inspected = apache_intervention_body_bytes_inspected(msr,
        input->phase);
    event.body.limit_outcome = strcmp(input->event_name, "body_limit") == 0
        ? "reject" : NULL;
    event.flags.late_intervention = input->response_already_committed;
    if (input->response_already_committed)
    {
        event.flags.late_intervention_mode = apache_phase4_mode_name(
            conf->common_config.phase4_mode);
    }
    event.flags.response_started = input->response_already_committed;
    event.flags.response_committed = input->response_already_committed;
    event.flags.headers_sent = input->response_already_committed;
    event.flags.body_started = input->phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        input->response_already_committed;
    /* Phase-2/4 intervention records are emitted only after their explicit
     * body finish boundary; this is not a claim about client completion. */
    event.flags.eos_seen = input->phase == MSCONNECTOR_PHASE_REQUEST_BODY ||
        input->phase == MSCONNECTOR_PHASE_RESPONSE_BODY;
    event.flags.connection_aborted = input->phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        strcmp(input->actual, "abort_connection") == 0;
    event.flags.body_truncated = input->phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        msr->response_body_truncated;

    apache_intervention_write_event(file, r,
        conf->common_config.phase4_log_path, input, &event);

    rc = apr_file_close(file);
    if (rc != APR_SUCCESS)
    {
        ap_log_rerror(APLOG_MARK, APLOG_WARNING, rc, r,
            "ModSecurity: failed to close intervention log %s",
            conf->common_config.phase4_log_path);
    }
}


void apache_emit_intervention_event(msc_t *msr, request_rec *r,
    const apache_intervention_event_input *input)
{
    apache_log_intervention_event(msr, r, input);
}


static const char *apache_contract_failure_event_name(
    msconnector_transaction_error_class error_class)
{
    switch (error_class)
    {
        case MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT:
            return "body_limit";
        case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE:
            return "invalid_engine_response";
        case MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE:
        case MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL:
            return "protocol_error";
        default:
            return "connector_error";
    }
}

static const char *apache_contract_failure_reason(
    msconnector_transaction_error_class error_class)
{
    switch (error_class)
    {
        case MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT:
            return "request_body_limit_exceeded";
        case MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE:
            return "invalid_engine_response";
        case MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE:
            return "invalid_phase_sequence";
        case MSCONNECTOR_TRANSACTION_ERROR_PROTOCOL:
            return "protocol_error";
        default:
            return "connector_error";
    }
}

static void apache_emit_contract_failure_event_with_action(msc_t *msr,
    request_rec *r, enum msconnector_phase phase,
    msconnector_transaction_error_class error_class, int status,
    const char *actual)
{
    apache_intervention_event_input input;

    if (msr == NULL || r == NULL || status < HTTP_BAD_REQUEST ||
        status > 599 || actual == NULL ||
        msr->contract_failure_event_emitted)
    {
        return;
    }
    /* A contract failure is terminal. Preserve exactly one payload-free
     * observability record and never derive a rule ID from a malformed engine
     * message. */
    msr->contract_failure_event_emitted = 1;
    msr->last_intervention_status = status;
    msr->last_intervention_log = "";
    input.event_name = apache_contract_failure_event_name(error_class);
    input.phase = phase;
    input.wanted = "deny";
    input.actual = actual;
    input.reason = apache_contract_failure_reason(error_class);
    input.original_status = phase == MSCONNECTOR_PHASE_RESPONSE_BODY &&
        strcmp(actual, "abort_connection") == 0 &&
        msr->response_headers_snapshot_taken
        ? msr->response_status_snapshot : r->status;
    input.response_already_committed = msr->response.committed;
    apache_log_intervention_event(msr, r, &input);
}


void apache_emit_contract_failure_event(msc_t *msr, request_rec *r,
    enum msconnector_phase phase,
    msconnector_transaction_error_class error_class, int status)
{
    apache_emit_contract_failure_event_with_action(msr, r, phase,
        error_class, status, "deny");
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
    apache_intervention_event_input input;

    input.event_name = "phase4_intervention";
    input.phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    input.wanted = wanted;
    input.actual = actual;
    input.reason = reason;
    input.original_status = r->status;
    input.response_already_committed = msr != NULL ? msr->response.committed : 0;
    apache_log_intervention_event(msr, r, &input);
}


static void apache_phase3_log_event(msc_t *msr, request_rec *r,
    const char *wanted, const char *actual, int original_status)
{
    apache_intervention_event_input input;

    input.event_name = "phase3_intervention";
    input.phase = MSCONNECTOR_PHASE_RESPONSE_HEADERS;
    input.wanted = wanted;
    input.actual = actual;
    input.reason = "response_headers_before_commit";
    input.original_status = original_status;
    input.response_already_committed = 0;
    apache_log_intervention_event(msr, r, &input);
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
        if (msr->contract.active_phase != MSCONNECTOR_PHASE_RESPONSE_BODY &&
            !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_RESPONSE_BODY))
        {
            return APR_EGENERAL;
        }
        msr->response_body_seen = 1;
        /* Phase 4 has an EOS-only final decision. libModSecurity owns the
         * effective SecResponseBodyMimeType policy, but its C API does not
         * expose a safe way for this connector to query that selection.
         * Therefore every response bucket is appended exactly once before the
         * current non-terminal brigade is forwarded. Processing a bounded
         * prefix and then forwarding an uninspected tail would recreate the
         * bypass, so an oversize current bucket is rejected before forwarding;
         * output committed by an earlier brigade is never rewritten.
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
        if (!msc_apache_contract_record_body(msr, 1, plan.append_size))
        {
            return APR_EGENERAL;
        }
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


static apr_bucket *apache_phase4_normalize_response_brigade(
    apr_bucket_brigade *bb_in)
{
    apr_bucket *bucket;
    apr_bucket *next;
    apr_bucket *eos = NULL;

    for (bucket = APR_BRIGADE_FIRST(bb_in);
        bucket != APR_BRIGADE_SENTINEL(bb_in); bucket = next)
    {
        next = APR_BUCKET_NEXT(bucket);
        /* Apache output-filter ownership ends at the first EOS. No later
         * bucket belongs to this response, so never append, retain, or emit
         * it. This also ensures a malformed one-brigade suffix cannot bypass
         * the terminal Phase-4 decision. */
        if (eos != NULL)
        {
            APR_BUCKET_REMOVE(bucket);
            apr_bucket_destroy(bucket);
            continue;
        }
        if (APR_BUCKET_IS_EOS(bucket))
        {
            eos = bucket;
            continue;
        }
    }
    return eos;
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
static apr_status_t apache_phase4_abort_response_connection(ap_filter_t *f);


static int apache_phase4_brigade_starts_response(
    const apr_bucket_brigade *brigade)
{
    apr_bucket *bucket;

    if (brigade == NULL)
    {
        return 0;
    }
    for (bucket = APR_BRIGADE_FIRST(brigade);
        bucket != APR_BRIGADE_SENTINEL(brigade);
        bucket = APR_BUCKET_NEXT(bucket))
    {
        if (APR_BUCKET_IS_FLUSH(bucket) ||
            (!APR_BUCKET_IS_METADATA(bucket) && !APR_BUCKET_IS_EOS(bucket)))
        {
            return 1;
        }
    }
    return 0;
}

static apr_status_t apache_phase4_release_response_brigade(msc_t *msr,
    ap_filter_t *f, apr_bucket_brigade *brigade, int terminal)
{
    apr_status_t rc;
    int starts_response;
    request_rec *r;

    if (msr == NULL || f == NULL || f->next == NULL || brigade == NULL)
    {
        return apache_phase4_fail_closed(msr, f, brigade,
            "missing progressive response brigade");
    }
    r = f->r;
    starts_response = apache_phase4_brigade_starts_response(brigade);
    if ((starts_response || terminal) && !msr->response.committed &&
        !apache_phase3_restore_response_state(msr, f->r))
    {
        return apache_phase4_fail_closed(msr, f, brigade,
            "missing Phase 3 response-state snapshot");
    }
    /* The next-filter invocation is the Apache commitment boundary. Record
     * it immediately before forwarding any data or FLUSH bucket: a failing
     * downstream filter can have emitted a prefix, so treating that boundary
     * as committed is the conservative, non-rewriteable outcome. */
    if ((starts_response || terminal) && !msr->response.committed)
    {
        if (!msc_apache_contract_mark_response_committed(msr))
        {
            return apache_phase4_fail_closed(msr, f, brigade,
                "canonical response commitment is invalid");
        }
        msr->response.committed = 1;
    }
    if (terminal)
    {
        msr->response_phase4_eos_released = 1;
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_EMITTING;
    }
    rc = ap_pass_brigade(f->next, brigade);
    if (rc != APR_SUCCESS)
    {
        /* A progressive downstream failure may already have exposed a body
         * prefix. Seal the transaction before returning so no later brigade
         * can be appended to a response whose native output path failed.
         * Record the host failure while the contract is still mutable too:
         * otherwise cleanup would misclassify an incomplete output stream as
         * ordinary P4 completion or generic premature cleanup. */
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        msr->response_phase4_gate_failed = 1;
        msr->response.committed = 1;
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
        apache_emit_contract_failure_event_with_action(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR, "abort_connection");
        rc = apache_phase4_abort_response_connection(f);
    }
    if (terminal)
    {
        msr->response_phase4_terminal_output =
            MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
        apr_brigade_cleanup(brigade);
    }
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
    /* A progressive prefix becomes non-rewriteable when it crosses this
     * filter's next-filter boundary. Native sent_bodyct/eos_sent remain
     * unsuitable because upstream/core can set them before this filter sees
     * the brigade; bytes_sent remains a second, host-provided proof. */
    return (msr != NULL && (msr->response.committed ||
        msr->response_phase4_eos_released)) ||
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

    if (r == NULL || r->connection == NULL)
    {
        return APR_EGENERAL;
    }
    /* The pre-commit core error path must never be selected after any
     * progressive response prefix crossed the next-filter boundary. A later
     * Apache error bucket is therefore terminal transport failure, not a
     * second response that ap_die() may render. */
    if (apache_phase4_response_committed(msr, r))
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "precommit terminal error requested after response commit");
    }
    if (bb_in != NULL)
    {
        apr_brigade_cleanup(bb_in);
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
    msconnector_transaction_error_class error_class;

    error_class = MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR;
    if (msr != NULL && msr->response_body_truncated)
    {
        error_class = MSCONNECTOR_TRANSACTION_ERROR_BODY_LIMIT;
    }

    if (bb_in != NULL)
    {
        apr_brigade_cleanup(bb_in);
    }
    msc_discard_response_brigade(msr);
    if (msr != NULL)
    {
        (void)msc_apache_contract_fail(msr, error_class);
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
            msr->response.committed = 1;
            msr->response_phase4_terminal_output =
                MSC_PHASE4_TERMINAL_OUTPUT_SEALED;
        }
        apache_emit_contract_failure_event_with_action(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_BODY,
            error_class,
            HTTP_INTERNAL_SERVER_ERROR, "abort_connection");
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: Phase 4 response gate failed after response commit: %s",
            reason != NULL ? reason : "unspecified failure");
        return apache_phase4_abort_response_connection(f);
    }

    ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
        "ModSecurity: Phase 4 response gate failed before response commit: %s",
        reason != NULL ? reason : "unspecified failure");
    apache_emit_contract_failure_event(msr, r,
        MSCONNECTOR_PHASE_RESPONSE_BODY,
        error_class,
        HTTP_INTERNAL_SERVER_ERROR);
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
            /* MODSECURITY_IN has already invoked the core terminal path for
             * a disruptive Phase-2 decision; do not emit it a second time. */
            if (msr->request_body_intervention_sent)
            {
                return AP_FILTER_ERROR;
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


static apr_status_t apache_output_filter_terminal_result(msc_t *msr,
    ap_filter_t *filter, apr_bucket_brigade *brigade, int *handled)
{
    *handled = 0;
    if (msr->response_phase4_gate_failed)
    {
        *handled = 1;
        if (brigade != NULL)
        {
            apr_brigade_cleanup(brigade);
        }
        if (msr->phase4_strict_abort || msr->response.committed)
        {
            return apache_phase4_abort_response_connection(filter);
        }
        return APR_EGENERAL;
    }
    if (msr->response_phase4_eos_released)
    {
        *handled = 1;
        if (brigade != NULL)
        {
            apr_brigade_cleanup(brigade);
        }
        return APR_EGENERAL;
    }
    return APR_SUCCESS;
}

static int apache_add_response_headers(msc_t *msr, apr_table_t *headers)
{
    const apr_array_header_t *entries;
    const apr_table_entry_t *header;
    int index;

    if (msr == NULL || msr->t == NULL) {
        return 0;
    }
    if (headers == NULL) {
        return 1;
    }
    entries = apr_table_elts(headers);
    if (entries == NULL || entries->nelts == 0) {
        return entries != NULL;
    }
    if (entries->elts == NULL) {
        return 0;
    }
    header = (const apr_table_entry_t *)entries->elts;
    for (index = 0; index < entries->nelts; index++)
    {
        if (header[index].key == NULL || header[index].val == NULL ||
            msc_add_response_header(msr->t,
                (const unsigned char *)header[index].key,
                (const unsigned char *)header[index].val) != 1)
        {
            return 0;
        }
    }
    return 1;
}

static int apache_response_header_metrics(const apr_table_t *headers,
    size_t *count, size_t *bytes)
{
    const apr_array_header_t *entries;
    const apr_table_entry_t *header;
    int index;

    if (headers == NULL || count == NULL || bytes == NULL)
    {
        return 1;
    }
    entries = apr_table_elts(headers);
    if (entries == NULL || entries->elts == NULL)
    {
        return 1;
    }
    header = (const apr_table_entry_t *)entries->elts;
    for (index = 0; index < entries->nelts; ++index)
    {
        size_t name_size = header[index].key == NULL ? 0U : strlen(header[index].key);
        size_t value_size = header[index].val == NULL ? 0U : strlen(header[index].val);

        if (name_size == 0U || name_size > MSCONNECTOR_MAX_HEADER_NAME_LENGTH ||
            value_size > MSCONNECTOR_MAX_HEADER_VALUE_LENGTH ||
            *count >= MSCONNECTOR_MAX_HEADER_COUNT ||
            name_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes ||
            value_size > MSCONNECTOR_MAX_TOTAL_HEADER_BYTES - *bytes - name_size)
        {
            return 0;
        }
        ++*count;
        *bytes += name_size + value_size;
    }
    return 1;
}

static int apache_contract_record_response_metadata(msc_t *msr,
    request_rec *r, const char *content_type, size_t body_limit)
{
    size_t header_count = 0U;
    size_t header_bytes = 0U;

    if (msr == NULL || r == NULL || !msr->contract_initialized ||
        !apache_response_header_metrics(r->err_headers_out, &header_count,
            &header_bytes) ||
        !apache_response_header_metrics(r->headers_out, &header_count,
            &header_bytes))
    {
        return 0;
    }
    return msconnector_transaction_contract_record_response_metadata(&msr->contract,
        r->status, content_type, header_count, header_bytes, body_limit) ==
        MSCONNECTOR_TRANSACTION_TRANSITION_OK;
}

static apr_status_t apache_output_filter_process_headers(msc_t *msr,
    request_rec *r, ap_filter_t *filter, apr_bucket_brigade *brigade)
{
    const char *content_type;
    const char *wanted;
    msc_conf_t *conf;
    int original_status;
    int intervention;
    int error_headers_added;
    int response_headers_added;

    if (msr->response_headers_processed)
    {
        return APR_SUCCESS;
    }
    conf = (msc_conf_t *)ap_get_module_config(r->per_dir_config,
        &security3_module);
    if (conf == NULL)
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    content_type = apache_response_content_type(r);
    if (!apache_contract_record_response_metadata(msr, r, content_type,
            conf->common_config.phase4_body_limit))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    if (!msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_RESPONSE_HEADERS))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: invalid canonical P3 transition");
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    error_headers_added = apache_add_response_headers(msr, r->err_headers_out);
    response_headers_added = apache_add_response_headers(msr, r->headers_out);
    if (!error_headers_added || !response_headers_added ||
        (content_type != NULL && content_type[0] != '\0' &&
            msc_add_response_header(msr->t,
                (const unsigned char *)"Content-Type",
                (const unsigned char *)content_type) != 1))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    original_status = r->status;
    if (!apache_phase3_snapshot_response_state(msr, r))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    if (msc_process_response_headers(msr->t, original_status, "HTTP 1.1") != 1)
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_CONNECTOR,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    if (!msc_apache_contract_complete(msr,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_PHASE_SEQUENCE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    msr->response_headers_seen = 1;
    msr->response_headers_processed = 1;
    /* See the P2 handoff: an invalid status can be reported only when the
     * native intervention is collected, after Common has completed P3. */
    msr->native_event_phase = MSCONNECTOR_PHASE_RESPONSE_HEADERS;
    msr->native_event_phase_active = 1;
    intervention = process_intervention(msr->t, r);
    msr->native_event_phase_active = 0;
    if (intervention == N_INTERVENTION_STATUS)
    {
        return APR_SUCCESS;
    }
    if (!msc_apache_contract_record_intervention_decision(msr))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
        apache_emit_contract_failure_event(msr, r,
            MSCONNECTOR_PHASE_RESPONSE_HEADERS,
            MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
            HTTP_INTERNAL_SERVER_ERROR);
        ap_log_rerror(APLOG_MARK, APLOG_ERR | APLOG_NOERRNO, 0, r,
            "ModSecurity: could not record canonical P3 intervention decision");
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, brigade,
            HTTP_INTERNAL_SERVER_ERROR);
    }
    wanted = msc_apache_contract_intervention_action(msr);
    apache_phase3_log_event(msr, r, wanted, wanted, original_status);
    ap_remove_output_filter(filter);
    return apache_send_precommit_terminal_error(msr, filter, brigade,
        intervention);
}

static apr_status_t apache_output_filter_prepare_response_brigade(msc_t *msr,
    msc_conf_t *conf, ap_filter_t *filter, apr_bucket_brigade **brigade,
    apr_bucket **eos_bucket)
{
    apr_bucket *bucket;
    apr_status_t rc;
    int error_status;

    if (*brigade == NULL)
    {
        return apache_phase4_fail_closed(msr, filter, NULL,
            "missing response brigade");
    }
    error_status = apache_phase4_error_bucket_status(*brigade);
    if (error_status < 0)
    {
        return apache_phase4_fail_closed(msr, filter, *brigade,
            "malformed response error bucket before Phase 4 decision");
    }
    if (error_status > 0)
    {
        ap_remove_output_filter(filter);
        return apache_send_precommit_terminal_error(msr, filter, *brigade,
            error_status);
    }
    *eos_bucket = apache_phase4_normalize_response_brigade(*brigade);
    for (bucket = APR_BRIGADE_FIRST(*brigade);
        bucket != APR_BRIGADE_SENTINEL(*brigade);
        bucket = APR_BUCKET_NEXT(bucket))
    {
        rc = apache_phase4_append_bucket(msr, conf, bucket);
        if (rc != APR_SUCCESS)
        {
            return apache_phase4_fail_closed(msr, filter, *brigade,
                msr->response_body_truncated
                    ? "response body exceeds modsecurity_phase4_body_limit"
                    : "failed to append response body to libmodsecurity");
        }
    }
    return APR_SUCCESS;
}

static apr_status_t apache_phase4_finish_response_body(msc_t *msr,
    ap_filter_t *f, apr_bucket_brigade *bb_in, int *intervention)
{
    if (msr->contract.active_phase != MSCONNECTOR_PHASE_RESPONSE_BODY &&
        !msc_apache_contract_begin(msr, MSCONNECTOR_PHASE_RESPONSE_BODY))
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "invalid canonical P4 transition");
    }
    if (msc_process_response_body(msr->t) != 1)
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "failed to finish response body in libmodsecurity");
    }
    if (!msc_apache_contract_complete(msr, MSCONNECTOR_PHASE_RESPONSE_BODY))
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "invalid canonical P4 completion");
    }
    msr->response_body_processed = 1;
    /* Preserve P4 as the error correlation while process_intervention()
     * validates the terminal native response after Common completed EOS. */
    msr->native_event_phase = MSCONNECTOR_PHASE_RESPONSE_BODY;
    msr->native_event_phase_active = 1;
    *intervention = process_intervention(msr->t, f->r);
    msr->native_event_phase_active = 0;
    if (*intervention != N_INTERVENTION_STATUS &&
        !msc_apache_contract_record_intervention_decision(msr))
    {
        (void)msc_apache_contract_fail(msr,
            MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE);
        apache_emit_contract_failure_event(msr, f->r,
            MSCONNECTOR_PHASE_RESPONSE_BODY,
            MSCONNECTOR_TRANSACTION_ERROR_INVALID_ENGINE_RESPONSE,
            HTTP_INTERNAL_SERVER_ERROR);
        return apache_phase4_fail_closed(msr, f, bb_in,
            "could not record canonical P4 intervention decision");
    }
    return APR_SUCCESS;
}

static apr_status_t apache_phase4_handle_intervention(msc_t *msr,
    msc_conf_t *conf, ap_filter_t *f, apr_bucket_brigade *bb_in,
    int intervention)
{
    request_rec *r = f->r;
    msconnector_late_intervention_policy policy;
    msconnector_late_intervention_action action;
    const char *wanted;
    const char *actual;

    msr->phase4_intervention = 1;
    msr->response.committed = apache_phase4_response_committed(msr, r);
    wanted = msc_apache_contract_intervention_action(msr);
    msconnector_late_intervention_policy_init(&policy);
    action = msconnector_late_intervention_resolve(&policy,
        msr->response.committed, msr->response.committed,
        conf->common_config.phase4_mode == MSCONNECTOR_PHASE4_MODE_STRICT);
    actual = apache_phase4_actual_action(action, wanted);
    if (action == MSCONNECTOR_LATE_INTERVENTION_LOG_ONLY)
    {
        apache_phase4_log_event(msr, r, wanted, actual,
            "response_committed_safe");
        return APR_SUCCESS;
    }
    if (action == MSCONNECTOR_LATE_INTERVENTION_ABORT_CONNECTION)
    {
        msr->phase4_strict_abort = 1;
        msr->response.committed = 1;
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
    return apache_send_precommit_terminal_error(msr, f, NULL, intervention);
}

static apr_status_t apache_output_filter_finish_response(msc_t *msr,
    msc_conf_t *conf, ap_filter_t *f, apr_bucket_brigade *bb_in,
    apr_bucket_brigade *terminal_brigade)
{
    int intervention = N_INTERVENTION_STATUS;
    apr_status_t rc;

    if (!msr->response_body_processed)
    {
        rc = apache_phase4_finish_response_body(msr, f, bb_in,
            &intervention);
        if (rc != APR_SUCCESS)
        {
            return rc;
        }
        if (intervention != N_INTERVENTION_STATUS)
        {
            rc = apache_phase4_handle_intervention(msr, conf, f, bb_in,
                intervention);
            if (rc != APR_SUCCESS)
            {
                return rc;
            }
        }
    }
    return apache_phase4_release_response_brigade(msr, f, terminal_brigade,
        1);
}

apr_status_t output_filter(ap_filter_t *f, apr_bucket_brigade *bb_in)
{
    request_rec *r = f->r;
    msc_t *msr = (msc_t *)f->ctx;
    msc_conf_t *conf = NULL;
    apr_status_t rc;
    apr_bucket *eos_bucket = NULL;
    apr_bucket_brigade *terminal_brigade = NULL;
    int terminal_handled;

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
    rc = apache_output_filter_terminal_result(msr, f, bb_in,
        &terminal_handled);
    if (terminal_handled)
    {
        return rc;
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
        apr_status_t request_body_rc = apache_finish_unread_request_body(f);
        if (request_body_rc != APR_SUCCESS)
        {
            return request_body_rc;
        }
    }

    rc = apache_output_filter_process_headers(msr, r, f, bb_in);
    if (rc != APR_SUCCESS)
    {
        return rc;
    }

    /* Response body. The C API does not expose libModSecurity's effective
     * SecResponseBodyMimeType selection, so every response remains in the
     * bounded Common inspection path. The adapter keeps only the current
     * Apache brigade: it appends its borrowed data buckets once, forwards the
     * pre-EOS prefix immediately, and retains only the terminal EOS fragment
     * long enough to run the one-shot final P4 decision. */
    rc = apache_output_filter_prepare_response_brigade(msr, conf, f, &bb_in,
        &eos_bucket);
    if (rc != APR_SUCCESS)
    {
        return rc;
    }
    if (eos_bucket == NULL)
    {
        return apache_phase4_release_response_brigade(msr, f, bb_in, 0);
    }
    terminal_brigade = apr_brigade_split_ex(bb_in, eos_bucket, NULL);
    if (terminal_brigade == NULL)
    {
        return apache_phase4_fail_closed(msr, f, bb_in,
            "failed to split response brigade at EOS");
    }
    if (APR_BRIGADE_FIRST(bb_in) != APR_BRIGADE_SENTINEL(bb_in))
    {
        rc = apache_phase4_release_response_brigade(msr, f, bb_in, 0);
        if (rc != APR_SUCCESS)
        {
            apr_brigade_cleanup(terminal_brigade);
            return rc;
        }
    }
    return apache_output_filter_finish_response(msr, conf, f,
        terminal_brigade, terminal_brigade);
}
