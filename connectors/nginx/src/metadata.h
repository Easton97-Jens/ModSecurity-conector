#ifndef MSCONNECTOR_NGINX_METADATA_H
#define MSCONNECTOR_NGINX_METADATA_H

#include "msconnector/origin.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_nginx_adapter_metadata {
    msconnector_origin origin;
    const char *source_kind;
    const char *imported_path;
} msconnector_nginx_adapter_metadata;

msconnector_origin msconnector_nginx_adapter_origin(void);
const msconnector_nginx_adapter_metadata *msconnector_nginx_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
