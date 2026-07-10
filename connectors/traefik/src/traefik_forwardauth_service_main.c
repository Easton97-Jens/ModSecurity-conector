#include "traefik_modsecurity_mapper.h"

#include "common/runtime/http_authorization_service.h"

static const char *const traefik_original_uri_headers[] = {
    "X-Forwarded-Uri",
    "X-Original-Uri"
};

static const msconnector_http_authorization_profile traefik_forwardauth_profile = {
    "traefik",
    "forwardAuth",
    traefik_original_uri_headers,
    sizeof(traefik_original_uri_headers) / sizeof(traefik_original_uri_headers[0]),
    traefik_modsecurity_map_request,
    traefik_modsecurity_map_response
};

int main(int argc, char **argv)
{
    return msconnector_http_authorization_service_main(
        argc,
        argv,
        &traefik_forwardauth_profile);
}
