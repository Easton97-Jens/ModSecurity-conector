# lighttpd Connector

Status: bridge-starter
Runtime status: not-verified
Template alignment: bridge-starter, not runtime-verified

This connector now contains a repository-owned decision-service bridge starter
for lighttpd. It is the smallest local next step after the metadata/probe
build-starter: it defines local request/decision data flow, compiles a CLI
self-test, and reuses connector-neutral `common/` status, origin, intervention,
and capability helpers.

The bridge starter is not a lighttpd module, not a FastCGI/SCGI implementation,
not a runtime harness, and not a libmodsecurity integration. It does not include
lighttpd headers, call lighttpd APIs, call ModSecurity APIs, process real
lighttpd traffic, load CRS, or write framework result JSON.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

The shared rules, gates, status vocabulary, No-CRS/With-CRS separation,
coverage matrix requirements, runtime evidence requirements, and RESPONSE_BODY
minimum evidence are defined globally and are not duplicated here.

## lighttpd-specific State

- Origin/license: documented for current repo-owned bridge starter; no upstream
  lighttpd source imported.
- Metadata: `metadata.c` / `metadata.h` present for bridge-starter status.
- Metadata/probe build: `build/build_starter.sh` compile-checkable.
- Bridge starter: local decision-service starter with CLI self-test.
- Native lighttpd module: not implemented.
- FastCGI/SCGI bridge: not implemented.
- Harness: contract only.
- No-CRS runtime: not run.
- With-CRS runtime: not run.
- RESPONSE_BODY blocking: not verified.

## Build and Self-Test Starters

Local starter commands:

```sh
make -C connectors/lighttpd build-starter
make -C connectors/lighttpd self-test
make -C connectors/lighttpd build-bridge-starter
make -C connectors/lighttpd self-test-bridge
```

The bridge starter sources are:

- `connectors/lighttpd/src/lighttpd_bridge.h`
- `connectors/lighttpd/src/lighttpd_bridge.c`
- `connectors/lighttpd/src/lighttpd_bridge_main.c`

A PASS from these commands proves only local compile/self-test behavior for the
repo-owned starter. It is not a lighttpd module build and is not runtime
validation.

## Chosen Minimal Next Step

Native lighttpd module, FastCGI, and SCGI integration are deferred because this
repository does not currently contain selected lighttpd headers/SDK/source,
module build configuration, FastCGI/SCGI protocol adapter code, or a lighttpd
runtime harness.

The chosen next step is a local decision-service bridge starter. It is a future
bridge integration point only. It intentionally evaluates a local probe request
as `blocked` because no real lighttpd runtime hook, FastCGI/SCGI protocol
adapter, or libmodsecurity integration exists yet.

## Tests

No local `connectors/lighttpd/tests` folder is used. Executable tests are
framework-owned.

Framework-owned paths and targets to use when a real lighttpd build and harness
exist:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No lighttpd runtime result is claimed by this bridge starter. No-CRS and
With-CRS must be validated separately before promotion, and RESPONSE_BODY
blocking remains not verified.

## Parallel Runtime-Smoke Phase

Phase 1 uses `integration_mode=architecture_spike_plus_runtime_smoke`. The
selected production integration path is still open and must be chosen before any
runtime success can be claimed.

The lighttpd connector-specific surface is limited to:

- evaluating native module, FastCGI/SCGI, sidecar/proxy, and mod_magnet/Lua
  paths;
- future lighttpd configuration for the chosen path;
- lighttpd smoke harness entrypoint.

Shared request, response, intervention, status, logging, capabilities, origin,
and transaction concepts come from `common/include/msconnector/`. Runtime smoke
evidence is written through `common/scripts/write_smoke_result.py`, so lighttpd
does not maintain its own JSON result writer.

`make smoke-lighttpd` sources the framework common smoke wrapper, which sources
`modules/ModSecurity-test-Framework/ci/common.sh`. Runtime dependencies are not
installed globally and the harness does not assume `lighttpd` exists in the
global `PATH`.

Lighttpd binary lookup uses:

1. `LIGHTTPD_BIN`;
2. local common.sh-managed paths such as `$CONNECTOR_COMPONENT_CACHE`,
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
   `$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`;
3. Exit 77 with BLOCKED evidence if no local binary is found or if the
   integration path is still open.

Example:

```sh
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```

Local staging helper:

```sh
make prepare-lighttpd-runtime
```

The helper prepares `$CONNECTOR_COMPONENT_CACHE/lighttpd/bin` and reports
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd` when present. If the binary is
missing, it exits 77 without installing or downloading lighttpd. The smoke stays
BLOCKED until the lighttpd integration mode is implemented.

lighttpd source metadata is centralized in `common.sh`: `LIGHTTPD_VERSION=1.4.84`,
the official 1.4.x release index, the latest marker URL used only for pinning,
the fixed tar.xz download URL, `LIGHTTPD_SHA256_URL`, and the pinned SHA256.
The machine-readable mirror is
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
Downloads are not executed by default; any future download path must require
`ALLOW_RUNTIME_DOWNLOADS=1`, verify the pinned SHA256, and stage only under
`$CONNECTOR_COMPONENT_CACHE/lighttpd`.

Current evidence uses `skipped_reason="lighttpd integration mode not selected"`.
When no local binary is found, `missing_dependencies` includes `lighttpd`.
Evidence is written to `$VERIFIED_RUN_ROOT/lighttpd-smoke/`; if
`VERIFIED_RUN_ROOT` is not set, the fallback is
`$BUILD_ROOT/results/lighttpd-smoke/`.

The recommended Phase 1 integration mode is sidecar/proxy, but it is not yet
implemented as runtime evidence. Until that path has real lighttpd traffic and a
documented ModSecurity decision boundary, `runtime_verified` remains `false`.
