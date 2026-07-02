#ifndef MSCONNECTOR_RESPONSE_HPP
#define MSCONNECTOR_RESPONSE_HPP
#include "msconnector/response.h"
#include "msconnector/response_helpers.h"
namespace msconnector { inline void response_init(msconnector_response *response) noexcept { msconnector_response_init(response); } inline bool response_validate(const msconnector_response *response) noexcept { return msconnector_response_validate(response) != 0; } }
#endif
