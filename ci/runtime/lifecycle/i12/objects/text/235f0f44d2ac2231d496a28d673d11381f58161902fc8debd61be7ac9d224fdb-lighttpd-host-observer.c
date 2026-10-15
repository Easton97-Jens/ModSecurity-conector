#define _GNU_SOURCE
#include "lighttpd-host-observer.h"
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
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
static unsigned long sequence;
static int fd = -1;
static int invalid;
static void observe(const char *kind, const msconnector_runtime_transaction *transaction,
    int64_t entity_length, int64_t stream_offset, size_t input_size, int eos, int empty_boundary) {
    int saved = errno;
    (void)pthread_mutex_lock(&lock);
    uint64_t scope = msconnector_lifecycle_runtime_scope_call(transaction);
    const char *path = getenv("MSCONNECTOR_LIGHTTPD_HOST_OBSERVER");
    if (fd < 0 && path != NULL && strncmp(path,"/task/",6U)==0) {
        fd = open(path,O_WRONLY|O_APPEND|O_CREAT|O_NOFOLLOW|O_CLOEXEC,0600);
        struct stat details;
        if (fd >= 0 && (fstat(fd,&details)!=0 || !S_ISREG(details.st_mode) ||
            details.st_uid!=geteuid() || (details.st_mode&0777U)!=0600U || details.st_nlink!=1)) {
            (void)close(fd);fd=-1;
        }
    }
    struct timespec now;
    if (++sequence>4096U || fd<0 || scope==0U || kind==NULL ||
        strspn(kind,"abcdefghijklmnopqrstuvwxyz_")!=strlen(kind) || clock_gettime(CLOCK_MONOTONIC,&now)!=0) {
        invalid=1;goto done;
    }
    char eos_literal[16];
    if (empty_boundary) memcpy(eos_literal, "null", 5U);
    else (void)snprintf(eos_literal, sizeof(eos_literal), "%d", eos);
    char record[1000];
    int count=snprintf(record,sizeof(record),
        "{\"schema\":\"lighttpd-physical-host-v1\",\"pid\":%ld,\"uid\":%ld,\"gid\":%ld,"
        "\"sequence\":%lu,\"monotonic_ns\":%" PRIu64 ",\"kind\":\"%s\","
        "\"runtime_allocation_scope_call\":%" PRIu64 ",\"entity_length\":%" PRId64 ","
        "\"stream_offset\":%" PRId64 ",\"input_size\":%zu,\"actual_eos_argument\":%s,\"empty_request_boundary\":%s,\"invalid\":%s}\n",
        (long)getpid(),(long)geteuid(),(long)getegid(),sequence,
        (uint64_t)now.tv_sec*UINT64_C(1000000000)+(uint64_t)now.tv_nsec,kind,scope,
        entity_length,stream_offset,input_size,eos_literal,empty_boundary?"true":"false",invalid?"true":"false");
    if (count<=0 || (size_t)count>=sizeof(record) || write(fd,record,(size_t)count)!=count) invalid=1;
done:
    (void)pthread_mutex_unlock(&lock);errno=saved;
}
__attribute__((destructor)) static void finish(void) {
    int saved=errno;
    if (fd>=0 && close(fd)!=0) invalid=1;
    if (invalid) {
        static const char message[]="lighttpd-host-observer: evidence invalid\n";
        (void)write(STDERR_FILENO,message,sizeof(message)-1U);
    }
    errno=saved;
}

void lighttpd_observe_body(const char *kind, const msconnector_runtime_transaction *transaction,
    int64_t entity_length, int64_t stream_offset, size_t input_size, int eos) {
    observe(kind, transaction, entity_length, stream_offset, input_size, eos, 0);
}
void lighttpd_observe_empty_request_boundary(const msconnector_runtime_transaction *transaction,
    int64_t actual_entity_length) {
    observe("patched_empty_request_boundary", transaction, actual_entity_length, 0, 0U, 0, 1);
}
