# HAProxy Connector

Status: live-yaml-spoa-runtime (partial)
Runtime status: live request-side YAML execution through HAProxy, SPOA/SPOP,
and libmodsecurity. Current evidence:
No-CRS `46 PASS / 0 FAIL / 8 BLOCKED`; With-CRS
`48 PASS / 0 FAIL / 7 BLOCKED`.
Template alignment: scaffold-aligned plus local SPOA agent starter/runtime

This connector contains repository-owned metadata, a local HAProxy SPOA agent
starter, a request-side SPOP runtime, and a local libmodsecurity binding. The
runtime self-tests HELLO/AGENT-HELLO, NOTIFY parsing, verified
`set-var txn.modsecdiag.blocked true` ACK encoding, and DISCONNECT handling.
`make smoke-haproxy` now lists shared framework YAML cases with `case_cli.py`,
materializes each case, starts HAProxy plus the SPOP runtime plus a backend,
sends the case request with curl, asserts the observed status, and writes the
standard HAProxy summary artifacts.

`make runtime-matrix-haproxy` consumes live summary evidence from the split
No-CRS and With-CRS HAProxy runs. The current combined artifact is copied from
the With-CRS run and records `48 PASS`, `0 FAIL`, and `7 BLOCKED` across 55
shared executable YAML rows. The No-CRS split records `46 PASS`, `0 FAIL`, and
`8 BLOCKED`. Split artifacts are written under
`/src/ModSecurity-conector-build/results/no-crs/` and
`/src/ModSecurity-conector-build/results/with-crs/`.

The proven request-side variables are `REQUEST_URI`, `REQUEST_HEADERS`,
`REQUEST_HEADERS_NAMES`, `ARGS`, `ARGS_NAMES`, `REQUEST_COOKIES`,
`REQUEST_COOKIES_NAMES`, `REQUEST_BODY`, `FILES`, and `XML`. URL-encoded,
JSON, XML, multipart, and CRS SQLi anomaly request-body coverage is live
evidence, limited by the current single-frame SPOE path (`max-frame-size 65532`
and HAProxy `tune.bufsize 65536`). Response phases, audit-log assertions,
redirects, and non-403 disruptive statuses remain blocked unless live HAProxy
support is added and proven. `RESPONSE_BODY` is not promoted.

## Global Contract

See:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`

Shared connector-neutral data shapes used by the starter:

- `common/include/msconnector/origin.h`
- `common/include/msconnector/request.h`
- `common/include/msconnector/intervention.h`
- `common/include/msconnector/status.h`
- `common/src/intervention.c`

## HAProxy-specific State

- Origin/license: documented for repo-authored starter only; upstream HAProxy
  connector source is not selected.
- Metadata: `metadata.c` and `metadata.h` present.
- Build: metadata object and local SPOA agent starter build are present.
- Self-test: local starter self-test exists; it does not start HAProxy.
- SPOP runtime: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-spoa-runtime/`; request-side runtime
  evidence exists, but this is still not a complete production SPOA agent.
- ModSecurity binding self-test: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-modsecurity-binding/`; verifies
  phase-1 header blocking and request-body append/processing in process.
- Harness: `make smoke-haproxy` verifies live HAProxy to SPOA/SPOP to
  libmodsecurity enforcement for shared framework YAML request-side cases.
- No-CRS HAProxy split: 46 PASS, 0 FAIL, 8 BLOCKED.
- With-CRS HAProxy split: 48 PASS, 0 FAIL, 7 BLOCKED, including
  `crs_sqli_anomaly_block`.
- Combined HAProxy artifact: 48 PASS, 0 FAIL, 7 BLOCKED from the With-CRS
  live summary.
- RESPONSE_BODY blocking: not verified.

## Build Starter

For the complete repository-supported HAProxy compile and local verification
flow, see the root guide: [`COMPILE_HAPROXY.md`](../../COMPILE_HAPROXY.md).
The connector-local notes below describe status and target scope only.

Supported local build targets:

```sh
make -C connectors/haproxy build-metadata
make -C connectors/haproxy build-spoa-starter
make -C connectors/haproxy build-starter
make -C connectors/haproxy self-test-spoa
make -C connectors/haproxy self-test
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-spoa-runtime
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-modsecurity-binding-crs
```

`build-spoa-starter` compiles a local binary that can describe its limitations
and run a synthetic allow/block decision self-test. It does not compile HAProxy,
does not compile a HAProxy module, does not parse SPOP frames, does not run as a
verified SPOA server, and does not link libmodsecurity.

`build-spoa-runtime` compiles the request-side SPOP runtime. Its self-test is
protocol diagnostic evidence; `make smoke-haproxy` is the live gate that starts
HAProxy against this runtime and executes framework YAML cases.

`build-modsecurity-binding` first verifies the local libmodsecurity C API
signatures through a compiled probe, then builds a small self-test binary.
`self-test-modsecurity-binding` proves in-process phase-1 header blocking and
request-body processing. `make smoke-haproxy` is required for live HAProxy
runtime evidence.

## Tests

No local `connectors/haproxy/tests` folder is used. Executable runtime tests are
framework-owned.

Framework-owned paths and targets to use for future evidence:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make runtime-matrix-haproxy`
- `make test-haproxy-no-crs`
- `make test-haproxy-with-crs`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

Unsupported or currently unmaterializable rows are documented as BLOCKED or
NOT_EXECUTABLE. Response phases, audit/log assertions, redirects,
non-403 disruptive statuses, and `RESPONSE_BODY` remain unverified until live
HAProxy evidence exists for those exact scopes.
