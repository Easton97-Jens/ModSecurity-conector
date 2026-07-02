#ifndef MSCONNECTOR_CONNECTOR_MANIFEST_H
#define MSCONNECTOR_CONNECTOR_MANIFEST_H
#include "msconnector/adapter_metadata.h"
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct msconnector_connector_manifest { const char *connector; const char *server_family; const char *source_kind; const char *build_status; const char *runtime_status; const char *verification_status; msconnector_capability_flags capabilities; } msconnector_connector_manifest;
void msconnector_connector_manifest_init(msconnector_connector_manifest *manifest);
int msconnector_connector_manifest_from_metadata(msconnector_connector_manifest *out, const msconnector_adapter_metadata *metadata);
int msconnector_connector_manifest_write_json(const msconnector_connector_manifest *manifest, char *dst, size_t dst_size, int *truncated);
#ifdef __cplusplus
}
#endif
#endif
