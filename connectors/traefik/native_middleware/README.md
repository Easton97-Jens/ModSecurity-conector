# Native Traefik streaming middleware source

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

- wraps the request body so reads are capped to `maxRequestChunkBytes` and sent
  synchronously to a per-request `Transaction` seam;
- wraps the response writer, evaluates response headers before commitment, and
  slices every `Write` into `maxResponseChunkBytes` callbacks before forwarding
  each slice;
- implements `http.Flusher`, `http.Hijacker`, `http.Pusher`, `io.ReaderFrom`,
  and `Unwrap`; `ReadFrom` keeps the wrapped writer's fast path after one
  bounded first chunk;
- keeps only metadata and byte/chunk counters in `Summary`, never a complete
  request or response body;
- treats a disruptive result after response commitment as `log_only`; it does
  not synthesize a changed status, reset, or client-abort claim.

The optional-engine shape is intentional. `New` defaults to
`PassthroughEngine` for a source-only configuration, while `engineMode: uds`
opens one private Unix-domain-socket session per `ServeHTTP` to the persistent
Common/libmodsecurity engine service. The selected host runner supplies its
own private socket and run-local event path; it does not reuse a checked-in
socket path. It proves targeted P1--P4 host behavior without promoting a
capability, CRS completeness, Safe/Strict, or production readiness.

The UDS protocol rejects unknown engine actions instead of relabelling them as
an HTTP denial. It reports a disruptive outcome only after the actual
`ResponseWriter` write succeeds. After response commitment a disruptive Phase
4 result is deliberately `log_only`; it does not synthesize a changed status,
reset, or client-abort claim.

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
