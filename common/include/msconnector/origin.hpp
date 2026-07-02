#ifndef MSCONNECTOR_ORIGIN_HPP
#define MSCONNECTOR_ORIGIN_HPP
#include "msconnector/origin.h"
namespace msconnector {
using Origin = msconnector_origin;
inline bool origin_is_empty(const msconnector_origin *origin) noexcept { return msconnector_origin_is_empty(origin) != 0; }
}
#endif
