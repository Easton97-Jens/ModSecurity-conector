#ifndef MSCONNECTOR_RUNTIME_H
#define MSCONNECTOR_RUNTIME_H

#include <stddef.h>

#include "msconnector/body_policy.h"
#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/request.h"
#include "msconnector/request_mapper_contract.h"
#include "msconnector/response.h"
#include "msconnector/response_mapper_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral, libmodsecurity-backed runtime used by external-service
 * and native-module adapters. Host API types deliberately do not cross this
 * boundary. The runtime owns its engine, rules and configuration strings;
 * request/response objects and body chunks are borrowed only for their
 * corresponding call. A transaction retains bounded metadata, never a host
 * request, response, or body pointer.
 */
typedef struct msconnector_runtime msconnector_runtime;
typedef struct msconnector_runtime_transaction msconnector_runtime_transaction;

/*
 * Body chunks are borrowed from the host.  The runtime never retains a chunk
 * pointer after append_*_body_chunk() returns.  Counters describe metadata
 * only and are safe to place in events or result records.
 */
typedef struct msconnector_runtime_body_progress {
    size_t bytes_seen;
    size_t bytes_inspected;
    int truncated;
    int finished;
    msconnector_body_limit_outcome limit_outcome;
} msconnector_runtime_body_progress;

int msconnector_runtime_config_check(
    const char *connector_name,
    const char *config_path,
    char *error,
    size_t error_len);

int msconnector_runtime_create(
    const char *connector_name,
    const char *config_path,
    msconnector_runtime **out,
    char *error,
    size_t error_len);

void msconnector_runtime_destroy(msconnector_runtime **runtime);

void msconnector_runtime_request_contract(
    const msconnector_runtime *runtime,
    msconnector_request_mapper_contract *contract);

void msconnector_runtime_response_contract(
    const msconnector_runtime *runtime,
    msconnector_response_mapper_contract *contract);

size_t msconnector_runtime_request_body_limit(const msconnector_runtime *runtime);
size_t msconnector_runtime_response_body_limit(const msconnector_runtime *runtime);
msconnector_body_mode msconnector_runtime_request_body_mode(
    const msconnector_runtime *runtime);
msconnector_body_mode msconnector_runtime_response_body_mode(
    const msconnector_runtime *runtime);
size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime);
size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime);

/* The parsed budget is in milliseconds. A zero value disables it. Common
 * stores this adapter-facing value but does not own a host timer or a
 * cancellation primitive, so callers must not treat the getter as proof that
 * their transport enforces a deadline. */
size_t msconnector_runtime_late_intervention_timeout_ms(
    const msconnector_runtime *runtime);

/*
 * Maps a concrete runtime error to the configured HTTP error policy while
 * preserving protocol-specific statuses such as body-limit and timeout
 * failures.
 */
int msconnector_runtime_error_http_status(
    const msconnector_runtime *runtime,
    msconnector_error_code code);

int msconnector_runtime_transaction_begin(
    msconnector_runtime *runtime,
    const msconnector_request *request,
    const char *host_request_id,
    msconnector_runtime_transaction **out,
    msconnector_decision *decision,
    msconnector_error *error);

/*
 * Explicit low-latency lifecycle operations.  Request/response headers are
 * processed once.  Body chunks are ingested incrementally and phase 2/4 is
 * finalized exactly once at end of stream.  libmodsecurity may evaluate body
 * rules during the finish call rather than on an individual chunk.
 */
int msconnector_runtime_transaction_append_request_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error);

int msconnector_runtime_transaction_finish_request_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_process_response_headers(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_append_response_body_chunk(
    msconnector_runtime_transaction *transaction,
    const unsigned char *data,
    size_t size,
    msconnector_error *error);

int msconnector_runtime_transaction_finish_response_body(
    msconnector_runtime_transaction *transaction,
    msconnector_decision *decision,
    msconnector_error *error);

/*
 * Hosts call this immediately before or after handing bytes to their next
 * filter.  It records only commit metadata; it cannot retroactively change a
 * response and does not retain any host buffer.
 */
void msconnector_runtime_transaction_set_response_commit_state(
    msconnector_runtime_transaction *transaction,
    int headers_sent,
    int body_started);

void msconnector_runtime_transaction_request_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress);

void msconnector_runtime_transaction_response_body_progress(
    const msconnector_runtime_transaction *transaction,
    msconnector_runtime_body_progress *progress);

/* Buffered compatibility helper. Prefer the explicit header/chunk/finish API
 * for full-lifecycle paths. */
int msconnector_runtime_transaction_process_response(
    msconnector_runtime_transaction *transaction,
    const msconnector_response *response,
    msconnector_decision *decision,
    msconnector_error *error);

int msconnector_runtime_transaction_finish(
    msconnector_runtime_transaction *transaction,
    msconnector_error *error);

const char *msconnector_runtime_transaction_id(
    const msconnector_runtime_transaction *transaction);

void msconnector_runtime_transaction_destroy(
    msconnector_runtime_transaction **transaction);

#ifdef __cplusplus
}
#endif

#endif
