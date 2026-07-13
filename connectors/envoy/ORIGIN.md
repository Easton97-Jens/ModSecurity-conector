# Envoy Connector Origin

**Language:** English | [Deutsch](ORIGIN.de.md)

Status: repository-local ext_authz connector source plus a non-promoted Go/CGo
ext_proc Common/libmodsecurity path selected by the full-lifecycle profile
Runtime status: `minimal_runtime_smoke` for the HTTP ext_authz request path

No upstream Envoy connector source has been imported into this repository.

## Source Evidence

| Field | Value |
| --- | --- |
| Component | ModSecurity Envoy ext_authz connector plus full-lifecycle-selected ext_proc transport path |
| Upstream Envoy source | not selected |
| Upstream connector source | not selected |
| Source branch | not selected |
| Source commit | not selected |
| Source describe/version | not selected |
| License for imported upstream code | not selected |
| Imported upstream files | none |
| Local source kind | repository-local ext_authz service, bridge self-test, and ext_proc CGo/Common stream adapter |

The C source in `connectors/envoy/metadata.*` and `connectors/envoy/src/`, and
the Go source in `connectors/envoy/ext_proc/`, are repository-local code. They
are not copied from Envoy, proxy-wasm, gRPC, protobuf, or a ModSecurity
connector upstream. The ext_proc build resolves official generated Envoy Go API
dependencies through the pinned module/checksum files; no generated upstream
protobuf code is checked into this repository.

## Claims Not Made

- No native Envoy HTTP filter implementation is imported or implemented.
- No Envoy external processing service is imported. A repository-local Go/CGo
  ext_proc service links Common Runtime and libmodsecurity and has a bounded
  real-Envoy HTTP/1.1 rule/action smoke; that evidence is non-promoted and is
  not canonical collection or production verification.
- No proxy-wasm module is imported or implemented.
- The connector delegates libmodsecurity lifecycle to the connector-neutral
  `common/runtime` API rather than embedding host-specific runtime code.
- No response-phase, CRS, security, full-matrix, or production compatibility is
  verified by the minimal request-path smoke.

## Local Bridge Starter

The local bridge starter models an HTTP request with connector-neutral
`msconnector_request` data, evaluates a deterministic self-test block/allow
signal, and returns an `msconnector_intervention`. This is a local CLI self-test
for the future sidecar/HTTP bridge path, not Envoy runtime evidence and not a
ModSecurity rule evaluation.

## Local ext_authz service

`envoy_ext_authz_service_main.c` defines a repository-local Envoy host profile
for the connector-neutral HTTP authorization service. No Envoy SDK source or
types are imported: Envoy communicates with the service through its external
HTTP `ext_authz` protocol. Compile, start, and real Envoy request evidence remain
separate promotion gates.

## Local ext_proc Common-runtime path

`ext_proc/` uses Envoy's official generated Go external-processing API through
the pinned `github.com/envoyproxy/go-control-plane/envoy` module. It keeps
protobuf types local to the connector and has per-stream bounded state,
incremental body callbacks, EOS/cancellation cleanup, and a `STREAMED` Envoy
template. The normal CGo executable opens a real Common/libmodsecurity
transaction for each stream. `runtime-smoke-envoy-ext-proc` separately validates
generated YAML with real Envoy and records run-local raw Common decision JSONL
plus payload-free completion metadata. It has bounded HTTP/1.1 P1/P2/P3/P4
rule/action evidence but does not promote a capability.
