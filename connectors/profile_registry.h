#ifndef MSCONNECTOR_PROFILE_REGISTRY_H
#define MSCONNECTOR_PROFILE_REGISTRY_H

#include <stddef.h>

#include "msconnector/transaction_contract.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum msconnector_profile_id {
    MSCONNECTOR_PROFILE_UNKNOWN = 0,
    MSCONNECTOR_PROFILE_APACHE,
    MSCONNECTOR_PROFILE_NGINX,
    MSCONNECTOR_PROFILE_HAPROXY_HTX,
    MSCONNECTOR_PROFILE_HAPROXY_SPOE_SPOP,
    MSCONNECTOR_PROFILE_ENVOY_EXT_AUTHZ,
    MSCONNECTOR_PROFILE_ENVOY_EXT_PROC,
    MSCONNECTOR_PROFILE_TRAEFIK_FORWARDAUTH,
    MSCONNECTOR_PROFILE_TRAEFIK_NATIVE_UDS,
    MSCONNECTOR_PROFILE_LIGHTTPD_STOCK,
    MSCONNECTOR_PROFILE_LIGHTTPD_PATCHED
} msconnector_profile_id;

const msconnector_transaction_profile *
msconnector_profile_registry_all(size_t *count);
const msconnector_transaction_profile *
msconnector_profile_registry_find(const char *profile_name);
const msconnector_transaction_profile *
msconnector_profile_registry_find_route(const char *connector_id,
    const char *host_adapter_id);

#ifdef __cplusplus
}
#endif

#endif
