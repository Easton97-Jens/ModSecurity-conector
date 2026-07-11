# Traefik Validation

Status: minimal_runtime_smoke for the forwardAuth request path only
Runtime status: verified only when a local common.sh-managed Traefik binary runs the HTTP smoke

Traefik runtime validation is conditional. Without a local binary from
`TRAEFIK_BIN` or common.sh-managed caches, `make smoke-traefik` exits 77 with
BLOCKED evidence. With a resolved local binary, the smoke runner starts a
minimal upstream, minimal forwardAuth decision service, and Traefik with a
generated local config. Global validation gates and status vocabulary are defined in
`reports/template-verification-nginx-apache/connector-scaffold-decisions.md` and
`connectors/_template/docs/coverage-decision-matrix.md`.

Runtime component metadata is pinned centrally in `common.sh`:
`TRAEFIK_VERSION=3.7.5`, `TRAEFIK_SOURCE_URL`, `TRAEFIK_INSTALL_DOCS_URL`,
`TRAEFIK_DOWNLOAD_URL`, `TRAEFIK_SHA256_URL`, and `TRAEFIK_SHA256`. The expected
local binary remains `$CONNECTOR_COMPONENT_CACHE/traefik/bin/traefik`.
Downloads are disabled unless explicit `ALLOW_RUNTIME_DOWNLOADS=1` prepare
execution verifies the pinned SHA256, extracts only the `traefik` binary, and
writes only to the local component cache:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-traefik-runtime
make smoke-traefik
```

## Current Traefik Evidence

- Metadata build starter: PASS for metadata compile smoke.
- Decision-service starter build: PASS for local compile smoke.
- Decision-service self-test: PASS for in-memory allow/block decisions.
- Connector service: C17 compile/link target with explicit local libmodsecurity
  include and library paths.
- Config load: `make -C connectors/traefik check-config` invokes
  `--check-config` on the built service.
- Start smoke: `make -C connectors/traefik start-smoke` invokes `--serve`, starts
  real Traefik with a temporary forwardAuth File Provider config, verifies both
  process lifecycles, and cleans up without sending requests.
- Connector runtime: `make -C connectors/traefik runtime-smoke` requires a real
  Traefik -> forwardAuth -> Common runtime path with allowed 200 and blocked 403.
- Request-body compatibility probe: conditional via
  `make smoke-traefik-request-body`; it uses a separate generated middleware
  configuration with `forwardBody` enabled. It is not canonical No-CRS
  evidence for the checked-in `request_body_mode=none` path.
- Minimal CRS smoke: conditional via `make smoke-traefik-crs`; PASS only with
  local CRS and CRS-backed 403 evidence.
- Secondary CRS smoke: conditional via `make smoke-traefik-crs-secondary`; PASS
  only with local CRS and secondary CRS-backed 403 evidence.
- CRS complete: not claimed.
- RESPONSE_BODY: not verified.
- Negative/pass-through: proven only by local runtime smoke when allowed request
  returns 200.
- Audit/log: not verified.

Framework-owned paths and targets for future validation:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

The local decision-service self-test remains non-runtime evidence. The real
service source and local targeted smoke still do not establish production,
full-matrix, CRS-complete, response-body, or retained CI verification.

## Connector-Owned Service Entry Points

```sh
make -C connectors/traefik build-connector
make -C connectors/traefik check-config
make -C connectors/traefik start-smoke
make -C connectors/traefik runtime-smoke
```

These stages do not invoke each other implicitly. The runtime harness writes
temporary concrete service and Traefik File Provider configurations outside the
checkout and cleans up every process. Missing pre-run local executables are
BLOCKED/77; resolved config, startup, mapping, or status errors are FAIL.

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
`connectors/traefik/harness/run_traefik_smoke.sh` resolves `TRAEFIK_BIN` or
local common.sh-managed cache artifacts through the shared helpers. If a local
Traefik binary is found, the runner sends one allowed request and one blocked
request through Traefik and records the observed HTTP statuses. If no local
binary is found, it exits 77 with BLOCKED evidence.

This entrypoint does not run decision-service starter self-tests as runtime
evidence. RESPONSE_BODY remains not verified.

The optional targeted ModSecurity backend uses the same runtime entrypoint with
an explicit backend selector:

```sh
DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-modsecurity
```

This mode loads `common/rules/modsecurity_targeted_smoke.conf` through a local
libmodsecurity C-API evaluator. The allowed request must return 200 and the
request with `X-Modsec-Smoke: block` must return 403 from rule `1000001`.
`result.json` adds `decision_backend`, `modsecurity_backend_verified`,
`modsecurity_rule_file`, `modsecurity_rule_id`, `modsecurity_rule_loaded`,
`intervention_status`, and `decision_log_path`. Missing local libmodsecurity
headers/libraries are reported as Exit 77/BLOCKED, not as failure or success.

The legacy request-body capability probe uses the same Traefik `forwardAuth`
architecture, but not the canonical checked-in configuration: it creates a
separate local middleware with `forwardBody` enabled and selects the
request-body smoke case:

```sh
MODSECURITY_SMOKE_CASE=request_body DECISION_BACKEND=libmodsecurity make smoke-traefik
make smoke-traefik-request-body
make smoke-open-connectors-request-body
```

This mode loads `common/rules/modsecurity_request_body_smoke.conf`, sends POST
requests with `Content-Type: application/x-www-form-urlencoded`, and requires
the blocked body marker `modsec-request-body-block` to return 403 from rule
`1000002`. Successful evidence writes
`$TRAEFIK_RESULT_ROOT/request-body-result.json`,
`$TRAEFIK_LOG_ROOT/request-body-decision.log`, and
`$TRAEFIK_LOG_ROOT/request-body-request-transcript.jsonl`. It may set
`request_body_smoke_verified` for that isolated compatibility run; the
canonical No-CRS writer does not import that flag and keeps
`request_body_verified=false`. `response_body_verified` remains false.

The minimal CRS smoke uses the same runtime entrypoint with CRS selected:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-traefik
make smoke-traefik-crs
make smoke-traefik-crs-secondary
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

This mode loads CRS from common.sh-managed local paths, writes the generated
CRS smoke config under `$TRAEFIK_RESULT_ROOT/crs-smoke`, and records
CRS-specific evidence in `$TRAEFIK_RESULT_ROOT/crs-result.json` and
`$TRAEFIK_LOG_ROOT/crs-decision.log`. The allowed request must return 200. The
blocked request uses `/?id=1%20UNION%20SELECT%20password%20FROM%20users` and
must return 403 from CRS, not from rule `1000001`.

The secondary CRS smoke uses the same runner with `CRS_SMOKE_CASE=secondary`.
It writes generated config under `$TRAEFIK_RESULT_ROOT/crs-secondary-smoke`,
records `$TRAEFIK_RESULT_ROOT/crs-secondary-result.json`,
`$TRAEFIK_LOG_ROOT/crs-secondary-decision.log`, and
`$TRAEFIK_LOG_ROOT/crs-secondary-audit.log`, and sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`. A PASS requires HTTP 200 for the
allowed request, HTTP 403 for the secondary probe, and an actual CRS rule
ID/message extracted from evidence. If CRS, libmodsecurity, and Traefik are
available but the secondary probe is not blocked, the result is FAIL.

## Runtime status distinction

Connector metadata remains `runtime_status: not_verified` and `verification_status: connector-gap`. Generated per-run `result.json` files may differ: local starter-smoke PASS can report `runtime_verified: true` and `runtime_status: verified`; no-local-binary or missing runtime cases can report `status: BLOCKED`, `runtime_verified: false`, and `runtime_status: blocked`. These per-run fields do not mean production, CRS, RESPONSE_BODY, or full-matrix verification.

## Common Result Schema

`make smoke-traefik` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`request_body_smoke_verified`, `request_body_access_enabled`,
`request_body_rule_file`, `request_body_rule_id`, `request_method`,
`blocked_body_marker`, `evidence_root`, `timestamp`, `skipped_reason`,
`missing_dependencies`, and `claims_not_allowed`.

Current expected result without a local binary:

- Integration mode: `forwardAuth`
- Status: `BLOCKED`
- Exit code: 77
- Runtime status: generated no-local-binary or missing-runtime `result.json` files may report `runtime_status: blocked`; connector metadata remains `runtime_status: not_verified` and `verification_status: connector-gap`.
- Evidence root: `$VERIFIED_RUN_ROOT/traefik-smoke/`, falling back to
  `$BUILD_ROOT/results/traefik-smoke/`
- Binary environment variable: `TRAEFIK_BIN`
- Local search paths: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
  `$SOURCE_ROOT`, all provided by `common.sh`
- Missing dependencies when no local binary is found: `["traefik"]`
- skipped_reason when no local binary is found:
  `traefik runtime dependency not available in local common.sh-managed paths`
- For BLOCKED evidence, `runtime_verified`, `production_ready`,
  `full_matrix_ready`, `crs_complete`, and `response_body_verified` all remain
  false.

Expected PASS result with a local binary:

- Runtime status: generated local starter PASS `result.json` files may use `runtime_verified: true` and `runtime_status: verified` for that single local starter execution; connector metadata remains `runtime_status: not_verified` and `verification_status: connector-gap` until real Traefik connector runtime evidence exists.
- Allowed request status: `200`
- Blocked request status: `403`
- Resolved runtime binary: local path from `TRAEFIK_BIN` or a common.sh-managed
  lookup root
- `production_ready`, `full_matrix_ready`, `crs_complete`, and
  `response_body_verified` remain false.
- This local starter PASS status is not production, CRS, RESPONSE_BODY, or full-matrix verification.

Expected targeted ModSecurity PASS result with local Traefik and local
libmodsecurity:

- Decision backend: `libmodsecurity`
- ModSecurity backend verified: `true`
- ModSecurity rule file: `common/rules/modsecurity_targeted_smoke.conf`
- ModSecurity rule ID: `1000001`
- ModSecurity rule loaded: `true`
- Intervention status: `403`
- Decision log path: `$TRAEFIK_LOG_ROOT/modsecurity-decision.log`
- `production_ready`, `full_matrix_ready`, `crs_complete`, and
  `response_body_verified` remain false.
- This local starter PASS status is not production, CRS, RESPONSE_BODY, or full-matrix verification.

Expected legacy request-body capability-probe PASS result with local Traefik
and local libmodsecurity (not canonical No-CRS evidence):

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
- `production_ready`, `full_matrix_ready`, `crs_complete`, and
  `response_body_verified` remain false.

Expected minimal CRS PASS result with local Traefik, local libmodsecurity, and
local CRS:

- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- CRS version/ref: from common.sh-managed CRS source, for example `v4.26.0`
- CRS runtime dir: `$TRAEFIK_RESULT_ROOT/crs-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: from libmodsecurity intervention evidence
- `crs_minimal_smoke_verified=true`
- `production_ready`, `full_matrix_ready`, `crs_complete`, and
  `response_body_verified` remain false.

Expected secondary CRS PASS result with local Traefik, local libmodsecurity,
and local CRS:

- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- CRS smoke case: `secondary`
- CRS runtime dir: `$TRAEFIK_RESULT_ROOT/crs-secondary-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: extracted from audit/intervention evidence
- `crs_secondary_smoke_verified=true`
- `production_ready`, `full_matrix_ready`, `crs_complete`, and
  `response_body_verified` remain false.

No global installation is attempted. To run against a prepared local binary:

```sh
TRAEFIK_BIN=/lokaler/pfad/traefik make smoke-traefik
```
