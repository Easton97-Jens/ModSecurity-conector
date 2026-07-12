# HAProxy Connector PoC

**Language:** English | [Deutsch](haproxy-poc.de.md)

Status: production SPOA runtime evidence for request phases and response
headers only; Phase 4 / RESPONSE_BODY is not canonical evidence

## Implemented

- `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c` builds the
  `haproxy-modsecurity-spoa` production SPOA/SPOP runtime.
- `connectors/haproxy/src/haproxy_modsecurity_binding.c` integrates the SPOA
  runtime with libmodsecurity.
- `connectors/haproxy/harness/run_haproxy_smoke.sh` starts HAProxy, the SPOA
  runtime, and a local backend, then records live runtime decisions.
- `modules/ModSecurity-test-Framework/ci/run-haproxy-runtime-matrix.sh` runs
  the no-CRS, with-CRS, and force-all evidence paths.
- Runtime evidence includes `decision.jsonl`, HAProxy logs, SPOA logs, audit
  logs when configured, JSONL case results, and generated summaries.

When the smoke passes it is a production-style connector validation:

```text
HTTP client -> HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity -> HAProxy response
```

There is no synthetic matrix writer. Generated reports consume live runtime
artifacts and the runtime validation snapshot.

## Build Flow

The local build keeps generated artifacts outside the checkout:

```bash
BUILD_ROOT=/src/ModSecurity-conector-build
SOURCE_ROOT=/src
make -C connectors/haproxy build-modsecurity-binding
make -C connectors/haproxy build-spoa-runtime
make -C connectors/haproxy self-test-modsecurity-binding
make -C connectors/haproxy self-test-spoa-runtime
```

The production SPOA binary is staged at:

```text
/src/ModSecurity-conector-build/haproxy-spoa-runtime/haproxy-modsecurity-spoa
```

The HAProxy runtime helper downloads, verifies, builds, and stages HAProxy
under `BUILD_ROOT` using source pins from
`modules/ModSecurity-test-Framework/ci/common.sh`.

## Runtime Smoke

Run default evidence:

```bash
make smoke-haproxy
make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

Current generated default status:

| Connector | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| HAProxy | 55 | 55 | 0 | 0 | 0 |

Default HAProxy evidence is the supported non-former-XFAIL subset of live
HAProxy matrix evidence. Former-XFAIL and broader rows remain separate runtime
evidence.

## Force-All Evidence

Run force-all evidence:

```bash
FORCE_ALL_CASES=1 make runtime-matrix-haproxy
make generate-test-matrix
make check-test-matrix
```

Current generated force-all status:

| Connector | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| HAProxy | 133 | 104 | 23 | 0 | 6 |

Force-all FAIL and NOT_EXECUTABLE rows stay in
`reports/testing/generated/runtime/haproxy-runtime-results.generated.md`. Root
summaries remain connector-neutral.

## Decision And Audit Logs

The runtime writes per-case and aggregate evidence:

- `decision.jsonl`: SPOA decisions, action, status, rule id, phase, and
  processing flags.
- `audit.log`: libmodsecurity audit output when audit logging is configured.
- `haproxy.stderr.log`: HAProxy runtime diagnostics.
- `spoa-agent.log`: SPOA runtime diagnostics.
- `haproxy-results.jsonl`: normalized case evidence.
- `haproxy-summary.json`: normalized counts and artifact references.

Production-style example paths:

```text
/var/log/haproxy-modsecurity/decision.jsonl
/var/log/haproxy-modsecurity/audit.log
/var/log/haproxy-modsecurity/agent.log
```

## Request Phases

The `request-check` SPOE group sends:

- request id
- client and server addresses
- method, path, URI, and host
- request headers
- request body bytes and length

The SPOA runtime maps those fields to libmodsecurity request processing and
returns HAProxy variables such as `blocked`, `action`, `status`,
`redirect_url`, `rule_id`, `phase`, and `error`.

## Phase 3 Response Headers

The `response-check` SPOE group sends response status and response headers,
including content type, location, set-cookie, server, and last-modified values.
The SPOA runtime processes response headers through libmodsecurity and returns
HAProxy variables for response-side enforcement.

## Phase 4 / RESPONSE_BODY

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` sample and its `response_body` arguments are
disabled: the harness sets `HAPROXY_ENABLE_RESPONSE_BODY=0` and emits neither
of them. The retired sample is legacy/noncanonical and must not be reported as
current runtime evidence. The separate HAProxy 3.2.21 HTX full-lifecycle path
is non-promoted; its one-block P2 probe records zero or one observed upstream
requests without proving their ordering and does not prove incremental forwarding.

## Production Configuration Shape

The example production path is:

- HAProxy config: `/etc/haproxy/haproxy.cfg`
- SPOE config: `/etc/haproxy/spoe-modsecurity.conf`
- SPOA config: `/etc/haproxy/modsecurity-agent.conf`
- SPOA binary: `/usr/local/sbin/haproxy-modsecurity-spoa`
- ModSecurity rules: `/etc/modsecurity/haproxy-rules.conf`

Changing HAProxy or SPOE config requires a HAProxy reload. Changing agent
config, the SPOA binary, libmodsecurity, or rule files requires restarting the
SPOA service.

## Status Meanings

- `PASS`: live HAProxy and SPOA runtime produced the expected case result.
- `FAIL`: live runtime executed but observed behavior differed from the
  expectation.
- `BLOCKED`: relevant, but blocked by environment or runtime prerequisites.
- `NOT_EXECUTABLE`: outside current HAProxy runtime scope.
- `former_xfail`: broader evidence tracked outside the default smoke subset.

## Tracked Open Work

- Broader force-all FAIL investigation.
- Promotion criteria for full RESPONSE_BODY support.
- Production packaging and service-manager examples.
- Wider deployment documentation after additional runtime environments are
  proven.

## Related Reports

- `reports/testing/generated/runtime/haproxy-runtime-results.generated.md`
- `reports/testing/test-coverage-overview.md`
- `modules/ModSecurity-test-Framework/TEST-COVERAGE-SUMMARY.md`
- `COMPILE_HAPROXY.md`
