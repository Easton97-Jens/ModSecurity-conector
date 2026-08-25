#ifndef MSCONNECTOR_EVENT_JSONL_H
#define MSCONNECTOR_EVENT_JSONL_H

#include "msconnector/event.h"
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int msconnector_event_write_jsonl_line(const msconnector_event *event, char *dst, size_t dst_size, int *truncated);

/*
 * Open a metadata-event sink without following a symlink in any path
 * component.  On success, returns 1 and transfers an owned POSIX descriptor
 * through out_fd.  The opened object is a regular file owned by the effective
 * user and restricted to mode 0600; otherwise it returns 0, leaves out_fd at
 * -1, and sets errno.  Platforms without an equivalent no-follow directory
 * walk fail closed.
 */
int msconnector_open_private_event_file(const char *path, int *out_fd);

#ifdef __cplusplus
}
#endif

#endif
