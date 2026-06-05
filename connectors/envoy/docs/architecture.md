# Envoy Architecture

Status: bridge-starter
Runtime status: not-verified

The selected repository-backed Envoy integration path is a sidecar/HTTP bridge
starter. Native Envoy filter, ext_proc, and proxy-wasm implementations remain
deferred because this checkout does not contain Envoy SDK/API headers,
proxy-wasm SDK headers, Envoy ext_proc protobuf or gRPC bindings, or an Envoy
runtime harness.

## Repository Evidence

- `common/` provides connector-neutral request, response, transaction,
  intervention, status, origin, logging, and capability shapes without depending
  on a server SDK.
- Apache and NGINX have adapter-owned source plus server-specific build and
  harness files.
- Envoy now has repository-local metadata and a bridge starter that models
  request data and returns an intervention decision in a CLI self-test.

## Target parity with Apache/NGINX

Envoy should eventually prove the same core gates that Apache and NGINX prove in
this repository:

| Capability | Envoy bridge-starter status |
| --- | --- |
| Request headers inspection | local self-test model only; no Envoy traffic |
| Request URI / args inspection | local self-test model only; no Envoy traffic |
| Request body inspection | not implemented |
| CRS loading | not implemented |
| Blocking decision | local self-test returns `msconnector_intervention` 403 only |
| No-CRS runtime | not-run |
| With-CRS runtime | not-run |
| RESPONSE_BODY | separate gate; not verified |

The bridge starter is a step toward request and intervention mapping. It is not
Apache/NGINX-equivalent runtime evidence.

## Integration Options

| Option | Current status | Reason |
| --- | --- | --- |
| Native Envoy HTTP filter | deferred | Envoy C++ SDK/API headers are not present in this repository. |
| External processing service | deferred | ext_proc protobuf/gRPC generated sources and service dependencies are not present. |
| proxy-wasm/WASM | deferred | proxy-wasm SDK and WASM build toolchain are not present. |
| Sidecar/HTTP bridge | selected starter path | A local C CLI can model request/intervention decisions using `common/` without fake Envoy APIs. |

## Selected Minimal Path

The selected path for this change is a sidecar/HTTP bridge starter. It compiles
`connectors/envoy/src/envoy_bridge.c`, `envoy_bridge_main.c`, and Envoy metadata
with connector-neutral `common/` code. The self-test exercises allow and block
branches using local request data and `msconnector_intervention`.

No Envoy API, libmodsecurity transaction lifecycle, HTTP filter hook, ext_proc
service, proxy-wasm function, CRS load, or Envoy runtime request handling is
implemented or claimed.

Global references:

- `reports/template-verification-nginx-apache/connector-scaffold-decisions.md`
- `connectors/_template/docs/coverage-decision-matrix.md`
