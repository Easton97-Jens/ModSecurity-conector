#ifndef MSCONNECTOR_ORIGIN_GOVERNANCE_H
#define MSCONNECTOR_ORIGIN_GOVERNANCE_H
#include "msconnector/adapter_metadata.h"
#ifdef __cplusplus
extern "C" {
#endif
typedef struct msconnector_origin_governance { const char *source_repository; const char *source_branch; const char *source_commit; const char *source_describe; const char *license; const char *imported_path; const char *source_kind; const char *upstream_base; const char *local_modifications; const char *patches_applied; } msconnector_origin_governance;
void msconnector_origin_governance_init(msconnector_origin_governance *governance);
int msconnector_origin_governance_is_complete(const msconnector_origin_governance *governance);
int msconnector_origin_governance_from_metadata(msconnector_origin_governance *out, const msconnector_adapter_metadata *metadata);
#ifdef __cplusplus
}
#endif
#endif
