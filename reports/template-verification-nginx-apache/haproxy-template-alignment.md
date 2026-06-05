# HAProxy Template Alignment

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block`
Template alignment: scaffold-aligned plus local SPOA agent starter

HAProxy is no longer only a metadata build-starter. It now has repo-authored
ORIGIN/SOURCE_MAP metadata, a compile-time local SPOA agent starter with a
local synthetic request-decision self-test, and one verified live runtime-smoke
case. This is not a productive HAProxy adapter and is not CRS, RESPONSE_BODY,
or full-matrix verified.

## Claims Not Made

- No local `connectors/haproxy/tests` folder is used.
- No HAProxy API is used by the starter.
- Only a minimal diagnostic SPOP handshake subset is present.
- No complete SPOE/SPOA protocol implementation is present.
- HAProxy runtime PASS is claimed only for `haproxy_phase1_header_block`.
- No broader No-CRS matrix result is claimed beyond the minimal phase-1
  header-block smoke.
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
| Local HAProxy binary prepare | PASS | framework `ci/prepare-haproxy-runtime.sh` prepares HAProxy under `/src/ModSecurity-conector-build` |
| Diagnostic SPOP subset | PASS for diagnostic scope only | `make -C connectors/haproxy self-test-spoa-runtime` verifies a minimal diagnostic SPOP handshake subset |
| SPOE config syntax | syntax-valid | `make smoke-haproxy` generates config under `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` |
| Diagnostic HAProxy-to-agent runtime | diagnostic-enforcement-verified | fresh run-specific NOTIFY, arg extraction, ModSecurity 403, set-var ACK, block 403, and pass 200 evidence |
| ModSecurity binding | live-enforcement-verified | local libmodsecurity C API signatures verified; phase-1 header block enforced by HAProxy over SPOA |
| Productive adapter build | BLOCKED for broader adapter ownership | Full SPOA implementation and broader Framework-case runtime evidence missing |
| Runtime smoke | PASS for one case | `make smoke-haproxy` verifies `haproxy_phase1_header_block` |

## Phase Matrix

| Phase | Area | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter plus ModSecurity binding self-test; productive build BLOCKED |
| Phase 3 | Harness | PASS for `haproxy_phase1_header_block`; broader harness incomplete |
| Phase 4 | No-CRS | partial; header-block smoke only |
| Phase 5 | With-CRS | not-run |
| Phase 6 | Coverage Matrix | spoa-agent-starter documented |
| Phase 7 | RESPONSE_BODY | not-verified |
| Phase 8 | Negative/pass-through | not-verified |
| Phase 9 | Audit/log | not-verified |
| Phase 10 | Promotion | partial only |

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
Current status is PASS for the single `haproxy_phase1_header_block` smoke.
HAProxy `3.2.19` source acquisition is pinned only in framework `common.sh`;
the official checksum file and source Makefile support for
`TARGET=linux-glibc` were verified before the pin was added. The local HAProxy
binary can be prepared under
`/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy`.
`make smoke-haproxy` also verifies a minimal diagnostic SPOP handshake subset
and validates generated SPOE config syntax with `haproxy -c`. It live-starts
HAProxy, the diagnostic SPOP agent, and a local backend, then records
`spoe_config_status: syntax-valid`,
`spoe_runtime_status: diagnostic-enforcement-verified`,
`modsecurity_binding_status: live-enforcement-verified`,
`runtime_verified: true`, block-probe 403, and pass-probe 200. CRS,
RESPONSE_BODY, broader No-CRS/With-CRS, negative/pass-through, and audit/log
evidence remain not verified.
