# Traefik Build

Status: minimal_runtime_smoke (forwardAuth request path only)
Runtime status: broader connector behavior not verified

A compile-time metadata starter and local decision-service self-test remain for
compatibility. The real connector build now produces a long-running external
`forwardAuth` service linked to the Common runtime and libmodsecurity.

## Connector Build

```sh
MODSECURITY_INCLUDE_DIR=/local/include \
MODSECURITY_LIB_DIR=/local/lib \
make -C connectors/traefik build-connector
```

The build uses C17 with `-Wall -Wextra -Werror`, writes outside the checkout,
and performs compile/link only. Its default artifact is
`$BUILD_ROOT/traefik-connector/traefik-forwardauth`.

Subsequent stages are intentionally separate:

```sh
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

The config check executes `--check-config`. The start smoke executes `--serve`,
starts real Traefik with a temporary forwardAuth File Provider config, checks
both process lifecycles, and stops both without sending HTTP requests.
The runtime smoke is a third, separate stage that sends real traffic through
Traefik and the built connector service.

## Build Starter Commands

```sh
connectors/traefik/build/build-starter.sh
make -C connectors/traefik build-starter
make -C connectors/traefik build-decision-service
make -C connectors/traefik self-test-decision-service
```

`build-forwardauth-starter` now aliases the real compile/link target.
`self-test-forwardauth` remains an explicitly local legacy decision-model test
and is not runtime evidence.

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

## Not Implemented / Not Verified

No Traefik plugin, middleware module, Go module, or cgo integration is built.
The repository does not build Traefik itself. Response-phase inspection is not
supported by the selected authorization protocol, and no production or current
runtime verification is claimed by the service source alone.

## Production Build Blockers

A production-support claim remains blocked until these are implemented or
evidenced:

- retained CI build/link evidence with pinned libmodsecurity inputs
- retained config-load and service-start evidence
- retained Traefik-to-service allow/block request evidence
- broader shutdown, concurrency, timeout, and error-path evidence
- request-body limit and oversized-request evidence
- event JSONL evidence without request-body payloads
- explicit deployment and origin/license documentation
