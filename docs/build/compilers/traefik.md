<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: Traefik

**Language:** English | [Deutsch](traefik.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for Traefik. The
selected full-lifecycle route is `full-lifecycle-traefik-native` with profile
`native-middleware`: native Traefik middleware with a private persistent UDS engine service. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-traefik` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-traefik` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-traefik` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-traefik` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-traefik-native` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework runtime preparer supplies the selected Traefik input and records its provenance. Use Cache-v2 inventory and the selected run records as the version source; a locally installed binary is an explicit override, not a hidden default.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `TRAEFIK_BIN`, `TRAEFIK_NATIVE_RUNTIME_ROOT`, `TRAEFIK_CONNECTOR_CONFIG`, `TRAEFIK_ENGINE_SERVICE_BIN`, `MSCONNECTOR_RULES_FILE`, and normal compiler/linker variables.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../configuration/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted Traefik binary, Go toolchain, C compiler and libmodsecurity build inputs are required for the selected native middleware route. The UDS service and generated provider configuration are invocation-local runtime files.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-traefik-runtime VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-traefik VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-traefik
make check-config-traefik
make start-smoke-traefik
make runtime-smoke-traefik
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="traefik-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-traefik-native
NO_CRS_RUN_ID="$run_id" make evidence-check-traefik
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

`make -C connectors/traefik build-native-middleware`, `test-native-middleware`, `build-engine-service`, and `test-engine-service` are focused local checks. They do not themselves create canonical evidence.

> Historical note: The forwardAuth compatibility service and `make smoke-traefik` are separate diagnostic routes. They do not replace the selected `native-middleware` profile or prove a strict post-commit action.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [Traefik](../../connectors/traefik/README.md)
- Configuration details:
  [connector configuration](../../connectors/traefik/configuration.md)
- Repository examples: [examples/traefik](../../../examples/traefik/README.md)
- Test and evidence boundaries: [test levels](../../testing/README.md) ·
  [evidence rules](../../evidence/README.md)

Check the selected `TRAEFIK_BIN`, UDS permissions, generated File Provider configuration and loopback listeners. Do not solve a native middleware failure by publishing forwardAuth compatibility output as canonical evidence.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
