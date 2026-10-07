# Traefik Connector

**Language:** English | [Deutsch](traefik.de.md)

## Go composite Common runtime and observed lifecycle

The separately built `msconnector-composite --mode traefik` selects the
canonical `traefik / forwardAuth / traefik-forwardauth` identity with buffered
requests and streaming responses. It uses the additive header-only buffered
start, explicit request append/EOS, and a private Common response-companion
session for P3/P4. Direct Envoy ext_proc remains streaming in both directions.

The Go lease/context/deadline is checked before the native claim. Native
expiry consumes ownership; consumed cleanup errors are not retried. Unresolved
cleanup permanently faults the coordinator and closes admission for controlled
restart. Terminal cleanup is guarded once and retains entry ownership until
it completes. A real Common body-limit failure maps to 413 with actual
host-action metadata; terminal incomplete-body cleanup does not invent EOS
or P2 rule evaluation.

On 2026-10-03 external run `p370t.T4wJJ8kA` exercised the real Traefik host,
local composite middleware and Go Common/libmodsecurity service. Ten cases
returned `LIFECYCLE_ONLY`: P1 allow/deny, P2 allow/deny/oversize, P3
deny/redirect, P4 Safe, missing metadata, and P2-to-P3 timeout. P4 Strict
returned the expected `NON_PASS` because no independent host reset/abort
was demonstrated. All cases retain `catalog_acceptance=false`.

The final source manifest was unchanged, cleanup reported no issues, and
ephemeral test keys were removed. Executable/library hashes, loaded-library
observations, resource samples and upstream observations remain in the
external evidence. This evidence applies to the Go composite route and does
not promote the legacy C service's `implemented_not_asserted` or
`configured_not_exercised` statuses, nor the separate native UDS profile.

Complete G1–G9 acceptance for all nine non-NGINX profiles remains open;
production readiness is not claimed. See the
[Change Record](../../reports/audits/change-records/CR-20261003-pr370-composite-common-runtime.md)
for scope, commands and remaining gaps.

## Overview

Traefik uses the selected <code>native-traefik-middleware</code> route: a local
plugin/middleware path with a private UDS Common/libmodsecurity engine service.
The retained forwardAuth service is a separate compatibility path. This guide
describes the selected HTTP/1.1 P1--P4-safe boundary and does not claim
production readiness, CRS completeness, complete protocol coverage, strict
late abort, first-byte behavior, no-full-response-buffering, or a complete
matrix.

## Architecture and ownership

The native middleware owns Traefik-shaped request/response handling,
ResponseWriter behavior, plugin lifecycle, and UDS client interaction. The
local engine service owns bounded per-transaction protocol framing and explicit
finish/destroy handling. Common owns neutral runtime configuration, engine
calls, limits, decisions, and payload-safe events; it does not own Traefik
objects or commit semantics.

| Lifecycle area | Selected native responsibility | Boundary |
| --- | --- | --- |
| P1/P2 | Map the selected request path to a private engine session | Body mode and host behavior remain profile-specific |
| P3 | Process response headers before/at the host writer boundary | Actual writer commitment controls intervention options |
| P4 | Process bounded response ranges with a conservative post-commit outcome | Selected safe outcome is <code>log_only</code> |
| Service cleanup | Finish/destroy exactly one transaction per selected request | Focused source tests are not a host traffic claim |

## Build

Use [the Traefik compiler guide](../build/compilers/traefik.md) for selected
build/service/runtime component procedures. The code-adjacent
[Traefik source guide](../../connectors/traefik/README.md) and
<code>connectors/traefik/native_middleware/</code> document the local source
layout. Unit/build/self-test stages remain separate from a real host run.

## Configuration

The complete static/dynamic/native-plugin/Common Runtime configuration surface,
defaults, placeholders, and forwardAuth compatibility fields are in the
[Traefik configuration reference](../../examples/traefik/configuration-reference.md).
The selected native UDS route and forwardAuth have different response
visibility; do not promote a forwardAuth request result as native P3/P4 proof.

## forwardAuth logical response companion

The <code>forwardAuth</code> request protocol cannot itself carry P3/P4. Its
authorization service transfers the same live Common/native transaction after
completed P1/P2 into a fixed 64-entry, TTL-bounded response companion. It emits
one server-generated 256-bit opaque response handle, never a transaction ID,
connector ID, or host ID. The private MRC1 listener accepts that handle exactly
once, so all retained native state stays inside Common Runtime.

The supplied response-observer plugin and the
<code>traefik-response-observer-{static,dynamic}.yaml</code> artifacts make
forwardAuth plus its response observer one logical connector. The dynamic
chain is <code>forwardAuth -&gt; response observer -&gt; upstream</code> and permits
only <code>X-Msconnector-Response-Handle</code> from the authorization response.
The observer claims and strips that header before the upstream handler. It
sends P3 before the writer commits, P4 chunks/EOS after commitment, records
the actual host outcome, and releases or cancels deterministically. It uses
only a private UDS; the default companion path is below
<code>/run/modsecurity</code>, whose canonical owner-only <code>0700</code>
parent must be provisioned by the operator. There is no TCP fallback.

Missing, malformed, expired, duplicate, replayed, or unavailable handles are
fail-closed before upstream response commitment. A malformed MRC1 result,
deadline, or cleanup failure follows the same error/cancel path; TTL expiry
records timeout and destroys retained state. Post-commit disruptive engine
results are recorded as log-only because Traefik cannot retroactively rewrite
the response. The local plugin exposes neither <code>Unwrap</code> nor
<code>Hijacker</code>, avoiding a bypass around that boundary.

The legacy C route and its component tests above are source-level evidence. A deployed
Traefik instance still requires plugin-load, configuration, and traffic
evidence before it is described as host-runtime evidence.

See the [shared transaction and phase contract](../../common/docs/transaction-phase-contract.md)
for the state machine and uniform decision policy.

## P1--P4 lifecycle and local engine service

The selected native host check stages the middleware in an isolated local-plugin
workspace, starts the private engine service, and records selected P1/P2/P3
and Safe P4 metadata. The service protocol is bounded and per transaction; it
does not establish global host behavior merely because its local self-test
passes.

| Question | Required evidence |
| --- | --- |
| Native host path | Plugin-load confirmation, selected traffic, and matching integration metadata |
| P3 | Response-header timing/commit metadata and actual visible result |
| Safe P4 | Original visible response, <code>log_only</code>, and post-commit metadata |
| Strict P4 | A separately proven host/client abort; not a configured service mode |

## Testing and evidence

Run only the target layer needed for the question: configuration, request-free
start, local service protocol, native middleware source tests, or selected host
traffic. Missing optional Traefik binaries remain blocked prerequisites. A
real host claim requires the selected run's result/event/effective-configuration
artifacts as described in [Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Keep the service socket, runtime roots, component cache, and evidence roots
outside the checkout and private to the intended local run. Diagnose plugin
load, UDS service startup, request mapping, and writer commitment separately.
Do not expose engine-service control endpoints or secret-bearing configuration
in checked-in examples or logs.

## Limitations and compatibility

ForwardAuth is compatibility-only and has its own request-oriented boundary.
The selected native middleware remains evidence-scoped for P4 Safe; strict
abort/cancellation, first byte before EOS, full response-buffer properties,
HTTP/2/HTTP/3, and CRS claims require dedicated selected artifacts.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [Traefik configuration reference](../../examples/traefik/configuration-reference.md)
