# Envoy Connector

**Language:** English | [Deutsch](envoy.de.md)

## Overview

Envoy uses the selected streamed <code>ext_proc</code> route with a local
Common/libmodsecurity service. It is distinct from the retained
<code>ext_authz</code> compatibility example. This guide describes the selected
HTTP/1.1 P1--P4-safe architecture and does not claim production readiness,
CRS verification, complete matrix/protocol coverage, strict post-commit action,
or a universal Envoy deployment.

## Architecture and ownership

Envoy owns filter chain configuration, transport, stream callbacks, and host
response behavior. The ext_proc service owns its bounded protocol/session
mapping and calls into the Common/libmodsecurity runtime. Common remains free
of Envoy SDK types and owns only neutral configuration, mapping contracts,
limits, decision/event data, and engine-facing helpers.

| Lifecycle area | Selected ext_proc responsibility | Boundary |
| --- | --- | --- |
| P1/P2 | Map streamed request headers/body messages to the selected service session | Request flow is protocol/configuration dependent |
| P3 | Map response headers through the ext_proc service | Host-visible behavior depends on commit state |
| P4 | Process selected response-body stream messages and finish at EOS | Safe post-commit behavior remains conservative |
| Events | Write payload-free service/runtime metadata | A service record is not a client transport assertion |

## Build

Use [the Envoy compiler guide](../build/compilers/envoy.md) for service build,
runtime component selection, explicit preparation, and diagnostics. The
code-adjacent [Envoy source guide](../../connectors/envoy/README.md) and
<code>connectors/envoy/ext_proc/</code> describe source layout. A service build
or request-free start smoke is not full-lifecycle evidence.

## Configuration

The complete Envoy YAML/service/CLI configuration surface, placeholders,
defaults, and compatibility entries are in the
[Envoy configuration reference](../../examples/envoy/configuration-reference.md).
The selected <code>ext_proc</code> profile and the
<code>compatibility-ext-authz</code> example have separate semantics. Do not
present ext_authz response visibility as ext_proc P4 support.

## P1--P4 lifecycle and transport hardening

The selected service must preserve bounded message handling, explicit session
completion, and payload-safe metadata. A post-commit intervention is an
evidence-gated host/transport question: Safe records the actual conservative
outcome; Strict is not established merely by a configured mode or service
decision.

| Question | Required evidence |
| --- | --- |
| Selected P1--P3 path | Real Envoy traffic, selected service records, and matching effective configuration |
| P4 rule observation | Response-body stream/EOS metadata for the selected profile |
| Safe late behavior | Actual visible response plus recorded late/actual action |
| Strict/cancellation behavior | Explicit host/client transport observation, not API/source inspection |

## Testing and evidence

Use the selected build/config/start/runtime targets only for the layer named by
the target. Missing optional Envoy components should remain declared blocked
prerequisites rather than silently selecting a system binary. For a lifecycle
claim, inspect the run ID, selected integration mode, result/event records,
effective configuration, and host observations as described in
[Testing and evidence](../testing-and-evidence.md).

## Operations and troubleshooting

Use explicit external component, runtime, log, and evidence roots. Diagnose
configuration and service startup separately from real Envoy traffic. For a
response or late-intervention issue, inspect the stream/commit boundary and
actual action before interpreting a returned status.

## Limitations and compatibility

<code>ext_authz</code> is retained as a compatibility route and does not
substitute for selected full-lifecycle ext_proc response processing. HTTP/2,
HTTP/3, CRS, strict reset/cancellation, first-byte, and no-full-response-buffer
properties require their own selected host evidence.

## Related references

- [Architecture](../architecture.md)
- [Configuration](../configuration.md)
- [Operations and security](../operations-and-security.md)
- [Envoy configuration reference](../../examples/envoy/configuration-reference.md)
