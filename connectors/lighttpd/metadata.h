#ifndef MSCONNECTOR_LIGHTTPD_METADATA_H
#define MSCONNECTOR_LIGHTTPD_METADATA_H

#include "msconnector/origin.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_lighttpd_adapter_metadata {
    msconnector_origin origin;
    const char *source_kind;
    const char *imported_path;
    const char *build_status;
    const char *runtime_status;
    const char *verification_status;
    const char *integration_path;
} msconnector_lighttpd_adapter_metadata;

msconnector_origin msconnector_lighttpd_adapter_origin(void);
const msconnector_lighttpd_adapter_metadata *msconnector_lighttpd_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
