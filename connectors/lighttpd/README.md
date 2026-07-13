# lighttpd Connector

**Language:** English | [Deutsch](README.de.md)

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

This is a narrow, partial runtime path. In the default stock build, request and
response bodies are not implemented and are never passed to the runtime. The
separate patched 1.4.84 pair has a source/build contract for borrowed HTTP/1.1
request ranges and identity response-entity ranges, but that contract is not a
response-body runtime proof. CRS, production hardening, security verification,
and full-matrix verification are not claimed.

The full-lifecycle profile selects a separate, versioned lighttpd 1.4.84
patched-host target that copies, patches, configures, builds, installs, and
stages a matching core and module together.
`runtime-smoke-lighttpd-patched` performs an isolated patched-core/module load
and the same narrow Phase-1 200/403 smoke; it remains separate from the
generic stock No-CRS target and does not promote any capability. The patched
ABI invokes its response callback in `http_chunk.c`, on the current borrowed
HTTP/1.1 entity range before transfer framing and before any socket write. The
selected configuration scope is identity only: HTTP/2 and gzip/br are excluded,
and no file/zero-copy or content-encoding route is asserted as an inspected
response path.

## Implemented path

The native module is in `module/mod_msconnector.c`. It provides:

- lighttpd plugin initialization, cleanup, and configuration registration;
- `handle_uri_clean` request-header processing;
- `handle_response_start` response-header processing;
- in the patched 1.4.84 ABI, synchronous borrowed request and identity
  entity-response callbacks with monotonic offsets and one response EOS;
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
block/error statuses, event path, and header/resource limits. The stock
Phase-1 module requires both body modes to be `none`. The separately selected
patched build accepts `none` or `streaming` for each body direction, but its
response streaming contract is restricted to HTTP/1.1 identity entity bytes.
The checked-in patched smoke still uses both modes as `none`; setting its
preparer to response streaming is a configuration/source-contract check, not a
Phase-4 promotion. `LIGHTTPD_PATCHED_ENTITY_ENCODING=gzip` or `br` is blocked
until the filter order and decompression behavior have real host evidence.

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

# Requires LIGHTTPD_SOURCE_DIR, MODSECURITY_INCLUDE_DIR and
# MODSECURITY_LIB_DIR.  This builds a copied 1.4.84 core and its module
# together below BUILD_ROOT/lighttpd-core-patched.
make -C connectors/lighttpd build-lighttpd-patched-host
make -C connectors/lighttpd check-lighttpd-patched-host
make -C connectors/lighttpd runtime-smoke-lighttpd-patched
```

The native build requires absolute `LIGHTTPD_SOURCE_DIR`,
`MODSECURITY_INCLUDE_DIR`, and `MODSECURITY_LIB_DIR` paths plus the generated
lighttpd `config.h` through `LIGHTTPD_BUILD_ROOT`, `LIGHTTPD_BUILD_DIR`, or
`LIGHTTPD_CONFIG_DIR`. Validation also requires `LIGHTTPD_BIN`.

`start-smoke-lighttpd` sends no requests. Only
`runtime-smoke-lighttpd` sends the baseline and blocking requests, so build,
self-test, process-start, and runtime evidence cannot be confused.

The patched target writes core and host manifests with the patch SHA-256,
binary/module paths, and artifact hashes. It refuses a stock binary/module
mix. The older bridge starter and framework sidecar smoke remain separate
historical/alternative paths. Their self-tests are not native-host runtime
evidence.

## Claim boundaries

The current runtime evidence supports only `minimal_runtime_smoke` / a
`partial_runtime_path` for request and response headers and a Phase-1 deny.
The patched-core compile and module-object checks establish a release-pinned
source/build contract, not a real response-body host run. It does not establish:

- a client-observed Phase-4 rule result or response-body enforcement;
- response-body blocking, late-intervention behavior, first-byte timing, or
  no-full-buffer client evidence;
- CRS completeness or any CRS claim;
- production readiness, security verification, or full-matrix verification.

## Canonical Phase-4 boundary

The stock native path has only a response-start header hook. The release-pinned
patched path adds a distinct HTTP/1.1 identity entity-body callback before
HTTP/1 transfer framing: application/backend output → selected identity entity
range → msconnector callback → HTTP/1 chunk framing (if selected) → socket.
It passes a borrowed pointer and length synchronously, tracks a monotonic
entity offset, and emits EOS at most once. Socket short writes and `EAGAIN`
occur later, so their retries cannot re-submit the entity range. This is
incremental body ingestion with end-of-stream Phase-4 evaluation; it is not a
claim that rules run per chunk.

The selected scope does not assert gzip/br, HTTP/2, or every file/zero-copy
output route. The current harness does not execute streaming P4 traffic, and
there is no real-client proof of a visible safe result, a precommit deny,
first-byte delivery, or a strict connection abort. The source path records a
safe/minimal disruptive outcome as `log_only`; strict deliberately logs
`NOT EXECUTED` and continues because no client-validated abort primitive has
been proven. Accordingly the checked-in Phase-4-related capability states
remain `not_implemented` for the selected evidence profile.

This is an evidence boundary, not a statement that lighttpd can never support
response-body processing. Phase-4 cases remain `NOT_EXECUTED` (or are omitted
by capability selection) until a real host run supplies the missing client and
transport artifacts; they must not be called `UNSUPPORTED` without an
architecture proof. There is consequently no client-verified Phase-4
original/requested/visible status split, late action, or connection-abort
evidence to report yet.

The existing Phase-1 header deny is separate evidence.  Events and reports
remain metadata-only and never include a response-body payload.
