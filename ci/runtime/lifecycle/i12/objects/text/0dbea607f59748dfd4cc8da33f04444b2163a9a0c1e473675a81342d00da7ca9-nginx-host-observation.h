/* Test-only typed host observations. Never changes product decisions. */
#ifndef NGXI12_HOST_OBSERVATION_H
#define NGXI12_HOST_OBSERVATION_H
#include <errno.h>
#include <dirent.h>
#include <fcntl.h>
#include <inttypes.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>
#include "native-lifecycle-observer.h"
static inline uint64_t ngxi12_host_begin(void)
{
    int saved = errno;
    uint64_t call = msconnector_lifecycle_host_begin();
    errno = saved;
    return call;
}
static inline void ngxi12_host_end(uint64_t call, const ngx_http_modsecurity_ctx_t *ctx,
    const msconnector_transaction_contract *common, const Transaction *native, int result)
{
    int saved = errno;
    (void)msconnector_lifecycle_host_end(call, ctx, common, native, result);
    errno = saved;
}
static inline void ngxi12_host_retire(const ngx_http_modsecurity_ctx_t *ctx)
{
    int saved = errno;
    (void)msconnector_lifecycle_host_retire(ctx);
    errno = saved;
}
static inline int ngxi12_fd_count(void)
{
    DIR *directory = opendir("/proc/self/fd");
    struct dirent *entry;
    int total = 0;
    int scan;
    if (directory == NULL) { return -1; }
    scan = dirfd(directory);
    while ((entry = readdir(directory)) != NULL) {
        char *end = NULL;
        long fd = strtol(entry->d_name, &end, 10);
        if (end != entry->d_name && *end == '\0' && fd >= 0 && fd != scan) { ++total; }
    }
    (void)closedir(directory);
    return total;
}
static inline void ngxi12_host_note(const ngx_http_modsecurity_ctx_t *ctx,
    const char *operation, unsigned int last_buf, unsigned int last_in_chain,
    int64_t remaining)
{
    int saved_errno = errno;
    const char *setting = getenv("MSCONNECTOR_NGX_HOST_FD");
    char *end = NULL;
    long fd = setting != NULL ? strtol(setting, &end, 10) : -1;
    struct stat info;
    struct timespec mono, real;
    int descriptors = ngxi12_fd_count();
    if (ctx != NULL && setting != NULL && end != setting && *end == '\0' &&
        fd >= 3 && fd <= 1048576 && fstat((int)fd, &info) == 0 &&
        S_ISREG(info.st_mode) && info.st_nlink == 1 &&
        (fcntl((int)fd, F_GETFL) & O_ACCMODE) != O_RDONLY &&
        clock_gettime(CLOCK_MONOTONIC, &mono) == 0 &&
        clock_gettime(CLOCK_REALTIME, &real) == 0) {
        (void)dprintf((int)fd, "{\"pid\":%ld,\"operation\":\"%s\",\"allocation_scope_call\":%" PRIu64
            ",\"last_buf\":%u,\"last_in_chain\":%u,\"remaining\":%" PRId64
            ",\"header_sent\":%u,\"connection_sent\":%" PRId64
            ",\"fd_count\":%d,\"monotonic_ns\":%" PRId64 ",\"realtime_ns\":%" PRId64 "}\n",
            (long)getpid(), operation, msconnector_lifecycle_host_scope_call(ctx),
            last_buf, last_in_chain, remaining,
            ctx->r != NULL ? (unsigned int)ctx->r->header_sent : 0U,
            ctx->r != NULL && ctx->r->connection != NULL ? (int64_t)ctx->r->connection->sent : -1,
            descriptors, (int64_t)mono.tv_sec * INT64_C(1000000000) + mono.tv_nsec,
            (int64_t)real.tv_sec * INT64_C(1000000000) + real.tv_nsec);
    }
    errno = saved_errno;
}
#endif
