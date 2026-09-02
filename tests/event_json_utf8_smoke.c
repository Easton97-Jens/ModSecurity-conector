/*
 * Focused Common-event regression smoke.
 *
 * Manual run (from the repository root):
 *   cc -std=c17 -Wall -Wextra -Werror -Icommon/include \
 *     tests/event_json_utf8_smoke.c <all Common C sources> -o /tmp/event-json-smoke \
 *     && /tmp/event-json-smoke | python3 -c 'import json,sys; json.loads(sys.stdin.read())'
 */

#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/json_escape.h"

#include <stdio.h>
#include <string.h>

static int expect_string(const char *actual, const char *expected) {
    return actual != NULL && expected != NULL && strcmp(actual, expected) == 0;
}
int main(void) {
    static const char invalid_utf8[] = {
        'o', 'k', (char)0x80, (char)0xc0, (char)0xaf, '\0'
    };
    static const char valid_utf8[] = {
        'o', 'k', (char)0xc3, (char)0xa4, '\0'
    };
    static const char embedded_nul[] = {'a', '\0', 'b'};
    char escaped[128];
    char json[16384];
    char bounded_json[16384];
    char unterminated[1024];
    msconnector_event event;
    int truncated = 0;

    if (!expect_string(
            (msconnector_json_escape(invalid_utf8, escaped, sizeof(escaped)), escaped),
            "ok\\u0080\\u00c0\\u00af") ||
        !expect_string(
            (msconnector_json_escape(valid_utf8, escaped, sizeof(escaped)), escaped),
            valid_utf8) ||
        !expect_string(
            (msconnector_json_escape_n(embedded_nul, sizeof(embedded_nul),
                escaped, sizeof(escaped)), escaped),
            "a\\u0000b")) {
        (void)fprintf(stderr, "event JSON UTF-8 escaping control failed\n");
        return 1;
    }

    msconnector_event_init(&event);
    event.meta.timestamp = "2026-08-24T00:00:00Z";
    event.meta.level = "error";
    event.meta.message_id = "MSCONN_EVENT_INTERNAL_ERROR";
    event.meta.event = event.meta.message_id;
    event.meta.connector = "event-json-smoke";
    event.request.uri = invalid_utf8;
    event.protocol.requested_protocol = invalid_utf8;
    if (!msconnector_event_write_jsonl_line(&event, json, sizeof(json),
            &truncated) || truncated != 0 ||
        strstr(json, "\\u0080\\u00c0\\u00af") == NULL ||
        strstr(json,
            "\"requested_protocol\":\"ok\\\\u0080\\\\u00c0\\\\u00af\"") == NULL) {
        (void)fprintf(stderr, "event JSONL UTF-8 serialization control failed\n");
        return 1;
    }

    /* The event writer reads no more than its declared metadata input cap. */
    memset(unterminated, 'x', sizeof(unterminated));
    event.request.uri = unterminated;
    truncated = 0;
    if (msconnector_event_write_json_ex(&event, bounded_json, sizeof(bounded_json),
            &truncated) != 0 || truncated == 0) {
        (void)fprintf(stderr, "event metadata bound control failed\n");
        return 1;
    }

    (void)fputs(json, stdout);
    return 0;
}
