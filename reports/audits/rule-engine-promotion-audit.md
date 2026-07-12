# Rule-engine promotion audit

**Language:** English | [Deutsch](rule-engine-promotion-audit.de.md)

## Scope and evidence boundary

This audit maps selected real host paths on `feature/all-connectors-no-crs-baseline`. It does not promote a capability itself. A `PASS` is valid only when one canonical host run binds the selected integration mode, transaction ID, rule ID, phase, requested and actual action, and visible host result. Builds, direct Common calls, synthetic barriers, and normalized summaries are not substitutes for that evidence.

| Connector | Real host entry | Engine begin | P1 | P2 | P3 | P4 append | EOS finish | Intervention | Host action | Cleanup |
|---|---|---|---|---|---|---|---|---|---|---|
| Traefik native middleware | `Middleware.ServeHTTP` in the pinned local plugin | Request-scoped UDS session to `traefik_engine_service` starts Common/libmodsecurity | Headers before upstream | Same-session request body, selected P2 403 | Wrapped writer before commit | Current `Write` chunk only; no recorder | Close sends EOS once | Common decision per session | Pre-commit status; Safe log_only | Idempotent deferred close; reset/cancel unselected |
| Envoy ext_proc | `processor.Service.Process` on the real gRPC listener | CGo Common/runtime bridge, one transaction per stream | Real request headers | Streamed request body/EOS | Real upstream response headers | Streamed messages, no service-side full body | `end_of_stream` once | Common decision per stream | Immediate response before commit; Safe log_only | Stream close; downstream reset/cancel unselected |
| HAProxy HTX | Native `flt_ops` callbacks in `haproxy_modsecurity_htx_filter.c` | Per-stream `msc_new_transaction_with_id` | Real 403 and 429 replies | Payload callbacks/EOS, no selected P2 enforcement | Real 403 before client commit | Payload callback, no selected P4 outcome | `http_end` guards finishes | Stream transaction reads libmodsecurity result | Native P1/P3 reply path | Filter detach frees stream state |
| lighttpd patched native | Patched URI-clean/module hooks | `msconnector_runtime_transaction_begin` per request | Real 403 and 429 | Patched decoded body, real P2 403 | Response-start, real P3 403 | Borrowed identity entity ranges in `http_chunk`; no real P4 host result | Request EOS; entity EOS is once-only | Common reads available decisions | `http_status_set_err()` before commit; Safe is `log_only` | `handle_request_reset` finishes/destroys once |
| Apache native module | Native httpd hooks/input/output filters | Per-request libmodsecurity transaction | Real 403/429/redirect | Input-filter EOS, P2 403 | P3 403/302 before commit | Bounded brigades pass onward | EOS once | Bounded Common events | Pre-commit reply, Safe log_only, Strict abort | Normal completion exercised |
| NGINX native module | Native access/header/body filters | Per-request libmodsecurity transaction | Real 403/429/redirect | Native path, P2 403 | P3 403/302 before commit | Bounded response chains | last-buffer EOS once | Bounded Common events | Pre-commit reply, Safe log_only, Strict abort | Normal completion; HTTP/2 not applicable |

## Current selected host evidence

- Canonical aggregate `full-lifecycle-rule-engine-all-final-20260712T083029Z`:
  all six runners exited 0 with complete artifacts and no FAIL/BLOCKED. Its
  PASS/NOT EXECUTED counts are Apache 31/73, NGINX 31/73, HAProxy 13/91,
  Envoy 17/87, Traefik 16/88, and lighttpd 19/85.

- Each final connector directory also contains payload-free engine provenance
  and accounting sidecars: `engine-version.txt`, engine-library and ruleset
  SHA-256 files, `transaction-counts.json`, and `lifecycle-counters.json`.
  They inventory the current host run only and are not a promotion input.

- Traefik `rule-engine-traefik-final-20260712T071711Z`: real P1/P2/P3 enforcement and P4 Safe `log_only`, with matching event metadata.
- Envoy `rule-engine-envoy-20260712T070435Z`: real ext_proc P1/P2/P3, P3 redirect, and P4 Safe `log_only` through the CGo bridge.
- HAProxy `rule-engine-haproxy-20260712T070510Z`: native P1 403, P1 429, and P3 403 replies. P2/P4 are not promoted from callbacks alone.
- lighttpd `rule-engine-lighttpd-20260712T070545Z`: patched-host P1 403/429, P2 403, and P3 403; response-body P4 remains unexecuted.
- Apache `rule-engine-apache-20260712T072808Z`: P1/P2/P3 plus distinct P4 Safe `log_only` and Strict `connection_aborted` events.
- NGINX `rule-engine-nginx-retry-20260712T073639Z`: equivalent P1/P2/P3 and distinct P4 Safe/Strict outcomes. `nginx -V` lacks `--with-http_v2_module`, so HTTP/2 is `NOT_APPLICABLE` for this build.

All cited raw events are metadata-only: no request/response payloads, matched values, complete rule messages, authorization values, or cookies are used.

## HTTP/2 and HTTP/3 protocol status

The transport-hardening catalog and payload-free managed client are present,
but this report does not promote a modern-protocol lifecycle result. Local
`curl 8.18.0` supports HTTP/2 and lacks HTTP/3, so forced H3 work is `BLOCKED`
with `client_http3_unsupported`; that is an environment blocker rather than a
connector classification. The inspected NGINX runtime binary lacks both
`--with-http_v2_module` and `--with-http_v3_module`; the HAProxy binary lists
an H2 mux but has no SSL/QUIC build; and Apache has no loaded `mod_http2`.

Modern probes now carry a bounded `transport_case_id` in a redacted request
header; a future PASS must match it in client observation, connector event,
and case result. The managed curl helper is negotiation-only, so it cannot
promote Strict/reset/cancel/multiplexing evidence without a dedicated
stream-control client. The NGINX profile harness does provide ephemeral local
CA/leaf material and separate TCP/UDP listener facts, while H3 0-RTT remains
`NOT EXECUTED`.

Accordingly all H2/H2C/H3 phase, multiplexing, stream-reset, first-byte, and
no-full-buffer cases remain `NOT EXECUTED` unless a future forced, negotiated
host run supplies correlated client and connector evidence. A build profile,
an H2 mux, `Alt-Svc`, a connection abort, or an internal service-stream close
is not an H2/H3 `PASS` or a request-local stream reset. See the
[transport-hardening audit](transport-hardening-audit.md) for the exact
connector matrix and non-claims.

## Remaining boundaries

- Traefik and Envoy Strict are `NOT EXECUTED`: no client-visible post-commit reset is proven. An internal service-stream close is not proof.
- HAProxy P2/P4 enforcement, late action, first-byte, and no-full-buffer claims remain `NOT EXECUTED`; native callbacks are not synthetic evidence.
- lighttpd P4 remains `NOT EXECUTED`: the selected decoded identity-entity hook, cursor, short-write/EAGAIN handling, and once-only EOS are in place, but a real P4 host run and client-visible Strict evidence are still absent.
- Apache and NGINX do not claim every catalog cleanup, disconnect, body-limit, content-type, or transport case from these normal-path runs.

Selected previously unpromoted lifecycle cases now have real host and libmodsecurity rule-engine evidence. Remaining `NOT EXECUTED` cases continue to represent unverified or unimplemented behavior and were not promoted from synthetic artifacts.
