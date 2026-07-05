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
| libmodsecurity request-body smoke | conditional via `make smoke-envoy-request-body`; PASS only with local body-forwarding evidence and rule `1000002` |
| Minimal CRS smoke | conditional via `make smoke-envoy-crs`; PASS only with local CRS and CRS-backed 403 evidence |
| Secondary CRS smoke | conditional via `make smoke-envoy-crs-secondary`; PASS only with local CRS and secondary CRS-backed 403 evidence |
| CRS complete | not claimed |
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

The request-body ModSecurity smoke uses the same Envoy `ext_authz` path, but
enables body forwarding for the generated local authz configuration and selects
the request-body smoke case:

```sh
MODSECURITY_SMOKE_CASE=request_body DECISION_BACKEND=libmodsecurity make smoke-envoy
make smoke-envoy-request-body
make smoke-open-connectors-request-body
```

This mode loads `common/rules/modsecurity_request_body_smoke.conf`, sends POST
requests with `Content-Type: application/x-www-form-urlencoded`, and requires
the blocked body marker `modsec-request-body-block` to return 403 from rule
`1000002`. Successful evidence writes `$ENVOY_RESULT_ROOT/request-body-result.json`,
`$ENVOY_LOG_ROOT/request-body-decision.log`, and
`$ENVOY_LOG_ROOT/request-body-request-transcript.jsonl`. It may set
`request_body_smoke_verified=true`; `response_body_verified=true` remains
forbidden.

The minimal CRS smoke uses the same runtime entrypoint with CRS selected:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-envoy
make smoke-envoy-crs
make smoke-envoy-crs-secondary
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

This mode loads CRS from common.sh-managed local paths, writes the generated
CRS smoke config under `$ENVOY_RESULT_ROOT/crs-smoke`, and records CRS-specific
evidence in `$ENVOY_RESULT_ROOT/crs-result.json` and
`$ENVOY_LOG_ROOT/crs-decision.log`. The allowed request must return 200. The
blocked request uses `/?id=1%20UNION%20SELECT%20password%20FROM%20users` and
must return 403 from CRS, not from rule `1000001`.

The secondary CRS smoke uses the same runner with `CRS_SMOKE_CASE=secondary`.
It writes generated config under `$ENVOY_RESULT_ROOT/crs-secondary-smoke`,
records `$ENVOY_RESULT_ROOT/crs-secondary-result.json`,
`$ENVOY_LOG_ROOT/crs-secondary-decision.log`, and
`$ENVOY_LOG_ROOT/crs-secondary-audit.log`, and sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`. A PASS requires HTTP 200 for the
allowed request, HTTP 403 for the secondary probe, and an actual CRS rule
ID/message extracted from evidence. If CRS, libmodsecurity, and Envoy are
available but the secondary probe is not blocked, the result is FAIL.

## Runtime status distinction

Connector metadata remains `runtime_status: not_verified` and `verification_status: connector-gap`. Generated per-run `result.json` files may differ: local starter-smoke PASS can report `runtime_verified: true` and `runtime_status: verified`; no-local-binary or missing runtime cases can report `status: BLOCKED`, `runtime_verified: false`, and `runtime_status: blocked`. These per-run fields do not mean production, CRS, RESPONSE_BODY, or full-matrix verification.

## Common Result Schema

`make smoke-envoy` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`request_body_smoke_verified`, `request_body_access_enabled`,
`request_body_rule_file`, `request_body_rule_id`, `request_method`,
`blocked_body_marker`, `evidence_root`, `timestamp`, `skipped_reason`,
`missing_dependencies`, and `claims_not_allowed`.

Current expected result without a local binary:

- Integration mode: `ext_authz`
- Status: `BLOCKED`
- Exit code: 77
- Runtime status: generated no-local-binary or missing-runtime `result.json` files may report `runtime_status: blocked`; connector metadata remains `runtime_status: not_verified` and `verification_status: connector-gap`.
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

- Runtime status: generated local starter PASS `result.json` files may use `runtime_verified` because the starter smoke completed successfully; connector metadata remains `not_verified` / `connector-gap` until real Envoy runtime evidence exists.
- Allowed request status: `200`
- Blocked request status: `403`
- Resolved runtime binary: local path from `ENVOY_BIN` or a common.sh-managed
  lookup root
- Claims still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`
- This local starter PASS status is not a production, CRS, RESPONSE_BODY, or full-matrix verification claim.

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
- This local starter PASS status is not a production, CRS, RESPONSE_BODY, or full-matrix verification claim.

Expected request-body PASS result with local Envoy and local libmodsecurity:

- Decision backend: `libmodsecurity`
- ModSecurity smoke case: `request_body`
- Request method: `POST`
- Request body access enabled: `true`
- Request body rule file: `common/rules/modsecurity_request_body_smoke.conf`
- Request body rule ID: `1000002`
- Request body rule loaded: `true`
- Blocked body marker: `modsec-request-body-block`
- Allowed request status: `200`
- Blocked request status: `403`
- `request_body_smoke_verified=true`
- Still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`

Expected minimal CRS PASS result with local Envoy, local libmodsecurity, and
local CRS:

- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- CRS version/ref: from common.sh-managed CRS source, for example `v4.26.0`
- CRS runtime dir: `$ENVOY_RESULT_ROOT/crs-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: from libmodsecurity intervention evidence
- `crs_minimal_smoke_verified=true`
- Still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`

Expected secondary CRS PASS result with local Envoy, local libmodsecurity, and
local CRS:

- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- CRS smoke case: `secondary`
- CRS runtime dir: `$ENVOY_RESULT_ROOT/crs-secondary-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: extracted from audit/intervention evidence
- `crs_secondary_smoke_verified=true`
- Still forbidden: `production_ready=true`, `full_matrix_ready=true`,
  `crs_complete=true`, `response_body_verified=true`

No global installation is attempted. To run against a prepared local binary:

```sh
ENVOY_BIN=/lokaler/pfad/envoy make smoke-envoy
```
