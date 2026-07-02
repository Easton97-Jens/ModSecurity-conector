#include "msconnector/memory.h"
#include <stdlib.h>

static void *default_alloc(size_t size, void *userdata) { (void)userdata; return malloc(size); }
static void default_free(void *ptr, void *userdata) { (void)userdata; free(ptr); }

void msconnector_allocator_init(msconnector_allocator *allocator, size_t max_bytes) {
    if (allocator == 0) { return; }
    allocator->bytes_allocated = 0U;
    allocator->max_bytes = max_bytes;
    allocator->alloc = default_alloc;
    allocator->free = default_free;
    allocator->userdata = 0;
}

int msconnector_alloc_checked(msconnector_allocator *allocator, size_t size, void **out) {
    void *ptr;
    if (out != 0) { *out = 0; }
    if (allocator == 0 || out == 0 || size == 0U || allocator->alloc == 0) { return 0; }
    if (size > allocator->max_bytes || allocator->bytes_allocated > allocator->max_bytes - size) { return 0; }
    ptr = allocator->alloc(size, allocator->userdata);
    if (ptr == 0) { return 0; }
    allocator->bytes_allocated += size;
    *out = ptr;
    return 1;
}

void msconnector_free_checked(msconnector_allocator *allocator, void **ptr, size_t size) {
    if (allocator == 0 || ptr == 0 || *ptr == 0 || allocator->free == 0) { return; }
    allocator->free(*ptr, allocator->userdata);
    *ptr = 0;
    allocator->bytes_allocated = size > allocator->bytes_allocated ? 0U : allocator->bytes_allocated - size;
}

int msconnector_allocator_within_limit(const msconnector_allocator *allocator) { return allocator != 0 && allocator->bytes_allocated <= allocator->max_bytes; }
