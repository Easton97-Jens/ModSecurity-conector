#ifndef MSCONNECTOR_HTTP_STATUS_H
#define MSCONNECTOR_HTTP_STATUS_H

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral HTTP response status metadata.
 *
 * This table is common metadata only. It does not change any connector runtime
 * response behavior unless a connector explicitly integrates it in a separate
 * tested change. Unknown syntactically valid status codes use safe fallback
 * text; invalid status codes return invalid-status fallback text.
 */
typedef enum msconnector_http_status_class {
    MSCONNECTOR_HTTP_STATUS_CLASS_UNKNOWN = 0,
    MSCONNECTOR_HTTP_STATUS_CLASS_INFORMATIONAL = 1,
    MSCONNECTOR_HTTP_STATUS_CLASS_SUCCESS = 2,
    MSCONNECTOR_HTTP_STATUS_CLASS_REDIRECTION = 3,
    MSCONNECTOR_HTTP_STATUS_CLASS_CLIENT_ERROR = 4,
    MSCONNECTOR_HTTP_STATUS_CLASS_SERVER_ERROR = 5
} msconnector_http_status_class;

typedef struct msconnector_http_status_info {
    int status;
    const char *reason_phrase;
    const char *default_message;
    msconnector_http_status_class status_class;
    int suitable_for_blocking;
} msconnector_http_status_info;

const msconnector_http_status_info *msconnector_http_status_info_find(int status);
const char *msconnector_http_status_reason_phrase(int status);
const char *msconnector_http_status_default_message(int status);
msconnector_http_status_class msconnector_http_status_classify(int status);
int msconnector_http_status_is_valid(int status);
int msconnector_http_status_is_error(int status);
int msconnector_http_status_is_block_response(int status);

#ifdef __cplusplus
}
#endif

#endif
