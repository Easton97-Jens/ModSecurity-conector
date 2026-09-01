#ifndef MSCONNECTOR_TRAEFIK_FORWARDAUTH_RESPONSE_COMPANION_H
#define MSCONNECTOR_TRAEFIK_FORWARDAUTH_RESPONSE_COMPANION_H

#include <stddef.h>
#include <stdint.h>

#include "common/runtime/msconnector_runtime.h"
#include "common/runtime/response_companion_transport.h"

#ifdef __cplusplus
extern "C" {
#endif

#define MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET \
    "/run/modsecurity/traefik-forwardauth-companion.sock"
#define MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET_SIZE 108U
#define MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_TTL_MS 30000ULL

/* Host-specific configuration only. Correlation, state transitions, and
 * response processing live in the common opaque-handle MRC1 transport. */
typedef struct msconnector_traefik_forwardauth_response_companion {
    msconnector_runtime_response_companion_registry runtime_transactions;
    msconnector_response_companion_transport transport;
    int transport_initialized;
    int transport_ready;
    uint64_t ttl_ms;
    size_t max_header_count;
    size_t max_header_bytes;
    size_t max_response_body_bytes;
    char socket_path[MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET_SIZE];
} msconnector_traefik_forwardauth_response_companion;

int msconnector_traefik_forwardauth_response_companion_init(
    msconnector_traefik_forwardauth_response_companion *companion,
    const char *socket_path,
    uint64_t ttl_ms);
int msconnector_traefik_forwardauth_response_companion_set_limits(
    msconnector_traefik_forwardauth_response_companion *companion,
    size_t max_header_count,
    size_t max_header_bytes,
    size_t max_response_body_bytes);

#ifdef __cplusplus
}
#endif

#endif
