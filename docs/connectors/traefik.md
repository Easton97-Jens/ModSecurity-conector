# Traefik Connector

**Language:** English | [Deutsch](traefik.de.md)

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
