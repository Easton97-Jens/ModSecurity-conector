#if !defined(_WIN32) && !defined(_POSIX_C_SOURCE)
#define _POSIX_C_SOURCE 200809L
#endif

#include "msconnector/event_jsonl.h"

#include <errno.h>
#include <string.h>

#if !defined(_WIN32)
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#endif

#define MSCONNECTOR_EVENT_SINK_PATH_SIZE 4096U

#if defined(O_NOFOLLOW) && defined(O_DIRECTORY) && !defined(_WIN32)
static int open_event_parent(const char *path, char *path_copy, int *out_directory_fd,
    const char **out_component) {
    const char *cursor;
    const char *separator;
    const char *component;
    int directory_fd;
    size_t path_length;
    if (path == NULL || path[0] == '\0') { errno = EINVAL; return 0; }
    path_length = strlen(path);
    if (path_length >= MSCONNECTOR_EVENT_SINK_PATH_SIZE ||
        path[path_length - 1U] == '/') { errno = EINVAL; return 0; }
    (void)memcpy(path_copy, path, path_length + 1U);
    directory_fd = open(path[0] == '/' ? "/" : ".",
        O_RDONLY | O_DIRECTORY | O_NOFOLLOW
#if defined(O_CLOEXEC)
        | O_CLOEXEC
#endif
        );
    if (directory_fd < 0) { return 0; }
    cursor = path_copy + (path[0] == '/' ? 1 : 0);
    component = cursor;
    for (;;) {
        int next;
        separator = strchr(cursor, '/');
        if (separator != NULL) { path_copy[separator - path_copy] = '\0'; }
        if (component[0] == '\0' || strcmp(component, ".") == 0 ||
            strcmp(component, "..") == 0) {
            (void)close(directory_fd); errno = EINVAL; return 0;
        }
        if (separator == NULL) { *out_directory_fd = directory_fd; *out_component = component; return 1; }
        next = openat(directory_fd, component, O_RDONLY | O_DIRECTORY | O_NOFOLLOW
#if defined(O_CLOEXEC)
            | O_CLOEXEC
#endif
            );
        if (next < 0) { int saved = errno; (void)close(directory_fd); errno = saved; return 0; }
        (void)close(directory_fd); directory_fd = next;
        cursor = separator + 1; component = cursor;
    }
}

static int validate_event_file(int fd) {
    struct stat file_status;
    if (fstat(fd, &file_status) != 0) { return 0; }
    if (!S_ISREG(file_status.st_mode)) { errno = EINVAL; return 0; }
    if (file_status.st_uid != geteuid()) { errno = EACCES; return 0; }
    if (fchmod(fd, (mode_t)0600) != 0) { return 0; }
    return 1;
}
#endif

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

int msconnector_open_private_event_file(const char *path, int *out_fd) {
    if (out_fd == NULL) {
        errno = EINVAL;
        return 0;
    }
    *out_fd = -1;

#if defined(_WIN32)
    (void)path;
#if defined(ENOTSUP)
    errno = ENOTSUP;
#else
    errno = EACCES;
#endif
    return 0;
#elif !defined(O_NOFOLLOW) || !defined(O_DIRECTORY)
    (void)path;
#if defined(ENOTSUP)
    errno = ENOTSUP;
#else
    errno = EACCES;
#endif
    return 0;
#else
    int directory_fd = -1;
    int fd = -1;
    int flags = O_WRONLY | O_APPEND | O_CREAT | O_NONBLOCK | O_NOFOLLOW;
    char path_copy[MSCONNECTOR_EVENT_SINK_PATH_SIZE];
    const char *component;
    struct stat directory_status;

#if defined(O_CLOEXEC)
    flags |= O_CLOEXEC;
#endif

    /* The parent walker performs the no-follow checks (next_directory_fd,
     * strcmp(component, ".") == 0, strcmp(component, "..") == 0);
     * the final object check enforces
     * !S_ISREG(file_status.st_mode), file_status.st_uid ownership, and
     * fchmod(fd, (mode_t)0600). */
    if (!open_event_parent(path, path_copy, &directory_fd, &component)) { return 0; }

    if (fstat(directory_fd, &directory_status) != 0) {
        const int saved_errno = errno;
        (void)close(directory_fd);
        errno = saved_errno;
        return 0;
    }
    /* A privilege-dropped host process may append to its own 0600 leaf in a
     * root-owned log directory. Root remains trusted, while writable parents
     * and non-euid final files remain rejected. */
    if ((directory_status.st_uid != geteuid() &&
            directory_status.st_uid != 0) ||
        (directory_status.st_mode & (S_IWGRP | S_IWOTH)) != 0) {
        (void)close(directory_fd);
        errno = EACCES;
        return 0;
    }

    fd = openat(directory_fd, component, flags, (mode_t)0600);
    {
        const int saved_errno = errno;
        (void)close(directory_fd);
        errno = saved_errno;
    }
    if (fd < 0) {
        return 0;
    }
    if (!validate_event_file(fd)) { int saved_errno = errno; (void)close(fd); errno = saved_errno; return 0; }
#if !defined(O_CLOEXEC)
    {
        const int close_on_exec_flags = fcntl(fd, F_GETFD);
        if (close_on_exec_flags < 0 ||
            fcntl(fd, F_SETFD, close_on_exec_flags | FD_CLOEXEC) < 0) {
            const int saved_errno = errno;
            (void)close(fd);
            errno = saved_errno;
            return 0;
        }
    }
#endif
    {
        const int descriptor_flags = fcntl(fd, F_GETFL);
        if (descriptor_flags < 0 ||
            fcntl(fd, F_SETFL, descriptor_flags & ~O_NONBLOCK) < 0) {
            const int saved_errno = errno;
            (void)close(fd);
            errno = saved_errno;
            return 0;
        }
    }

    *out_fd = fd;
    return 1;
#endif
}
