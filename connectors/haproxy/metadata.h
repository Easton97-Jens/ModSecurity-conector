#ifndef MSCONNECTOR_HAPROXY_METADATA_H
#define MSCONNECTOR_HAPROXY_METADATA_H

#include "msconnector/origin.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_haproxy_adapter_metadata {
    msconnector_origin origin;
    const char *source_kind;
    const char *imported_path;
    const char *build_status;
    const char *starter_status;
    const char *runtime_status;
} msconnector_haproxy_adapter_metadata;

msconnector_origin msconnector_haproxy_adapter_origin(void);
const msconnector_haproxy_adapter_metadata *msconnector_haproxy_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
