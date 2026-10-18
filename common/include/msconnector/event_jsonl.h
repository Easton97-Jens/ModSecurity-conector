#ifndef MSCONNECTOR_EVENT_JSONL_H
#define MSCONNECTOR_EVENT_JSONL_H

#include "msconnector/event.h"
#include "msconnector/error.h"
#include <stddef.h>
#include <stdio.h>

#ifdef __cplusplus
extern "C" {
#endif

int msconnector_event_write_jsonl_line(const msconnector_event *event, char *dst, size_t dst_size, int *truncated);

/* Serialized, bounded metadata only. The owner holds its stream lock. A
 * supplied first error is sticky: writes never retry an already failed sink.
 * close always consumes the owned stream, including when an earlier error
 * must be retained. These helpers do not claim delivery or durability. */
int msconnector_event_file_write(FILE *file, const char *serialized,
    msconnector_error *error);
int msconnector_event_file_close(FILE **file, msconnector_error *error);
int msconnector_event_write_jsonl_stream(const msconnector_event *event,
    FILE *file, char *scratch, size_t scratch_size, msconnector_error *error);

/*
 * Open a metadata-event sink without following a symlink in any path
 * component.  On success, returns 1 and transfers an owned POSIX descriptor
 * through out_fd.  The final parent must be owned by the effective user or
 * root and be non-writable by group/other. The opened object is a regular
 * file owned by the effective user and restricted to mode 0600; otherwise it
 * returns 0, leaves out_fd at -1, and sets errno. Platforms without an
 * equivalent no-follow directory walk fail closed.
 */
int msconnector_open_private_event_file(const char *path, int *out_fd);

#ifdef __cplusplus
}
#endif

#endif
