#ifndef MSCONNECTOR_INTEGRITY_EVENT_H
#define MSCONNECTOR_INTEGRITY_EVENT_H

#include "msconnector/event.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint64_t msconnector_non_crypto_hash_bytes(const unsigned char *data, size_t size);
uint64_t msconnector_non_crypto_hash_string(const char *value);
uint64_t msconnector_integrity_event_hash(const msconnector_event *event, uint64_t previous_hash);
int msconnector_integrity_event_chain_verify(uint64_t previous_hash, uint64_t event_hash, const msconnector_event *event);

#ifdef __cplusplus
}
#endif

#endif
