# HAProxy Connector

Status: spoa-agent-starter
Runtime status: runtime-smoke-verified for `haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block`
Template alignment: scaffold-aligned plus local SPOA agent starter

This connector now contains repository-owned metadata, a local HAProxy SPOA
agent starter, a separate minimal diagnostic SPOP handshake subset, and a local
libmodsecurity binding. The starter compiles and self-tests local
request-decision logic. The diagnostic runtime self-tests HELLO/AGENT-HELLO,
NOTIFY, verified `set-var txn.blocked true` ACK encoding, and DISCONNECT
handling, then `make smoke-haproxy` live-starts HAProxy and verifies the narrow
No-CRS `haproxy_phase1_header_block` and With-CRS
`haproxy_crs_sqli_anomaly_block` runtime-smoke cases.

No full SPOE/SPOA protocol implementation, CRS behavior beyond the single SQLi
anomaly smoke, RESPONSE_BODY handling, negative/pass-through matrix beyond the
clean probes, or productive adapter ownership is claimed by this connector.

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
- Diagnostic SPOP subset: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-spoa-runtime/`; not a full SPOA
  agent implementation.
- ModSecurity binding self-test: buildable and self-testable under
  `/src/ModSecurity-conector-build/haproxy-modsecurity-binding/`; verifies only
  local libmodsecurity phase-1 header blocking.
- Harness: `make smoke-haproxy` verifies live HAProxy to diagnostic SPOA to
  libmodsecurity enforcement for `haproxy_phase1_header_block` and
  `haproxy_crs_sqli_anomaly_block` only.
- No-CRS minimal phase-1 runtime: PASS for `haproxy_phase1_header_block` only.
- Broader No-CRS matrix: not run.
- With-CRS minimal SQLi runtime: PASS for `haproxy_crs_sqli_anomaly_block`
  with CRS loaded from the prepared preamble.
- Broader With-CRS matrix: not run.
- RESPONSE_BODY blocking: not verified.

## Build Starter

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

`build-spoa-runtime` compiles a minimal diagnostic SPOP handshake subset. Its
self-test is protocol diagnostic evidence only; `make smoke-haproxy` is the
runtime gate that starts HAProxy against this diagnostic agent.

`build-modsecurity-binding` first verifies the local libmodsecurity C API
signatures through a compiled probe, then builds a small self-test binary.
`self-test-modsecurity-binding` proves only an in-process phase-1 header block
decision with status 403. `make smoke-haproxy` is required to set
`runtime_verified: true`, and only for the live
`haproxy_phase1_header_block` and `haproxy_crs_sqli_anomaly_block` cases.

## Tests

No local `connectors/haproxy/tests` folder is used. Executable runtime tests are
framework-owned.

Framework-owned paths and targets to use for future evidence:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No broader No-CRS, broader With-CRS, RESPONSE_BODY, negative/pass-through, or
audit/log runtime result is claimed for HAProxy until those commands are
executed for an explicit HAProxy scope and their evidence paths are recorded.
