#include "msconnector/runtime_report.h"
#include "msconnector/json_escape.h"
#include <stdio.h>
#include <string.h>
#define F 160U
static void esc(const char *s, char *d, size_t n, int *t) { size_t need = msconnector_json_escape(s,d,n); if ((n == 0U || need >= n) && t != 0) { *t = 1; } }
void msconnector_runtime_report_init(msconnector_runtime_report *report) { if (report != 0) { memset(report, 0, sizeof(*report)); report->status = MSCONNECTOR_STATUS_UNSUPPORTED; } }
int msconnector_runtime_report_write_json(const msconnector_runtime_report *r, char *dst, size_t size, int *truncated) {
    char connector[F], case_name[F], capability[F], result[F], decision[F], reason[F]; int was = 0; int written;
    if (truncated != 0) { *truncated = 0; } if (dst != 0 && size > 0U) { dst[0] = '\0'; }
    if (r == 0 || dst == 0 || size == 0U) { return 0; }
    esc(r->connector,connector,F,&was); esc(r->case_name,case_name,F,&was); esc(r->capability,capability,F,&was); esc(r->artifact_result_json,result,F,&was); esc(r->artifact_decision_jsonl,decision,F,&was); esc(r->reason,reason,F,&was);
    written = snprintf(dst,size,"{\"connector\":\"%s\",\"case\":\"%s\",\"status\":\"%s\",\"capability\":\"%s\",\"artifact_result_json\":\"%s\",\"artifact_decision_jsonl\":\"%s\",\"reason\":\"%s\"}",connector,case_name,msconnector_status_name(r->status),capability,result,decision,reason);
    if (written < 0 || (size_t)written >= size) { was = 1; } if (truncated != 0) { *truncated = was; } return !was;
}
