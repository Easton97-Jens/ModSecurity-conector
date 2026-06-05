# HAProxy Connector

Status: spoa-agent-starter
Runtime status: not-verified
Template alignment: scaffold-aligned plus local SPOA agent starter

This connector now contains repository-owned metadata, a local HAProxy SPOA
agent starter, and a separate minimal diagnostic SPOP handshake subset. The
starter compiles and self-tests local request-decision logic, while the
diagnostic subset self-tests local HELLO/AGENT-HELLO, NOTIFY-to-empty-ACK, and
DISCONNECT handling. Neither path is a runtime-verified HAProxy adapter
implementation.

No productive HAProxy API integration, full SPOE/SPOA protocol implementation,
libmodsecurity transaction binding, runtime harness, or runtime compatibility is
claimed by this connector.

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
- Harness: blocked runtime-smoke entrypoint only.
- No-CRS runtime: not run.
- With-CRS runtime: not run.
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
```

`build-spoa-starter` compiles a local binary that can describe its limitations
and run a synthetic allow/block decision self-test. It does not compile HAProxy,
does not compile a HAProxy module, does not parse SPOP frames, does not run as a
verified SPOA server, and does not link libmodsecurity.

`build-spoa-runtime` compiles a minimal diagnostic SPOP handshake subset. Its
self-test is protocol diagnostic evidence only; it does not start HAProxy
against ModSecurity, load CRS, or verify RESPONSE_BODY behavior.

## Tests

No local `connectors/haproxy/tests` folder is used. Executable runtime tests are
framework-owned.

Framework-owned paths and targets to use for future evidence:

- `modules/ModSecurity-test-Framework/tests/cases/`
- `modules/ModSecurity-test-Framework/tests/runners/case_cli.py`
- `make test-no-crs`
- `make test-with-crs`
- `make smoke-common`

No No-CRS, With-CRS, RESPONSE_BODY, negative/pass-through, or audit/log runtime
result is claimed for HAProxy until those commands are executed for an explicit
HAProxy scope and their evidence paths are recorded.
