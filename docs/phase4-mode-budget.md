# Phase-4 mode and response-body limit ownership

**Language:** English | [Deutsch](phase4-mode-budget.de.md)

## Quick orientation

Phase 4 is response-body processing. The Phase-4 mode controls **late intervention behavior**, not a second connector-owned WAF inspection byte policy.

libModSecurity owns response inspection enablement, MIME selection, and WAF response byte limits through `SecResponseBodyAccess`, `SecResponseBodyMimeType` / `SecResponseBodyMimeTypesClear`, `SecResponseBodyLimit`, and `SecResponseBodyLimitAction`.

Legacy connector response-limit settings may remain parseable for compatibility, but `off`, `safe`, and `strict` do not add different cumulative WAF byte budgets. Independent host/transport capacity limits, bounded storage, allocation guards, timeouts, and message/frame limits still apply.

## Scope

This contract covers Apache, NGINX, HAProxy, Envoy, Traefik and lighttpd in this
repository. Phase-4 mode controls late-intervention behavior; it does not create
a second response-inspection policy in the connector.

## Ownership contract

| Concern | Owner | Required behavior |
| --- | --- | --- |
| Response inspection enablement and MIME selection | libModSecurity | Use `SecResponseBodyAccess`, `SecResponseBodyMimeType`, and `SecResponseBodyMimeTypesClear`. |
| WAF response inspection byte limit | libModSecurity | Use `SecResponseBodyLimit` and `SecResponseBodyLimitAction`. |
| Late intervention behavior | Connector/host | `off`, `safe`, and `strict` retain their host-specific intervention semantics. |
| Host/transport capacity | Connector/host | Chunk/frame caps, bounded storage, allocation ceilings, timeouts, file-read validation, and overflow guards remain independent controls. |

No valid Phase-4 mode enforces an additional connector-owned cumulative
response-inspection budget. In particular, `safe` and `strict` must not reject
or abort a response merely because a legacy connector inspection byte count was
exceeded.

## Compatibility

Legacy settings such as `modsecurity_phase4_body_limit` may remain accepted
while configurations migrate. They are compatibility values, not WAF
inspection policy, and do not create a safe/strict-only cumulative response
limit. Removing such settings from public configuration is a separate breaking
change.

Common Runtime `response_body_limit` values can still describe bounded
host/transport or storage capacity where a host genuinely needs that capacity.
They must not be presented as a replacement for `SecResponseBodyLimit`.

## Streaming and memory

Removing the connector inspection budget does not authorize unbounded
allocation. Native/streaming connectors should pass body ranges incrementally
to libModSecurity. NGINX file-backed buffers use a fixed reusable scratch
buffer rather than allocating the full response.

Buffered compatibility routes may still reject a response that cannot fit
their bounded host storage. Envoy/gRPC chunk or message limits, HAProxy
transport limits, lighttpd sidecar capacity, header/event limits, correlation
capacities, timeouts, pointer validation, file-read checks, and integer-overflow
checks remain active.

## Native errors and intervention modes

Real engine, memory, transport, lifecycle, and processing failures remain
failures. This change does not convert them into `log_only`.

In NGINX `off`, a negative native intervention result keeps the historical
`ngx_http_filter_finalize_request(..., NGX_HTTP_INTERNAL_SERVER_ERROR)` path.
Positive statuses are returned unchanged; zero continues normally. Safe/Strict
late-intervention behavior remains separate from response-limit ownership.

Other integrations retain their own return conventions and supported
late-action mechanisms.

## Verification boundary

Source wiring and unit tests can verify that all valid modes resolve the legacy
connector inspection ceiling to an accounting-only maximum and that independent
host limits remain wired. They do not prove live HTTP/1, HTTP/2, HTTP/3 or
host-specific late-abort behavior.

See the Change Record
[CR-20261004-engine-owned-response-limits](../reports/audits/change-records/CR-20261004-engine-owned-response-limits.md)
for this migration's scoped implementation and validation status.
