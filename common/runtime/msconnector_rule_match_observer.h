#ifndef MSCONNECTOR_RULE_MATCH_OBSERVER_H
#define MSCONNECTOR_RULE_MATCH_OBSERVER_H

#include "msconnector/limits.h"
#include "msconnector/phase.h"

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* The observer is per native transaction. It never retains RuleMessage text,
 * headers, bodies, audit paths, or dynamically allocated data. */
#define MSCONNECTOR_RULE_MATCH_OBSERVER_MAX_MATCHES 32U
#define MSCONNECTOR_RULE_MATCH_OBSERVER_RULE_ID_SIZE 13U

typedef struct msconnector_rule_match_observer_match {
    char rule_id[MSCONNECTOR_RULE_MATCH_OBSERVER_RULE_ID_SIZE];
    enum msconnector_phase phase;
    int emitted;
} msconnector_rule_match_observer_match;

typedef struct msconnector_rule_match_observer {
    char expected_transaction_id[MSCONNECTOR_MAX_TRANSACTION_ID_LENGTH];
    size_t expected_transaction_id_length;
    msconnector_rule_match_observer_match matches[
        MSCONNECTOR_RULE_MATCH_OBSERVER_MAX_MATCHES];
    size_t match_count;
    int enabled;
    int failed;
} msconnector_rule_match_observer;

void msconnector_rule_match_observer_init(
    msconnector_rule_match_observer *observer,
    int enabled,
    const char *expected_transaction_id);

/* Installs a RuleMessage-only callback on the supplied ModSecurity instance.
 * The pointer is intentionally opaque to the C runtime. */
int msconnector_rule_match_observer_install(void *modsecurity);

/* This function is called only by the C++ RuleMessage callback. It marks a
 * transaction-local failure for any mismatch, malformed value, or overflow. */
void msconnector_rule_match_observer_capture(
    msconnector_rule_match_observer *observer,
    const char *transaction_id,
    size_t transaction_id_length,
    int64_t rule_id,
    int libmodsecurity_phase);

void msconnector_rule_match_observer_fail(
    msconnector_rule_match_observer *observer);
int msconnector_rule_match_observer_failed(
    const msconnector_rule_match_observer *observer);

/* Returns one un-emitted match for the exact Common phase: 1 for a match,
 * 0 when none remain, and -1 after any observer failure. */
int msconnector_rule_match_observer_next(
    msconnector_rule_match_observer *observer,
    enum msconnector_phase phase,
    const char **rule_id);

#ifdef __cplusplus
}
#endif

#endif
