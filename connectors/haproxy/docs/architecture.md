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
runtime evidence. The separate `full-lifecycle-haproxy-htx` profile selects
the HAProxy 3.2.21 HTX route. It has its own real-host P1–P4 transport smoke
with borrowed request/response chunks. P1/P3 can issue a local precommit
reply; the one-block P2 probe can issue a client 403 at request EOS while the
runner records zero or one observed upstream requests without proving their
ordering. That outcome is deliberately not presented as incremental
request-forwarding evidence, and P4 Safe is an
explicit `log_only` result.

That smoke proves a patched HTX filter can invoke libmodsecurity in all four
phases. Canonical P1 rules `1100001`/`1100002` produce real 403/429 replies,
and P3 rule `1100201` produces a real 403 before the received upstream header
response is forwarded. P2's one-block client 403 has an observed upstream
request count of zero, so the host smoke does not establish incremental
request forwarding or a general buffering property. P4 Safe forwards the
original response and records `host_action=log_only`; P4 Strict remains
`host_action=not_attempted`. Neither path is a stream-abort, first-byte, or
client no-full-buffer proof.

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
