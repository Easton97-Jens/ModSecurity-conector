# Architecture

**Language:** English | [Deutsch](architecture.de.md)

## Scope

This is the current architecture source of truth for the connector repository.
It describes the selected six HTTP/1.1 core routes and their shared boundaries.
It does not claim production readiness, production hardening, CRS verification,
complete HTTP/2 or HTTP/3 coverage, a complete matrix, or strict behavior for
every connector.

## Repository ownership

| Layer | Owns | Does not own |
| --- | --- | --- |
| <code>common/</code> | Connector-neutral C-first types, parsers, limits, event shapes, and helper implementations | Host SDK objects, hooks, filters, host configuration registration, or transaction lifetime |
| <code>connectors/&lt;name&gt;/</code> | Host integration, source attribution, build glue, host configuration, request/response mapping, and host-specific tests | A second generic Common runtime contract |
| Framework submodule | Reusable cases, schemas, catalog selection, normalization, and Framework-owned runners | Connector source, host integration, or a connector PASS claim without run evidence |
| Runtime evidence | One selected run's results, events, effective configuration, and provenance | A general assurance beyond that profile, ruleset, and run ID |

The checked-in source and build scripts define implementation details. This
document records the intended ownership and safety boundary around them.

## Selected host routes

| Connector | Selected integration mode | Response-body boundary |
| --- | --- | --- |
| Apache | Native HTTPD module | Output-filter/EOS handling |
| NGINX | Native HTTP module | Response filter and request/subrequest end-of-stream |
| HAProxy | Native HTX filter | HTX end-of-stream |
| Envoy | Streamed <code>ext_proc</code> service | Stream completion in the selected service protocol |
| Traefik | Native middleware with local UDS engine service | Response-writer commit boundary |
| lighttpd | Patched native module | Decoded entity-body end-of-stream |

Each connector guide documents its host-specific route, lifecycle, build path,
limitations, compatibility paths, operations, and validation:
[Apache](connectors/apache.md), [NGINX](connectors/nginx.md),
[HAProxy](connectors/haproxy.md), [Envoy](connectors/envoy.md),
[Traefik](connectors/traefik.md), and [lighttpd](connectors/lighttpd.md).

## Transaction lifecycle

| Phase | Neutral operation | Host responsibility | Evidence boundary |
| --- | --- | --- | --- |
| P1 | Connection, URI, and request-header processing | Map connection/request metadata and apply an eligible pre-commit intervention | A request result is not proof of other phases |
| P2 | Request-body append and finalization | Stream or buffer only as the selected host route permits; finalize once at request EOS | Body support is profile-specific |
| P3 | Response-header processing | Preserve original status and determine whether headers are still mutable | A P3 result does not establish P4 behavior |
| P4 | Response-body append and finalization | Process bounded chunks, preserve first-byte/no-full-buffer boundaries, and resolve late intervention safely | Post-commit action remains host- and evidence-dependent |
| Logging | Transaction logging and cleanup | Emit payload-safe metadata and release host/engine state exactly once | Logs are run-scoped evidence, not a runtime guarantee |

The engine-facing public sequence is based on libmodsecurity v3 calls for
connection, URI, request headers/body, response headers/body, intervention,
logging, and cleanup. A connector must not advertise a phase merely because a
neutral type or source branch exists.

## Common boundary and C-first contract

The Common layer is intentionally C-first. Its public headers model request,
response, transaction, intervention, status, capability, origin, logging,
limits, and configuration without including Apache, NGINX, HAProxy, Envoy,
Traefik, or lighttpd SDK headers. Thin C++ wrappers do not establish a second
ownership model and must not cross a host ABI boundary.

Common may validate neutral input, normalize configuration, redact event data,
and write bounded metadata. It must not retain a connector-owned full response
body merely to evaluate a rule, own a host object, decide a host-specific late
response action, or embed a server/proxy integration.

## Ownership, limits, and safe late behavior

Request and response buffers remain owned by the host adapter. Common receives
validated views or bounded copies only where its API explicitly requires one.
Headers, body ranges, transaction IDs, intervention data, and event metadata
must have a documented lifetime at every adapter boundary.

The selected Safe P4 behavior is conservative: a post-commit condition is
recorded as a bounded, payload-safe observation unless the selected host route
and run evidence prove a client-visible action. A documentation label such as
<code>strict</code> is not proof of an abort or HTTP error.

## Capability, status, and evidence model

Capabilities describe a host/profile property; they are not result records.
The status vocabulary distinguishes implemented, unsupported, blocked,
not executed, and observed result states. A source build, configuration load,
or generated matrix cannot promote an unexecuted host behavior.

Canonical evidence binds a result to a connector, selected profile, rule input,
run ID, effective configuration, and required artifact schema. Result/event
records remain payload-safe: do not persist request bodies, response bodies,
credentials, cookies, or authorization values merely to document a phase.

## Rule-load metadata

The Common rule-load structure records only successful inline, file, and remote
rule additions. It counts rules rather than directive calls or file count.
Failed loads keep their existing error path and do not increment a counter.
The metadata does not affect RulesSet ownership, merge behavior, request or
response processing, body handling, interventions, or phase behavior.

| Field | Meaning | Current exposure |
| --- | --- | --- |
| <code>inline_rules</code> | Rules loaded from inline rule content | Connector configuration metadata |
| <code>file_rules</code> | Rules loaded from rule files | NGINX startup logging; Apache internal metadata |
| <code>remote_rules</code> | Rules loaded from remote rule inputs | Connector configuration metadata |

Common has no reporting API for these values. Any shared report or Apache
post-config display remains separate work and cannot be inferred from a counter.

## Security-data-flow contract

Common integrity helpers are explicitly <code>non_crypto</code>; they are not a
cryptographic or general integrity guarantee. CI and focused smoke checks verify the
documented source/contract boundary only. Event and decision serialization
remains payload-free, bounded, and connector-neutral; host integrations remain
responsible for their own request/response and transport behavior.

## Configuration and build boundaries

Host/connector configuration, Common Runtime key/value configuration, and
ModSecurity Engine <code>Sec*</code> directives are separate layers. The
repository-wide overview is [Configuration](configuration.md); complete
connector directive references remain under <code>examples/&lt;connector&gt;/</code>.

Builds materialize outside the checkout and remain separate from configuration
load, host startup, traffic execution, and evidence promotion. The current
compiler/build entry points are [Build documentation](build/README.md).

## Historical context

Earlier extraction plans, refactor reviews, migration plans, and per-topic
Common notes were consolidated here. Git history retains their detailed
chronology. The current rule is unchanged: move connector-neutral code only
when ownership, source attribution, build behavior, and host evidence remain
explicit and reviewable.

## Related references

- [Configuration and runtime guidance](configuration.md)
- [Testing and evidence](testing-and-evidence.md)
- [Operations and security](operations-and-security.md)
- [Variables](reference/variables.md) and [glossary](reference/glossary.md)
- [Common source-tree guide](../common/README.md)
