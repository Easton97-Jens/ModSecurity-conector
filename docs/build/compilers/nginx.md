<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: NGINX

**Language:** English | [Deutsch](nginx.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for NGINX. The
selected full-lifecycle route is `full-lifecycle-nginx` with profile
`native-nginx-http-module`: native NGINX HTTP module. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-nginx` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-nginx` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-nginx` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-nginx` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-nginx` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework resolves the NGINX source policy and libmodsecurity inputs. The prepared Cache-v2 inventory and its provenance records, not this guide, are the source of the effective revision and host build identity.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `BUILD_NGINX_FROM_SOURCE`, `NGINX_SOURCE_MODE`, `NGINX_SOURCE_REPO_URL`, `NGINX_SOURCE_GIT_REF`, `NGINX_RELEASE_TAG`, `NGINX_BIN`, `NGINX_PREFIX`, and `NGINX_MODULE`.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../reference/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted C compiler and the selected NGINX build inputs are required. Module ABI, prefix, worker permissions and runtime paths belong to the selected host and must stay outside the checkout.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-runtime-components VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-nginx VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-nginx
make check-config-nginx
make start-smoke-nginx
make runtime-smoke-nginx
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="nginx-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-nginx
NO_CRS_RUN_ID="$run_id" make evidence-check-nginx
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

For a diagnostic source-host smoke, use `BUILD_NGINX_FROM_SOURCE=1 make smoke-nginx`. `make check-nginx-c17` checks the adoption boundary; it is not runtime evidence.

> Historical note: A direct dynamic-module build or a narrowed smoke can help diagnose an ABI or permissions issue, but it is not a substitute for the selected `native-nginx-http-module` evidence route.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [NGINX](../../connectors/nginx.md)
- Configuration details:
  [complete connector reference](../../../examples/nginx/configuration-reference.md)
- Repository examples: [examples/nginx](../../../examples/nginx/README.md)
- Test and evidence boundary:
  [testing and evidence guide](../../testing-and-evidence.md)

For module-load failures, verify the selected binary, module ABI, prefix and worker-access preflight. Do not relabel a protocol profile as HTTP/2 or HTTP/3 proof without matching evidence.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
