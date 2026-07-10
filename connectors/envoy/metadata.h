#ifndef MSCONNECTOR_ENVOY_METADATA_H
#define MSCONNECTOR_ENVOY_METADATA_H

#include "msconnector/adapter_metadata.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_adapter_metadata msconnector_envoy_adapter_metadata;

msconnector_origin msconnector_envoy_adapter_origin(void);
const msconnector_envoy_adapter_metadata *msconnector_envoy_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
