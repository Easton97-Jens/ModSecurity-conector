#ifndef MSCONNECTOR_HTTP_AUTHORIZATION_SERVICE_H
#define MSCONNECTOR_HTTP_AUTHORIZATION_SERVICE_H

#include <stddef.h>

#include "msconnector/generic_mapper.h"
#include "msconnector_runtime.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef int (*msconnector_runtime_request_mapper)(
    const msconnector_generic_request_source *source,
    const msconnector_request_mapper_contract *contract,
    msconnector_request *request,
    char *error,
    size_t error_len);

typedef int (*msconnector_runtime_response_mapper)(
    const msconnector_generic_response_source *source,
    const msconnector_response_mapper_contract *contract,
    msconnector_response *response,
    char *error,
    size_t error_len);

/* A request-only protocol transfers ownership of its live transaction to this
 * callback only when the authorization decision permits an upstream response.
 * The callback owns the bounded companion registry or private transport and
 * must finish/destroy the transaction at P4 EOS, cancellation, or TTL expiry.
 * It must be configured together with shutdown_response_companion.
 */
typedef int (*msconnector_runtime_response_companion_handoff_callback)(
    const msconnector_runtime *runtime,
    msconnector_runtime_transaction *transaction,
    void *userdata,
    char response_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error);

/* Called only after request workers and the external response observer have
 * quiesced. It drains retained live transactions before the Common runtime
 * can be destroyed; failure is fail-fast rather than a use-after-free. */
typedef int (*msconnector_runtime_response_companion_shutdown_callback)(
    void *userdata,
    msconnector_error *error);

typedef int (*msconnector_runtime_response_companion_revoke_callback)(
    void *userdata,
    const char *response_handle,
    msconnector_error *error);

typedef struct msconnector_http_authorization_profile {
    const char *connector_name;
    const char *integration_mode;
    /* Immutable, adapter-selected transaction route. The generic service
     * never resolves a connector name into a profile: an omitted or invalid
     * route is rejected before a request can begin. */
    const msconnector_transaction_profile *transaction_profile;
    const char *const *original_uri_headers;
    size_t original_uri_header_count;
    msconnector_runtime_request_mapper map_request;
    msconnector_runtime_response_mapper map_response;
    msconnector_runtime_response_companion_handoff_callback handoff_response_companion;
    void *response_companion_userdata;
    msconnector_runtime_response_companion_revoke_callback revoke_response_companion;
    msconnector_runtime_response_companion_shutdown_callback shutdown_response_companion;
    /* Optional, profile-owned attestation for a terminal authorization reply
     * that must traverse a following response observer without a P3/P4
     * companion.  Both fields are either NULL or fixed valid HTTP header
     * values; they are never copied from an authorization request. */
    const char *terminal_response_marker_header;
    const char *terminal_response_marker_value;
} msconnector_http_authorization_profile;

/*
 * Supported CLI:
 *   --check-config --config PATH
 *   --serve --config PATH --listen HOST:PORT
 *
 * The service is intentionally request-phase only. A profile whose native
 * protocol has no response stream may install `handoff_response_companion`;
 * it transfers P1/P2 to a bounded, response-capable companion rather than
 * treating P3/P4 as not applicable.
 */
int msconnector_http_authorization_service_main(
    int argc,
    char **argv,
    const msconnector_http_authorization_profile *profile);

#ifdef __cplusplus
}
#endif

#endif
