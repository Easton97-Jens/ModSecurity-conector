# lighttpd Connector

Status: `minimal_runtime_smoke` for the native Phase-1 header path

The primary integration is now a repository-owned native lighttpd module. It
loads the connector-neutral runtime from `common/runtime`, maps real lighttpd
request and response headers into Common SDK models, evaluates ModSecurity, and
maps a disruptive Phase-1 decision to lighttpd with `http_status_set_err()`.

Verified locally against pinned lighttpd 1.4.84 and libmodsecurity:

- C17 compile and link of `mod_msconnector.so` with warnings as errors;
- real lighttpd module load and configuration check;
- real foreground start, PID check, and clean stop without sending a request;
- separate real-host runtime smoke: baseline `OPTIONS *` returns 200 and
  `X-Modsec-Smoke: block` is denied with 403 by rule `1000001`;
- JSONL decision metadata contains the connector and rule ID, not body payloads.

This is a narrow, partial runtime path. Request and response bodies are
advertised as unsupported and are never passed to the runtime. CRS, production
hardening, security verification, response-body handling, and full-matrix
verification are not claimed.

## Implemented path

The native module is in `module/mod_msconnector.c`. It provides:

- lighttpd plugin initialization, cleanup, and configuration registration;
- `handle_uri_clean` request-header processing;
- `handle_response_start` response-header processing;
- one Common runtime transaction per lighttpd request;
- Phase-1 block/error status mapping;
- transaction finish and storage cleanup in `handle_request_reset`.

`src/lighttpd_modsecurity_mapper.c` owns all lighttpd-specific mapping. Host
types do not enter `common/`. Mapped header arrays remain alive until request
reset because the Common runtime borrows request and response data for the
transaction lifetime.

## Configuration

The lighttpd host configuration has two server-scoped directives:

```lighttpd
server.modules += ( "mod_msconnector" )
msconnector.enabled = "enable"
msconnector.config-file = "/absolute/path/msconnector-runtime.conf"
```

The referenced Common runtime file uses `key=value` syntax. Supported values
include rule sources, transaction-ID settings, body policy and limits,
block/error statuses, event path, and header/resource limits. The native
Phase-1 module requires both body modes to be `none`; body payloads are not
supported by this module yet.

`config/lighttpd-native.conf` is a documented example; its two absolute
placeholder paths must be replaced. The native harness generates a runnable
configuration with managed absolute paths.

## Build and validation

Build, bridge self-test, config check, start smoke, and runtime smoke are
separate operations:

```sh
make -C connectors/lighttpd build-lighttpd-bridge
make -C connectors/lighttpd self-test-lighttpd-bridge
make -C connectors/lighttpd build-lighttpd-connector
make -C connectors/lighttpd check-lighttpd-config
make -C connectors/lighttpd start-smoke-lighttpd
make -C connectors/lighttpd runtime-smoke-lighttpd
```

The native build requires absolute `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR`, and `MODSECURITY_LIB_DIR` paths plus the generated
lighttpd `config.h` through `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR`, or
`LIGHTTPD_CONFIG_DIR`. Validation also requires `LIGHTTPD_BIN`.

`start-smoke-lighttpd` sends no requests. Only
`runtime-smoke-lighttpd` sends the baseline and blocking requests, so build,
self-test, process-start, and runtime evidence cannot be confused.

The older bridge starter and framework sidecar smoke remain available as
separate historical/alternative paths. Their self-tests are not native-host
runtime evidence.

## Claim boundaries

The current evidence supports only `minimal_runtime_smoke` / a
`partial_runtime_path` for request and response headers and a Phase-1 deny.
It does not establish:

- request-body or response-body inspection;
- response-body blocking or late-intervention behavior;
- CRS completeness or any CRS claim;
- production readiness, security verification, or full-matrix verification.
