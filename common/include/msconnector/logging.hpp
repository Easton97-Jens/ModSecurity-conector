#ifndef MSCONNECTOR_LOGGING_HPP
#define MSCONNECTOR_LOGGING_HPP
#include "msconnector/logging.h"
namespace msconnector {
using LogLevel = msconnector_log_level;
using LogRecord = msconnector_log_record;
using Logger = msconnector_logger;
inline void log(const msconnector_logger *logger, const msconnector_log_record *record) noexcept { msconnector_log(logger, record); }
}
#endif
