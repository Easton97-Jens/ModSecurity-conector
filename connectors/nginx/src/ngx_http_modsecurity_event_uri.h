#ifndef NGX_HTTP_MODSECURITY_EVENT_URI_H
#define NGX_HTTP_MODSECURITY_EVENT_URI_H

#include "msconnector/event.h"
#include "msconnector/json_escape.h"
#include <string.h>

/* Project ONLY URI metadata at the NGX producer, before the unchanged strict
 * Common serializer. Stack storage is caller-owned and payload/query values
 * never enter the projected event. Escaped size, not merely byte count, is
 * bounded. Other original fields are copied unchanged and still fail closed. */
static inline int
ngx_http_modsecurity_bounded_event_uri(const msconnector_event *source,
    msconnector_event *projected, char *uri, size_t uri_size)
{
    size_t length;
    char *query;
    int truncated = 0;
    int redacted;
    static const char replacement[] = "?" MSCONNECTOR_EVENT_URI_REDACTION;

    if (source == NULL || projected == NULL || uri == NULL ||
        uri_size != MSCONNECTOR_EVENT_URI_SAFE_BUFFER_SIZE) {
        return 0;
    }
    *projected = *source;
    redacted = msconnector_event_uri_redact_query_ex(source->request.uri,
        uri, uri_size, &truncated);
    query = redacted ? strchr(uri, '?') : NULL;
    if (redacted) {
        /* Common may have truncated the path before reaching '?'. Retain
         * the redaction marker even then, without retaining query bytes. */
        size_t prefix = query != NULL ? (size_t)(query - uri) : strlen(uri);
        size_t maximum = uri_size - sizeof(replacement);
        if (prefix > maximum) {
            prefix = maximum;
            truncated = 1;
        }
        memcpy(uri + prefix, replacement, sizeof(replacement));
        query = uri + prefix;
    }
    length = strlen(uri);
    while (msconnector_json_escape_n(uri, length, NULL, 0U) >= uri_size) {
        if (query != NULL) {
            if (query == uri) return 0;
            --query;
            memcpy(query, replacement, sizeof(replacement));
        } else {
            uri[length - 1U] = '\0';
        }
        length = strlen(uri);
        truncated = 1;
    }
    projected->request.uri = uri;
    projected->flags.redacted = source->flags.redacted || redacted;
    projected->flags.truncated = source->flags.truncated || truncated;
    return 1;
}

#endif
