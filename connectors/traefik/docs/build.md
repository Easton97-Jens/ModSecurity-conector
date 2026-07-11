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

## Unselected native Go middleware source build

The repository also contains `connectors/traefik/native_middleware/`, a Go
module shaped for Traefik's middleware entry points. It is deliberately
separate from `build-connector`, which continues to build the selected C
`forwardAuth` service.

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

The first target runs focused `go test ./...` and `go vet ./...`; the second
also runs `go build ./...`. Its only retained output is a compile report under
`$BUILD_ROOT/traefik-native-middleware/build.txt`, outside the checkout. The
source uses a `PassthroughEngine` seam rather than Common/libmodsecurity FFI,
so a successful local build is not a rule-evaluation, config-load, Traefik
runtime, response-body, or capability-verification result.

`config/traefik-native-middleware-static.yaml` and
`config/traefik-native-middleware-dynamic.yaml` are unselected local-plugin
and File Provider shapes for an operator-staged local plugin. Neither is loaded
by the forwardAuth smokes or changes their compatibility contract.

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

No Traefik SDK, cgo integration, or Traefik binary is built. The native Go
middleware module is compile-tested only and is unselected; the repository does
not build Traefik itself. Response-phase inspection remains unsupported by the
selected authorization protocol, and no production or current runtime
verification is claimed by either source path alone.

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
