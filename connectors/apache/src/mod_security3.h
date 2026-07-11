

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
#include "msconnector/rule_load_stats.h"

#ifndef _SRC_APACHE_HTTP_MODSECURITY__
#define _SRC_APACHE_HTTP_MODSECURITY__

#define NOTE_MSR "modsecurity3-tx-context"
#define MSC_APACHE_CONNECTOR "ModSecurity-Apache v0.1.1-beta"
/* #define REQUEST_EARLY */
#define LATE_CONNECTION_PROCESS

#define N_INTERVENTION_STATUS 200


typedef struct
{
    request_rec *r;
    Transaction *t;
    apr_size_t request_body_bytes_seen;
    apr_size_t request_body_bytes_inspected;
    apr_size_t response_body_bytes_seen;
    apr_size_t response_body_bytes_inspected;
    int request_body_truncated;
    int request_body_processed;
    int request_body_intervention_sent;
    int response_headers_seen;
    int response_body_seen;
    int response_body_truncated;
    int response_committed;
    int response_headers_processed;
    int response_body_processed;
    int phase4_intervention;
    int phase4_strict_abort;
    int last_intervention_status;
    const char *last_intervention_log;
    const char *event_transaction_id;
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

int msc_apache_init(apr_pool_t *pool);
int msc_apache_cleanup();

#endif /*  _SRC_APACHE_HTTP_MODSECURITY__ */
