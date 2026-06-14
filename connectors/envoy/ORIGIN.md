# Envoy Connector Origin

Status: bridge-starter
Runtime status: not-verified

No upstream Envoy connector source has been imported into this repository.

## Source Evidence

| Field | Value |
| --- | --- |
| Component | ModSecurity-envoy build starter |
| Upstream Envoy source | not selected |
| Upstream connector source | not selected |
| Source branch | not selected |
| Source commit | not selected |
| Source describe/version | not selected |
| License for imported upstream code | not selected |
| Imported upstream files | none |
| Local source kind | repository-local sidecar/HTTP bridge starter |

The current C source in `connectors/envoy/metadata.c`,
`connectors/envoy/metadata.h`, and `connectors/envoy/src/envoy_bridge*` is
repository-local starter code. It is not copied from Envoy, proxy-wasm,
ext_proc, gRPC, protobuf, or ModSecurity connector upstream code.

## Claims Not Made

- No native Envoy HTTP filter implementation is imported or implemented.
- No Envoy external processing service is imported or implemented.
- No proxy-wasm module is imported or implemented.
- No libmodsecurity adapter lifecycle is implemented.
- No Envoy runtime compatibility is verified.

## Local Bridge Starter

The local bridge starter models an HTTP request with connector-neutral
`msconnector_request` data, evaluates a deterministic self-test block/allow
signal, and returns an `msconnector_intervention`. This is a local CLI self-test
for the future sidecar/HTTP bridge path, not Envoy runtime evidence and not a
ModSecurity rule evaluation.
