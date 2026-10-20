#include "traefik_modsecurity_mapper.h"
#include "traefik_forwardauth_response_companion.h"
#include "traefik_provenance.h"

#include "common/runtime/http_authorization_service.h"
#include "connectors/profile_registry.h"

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

static const char *const traefik_original_uri_headers[] = {
    "X-Forwarded-Uri",
    "X-Original-Uri"
};

static msconnector_traefik_forwardauth_response_companion traefik_response_companion;
static int traefik_response_companion_ready;

static const char *traefik_response_companion_socket_path(void)
{
    const char *configured = getenv(
        "MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET");

    return configured == NULL || configured[0] == '\0' ? NULL : configured;
}

static int traefik_handoff_response_companion(
    const msconnector_runtime *runtime,
    msconnector_runtime_transaction *transaction,
    void *userdata,
    char response_handle[MSCONNECTOR_RUNTIME_RESPONSE_COMPANION_HANDLE_SIZE],
    msconnector_error *error)
{
    msconnector_traefik_forwardauth_response_companion *companion = userdata;
    const size_t configured_timeout =
        msconnector_runtime_late_intervention_timeout_ms(runtime);

    if (runtime == NULL || companion == NULL) {
        return 0;
    }
    if (!traefik_response_companion_ready) {
        if (!msconnector_traefik_forwardauth_response_companion_init(companion,
                traefik_response_companion_socket_path(),
                MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_TTL_MS)) {
            return 0;
        }
        if (!msconnector_traefik_forwardauth_response_companion_set_limits(companion,
                msconnector_runtime_header_count_limit(runtime),
                msconnector_runtime_total_header_limit(runtime))) {
            return 0;
        }
        traefik_response_companion_ready = 1;
    }
    if (!msconnector_response_companion_transport_ensure_started(
            &companion->transport, &companion->runtime_transactions,
            &companion->transport_initialized, &companion->transport_ready,
            &(msconnector_response_companion_transport_options){
                "traefik", companion->socket_path, companion->max_header_count,
                companion->max_header_bytes,
                configured_timeout == 0U ?
                MSCONNECTOR_RESPONSE_COMPANION_TRANSPORT_DEFAULT_TIMEOUT_MS :
                configured_timeout}, error)) {
        return 0;
    }
    return msconnector_runtime_response_companion_handoff_with_handle(
        &companion->runtime_transactions, transaction, companion->ttl_ms,
        response_handle, error);
}

static int traefik_shutdown_response_companion(void *userdata,
    msconnector_error *error)
{
    msconnector_traefik_forwardauth_response_companion *companion = userdata;

    if (companion == NULL || !traefik_response_companion_ready) {
        return 1;
    }
    if (companion->transport_ready &&
        !msconnector_response_companion_transport_stop(&companion->transport, error)) {
        return 0;
    }
    return msconnector_runtime_response_companion_registry_shutdown(
        &companion->runtime_transactions, error);
}

static int traefik_revoke_response_companion(void *userdata,
    const char *response_handle, msconnector_error *error)
{
    msconnector_traefik_forwardauth_response_companion *companion = userdata;
    return companion != NULL && msconnector_runtime_response_companion_revoke_handle(
        &companion->runtime_transactions, response_handle, error);
}

static int traefik_confirm_response_companion(void *userdata,
    const char *response_handle, msconnector_error *error)
{
    msconnector_traefik_forwardauth_response_companion *companion = userdata;
    return companion != NULL && traefik_response_companion_ready &&
        msconnector_runtime_response_companion_confirm_preclaim(
            &companion->runtime_transactions, response_handle, error);
}

static const msconnector_http_authorization_profile traefik_forwardauth_profile = {
    "traefik",
    "forwardAuth",
    NULL,
    traefik_original_uri_headers,
    sizeof(traefik_original_uri_headers) / sizeof(traefik_original_uri_headers[0]),
    traefik_modsecurity_map_request,
    traefik_modsecurity_map_response,
    traefik_handoff_response_companion,
    &traefik_response_companion,
    traefik_revoke_response_companion,
    traefik_shutdown_response_companion,
    NULL,
    NULL
};

int main(int argc, char **argv)
{
    msconnector_http_authorization_profile profile = traefik_forwardauth_profile;
    const char *provenance_socket = getenv("MSCONNECTOR_TRAEFIK_PROVENANCE_SOCKET");
    int serving = 0;
    int result;
    static const msconnector_http_authorization_trusted_binding binding = {
        msconnector_traefik_provenance_claim, NULL,
        MSCONNECTOR_TRAEFIK_PROVENANCE_HEADER,
        msconnector_traefik_provenance_complete
    };

    profile.transaction_profile = msconnector_profile_registry_find(
        "traefik-forwardauth");
    for (int i = 1; i < argc; ++i)
        if (strcmp(argv[i], "--serve") == 0) serving = 1;
    if (provenance_socket == NULL || provenance_socket[0] == '\0' || !serving)
        return msconnector_http_authorization_service_main(argc, argv, &profile);
    if (!msconnector_traefik_provenance_start_with_confirmation(provenance_socket,
            traefik_confirm_response_companion, &traefik_response_companion)) {
        fprintf(stderr, "traefik trusted provenance listener initialization failed\n");
        return 1;
    }
    result = msconnector_http_authorization_service_main_with_trusted_binding(
        argc, argv, &profile, &binding);
    msconnector_traefik_provenance_stop();
    return result;
}
