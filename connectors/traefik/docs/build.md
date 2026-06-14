# Traefik Build

Status: decision-service-starter
Runtime status: not-verified

A compile-time metadata starter and a local decision-service starter exist. They
are not Traefik runtime adapter builds.

## Build Starter Commands

```sh
connectors/traefik/build/build-starter.sh
make -C connectors/traefik build-starter
make -C connectors/traefik build-decision-service
make -C connectors/traefik self-test-decision-service
```

Compatibility aliases `build-forwardauth-starter` and `self-test-forwardauth`
currently run the same local decision-service starter. They do not implement or
verify Traefik `forwardAuth` HTTP behavior.

The metadata starter compiles:

- `common/src/origin.c`
- `common/src/capabilities.c`
- `connectors/traefik/metadata.c`
- `connectors/traefik/src/traefik_build_starter.c`

The decision-service starter additionally compiles:

- `common/src/intervention.c`
- `common/src/status.c`
- `connectors/traefik/src/traefik_decision_service.c`
- `connectors/traefik/src/traefik_decision_service_main.c`

Include paths:

- `common/include`
- `connectors/traefik`
- `connectors/traefik/src`

Default artifact paths:

- `$BUILD_ROOT/traefik-build-starter/traefik_build_starter`
- `$BUILD_ROOT/traefik-build-starter/traefik_decision_service_starter`

Default result paths:

- `$BUILD_ROOT/traefik-build-starter/result.txt`
- `$BUILD_ROOT/traefik-build-starter/decision-service-result.txt`

Last local status: metadata build-starter PASS; decision-service starter build
PASS; decision-service self-test PASS.

## Not Implemented

No production Traefik build is implemented. No Traefik binary, container,
plugin, middleware, Go module, HTTP server, `forwardAuth` runtime, or
libmodsecurity runtime integration is built by this starter.

## Production Build Blockers

A production Traefik adapter build is blocked until these are selected and
documented:

- Traefik integration API or bridge strategy
- Traefik source, binary, container, plugin SDK, middleware SDK, or Go module
- license and origin evidence for any imported Traefik-facing source
- libmodsecurity runtime integration point
- HTTP service or other bridge runtime if `forwardAuth` is selected
- build command and reproducible artifact path
- runtime harness command and evidence paths
