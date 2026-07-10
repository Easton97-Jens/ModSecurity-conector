# Envoy Connector Origin

Status: repository-local ext_authz connector source
Runtime status: `minimal_runtime_smoke` for the HTTP ext_authz request path

No upstream Envoy connector source has been imported into this repository.

## Source Evidence

| Field | Value |
| --- | --- |
| Component | ModSecurity Envoy ext_authz connector |
| Upstream Envoy source | not selected |
| Upstream connector source | not selected |
| Source branch | not selected |
| Source commit | not selected |
| Source describe/version | not selected |
| License for imported upstream code | not selected |
| Imported upstream files | none |
| Local source kind | repository-local ext_authz service and bridge self-test |

The C source in `connectors/envoy/metadata.*` and `connectors/envoy/src/` is
repository-local code. It is not copied from Envoy, proxy-wasm, ext_proc, gRPC,
protobuf, or a ModSecurity connector upstream.

## Claims Not Made

- No native Envoy HTTP filter implementation is imported or implemented.
- No Envoy external processing service is imported or implemented.
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
