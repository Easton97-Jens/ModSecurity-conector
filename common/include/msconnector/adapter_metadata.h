#ifndef MSCONNECTOR_ADAPTER_METADATA_H
#define MSCONNECTOR_ADAPTER_METADATA_H
#include "msconnector/capabilities.h"
#include "msconnector/origin.h"
#ifdef __cplusplus
extern "C" {
#endif
/* Common metadata target contract for future migration; this PR does not migrate existing connectors. */
typedef struct msconnector_adapter_metadata { msconnector_origin origin; msconnector_capabilities capabilities; const char *connector_name; const char *server_family; const char *source_kind; const char *imported_path; const char *integration_path; const char *build_status; const char *runtime_status; const char *verification_status; } msconnector_adapter_metadata;
void msconnector_adapter_metadata_init(msconnector_adapter_metadata *metadata);
int msconnector_adapter_metadata_is_complete(const msconnector_adapter_metadata *metadata);
#ifdef __cplusplus
}
#endif
#endif
