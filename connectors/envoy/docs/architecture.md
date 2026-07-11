# Envoy Connector Architecture

Status: the targeted ext_authz request path is `minimal_runtime_smoke` /
`connector-gap`. The separate ext_proc source is build-tested only and has no
runtime or capability promotion.

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

## Separate ext_proc source boundary

`ext_proc/cmd/msconnector-envoy-ext-proc` implements the official Go
`ExternalProcessor` gRPC service with one `streamState` per `Process` stream.
`config/envoy-ext-proc-streaming.yaml.in` selects `STREAMED` request and
response body modes. The Go adapter bounds headers/chunks/totals, forwards each
chunk immediately to an `Engine` transaction seam, and retains only counters.
EOS, gRPC cancellation, and graceful shutdown call the transaction cleanup
seam. Envoy-specific protobuf types remain under `connectors/envoy/ext_proc`;
none are added to `common/`.

The currently wired engine is `PassthroughEngine`, not Common/libmodsecurity.
This is intentional groundwork rather than an adapter-owned transaction path.
For a request-phase decision before response headers, the code can form an
`ImmediateResponse`. Once response headers have been observed, it always emits
the matching continue response. `minimal`/`safe` record `log_only`; `strict`
records `strict_abort_not_attempted`. A gRPC error is not represented as a
stream reset, and cancellation is not attributed to client versus upstream.

Thus no ext_proc runtime, HTTP/1.1/HTTP/2, timeout, reset, first-byte,
libmodsecurity, or response-body capability has been verified.

## Lifecycle and evidence

- `build-envoy-connector`: compile/link only.
- `check-envoy-config`: load config, initialize runtime/rules, then clean up.
- `start-smoke-envoy`: validate and start/stop Envoy plus connector service
  without requests.
- `runtime-smoke-envoy`: real Envoy 200/403 request path with clean shutdown.
- `build-envoy-ext-proc`, `test-envoy-ext-proc`, and
  `check-envoy-ext-proc-config`: isolated Go source/build/config gates only.

The legacy `envoy_bridge` remains self-test-only and is not part of this flow.
