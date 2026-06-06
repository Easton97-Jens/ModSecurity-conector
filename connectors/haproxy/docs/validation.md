# HAProxy Validation

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity.

`make smoke-haproxy` now verifies shared request-side framework YAML cases by
materializing each case, starting HAProxy, the SPOP runtime, and a backend,
sending the case request through HAProxy, and asserting the observed status.
CRS is verified by the With-CRS `crs_sqli_anomaly_block` case. Response
phases, audit-log assertions, redirects, non-403 disruptive statuses, and
`RESPONSE_BODY` remain not verified.

`make runtime-matrix-haproxy` now records HAProxy rows from live summary
evidence instead of fabricated diagnostic rows. The current No-CRS artifact
records `46 PASS`, `0 FAIL`, and `8 BLOCKED`; the current With-CRS and
combined artifacts record `48 PASS`, `0 FAIL`, and `7 BLOCKED`. PASS/FAIL is
used only for live HAProxy execution.

The complete local compile and verification flow is documented in the root
guide: [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md).

Global runtime rules and promotion gates are defined in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Current HAProxy Validation Status

- Metadata build-starter: buildable as a compile-time object target.
- SPOA agent starter: buildable as a local binary with local self-test.
- Productive adapter build: BLOCKED.
- HAProxy runtime harness: verifies shared request-side YAML cases.
- HAProxy binary: locally prepared under
  `/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy`.
- HAProxy source/binary acquisition: defined only in framework `common.sh`;
  HAProxy `3.2.19` official checksum and `TARGET=linux-glibc` support were
  verified before pinning.
- SPOP runtime: request-side SPOP subset self-test passes; this is not a full
  production SPOA agent implementation.
- SPOE/HAProxy config: generated under
  `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` and syntax-valid by
  `haproxy -c`.
- SPOE runtime: `make smoke-haproxy` live-starts HAProxy, the SPOP runtime,
  and a local backend; fresh per-case evidence sets runtime status to live
  request-side verified for PASS/FAIL rows.
- ModSecurity binding: live enforcement verified for materialized request-side
  YAML rules; standalone self-tests verify in-process transactions.
- HAProxy enforcement path for ModSecurity decisions: verified for 403
  disruptive decisions through `txn.modsecdiag.blocked` and HAProxy
  `http-request deny status 403`.
- Framework case runtime: rows without live HAProxy evidence are not promoted.
- No-CRS matrix artifact: 46 PASS, 0 FAIL, 8 BLOCKED.
- With-CRS matrix artifact: 48 PASS, 0 FAIL, 7 BLOCKED, including
  `crs_sqli_anomaly_block` with CRS loaded from
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- Verified request-side variables: `REQUEST_URI`, `REQUEST_HEADERS`,
  `REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
  `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`.
- Request-body/frame limit: HAProxy request buffering with
  `tune.bufsize 65536`, SPOE `max-frame-size 65532`, and one `req.body`
  argument. Larger, streamed, or multi-frame request bodies are not proven.
- CRS verified: true for the live With-CRS `crs_sqli_anomaly_block`.
- RESPONSE_BODY: not verified.
- Negative/pass-through: verified for live request-side clean probes.
- Audit/log: not verified.

Executable tests are framework-owned and must use evidence from paths such as:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`

Future HAProxy validation may reference these parent Make targets only after an
explicit HAProxy runtime scope exists and is executed:

- `make runtime-matrix-haproxy`
- `make test-haproxy-no-crs`
- `make test-haproxy-with-crs`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

## Remaining Blockers

`connectors/haproxy/harness/run_haproxy_smoke.sh` exists as a live per-YAML
request-side runtime entrypoint. The local starter self-test remains synthetic
in-process request-decision logic only.

A future broader harness must add response phase, audit/log assertion,
redirect, non-403 disruptive status, and `RESPONSE_BODY` evidence before this
connector can be promoted beyond partial request-side status.

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
The current result is 46 PASS / 0 FAIL / 8 BLOCKED for No-CRS and
48 PASS / 0 FAIL / 7 BLOCKED for With-CRS. Evidence is written under
`/src/ModSecurity-conector-build/results/`.

The entrypoint may prepare the local HAProxy binary first; that is preparation
evidence only. It may also run the SPOP runtime self-test, generate SPOE config
that is syntax-valid under `haproxy -c`, prove fresh HAProxy-to-SPOP-runtime
NOTIFY/contact, run libmodsecurity live, send the verified set-var ACK, and
verify the YAML expected status. For With-CRS it loads the prepared CRS preamble
and records CRS decision evidence for the SQLi case. RESPONSE_BODY remains not
verified.
