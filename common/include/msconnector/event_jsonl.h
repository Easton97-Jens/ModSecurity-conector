#ifndef MSCONNECTOR_EVENT_JSONL_H
#define MSCONNECTOR_EVENT_JSONL_H

#include "msconnector/event.h"
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int msconnector_event_write_jsonl_line(const msconnector_event *event, char *dst, size_t dst_size, int *truncated);

#ifdef __cplusplus
}
#endif

#endif
