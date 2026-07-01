# Common connector SDK scaffolding

`common/` contains connector-neutral C99 data models and helpers intended for future connector integration. These APIs do not automatically make NGINX, Apache, HAProxy, Envoy, Traefik, lighttpd, or any other connector support a feature. Each connector remains separately compiled and must explicitly map its own server APIs to these models in a later change.

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
