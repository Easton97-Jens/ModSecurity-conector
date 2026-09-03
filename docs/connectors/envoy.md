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


## ext_authz logical response companion

The <code>ext_authz</code> request protocol does not carry a response stream.
For the shared contract it transfers the live Common/native transaction after
completed P1/P2 into a fixed 64-entry, TTL-bounded response companion. The
authorization service generates a 256-bit opaque response handle with the
kernel randomness API; it never exposes a transaction ID, connector ID, or
host ID for correlation. The handle is accepted exactly once over the private
MRC1 UDS, then the live transaction remains internal to Common Runtime.

The supplied <code>envoy-ext-authz-smoke.yaml.in</code> wires this as one
logical connector: <code>ext_authz</code> may copy only
<code>x-msconnector-response-handle</code> onto Envoy's internal upstream-header
path to the immediately following private-UDS <code>ext_proc</code> response
observer. That observer claims and immediately removes the header before the
real application upstream; it receives no request body. It sends P3
before response commitment, P4 chunks/EOS afterwards, reports the actual host
outcome, and releases or cancels the handle deterministically. Its default UDS
and the C companion UDS are below <code>/run/modsecurity</code>; operators must
provision that parent as a canonical, owner-only <code>0700</code> directory.
There is no TCP fallback for either private binding.

A missing, malformed, expired, duplicate, or already claimed handle is a
protocol error. An unavailable observer, malformed MRC1 result, deadline, or
cleanup failure is fail-closed: the configured <code>ext_proc</code> filter has
<code>failure_mode_allow: false</code> and prevents routing rather than silently
claiming P3/P4 coverage. TTL expiry records timeout and destroys the retained
transaction; cancellation and observer shutdown use the same canonical cleanup
path. The local harness starts the required observer with isolated owner-only
sockets and passes the companion socket explicitly to the authorization
service.

This is source and component evidence only. A deployed Envoy instance still
needs a configuration-validation and traffic run before it is described as
host-runtime evidence.

See the [shared transaction and phase contract](../../common/docs/transaction-phase-contract.md)
for its exact state machine and decision policy.

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
