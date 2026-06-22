# lighttpd Validation

Status: bridge-starter
Runtime status: not-verified

The lighttpd metadata/probe and bridge starter can be compile-checked and
self-tested locally, but lighttpd runtime validation has not been run.

Runtime component metadata is pinned centrally in `common.sh`:
`LIGHTTPD_VERSION=1.4.84`, `LIGHTTPD_SOURCE_PAGE`,
`LIGHTTPD_LATEST_MARKER_URL`, `LIGHTTPD_DOWNLOAD_URL`,
`LIGHTTPD_SHA256_URL`, and `LIGHTTPD_SHA256`. The expected local binary remains
`$CONNECTOR_COMPONENT_CACHE/lighttpd/bin/lighttpd`. Downloads are disabled
unless future explicit `ALLOW_RUNTIME_DOWNLOADS=1` logic verifies the pinned
SHA256 and writes only to the local component cache. The pinned component does
not change the current BLOCKED runtime status; the integration mode still must
be implemented before runtime verification is possible.

| Area | lighttpd status |
| --- | --- |
| Metadata/build-starter compile | PASS via `connectors/lighttpd/build/build_starter.sh` |
| Bridge-starter compile | PASS via `make -C connectors/lighttpd build-bridge-starter` |
| Bridge-starter self-test | PASS via `make -C connectors/lighttpd self-test-bridge` |
| Native lighttpd module build | blocked |
| FastCGI implementation | blocked |
| SCGI implementation | blocked |
| Runtime harness | blocked entrypoint only |
| No-CRS | not run |
| With-CRS | not run |
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
The current result is BLOCKED because
`connectors/lighttpd/harness/run_lighttpd_smoke.sh` writes diagnostic evidence
and no real lighttpd server/config/runtime harness exists. Evidence is written
under `/src/ModSecurity-conector-build/results/`.

This entrypoint does not run bridge-starter scripts as runtime evidence.
Runtime remains not verified and RESPONSE_BODY remains not verified.

## Common Result Schema

`make smoke-lighttpd` now uses the shared smoke-result writer in
`common/scripts/write_smoke_result.py`. The generated `result.json` contains the
common schema fields `connector`, `integration_mode`, `runtime_verified`,
`full_matrix_ready`, `production_ready`, `crs_complete`,
`response_body_verified`, `allowed_request_status`, `blocked_request_status`,
`evidence_root`, `timestamp`, `skipped_reason`, `missing_dependencies`, and
`claims_not_allowed`.

Current expected result:

- Integration mode: `architecture_spike_plus_runtime_smoke`
- Status: `BLOCKED`
- Exit code: 77
- Runtime verified: `false`
- Evidence root: `$VERIFIED_RUN_ROOT/lighttpd-smoke/`, falling back to
  `$BUILD_ROOT/results/lighttpd-smoke/`
- Binary environment variable: `LIGHTTPD_BIN`
- Local search paths: `$CONNECTOR_COMPONENT_CACHE`, `$VERIFIED_COMPONENT_CACHE`,
  `$VERIFIED_BUILD_ROOT`, `$BUILD_ROOT`, `$VERIFIED_RUN_ROOT`, and
  `$SOURCE_ROOT`, all provided by `common.sh`
- skipped_reason while the integration path is open:
  `lighttpd integration mode not selected`
- Missing dependencies when no local binary is found: `["lighttpd"]`
- Architecture decision: compare native module, FastCGI/SCGI, sidecar/proxy,
  and mod_magnet/Lua before selecting the runtime path
- Recommended Phase 1 mode: sidecar/proxy, not yet runtime-implemented
- Claims still forbidden: `runtime_verified=true`, `production_ready=true`,
  `full_matrix_ready=true`, `crs_complete=true`, `response_body_verified=true`

No global installation is attempted. To run against a prepared local binary:

```sh
LIGHTTPD_BIN=/lokaler/pfad/lighttpd make smoke-lighttpd
```
