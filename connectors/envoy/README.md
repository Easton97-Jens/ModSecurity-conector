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
