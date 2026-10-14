/* External test-only APX physical host observations. Never release-linked. */
#include "apache-host-observer.h"
#include <errno.h>
#include <fcntl.h>
#include <inttypes.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

static pthread_mutex_t observer_lock = PTHREAD_MUTEX_INITIALIZER;
static int observer_fd = -1;
static unsigned long record_count;
static int invalid;

static int open_observer(void) {
    if (observer_fd >= 0) return 1;
    const char *path = getenv("MSCONNECTOR_APACHE_HOST_OBSERVER");
    if (path == NULL || path[0] != '/') return 0;
    int fd = open(path, O_WRONLY | O_APPEND | O_CREAT | O_NOFOLLOW | O_CLOEXEC, 0600);
    struct stat details;
    if (fd < 0) return 0;
    if (fstat(fd, &details) != 0 || !S_ISREG(details.st_mode) ||
            details.st_uid != geteuid() || (details.st_mode & 077U) != 0 || details.st_nlink != 1) {
        (void)close(fd);
        return 0;
    }
    observer_fd = fd;
    return 1;
}

static void observe(const char *kind, msc_t *msr, request_rec *request,
                    const apr_bucket *bucket, uint64_t scope_call) {
    struct timespec now;
    char record[1536];
    char request_uri[300] = "null";
    char request_method[40] = "null";
    int saved = errno;
    (void)pthread_mutex_lock(&observer_lock);
    if (++record_count > 4096U || !open_observer() || clock_gettime(CLOCK_MONOTONIC, &now) != 0) {
        invalid = 1;
        goto done;
    }
    /* Labels come only from the instrumented constant source callsites. */
    if (kind == NULL || strspn(kind, "abcdefghijklmnopqrstuvwxyz_") != strlen(kind)) {
        invalid = 1;
        goto done;
    }
    if (request != NULL && request->uri != NULL && strlen(request->uri) < 256U &&
            strspn(request->uri, "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/_-.") == strlen(request->uri)) {
        (void)snprintf(request_uri, sizeof(request_uri), "\"%s\"", request->uri);
    }
    if (request != NULL && request->method != NULL && strlen(request->method) < 16U &&
            strspn(request->method, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") == strlen(request->method)) {
        (void)snprintf(request_method, sizeof(request_method), "\"%s\"", request->method);
    }
    int count = snprintf(record, sizeof(record),
        "{\"schema\":\"apache-host-observer-v1\",\"pid\":%ld,\"uid\":%ld,\"gid\":%ld,"
        "\"sequence\":%lu,\"monotonic_ns\":%" PRIu64 ",\"kind\":\"%s\","
        "\"request_uri\":%s,\"request_method\":%s,"
        "\"allocation_scope_call\":%" PRIu64 ",\"host_context_present\":%s,"
        "\"native_transaction_present\":%s,\"owner_request_matches\":%s,"
        "\"actual_apr_bucket_present\":%s,\"actual_apr_bucket_is_eos\":%s,"
        "\"response_committed\":%d,\"response_eos_released\":%d,\"terminal_event_attempted\":%d,\"event_sink_error\":%d,"
        "\"request_eos_released\":%d,\"response_eos_seen\":%d,"
        "\"request_body_processed\":%d,\"response_body_processed\":%d,"
        "\"contract_initialized\":%d,\"contract_last_completed_phase\":%d,"
        "\"contract_error_class\":%d,\"contract_cleanup_complete\":%d,"
        "\"native_mime_selection\":null,\"invalid\":%s}\n",
        (long)getpid(), (long)geteuid(), (long)getegid(), record_count,
        (uint64_t)now.tv_sec*UINT64_C(1000000000)+(uint64_t)now.tv_nsec, kind, request_uri, request_method, scope_call,
        msr != NULL ? "true" : "false", msr != NULL && msr->t != NULL ? "true" : "false",
        msr != NULL && msr->owner_request == request ? "true" : "false",
        bucket != NULL ? "true" : "false", bucket != NULL && APR_BUCKET_IS_EOS(bucket) ? "true" : "false",
        msr != NULL ? msr->response.committed : -1,
        msr != NULL ? msr->response_phase4_eos_released : -1,
        msr != NULL ? msr->intervention.terminal_event_attempted : -1,
        msr != NULL ? (int)msr->intervention.event_sink_error : -1,
        msr != NULL ? msr->request_body_eos_released : -1, msr != NULL ? msr->response.body_eos_seen : -1,
        msr != NULL ? msr->request_body_processed : -1, msr != NULL ? msr->response_body_processed : -1,
        msr != NULL ? msr->contract_initialized : -1, msr != NULL ? (int)msr->contract.last_completed_phase : -1,
        msr != NULL ? (int)msr->contract.error_class : -1, msr != NULL ? msr->contract.cleanup_complete : -1,
        invalid ? "true" : "false");
    if (count <= 0 || (size_t)count >= sizeof(record) || scope_call == 0U ||
            write(observer_fd, record, (size_t)count) != count) invalid = 1;
done:
    (void)pthread_mutex_unlock(&observer_lock);
    errno = saved;
}

void apache_lifecycle_observe(const char *kind, msc_t *msr, request_rec *request,
                              const apr_bucket *bucket) {
    int saved = errno;
    uint64_t call = msconnector_lifecycle_host_scope_call(msr);
    observe(kind, msr, request, bucket, call);
    errno = saved;
}

void apache_lifecycle_retire(msc_t *msr, request_rec *request) {
    int saved = errno;
    uint64_t call = msconnector_lifecycle_host_scope_call(msr);
    if (!msconnector_lifecycle_host_retire(msr)) invalid = 1;
    observe("host_context_retired", msr, request, NULL, call);
    errno = saved;
}

__attribute__((destructor)) static void close_observer(void) {
    int saved = errno;
    if (observer_fd >= 0 && close(observer_fd) != 0) invalid = 1;
    if (invalid) {
        static const char error[] = "apache-host-observer: evidence invalid\n";
        (void)write(STDERR_FILENO, error, sizeof(error)-1U);
    }
    errno = saved;
}
