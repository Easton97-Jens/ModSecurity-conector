#include "msconnector/event_jsonl.h"
#include <string.h>

int msconnector_event_write_jsonl_line(const msconnector_event *event, char *dst, size_t dst_size, int *truncated) {
    int local_truncated = 0;
    int ok;
    size_t len;
    if (truncated != 0) { *truncated = 0; }
    if (dst != 0 && dst_size > 0) { dst[0] = '\0'; }
    if (dst == 0 || dst_size == 0) { if (truncated != 0) { *truncated = 1; } return 0; }
    ok = msconnector_event_write_json_ex(event, dst, dst_size, &local_truncated);
    len = strlen(dst);
    if (len + 1U >= dst_size) { if (truncated != 0) { *truncated = 1; } return 0; }
    dst[len] = '\n'; dst[len + 1U] = '\0';
    if (truncated != 0) { *truncated = local_truncated; }
    return ok && !local_truncated;
}
