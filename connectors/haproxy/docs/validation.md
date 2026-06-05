# HAProxy Validation

Status: spoa-agent-starter
Runtime status: not-verified

HAProxy runtime validation is not run. No runtime result is claimed.
`make smoke-haproxy` performs prerequisite diagnostics and currently remains
BLOCKED.

Global runtime rules and promotion gates are defined in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Current HAProxy Validation Status

- Metadata build-starter: buildable as a compile-time object target.
- SPOA agent starter: buildable as a local binary with local self-test.
- Productive adapter build: BLOCKED.
- HAProxy runtime harness: blocked prerequisite-diagnostic entrypoint only.
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
  `diagnostic-handshake-verified`.
- ModSecurity binding: missing.
- No-CRS: not run.
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

`connectors/haproxy/harness/run_haproxy_smoke.sh` exists as a blocked
runtime-smoke entrypoint with prerequisite diagnostics. The local self-test runs
only synthetic in-process request-decision logic.

A future harness must provide HAProxy binary/container/source-build evidence,
HAProxy config, SPOE/SPOA config, agent endpoint, ModSecurity integration point
evidence, result JSON, and PASS/FAIL/BLOCKED counts.

HAProxy cannot be promoted beyond spoa-agent-starter or partial status without
recorded runtime evidence.

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
The current result is BLOCKED because the connector-side entrypoint writes
diagnostic evidence and no real HAProxy to SPOA to ModSecurity Framework-case
runtime exists. Evidence is written under `/src/ModSecurity-conector-build/results/`
with `blocked_reasons` for the remaining runtime prerequisites.

The entrypoint may prepare the local HAProxy binary first; that is preparation
evidence only. It may also run the minimal diagnostic SPOP handshake subset
self-test, generate SPOE config that is syntax-valid under `haproxy -c`, and
prove fresh HAProxy-to-diagnostic-agent contact. Those are diagnostic signals
only. Runtime remains blocked because no ModSecurity transaction is executed,
and RESPONSE_BODY remains not verified.
