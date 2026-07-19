

#include <ctype.h>

#include <modsecurity/modsecurity.h>
#if defined(MODSECURITY_CHECK_VERSION)
#if MODSECURITY_VERSION_NUM >= 304010
#define MSC_USE_RULES_SET 1
#endif
#endif

#if defined(MSC_USE_RULES_SET)
#include <modsecurity/rules_set.h>
#else
#include <modsecurity/rules.h>
#endif
#include <modsecurity/intervention.h>

#include "apr_buckets.h"
#include "apr_general.h"
#include "apr.h"
#include "apr_hash.h"
#include "apr_lib.h"
#include "apr_strings.h"
#define APR_WANT_STRFUNC
#include "apr_want.h"
#include "util_filter.h"

#include "httpd.h"
#include "ap_expr.h"
#include "http_config.h"
#include "http_connection.h"
#include "http_core.h"
#include "http_log.h"
#include "http_protocol.h"
#include "http_request.h"

#include "msc_filters.h"
#include "msconnector/config.h"
#include "msconnector/phase.h"
#include "msconnector/rule_load_stats.h"

#ifndef _SRC_APACHE_HTTP_MODSECURITY__
#define _SRC_APACHE_HTTP_MODSECURITY__

#define NOTE_MSR "modsecurity3-tx-context"
#define MSC_APACHE_CONNECTOR "ModSecurity-Apache v0.1.1-beta"
/* #define REQUEST_EARLY */
#define LATE_CONNECTION_PROCESS

#define N_INTERVENTION_STATUS 200

/* The protocol-level Phase-4 guard must allow Apache's synchronous terminal
 * error response (including a local ErrorDocument) before it seals the
 * request against an invalid later producer brigade. */
enum msc_phase4_terminal_output_state
{
    MSC_PHASE4_TERMINAL_OUTPUT_OPEN = 0,
    MSC_PHASE4_TERMINAL_OUTPUT_EMITTING,
    MSC_PHASE4_TERMINAL_OUTPUT_SEALED
};


typedef struct
{
    request_rec *r;
    /* The primary request owns the native transaction.  `r` changes while
     * sharing the context with redirects and subrequests, so cleanup must
     * retain this immutable owner separately. */
    request_rec *owner_request;
    Transaction *t;
    apr_size_t request_body_bytes_seen;
    apr_size_t request_body_bytes_inspected;
    apr_size_t response_body_bytes_seen;
    apr_size_t response_body_bytes_inspected;
    /* The Phase-4 payload cap does not by itself bound Apache bucket-object
     * overhead. Count every normalized bucket retained pending EOS. */
    apr_size_t response_brigade_bucket_count;
    int request_body_truncated;
    int request_body_processed;
    int request_body_intervention_sent;
    int response_headers_seen;
    int response_body_seen;
    int response_body_truncated;
    /* Apache normally commits this state when the first response brigade
     * reaches HTTP_HEADER. The Phase-4 gate delays that pass until EOS, so
     * retain the P3-inspected snapshot and restore it before release. */
    int response_headers_snapshot_taken;
    apr_table_t *response_headers_snapshot;
    apr_table_t *response_err_headers_snapshot;
    int response_status_snapshot;
    const char *response_status_line_snapshot;
    const char *response_content_type_snapshot;
    const char *response_content_encoding_snapshot;
    apr_array_header_t *response_content_languages_snapshot;
    apr_off_t response_clength_snapshot;
    int response_chunked_snapshot;
    int response_no_cache_snapshot;
    /* HTTP_HEADER derives further visible response behavior from these
     * request controls when it finally runs. Retain the P3-era values rather
     * than a whole notes/environment table so unrelated late request state is
     * not discarded by the Phase-4 response gate. */
    int response_note_no_etag_snapshot_set;
    const char *response_note_no_etag_snapshot;
    int response_env_force_no_vary_snapshot_set;
    const char *response_env_force_no_vary_snapshot;
    int response_env_downgrade_1_0_snapshot_set;
    const char *response_env_downgrade_1_0_snapshot;
    int response_env_force_response_1_0_snapshot_set;
    const char *response_env_force_response_1_0_snapshot;
    int response_env_nokeepalive_snapshot_set;
    const char *response_env_nokeepalive_snapshot;
    int response_proto_num_snapshot;
    int response_header_only_snapshot;
    int response_assbackwards_snapshot;
    int response_proxyreq_snapshot;
    int response_expecting_100_snapshot;
    apr_time_t response_request_time_snapshot;
    /* LibModSecurity's effective MIME policy is opaque to the C connector.
     * Every Apache response is set aside until EOS so a disruptive
     * response-body decision is made before Apache can commit it. */
    apr_bucket_brigade *response_brigade;
    /* A terminal Phase-4 error, deny, or late abort must keep this filter
     * authoritative for the remainder of the request. A producer that ignores
     * the returned error must not bypass the gate with another brigade. */
    int response_phase4_gate_failed;
    enum msc_phase4_terminal_output_state response_phase4_terminal_output;
    /* At most one Apache-core local ErrorDocument redirect may use the
     * bounded terminal-emission exception. Nested redirects would otherwise
     * turn this exception into a path around the Phase-4 request boundary. */
    int response_phase4_terminal_error_redirect_seen;
    /* This filter has passed its retained EOS to the next output filter. Any
     * later producer brigade is invalid and must not create a second response
     * sequence. */
    int response_phase4_eos_released;
    int response_committed;
    int response_headers_processed;
    int response_body_processed;
    int phase4_intervention;
    int phase4_strict_abort;
    int last_intervention_status;
    const char *last_intervention_log;
    const char *event_transaction_id;
    /* A libmodsecurity log callback is synchronous with the host processing
     * call.  Keep only the active lifecycle phase so a non-disruptive rule
     * match can be recorded as native metadata without retaining its text. */
    enum msconnector_phase native_event_phase;
    int native_event_phase_active;
} msc_t;


typedef struct
{
    void *rules_set;
    msconnector_config common_config;
    ap_expr_info_t *transaction_id_expr;
    apr_array_header_t *phase4_content_types;
    msconnector_rule_load_stats rule_load_stats;
    char *name_for_debug;
} msc_conf_t;

typedef struct
{
    ModSecurity *modsec;
} msc_global;

extern module AP_MODULE_DECLARE_DATA security3_module;
extern msc_global *msc_apache;
extern const command_rec module_directives[];


int process_intervention (Transaction *t, request_rec *r);
int msc_finalize_request_body(msc_t *msr, request_rec *r);
void apache_emit_intervention_event(msc_t *msr, request_rec *r,
    const char *event_name, enum msconnector_phase phase,
    const char *wanted, const char *actual, const char *reason,
    int original_status, int response_committed);
void apache_log_rule_match_event(msc_t *msr, request_rec *r,
    enum msconnector_phase phase, const char *rule_id);

int msc_apache_init(apr_pool_t *pool);
int msc_apache_cleanup();

#endif /*  _SRC_APACHE_HTTP_MODSECURITY__ */
