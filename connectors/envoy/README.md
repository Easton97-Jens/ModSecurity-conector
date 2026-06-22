# Envoy Connector

Status: bridge-starter with conditional local runtime smoke
Runtime status: verified only when a local common.sh-managed Envoy binary runs the HTTP smoke

This connector contains a repository-local sidecar/HTTP bridge starter. It can
compile a small CLI that models request data, returns allow/block decisions, and
uses connector-neutral `common/` request/intervention/status metadata. It does
not contain a production Envoy adapter implementation yet. When a local Envoy
binary is provided through `ENVOY_BIN` or common.sh-managed caches, the
runtime-smoke harness starts a minimal upstream, a minimal ext_authz decision
service, and Envoy with a generated local config to prove an allowed request and
a blocked HTTP 403 path.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Envoy-specific State

- Origin/license: documented as no upstream source selected or imported
- Metadata: repository-local bridge-starter metadata in `metadata.c` and
  `metadata.h`
- Build: bridge starter via `make -C connectors/envoy build-starter`
- Self-test: local CLI self-test via `make -C connectors/envoy self-test`
- Integration path: sidecar/HTTP bridge starter, because native Envoy SDK/API
  headers, proxy-wasm SDK, ext_proc protobuf/gRPC bindings, and an Envoy harness
  are not present in this repository
- Harness: conditional local Envoy ext_authz smoke when a local binary is available
- No-CRS runtime: not run
- With-CRS runtime: not run
- RESPONSE_BODY blocking: not verified

No native Envoy filter, ext_proc service, proxy-wasm module, or libmodsecurity
adapter lifecycle is present. The bridge starter is not runtime compatibility
evidence.

## Tests

No local `connectors/envoy/tests` folder is used. Executable testcases are
framework-owned.

Framework-owned test references:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Make targets: `test-no-crs`, `test-with-crs`, `smoke-common`

No-CRS and With-CRS must be validated separately in the future. RESPONSE_BODY
blocking is not verified for Envoy.

## Parallel Runtime-Smoke Phase

Phase 1 targets Envoy `ext_authz`. `ext_proc` remains documented as a later
phase and is not implemented by this connector tree.

The Envoy connector-specific surface is limited to:

- ext_authz integration design and future Envoy configuration;
- Envoy smoke harness entrypoint;
- Envoy bridge-starter CLI/self-test code.

Shared request, response, intervention, status, logging, capabilities, origin,
and transaction concepts come from `common/include/msconnector/`. Runtime smoke
evidence is written through `common/scripts/write_smoke_result.py`, so Envoy does
not maintain its own JSON result writer.

`make smoke-envoy` sources the framework common smoke wrapper, which sources
`modules/ModSecurity-test-Framework/ci/common.sh`. Runtime dependencies are not
installed globally and the harness does not assume `envoy` exists in the global
`PATH`.

Envoy binary lookup uses:

1. `ENVOY_BIN`;
2. local common.sh-managed paths such as `$CONNECTOR_COMPONENT_CACHE`,
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`,
   `$VERIFIED_RUN_ROOT`, and `$SOURCE_ROOT`;
3. Exit 77 with BLOCKED evidence if no local binary is found.

Example:

```sh
ENVOY_BIN=/lokaler/pfad/envoy make smoke-envoy
```

Local staging helper:

```sh
make prepare-envoy-runtime
```

The helper prepares `$CONNECTOR_COMPONENT_CACHE/envoy/bin` and reports
`$CONNECTOR_COMPONENT_CACHE/envoy/bin/envoy` when present. If the binary is
missing, it exits 77 without installing or downloading Envoy.

Envoy source metadata is centralized in `common.sh`: `ENVOY_VERSION=1.38.2`,
the official GitHub release page, the install docs URL, the Linux x86_64
download URL, `ENVOY_SHA256_URL`, and the pinned SHA256. The
machine-readable mirror is
`modules/ModSecurity-test-Framework/ci/runtime-components.manifest.json`.
Downloads are not executed by default; any future download path must require
`ALLOW_RUNTIME_DOWNLOADS=1`, verify the pinned SHA256, and stage only under
`$CONNECTOR_COMPONENT_CACHE/envoy`.

Current missing-binary evidence uses
`skipped_reason="envoy runtime dependency not available in local common.sh-managed paths"`
and `missing_dependencies=["envoy"]`. Evidence is written to
`$VERIFIED_RUN_ROOT/envoy-smoke/`; if `VERIFIED_RUN_ROOT` is not set, the
fallback is `$BUILD_ROOT/results/envoy-smoke/`.

If a local binary is resolved, `make smoke-envoy` can return PASS only after a
real HTTP smoke observes an allowed request status of 200 and a blocked request
status of 403 through Envoy. That PASS still does not claim production
readiness, full matrix readiness, CRS completeness, or response-body
verification.
