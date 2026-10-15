#ifndef I12_APACHE_HOST_OBSERVER_H
#define I12_APACHE_HOST_OBSERVER_H
#include <stdint.h>
#include "mod_security3.h"
/* Test-only observer ABI; native owner finalizes these declarations. */
uint64_t msconnector_lifecycle_host_begin(void);
int msconnector_lifecycle_host_end(uint64_t, const void *, const msconnector_transaction_contract *, const Transaction *, int);
uint64_t msconnector_lifecycle_host_scope_call(const void *);
int msconnector_lifecycle_host_retire(const void *);
void apache_lifecycle_observe(const char *, msc_t *, request_rec *, const apr_bucket *);
void apache_lifecycle_retire(msc_t *, request_rec *);
#endif
