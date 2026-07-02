#ifndef MSCONNECTOR_REQUEST_HPP
#define MSCONNECTOR_REQUEST_HPP
#include "msconnector/request.h"
#include "msconnector/request_helpers.h"
namespace msconnector {
using Bytes = msconnector_bytes;
using Header = msconnector_header;
using Endpoint = msconnector_endpoint;
using Request = msconnector_request;
inline void request_init(msconnector_request *request) noexcept { msconnector_request_init(request); }
inline bool request_validate(const msconnector_request *request) noexcept { return msconnector_request_validate(request) != 0; }
}
#endif
