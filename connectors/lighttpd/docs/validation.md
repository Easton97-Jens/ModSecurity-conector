# lighttpd Validation

Status: bridge-starter plus sidecar_proxy runtime-smoke path
Runtime status: locally verifiable with a staged lighttpd binary

The lighttpd metadata/probe and bridge starter can be compile-checked and
self-tested locally. Lighttpd Phase 1 runtime validation is available through
the sidecar_proxy smoke and the targeted libmodsecurity-backed smoke.

Runtime component metadata is pinned centrally in `common.sh`:
`LIGHTTPD_VERSION=1.4.84`, `LIGHTTPD_SOURCE_URL`, `LIGHTTPD_LATEST_URL`,
`LIGHTTPD_DOWNLOAD_URL`,
`LIGHTTPD_SHA256_URL`, and `LIGHTTPD_SHA256`. The expected local binary remains
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd`. Downloads are disabled
unless explicit `ALLOW_RUNTIME_DOWNLOADS=1` prepare execution verifies the
pinned source tarball SHA256 and writes source to the local component cache.
The local build is also opt-in and writes only under
`$CONNECTOR_COMPONENT_CACHE/lighttpd`:

```sh
ALLOW_RUNTIME_DOWNLOADS=1 ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_DOWNLOADS=1 make prepare-lighttpd-runtime
ALLOW_RUNTIME_BUILDS=1 make prepare-lighttpd-runtime-build
make smoke-lighttpd
```

Source staging is not runtime readiness. A local lighttpd binary must be
available through `LIGHTTPD_BIN` or the common.sh-managed component cache before
runtime verification is possible. The Phase 1 integration mode is
`sidecar_proxy`: the smoke starts real local lighttpd, verifies direct upstream
HTTP 200, then sends allowed and blocked requests through the sidecar proxy.

The optional targeted libmodsecurity-backed smoke is enabled for lighttpd:

```sh
DECISION_BACKEND=libmodsecurity make smoke-lighttpd
make smoke-lighttpd-modsecurity
```

This mode requires local common.sh-managed libmodsecurity headers and libraries.
It may set `modsecurity_backend_verified=true` only when rule `1000001` returns
a 403 intervention for `X-Modsec-Smoke: block`. No fake binary, fake sidecar
success, CRS claim, production claim, or response-body claim is allowed.

| Area | lighttpd status |
| --- | --- |
| Metadata/build-starter compile | PASS via `connectors/lighttpd/build/build_starter.sh` |
| Bridge-starter compile | PASS via `make -C connectors/lighttpd build-bridge-starter` |
| Bridge-starter self-test | PASS via `make -C connectors/lighttpd self-test-bridge` |
| Native lighttpd module build | blocked |
| FastCGI implementation | blocked |
| SCGI implementation | blocked |
| Runtime harness | sidecar_proxy smoke available with local binary |
| Targeted libmodsecurity smoke | PASS when local common.sh-managed libmodsecurity is available |
| Minimal CRS smoke | PASS when local common.sh-managed CRS and libmodsecurity are available |
| Secondary CRS smoke | PASS when local common.sh-managed CRS and libmodsecurity block the secondary probe |
| CRS complete | not claimed |
| RESPONSE_BODY | not verified |
| Negative/pass-through | not verified |
| Audit/log | not verified |

Executable tests are framework-owned and must use shared paths when a real
lighttpd build and harness exist:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/cases/connector-specific/lighttpd/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Starter PASS does not count as runtime evidence. lighttpd cannot be promoted
beyond bridge-starter/partial without repository-backed runtime evidence and
PASS/FAIL/BLOCKED counts for its own real-world connector path.

## Framework-Owned Starter Evidence

`make connector-starter-checks` runs lighttpd build-starter, bridge-starter, and
bridge self-test checks from
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
Results are written to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

The lighttpd entries are connector-starter build/self-test evidence only:
`runtime_verified` is `false`, `runtime_status` is `not-verified`, and
`response_body_verified` is `false`.

## Runtime-Smoke Entry Point

`make smoke-lighttpd` invokes the framework-owned lighttpd runtime-smoke runner.
When no local `lighttpd` binary is resolved, the result is BLOCKED with
`missing_dependencies=["lighttpd"]`. When a local binary is resolved, the runner
generates a minimal lighttpd config, starts lighttpd as the upstream server,
starts the local sidecar decision proxy, and requires HTTP 200 for an allowed
request plus HTTP 403 for `X-Modsec-Smoke: block`. Evidence is written under the
common.sh-managed lighttpd smoke root.

This entrypoint does not run bridge-starter scripts as runtime evidence.
RESPONSE_BODY remains not verified.

The minimal CRS smoke uses the same Phase 1 sidecar_proxy runtime entrypoint
with CRS selected:

```sh
DECISION_BACKEND=libmodsecurity MODSECURITY_RULESET=crs make smoke-lighttpd
make smoke-lighttpd-crs
make smoke-lighttpd-crs-secondary
make smoke-open-connectors-crs
make smoke-open-connectors-crs-secondary
```

This mode loads CRS from common.sh-managed local paths, writes the generated
CRS smoke config under `$LIGHTTPD_RESULT_ROOT/crs-smoke`, and records
CRS-specific evidence in `$LIGHTTPD_RESULT_ROOT/crs-result.json`,
`$LIGHTTPD_LOG_ROOT/crs-decision.log`, and
`$LIGHTTPD_LOG_ROOT/crs-request-transcript.jsonl`. The allowed request must
return 200 through the sidecar. The blocked request uses
`/?id=1%20UNION%20SELECT%20password%20FROM%20users` and must return 403 from
CRS, not from rule `1000001`.

The secondary CRS smoke uses the same Phase 1 `sidecar_proxy` runner with
`CRS_SMOKE_CASE=secondary`. It writes generated config under
`$LIGHTTPD_RESULT_ROOT/crs-secondary-smoke`, records
`$LIGHTTPD_RESULT_ROOT/crs-secondary-result.json`,
`$LIGHTTPD_LOG_ROOT/crs-secondary-decision.log`,
`$LIGHTTPD_LOG_ROOT/crs-secondary-audit.log`, and
`$LIGHTTPD_LOG_ROOT/crs-secondary-request-transcript.jsonl`, and sends
`/?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E`. A PASS requires HTTP 200 for the
allowed request, HTTP 403 for the secondary probe, and an actual CRS rule
ID/message extracted from evidence. If CRS, libmodsecurity, and Lighttpd are
available but the secondary probe is not blocked, the result is FAIL.

## Common Result Schema

`make smoke-lighttpd` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`evidence_root`, `timestamp`, `skipped_reason`, `missing_dependencies`, and
`claims_not_allowed`.

Current expected result without a local binary:

- Integration mode: `sidecar_proxy`
- Status: `BLOCKED`
- Exit code: 77
- Runtime verified: `false`
- Evidence root: `$VERIFIED_RUN_ROOT/lighttpd-smoke/`, falling back to
  `$BUILD_ROOT/results/lighttpd-smoke/`
- Binary environment variable: `LIGHTTPD_BIN`
- Local search paths: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
  `$SOURCE_ROOT`, all provided by `common.sh`
- Missing dependencies when no local binary is found: `["lighttpd"]`
- Architecture decision: Phase 1 selects sidecar_proxy after comparing native
  module, FastCGI/SCGI, sidecar/proxy, and mod_magnet/Lua
- Claims still forbidden from Lighttpd Phase 1 evidence:
  `production_ready=true`, `full_matrix_ready=true`, `crs_complete=true`,
  `response_body_verified=true`

Current expected result with a local binary and successful simple sidecar smoke:

- Integration mode: `sidecar_proxy`
- Status: `PASS`
- Exit code: 0
- Runtime verified: `true`
- `lighttpd_binary_verified=true`
- `lighttpd_http_verified=true`
- `sidecar_proxy_verified=true`
- Allowed request status: `200`
- Blocked request status: `403`
- `production_ready=false`, `full_matrix_ready=false`, `crs_complete=false`,
  and `response_body_verified=false`

Current expected result with a local binary and successful targeted
libmodsecurity smoke:

- Integration mode: `sidecar_proxy`
- Decision backend: `libmodsecurity`
- Status: `PASS`
- Exit code: `0`
- Runtime verified: `true`
- `lighttpd_binary_verified=true`
- `lighttpd_http_verified=true`
- `sidecar_proxy_verified=true`
- Rule file: `common/rules/modsecurity_targeted_smoke.conf`
- Rule ID: `1000001`
- Rule loaded: `true`
- Allowed request status: `200`
- Blocked request status: `403`
- Intervention status: `403`
- `modsecurity_backend_verified=true`
- `production_ready=false`, `full_matrix_ready=false`, `crs_complete=false`,
  and `response_body_verified=false`

Current expected result with a local binary and successful minimal CRS smoke:

- Integration mode: `sidecar_proxy`
- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- Runtime verified: `true`
- `lighttpd_binary_verified=true`
- `lighttpd_http_verified=true`
- `sidecar_proxy_verified=true`
- CRS version/ref: from common.sh-managed CRS source, for example `v4.26.0`
- CRS runtime dir: `$LIGHTTPD_RESULT_ROOT/crs-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: from libmodsecurity intervention evidence
- `crs_minimal_smoke_verified=true`
- `production_ready=false`, `full_matrix_ready=false`, `crs_complete=false`,
  and `response_body_verified=false`

Current expected result with a local binary and successful secondary CRS smoke:

- Integration mode: `sidecar_proxy`
- Decision backend: `libmodsecurity`
- Ruleset: `crs`
- CRS smoke case: `secondary`
- Runtime verified: `true`
- `lighttpd_binary_verified=true`
- `lighttpd_http_verified=true`
- `sidecar_proxy_verified=true`
- CRS runtime dir: `$LIGHTTPD_RESULT_ROOT/crs-secondary-smoke`
- Allowed request status: `200`
- Blocked request status: `403`
- Observed CRS rule ID/message: extracted from audit/intervention evidence
- `crs_secondary_smoke_verified=true`
- `production_ready=false`, `full_matrix_ready=false`, `crs_complete=false`,
  and `response_body_verified=false`

No global installation is attempted. To run against a prepared local binary:

```sh
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```
