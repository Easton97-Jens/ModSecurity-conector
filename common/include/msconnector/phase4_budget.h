#ifndef MSCONNECTOR_PHASE4_BUDGET_H
#define MSCONNECTOR_PHASE4_BUDGET_H

#include <stddef.h>
#include <stdint.h>

#include "msconnector/options.h"

/*
 * Checked-accounting ceiling for connector Phase-4 modes.
 *
 * Response-inspection scope and limits belong to libModSecurity
 * (SecResponseBodyAccess, SecResponseBodyMimeType, SecResponseBodyLimit and
 * SecResponseBodyLimitAction). A valid Phase-4 mode therefore has no separate
 * connector-owned cumulative inspection ceiling. SIZE_MAX is only an
 * arithmetic/accounting ceiling and must never be used as an allocation size.
 *
 * Independent host, transport, chunk/frame, bounded-storage and allocation
 * limits remain authoritative. UNSET/unknown modes still return zero so an
 * invalid configuration cannot silently become unlimited.
 */
static inline size_t msconnector_phase4_effective_body_limit(
    enum msconnector_phase4_mode mode)
{
    switch (mode) {
    case MSCONNECTOR_PHASE4_MODE_OFF:
    case MSCONNECTOR_PHASE4_MODE_SAFE:
    case MSCONNECTOR_PHASE4_MODE_STRICT:
        return SIZE_MAX;
    default:
        return 0U;
    }
}

#endif
