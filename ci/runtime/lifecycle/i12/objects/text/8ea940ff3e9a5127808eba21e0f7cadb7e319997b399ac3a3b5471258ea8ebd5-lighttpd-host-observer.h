#ifndef LIGHTTPD_TEST_HOST_OBSERVER_H
#define LIGHTTPD_TEST_HOST_OBSERVER_H
#include <stdint.h>
#include <stddef.h>
#include "ci/runtime/lifecycle/native-lifecycle-observer.h"
void lighttpd_observe_body(const char *kind, const msconnector_runtime_transaction *transaction,
    int64_t entity_length, int64_t stream_offset, size_t input_size, int eos);
void lighttpd_observe_empty_request_boundary(const msconnector_runtime_transaction *transaction,
    int64_t actual_entity_length);
#endif
