# HAProxy Validation

Status: production-spoa-runtime (partial)
Runtime status: live YAML execution through HAProxy, SPOA/SPOP, and
libmodsecurity using `haproxy-modsecurity-spoa`.

`make smoke-haproxy` verifies shared framework YAML cases by materializing each
case, starting HAProxy, the production SPOA agent, and a backend, sending the
case request through HAProxy, and asserting the observed status. CRS is verified
by the With-CRS `crs_sqli_anomaly_block` case. Response headers and audit-log
assertions execute live through the production path. Bounded Phase 4 response
body probes execute only as experimental/non-promoted evidence.

`make runtime-matrix-haproxy` records HAProxy rows from live summary evidence
instead of fabricated diagnostic rows. PASS/FAIL is used only for live HAProxy
execution. Generated artifacts may differ by environment and case inventory;
the rule is that no HAProxy PASS/FAIL may be fabricated from synthetic matrix
writers.

The complete local compile and verification flow is documented in the root
guide: [`COMPILE_HAPROXY.md`](../../../COMPILE_HAPROXY.md).

Global runtime rules and promotion gates are defined in:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

## Current HAProxy Validation Status

- Metadata build-starter: buildable as a compile-time object target.
- SPOA agent starter: buildable as a local binary with local self-test.
- Productive adapter build: `haproxy-modsecurity-spoa`.
- HAProxy runtime harness: verifies shared YAML cases through the production
  SPOA agent.
- HAProxy binary: locally prepared under
  `/src/ModSecurity-conector-build/haproxy-runtime/haproxy/sbin/haproxy`.
- HAProxy source/binary acquisition: defined only in framework `common.sh`;
  HAProxy `3.2.19` official checksum and `TARGET=linux-glibc` support were
  verified before pinning.
- SPOP runtime: protocol self-test passes; live validation comes from
  `make smoke-haproxy`.
- SPOE/HAProxy config: generated under
  `/src/ModSecurity-conector-build/haproxy-runtime/spoe/` and syntax-valid by
  `haproxy -c`.
- SPOE runtime: `make smoke-haproxy` live-starts HAProxy, the SPOP runtime,
  and a local backend; fresh per-case evidence sets runtime status to live
  request-side verified for PASS/FAIL rows.
- ModSecurity binding: live enforcement verified for materialized YAML rules;
  standalone self-tests verify in-process transactions.
- HAProxy enforcement path for ModSecurity decisions: fixed status deny rules,
  request redirects where HAProxy syntax supports them, and silent-drop are
  driven by typed `txn.modsec.*` variables.
- Framework case runtime: rows without live HAProxy evidence are not promoted.
- No-CRS matrix artifact from the latest local run: 54 PASS, 0 FAIL,
  0 BLOCKED, 0 NOT_EXECUTABLE.
- With-CRS matrix artifact from the latest local run: 55 PASS, 0 FAIL,
  0 BLOCKED, 0 NOT_EXECUTABLE, including
  `crs_sqli_anomaly_block` with CRS loaded from
  `/src/ModSecurity-conector-build/crs/modsecurity-crs-preamble.conf`.
- Verified request-side variables: `REQUEST_URI`, `REQUEST_HEADERS`,
  `REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
  `REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`.
- Request-body/frame limit: HAProxy request buffering with
  `tune.bufsize 65536`, SPOE `max-frame-size 65532`, and one `req.body`
  argument. Larger, streamed, or multi-frame request bodies are not proven.
- CRS verified: true for the live With-CRS `crs_sqli_anomaly_block`.
- RESPONSE_BODY: bounded experimental execution only; not verified/promoted as
  full-body support.
- Negative/pass-through: verified for live request-side clean probes.
- Audit/log: live audit assertions use real libmodsecurity audit output.

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

## Remaining Risks

`connectors/haproxy/harness/run_haproxy_smoke.sh` exists as a live per-YAML
runtime entrypoint. The local starter self-test remains synthetic in-process
request-decision logic only.

A future broader harness must prove arbitrary dynamic status/redirect behavior,
long-running transaction cache pressure, multi-worker behavior, and full-body
response buffering before this connector can be promoted beyond partial status.

HAProxy cannot promote `RESPONSE_BODY` without full-body guarantees beyond the
current bounded `wait-for-body`/SPOE-frame/timeout evidence.

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
Evidence is written under `/src/ModSecurity-conector-build/results/`.

The entrypoint may prepare the local HAProxy binary first; that is preparation
evidence only. It may also run the SPOP runtime self-test, generate SPOE config
that is syntax-valid under `haproxy -c`, prove fresh HAProxy-to-SPOP-runtime
NOTIFY/contact, run libmodsecurity live, send typed set-var ACK variables, and
verify the YAML expected status. For With-CRS it loads the prepared CRS preamble
and records CRS decision evidence for the SQLi case. RESPONSE_BODY remains
non-promoted.
