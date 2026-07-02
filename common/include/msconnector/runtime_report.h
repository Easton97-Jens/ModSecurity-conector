#ifndef MSCONNECTOR_RUNTIME_REPORT_H
#define MSCONNECTOR_RUNTIME_REPORT_H
#include "msconnector/status.h"
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct msconnector_runtime_report { const char *connector; const char *case_name; enum msconnector_status status; const char *capability; const char *artifact_result_json; const char *artifact_decision_jsonl; const char *reason; } msconnector_runtime_report;
void msconnector_runtime_report_init(msconnector_runtime_report *report);
int msconnector_runtime_report_write_json(const msconnector_runtime_report *report, char *dst, size_t dst_size, int *truncated);
#ifdef __cplusplus
}
#endif
#endif
