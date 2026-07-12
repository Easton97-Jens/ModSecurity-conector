<!-- Generated from scripts/generate_compiler_guides.py; do not edit directly. -->

# Build and lifecycle: lighttpd

**Language:** English | [Deutsch](lighttpd.de.md)

## Purpose and selected host route

This guide documents the current root Make targets for lighttpd. The
selected full-lifecycle route is `full-lifecycle-lighttpd-patched` with profile
`patched-native`: patched native lighttpd host and matching connector module. It is deliberately separate from build,
configuration, and compatibility smokes.

| Stage | current target | what it does | does not establish |
| --- | --- | --- | --- |
| Build | `make build-lighttpd` | builds the connector's selected stage | config load or traffic |
| Configuration | `make check-config-lighttpd` | loads/checks the selected configuration | a sent request |
| Start | `make start-smoke-lighttpd` | starts and stops the host route without full traffic | lifecycle coverage |
| Minimal runtime smoke | `make runtime-smoke-lighttpd` | sends bounded runtime traffic | canonical full lifecycle |
| Full lifecycle | `make full-lifecycle-lighttpd-patched` | collects selected No-CRS host evidence | production, CRS, or full matrix |

## Host version and source provenance

The Framework/provider-selected lighttpd source, patch and libmodsecurity inputs are provenance-controlled. The Cache-v2 inventory and selected host records state the effective source identity; a stock local binary is not the selected patched host.

Show the prepared values before building:

```sh
make runtime-components-inventory
make runtime-components-sources
```

Relevant variables: `LIGHTTPD_BIN`, `LIGHTTPD_SOURCE_DIR`, `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_INCLUDE_DIR`, `LIGHTTPD_MODULE_DIR`, `LIGHTTPD_PATCHED_ROOT`, and the documented `LIGHTTPD_PATCHED_*` runtime paths.
Their format, defaults, scope, effect, and security boundary are defined in the
[central variable reference](../../configuration/variables.md). An override is
an explicit input change, not a capability upgrade.

## Toolchain and Cache-v2

A trusted C toolchain, the selected lighttpd source/patch, libmodsecurity headers/libraries and an external build root are required. The patched host and module must be built as one compatible input set.

For a clean local invocation, choose a writable parent outside the checkout.
`VERIFIED_RUN_PARENT` derives `BUILD_ROOT` and `CACHE_ROOT=.../cache-v2`. The
shared cache holds reusable inputs, not canonical evidence; do not manually
rearrange it or mix incompatible provenance.

```sh
make prepare-lighttpd-runtime-build VERIFIED_RUN_PARENT="/srv/modsecurity-work"
make build-lighttpd VERIFIED_RUN_PARENT="/srv/modsecurity-work"
```

`/srv/modsecurity-work` is an example absolute runtime path, not a repository
default. A target can end with `BLOCKED`/exit code `77` when a prerequisite is
absent.

## Build, configuration, and smoke

Run stages independently so that a failure is not mistaken for a stronger
claim:

```sh
make build-lighttpd
make check-config-lighttpd
make start-smoke-lighttpd
make runtime-smoke-lighttpd
```

For one selected canonical evidence run, use the same safe run identifier. The
`evidence-check` command validates already-produced artifacts only.

```sh
run_id="lighttpd-core-$(date -u +%Y%m%dT%H%M%SZ)"
NO_CRS_RUN_ID="$run_id" make full-lifecycle-lighttpd-patched
NO_CRS_RUN_ID="$run_id" make evidence-check-lighttpd
```

`NO_CRS_RUN_ID` must be a filesystem-safe token. Do not set internal
full-lifecycle profile variables to relabel a direct or compatibility run.

## Optional and historical integration notes

`make -C connectors/lighttpd check-lighttpd-core-patch`, `build-lighttpd-patched-host`, and `check-lighttpd-patched-host` are targeted preparation checks. `make smoke-lighttpd` remains a compatibility smoke, not the patched full-lifecycle run.

> Historical note: Stock-host and bridge/sidecar descriptions are historical or diagnostic routes. The current canonical selection is the `patched-native` host profile, and a successful patch application alone is not runtime proof.

A narrowed case, `FORCE_ALL_CASES=1`, or a direct connector-subdirectory
command is diagnostic input. Only the documented target with its artifact
profile can produce canonical evidence.

## Configuration, examples, and troubleshooting

- Current connector guide: [lighttpd](../../connectors/lighttpd/README.md)
- Configuration details:
  [connector configuration](../../connectors/lighttpd/configuration.md)
- Repository examples: [examples/lighttpd](../../../examples/lighttpd/README.md)
- Test and evidence boundaries: [test levels](../../testing/README.md) ·
  [evidence rules](../../evidence/README.md)

For module-load or patch failures, keep the selected source, patch and module build roots together and inspect the sanitized host log. Do not combine a stock binary with a module built against a different header set.

Do not put unsanitized cookies, authorization values, tokens, private keys, or
raw logs into configuration, issues, or evidence.

## Evidence boundary

This text does not claim production readiness, complete CRS coverage, HTTP/2
or HTTP/3 support, a full matrix, or strict post-commit intervention. A PASS
applies only to the target actually executed, its documented host profile, and
its sanitized run-specific evidence set.
