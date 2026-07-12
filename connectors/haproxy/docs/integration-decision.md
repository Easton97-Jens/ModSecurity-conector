# HAProxy Integration Decision

**Language:** English | [Deutsch](integration-decision.de.md)

Status: SPOE/SPOA selected for current production runtime scope

## Decision

Use HAProxy SPOE/SPOP with an external `haproxy-modsecurity-spoa` process that
loads libmodsecurity.

```text
HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity
```

## Why This Path

- HAProxy documents SPOE/SPOP for external stream-processing agents.
- The path avoids inventing a native HAProxy module interface.
- The repository now has a buildable SPOA runtime and libmodsecurity binding.
- The runtime harness starts HAProxy, the SPOA process, and a backend, then
  verifies live framework YAML expectations.
- The same path produces `decision.jsonl`, audit-log plumbing, and generated
  runtime summaries.

## Alternatives

| Alternative | Current decision |
| --- | --- |
| Native HAProxy filter or extension | The separate `full-lifecycle-haproxy-htx` profile selects a HAProxy 3.2.21 HTX route with isolated P1–P4 transport evidence. It proves canonical P1/P3 replies; its one-block P2 probe returns a client 403 and records zero or one observed upstream requests without proving their ordering or incremental forwarding. P4 Safe records `log_only`. Strict has no client-visible abort proof and the route has no capability-promotion evidence. |
| Lua integration | Deferred. Not proven for full ModSecurity lifecycle. |
| External HTTP sidecar | Deferred. The implemented path uses SPOE/SPOP instead. |

## Current Evidence

- Default HAProxy smoke: `55/55 PASS`.
- HAProxy force-all: `133 attempted / 104 PASS / 23 FAIL / 0 BLOCKED /
  6 NOT_EXECUTABLE`.
- Details: `reports/testing/generated/haproxy-runtime-results.generated.md`.
- PoC report: `reports/testing/haproxy-poc.md`.

Phase 4 / RESPONSE_BODY is `not_implemented` in the selected SPOE/SPOP path.
The former `wait-for-body` strict-abort sample is disabled, legacy, and
noncanonical; it is not current runtime evidence.
