/* Test-only, opt-in observer and physical FD fault. APR results are forwarded
 * unchanged. No production sink admission or file validation is bypassed. */
#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif
#include <apr_file_io.h>
#include <apr_portable.h>
#include <dlfcn.h>
#include <errno.h>
#include <fcntl.h>
#include <pthread.h>
#include <stdatomic.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>

static _Atomic unsigned fired;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static struct { apr_file_t *file; int fd; } tracked[256];
static const char root[] = "/var/tmp/codex/ModSecurity-conector/";

static int private_path(const char *path)
{
    return path != NULL && strncmp(path, root, sizeof(root) - 1U) == 0 &&
        strstr(path, "/../") == NULL && strstr(path, "/./") == NULL;
}

static int admitted(void)
{
    const char *marker = getenv("I12_SINK_MARKER");
    const char *target = getenv("I12_SINK_PATH");
    const char *mode = getenv("I12_SINK_FAULT");
    const char expected[] = "I12_APACHE_SINK_FAULT_V1\n";
    char value[sizeof(expected)] = {0};
    struct stat st;
    int saved = errno;
    int ok = 0;
    if (!private_path(marker) || target == NULL || mode == NULL ||
        (!private_path(target) && strcmp(target, "/dev/full") != 0) ||
        (strcmp(mode, "observe") != 0 && strcmp(mode, "closed-descriptor") != 0 &&
         strcmp(mode, "physical-enospc") != 0)) goto done;
    int fd = (int)syscall(SYS_openat, AT_FDCWD, marker, O_RDONLY | O_CLOEXEC | O_NOFOLLOW, 0);
    if (fd < 0) goto done;
    if (fstat(fd, &st) == 0 && S_ISREG(st.st_mode) && st.st_uid == geteuid() &&
        (st.st_mode & 0777) == 0600 &&
        syscall(SYS_read, fd, value, sizeof(value)) == (long)(sizeof(expected) - 1U) &&
        memcmp(value, expected, sizeof(expected) - 1U) == 0) ok = 1;
    (void)syscall(SYS_close, fd);
done:
    errno = saved;
    return ok;
}

static int exact_path(const char *path)
{
    const char *target = getenv("I12_SINK_PATH");
    return admitted() && path != NULL && target != NULL && strcmp(path, target) == 0;
}

static int exact_fd(int fd)
{
    char proc[64], path[4096];
    int saved = errno;
    int match = 0;
    if (fd < 0 || !admitted()) goto done;
    (void)snprintf(proc, sizeof(proc), "/proc/self/fd/%d", fd);
    ssize_t count = readlink(proc, path, sizeof(path) - 1U);
    if (count >= 0) {
        path[count] = '\0';
        match = exact_path(path);
    }
done:
    errno = saved;
    return match;
}

static void remember(apr_file_t *file, int fd)
{
    (void)pthread_mutex_lock(&lock);
    for (size_t i = 0; i < sizeof(tracked) / sizeof(tracked[0]); ++i) {
        if (tracked[i].file == NULL || tracked[i].file == file) {
            tracked[i].file = file;
            tracked[i].fd = fd;
            break;
        }
    }
    (void)pthread_mutex_unlock(&lock);
}

static int lookup(apr_file_t *file, int remove)
{
    int fd = -1;
    (void)pthread_mutex_lock(&lock);
    for (size_t i = 0; i < sizeof(tracked) / sizeof(tracked[0]); ++i) {
        if (tracked[i].file == file) {
            fd = tracked[i].fd;
            if (remove) tracked[i].file = NULL;
            break;
        }
    }
    (void)pthread_mutex_unlock(&lock);
    return fd;
}

static void observe(const char *stage, int result, int return_errno, int fd,
    size_t requested, size_t written, const char *action, int operation_result,
    int operation_errno, int before, int after)
{
    char line[1024];
    int saved = errno;
    int length = snprintf(line, sizeof(line),
        "I12_APACHE_APR {\"pid\":%ld,\"stage\":\"%s\",\"result\":%d,"
        "\"errno_at_return\":%d,\"fd\":%d,\"requested_bytes\":%zu,"
        "\"written_bytes\":%zu,\"action\":\"%s\",\"operation_result\":%d,"
        "\"operation_errno\":%d,\"fd_valid_before\":%d,\"fd_valid_after\":%d}\n",
        (long)getpid(), stage, result, return_errno, fd, requested, written,
        action, operation_result, operation_errno, before, after);
    if (length > 0 && (size_t)length < sizeof(line))
        (void)syscall(SYS_write, STDERR_FILENO, line, (size_t)length);
    errno = saved;
}

static void *symbol(const char *name)
{
    void *result = dlsym(RTLD_NEXT, name);
    if (result == NULL) {
        const char message[] = "I12 sink interposer unresolved real symbol\n";
        (void)syscall(SYS_write, STDERR_FILENO, message, sizeof(message) - 1U);
        _exit(78);
    }
    return result;
}

int msconnector_open_private_event_file(const char *path, int *out_fd)
{
    int (*real_call)(const char *, int *) = symbol("msconnector_open_private_event_file");
    int scoped = exact_path(path);
    int result = real_call(path, out_fd);
    int saved = errno;
    if (scoped) observe("common_private_open", result, saved,
        result && out_fd != NULL ? *out_fd : -1, 0, 0, "none", 0, 0, -1,
        result && out_fd != NULL ? fcntl(*out_fd, F_GETFD) >= 0 : -1);
    errno = saved;
    return result;
}

apr_status_t apr_file_open(apr_file_t **file, const char *path, apr_int32_t flags,
    apr_fileperms_t permissions, apr_pool_t *pool)
{
    apr_status_t (*real_call)(apr_file_t **, const char *, apr_int32_t,
        apr_fileperms_t, apr_pool_t *) = symbol("apr_file_open");
    int scoped = exact_path(path);
    apr_status_t result = real_call(file, path, flags, permissions, pool);
    int saved = errno;
    int fd = -1;
    if (scoped && result == APR_SUCCESS && file != NULL) {
        apr_status_t (*get)(apr_os_file_t *, apr_file_t *) = symbol("apr_os_file_get");
        if (get(&fd, *file) == APR_SUCCESS) remember(*file, fd);
    }
    if (scoped) observe("apr_file_open", result, saved, fd, 0, 0,
        "none", 0, 0, -1, fd >= 0 ? fcntl(fd, F_GETFD) >= 0 : -1);
    errno = saved;
    return result;
}

apr_status_t apr_os_file_put(apr_file_t **file, apr_os_file_t *fd,
    apr_int32_t flags, apr_pool_t *pool)
{
    apr_status_t (*real_call)(apr_file_t **, apr_os_file_t *, apr_int32_t,
        apr_pool_t *) = symbol("apr_os_file_put");
    int descriptor = fd != NULL ? *fd : -1;
    int scoped = exact_fd(descriptor);
    apr_status_t result = real_call(file, fd, flags, pool);
    int saved = errno;
    if (scoped && result == APR_SUCCESS && file != NULL) remember(*file, descriptor);
    if (scoped) observe("apr_os_file_put", result, saved, descriptor, 0, 0,
        "none", 0, 0, 1, fcntl(descriptor, F_GETFD) >= 0);
    errno = saved;
    return result;
}

apr_status_t apr_file_write_full(apr_file_t *file, const void *buffer,
    apr_size_t size, apr_size_t *written)
{
    apr_status_t (*real_call)(apr_file_t *, const void *, apr_size_t,
        apr_size_t *) = symbol("apr_file_write_full");
    apr_status_t (*get)(apr_os_file_t *, apr_file_t *) = symbol("apr_os_file_get");
    int fd = -1;
    int before = -1, after = -1, operation_result = 0, operation_errno = 0;
    const char *action = "none";
    int scoped = get(&fd, file) == APR_SUCCESS && exact_fd(fd);
    if (scoped) {
        remember(file, fd);
        before = fcntl(fd, F_GETFD) >= 0;
        const char *mode = getenv("I12_SINK_FAULT");
        struct stat st;
        int private = fstat(fd, &st) == 0 && S_ISREG(st.st_mode) &&
            st.st_uid == geteuid() && (st.st_mode & 0777) == 0600;
        if (private && strcmp(mode, "observe") != 0 && atomic_exchange(&fired, 1) == 0) {
            action = mode;
            if (strcmp(mode, "closed-descriptor") == 0) {
                operation_result = close(fd);
                operation_errno = operation_result < 0 ? errno : 0;
            } else {
                int full = open("/dev/full", O_WRONLY | O_CLOEXEC | O_NONBLOCK);
                if (full < 0) { operation_result = -1; operation_errno = errno; }
                else {
                    operation_result = dup2(full, fd);
                    operation_errno = operation_result < 0 ? errno : 0;
                    if (full != fd) (void)close(full);
                }
            }
        }
        after = fcntl(fd, F_GETFD) >= 0;
    }
    apr_size_t local_written = 0;
    apr_status_t result = real_call(file, buffer, size, written != NULL ? written : &local_written);
    int saved = errno;
    if (scoped) observe("apr_file_write_full", result, saved, fd, (size_t)size,
        (size_t)(written != NULL ? *written : local_written), action,
        operation_result, operation_errno, before, after);
    errno = saved;
    return result;
}

apr_status_t apr_file_flush(apr_file_t *file)
{
    apr_status_t (*real_call)(apr_file_t *) = symbol("apr_file_flush");
    int fd = lookup(file, 0);
    apr_status_t result = real_call(file);
    int saved = errno;
    if (fd >= 0 && admitted()) observe("apr_file_flush", result, saved, fd,
        0, 0, "none", 0, 0, -1, fcntl(fd, F_GETFD) >= 0);
    errno = saved;
    return result;
}

apr_status_t apr_file_close(apr_file_t *file)
{
    apr_status_t (*real_call)(apr_file_t *) = symbol("apr_file_close");
    int fd = lookup(file, 1);
    int before = fd >= 0 ? fcntl(fd, F_GETFD) >= 0 : -1;
    apr_status_t result = real_call(file);
    int saved = errno;
    if (fd >= 0 && admitted()) observe("apr_file_close", result, saved, fd,
        0, 0, "none", 0, 0, before, fcntl(fd, F_GETFD) >= 0);
    errno = saved;
    return result;
}
