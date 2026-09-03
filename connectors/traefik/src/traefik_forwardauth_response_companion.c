#include "traefik_forwardauth_response_companion.h"
#include "connectors/profile_registry.h"

#include <stdio.h>
#include <string.h>

static int safe_socket_path(const char *path)
{
    size_t length;
    if (path == NULL || path[0] != '/') {
        return 0;
    }
    length = strlen(path);
    for (const char *cursor = path; *cursor != '\0'; ++cursor) {
        if (*cursor == '\n' || *cursor == '\r') {
            return 0;
        }
    }
    return length > 0U && length < MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET_SIZE &&
        strstr(path, "/../") == NULL &&
        (length < 3U || strcmp(path + length - 3U, "/..") != 0);
}

static const msconnector_transaction_profile *profile(void)
{
    return msconnector_profile_registry_find("traefik-forwardauth");
}

int msconnector_traefik_forwardauth_response_companion_init(
    msconnector_traefik_forwardauth_response_companion *companion,
    const char *socket_path,
    uint64_t ttl_ms)
{
    const char *selected = socket_path == NULL || socket_path[0] == '\0' ?
        MSCONNECTOR_TRAEFIK_FORWARDAUTH_COMPANION_SOCKET : socket_path;
    if (companion == NULL || ttl_ms == 0U || !safe_socket_path(selected) ||
        profile() == NULL) {
        return 0;
    }
    memset(companion, 0, sizeof(*companion));
    msconnector_runtime_response_companion_registry_init(
        &companion->runtime_transactions);
    (void)snprintf(companion->socket_path, sizeof(companion->socket_path), "%s", selected);
    companion->ttl_ms = ttl_ms;
    companion->max_header_count = MSCONNECTOR_MAX_HEADER_COUNT;
    companion->max_header_bytes = MSCONNECTOR_MAX_TOTAL_HEADER_BYTES;
    companion->max_response_body_bytes = MSCONNECTOR_MAX_RESPONSE_BODY_BUFFER_SIZE;
    return 1;
}

int msconnector_traefik_forwardauth_response_companion_set_limits(
    msconnector_traefik_forwardauth_response_companion *companion,
    size_t max_header_count,
    size_t max_header_bytes,
    size_t max_response_body_bytes)
{
    if (companion == NULL || max_header_count == 0U ||
        max_header_bytes == 0U || max_response_body_bytes == 0U) {
        return 0;
    }
    companion->max_header_count = max_header_count;
    companion->max_header_bytes = max_header_bytes;
    companion->max_response_body_bytes = max_response_body_bytes;
    return 1;
}
