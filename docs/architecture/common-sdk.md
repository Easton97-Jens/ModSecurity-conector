**Language:** English | [Deutsch](common-sdk.de.md)

# Common connector SDK scaffolding

`common/` contains connector-neutral C17-oriented data models and helpers intended for future connector integration. These APIs do not automatically make NGINX, Apache, HAProxy, Envoy, Traefik, lighttpd, or any other connector support a feature. Each connector remains separately compiled and must explicitly map its own server APIs to these models in a later change.

## Modules

- `config`: shared configuration value model, merge, defaults, and validation helpers.
- `directive_spec`: semantic catalog of common directive names and value shapes; server-specific directive registration remains connector-owned.
- `headers`: case-insensitive lookup helpers for `msconnector_header` arrays.
- `body_policy`: request/response body support model only; it does not claim runtime support.
- `transaction_state`: connector-neutral transaction phase bookkeeping.
- `decision_action`: high-level action names derived from common decisions/interventions.
- `late_intervention`: decision model for disruptive actions after response output begins.
- `event` and `json_escape`: metadata event model and deterministic JSON escaping. Request/response bodies are not represented.
- `redaction`: small redacted-string copy helpers for log output.
- `artifacts`: relative default artifact file names.
- `adapter_metadata`: common metadata shape for future connector metadata migration.
- `lifecycle_status`: shared build/runtime/verification vocabulary only.
- `test_result`: small smoke/runtime result metadata model.
- `path_policy`: conservative path checks for generated artifacts.

## Integration status

Connector integration is future work. This document and the common SDK scaffolding do not claim production readiness, connector capability support, runtime support, or full-matrix readiness.

## HTTP status metadata

The common HTTP status table is connector-neutral metadata for reason phrases,
default connector-neutral messages, status classes, and block-response
suitability. It does not change connector runtime responses. NGINX, Apache,
HAProxy, Envoy, Traefik, lighttpd, and future connectors must explicitly map to
this metadata in later connector-specific changes before any runtime response
message behavior can be claimed.

## Event and log message model

The common event model is connector-neutral metadata intended for future runtime
integration. It does not change existing connector logs by itself. The model
avoids request and response body payloads by design, and includes message IDs,
short operator-facing messages, HTTP status metadata, action metadata,
redaction markers, and truncation markers so future connector integrations can
produce understandable logs without leaking payloads by default. The C event
structure groups those fields into nested connector-neutral sections for
metadata, decisions, HTTP status data, request-identifying data, and flags; this
layout is only a data model and does not imply runtime log integration.

### Phase 4 hard abort after HTTP 200

If Phase 4 detects a blocking rule after a response has already started with
HTTP 200, a connector may not be able to send a clean replacement HTTP status.
The common event model represents this with
`MSCONN_EVENT_PHASE4_HARD_ABORT_AFTER_200` and the short message:
"Response already started with HTTP 200; Phase 4 requested a block; connection
was aborted."

No connector currently emits this event from this common model in this PR.

## Header policy

Common header helpers perform case-insensitive lookup, first/last duplicate
selection, and duplicate counts. Content-Type matching accepts an exact media
type or a parameter separator after optional whitespace; whitespace followed by
other text is not treated as a match. `Set-Cookie`, `Cookie`, `Content-Length`,
and `Host` are not treated as comma-combinable by the common helper. Duplicate
identical `Content-Length` values are accepted by the parser, while conflicting,
empty, signed, invalid, or overflowing values fail. Header log sanitizing
replaces control characters so multiline values are not emitted directly; it is
not redaction and connectors remain responsible for not passing secrets.

## Decision model

The common decision model represents connector-neutral outcomes: allow,
log-only, deny, redirect, drop, connection-abort, error, and unsupported. It can
map decisions to common events, including action names and HTTP status metadata.
This is only a data model until a connector explicitly adopts it.

## Error model

The common error model defines stable error codes, default messages, status
mapping, HTTP status mapping, fatal classification, and conversion to common
events. It does not change connector error handling by itself.

## Rule loader

The rule loader is an orchestration helper around caller-provided backend
callbacks for inline, file, and remote rules. It tracks `msconnector_rule_load_stats`
but does not own the native rules object and does not include libmodsecurity
headers.

## ModSecurity engine facade

The ModSecurity engine facade is a connector-neutral lifecycle and transaction
phase wrapper around caller-provided backend callbacks. It does not include or
link libmodsecurity by itself. Actual libmodsecurity bindings remain future
connector-specific or optional adapter work.

## Transaction ID policy

The transaction ID resolver checks sources in this order: static config ID,
config expression callback, host request ID, configured header, then fallback ID.
Resolved IDs must be non-empty printable ASCII, must not contain CR/LF or other
control characters, and must fit the fixed common result buffer without
truncation.

## Common-only merge-blocker infrastructure

The SDK also includes connector-neutral scaffolding for adapter interfaces,
adapter contract checks, capability-to-test mapping, JSONL event output,
runtime artifact layout, and runtime path validation. These helpers are Common
SDK infrastructure only. They do not start connector runtimes, do not link
libmodsecurity, and do not change NGINX, Apache, HAProxy, Envoy, Traefik, or
lighttpd behavior.

## Header policy

Header helpers perform case-insensitive lookup, trim leading optional whitespace
for Content-Type media-type comparisons, reject garbage suffixes after the media
type, keep Set-Cookie/Cookie/Content-Length/Host out of blind comma-combining,
and parse duplicate Content-Length values only when they are identical. Log
sanitizing replaces control characters; it is not redaction.

## Adapter and connector contract model

The adapter interface and contract helpers define what a future connector may
provide: metadata, capabilities, phase callbacks, decisions, events, and
artifacts. Existing connectors are not migrated by this change and must adopt the
interface explicitly in later connector-specific work before runtime behavior can
be claimed.

## Artifact and path policy

The common artifact layout defines standard names such as `result.json`,
`decision.jsonl`, `audit.log`, and `error.log`. Runtime path joining rejects
absolute artifact names, Windows absolute and UNC names, and parent traversal.

## Remaining package helpers

The common SDK package now also includes config parser helpers, request and
response validation helpers, rule collection merge helpers, rule error/event
helpers, test-result JSON, connector manifests, runtime report skeletons, origin
governance, build-contract targets, C++ header-only wrappers, central resource
limits, rule-ID extraction, log sanitizing, and body-snippet redaction. These are
connector-neutral scaffolding only and do not migrate or verify any connector.
They do not add a real libmodsecurity binding and do not claim production or
full-matrix readiness.

## Global adapter contracts for new connectors

Common now also exposes connector-neutral contracts for future host adapters:

- `directive_adapter`: a deterministic directive adapter catalog derived from `directive_spec`. It gives future adapters canonical names, host-visible names, scopes, and argument policies without generating host directive types.
- `request_mapper_contract`: the minimum request fields and limits that a host mapper must satisfy when it converts a server request into `msconnector_request`.
- `response_mapper_contract`: the equivalent response-output contract for `msconnector_response`, including HTTP status validation and header/body limits.
- `crs`: a neutral CRS/ruleset setup convention for disabled, external path, bundled path, and test fixture configurations.

These contracts are global SDK surface only. They do not migrate NGINX, Apache, HAProxy, Envoy, lighttpd, or Traefik runtime code, and they do not claim CRS runtime verification, production readiness, or full-matrix coverage.

Host-specific APIs stay in connector-owned code. Examples include `ngx_command_t`, `ngx_http_request_t`, `ngx_chain_t`, Apache `command_rec`, Apache `request_rec`, APR pools, bucket brigades, and server hooks/filters. NGINX and Apache can later implement thin mappers on top of these contracts, but this SDK layer does not assert that they already do.

## Apache adoption boundary

Apache now consumes the Common SDK for the adopted semantic layer: embedded
`msconnector_config`, Common parser helpers, directive spec/adapter lookup,
request/response mapper contracts, and metadata-only event JSONL primitives.
Apache still owns Apache server APIs such as `request_rec`, `command_rec`,
hooks, filters, APR pools, bucket brigades, APLOG, return codes, and APXS
build glue. This is not a production, CRS, full-matrix, or runtime verification
claim.

## NGINX adoption boundary

NGINX now consumes the Common SDK for shared configuration defaults/merge/validate,
directive catalog contracts, mapper contracts, header helpers, event/limit-facing
helpers, and compile-only C17 checks where wired. NGINX-specific APIs stay in the
NGINX connector: `ngx_command_t`, `ngx_http_request_t`, `ngx_chain_t`,
`ngx_buf_t`, filters, pools, return codes, and build glue. The NGINX C17 check is
blocked with exit 77 when NGINX/libmodsecurity headers are absent; C23/future-C
checks are optional and do not imply runtime verification.

## HAProxy adoption note

The HAProxy connector is expected to consume the Common SDK for connector-neutral semantics: configuration, directive specs/adapters, primitive parsers, mapper contracts, event JSONL, redaction, resource limits, guards, CRS setup contracts, artifact/test-result contracts, and status/error mapping. HAProxy-specific SPOE/SPOP protocol code, HAProxy cfg glue, runtime process handling, frame parsing, socket handling, and build integration remain adapter-owned. C17 compile evidence is structural only and must not be described as production, CRS, full-matrix, or runtime verification.

## Remaining connector starter adoption

Envoy, Traefik, and lighttpd now carry connector-local Common SDK mapper scaffolding for `msconnector_config`, `msconnector_request`, and `msconnector_response`. This is a structure/compile contract only. Host API glue, runtime lifecycle, build glue, protocol/frame handling, event artifact callsites, and libmodsecurity transaction ownership remain connector-specific work. These connectors must remain `not_verified` / `connector-gap` until runtime evidence exists.

## Generic mapper helper

The Common SDK includes `msconnector_generic_map_request()` and `msconnector_generic_map_response()` for starter connectors that already have connector-neutral request and response fields. Envoy, Traefik, and lighttpd use this helper through thin local adapters. The helper does not take ownership of headers or body bytes, does not log body payloads, and does not change their `not_verified` / `connector-gap` status.
The remaining starter connectors now avoid connector-local mapper source copies by aliasing their map entry points to the connector-neutral generic mapper; this keeps duplicated Host lookup, validation, and body metadata assignment in one Common implementation only.

Generic mapper callers must pass `hostname` as a NUL-terminated string when it is set; header value slices are never exposed as C-string hostnames. Nonzero body sizes require non-NULL body data and remain metadata-only unless the caller owns safe body bytes.
