#ifndef MSCONNECTOR_CAPABILITIES_HPP
#define MSCONNECTOR_CAPABILITIES_HPP
#include "msconnector/capabilities.h"
namespace msconnector {
using CapabilityFlags = msconnector_capability_flags;
using Capability = msconnector_capability_flag;
using Capabilities = msconnector_capabilities;
inline const char *capability_name(msconnector_capability_flag flag) noexcept { return msconnector_capability_name(flag); }
}
#endif
