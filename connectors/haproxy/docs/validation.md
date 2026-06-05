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
- HAProxy binary: missing from the local runtime environment.
- HAProxy source/binary acquisition: not defined in framework `common.sh`.
- SPOA runtime agent: missing; starter binary is self-test-only.
- SPOE/HAProxy config: example-only and not runtime-verified.
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
diagnostic evidence and no real HAProxy server/config/SPOE runtime harness
exists. Evidence is written under `/src/ModSecurity-conector-build/results/`
with `blocked_reasons` for the missing runtime prerequisites.

This entrypoint does not run the SPOA starter self-test as runtime evidence.
Runtime remains not verified and RESPONSE_BODY remains not verified.
