# Envoy Connector

Status: bridge-starter
Runtime status: not-verified

This connector contains a repository-local sidecar/HTTP bridge starter. It can
compile a small CLI that models request data, returns allow/block decisions, and
uses connector-neutral `common/` request/intervention/status metadata. It does
not contain a runtime-verified Envoy adapter implementation yet.

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
- Harness: Envoy runtime harness missing; CLI self-test only
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
   `$VERIFIED_COMPONENT_CACHE`, `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, and
   `$VERIFIED_RUN_ROOT`;
3. Exit 77 with BLOCKED evidence if no local binary is found.

Example:

```sh
ENVOY_BIN=/path/to/local/envoy make smoke-envoy
```

Current missing-binary evidence uses
`skipped_reason="envoy runtime dependency not available in local common.sh-managed paths"`
and `missing_dependencies=["envoy"]`. Evidence is written to
`$VERIFIED_RUN_ROOT/envoy-smoke/`; if `VERIFIED_RUN_ROOT` is not set, the
fallback is `$BUILD_ROOT/results/envoy-smoke/`.
