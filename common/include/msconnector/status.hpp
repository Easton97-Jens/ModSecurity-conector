#ifndef MSCONNECTOR_STATUS_HPP
#define MSCONNECTOR_STATUS_HPP
#include "msconnector/status.h"
namespace msconnector {
using Status = msconnector_status;
inline const char *status_name(msconnector_status status) noexcept { return msconnector_status_name(status); }
}
#endif
