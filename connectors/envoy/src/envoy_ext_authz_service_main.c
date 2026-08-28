#include "envoy_modsecurity_mapper.h"
#include "envoy_ext_authz_response_companion.h"

#include "common/runtime/http_authorization_service.h"
#include "common/runtime/msconnector_runtime.h"
#include "connectors/profile_registry.h"

#include <stdlib.h>

static const char *const envoy_original_uri_headers[] = {
    "x-envoy-original-path",
    "x-forwarded-uri",
    "x-original-uri"
};

static msconnector_envoy_ext_authz_response_companion envoy_response_companion;
static int envoy_response_companion_ready;

/* The default remains the deployment-private /run binding.  The explicit
 * override exists for an isolated, owner-only runtime root (for example the
 * local harness); the companion initializer and Common transport reject an
 * unsafe path or parent instead of falling back to a public socket. */
static const char *envoy_response_companion_socket(void)
{
    const char *configured = getenv("MSCONNECTOR_ENVOY_EXT_AUTHZ_COMPANION_SOCKET");
    return configured != NULL && configured[0] != '\0' ? configured : NULL;
}

static int envoy_handoff_response_companion(
    const msconnector_runtime *runtime,
    msconnector_runtime_transaction *transaction,
    void *userdata,
    char response_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error)
{
    msconnector_envoy_ext_authz_response_companion *companion = userdata;
    const size_t configured_timeout =
        msconnector_runtime_late_intervention_timeout_ms(runtime);

    if (runtime == NULL || companion == NULL) {
        return 0;
    }
    if (!envoy_response_companion_ready) {
        if (!msconnector_envoy_ext_authz_response_companion_init(companion,
                envoy_response_companion_socket(),
                MSCONNECTOR_ENVOY_EXT_AUTHZ_COMPANION_TTL_MS)) {
            return 0;
        }
        if (!msconnector_envoy_ext_authz_response_companion_set_limits(companion,
                msconnector_runtime_header_count_limit(runtime),
                msconnector_runtime_total_header_limit(runtime),
                msconnector_runtime_response_body_limit(runtime))) {
            return 0;
        }
        envoy_response_companion_ready = 1;
    }
    if (!companion->transport_initialized) {
        if (!msconnector_response_companion_transport_init(&companion->transport,
                &companion->runtime_transactions,
                &(msconnector_response_companion_transport_options){
                    "envoy", companion->socket_path, companion->max_header_count,
                    companion->max_header_bytes, companion->max_response_body_bytes,
                    configured_timeout == 0U ?
                    MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_DEFAULT_TIMEOUT_MS :
                    configured_timeout}, error)) {
            return 0;
        }
        companion->transport_initialized = 1;
    }
    if (!companion->transport_ready) {
        if (!msconnector_response_companion_transport_start(&companion->transport,
                error)) {
            return 0;
        }
        companion->transport_ready = 1;
    }
    return msconnector_runtime_response_companion_handoff_with_handle(
        &companion->runtime_transactions, transaction, companion->ttl_ms,
        response_handle, error);
}

static int envoy_shutdown_response_companion(void *userdata,
    msconnector_error *error)
{
    msconnector_envoy_ext_authz_response_companion *companion = userdata;

    if (companion == NULL || !envoy_response_companion_ready) {
        return 1;
    }
    if (companion->transport_ready &&
        !msconnector_response_companion_transport_stop(&companion->transport, error)) {
        return 0;
    }
    return msconnector_runtime_response_companion_registry_shutdown(
        &companion->runtime_transactions, error);
}

static int envoy_revoke_response_companion(void *userdata,
    const char *response_handle, msconnector_error *error)
{
    msconnector_envoy_ext_authz_response_companion *companion = userdata;
    return companion != NULL && msconnector_runtime_response_companion_revoke_handle(
        &companion->runtime_transactions, response_handle, error);
}

static const msconnector_http_authorization_profile envoy_ext_authz_profile = {
    "envoy",
    "ext_authz",
    NULL,
    envoy_original_uri_headers,
    sizeof(envoy_original_uri_headers) / sizeof(envoy_original_uri_headers[0]),
    envoy_modsecurity_map_request,
    envoy_modsecurity_map_response,
    envoy_handoff_response_companion,
    &envoy_response_companion,
    envoy_revoke_response_companion,
    envoy_shutdown_response_companion,
    "x-msconnector-terminal-authz",
    "1"
};

int main(int argc, char **argv)
{
    msconnector_http_authorization_profile profile = envoy_ext_authz_profile;

    profile.transaction_profile = msconnector_profile_registry_find(
        "envoy-ext-authz");
    return msconnector_http_authorization_service_main(
        argc,
        argv,
        &profile);
}
