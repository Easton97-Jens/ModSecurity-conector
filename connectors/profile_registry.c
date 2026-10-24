#include "profile_registry.h"

#include <string.h>

static const msconnector_transaction_profile profiles[] = {
    {MSCONNECTOR_PROFILE_APACHE, "apache", "apache", "native-httpd-module",
        MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1},
    {MSCONNECTOR_PROFILE_NGINX, "nginx", "nginx", "native-nginx-http-module",
        MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1},
    {MSCONNECTOR_PROFILE_HAPROXY_HTX, "haproxy-htx", "haproxy", "htx-filter",
        MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1},
    {MSCONNECTOR_PROFILE_HAPROXY_SPOE_SPOP, "haproxy-spoe-spop", "haproxy",
        "spoe-spop-agent", MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 |
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P2,
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 |
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P4, 0, 1},
    {MSCONNECTOR_PROFILE_ENVOY_EXT_AUTHZ, "envoy-ext-authz", "envoy", "ext_authz",
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P2,
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P4, 0, 1},
    {MSCONNECTOR_PROFILE_ENVOY_EXT_PROC, "envoy-ext-proc", "envoy", "ext_proc",
        MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1},
    {MSCONNECTOR_PROFILE_TRAEFIK_FORWARDAUTH, "traefik-forwardauth", "traefik",
        "forwardAuth", MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P2,
        MSCONNECTOR_TRANSACTION_PHASE_MASK_P3 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P4, 0, 1},
    {MSCONNECTOR_PROFILE_TRAEFIK_NATIVE_UDS, "traefik-native-uds", "traefik",
        "native-traefik-middleware", MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1},
    {MSCONNECTOR_PROFILE_LIGHTTPD_STOCK, "lighttpd-stock", "lighttpd",
        "stock-lighttpd-sidecar", MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL,
        0U, 1, 1},
    {MSCONNECTOR_PROFILE_LIGHTTPD_PATCHED, "lighttpd-patched", "lighttpd",
        "patched-native-lighttpd", MSCONNECTOR_TRANSACTION_PHASE_MASK_ALL, 0U, 0, 1}
};

static const msconnector_transaction_profile stock_native_translation = {
    MSCONNECTOR_PROFILE_LIGHTTPD_STOCK,
    "lighttpd-stock-native-translation", "lighttpd", "stock-lighttpd",
    MSCONNECTOR_TRANSACTION_PHASE_MASK_P1 | MSCONNECTOR_TRANSACTION_PHASE_MASK_P3,
    0U, 0, 1
};

static int equal_text(const char *left, const char *right) {
    return left != NULL && right != NULL && strcmp(left, right) == 0;
}

const msconnector_transaction_profile *
msconnector_profile_registry_all(size_t *count) {
    if (count != NULL) {
        *count = sizeof(profiles) / sizeof(profiles[0]);
    }
    return profiles;
}

const msconnector_transaction_profile *
msconnector_profile_registry_find(const char *profile_name) {
    if (profile_name == NULL || profile_name[0] == '\0') {
        return NULL;
    }
    for (size_t index = 0U; index < sizeof(profiles) / sizeof(profiles[0]); ++index) {
        if (equal_text(profiles[index].profile_name, profile_name)) {
            return &profiles[index];
        }
    }
    return NULL;
}

const msconnector_transaction_profile *
msconnector_profile_registry_find_route(const char *connector_id,
    const char *host_adapter_id) {
    if (connector_id == NULL || connector_id[0] == '\0' ||
        host_adapter_id == NULL || host_adapter_id[0] == '\0') {
        return NULL;
    }
    for (size_t index = 0U; index < sizeof(profiles) / sizeof(profiles[0]); ++index) {
        if (equal_text(profiles[index].connector_id, connector_id) &&
            equal_text(profiles[index].host_adapter_id, host_adapter_id)) {
            return &profiles[index];
        }
    }
    if (equal_text(stock_native_translation.connector_id, connector_id) &&
        equal_text(stock_native_translation.host_adapter_id, host_adapter_id)) {
        return &stock_native_translation;
    }
    return NULL;
}
