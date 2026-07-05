#ifndef LIGHTTPD_MODSECURITY_MAPPER_H
#define LIGHTTPD_MODSECURITY_MAPPER_H

#include "msconnector/config.h"
#include "msconnector/generic_mapper.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef msconnector_generic_request_source lighttpd_modsecurity_request;
typedef msconnector_generic_response_source lighttpd_modsecurity_response;

#define lighttpd_modsecurity_config_init msconnector_generic_config_init
#define lighttpd_modsecurity_map_request msconnector_generic_map_request
#define lighttpd_modsecurity_map_response msconnector_generic_map_response

#ifdef __cplusplus
}
#endif

#endif
