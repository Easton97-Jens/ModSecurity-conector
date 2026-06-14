# Envoy Validation

Status: bridge-starter
Runtime status: not-verified

Envoy runtime validation has not been executed. The executable Envoy check
currently available in this repository is a local bridge CLI self-test.

| Gate | Envoy status |
| --- | --- |
| Build starter | available via `make -C connectors/envoy build-starter` |
| Bridge self-test | available via `make -C connectors/envoy self-test` |
| libmodsecurity bridge | blocked; headers/libs not found in `/src` paths checked |
| No-CRS | not run |
| With-CRS | not run |
| RESPONSE_BODY | not verified |
| Negative/pass-through | local self-test allow branch only; no runtime evidence |
| Audit/log | not verified |

Envoy cannot be promoted beyond bridge-starter without repository-backed
ModSecurity and Envoy runtime evidence for the claimed scope.

Global validation and evidence rules:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

Framework-owned test references:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- Make targets: `test-no-crs`, `test-with-crs`, `smoke-common`

## Executed Bridge-Starter Checks

- Command: `make -C connectors/envoy build-starter`
- Result: PASS for local bridge-starter compilation
- Command: `make -C connectors/envoy self-test`
- Result: PASS for local bridge decision self-test
- Output path: `/src/ModSecurity-conector-build/envoy-bridge-starter`
- Runtime impact: none; Envoy runtime remains `not-verified`

## Framework-Owned Starter Evidence

`make connector-starter-checks` runs Envoy starter checks from
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
Results are written to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

The Envoy entries are connector-starter build/self-test evidence only:
`runtime_verified` is `false`, `runtime_status` is `not-verified`, and
`response_body_verified` is `false`.

## Runtime-Smoke Entry Point

`make smoke-envoy` invokes the framework-owned Envoy runtime-smoke runner. The
current result is BLOCKED. `connectors/envoy/harness/run_envoy_smoke.sh` exists
as a connector-side runtime-smoke entrypoint, but it only writes blocked
diagnostic evidence because no real Envoy server/config/runtime harness exists.
Evidence is written under `/src/ModSecurity-conector-build/results/`.

This entrypoint does not run the bridge starter self-test as runtime evidence.
Runtime remains not verified and RESPONSE_BODY remains not verified.
