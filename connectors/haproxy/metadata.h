#ifndef MSCONNECTOR_HAPROXY_METADATA_H
#define MSCONNECTOR_HAPROXY_METADATA_H

#include "msconnector/adapter_metadata.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_adapter_metadata msconnector_haproxy_adapter_metadata;

msconnector_origin msconnector_haproxy_adapter_origin(void);
const msconnector_capabilities *msconnector_haproxy_adapter_capabilities(void);
const msconnector_haproxy_adapter_metadata *msconnector_haproxy_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
