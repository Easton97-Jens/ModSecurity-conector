# HAProxy Template Alignment

Status: spoa-agent-starter
Runtime status: not-verified
Template alignment: scaffold-aligned plus local SPOA agent starter

HAProxy is no longer only a metadata build-starter. It now has repo-authored
ORIGIN/SOURCE_MAP metadata and a compile-time local SPOA agent starter with a
local synthetic request-decision self-test. This is not a productive HAProxy
adapter and is not runtime verified.

## Claims Not Made

- No local `connectors/haproxy/tests` folder is used.
- No HAProxy API is used by the starter.
- No SPOP frame parser is present.
- No complete SPOE/SPOA protocol implementation is present.
- No libmodsecurity transaction binding is present.
- No HAProxy runtime PASS is claimed.
- No No-CRS result is claimed.
- No With-CRS result is claimed.
- No RESPONSE_BODY blocking result is claimed.
- No negative/pass-through result is claimed.
- No audit/log evidence is claimed.

## Shared Rules And Code Used

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`

## Starter Evidence

| Item | Status | Evidence |
| --- | --- | --- |
| Origin file | present | `connectors/haproxy/ORIGIN.md` |
| Source map | present | `connectors/haproxy/SOURCE_MAP.json` |
| Metadata source | present | `connectors/haproxy/metadata.c`, `connectors/haproxy/metadata.h` |
| Metadata build | PASS | `make -C connectors/haproxy build-metadata` |
| SPOA starter build | PASS | `make -C connectors/haproxy build-spoa-starter` |
| Local self-test | PASS | `make -C connectors/haproxy self-test-spoa` |
| Productive adapter build | BLOCKED | SPOP parser/library, HAProxy runtime harness, verified HAProxy config, libmodsecurity binding strategy, and runtime evidence not selected |
| Runtime prerequisite diagnostics | BLOCKED | `make smoke-haproxy` writes granular blocked reasons |

## Phase Matrix

| Phase | Area | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter; productive build BLOCKED |
| Phase 3 | Harness | blocked entrypoint only |
| Phase 4 | No-CRS | not-run |
| Phase 5 | With-CRS | not-run |
| Phase 6 | Coverage Matrix | spoa-agent-starter documented |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | not allowed |

## Framework Starter Evidence

`make connector-starter-checks` records HAProxy starter results in
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl` and
`/src/ModSecurity-conector-build/results/connector-starters/summary.json`.
Those records are connector-starter evidence only and keep
`runtime_verified: false`, `runtime_status: not-verified`, and
`response_body_verified: false`.

## Runtime-Smoke Entry Point

`make smoke-haproxy` now invokes the framework-owned HAProxy runtime-smoke
runner, which dispatches to `connectors/haproxy/harness/run_haproxy_smoke.sh`.
Current status is BLOCKED because that connector-side entrypoint only writes
diagnostic evidence and no real HAProxy server/config/SPOE runtime harness
exists. The recorded blockers are: missing HAProxy binary, no HAProxy
source/binary acquisition in framework `common.sh`, self-test-only SPOA starter,
example-only SPOE/HAProxy config, and missing ModSecurity binding. Runtime
remains not verified and RESPONSE_BODY remains not verified.
