#ifndef MSCONNECTOR_TRAEFIK_METADATA_H
#define MSCONNECTOR_TRAEFIK_METADATA_H

#include "msconnector/capabilities.h"
#include "msconnector/origin.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_traefik_adapter_metadata {
    msconnector_origin origin;
    msconnector_capabilities capabilities;
    const char *source_kind;
    const char *imported_path;
    const char *build_status;
    const char *runtime_status;
} msconnector_traefik_adapter_metadata;

msconnector_origin msconnector_traefik_adapter_origin(void);
const msconnector_capabilities *msconnector_traefik_adapter_capabilities(void);
const msconnector_traefik_adapter_metadata *msconnector_traefik_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
