# Envoy `ext_proc` non-promoted full-lifecycle transport path

This directory is a pinned Go implementation of Envoy's official
`envoy.service.ext_proc.v3.ExternalProcessor` gRPC interface. It is separate
from the existing C `ext_authz` service and does not change that selected,
runtime-evidenced request-only path.

The canonical full-lifecycle dispatcher selects this service through
`full-lifecycle-envoy-ext-proc`; it does not fall through to the standard
`ext_authz` compatibility runner. That target establishes a real listener and
stream-callback route only, with no rule-action or capability promotion.

## What is implemented here

- one independent `streamState` and transaction seam per gRPC `Process` call;
- bounded request/response header mapping and incremental body callbacks;
- no full request or response body collection; state retains counters only;
- matching `HeadersResponse` / `BodyResponse` messages for `STREAMED` mode;
- EOS cleanup, gRPC-context cancellation cleanup, and bounded graceful stop;
- request-phase deny/redirect mapped to `ImmediateResponse` before response
  headers have been observed;
- a small unit test covering chunks, EOS, cancellation, pre-response deny, and
  the deliberately conservative late-action result.

The pinned dependency is the official generated Envoy Go API module in
`go.mod`/`go.sum`. `../config/envoy-ext-proc-versions.env` records the intended
Envoy release (`1.38.2`) and `../config/envoy-ext-proc-streaming.yaml.in` uses
only `STREAMED` body modes, never `BUFFERED`.

## Explicit non-claims and late-action behavior

The checked-in service installs `PassthroughEngine`. It has a narrow
incremental `Engine`/`Transaction` seam for a later Common/libmodsecurity
bridge, but it does **not** call `common/runtime` or libmodsecurity today.
Consequently it is an unpromoted transport-only runtime path, not a
full-lifecycle rule-evaluation implementation or capability evidence.

The service uses the conservative response-header boundary: once response
headers are observed, it never emits a later local status or claims to change a
visible status. For a disruptive prospective decision found later:

- `minimal` and `safe` record the adapter outcome `log_only` and continue;
- `strict` records `strict_abort_not_attempted` and continues.

`strict` intentionally does not turn into a gRPC error, `ImmediateResponse`, or
a claimed reset. Those mechanisms do not independently prove a deterministic
client-visible abort in Envoy. Likewise a canceled gRPC context is cleaned up
as `grpc_context_canceled_unattributed`; this service cannot honestly label it
as a downstream client reset or an upstream reset.

## Local source/build commands

```sh
make -C connectors/envoy build-envoy-ext-proc
make -C connectors/envoy test-envoy-ext-proc
make -C connectors/envoy check-envoy-ext-proc-config
make -C connectors/envoy prepare-envoy-ext-proc-config
make -C connectors/envoy runtime-smoke-envoy-ext-proc ENVOY_BIN=/absolute/path/to/envoy
```

`runtime-smoke-envoy-ext-proc` starts a real pinned-compatible Envoy process,
the Go `ext_proc` gRPC service, and a local upstream. It saves the effective
Envoy YAML and a metadata-only JSONL stream-completion record outside the
checkout. The record proves that Envoy delivered request and response body
bytes to `ext_proc`; it explicitly records
`evaluation_mode=passthrough_nonpromoted` and `rule_evaluation=not_wired`.
It is transport evidence only, not a rule-evaluation or capability promotion.

## Promotion blocker

The executable still instantiates `PassthroughEngine`. A genuine bridge needs a
connector-local CGo/C ABI around `common/runtime` that maps Envoy pseudo- and
ordinary headers to `msconnector_request`/`msconnector_response`, explicitly
calls the request/response body finish APIs at EOS, links libmodsecurity, and
maps the resulting metadata-only decisions back to the ext_proc stream. Until
that adapter is built and exercised through this real-host runner, this path
must remain `passthrough_nonpromoted`.
