# Envoy Connector Architecture

Status: the targeted ext_authz request path is `minimal_runtime_smoke` /
`connector-gap`. The separate ext_proc path has connector-local real-Envoy
Common/libmodsecurity host evidence but no capability promotion.

## Selected host model

The selected, canonical connector path implements Envoy's external HTTP
`ext_authz` model. Envoy sends
request metadata, selected headers, and an optional bounded buffered request
body to a connector-owned service. No Envoy SDK types cross into Common.

`src/envoy_ext_authz_service_main.c` owns the Envoy-specific profile:

- connector name `envoy`;
- integration mode `ext_authz`;
- original-URI header preferences;
- request and response mapper callbacks.

`src/envoy_modsecurity_mapper.c` is a thin C17 adapter over the Common generic
mapper. `common/runtime` owns config parsing and validation, resource/body
limits, rule loading, libmodsecurity engine/transaction lifecycle, transaction
IDs, decision/action mapping, and metadata-only event JSONL.

## Request flow

```text
client -> Envoy HTTP connection manager -> ext_authz HTTP request
       -> msconnector_envoy_ext_authz -> Common mapper/runtime
       -> libmodsecurity decision -> ext_authz allow/deny
       -> upstream or local 403
```

The checked-in Envoy smoke config forwards `content-length`, `content-type`,
`x-modsec-smoke`, and `x-request-id`; buffers at most 4096 request bytes and does
not permit partial bodies. Connector config independently enforces header, body,
event, and transaction constraints.

## Response boundary

HTTP `ext_authz` executes before upstream routing. It cannot inspect the
upstream response. The response mapper is linked and contract-checked for API
completeness, but response headers and bodies are unsupported in this host
model. A later response-phase implementation would require a separately proven
model such as `ext_proc`; it must not be inferred from this connector.

## Separate ext_proc Common-runtime boundary

`ext_proc/cmd/msconnector-envoy-ext-proc` implements the official Go
`ExternalProcessor` gRPC service with one `streamState` per `Process` stream.
The normal CGo build selects `CommonRuntimeEngine`, whose connector-local C ABI
opens a real Common/libmodsecurity transaction from actual Envoy request
headers. `config/envoy-ext-proc-streaming.yaml.in` selects `STREAMED` request
and response body modes. The Go adapter bounds headers/chunks/totals, forwards
each chunk immediately, and retains only counters. It maps Envoy-requested
protocol and endpoint attributes rather than inventing the gRPC peer address.
EOS, gRPC cancellation, processor failure, and graceful shutdown clean up the
native transaction. Envoy-specific protobuf types remain under
`connectors/envoy/ext_proc`; none are added to `common/`.

Raw Common decision JSONL is written to a per-run event path and is the
canonical connector-local evidence source. The separate completion log contains
only stream metadata. Pre-commit disruptive P1/P2/P3 decisions form an
`ImmediateResponse`; the Common host outcome is recorded only after the
matching gRPC send succeeds. A successful response-header `CONTINUE` is the
adapter's conservative commit boundary. A late P4 decision in `minimal`/`safe`
is recorded as `log_only`; `strict` records `strict_abort_not_attempted`. A
gRPC error is not represented as a stream reset, and cancellation is not
attributed to client versus upstream.

`runtime-smoke-envoy-ext-proc` validates the generated YAML with real Envoy and
performs local HTTP/1.1 P1/P2/P3/P4 traffic. It verifies raw Common rule events
and host-confirmed deny, redirect, and safe log-only outcomes. It does not prove
timeout/reset semantics, first-byte or client-byte behavior, HTTP/2 behavior,
canonical result collection, or a promoted response-body capability.

## Lifecycle and evidence

- `build-envoy-connector`: compile/link only.
- `check-envoy-config`: load config, initialize runtime/rules, then clean up.
- `start-smoke-envoy`: validate and start/stop Envoy plus connector service
  without requests.
- `runtime-smoke-envoy`: real Envoy 200/403 request path with clean shutdown.
- `build-envoy-ext-proc`, `test-envoy-ext-proc`, and
  `check-envoy-ext-proc-config`: pinned Go source/build/config gates; with
  libmodsecurity paths, the build/test target also runs the CGo Common bridge.
- `runtime-smoke-envoy-ext-proc`: real Envoy ext_proc/Common/libmodsecurity
  host smoke, explicitly marked `common_libmodsecurity_nonpromoted`.

The legacy `envoy_bridge` remains self-test-only and is not part of this flow.
