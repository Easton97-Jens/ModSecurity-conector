#include "msconnector/runtime_report.h"
#include "msconnector/json_escape.h"
#include <stdio.h>
#include <string.h>

#define FIELD_SIZE 160U

static void escape_report_field(const char *src, char *dst, size_t dst_size, int *truncated)
{
    const size_t needed = msconnector_json_escape(src, dst, dst_size);

    if (truncated != 0 && (dst_size == 0U || needed >= dst_size)) {
        *truncated = 1;
    }
}

void msconnector_runtime_report_init(msconnector_runtime_report *report)
{
    if (report != 0) {
        memset(report, 0, sizeof(*report));
        report->status = MSCONNECTOR_STATUS_UNSUPPORTED;
    }
}

int msconnector_runtime_report_write_json(
    const msconnector_runtime_report *report,
    char *dst,
    size_t dst_size,
    int *truncated)
{
    char connector[FIELD_SIZE];
    char case_name[FIELD_SIZE];
    char capability[FIELD_SIZE];
    char result[FIELD_SIZE];
    char decision[FIELD_SIZE];
    char reason[FIELD_SIZE];
    int was_truncated = 0;
    int written;

    if (truncated != 0) {
        *truncated = 0;
    }
    if (dst != 0 && dst_size > 0U) {
        dst[0] = '\0';
    }
    if (report == 0 || dst == 0 || dst_size == 0U) {
        return 0;
    }

    escape_report_field(report->connector, connector, FIELD_SIZE, &was_truncated);
    escape_report_field(report->case_name, case_name, FIELD_SIZE, &was_truncated);
    escape_report_field(report->capability, capability, FIELD_SIZE, &was_truncated);
    escape_report_field(report->artifact_result_json, result, FIELD_SIZE, &was_truncated);
    escape_report_field(report->artifact_decision_jsonl, decision, FIELD_SIZE, &was_truncated);
    escape_report_field(report->reason, reason, FIELD_SIZE, &was_truncated);

    written = snprintf(
        dst,
        dst_size,
        "{\"connector\":\"%s\",\"case\":\"%s\",\"status\":\"%s\",\"capability\":\"%s\",\"artifact_result_json\":\"%s\",\"artifact_decision_jsonl\":\"%s\",\"reason\":\"%s\"}",
        connector,
        case_name,
        msconnector_status_name(report->status),
        capability,
        result,
        decision,
        reason);
    if (written < 0 || (size_t)written >= dst_size) {
        was_truncated = 1;
    }
    if (truncated != 0) {
        *truncated = was_truncated;
    }
    return was_truncated ? 0 : 1;
}
