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
- Phase 4 / RESPONSE_BODY: `not_implemented` in the selected SPOE/SPOP path.

The former bounded strict-abort sample is disabled and retained only as a
legacy, noncanonical artifact. It must not be used or reported as current
runtime evidence. The optional HAProxy 3.2.21 HTX observer is nonselected and
observer-only after forwarding, but has its own real-host P1–P4 transport smoke
with incremental request/response chunks.

That smoke proves a patched HTX filter can invoke libmodsecurity in all four
phases and records metadata-only observations. It deliberately does not turn a
decision into a HAProxy reply or stream abort: P1/P2/P3 client status remains
the upstream 200 and P4 reports `host_action=not_attempted`.

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

## Common SDK adoption layer

HAProxy now treats Common as the owner for reusable semantics: config defaults/merge/validation, directive specifications, primitive option parsers, request/response mapper contracts, header/content helpers, event JSONL generation, rule-id extraction, log sanitizing/redaction, resource limits, DoS guard, flow guard, integrity events, rule-loading stats, CRS setup contracts, and test/artifact contracts where applicable.

HAProxy-owned code remains limited to SPOE/SPOP protocol handling, generated HAProxy cfg fragments, SPOA runtime loop/socket handling, HAProxy process lifecycle, frame parsing, return/action encoding, logging transport, and build glue. The C17 standard check compiles the adoption-relevant C objects without starting HAProxy and reports `BLOCKED`/77 when required external headers are absent.
