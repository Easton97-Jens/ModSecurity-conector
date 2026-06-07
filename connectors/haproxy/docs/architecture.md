# HAProxy Architecture

Status: production SPOA runtime, partial and evidence-scoped

The HAProxy connector uses a production SPOA/SPOP process instead of an
in-process HAProxy module:

```text
HTTP client -> HAProxy -> SPOE/SPOP -> haproxy-modsecurity-spoa -> libmodsecurity -> HAProxy response
```

## Implemented Path

- `haproxy-modsecurity-spoa` is built from
  `connectors/haproxy/src/haproxy_spop_diagnostic_runtime.c`.
- The local libmodsecurity binding is built from
  `connectors/haproxy/src/haproxy_modsecurity_binding.c`.
- HAProxy sends request and response data through SPOE/SPOP.
- The SPOA process returns typed `txn.modsec.*` variables for HAProxy
  enforcement.
- Runtime evidence includes `decision.jsonl`, audit-log plumbing, HAProxy logs,
  SPOA logs, JSONL case results, and generated summaries.

## Phase Coverage

- Request phases 1/2: live runtime evidence.
- Phase 3 response headers: implemented and live evidenced.
- Phase 4 / RESPONSE_BODY: bounded strict-abort evidence only.

Phase 4 / RESPONSE_BODY remains non-promoted; bounded strict-abort evidence is
documented/reported as runtime evidence only.

## Current Evidence

| Evidence set | Attempted | PASS | FAIL | BLOCKED | NOT_EXECUTABLE |
| --- | ---: | ---: | ---: | ---: | ---: |
| Default HAProxy smoke | 55 | 55 | 0 | 0 | 0 |
| HAProxy force-all | 133 | 104 | 23 | 0 | 6 |

## Boundaries

There is no synthetic matrix writer. Generated HAProxy reports consume live
runtime summaries and the runtime validation snapshot. Full-body guarantees,
arbitrary dynamic disruptive status mapping, and long-running production
hardening remain open before promotion beyond partial status.
