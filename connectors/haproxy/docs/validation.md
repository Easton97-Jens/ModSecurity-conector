# HAProxy Validation

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block`

`make smoke-haproxy` now verifies the narrow live HAProxy to diagnostic SPOA to
libmodsecurity case `haproxy_phase1_header_block`. CRS, RESPONSE_BODY,
negative/pass-through matrix coverage, and audit/log behavior remain not
verified.

Global runtime rules and promotion gates are defined in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Current HAProxy Validation Status

- Metadata build-starter: buildable as a compile-time object target.
- SPOA agent starter: buildable as a local binary with local self-test.
- Productive adapter build: BLOCKED.
- HAProxy runtime harness: verifies `haproxy_phase1_header_block` only.
- HAProxy binary: locally prepared under
  `/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy`.
- HAProxy source/binary acquisition: defined only in framework `common.sh`;
  HAProxy `3.2.19` official checksum and `TARGET=linux-glibc` support were
  verified before pinning.
- SPOA diagnostic runtime: minimal diagnostic SPOP handshake subset self-test
  passes; this is not a full SPOA agent implementation.
- SPOE/HAProxy config: generated under
  `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` and syntax-valid by
  `haproxy -c`.
- SPOE diagnostic runtime: `make smoke-haproxy` live-starts HAProxy, the
  diagnostic SPOP agent, and a local backend; fresh agent-log evidence after
  the run marker sets `spoe_runtime_status` to
  `diagnostic-enforcement-verified`.
- ModSecurity binding: live enforcement verified for the header-block smoke
  case; the standalone self-test still verifies only an in-process phase-1
  transaction.
- HAProxy enforcement path for ModSecurity decisions: verified only for
  `haproxy_phase1_header_block`.
- Framework case runtime for broader HAProxy to SPOA to ModSecurity coverage:
  missing.
- No-CRS minimal phase-1 runtime: PASS for `haproxy_phase1_header_block` only.
- Broader No-CRS matrix: not run.
- With-CRS: not run.
- RESPONSE_BODY: not verified.
- Negative/pass-through: not verified.
- Audit/log: not verified.

Executable tests are framework-owned and must use evidence from paths such as:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Future HAProxy validation may reference these parent Make targets only after an
explicit HAProxy runtime scope exists and is executed:

- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

## Harness Blocker

`connectors/haproxy/harness/run_haproxy_smoke.sh` exists as a runtime-smoke
entrypoint for the single `haproxy_phase1_header_block` case. The local starter
self-test remains synthetic in-process request-decision logic only.

A future broader harness must add No-CRS, With-CRS, RESPONSE_BODY,
negative/pass-through, and audit/log evidence before this connector can be
promoted beyond the current narrow runtime-smoke case.

HAProxy cannot be promoted beyond partial status without those broader recorded
runtime scopes.

## Framework-Owned Starter Evidence

`make connector-starter-checks` runs HAProxy metadata, SPOA starter build, and
SPOA self-test checks from
`modules/ModSecurity-test-Framework/ci/run-connector-starter-checks.sh`.
Results are written to
`/src/ModSecurity-conector-build/results/connector-starters/summary.json` and
`/src/ModSecurity-conector-build/results/connector-starters/results.jsonl`.

The HAProxy entries are connector-starter build/self-test evidence only:
`runtime_verified` is `false`, `runtime_status` is `not-verified`, and
`response_body_verified` is `false`.

## Runtime-Smoke Entry Point

`make smoke-haproxy` invokes the framework-owned HAProxy runtime-smoke runner.
The current result is PASS for `haproxy_phase1_header_block`. Evidence is
written under `/src/ModSecurity-conector-build/results/`.

The entrypoint may prepare the local HAProxy binary first; that is preparation
evidence only. It may also run the minimal diagnostic SPOP handshake subset
self-test, generate SPOE config that is syntax-valid under `haproxy -c`, prove
fresh HAProxy-to-diagnostic-agent NOTIFY/contact, run libmodsecurity live, send
the verified set-var ACK, and verify 403/200 probes. RESPONSE_BODY remains not
verified.
