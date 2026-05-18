#ifndef MSCONNECTOR_APACHE_METADATA_H
#define MSCONNECTOR_APACHE_METADATA_H

#include "msconnector/origin.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct msconnector_apache_adapter_metadata {
    msconnector_origin origin;
    const char *source_kind;
    const char *imported_path;
} msconnector_apache_adapter_metadata;

msconnector_origin msconnector_apache_adapter_origin(void);
const msconnector_apache_adapter_metadata *msconnector_apache_adapter_metadata_get(void);

#ifdef __cplusplus
}
#endif

#endif
