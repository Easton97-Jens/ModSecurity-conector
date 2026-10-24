# Common design

**Language:** English | [Deutsch](design.de.md)

Status: current-boundary reference

## Authority and scope

This note summarizes the current ownership boundary for `common/`. The binding
product source is the [Repository concept](../../docs/repository-concept.md),
and the current architectural source is [Architecture](../../docs/architecture.md).
Connector guides define their host-specific build, configuration, lifecycle,
compatibility, and evidence details. This note does not create a runtime,
production-readiness, or capability-promotion claim.

The [shared transaction and phase contract](transaction-phase-contract.md)
is the Common authority for source-derived P1--P4 meaning, bounded state,
decision policy, and all ten logical connector identities.

## Host-neutral Common contract

`common/` is connector-neutral. It provides C-first contracts and
implementations for neutral lifecycle support, configuration, limits,
decisions, events, logging/redaction, and engine-facing helpers. It must not
include or depend on host SDK types, host hooks, host filters, host object
lifetimes, host configuration registration, or client-visible host actions.

Host-specific mapping, callback registration, host-owned allocation, commit
semantics, intervention materialization, build glue, and installation remain
in `connectors/<name>/`. A Common type or helper is not evidence that every
host implements a lifecycle phase or an intervention.

## Ownership, data, and intervention boundary

The host adapter owns requests, responses, buffers, and host objects. Common
accepts validated bounded views or copies only for the corresponding call and
must not retain a connector-owned full response body across callbacks. It owns
only its documented neutral runtime, rules, copied configuration, and
transaction metadata; connectors retain host cleanup and exactly-once lifecycle
responsibilities.

Common can represent a requested decision and payload-safe metadata. The host
adapter determines whether and how that decision becomes an actual
client-visible action, especially after response commitment.

## Selected product routes

The selected product routes below identify ownership only. A route name,
source contract, build, or documentation check is not runtime evidence.

| Connector | Selected product route | Compatibility material |
| --- | --- | --- |
| Apache | `native-httpd-module` | No selected compatibility route |
| NGINX | `native-nginx-http-module` | No selected compatibility route |
| HAProxy | `native-htx-filter` | `spoe-spop-agent` is `compatibility_only` |
| Envoy | `ext_proc` | `ext_authz` is `compatibility_only` |
| Traefik | `native-traefik-middleware` | `forwardAuth` is `compatibility_only` |
| lighttpd | `patched-native-lighttpd` | canonical Stock logical route is `stock-lighttpd-sidecar`; native `stock-lighttpd` is an explicit P1/P3 `compatibility_only` translation |

`compatibility_only` is a promotion/evidence designation, not an exemption from
the shared transaction contract. Where an enabled compatibility route can
carry traffic, it uses its listed contract profile: raw SPOP carries direct
P1/P2 and requires the native-HTX response companion for P3/P4; `ext_authz` is `compatibility_only`
and requires its response companion for P3/P4;
`forwardAuth` is `compatibility_only` and requires its response companion for
P3/P4. The selected Stock lighttpd route is the traffic-owning
`stock-lighttpd-sidecar`: a private literal-loopback HTTP/1.1 sidecar owns one
bounded exchange and maps P1--P4 directly. The unchanged native Stock module
route remains an explicit P1/P3-only compatibility translation, never a silent
fallback. Because one sidecar worker owns the complete exchange, it needs no
cross-process correlation or TTL registry; the separate Patched route remains
its own logical solution.
The selected product route remains the only route with the separate
runtime-evidence claim.

## Test and evidence boundary

The Parent repository owns product contracts, connector seams, build wiring,
and host-specific artifact production. `modules/ModSecurity-test-Framework/`
owns reusable cases, runners, normalizers, schemas, and report generation.
Do not place a second reusable case catalog or normalizer in `common/`.

[Testing and evidence](../../docs/testing-and-evidence.md) defines what each
test layer can establish. Source, documentation, and contract checks protect
their stated boundary only; they do not replace selected host traffic or
canonical run-scoped evidence.

## Historical material

Earlier draft design and open-connector smoke material remains available
through Git history. It is not a current route, build, runtime, or evidence
guide. Preserve a legacy path only when the owning connector documentation
labels it `compatibility_only` and keeps it separate from the selected route.

## Related references

- [Repository concept](../../docs/repository-concept.md)
- [Architecture](../../docs/architecture.md)
- [ADR-003](../../docs/decisions/ADR-003-shared-p1-p4-lifecycle-semantics.md)
- [Testing and evidence](../../docs/testing-and-evidence.md)
- [Common source-tree guide](../README.md)
