# Envoy ext_proc transport-hardening boundary

This note covers the repository-owned HTTP `envoy.filters.http.ext_proc` path for pinned Envoy `1.38.2`. It is separate from legacy `ext_authz` and does not promote a capability.

## API audit and post-commit strict boundary

The selected configuration uses `STREAMED` request and response bodies. A successful ext_proc `CONTINUE` for response headers is an adapter ordering boundary only: it means the processor sent a response to Envoy, not that a downstream client byte has been observed.

The pinned `ProcessingResponse` API offers `BodyResponse`, stream closure, and `ImmediateResponse`. Its source documentation says that an `ImmediateResponse` after a response has started may either reach the downstream codec as a local reply or reset the stream. That is not deterministic, protocol-specific, client-observed reset evidence. The selected processor intentionally sends no post-commit `ImmediateResponse` and does not turn a gRPC error into a reset. See Envoy's [pinned `v1.38.2` ext_proc proto](https://github.com/envoyproxy/envoy/blob/v1.38.2/api/envoy/service/ext_proc/v3/external_processor.proto).

| Downstream protocol | Selected host/API state | Evidence state |
| --- | --- | --- |
| HTTP/1.1 | The host probe has a cleartext HTTP/1 listener; Strict continues as `strict_abort_not_attempted` | Post-commit client abort is `NOT EXECUTED` |
| HTTP/2 | The gRPC service cluster uses HTTP/2, but the repository-owned downstream listener has no TLS/ALPN or forced H2 profile | No downstream `RST_STREAM` evidence; `NOT EXECUTED` |
| HTTP/3 | No QUIC listener or HTTP/3 client profile is selected | `NOT EXECUTED` |

A future Strict implementation must use a pinned, request-local Envoy HTTP filter or verify the exact `ImmediateResponse` behavior with a real client for each protocol. It must prove a committed response, a visible first body byte, an incomplete response (or a concrete H2 reset code), exactly-once cleanup, and an independent healthy follow-up. A gRPC close, service error, or synthetic HTTP 403 is not enough.

## Opt-in client-cancel observation

The normal smoke stays short. An opt-in transport probe now:

1. uses a real cleartext HTTP/1 client that waits for headers and one body byte;
2. closes that client connection while the test upstream deliberately holds its final chunk;
3. requires exactly one ext_proc terminal completion record for that transaction
   with either `grpc_context_canceled_unattributed` or `grpc_peer_eof`; and
4. requires an independent follow-up request to succeed.

Run it only with the real pinned Envoy/ext_proc host path:

```sh
make -C connectors/envoy transport-cancel-smoke-envoy-ext-proc
```

The target is equivalent to setting `ENVOY_TRANSPORT_CANCEL_PROBE=1` for
`runtime-smoke-envoy-ext-proc`.

The result is a payload-free, non-promoting `transport-observations.diagnostic.json`. It records the client-side first-byte/close observation, the one completion record, host survival, and the follow-up result, but deliberately contains no synthetic canonical correlation fields. Both permitted service-level terminal labels remain unattributed: ext_proc cannot identify whether Envoy observed a downstream client reset, an upstream failure, or another stream termination reason. Therefore it does not promote client-cancel, upstream-reset, Strict, HTTP/2, or HTTP/3 capabilities.

## Lifecycle and non-claims

The processor owns one transaction state per gRPC stream and its cancellation path calls `Close` once. Unit tests cover exactly-once cancellation cleanup and the absence of a fabricated host action. A source/unit test or the opt-in sidecar alone is not a downstream reset proof; it is never treated as one.
