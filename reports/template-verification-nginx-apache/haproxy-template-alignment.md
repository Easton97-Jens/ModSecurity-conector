# HAProxy Template Alignment

**Language:** English | [Deutsch](haproxy-template-alignment.de.md)

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`
Template alignment: scaffold-aligned plus local SPOA agent starter

HAProxy is no longer only a metadata build-starter. It now has repo-authored
ORIGIN/SOURCE_MAP metadata, a compile-time local SPOA agent starter with a
local synthetic request-decision self-test, and two verified live runtime-smoke
cases. This is not a productive HAProxy adapter and is not broader CRS,
RESPONSE_BODY, or full-matrix verified.

The framework-owned HAProxy matrix target now records one row per existing
framework YAML case. The latest combined artifact attempted 141 YAML rows and
recorded 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, and 10 mapped-only
inventory entries. PASS is limited to the live With-CRS
`crs_sqli_anomaly_block` YAML case. The No-CRS
`haproxy_phase1_header_block` smoke remains a preserved diagnostic alias and is
not claimed as the framework `phase1_header_block` YAML row.

## Claims Not Made

- No local `connectors/haproxy/tests` folder is used.
- No HAProxy API is used by the starter.
- Only a minimal diagnostic SPOP handshake subset is present.
- No complete SPOE/SPOA protocol implementation is present.
- HAProxy runtime PASS is claimed only for `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block`.
- No broader No-CRS YAML PASS is claimed beyond the minimal phase-1 diagnostic
  header-block smoke alias.
- No broader With-CRS YAML PASS is claimed beyond `crs_sqli_anomaly_block`.
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
| Diagnostic HAProxy-to-agent runtime | diagnostic-enforcement-verified | fresh run-specific NOTIFY, arg extraction, ModSecurity 403, set-var ACK, block 403, and pass 200 evidence for No-CRS and With-CRS minimal scopes |
| ModSecurity binding | live-enforcement-verified | local libmodsecurity C API signatures verified; phase-1 header block and CRS SQLi anomaly decisions enforced by HAProxy over SPOA |
| Productive adapter build | BLOCKED for broader adapter ownership | Full SPOA implementation and live PASS/FAIL execution for currently BLOCKED framework rows are missing |
| Runtime smoke | PASS for two cases | `make smoke-haproxy` verifies `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block` |
| Combined matrix | partial | `make runtime-matrix-haproxy`; 141 YAML rows, 1 PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |
| No-CRS split matrix | partial | `make test-haproxy-no-crs`; 141 YAML rows, 0 YAML PASS, 0 FAIL, 59 BLOCKED, 82 NOT_EXECUTABLE, 10 MAPPED_ONLY; diagnostic alias preserved separately |
| With-CRS split matrix | partial | `make test-haproxy-with-crs`; 141 YAML rows, `crs_sqli_anomaly_block` PASS, 0 FAIL, 59 BLOCKED, 81 NOT_EXECUTABLE, 10 MAPPED_ONLY |

## Phase Matrix

| Phase | Area | HAProxy status |
| --- | --- | --- |
| Phase 0 | Scaffold | OK |
| Phase 1 | Origin/Metadata | spoa-agent-starter |
| Phase 2 | Build | spoa-agent-starter plus ModSecurity binding self-test; productive build BLOCKED |
| Phase 3 | Harness | PASS for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`; broader harness incomplete |
| Phase 4 | No-CRS | partial; diagnostic alias PASS, YAML rows otherwise BLOCKED/NOT_EXECUTABLE |
| Phase 5 | With-CRS | partial; `crs_sqli_anomaly_block` YAML PASS, other rows BLOCKED/NOT_EXECUTABLE |
| Phase 6 | Coverage Matrix | HAProxy generated beside Apache/NGINX; mapped-only inventory separate |
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
Current status is PASS for `haproxy_phase1_header_block` and
`haproxy_crs_sqli_anomaly_block`.
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
`runtime_verified: true`, block-probe 403, and pass-probe 200. The With-CRS
sub-scope records `crs_verified: true` only for
`haproxy_crs_sqli_anomaly_block`; the verified cases are scoped to
`haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`.
`make runtime-matrix-haproxy`, `make test-haproxy-no-crs`, and
`make test-haproxy-with-crs` write matrix evidence under
`/src/ModSecurity-conector-build/results/`, including split `no-crs/` and
`with-crs/` directories. RESPONSE_BODY, broader No-CRS/With-CRS live YAML
execution, negative/pass-through, audit/log, and full-matrix evidence remain
not verified.
