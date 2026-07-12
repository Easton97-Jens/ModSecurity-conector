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
response bodies are not implemented and are never passed to the runtime. CRS,
production hardening, security verification, response-body handling, and
full-matrix verification are not claimed.

The full-lifecycle profile selects a separate, versioned lighttpd 1.4.84
patched-host target that copies, patches, configures, builds, installs, and
stages a matching core and module together.
`runtime-smoke-lighttpd-patched` performs an isolated patched-core/module load
and the same narrow Phase-1 200/403 smoke; it remains separate from the
generic stock No-CRS target and does not promote any capability. The patched binding still rejects
response-body inspection because its HTTP/1.x socket-stage queue can contain
transfer framing; HTTP/2 is deliberately excluded.

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
block/error statuses, event path, and header/resource limits. The stock
Phase-1 module requires both body modes to be `none`. The separate
patched build is selected by the full-lifecycle profile; its isolated host
smoke also uses both body modes as `none`, so it makes no request- or
response-body streaming promotion.

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

The current evidence supports only `minimal_runtime_smoke` / a
`partial_runtime_path` for request and response headers and a Phase-1 deny.
It does not establish:

- request-body or response-body inspection;
- response-body blocking or late-intervention behavior;
- CRS completeness or any CRS claim;
- production readiness, security verification, or full-matrix verification.

## Canonical Phase-4 boundary

The asserted native path has a response-start header hook but no verified
native response-body data path. It deliberately supplies no response-body data
to ModSecurity. The selected patched host's output/EOS hook is raw HTTP/1.x wire
output and is deliberately a no-op for response-body inspection; it is not a
decoded entity-body filter. `response_body_buffered`, `phase4`,
`phase4_rule_evaluation`, `phase4_pre_commit_deny`, `late_intervention`,
`late_intervention_log_only`, `late_intervention_abort`, and
`late_intervention_status_metadata` are therefore `not_implemented` in this
module.

This is an implementation boundary, not a statement that lighttpd can never
support response-body processing.  Phase-4 cases must remain `NOT_EXECUTED`
(or be omitted by capability selection) until a native response-body path is
implemented; they must not be called `UNSUPPORTED` without an architecture
proof.  There is consequently no Phase-4 original/requested/visible status
split, late action, or connection-abort evidence to report yet.

The existing Phase-1 header deny is separate evidence.  Events and reports
remain metadata-only and never include a response-body payload.
