# Envoy `ext_proc` Common/libmodsecurity full-lifecycle path

**Language:** English | [Deutsch](README.de.md)

This directory is a pinned Go implementation of Envoy's official
`envoy.service.ext_proc.v3.ExternalProcessor` gRPC interface. It is separate
from the existing C `ext_authz` service and does not change that selected,
runtime-evidenced request-only path.

The canonical full-lifecycle dispatcher selects this service through
`full-lifecycle-envoy-ext-proc`; it does not fall through to the standard
`ext_authz` compatibility runner. The executable links a connector-local CGo
ABI to Common Runtime and libmodsecurity, while capability promotion remains a
separate evidence-review decision.

## What is implemented here

- one independent `streamState` and transaction seam per gRPC `Process` call;
- one real Common/libmodsecurity transaction per stream, opened from Envoy's
  actual request headers and destroyed on EOS, cancellation, or processor
  failure;
- bounded request/response header mapping and incremental body callbacks;
- no full request or response body collection; state retains counters only;
- explicit request/response body finish calls for header EOS, body EOS, and
  trailer EOS;
- downstream protocol and endpoints mapped from requested Envoy attributes,
  never inferred from the Envoy-to-service gRPC socket;
- matching `HeadersResponse` / `BodyResponse` messages for `STREAMED` mode;
- EOS cleanup, gRPC-context cancellation cleanup, and bounded graceful stop;
- pre-commit request and response decisions mapped to `ImmediateResponse`,
  with Common host-action metadata recorded only after the matching gRPC send
  succeeds;
- raw Common decision JSONL under the per-run runtime root plus a separate
  payload-free completion log; the latter is supplementary and never replaces
  the Common event stream;
- unit and CGo lifecycle tests covering P1/P2/P3/P4, incremental EOS,
  cancellation, commit ordering, and parallel transactions.

The pinned dependency is the official generated Envoy Go API module in
`go.mod`/`go.sum`. `../config/envoy-ext-proc-versions.env` records the intended
Envoy release (`1.38.2`) and `../config/envoy-ext-proc-streaming.yaml.in` uses
only `STREAMED` body modes, never `BUFFERED`.

## Explicit non-claims and late-action behavior

The shipped build uses `-tags libmodsecurity`; a source-only Go build retains a
PassthroughEngine only for protobuf/unit development and refuses a runtime
config. The normal build requires local libmodsecurity headers and library
paths, then links Common Runtime into the ext_proc executable.

The service uses the conservative response-commit boundary: only a successful
response-header `CONTINUE` send marks a response as committed. For a disruptive
decision found later:

- `minimal` and `safe` record a real Common host outcome `log_only` and
  continue with the original visible response status;
- `strict` records `strict_abort_not_attempted` and continues.

`strict` intentionally does not turn into a gRPC error, `ImmediateResponse`, or
a claimed reset. Those mechanisms do not independently prove a deterministic
client-visible abort in Envoy. A canceled gRPC context and an observed gRPC
peer EOF are recorded respectively as `grpc_context_canceled_unattributed` and
`grpc_peer_eof`; neither label can honestly be treated as a downstream client
reset or an upstream reset.

## Local source/build commands

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absolute/path/to/envoy
```

`runtime-smoke-envoy-ext-proc` starts a real pinned-compatible Envoy process,
the CGo/Common gRPC service, and a local upstream. It saves effective Envoy and
Common configurations, raw Common JSONL, and a separate metadata-only
completion log outside the checkout. The host smoke exercises P1, P2, P3 deny,
P3 redirect, and P4 post-commit safe/log-only behavior. It remains
non-promoted until the canonical collector and capability review accept the
raw host evidence.

## Remaining promotion boundary

The service does not claim a deterministic post-commit reset or a client-byte
observation. A late P4 rule is deliberately recorded as host-confirmed
`log_only`; `strict` remains `strict_abort_not_attempted`. Those limits, and
the canonical collector's independent validation of the raw Common JSONL, are
the remaining promotion boundary.
