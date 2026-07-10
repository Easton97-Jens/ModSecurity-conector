#include "envoy_modsecurity_mapper.h"

#include "common/runtime/http_authorization_service.h"
#include "common/runtime/msconnector_runtime.h"

static const char *const envoy_original_uri_headers[] = {
    "x-envoy-original-path",
    "x-forwarded-uri",
    "x-original-uri"
};

static const msconnector_http_authorization_profile envoy_ext_authz_profile = {
    "envoy",
    "ext_authz",
    envoy_original_uri_headers,
    sizeof(envoy_original_uri_headers) / sizeof(envoy_original_uri_headers[0]),
    envoy_modsecurity_map_request,
    envoy_modsecurity_map_response
};

int main(int argc, char **argv)
{
    return msconnector_http_authorization_service_main(
        argc,
        argv,
        &envoy_ext_authz_profile);
}
