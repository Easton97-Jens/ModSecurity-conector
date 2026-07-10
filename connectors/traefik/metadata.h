#ifndef MSCONNECTOR_TRAEFIK_METADATA_H
#define MSCONNECTOR_TRAEFIK_METADATA_H

#include "msconnector/adapter_metadata.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_adapter_metadata msconnector_traefik_adapter_metadata;

msconnector_origin msconnector_traefik_adapter_origin(void);
const msconnector_capabilities *msconnector_traefik_adapter_capabilities(void);
const msconnector_traefik_adapter_metadata *msconnector_traefik_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
