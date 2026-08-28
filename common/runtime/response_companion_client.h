#ifndef MSCONNECTOR_RESPONSE_COMPANION_CLIENT_H
#define MSCONNECTOR_RESPONSE_COMPANION_CLIENT_H

#include <stddef.h>
#include <stdint.h>
#include <sys/types.h>

#include "msconnector/decision.h"
#include "msconnector/error.h"
#include "msconnector/response.h"
#include "response_companion_transport.h"

#ifdef __cplusplus
extern "C" {
#endif

/* Synchronous MRC1 client for a private response companion.  The client
 * borrows all response and body input; it never retains or logs payloads. */
typedef struct msconnector_response_companion_result {
    int success;
    msconnector_decision_kind decision;
    uint16_t status;
    msconnector_error_code error_code;
    char *redirect_url;
    char *rule_id;
} msconnector_response_companion_result;

typedef struct msconnector_response_companion_client {
    int socket_fd;
    uint64_t timeout_ms;
    uid_t expected_uid;
    gid_t expected_gid;
    int opened;
    int claimed;
    int response_headers;
    int committed;
    int body_started;
    int response_eos;
    int outcome_recorded;
    int closed;
} msconnector_response_companion_client;

void msconnector_response_companion_result_destroy(
    msconnector_response_companion_result *result);

/* `client` must be zero-initialized before its first open. A live client must
 * be closed before it can be opened again; terminal CANCEL/RELEASE resets
 * only the transaction so the same trusted stream can claim a new handle. */
int msconnector_response_companion_client_open(
    msconnector_response_companion_client *client,
    const char *socket_path, uint64_t timeout_ms, uid_t expected_uid,
    gid_t expected_gid, msconnector_error *error);

int msconnector_response_companion_client_claim(
    msconnector_response_companion_client *client, const char *handle,
    msconnector_response_companion_result *result, msconnector_error *error);
int msconnector_response_companion_client_response_headers(
    msconnector_response_companion_client *client,
    const msconnector_response *response,
    msconnector_response_companion_result *result, msconnector_error *error);
int msconnector_response_companion_client_commit(
    msconnector_response_companion_client *client, int headers_sent,
    int body_started, msconnector_response_companion_result *result,
    msconnector_error *error);
int msconnector_response_companion_client_body_chunk(
    msconnector_response_companion_client *client, const unsigned char *data,
    size_t size, msconnector_response_companion_result *result,
    msconnector_error *error);
int msconnector_response_companion_client_body_eos(
    msconnector_response_companion_client *client,
    msconnector_response_companion_result *result, msconnector_error *error);
int msconnector_response_companion_client_outcome(
    msconnector_response_companion_client *client,
    msconnector_decision_action action, int visible_status,
    int connection_aborted, msconnector_response_companion_result *result,
    msconnector_error *error);
int msconnector_response_companion_client_cancel(
    msconnector_response_companion_client *client, int upstream_disconnect,
    msconnector_response_companion_result *result, msconnector_error *error);
/* Sends a typed terminal cause introduced by MRC1 protocol version 2.  It
 * performs deterministic release just like CANCEL; no fallback to a Boolean
 * cause is attempted when a peer does not support the selected protocol. */
int msconnector_response_companion_client_cancel_with_cause(
    msconnector_response_companion_client *client,
    msconnector_response_companion_cancel_cause cause,
    msconnector_response_companion_result *result, msconnector_error *error);
int msconnector_response_companion_client_release(
    msconnector_response_companion_client *client,
    msconnector_response_companion_result *result, msconnector_error *error);

/* Best-effort CANCEL (when still claimed), followed by fd close. */
int msconnector_response_companion_client_close(
    msconnector_response_companion_client *client, msconnector_error *error);

#ifdef __cplusplus
}
#endif

#endif
