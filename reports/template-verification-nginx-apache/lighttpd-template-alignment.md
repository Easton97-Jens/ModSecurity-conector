# lighttpd Template Alignment

**Language:** English | [Deutsch](lighttpd-template-alignment.de.md)

Status: bridge-starter
Runtime status: not-verified
Template alignment: bridge-starter, not runtime-verified

The lighttpd connector now has a repository-owned decision-service bridge
starter. It compiles and self-tests local probe flow against connector-neutral
`common/` helpers, but it is not a runtime adapter implementation.

No local `connectors/lighttpd/tests` folder is used. No runtime claims are made.
Executable tests remain framework-owned in
`modules/ModSecurity-test-Framework/tests/cases/` and use shared runners such as
`modules/ModSecurity-test-Framework/tests/runners/case_cli.py` when a real
lighttpd build and harness exist.

## Starter Scope

| Item | Status |
| --- | --- |
| `ORIGIN.md` | present for repo-owned bridge starter; no upstream source imported |
| `SOURCE_MAP.json` | present for repo-owned bridge starter |
| `metadata.c` / `metadata.h` | present |
| `src/lighttpd_build_starter.c` | present; compile-time probe only |
| `src/lighttpd_bridge.*` | present; local decision-service bridge starter only |
| `build/build_starter.sh` | present; compiles the metadata/probe starter |
| `build/bridge_starter.sh` | present; compiles and self-tests the bridge starter |
| `Makefile` starter targets | present |
| lighttpd API usage | none |
| FastCGI/SCGI protocol implementation | none |
| ModSecurity API usage | none |
| runtime harness | blocked entrypoint only |

## Phase Matrix

| Phase | lighttpd status | Notes |
| --- | --- | --- |
| Phase 0 Scaffold | OK | Scaffold files are present. |
| Phase 1 Origin/Metadata | bridge-starter documented | No upstream lighttpd source imported; metadata records bridge-starter status. |
| Phase 2 Build | bridge-starter | Compile/self-test checks exist for local starter source only. |
| Phase 3 Harness | blocked entrypoint only | Connector-side runtime-smoke script writes BLOCKED evidence only. |
| Phase 4 No-CRS | not-run | No lighttpd No-CRS runtime evidence. |
| Phase 5 With-CRS | not-run | No lighttpd With-CRS runtime evidence. |
| Phase 6 Coverage Matrix | bridge-starter documented | lighttpd matrix references the global matrix. |
| Phase 7 RESPONSE_BODY | not-verified | No lighttpd response-body blocking evidence. |
| Phase 8 Negative/pass-through | not-verified | No lighttpd negative/pass-through evidence. |
| Phase 9 Audit/log | not-verified | No lighttpd audit/log evidence. |
| Phase 10 Promotion | not allowed beyond bridge-starter/partial | Missing adapter and runtime evidence blocks promotion. |

## Last Local Starter Checks

`connectors/lighttpd/build/build_starter.sh`,
`make -C connectors/lighttpd build-bridge-starter`, and
`make -C connectors/lighttpd self-test-bridge` passed for local compile/self-test
checks. This does not prove lighttpd adapter or runtime behavior; the bridge
probe itself reports the local decision as blocked/not-verified.

## Blocked Dependencies

A real build/runtime path remains blocked until a selected production
integration path has repository-backed dependencies: lighttpd headers/SDK/source
or FastCGI/SCGI/bridge implementation, build flags, ModSecurity integration
code, a real lighttpd runtime harness, and framework-owned No-CRS/With-CRS
evidence.

## Decision

lighttpd is bridge-starter only. It must not be rated as adapter-owned,
runtime-smoke-verified, crs-verified, or more than partial until per-connector
origin/metadata, real adapter build, harness, No-CRS, With-CRS, coverage,
RESPONSE_BODY, negative/pass-through, and audit/log evidence is documented.

## Framework Starter Evidence

`make connector-starter-checks` records lighttpd starter results in
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` and
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Those records are connector-starter evidence only and keep
`runtime_verified: false`, `runtime_status: not-verified`, and
`response_body_verified: false`.

## Runtime-Smoke Entry Point

`make smoke-lighttpd` now invokes the framework-owned lighttpd runtime-smoke
runner, which dispatches to
`connectors/lighttpd/harness/run_lighttpd_smoke.sh`. Current status is BLOCKED
because that connector-side entrypoint only writes diagnostic evidence and no
real lighttpd server/config/runtime harness exists. Runtime remains not verified
and RESPONSE_BODY remains not verified.
