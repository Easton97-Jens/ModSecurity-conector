#ifndef MSCONNECTOR_PHASE4_BUDGET_H
#define MSCONNECTOR_PHASE4_BUDGET_H

#include <stddef.h>
#include <stdint.h>

#include "msconnector/options.h"

/*
 * Effective cumulative inspection budget, not an allocation or wire limit.
 * Off disables the extra Phase-4 budget while retaining SIZE_MAX accounting
 * overflow checks. Never use this value to allocate a response-sized buffer;
 * independent host/transport and libModSecurity limits remain authoritative.
 * Unset/unknown modes return zero and must fail closed, not act as off.
 */
static inline size_t msconnector_phase4_effective_body_limit(
    enum msconnector_phase4_mode mode, size_t configured_limit)
{
    switch (mode) {
    case MSCONNECTOR_PHASE4_MODE_OFF:
        return SIZE_MAX;
    case MSCONNECTOR_PHASE4_MODE_SAFE:
    case MSCONNECTOR_PHASE4_MODE_STRICT:
        return configured_limit;
    default:
        return 0U;
    }
}

#endif
