<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: Envoy

**Language:** English | [Deutsch](envoy.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for Envoy. The
selected full-lifecycle route is `full-lifecycle-envoy-ext-proc` with profile
`ext_proc`: streamed Envoy external-processing service with a Common/libmodsecurity bridge. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-envoy` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-envoy` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-envoy` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-envoy` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-envoy-ext-proc` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework runtime preparer selects and verifies the Envoy binary/input provenance. Read the Cache-v2 inventory and generated runtime records for the effective host version and checksum rather than relying on copied release text.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `ENVOY_BIN`, `EXT_PROC_CONFIG`, `EXT_PROC_RUNTIME_CONFIG`, `EXT_PROC_RUNTIME_ROOT`, `RULES_FILE`, `MSCONNECTOR_RULES_FILE`, and the opt-in `ENVOY_TRANSPORT_CANCEL_PROBE`.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../reference/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted C compiler, Go toolchain, libmodsecurity build inputs and a verified Envoy binary are needed for the selected ext_proc route. Direct connector targets use generated files beneath an external build root.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-envoy-runtime VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-envoy VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-envoy
make check-config-envoy
make start-smoke-envoy
make runtime-smoke-envoy
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="envoy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-envoy-ext-proc
NO_CRS_RUN_ID="$run_id" make evidence-check-envoy
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

`make -C connectors/envoy build-envoy-ext-proc`, `test-envoy-ext-proc`, and `check-envoy-ext-proc-config` are focused local gates. `transport-cancel-smoke-envoy-ext-proc` is opt-in and remains non-promoting.

> Historical note: The `ext_authz` service and `make smoke-envoy` compatibility path remain useful diagnostics. They do not silently become the selected `ext_proc` full-lifecycle profile.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [Envoy](../../connectors/envoy.md)
- Configuration details:
  [complete connector reference](../../../examples/envoy/configuration-reference.md)
- Repository examples: [examples/envoy](../../../examples/envoy/README.md)
- Test and evidence boundary:
  [testing and evidence guide](../../testing-and-evidence.md)

For a failed config/start check, verify the resolved `ENVOY_BIN`, generated ext_proc configuration, loopback ports and libmodsecurity runtime library paths. A cancellation probe does not prove a client-visible strict reset.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
