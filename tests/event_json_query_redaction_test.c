#include "msconnector/event.h"
#include "msconnector/event_jsonl.h"
#include "msconnector/integrity_event.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

const char *msconnector_phase_name(enum msconnector_phase phase) {
    (void)phase;
    return "connection";
}

static void check_uri(const char *input, const char *expected, int redacted) {
    msconnector_event event;
    char json[4096];
    char jsonl[4096];
    char safe[256];
    uint64_t hash;

    msconnector_event_init(&event);
    event.request.method = strcmp(input, "*") == 0 ? "OPTIONS" : "GET";
    event.request.uri = input;
    assert(msconnector_event_uri_query_redacted(input) == redacted);
    assert(msconnector_event_uri_redact_query(input, safe, sizeof(safe)) == redacted);
    assert(strcmp(safe, expected) == 0);
    hash = msconnector_integrity_event_hash(&event, 0U);
    event.integrity.event_hash = hash;
    assert(msconnector_integrity_event_chain_verify(0U, hash, &event));
    assert(msconnector_event_write_json(&event, json, sizeof(json)));
    assert(strstr(json, "\"uri\":\"") != NULL);
    assert(strstr(json, expected) != NULL);
    assert(strstr(json, "CANARY") == NULL);
    assert(strstr(json, redacted ? "\"redacted\":true" : "\"redacted\":false") != NULL);
    assert(msconnector_event_write_jsonl_line(&event, jsonl, sizeof(jsonl), NULL));
    assert(strstr(jsonl, "CANARY") == NULL);
    assert(strcmp(event.request.uri, input) == 0);
}

int main(void) {
    msconnector_event event;
    uint64_t safe_hash;

    check_uri("/path?x=CANARY", "/path?<redacted>", 1);
    check_uri("/path", "/path", 0);
    check_uri("/path?", "/path?", 0);
    check_uri("https://example.test/path?x=CANARY", "https://example.test/path?<redacted>", 1);
    check_uri("*", "*", 0);
    check_uri("example.test:443", "example.test:443", 0);

    msconnector_event_init(&event);
    event.request.uri = "/path?x=CANARY";
    safe_hash = msconnector_integrity_event_hash(&event, 0U);
    event.request.uri = "/path?<redacted>";
    assert(msconnector_integrity_event_hash(&event, 0U) == safe_hash);
    event.request.uri = "/path?x=OTHER";
    assert(msconnector_integrity_event_hash(&event, 0U) == safe_hash);
    return 0;
}
