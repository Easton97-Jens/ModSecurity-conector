#ifndef MSCONNECTOR_MEMORY_H
#define MSCONNECTOR_MEMORY_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/*
 * Connector-neutral checked allocator.
 * Ownership vocabulary: borrowed pointers are not freed here; owned pointers
 * returned by msconnector_alloc_checked must be released with
 * msconnector_free_checked; static pointers must never be passed to free; arena
 * allocations may use custom callbacks and are accounted by caller-provided size.
 */
typedef void *(*msconnector_alloc_callback)(size_t size, void *userdata);
typedef void (*msconnector_free_callback)(void *ptr, void *userdata);

typedef struct msconnector_allocator {
    size_t bytes_allocated;
    size_t max_bytes;
    msconnector_alloc_callback alloc;
    msconnector_free_callback free;
    void *userdata;
} msconnector_allocator;

void msconnector_allocator_init(msconnector_allocator *allocator, size_t max_bytes);
int msconnector_alloc_checked(msconnector_allocator *allocator, size_t size, void **out);
void msconnector_free_checked(msconnector_allocator *allocator, void **ptr, size_t size);
int msconnector_allocator_within_limit(const msconnector_allocator *allocator);

#ifdef __cplusplus
}
#endif

#endif
