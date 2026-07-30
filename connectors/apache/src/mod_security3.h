

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
    apr_size_t body_bytes_seen;
    apr_size_t body_bytes_inspected;
    int body_truncated;
    int body_processed;
    int body_intervention_sent;
} msc_request_state;

typedef struct
{
    int headers_snapshot_taken;
    apr_table_t *headers_snapshot;
    apr_table_t *err_headers_snapshot;
    int status_snapshot;
    const char *status_line_snapshot;
    const char *content_type_snapshot;
    const char *content_encoding_snapshot;
    apr_array_header_t *content_languages_snapshot;
    apr_off_t clength_snapshot;
    int chunked_snapshot;
    int no_cache_snapshot;
} msc_response_headers_snapshot;

typedef struct
{
    int note_no_etag_snapshot_set;
    const char *note_no_etag_snapshot;
    int env_force_no_vary_snapshot_set;
    const char *env_force_no_vary_snapshot;
    int env_downgrade_1_0_snapshot_set;
    const char *env_downgrade_1_0_snapshot;
    int env_force_response_1_0_snapshot_set;
    const char *env_force_response_1_0_snapshot;
    int env_nokeepalive_snapshot_set;
    const char *env_nokeepalive_snapshot;
    int proto_num_snapshot;
    int header_only_snapshot;
    int assbackwards_snapshot;
    int proxyreq_snapshot;
    int expecting_100_snapshot;
    apr_time_t request_time_snapshot;
} msc_response_request_snapshot;

typedef struct
{
    apr_size_t body_bytes_seen;
    apr_size_t body_bytes_inspected;
    apr_size_t brigade_bucket_count;
    int body_truncated;
    int headers_seen;
    int body_seen;
    apr_bucket_brigade *brigade;
    int gate_failed;
    enum msc_phase4_terminal_output_state terminal_output;
    int terminal_error_redirect_seen;
    int eos_released;
    int committed;
    int headers_processed;
    int body_processed;
    int phase4_intervention;
    int phase4_strict_abort;
} msc_response_state;

typedef struct
{
    int last_status;
    const char *last_log;
    const char *transaction_id;
    enum msconnector_phase native_event_phase;
    int native_event_phase_active;
} msc_intervention_state;


typedef struct
{
    request_rec *r;
    /* The primary request owns the native transaction.  `r` changes while
     * sharing the context with redirects and subrequests, so cleanup must
     * retain this immutable owner separately. */
    request_rec *owner_request;
    Transaction *t;
    msc_request_state request;
    /* Apache normally commits visible state in HTTP_HEADER. The Phase-4 gate
     * retains the P3 state until its own EOS decision has completed. */
    msc_response_headers_snapshot response_headers;
    msc_response_request_snapshot response_request;
    /* LibModSecurity's effective MIME policy is opaque to the C connector,
     * so this state owns the all-response pre-commit Phase-4 gate. */
    msc_response_state response;
    /* A log callback is synchronous with host processing; retain only the
     * decision needed to emit bounded native metadata. */
    msc_intervention_state intervention;
} msc_t;

/* Keep the established field vocabulary at call sites while grouping the
 * connector's internal state by lifecycle responsibility. */
#define request_body_bytes_seen request.body_bytes_seen
#define request_body_bytes_inspected request.body_bytes_inspected
#define request_body_truncated request.body_truncated
#define request_body_processed request.body_processed
#define request_body_intervention_sent request.body_intervention_sent
#define response_headers_snapshot_taken response_headers.headers_snapshot_taken
#define response_headers_snapshot response_headers.headers_snapshot
#define response_err_headers_snapshot response_headers.err_headers_snapshot
#define response_status_snapshot response_headers.status_snapshot
#define response_status_line_snapshot response_headers.status_line_snapshot
#define response_content_type_snapshot response_headers.content_type_snapshot
#define response_content_encoding_snapshot response_headers.content_encoding_snapshot
#define response_content_languages_snapshot response_headers.content_languages_snapshot
#define response_clength_snapshot response_headers.clength_snapshot
#define response_chunked_snapshot response_headers.chunked_snapshot
#define response_no_cache_snapshot response_headers.no_cache_snapshot
#define response_note_no_etag_snapshot_set response_request.note_no_etag_snapshot_set
#define response_note_no_etag_snapshot response_request.note_no_etag_snapshot
#define response_env_force_no_vary_snapshot_set response_request.env_force_no_vary_snapshot_set
#define response_env_force_no_vary_snapshot response_request.env_force_no_vary_snapshot
#define response_env_downgrade_1_0_snapshot_set response_request.env_downgrade_1_0_snapshot_set
#define response_env_downgrade_1_0_snapshot response_request.env_downgrade_1_0_snapshot
#define response_env_force_response_1_0_snapshot_set response_request.env_force_response_1_0_snapshot_set
#define response_env_force_response_1_0_snapshot response_request.env_force_response_1_0_snapshot
#define response_env_nokeepalive_snapshot_set response_request.env_nokeepalive_snapshot_set
#define response_env_nokeepalive_snapshot response_request.env_nokeepalive_snapshot
#define response_proto_num_snapshot response_request.proto_num_snapshot
#define response_header_only_snapshot response_request.header_only_snapshot
#define response_assbackwards_snapshot response_request.assbackwards_snapshot
#define response_proxyreq_snapshot response_request.proxyreq_snapshot
#define response_expecting_100_snapshot response_request.expecting_100_snapshot
#define response_request_time_snapshot response_request.request_time_snapshot
#define response_body_bytes_seen response.body_bytes_seen
#define response_body_bytes_inspected response.body_bytes_inspected
#define response_brigade_bucket_count response.brigade_bucket_count
#define response_body_truncated response.body_truncated
#define response_headers_seen response.headers_seen
#define response_body_seen response.body_seen
#define response_brigade response.brigade
#define response_phase4_gate_failed response.gate_failed
#define response_phase4_terminal_output response.terminal_output
#define response_phase4_terminal_error_redirect_seen response.terminal_error_redirect_seen
#define response_phase4_eos_released response.eos_released
#define response_headers_processed response.headers_processed
#define response_body_processed response.body_processed
#define phase4_intervention response.phase4_intervention
#define phase4_strict_abort response.phase4_strict_abort
#define last_intervention_status intervention.last_status
#define last_intervention_log intervention.last_log
#define event_transaction_id intervention.transaction_id
#define native_event_phase intervention.native_event_phase
#define native_event_phase_active intervention.native_event_phase_active


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

typedef struct
{
    const char *event_name;
    enum msconnector_phase phase;
    const char *wanted;
    const char *actual;
    const char *reason;
    int original_status;
    int response_already_committed;
} apache_intervention_event_input;

extern module AP_MODULE_DECLARE_DATA security3_module;
extern msc_global *msc_apache;
extern const command_rec module_directives[];


int process_intervention (Transaction *t, request_rec *r);
int msc_finalize_request_body(msc_t *msr, request_rec *r);
void apache_emit_intervention_event(msc_t *msr, request_rec *r,
    const apache_intervention_event_input *input);
void apache_log_rule_match_event(msc_t *msr, request_rec *r,
    enum msconnector_phase phase, const char *rule_id);

int msc_apache_init(apr_pool_t *pool);
int msc_apache_cleanup();

#endif /*  _SRC_APACHE_HTTP_MODSECURITY__ */
