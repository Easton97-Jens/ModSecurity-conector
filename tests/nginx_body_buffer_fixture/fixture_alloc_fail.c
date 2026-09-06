/*
 * Test-only allocation fault injector.
 *
 * The native fixture sets MSCONNECTOR_NGINX_BODY_FIXTURE_FAIL_ALLOC only for
 * its final allocation-failure request.  On the supported glibc GitHub-hosted
 * runner this makes the connector's fixed 32768-byte request-pool scratch
 * allocation fail.  It is compiled into a separately preloaded test library,
 * never into the connector or NGINX modules, and is not a production switch.
 */

#define _GNU_SOURCE

#include <errno.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

extern void *__libc_malloc(size_t size) __attribute__((weak));

void *
malloc(size_t size)
{
    const char *enabled = getenv("MSCONNECTOR_NGINX_BODY_FIXTURE_FAIL_ALLOC");

    if (enabled != NULL && strcmp(enabled, "1") == 0 && size == 32768U) {
        errno = ENOMEM;
        return NULL;
    }
    if (__libc_malloc != NULL) {
        return __libc_malloc(size);
    }
    return NULL;
}
