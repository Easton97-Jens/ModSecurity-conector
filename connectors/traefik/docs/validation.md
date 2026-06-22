# Traefik Validation

Status: decision-service-starter
Runtime status: not-verified

Traefik runtime validation has not been run. Global validation gates and status
vocabulary are defined in
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md` and
`connectors/_template/docs/coverage-decision-matrix.md`.

## Current Traefik Evidence

- Metadata build starter: PASS for metadata compile smoke.
- Decision-service starter build: PASS for local compile smoke.
- Decision-service self-test: PASS for in-memory allow/block decisions.
- No-CRS: not run.
- With-CRS: not run.
- RESPONSE_BODY: not verified.
- Negative/pass-through: not verified.
- Audit/log: not verified.

Framework-owned paths and targets for future validation:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

The local decision-service self-test is not a framework runtime result and is
not evidence of Traefik `forwardAuth`, CRS, or libmodsecurity behavior. Traefik
cannot be promoted beyond decision-service-starter without connector-specific
runtime evidence.

## Framework-Owned Starter Evidence

`make connector-starter-checks` runs Traefik metadata and decision-service
starter checks from
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
Results are written to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

The Traefik entries are connector-starter build/self-test evidence only:
`runtime_verified` is `false`, `runtime_status` is `not-verified`, and
`response_body_verified` is `false`.

## Runtime-Smoke Entry Point

`make smoke-traefik` invokes the framework-owned Traefik runtime-smoke runner.
The current result is BLOCKED because
`connectors/traefik/harness/run_traefik_smoke.sh` writes diagnostic evidence and
no real Traefik server/config/runtime harness exists. Evidence is written under
`/src/ModSecurity-conector-build/results/`.

This entrypoint does not run decision-service starter self-tests as runtime
evidence. Runtime remains not verified and RESPONSE_BODY remains not verified.

## Common Result Schema

`make smoke-traefik` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`evidence_root`, `timestamp`, `skipped_reason`, `missing_dependencies`, and
`claims_not_allowed`.

Current expected result:

- Integration mode: `forwardAuth`
- Status: `BLOCKED`
- Exit code: 77
- Runtime verified: `false`
- Evidence root: `$VERIFIED_RUN_ROOT/traefik-smoke/`, falling back to
  `$BUILD_ROOT/results/traefik-smoke/`
- Binary environment variable: `TRAEFIK_BIN`
- Local search paths: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
  `$SOURCE_ROOT`, all provided by `common.sh`
- Missing dependencies when no local binary is found: `["traefik"]`
- skipped_reason when no local binary is found:
  `traefik runtime dependency not available in local common.sh-managed paths`
- Claims still forbidden: `runtime_verified=true`, `production_ready=true`,
  `full_matrix_ready=true`, `crs_complete=true`

No global installation is attempted. To run against a prepared local binary:

```sh
TRAEFIK_BIN=/path/to/local/traefik make smoke-traefik
```
