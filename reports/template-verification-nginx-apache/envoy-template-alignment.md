# Envoy Template Alignment

Status: bridge-starter
Runtime status: not-verified

Envoy now has repository-local origin/source-map metadata and a local
sidecar/HTTP bridge starter. It still has no runtime-verified Envoy adapter
implementation, no local tests, and no Envoy runtime claims.

Global/shared rules are referenced instead of duplicated:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Integration Path

The selected minimal path is `bridge-starter`: compile a local sidecar/HTTP
bridge decision model against connector-neutral `common/` code. Productive
native/ext_proc/proxy-wasm integration remains deferred because this repository
does not contain Envoy SDK/API headers, ext_proc protobuf/gRPC bindings,
proxy-wasm SDK/toolchain, or an Envoy runtime harness.

## What The Starter Can Do

- compile repository-local Envoy metadata and bridge source;
- model request headers and URI/query input with `msconnector_request`;
- return allow/block decisions with `msconnector_status` and
  `msconnector_intervention`;
- run a local CLI self-test covering allow and 403 block decisions.

## What The Starter Cannot Claim

- no real Envoy API use;
- no libmodsecurity API use;
- no CRS loading;
- no No-CRS or With-CRS runtime run;
- no RESPONSE_BODY verification;
- no framework-owned YAML execution for Envoy.

## Phase Matrix

| Phase | Status |
| --- | --- |
| Phase 0 Scaffold | OK |
| Phase 1 Origin/Metadata | bridge-starter |
| Phase 2 Build | bridge-starter PASS |
| Phase 3 Bridge Self-Test | PASS |
| Phase 4 ModSecurity Bridge | blocked; libmodsecurity headers/libs not found |
| Phase 5 Envoy Harness | missing |
| Phase 6 No-CRS | not-run |
| Phase 7 With-CRS | not-run |
| Phase 8 CRS Evidence | not-verified |
| Phase 9 RESPONSE_BODY | not-verified |
| Phase 10 Negative/pass-through | local self-test only |
| Phase 11 Audit/log | not-verified |
| Phase 12 Promotion | not allowed beyond bridge-starter |

## Build-Starter Evidence

- Command: `make -C connectors/envoy build-starter`
- Result: PASS for local bridge-starter compilation
- Command: `make -C connectors/envoy self-test`
- Result: PASS for local bridge decision self-test
- Output path: `/src/ModSecurity-conector-build/envoy-bridge-starter`
- Runtime status remains `not-verified`

## Framework Starter Evidence

`make connector-starter-checks` also records Envoy starter results in
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` and
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Those records are connector-starter evidence only and keep
`runtime_verified: false`, `runtime_status: not-verified`, and
`response_body_verified: false`.

## Runtime-Smoke Entry Point

`make smoke-envoy` now invokes the framework-owned Envoy runtime-smoke runner.
Current status is BLOCKED because no executable Envoy runtime harness exists
under `connectors/envoy/harness/`. Runtime remains not verified and
RESPONSE_BODY remains not verified.
