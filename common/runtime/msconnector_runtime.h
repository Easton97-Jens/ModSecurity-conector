#ifndef MSCONNECTOR_RUNTIME_H
#define MSCONNECTOR_RUNTIME_H

#include <stddef.h>

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
 * request and response objects remain borrowed for a transaction lifetime.
 */
typedef struct msconnector_runtime msconnector_runtime;
typedef struct msconnector_runtime_transaction msconnector_runtime_transaction;

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
size_t msconnector_runtime_total_header_limit(const msconnector_runtime *runtime);
size_t msconnector_runtime_header_count_limit(const msconnector_runtime *runtime);

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
