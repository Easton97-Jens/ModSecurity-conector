<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: HAProxy

**Language:** English | [Deutsch](haproxy.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for HAProxy. The
selected full-lifecycle route is `full-lifecycle-haproxy-htx` with profile
`native-htx-filter`: native HTX filter selected for the full lifecycle. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-haproxy` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-haproxy` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-haproxy` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-haproxy` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-haproxy-htx` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework/provider pin selects HAProxy source, checksum and runtime inputs. Cache-v2 provenance and the selected run's host metadata provide the effective host identity; do not infer it from a compatibility agent build.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `HAPROXY_VERSION`, `HAPROXY_SOURCE_URL`, `HAPROXY_SHA256`, `HAPROXY_SOURCE_DIR`, `HAPROXY_BIN`, and the advanced `HAPROXY_HTX_*` paths.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../reference/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted C/C++ toolchain, libmodsecurity headers/libraries and the selected HAProxy source are needed. The root build stage creates the SPOA/libmodsecurity compatibility artifacts; the selected full-lifecycle route separately builds and observes the HTX host overlay.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-haproxy VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-haproxy
make check-config-haproxy
make start-smoke-haproxy
make runtime-smoke-haproxy
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="haproxy-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-haproxy-htx
NO_CRS_RUN_ID="$run_id" make evidence-check-haproxy
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

`make -C connectors/haproxy build-spoa-runtime` and its self-tests are useful local diagnostics. `make check-haproxy-htx-overlay` checks overlay structure; `make check-haproxy-c17` checks the C adoption boundary.

> Historical note: The SPOE/SPOP compatibility agent and a standalone HTX smoke are historical or diagnostic integration routes. They must not be relabelled as the canonical `native-htx-filter` run.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [HAProxy](../../connectors/haproxy.md)
- Configuration details:
  [complete connector reference](../../../examples/haproxy/configuration-reference.md)
- Repository examples: [examples/haproxy](../../../examples/haproxy/README.md)
- Test and evidence boundary:
  [testing and evidence guide](../../testing-and-evidence.md)

If a binding build is blocked, inspect the prepared libmodsecurity include/library paths. If the HTX route fails, preserve the generated overlay provenance and sanitized host records instead of substituting a SPOA result.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
