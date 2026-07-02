#ifndef MSCONNECTOR_LOGGING_HPP
#define MSCONNECTOR_LOGGING_HPP
#include "msconnector/logging.h"
namespace msconnector { inline void log(const msconnector_logger *logger, const msconnector_log_record *record) noexcept { msconnector_log(logger, record); } }
#endif
