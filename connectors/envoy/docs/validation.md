# Envoy Validation

Status: bridge-starter with conditional local runtime smoke
Runtime status: verified only when a local common.sh-managed Envoy binary runs the HTTP smoke

Envoy runtime validation is conditional. Without a local binary from `ENVOY_BIN`
or common.sh-managed caches, `make smoke-envoy` exits 77 with BLOCKED evidence.
With a resolved local binary, the smoke runner starts a minimal upstream,
minimal ext_authz decision service, and Envoy with a generated local config.

Runtime component metadata is pinned centrally in `common.sh`:
`ENVOY_VERSION=1.38.2`, `ENVOY_SOURCE_URL`, `ENVOY_INSTALL_DOCS_URL`,
`ENVOY_DOWNLOAD_URL`, `ENVOY_SHA256_URL`, and `ENVOY_SHA256`. The expected
local binary remains `$CONNECTOR_COMPONENT_CACHE/envoy/bin/envoy`. Downloads
are disabled unless explicit `ALLOW_RUNTIME_DOWNLOADS=1` prepare execution
verifies the pinned SHA256 and writes only to the local component cache:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-envoy-runtime
make smoke-envoy
```

| Gate | Envoy status |
| --- | --- |
| Build starter | available via `make -C connectors/envoy build-starter` |
| Bridge self-test | available via `make -C connectors/envoy self-test` |
| libmodsecurity targeted smoke | conditional via `DECISION_BACKEND=libmodsecurity make smoke-envoy`; PASS only with local common.sh-managed headers/libs and rule-backed 403 |
| No-CRS | not run |
| With-CRS | not run |
| RESPONSE_BODY | not verified |
| Negative/pass-through | proven only by local runtime smoke when allowed request returns 200 |
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

`make smoke-envoy` invokes the framework-owned Envoy runtime-smoke runner.
`connectors/envoy/harness/run_envoy_smoke.sh` resolves `ENVOY_BIN` or local
common.sh-managed cache artifacts through the shared helpers. If a local Envoy
binary is found, the runner sends one allowed request and one blocked request
through Envoy and records the observed HTTP statuses. If no local binary is
found, it exits 77 with BLOCKED evidence.

This entrypoint does not run the bridge starter self-test as runtime evidence.
RESPONSE_BODY remains not verified.

The optional targeted ModSecurity backend uses the same runtime entrypoint with
an explicit backend selector:

```sh
DECISION_BACKEND=libmodsecurity make smoke-envoy
make smoke-envoy-modsecurity
```

This mode loads `common/rules/modsecurity_targeted_smoke.conf` through a local
libmodsecurity C-API evaluator. The allowed request must return 200 and the
request with `X-Modsec-Smoke: block` must return 403 from rule `1000001`.
`result.json` adds `decision_backend`, `modsecurity_backend_verified`,
`modsecurity_rule_file`, `modsecurity_rule_id`, `modsecurity_rule_loaded`,
`intervention_status`, and `decision_log_path`. Missing local libmodsecurity
headers/libraries are reported as Exit 77/BLOCKED, not as failure or success.

## Common Result Schema

`make smoke-envoy` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`evidence_root`, `timestamp`, `skipped_reason`, `missing_dependencies`, and
`claims_not_allowed`.

Current expected result without a local binary:

- Integration mode: `ext_authz`
- Status: `BLOCKED`
- Exit code: 77
- Runtime verified: `false`
- Evidence root: `$VERIFIED_RUN_ROOT/envoy-smoke/`, falling back to
  `$BUILD_ROOT/results/envoy-smoke/`
- Binary environment variable: `ENVOY_BIN`
- Local search paths: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
  `$SOURCE_ROOT`, all provided by `common.sh`
- Missing dependencies when no local binary is found: `["envoy"]`
- skipped_reason when no local binary is found:
  `envoy runtime dependency not available in local common.sh-managed paths`
- Claims still forbidden for BLOCKED evidence: `runtime_verified=true`,
  `production_ready=true`, `full_matrix_ready=true`, `crs_complete=true`,
  `response_body_verified=true`

Expected PASS result with a local binary:

- Runtime verified: `true`
- Allowed request status: `200`
- Blocked request status: `403`
- Resolved runtime binary: local path from `ENVOY_BIN` or a common.sh-managed
  lookup root
- Claims still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`

Expected targeted ModSecurity PASS result with local Envoy and local
libmodsecurity:

- Decision backend: `libmodsecurity`
- ModSecurity backend verified: `true`
- ModSecurity rule file: `common/rules/modsecurity_targeted_smoke.conf`
- ModSecurity rule ID: `1000001`
- ModSecurity rule loaded: `true`
- Intervention status: `403`
- Decision log path: `$ENVOY_LOG_ROOT/modsecurity-decision.log`
- Claims still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`

No global installation is attempted. To run against a prepared local binary:

```sh
ENVOY_BIN=/lokaler/pfad/envoy make smoke-envoy
```
