# Native Traefik middleware source

**Language:** English | [Deutsch](README.de.md)

This is a repository-owned Go package shaped for Traefik's Go middleware
entry points: `CreateConfig`, `New`, and `ServeHTTP`. `New` has the required
`(http.Handler, error)` signature, and `.traefik.yml` records plugin metadata
and test data. It uses only the Go standard library; Traefik supplies the next
`http.Handler` when it loads a plugin. The full-lifecycle runner stages this
package below a pinned Traefik local-plugin workspace; it does not replace the
existing C `forwardAuth` compatibility service or alter its capability
declaration.

## What the source does

- reads the entire request body before calling the next handler, with reads
  capped to `maxRequestChunkBytes` and sent synchronously to the per-request
  `Transaction`; only a complete allowed request EOS admits the handler;
- buffers at most `maxRequestBodyBytes` (hard cap: 1 MiB) for byte-exact replay
  to the next handler, without inspecting replayed bytes a second time;
- enforces `requestBodyIdleTimeoutMillis` independently of the engine timeout
  and `maxRequestBodyBytes`; an idle or cancelled body fails closed before
  the next handler runs and its owned source is closed;
- shortens the host response controller's read deadline only after idle/cancel,
  since a server body's `Close` alone does not unblock a concurrent `Read`;
  successful reads never replace or clear the operator's absolute ReadTimeout.
  It follows wrappers exposing `Unwrap`. A wrapper hiding both deadlines and
  `Unwrap` returns `ErrNotSupported`; custom sources in that fallback must unblock
  reads on `Close`. Idle enforcement for a real HTTP body behind such an opaque
  wrapper requires a host read timeout and is not established by source tests;
- applies the finite `maxRequestBodyBytes` aggregate limit (default and hard
  cap: 1 MiB) before an over-limit chunk reaches the engine. The deterministic
  pre-commit action is HTTP 413; after that decision it stops inspecting and
  forwarding request bytes. The host-owned `Body.Close` may drain remaining
  bytes within the configured idle deadline;
- rejects truncated declared bodies (including nil/`NoBody` with a positive
  Content-Length) and read/engine failures through the
  closed HTTP 500 path, without downstream invocation or invented request EOS;
- wraps the response writer, evaluates response headers before commitment, and
  slices every `Write` into `maxResponseChunkBytes` callbacks before forwarding
  each slice;
- implements `http.Flusher`, `http.Hijacker`, `http.Pusher`, `io.ReaderFrom`,
  and `Unwrap`; `ReadFrom` keeps the wrapped writer's fast path after one
  bounded first chunk;
- keeps only metadata and byte/chunk counters in `Summary`, never a complete
  request or response body;
- derives `Metadata.ServerAddress` and `Metadata.ServerPort` only from the
  host-provided `http.LocalAddrContextKey`; a missing, non-IP, or invalid-port
  local endpoint returns HTTP 500 before the engine is opened, while the
  client-controlled request authority remains only `Metadata.Hostname`;
- treats a disruptive result after response commitment as `log_only`; it does
  not synthesize a changed status, reset, or client-abort claim.

The engine shape is fail-closed by default: an omitted `engineMode` selects
`uds`, and `New` requires a valid private Unix-domain-socket path before it can
reach the persistent Common/libmodsecurity engine service. The selected host
runner supplies a private socket and run-local event path. The checked-in
dynamic example names an expected private runtime path but does not materialize
or reuse a socket object. The production plugin constructor accepts only
`engineMode: uds`; it rejects an always-allow passthrough selection before a
handler is created. The injected engine seam is package-private test code, not
an operator-facing configuration path. The package proves targeted P1--P4 host
behavior without promoting a capability, CRS completeness, Safe/Strict, or
production readiness.

The Go client validates the socket path lexically and bounds every frame, but
does not claim portable peer-credential authentication. On platforms where
the host requires a distinct service identity, the runtime must enforce that
identity through the private socket parent and deployment permissions; adding
an OS-specific `SO_PEERCRED` check requires an explicit supported-platform
contract and is not implied by this package.

The trusted-local-endpoint mapping protects only server-endpoint provenance.
It does not authenticate a later UDS peer and therefore does not resolve
FND-PARENT-0015's socket-replacement risk.

The UDS protocol rejects unknown engine actions instead of relabelling them as
an HTTP denial. It reports a disruptive outcome only after the actual
`ResponseWriter` write succeeds. After response commitment a disruptive Phase
4 result is deliberately `log_only`; it does not synthesize a changed status,
reset, or client-abort claim.

## UDS cancellation, timeout, and cleanup boundary

Each `ServeHTTP` transaction owns one private UDS connection; it is never
reused by a following request. Each request/streaming exchange applies the smaller of the
configured engine timeout and the request-context deadline. A context
cancellation shortens the connection deadline immediately, unblocks a pending
read or write, and joins its watcher before the call returns. A timeout,
cancellation, peer reset, invalid result, or incomplete result discards the
connection, closes its FD, and marks only that transaction terminal so no
partial frame can be reused. `Close` is idempotent even when an earlier
exchange already discarded the connection.

After a regular handler return, a response with an explicit Content-Length
fully accepted by the host writer can finish even if the client closes after
reading the last byte. Only this complete response, with no read/write error or
hijack, uses a context retaining request values but with an independent one-second
deadline for the final body-commit acknowledgement, response EOS, and cleanup.
Unknown or incomplete lengths and failed streams keep normal request cancellation.
An engine error never becomes successful response EOS in `Summary`.

Before a response is committed, the middleware turns an engine-exchange error
into its closed HTTP 500 path. A canceled host request may already have lost
its response channel, so the connector does not invent a client-visible
status or an upstream-reset event. After commitment it retains the documented
log-only/unchanged-response limit rather than claiming a retroactive rewrite.
A fresh request opens a new UDS session and keeps normal allow/block semantics.

## Local source checks

```sh
make -C connectors/traefik test-native-middleware
make -C connectors/traefik build-native-middleware
```

The build script runs `go test ./...`, `go vet ./...`, and (for `build`) `go
build ./...`. It writes only a compile report outside the checkout, defaulting
to `$BUILD_ROOT/traefik-native-middleware/build.txt`. It does not install a
Traefik plugin, start the persistent engine, call Common/libmodsecurity, or
write runtime evidence.

## Bounded UDS parser fuzzing

`FuzzUDSFrameAndResult` exercises the custom UDS frame reader and result parser
with truncated, malformed, allow, deny, and redirect seeds plus arbitrary
bounded frames. It uses an in-memory reader only: it does not open a socket,
start the engine, or invoke CGo/Common. A malformed frame must return an error
without a panic; each successfully parsed frame must round-trip to its consumed
bytes unchanged (additional stream frames may follow), and a successfully parsed
result must have a recognized action.

Run the same bounded control from this module directory:

```sh
GOTOOLCHAIN=local go test -mod=readonly -run='^$' -fuzz='^FuzzUDSFrameAndResult$' -fuzztime=15s -parallel=1 .
```

The `traefik-go` CodeQL job runs this control with the same 15-second,
single-worker bound. It is source-level parser evidence, not Traefik host-
runtime or capability-promotion evidence.

## Configuration boundary

`../config/traefik-native-middleware-static.yaml` and
`../config/traefik-native-middleware-dynamic.yaml` are matching local-plugin
and File Provider shapes for an operator-created registration named
`modsecurityNative`. They are deliberately separate from the selected
`../config/traefik-forwardauth-dynamic.yaml`. The
`full-lifecycle-traefik-native` host target independently stages an equivalent
disposable workspace, builds and starts the local engine service, and asserts
plugin loading in the pinned host. It does not reuse these checked-in reference
files or a shared engine socket. An operator deployment must still stage the
module under the local-plugin workspace used by its installed Traefik release.
The probe is not deployment or capability-promotion evidence.
