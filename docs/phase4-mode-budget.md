# Phase-4 mode and response-body limit ownership

**Language:** English | [Deutsch](phase4-mode-budget.de.md)

## Scope

This contract covers Common Runtime and all Apache, NGINX, HAProxy, Envoy,
Traefik and lighttpd response routes, including middleware, companions and
sidecars. Phase-4 mode controls host intervention handling.

## Ownership contract

Response-body inspection limit and limit action are determined exclusively by
`SecResponseBodyLimit` and `SecResponseBodyLimitAction`. The connector has no
option, default or second enforcement logic for this policy.

| Concern | Owner | Required behavior |
| --- | --- | --- |
| Response inspection enablement and MIME selection | libModSecurity | `SecResponseBodyAccess`, `SecResponseBodyMimeType`, `SecResponseBodyMimeTypesClear` remain engine configuration. |
| Response inspection limit and Reject/ProcessPartial | libModSecurity | Native directives own the limit, action, results and interventions. |
| Response data and native results | Connector | Pass complete borrowed chunks safely; capture native operation results and interventions; finish the phase. |
| Late intervention behavior | Connector/host | Existing `off`, `safe`, `strict` and supported host actions remain. No mode selects a response limit. |
| Technical safety | Connector/host | Bounded work buffers, protocol frames/messages, actual buffered-storage capacity, file/descriptor/pointer checks, overflow, timeouts and metadata limits remain independent. |

The connector neither parses engine rules to find a limit nor injects a default
engine directive. Engine includes, inheritance and omitted configuration retain
native libModSecurity semantics. `body_limit_action` applies only to the existing
request policy.

## Compatibility

Remove `response_body_limit`, `modsecurity_response_body_limit`,
`modsecurity_phase4_body_limit`, HAProxy `response-body-limit` and Envoy
`max_response_body_bytes` from the corresponding configuration. Removed options
are rejected; there is no alias or replacement cumulative response option.
No new production configuration requirement is introduced. Operators configure
engine limits through their normal rule configuration.

## Streaming and memory

Streaming adapters offer every valid chunk to libModSecurity without connector
truncation or a cumulative inspection ceiling. A work block is not the permitted
size of an entire response. Checked counters detect overflow without substituting
`SIZE_MAX` for an engine limit or using it as an allocation size.

NGINX retains bounded reusable file scratch and validates file ranges. MRC1
retains 32-KiB body chunks and 64-KiB frames; these caps apply per message.
Envoy retains gRPC message limits. Traefik retains UDS frame/chunk checks.
HAProxy retains SPOP/HTX transport checks. The active lighttpd sidecar streams
through bounded scratch storage. Its old whole-response buffering implementation
is compiled out and does not impose a current runtime limit.
Headers, events, correlation registries, descriptors and timeouts remain bounded.

The response `bytes_inspected` counter records bytes offered to the engine. It
does not claim that the engine inspected every byte after choosing ProcessPartial.

## Native errors and intervention modes

Real engine-limit interventions remain native outcomes. `ProcessPartial` is
selected and performed by the engine, never simulated with a connector byte
counter. An append result alone is not an allow decision. Native return contracts,
intervention capture, phase completion and actual host outcome recording remain
operation-specific. Technical engine, memory, transport and lifecycle failures
remain failures; `safe` does not turn them into successful log-only outcomes.

## Verification boundary

Every response-inspection test must choose both directives explicitly in its
own configuration. Shared fixture helpers require limit and action arguments;
there are no global defaults or payload-derived values. Tests without response
inspection need no artificial response-limit configuration.

Real-engine integration verifies the limit behavior separately from stubbed
adapter contracts. Builds and unit/contract tests are not hosted HTTP/1, HTTP/2,
HTTP/3 or late-abort evidence. See the separate
[stack checklist](response-limit-stack-checklist.md) for implementation, tests and
missing real-host evidence.
