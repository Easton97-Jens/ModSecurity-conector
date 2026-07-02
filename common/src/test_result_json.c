#include "msconnector/test_result_json.h"
#include "msconnector/json_escape.h"
#include <stdio.h>
#define FIELD 256U
static void esc(const char *src, char *dst, size_t size, int *truncated) { size_t need = msconnector_json_escape(src, dst, size); if ((size == 0U || need >= size) && truncated != 0) { *truncated = 1; } }
int msconnector_test_result_write_json(const msconnector_test_result *result, char *dst, size_t dst_size, int *truncated) {
    char connector[FIELD], case_name[FIELD], status[64], reason[FIELD]; int was = 0; int written;
    if (truncated != 0) { *truncated = 0; } if (dst != 0 && dst_size > 0U) { dst[0] = '\0'; }
    if (result == 0 || dst == 0 || dst_size == 0U) { return 0; }
    esc(result->connector, connector, sizeof(connector), &was); esc(result->case_name, case_name, sizeof(case_name), &was); esc(msconnector_status_name(result->status), status, sizeof(status), &was); esc(result->reason, reason, sizeof(reason), &was);
    written = snprintf(dst, dst_size, "{\"connector\":\"%s\",\"case\":\"%s\",\"status\":\"%s\",\"expected_http_status\":%d,\"actual_http_status\":%d,\"reason\":\"%s\"}", connector, case_name, status, result->expected_http_status, result->actual_http_status, reason);
    if (written < 0 || (size_t)written >= dst_size) { was = 1; }
    if (truncated != 0) { *truncated = was; }
    return !was;
}
